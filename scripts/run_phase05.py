"""WP-5 phase runner for PHASEs 14-16: set-freeze -> clean-room freeze -> reveal-once
-> fresh evaluation -> agreement -> large-n -> OOD. Exit 0 iff a lawful WP-5
terminal is reached (SURVIVES_FINITE_TESTS or SET_REJECTED). Never evaluates
before reveal; never reveals twice; never regenerates the bank.

--resume continues lawfully after an interruption past STEP 137: it verifies the
completed artifacts on disk and resumes at STEP 138 (no re-freeze, no re-reveal).
"""
from __future__ import annotations
import datetime
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW
from solver import encode as E
from solver import search as S
from solver import promote as PM
from independent import config_exec as IX
from cleanroom import evaluator as CR
from cleanroom import batteries as CB

ART = ROOT / "artifacts" / "v04"
T0_WALL = time.time()
WALL_CAP = 7200


def step(sid: str, msg: str) -> None:
    print("[WP-5][STEP %s] %s" % (sid, msg), flush=True)


def run(cmd: list[str], label: str) -> int:
    step("RUN", "Executing %s" % label)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
    tail = r.stdout[-2000:] if len(r.stdout) > 2000 else r.stdout
    print(tail, end="")
    if r.returncode != 0:
        print((r.stderr or "")[-2000:], end="")
    step("RUN", "%s exit=%d" % (label, r.returncode))
    return r.returncode


def wall_left() -> float:
    return WALL_CAP - (time.time() - T0_WALL)


def w(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def utcnow() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main() -> int:
    RESUME = "--resume" in sys.argv
    # WP-5 STEP 132: entry recheck (WP-4 gate + firewall + freeze + contracts).
    step("132", "Rechecking WP-5 entry predicate (resume=%s)" % RESUME)
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    if not all(ps[k]["truth"] == "REVIEWED" for k in ps if k.startswith("LIQ0")):
        step("132", "LIQ0 REVIEWED gate failed; WP-5 blocked")
        return 2
    promo = json.loads((ART / "development" / "PROMOTED_SET_SURVIVES_DEV.json").read_text(
        encoding="utf-8"))
    if len(promo["promoted"]) < 1:
        step("132", "Empty promoted set; WP-5 blocked")
        return 2
    st = FW.read_state()
    want = "REVEALED_ONCE" if RESUME else "COMMITMENT_PUBLISHED"
    if st["state"] != want or st["unlocks"] != (1 if RESUME else 0):
        step("132", "Holdout firewall not in expected %s state; WP-5 blocked" % want)
        return 2
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "freeze") != 0:
        return 2
    if RESUME:
        # WP-5 STEP 132r: resume only over verified completed artifacts (no re-freeze).
        for p in [ART / "candidates" / "commit" / "set.json",
                  ART / "cleanroom" / "impl_freeze.json",
                  ART / "h4l_reveal" / "fresh_results.json",
                  ART / "h4l_reveal" / "eval_log.json",
                  ART / "cleanroom" / "agreement.json"]:
            if not p.exists():
                step("132r", "Resume artifact missing: %s" % p)
                return 2
        fresh = json.loads((ART / "h4l_reveal" / "fresh_results.json").read_text(encoding="utf-8"))
        survivors = [k for k, v in fresh.items() if v["violations"] == 0]
        step("132r", "Resume verified (set/impl/reveal/fresh/agreement on disk)")
    else:
        fresh, survivors = _freeze_reveal_evaluate_agree(promo)
        if fresh is None:
            return survivors  # _freeze... returns (None, exit_code) on block
    # Common state for STEP 138+.
    import zstandard  # noqa: F401 (ensures decompression backend present)
    man = json.loads((ART / "h4l_reveal" / "manifest.json").read_text(encoding="utf-8"))
    ce_dir = ART / "counterexamples"
    th_hash = hashlib.sha256((ROOT / "math" / "theorems" / "MSTL-14.md").read_bytes()).hexdigest()
    # WP-5 STEP 138: large-n + OOD on final survivors.
    step("138", "Large-n + OOD")
    large = CB.large_n()
    ood = CB.ood()
    w(ART / "large_n" / "id_registry.json", sorted(e["id"] for e in large))
    w(ART / "ood" / "id_registry.json", sorted(e["id"] for e in ood))
    ln_res, ood_res = {}, {}
    for key in survivors:
        P, k, C, rho_name = key.split("|")
        k, C, rho = int(k), int(C), S.rho_of(rho_name)
        lv = 0
        worst_ln = 0
        diag = None
        for ep in large:
            r_ = E.exec_counts(E.precompute(ep["n"], ep["T0"], ep["H"]), P, k, C, rho)
            if r_["violations"]:
                lv += 1
                worst_ln = max(worst_ln, max(kp["need"] - kp["paid"] for kp in r_["keeps"]))
                if diag is None:
                    diag = {"episode": ep["id"], "n": ep["n"], "keeps": r_["keeps"]}
                    _bundle(ce_dir, th_hash, P, k, C, rho, rho_name,
                            {"n": ep["n"], "T0": ep["T0"], "H": ep["H"],
                             "id": ep["id"], "battery": "large-n"}, r_)
        ln_res[key] = {"episodes": len(large), "violations": lv,
                       "worst_shortfall": worst_ln, "sample_diagnostic": diag}
        ov = 0
        worst_ood = 0
        for ep in ood:
            r_ = E.exec_counts(E.precompute(ep["n"], ep["T0"], ep["H"]), P, k, C, rho)
            if r_["violations"]:
                ov += 1
                worst_ood = max(worst_ood, max(kp["need"] - kp["paid"] for kp in r_["keeps"]))
                if ov == 1:
                    _bundle(ce_dir, th_hash, P, k, C, rho, rho_name,
                            {"n": ep["n"], "T0": ep["T0"], "H": ep["H"],
                             "id": ep["id"], "battery": "ood"}, r_)
        ood_res[key] = {"episodes": len(ood), "violations": ov,
                        "worst_shortfall": worst_ood, "label": "OOD (not fresh-holdout)"}
    w(ART / "large_n" / "large_n_results.json", ln_res)
    w(ART / "ood" / "ood_results.json", ood_res)
    step("138", "Large-n/OOD recorded")
    # WP-5 STEP 139: FRSH suite + mutants + regression.
    # NOTE: SYN-11 pinned WP-4's pre-reveal firewall state; WP-5's lawful reveal
    # supersedes it BY DESIGN (FRSH-03/09 verify exactly-once instead). Deselected
    # explicitly here — never silently; WP-4's 13/13 closeout record stands as history.
    step("139", "Final verification battery")
    if run([PY, "-m", "pytest", "tests/test_fresh_h4l.py", "-q"], "FRSH") != 0:
        return 2
    if run([PY, "-m", "pytest", "tests/test_synthesis.py", "-q", "--deselect",
            "tests/test_synthesis.py::test_syn_11_firewall_intact"], "SYN-regression") != 0:
        return 2
    if run([PY, "scripts/test_wp5_mutants.py"], "mutants") != 0:
        return 2
    if run([PY, "-m", "pytest", "tests/test_activation.py",
            "tests/test_legacy_embedding.py", "-q"], "regression") != 0:
        return 2
    gated = {k: {"large_n_violations": ln_res[k]["violations"],
                 "ood_violations": ood_res[k]["violations"]} for k in survivors}
    if survivors and all(g["large_n_violations"] == 0 and g["ood_violations"] == 0
                         for g in gated.values()):
        w(ART / "h4l_reveal" / "SURVIVES_FINITE_TESTS.json",
          {"survivors": survivors, "gates": gated,
           "ceiling": "finite survival only; no universality claimed"})
        step("140", "SURVIVES_FINITE_TESTS ceiling: %d" % len(survivors))
    else:
        w(ART / "h4l_reveal" / "PROMOTED_SET_REJECTED.json",
          {"stage": "fresh/large-n/ood", "gates": gated,
           "branchB_trigger": len(survivors) == 0})
        step("140", "Set-rejected at fresh gates (Branch-B trigger: %s)"
             % (len(survivors) == 0))
    return 0


def _freeze_reveal_evaluate_agree(promo):
    # WP-5 STEP 133a: freeze the promoted set + hash; advance to CANDIDATE_SET_FROZEN.
    step("133a", "Freezing candidate set")
    idents = []
    for key in sorted(promo["promoted"]):
        P, k, C, rho = key.split("|")
        ip = ART / "candidates" / "branchA" / PM.calculus_id(int(C)) / \
            key.replace("|", "__") / "identity.json"
        ident = json.loads(ip.read_text(encoding="utf-8"))
        idents.append({"key": key, "identity_hash": hashlib.sha256(
            json.dumps(ident, sort_keys=True).encode()).hexdigest()})
    set_rec = {"members": idents,
               "set_hash": hashlib.sha256(json.dumps(idents, sort_keys=True).encode()).hexdigest(),
               "order": "sorted-key (predetermined evaluation order)"}
    w(ART / "candidates" / "commit" / "set.json", set_rec)
    try:
        FW.transition("CANDIDATE_SET_FROZEN", "promoted set frozen %s" % set_rec["set_hash"][:16])
    except FW.FirewallError as e:
        step("133a", "Firewall refused set-freeze: %s" % e)
        return None, 2
    step("133a", "Set frozen: %d members hash=%s" % (len(idents), set_rec["set_hash"][:16]))
    # WP-5 STEP 133b: clean-room implementation freeze record (bytes committed pre-reveal).
    step("133b", "Clean-room implementation freeze check")
    ev_p = ROOT / "python" / "cleanroom" / "evaluator.py"
    r = subprocess.run(["git", "ls-files", "--error-unmatch", str(ev_p.relative_to(ROOT))],
                       capture_output=True, text=True, cwd=str(ROOT))
    d = subprocess.run(["git", "diff", "--quiet", "--", str(ev_p.relative_to(ROOT))],
                       capture_output=True, cwd=str(ROOT))
    if r.returncode != 0 or d.returncode != 0:
        step("133b", "Clean-room bytes not committed pre-reveal; WP-5 blocked")
        return None, 2
    import ast
    tree = ast.parse(ev_p.read_text(encoding="utf-8"))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
    if not mods <= {"__future__"}:
        step("133b", "Clean-room imports outside stdlib: %r" % (mods - {"__future__"}))
        return None, 2
    w(ART / "cleanroom" / "impl_freeze.json",
      {"sha256": hashlib.sha256(ev_p.read_bytes()).hexdigest(), "imports": sorted(mods)})
    step("133b", "Clean-room bytes frozen pre-reveal")
    # WP-5 STEP 135: reveal once.
    step("135", "Reveal-once")
    if run([PY, "scripts/reveal_h4l.py"], "reveal") != 0:
        step("135", "Reveal refused; WP-5 blocked")
        return None, 2
    reveal_utc = utcnow()
    eval_log = {"reveal_utc": reveal_utc, "evaluations_before_reveal": 0,
                "first_eval_utc": None, "last_eval_utc": None}
    # WP-5 STEP 136: fresh evaluation in predetermined order until exhausted.
    step("136", "Fresh H4L evaluation (sorted-key order, exhaustive)")
    import zstandard
    rev = ART / "h4l_reveal"
    man = json.loads((rev / "manifest.json").read_text(encoding="utf-8"))
    ce_dir = ART / "counterexamples"
    th_hash = hashlib.sha256((ROOT / "math" / "theorems" / "MSTL-14.md").read_bytes()).hexdigest()
    fresh, survivors = {}, []
    for key in sorted(promo["promoted"]):
        P, k, C, rho_name = key.split("|")
        k, C, rho = int(k), int(C), S.rho_of(rho_name)
        viol = worst = evaluated = 0
        first = None
        first_eval_marked = False
        for sh in sorted(man["shards"], key=lambda s: s["name"]):
            dctx = zstandard.ZstdDecompressor()
            raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
            for line in raw.decode("utf-8").splitlines():
                ep = json.loads(line)
                n, T0, H = ep["size"], ep["T0"], ep["H"]
                if not first_eval_marked:
                    eval_log["first_eval_utc"] = utcnow()
                    first_eval_marked = True
                res = E.exec_counts(E.precompute(n, T0, H), P, k, C, rho)
                evaluated += 1
                if res["violations"]:
                    viol += res["violations"]
                    worst = max(worst, max(kp["need"] - kp["paid"] for kp in res["keeps"]))
                    if first is None:
                        first = {"episode": ep["hash"], "keeps": res["keeps"]}
                        _bundle(ce_dir, th_hash, P, k, C, rho, rho_name, ep, res)
                    break
            if viol:
                break
            if wall_left() < 600:
                w(ART / "h4l_reveal" / "RESOURCE_LIMIT_NO_CLAIM.json",
                  {"candidate": key, "evaluated": evaluated})
                step("136", "Resource cap; RESOURCE_LIMIT_NO_CLAIM recorded")
                return None, 3
        fresh[key] = {"evaluated": evaluated, "violations": viol,
                      "worst_shortfall": worst, "exhausted": viol == 0,
                      "first_violation": first}
        if viol == 0:
            survivors.append(key)
        eval_log["last_eval_utc"] = utcnow()
    w(ART / "h4l_reveal" / "fresh_results.json", fresh)
    w(ART / "h4l_reveal" / "eval_log.json", eval_log)
    step("136", "Fresh survivors: %d/%d" % (len(survivors), len(fresh)))
    # WP-5 STEP 137: clean-room agreement (full bank, all evaluated candidates).
    step("137", "Clean-room agreement")
    agree = {}
    for key in sorted(fresh):
        P, k, C, rho_name = key.split("|")
        k, C, rho = int(k), int(C), S.rho_of(rho_name)
        match = mismatch = 0
        for sh in sorted(man["shards"], key=lambda s: s["name"]):
            dctx = zstandard.ZstdDecompressor()
            raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
            for line in raw.decode("utf-8").splitlines():
                ep = json.loads(line)
                n, T0, H = ep["size"], ep["T0"], ep["H"]
                a = E.exec_counts(E.precompute(n, T0, H), P, k, C, rho)["keeps"]
                b = CR.execute(n, T0, H, P, k, C, rho)["keeps"]
                if [(k_["need"], k_["paid"]) for k_ in a] == [(k_["need"], k_["paid"]) for k_ in b]:
                    match += 1
                else:
                    mismatch += 1
                    break
            if mismatch:
                break
        agree[key] = {"episodes_compared": match, "mismatches": mismatch}
    w(ART / "cleanroom" / "agreement.json", agree)
    if any(v["mismatches"] for v in agree.values()):
        step("137", "Clean-room disagreement; WP-5 blocked")
        return None, 2
    step("137", "Agreement: full-bank per-KEEP equality on all evaluated")
    return fresh, survivors


def _bundle(ce_dir, th_hash, P, k, C, rho, rho_name, ep, res):
    ind = IX.replay(ep["n"], ep["T0"], ep["H"], P, k, C, rho)
    assert [k_["need"] for k_ in res["keeps"]] == [k_["need"] for k_ in ind["keeps"]] \
        and [k_["paid"] for k_ in res["keeps"]] == [k_["paid"] for k_ in ind["keeps"]], \
        "independent replay disagreement"
    Hmin, certm = PM.minimize_history(
        lambda n, T0, H: E.exec_full(n, T0, H, P, k, C, rho), ep["n"], ep["T0"], ep["H"])
    level = "L1" if Hmin != [list(s) for s in ep["H"]] else "L0"
    # WP-5 bundle integrity: the stored bundle is recomputed ON the minimized
    # episode, so the record reproduces byte-for-byte from its own fields.
    res_min = E.exec_full(ep["n"], ep["T0"], Hmin, P, k, C, rho)
    ind_min = IX.replay(ep["n"], ep["T0"], Hmin, P, k, C, rho)
    assert [k_["need"] for k_ in res_min["keeps"]] == [k_["need"] for k_ in ind_min["keeps"]] \
        and [k_["paid"] for k_ in res_min["keeps"]] == [k_["paid"] for k_ in ind_min["keeps"]]
    assert res_min["violations"] > 0, "minimization lost the violation"
    PM.append_counterexample(
        ce_dir, th_hash, PM.calculus_id(C),
        {"n": ep["n"], "T0": ep["T0"], "H": Hmin, "id": ep.get("id"),
         "battery": ep.get("battery", "h4l-reveal")},
        {"keeps": res_min["keeps"], "violations": res_min["violations"]},
        {"keeps": ind_min["keeps"], "violations": ind_min["violations"]},
        level, "%s fresh: %s" % (level, certm),
        {"predicate": P, "k": k, "C": C, "rho": rho_name})
    print("[WP-5][STEP 136] Violation bundle appended (%s)" % level, flush=True)


if __name__ == "__main__":
    sys.exit(main())
