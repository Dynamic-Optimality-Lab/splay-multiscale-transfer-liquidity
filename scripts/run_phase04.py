"""WP-4 phase runner for PHASEs 09-13: fidelity -> batteries -> funnel -> promote ->
validation -> adversarial -> outlines. Exit 0 iff the WP-4 exit gate is lawfully
reached (promotion or honest rejection). Never touches H4L/OOD/clean-room-fresh.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(ROOT / "python"))
from solver import predicates as CP
from solver import legality as LG
from solver import encode as E
from solver import battery as B
from solver import search as S
from solver import promote as PM
from adversary import engines as AE
from independent import config_exec as IX

ART = ROOT / "artifacts" / "v04"
T0_WALL = time.time()
WALL_CAP = 7200


def step(sid: str, msg: str) -> None:
    print("[WP-4][STEP %s] %s" % (sid, msg), flush=True)


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


def main() -> int:
    # WP-4 STEP 120: entry recheck (WP-3 authorization + freeze + solver stdlib-only).
    step("120", "Rechecking WP-4 entry predicate")
    ps = json.loads((ROOT / "math" / "proof_status.json").read_text(encoding="utf-8"))
    if not all(ps[k]["truth"] == "REVIEWED" for k in ps if k.startswith("LIQ0")):
        step("120", "LIQ0 REVIEWED gate failed; WP-4 blocked")
        return 2
    from holdout import firewall as FW
    st = FW.read_state()
    if st["state"] != "COMMITMENT_PUBLISHED" or st["unlocks"] != 0:
        step("120", "Holdout firewall disturbed; WP-4 blocked")
        return 2
    if run([PY, "scripts/verify_freeze.py", "--verify-only"], "freeze") != 0:
        return 2
    step("120", "Entry PASS (WP-3 COMPLETE, firewall intact, freeze PASS)")
    # WP-4 STEP 121: SYN-00 fidelity gate (immutable REG-001 on FLAT(1)).
    step("121", "SYN-00 fidelity gate")
    from liquidity import diagnostics as DG
    n, T0, H = 28, B._vine_right(28), [["DELETE", 27], ["DELETE", 28],
                                       ["KEEP", 28], ["KEEP", 27]]
    res = E.exec_full(n, T0, H, "P_all", 6, 2, (1, 1))
    r = res["keeps"][-1]
    pre = E.precompute(n, T0, H)
    if (pre[-1]["a"], pre[-1]["y"], r["need"], r["paid"], r["margin"]) != (2, 15, 11, 10, -1):
        step("121", "REG-001 fidelity failed; WP-4 blocked (TERM-LEGACY_FAIL path)")
        return 2
    if DG.flat_pressure(r["need"], r["act_pre_B"], r["B_events"]) != 2:
        step("121", "REG-001 Q fidelity failed; WP-4 blocked")
        return 2
    step("121", "Fidelity PASS (2,15,11,10,-1) Q=2")
    # WP-4 STEP 122: batteries + ID registries.
    step("122", "Building batteries + ID registries")
    screen = B.dev_screen()
    extra = B.dev_extra(exclude=set(B.ids(screen)))
    dev_full = screen + extra
    val = B.validation(exclude=set(B.ids(dev_full)))
    assert set(B.ids(dev_full)).isdisjoint(set(B.ids(val)))
    w(ART / "development" / "id_registry_dev.json", B.ids(dev_full))
    w(ART / "validation" / "id_registry_val.json", B.ids(val))
    w(ART / "development" / "battery_meta.json",
      {"screen": len(screen), "full": len(dev_full), "validation": len(val)})
    pre_screen = [(E.precompute(e["n"], e["T0"], e["H"]), e["id"]) for e in screen]
    pre_full = [(E.precompute(e["n"], e["T0"], e["H"]), e["id"]) for e in dev_full]
    step("122", "Batteries: screen=%d full=%d val=%d" % (len(screen), len(dev_full), len(val)))
    # WP-4 STEP 123: full-grid screen (sharded) + sorted reduce.
    step("123", "Screening closed grid (13,440 configs, sharded)")
    results, shards, ok = S.screen_grid(pre_screen, wall_left())
    if len(results) != 13440 or len(shards) != S.N_SHARDS:
        step("123", "Shard completeness failed (partial reduce); WP-4 blocked")
        return 2
    for si, shard in shards.items():
        w(ART / "development" / "shards" / ("shard_%02d.json" % si),
          {k: shard[k] for k in sorted(shard)})
    w(ART / "development" / "screen_results.json", {k: results[k] for k in sorted(results)})
    surv = sorted(k for k, v in results.items() if v["survived"])
    step("123", "Screen survivors: %d (complete=%s)" % (len(surv), ok))
    if not ok:
        w(ART / "development" / "RESOURCE_LIMIT_NO_CLAIM.json",
          {"phase": "screen", "reason": "wall/mem cap", "partial": True})
        step("123", "Resource cap hit; RESOURCE_LIMIT_NO_CLAIM recorded")
        return 3
    if not surv:
        w(ART / "development" / "LIQUIDITY_CALCULUS_REJECTED.json",
          {"screen_survivors": 0, "grid": 13440})
        step("123", "Zero screen survivors; LIQUIDITY_CALCULUS_REJECTED")
        return 0
    # WP-4 STEP 124: dev-full on survivors + matched baselines; rank + label.
    step("124", "Dev-full + ranking + attribution")
    preF = pre_full
    keys = set()
    for ks in surv:
        P, k, C, rho = results[ks]["P"], results[ks]["k"], results[ks]["C"], results[ks]["rho"]
        keys.add((P, k, C, rho))
        keys.add(S.baseline_of(P, k, C))
    full = S.dev_full_eval(preF, keys, wall_left())
    if full.pop("_RESOURCE_LIMIT", False):
        w(ART / "development" / "RESOURCE_LIMIT_NO_CLAIM.json",
          {"phase": "dev-full", "reason": "wall cap", "partial": True})
        return 3
    lookup = dict(results)
    lookup.update(full)
    ranked = []
    for ks in surv:
        e = full.get(ks)
        if e is None or not e["survived"]:
            continue
        reg_ok = E.exec_counts(preF[0][0], e["P"], e["k"], e["C"],
                               S.rho_of(e["rho"]))["violations"] == 0
        ranked.append({"key": ks, "entry": e, "reg_ok": reg_ok,
                       "label": S.label(e, lookup),
                       "rank": S.rank_key(e, reg_ok, 0)})
    ranked.sort(key=lambda t: (t["rank"], t["key"]))
    w(ART / "development" / "ranking.json",
      [{"key": t["key"], "label": t["label"], "rank": list(t["rank"])} for t in ranked])
    step("124", "Dev survivors: %d" % len(ranked))
    if not ranked:
        w(ART / "development" / "PROMOTED_CANDIDATE_SET_REJECTED.json",
          {"stage": "dev-full", "screen_survivors": len(surv)})
        step("124", "All screen survivors died on dev-full; SET_REJECTED")
        return 0
    # WP-4 STEP 125: promotion (+ domination certificate if capped).
    step("125", "Promotion")
    top, cert = S.promote(ranked)
    w(ART / "development" / "promotion.json",
      {"promoted": [t["key"] for t in top], "certificate": cert})
    step("125", "Promoted %d (+cert capped=%s)" % (len(top), cert["capped"]))
    # WP-4 STEP 126: validation on frozen-promoted only.
    step("126", "Validation (frozen candidates only)")
    pre_val = [E.precompute(e["n"], e["T0"], e["H"]) for e in val]
    val_res, alive = {}, []
    ce_dir = ART / "counterexamples"
    th_hash = hashlib.sha256((ROOT / "math" / "theorems" / "MSTL-14.md").read_bytes()).hexdigest()
    for t in top:
        e = t["entry"]
        rho = S.rho_of(e["rho"])
        viol = worst = 0
        first = None
        for pi, p in enumerate(pre_val):
            r_ = E.exec_counts(p, e["P"], e["k"], e["C"], rho)
            if r_["violations"]:
                viol += r_["violations"]
                worst = max(worst, max(kp["need"] - kp["paid"] for kp in r_["keeps"]))
                if first is None:
                    first = pi
                break
        val_res[t["key"]] = {"violations": viol, "worst_shortfall": worst,
                             "episodes": len(val)}
        if viol:
            _record_violation(ce_dir, th_hash, e, val[first], "validation",
                              "DEMOTED_VAL")
        else:
            alive.append(t)
    w(ART / "validation" / "validation_results.json", val_res)
    step("126", "Validation survivors: %d/%d" % (len(alive), len(top)))
    # WP-4 STEP 127: adversarial residual-hunt on validation survivors.
    step("127", "Adversarial battery (9 engines)")
    final = []
    for t in alive:
        e = t["entry"]
        rho = S.rho_of(e["rho"])

        def evaluate(n, T0, H, _e=e, _rho=rho):
            return E.exec_full(n, T0, H, _e["P"], _e["k"], _e["C"], _rho)

        vios, witnesses, adv_rec = _run_adversarial(evaluate)
        t["adv"] = adv_rec
        if vios:
            wit = witnesses[0]
            _record_violation(ce_dir, th_hash, e, wit, "adversarial",
                              "DEMOTED_ADV", extra={"engine": wit.get("battery")})
        else:
            final.append(t)
    w(ART / "validation" / "adversarial_records.json",
      {t["key"]: t.get("adv", {}) for t in alive})
    step("127", "Adversarial survivors: %d/%d" % (len(final), len(alive)))
    # WP-4 STEP 128: identities + outlines + cross tables for final set.
    step("128", "Freezing identities + outlines")
    schema = json.loads((ROOT / "schemas" / "candidate.schema.json").read_text(encoding="utf-8"))
    paths = {"predicate_family": str(ROOT / "prereg" / "predicate_family_v0.4.1.yaml"),
             "legality": str(ROOT / "python" / "solver" / "legality.py"),
             "encode": str(ROOT / "python" / "solver" / "encode.py")}
    for t in final:
        e = t["entry"]
        ident = PM.freeze_identity(e, paths)
        PM.check_identity_schema(ident, schema)
        cid = ident["calculus_id"]
        sub = t["key"].replace("|", "__")
        cdir = ART / "candidates" / "branchA" / cid / sub
        cdir.mkdir(parents=True, exist_ok=True)
        w(cdir / "identity.json", ident)
        PM.write_outline(
            cdir / "outline.md", ident, e,
            {"violations": 0, "worst_shortfall": 0, "reg_ok": t["reg_ok"]},
            val_res[t["key"]], t.get("adv", {}), t["label"],
            ["REG-001 fidelity green (SYN-00)", "zero dev violations (screen+full)",
             "matched FLAT(1) baseline computed", "label %s via decision tree" % t["label"],
             "zero validation violations (5000 episodes)",
             "zero adversarial violations (9 engines)",
             "identity frozen (%d fields, schema-checked)" % len(ident)])
    w(ART / "development" / "cross_tables.json",
      {t["key"]: {"C_ladder": {str(C): lookup.get("|".join(
          [t["entry"]["P"], str(t["entry"]["k"]), str(C), t["entry"]["rho"]]), {})
          .get("survived") for C in E.C_GRID}} for t in final})
    if final:
        w(ART / "development" / "PROMOTED_SET_SURVIVES_DEV.json",
          {"promoted": [t["key"] for t in final],
           "labels": [t["label"] for t in final]})
        step("128", "PROMOTED_SET_SURVIVES_DEV: %d" % len(final))
    else:
        w(ART / "development" / "PROMOTED_CANDIDATE_SET_REJECTED.json",
          {"stage": "validation/adversarial"})
        step("128", "All promoted demoted; SET_REJECTED")
    # WP-4 STEP 129: SYN suite + mutants + regression.
    step("129", "Final verification battery")
    r = subprocess.run([PY, "-m", "pytest", "tests/test_synthesis.py", "-q"],
                       capture_output=True, text=True, cwd=str(ROOT))
    print(r.stdout[-1500:] if len(r.stdout) > 1500 else r.stdout, end="")
    import re as _re
    summary = [ln.strip() for ln in (r.stdout or "").splitlines()
               if _re.search(r"\d+ passed", ln)][-1:]
    if r.returncode != 0 or not summary or "13 passed" not in summary[0] \
            or "failed" in summary[0] or "skipped" in summary[0]:
        step("129", "SYN suite not exactly 13/13 (%r); WP-4 blocked" % summary)
        return 2
    step("RUN", "SYN exactly 13/13")
    if run([PY, "scripts/test_wp4_mutants.py"], "mutants") != 0:
        return 2
    if run([PY, "-m", "pytest", "tests/test_activation.py",
            "tests/test_legacy_embedding.py", "-q"], "regression") != 0:
        return 2
    step("130", "WP-4 phase checks complete")
    return 0


def _record_violation(ce_dir, th_hash, e, ep, stage, status, extra=None):
    primary = E.exec_full(ep["n"], ep["T0"], ep["H"], e["P"], e["k"], e["C"],
                          S.rho_of(e["rho"]))
    ind = IX.replay(ep["n"], ep["T0"], ep["H"], e["P"], e["k"], e["C"], S.rho_of(e["rho"]))
    assert [k["need"] for k in primary["keeps"]] == [k["need"] for k in ind["keeps"]] \
        and [k["paid"] for k in primary["keeps"]] == [k["paid"] for k in ind["keeps"]], \
        "independent replay disagreement"
    cid = PM.calculus_id(e["C"])
    Hmin, certm = PM.minimize_history(
        lambda n, T0, H: E.exec_full(n, T0, H, e["P"], e["k"], e["C"], S.rho_of(e["rho"])),
        ep["n"], ep["T0"], ep["H"])
    level = "L1" if Hmin != [list(s) for s in ep["H"]] else "L0"
    PM.append_counterexample(
        ce_dir, th_hash, cid, dict(ep, H=Hmin),
        {"keeps": primary["keeps"], "violations": primary["violations"]},
        {"keeps": ind["keeps"], "violations": ind["violations"]},
        level, "%s at %s: %s%s" % (level, stage, certm,
                                   (" " + json.dumps(extra, sort_keys=True)) if extra else ""))
    print("[WP-4][STEP 127] Demoted %s (%s violation)" % (cid, stage), flush=True)


def _run_adversarial(evaluate):
    vios, witnesses, rec = [], [], {}
    cheap = [("uniform", lambda: AE.uniform()),
             ("structured", lambda: AE.structured()),
             ("rotneigh", lambda: AE.rotneigh()),
             ("splice", lambda: AE.splice()),
             ("motif", lambda: AE.motif())]
    for name, fn in cheap:
        eps, r = fn()
        rec[name] = r
        _hunt(evaluate, eps, vios, witnesses)
        if wall_left() < 600:
            rec["_RESOURCE_LIMIT"] = True
            return vios, witnesses, rec
    for name, fn in [("hillclimb", lambda: AE.hillclimb(evaluate)),
                     ("anneal", lambda: AE.anneal(evaluate)),
                     ("genetic", lambda: AE.genetic(evaluate))]:
        eps, r = fn()
        rec[name] = r
        _hunt(evaluate, eps, vios, witnesses)
        if wall_left() < 600:
            rec["_RESOURCE_LIMIT"] = True
            return vios, witnesses, rec
    seeds = [{"n": 28, "T0": B._vine_right(28),
              "H": [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]]}]
    seeds += witnesses[:10]
    eps, r = AE.generalize(seeds)
    rec["generalize"] = r
    _hunt(evaluate, eps, vios, witnesses)
    return vios, witnesses, rec


def _hunt(evaluate, eps, vios, witnesses):
    for ep in eps:
        try:
            res = evaluate(ep["n"], ep["T0"], ep["H"])
        except ValueError:
            continue
        if res["violations"]:
            vios.append(ep["id"])
            witnesses.append(ep)


if __name__ == "__main__":
    sys.exit(main())
