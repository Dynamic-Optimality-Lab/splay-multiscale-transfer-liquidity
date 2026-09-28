"""WP-5X-K6C2 specialized runner: fixed k=6, C=2 slice of the frozen WP-5X pipeline.

Reuses the EXACT frozen WP-5X scientific semantics by importing
python/wp5x/{population,factored,stages,worker,gates} and
python/{solver,cleanroom,independent} bytes. No semantic duplication:
all evaluation goes through W.run_unit / G.finalize_kills /
ST.confirm_kill / ST.trace_pools / ST.classify / F.canonical_trace.

Output namespace ONLY: artifacts/v04/wp5x_k6c2/.
NEVER writes into artifacts/v04/wp5x/ (read-only history).
H4L is consumed ONLY from the published reveal (labeled REVEALED replay).
No dynamic P. No H5. No universality claims.

Stages:
  k0 : population freeze (k==6, C==2, WP-4 eligible, no cap, no promoted filter)
  k1 : known-counterexample regression (REG-001 + every preserved ce episode)
  k2 : revealed-H4L exhaustive replay (70k, resumable shards)
  k3 : clean-room agreement (full bank, every K2 survivor, fail-closed)
  k4 : large-n battery (360, unchanged)
  k5 : OOD battery (8000, unchanged, includes n192 killer)
  k6 : survivor freeze + phase diagram (report only, finite evidence)
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from wp5x import population as POP
from wp5x import factored as F
from wp5x import stages as ST

ART = ROOT / "artifacts" / "v04"
X_MAIN = ART / "wp5x"
X = ART / "wp5x_k6c2"
DEV = ART / "development"
CE_DIR = ART / "counterexamples"

K_FIXED = 6
C_FIXED = 2
BRANCH_REQUIRED = "wp5x-k6c2-specialized"


def step(sid: str, msg: str) -> None:
    print("[WP-5X-K6C2][STEP %s] %s" % (sid, msg), flush=True)


def w(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")
    tmp.replace(p)


def sha_bytes(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha_json(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def code_hashes() -> dict:
    return {"encode": sha_bytes(ROOT / "python" / "solver" / "encode.py"),
            "cleanroom": sha_bytes(ROOT / "python" / "cleanroom" / "evaluator.py"),
            "independent": sha_bytes(ROOT / "python" / "independent" / "config_exec.py"),
            "predicates": sha_bytes(ROOT / "python" / "solver" / "predicates.py")}


def assert_branch() -> None:
    try:
        b = subprocess.check_output(["git", "branch", "--show-current"],
                                    cwd=str(ROOT), text=True).strip()
    except Exception as e:
        raise ValueError("branch guard: cannot determine branch: %r" % (e,))
    if b != BRANCH_REQUIRED:
        raise ValueError("branch guard FAIL: current=%r required=%r" % (b, BRANCH_REQUIRED))


def check_code_frozen() -> None:
    rec = json.loads((X / "k0_population.json").read_text(encoding="utf-8"))
    if code_hashes() != rec["code_hashes"]:
        raise ValueError("code bytes changed mid-run; STOP FAIL-CLOSED")


def load_population():
    rec = json.loads((X / "k0_population.json").read_text(encoding="utf-8"))
    for m in rec["members"]:
        P, k, C, rho = m["key"].split("|")
        if int(k) != K_FIXED or int(C) != C_FIXED:
            raise ValueError("population drift: admitted k!=6 or C!=2: %s" % m["key"])
    return rec


def load_cfg():
    from solver import search as S
    rec = load_population()
    cfg = {}
    for m in rec["members"]:
        P, k, C, rho = m["key"].split("|")
        cfg[m["key"]] = (P, int(k), int(C), tuple(S.rho_of(rho)))
    return rec, cfg


def cmd_k0():
    import yaml
    assert_branch()
    step("K0", "Freezing k=6,C=2 eligible population from frozen WP-4")
    elig_all = POP.load_eligible(DEV)
    filt = [e for e in elig_all if e["k"] == K_FIXED and e["C"] == C_FIXED]
    if not filt:
        raise ValueError("empty k6c2 slice; STOP FAIL-CLOSED")
    # Assertions: every candidate has k==6, C==2, existed before, WP-4 eligible.
    rk = json.loads((DEV / "ranking.json").read_text(encoding="utf-8"))
    rk_by_key = {t["key"]: t for t in rk}
    res = json.loads((DEV / "screen_results.json").read_text(encoding="utf-8"))
    for e in filt:
        if e["k"] != 6 or e["C"] != 2:
            raise ValueError("admitted k!=6 or C!=2: %s" % e["key"])
        src = rk_by_key.get(e["key"])
        if src is None:
            raise ValueError("candidate did not exist before experiment: %s" % e["key"])
        if src["rank"][0] != 0:
            raise ValueError("candidate not WP-4 eligible (dev violations): %s" % e["key"])
        s = res.get(e["key"])
        if s is None or not s["survived"]:
            raise ValueError("candidate not WP-4 eligible (screen): %s" % e["key"])
        # No promoted-only filtering, no rank<=3, no cap: verify we did not filter on those.
        # (filt derived purely by k==6 and C==2 from the full eligible set.)
    # Guard against promoted-filter / top-N mutants: the slice must equal the
    # exact k==6,C==2 subset of the eligible set (no more, no fewer).
    expect_keys = sorted([e["key"] for e in elig_all if e["k"] == 6 and e["C"] == 2])
    got_keys = sorted([e["key"] for e in filt])
    if got_keys != expect_keys:
        raise ValueError("slice != exact k6c2 eligible subset; STOP FAIL-CLOSED")
    # Freeze identities with the same binding as WP-5X (30-field schema).
    pred = {p["id"]: p["hash"] for p in yaml.safe_load(
        open(ROOT / "prereg" / "predicate_family_v0.4.1.yaml").read())["predicates"]}
    filt = POP.freeze_identities(filt, pred, X)
    import json as _j
    schema = _j.loads(open(ROOT / "schemas" / "candidate.schema.json").read())
    for e in filt:
        if set(e["identity"]) != set(schema["required"]):
            raise ValueError("identity schema fail: %s" % e["key"])
        if e["identity"]["k"] != 6 or e["identity"]["C"] != 2:
            raise ValueError("identity k/C drift: %s" % e["key"])
    filt_sorted = sorted(filt, key=lambda e: e["key"])
    rec = {"slice": "k=6,C=2", "k": 6, "C": 2,
           "count": len(filt_sorted),
           "population_hash": POP.population_hash(filt_sorted),
           "code_hashes": code_hashes(),
           "source_hashes": {
               "ranking.json": sha_bytes(DEV / "ranking.json"),
               "screen_results.json": sha_bytes(DEV / "screen_results.json"),
               "promotion.json": sha_bytes(DEV / "promotion.json"),
               "predicate_family_v0.4.1.yaml": sha_bytes(
                   ROOT / "prereg" / "predicate_family_v0.4.1.yaml"),
               "x0_population_main": sha_bytes(X_MAIN / "x0_population.json"),
           },
           "members": [{"key": e["key"], "P": e["P"], "k": e["k"], "C": e["C"],
                        "rho": e["rho"], "label": e["label"], "rank": e["rank"],
                        "identity_hash": e["identity_hash"]} for e in filt_sorted]}
    w(X / "k0_population.json", rec)
    with open(X / "k0_identities.jsonl", "w", encoding="utf-8") as f:
        for e in filt_sorted:
            f.write(_j.dumps({"key": e["key"], "identity": e["identity"]},
                             sort_keys=True) + "\n")
    step("K0", "Frozen %d k6c2 identities hash=%s" % (len(filt_sorted), rec["population_hash"][:16]))


def known_witness_episodes():
    """K1 episodes: REG-001 first-class + every preserved counterexample episode.

    Returns (eps, by_id) with eps=[(eid,n,T0,H)], by_id={eid: {n,T0,H,battery,...}}.
    Order: n192 witness(es) first, then REG-001 (mirrors WP-5X X1 ordering
    convention of known killers first), then any further distinct preserved
    episodes sorted by id for determinism.
    """
    ces = sorted(CE_DIR.glob("ce_*.json"))
    if not ces:
        raise ValueError("no preserved counterexamples; STOP FAIL-CLOSED")
    by_id: dict = {}
    for p in ces:
        ce = json.loads(p.read_text(encoding="utf-8"))
        ep = ce["episode"]
        eid = ep.get("id", p.stem)
        if eid not in by_id:
            by_id[eid] = {"n": ep["n"], "T0": ep["T0"], "H": ep["H"],
                          "battery": ep.get("battery", "counterexample"),
                          "source": p.name,
                          "config": ce.get("config", {})}
    # Required: n192 OOD wealth witness present.
    n192_ids = [eid for eid, e in by_id.items() if e["n"] == 192]
    if not n192_ids:
        raise ValueError("n192 witness missing from preserved counterexamples")

    def vine(n):
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t

    reg = {"n": 28, "T0": vine(28),
           "H": [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]],
           "battery": "x1-REG-001", "source": "REG-001-constructed"}
    if "REG-001" in by_id:
        raise ValueError("REG-001 id collision with preserved bundle")
    by_id["REG-001"] = reg
    # Order: n192 first (sorted), then REG-001, then remaining sorted.
    n192_sorted = sorted(n192_ids)
    rest = sorted([eid for eid in by_id if eid not in n192_sorted and eid != "REG-001"])
    order = n192_sorted + ["REG-001"] + rest
    eps = [(eid, by_id[eid]["n"], by_id[eid]["T0"], by_id[eid]["H"]) for eid in order]
    return eps, by_id


def enrich_kills(res, by_id, cfg_map, stage, battery):
    """Same as wp5x.gates.finalize_kills plus full first-kill certificate fields."""
    from wp5x import gates as G
    from solver import encode as E
    live, kills = G.finalize_kills(res, by_id, cfg_map, stage, battery)
    # Enrich each kill with the exact first-kill certificate required by K1:
    # candidate ID, episode ID, n, T0, H, mode, rotation/StepEv class, a, y,
    # need, paid, margin, LATENT/ACTIVE pre/post, creation, activation,
    # discharge, ledger state.
    for key, k in kills.items():
        ep = by_id[k["kill_ep"]]
        pre = E.precompute(ep["n"], ep["T0"], ep["H"])
        # keeps[idx] corresponds to pre-access order filtered to KEEP? No:
        # exec_counts keeps list is per-KEEP in access order; find the
        # killing KEEP access record.
        kill_keep = None
        for kp in k["keeps"]:
            if kp["paid"] < kp["need"]:
                kill_keep = kp
                break
        if kill_keep is None:
            raise ValueError("kill without paid<need: %s" % key)
        acc = pre[kill_keep["idx"]]
        pool = None
        for pr in k["pools"]:
            if pr.get("x") == acc["x"] and pr.get("a") == acc["a"] and pr.get("y") == acc["y"]:
                # pools list is per-KEEP in order; match by need/paid too
                if pr.get("need") == kill_keep["need"] and pr.get("paid") == kill_keep["paid"]:
                    pool = pr
                    break
        k["certificate"] = {
            "candidate": key, "episode": k["kill_ep"],
            "n": ep["n"], "T0": ep["T0"], "H": ep["H"],
            "battery": ep.get("battery", battery), "source": ep.get("source", ""),
            "mode": acc["mode"], "x": acc["x"], "a": acc["a"], "y": acc["y"],
            "Aev": acc["Aev"], "Bev": acc["Bev"], "sites": acc["sites"],
            "need": kill_keep["need"], "paid": kill_keep["paid"],
            "margin": kill_keep.get("margin"),
            "pool": pool,
        }
        k["episode_n"] = ep["n"]
    return live, kills


def cmd_k1():
    from wp5x import gates as G
    assert_branch()
    step("K1", "Known-counterexample regression (n192 first, then REG-001, then rest)")
    check_code_frozen()
    rec, cfg = load_cfg()
    live = [m["key"] for m in rec["members"]]
    eps, by_id = known_witness_episodes()
    # Verify required witnesses present.
    if "REG-001" not in by_id:
        raise ValueError("REG-001 missing; STOP FAIL-CLOSED")
    res = G.run_unit_episodes(eps, live, cfg)
    live_out, kills = enrich_kills(res, by_id, cfg, "K1", "known-regression")
    w(X / "kills_k1.json", kills)
    w(X / "live_k1.json", {"live": sorted(live_out), "count": len(live_out)})
    step("K1", "Killed %d on known witnesses; live %d/%d" % (len(kills), len(live_out), len(live)))


def h4l_shards():
    import zstandard
    rev = ART / "h4l_reveal"
    man = json.loads((rev / "manifest.json").read_text(encoding="utf-8"))
    dctx = zstandard.ZstdDecompressor()
    out = []
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        eps = []
        for line in raw.decode().splitlines():
            ep = json.loads(line)
            eps.append((ep["hash"], ep["size"], ep["T0"], ep["H"]))
        out.append((sh["name"], eps))
    total = sum(len(eps) for _, eps in out)
    if total != 70000:
        raise ValueError("H4L bank size drift: %d != 70000; STOP FAIL-CLOSED" % total)
    return out


def ST_roll(prev: str, key: str, eid: str, verdict: str) -> str:
    return hashlib.sha256((prev + "|" + key + "|" + eid + "|" + verdict).encode()).hexdigest()


def cmd_k2(workers=4, chunk=32):
    import multiprocessing as mp
    from wp5x import worker as W
    from wp5x import gates as G
    assert_branch()
    step("K2", "REVEALED_H4L_K6C2_REPLAY exhaustive (workers=%d, NOT fresh)" % workers)
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_k1.json").read_text(encoding="utf-8"))
    live, dead, roll = sorted(prev["live"]), {}, "GENESIS"
    shards = h4l_shards()
    for si, (name, eps) in enumerate(shards):
        ck = X / "checkpoints" / ("k2_shard_%02d.json" % si)
        if ck.exists():
            c = json.loads(ck.read_text(encoding="utf-8"))
            dead.update(c["dead"])
            live = sorted(c["live"])
            roll = c["roll"]
            step("K2", "Shard %s resumed (%d live, %d dead-cum)" % (name, len(live), len(dead)))
            continue
        by_id = {e[0]: {"n": e[1], "T0": e[2], "H": e[3], "battery": "revealed-H4L",
                        "source": name} for e in eps}
        if len(live) <= chunk:
            res = W.run_unit(eps, live, cfg)
        else:
            chunks = [live[i:i + chunk] for i in range(0, len(live), chunk)]
            with mp.get_context("spawn").Pool(workers) as pool:
                units = pool.starmap(W.run_unit, [(eps, ch, cfg) for ch in chunks])
            res = {}
            for u in units:
                res.update(u)
        new_live, kills = enrich_kills(res, by_id, cfg, "K2", "revealed-H4L")
        for key in sorted(kills):
            roll = ST_roll(roll, key, kills[key]["kill_ep"], "DEAD")
            dead[key] = kills[key]
        live = sorted(new_live)
        w(ck, {"shard": name, "dead": dead, "live": live, "roll": roll,
               "label": "REVEALED_H4L_K6C2_REPLAY"})
        step("K2", "Shard %s: live %d dead-cum %d" % (name, len(live), len(dead)))
    w(X / "kills_k2.json", dead)
    w(X / "live_k2.json", {"live": live, "count": len(live), "roll": roll,
                           "label": "REVEALED_H4L_K6C2_REPLAY"})
    step("K2", "REVEALED_H4L_K6C2_REPLAY done: live %d" % len(live))


def _agree_unit(chunk):
    import zstandard
    from solver import encode as _E
    from solver import search as _S
    from cleanroom import evaluator as _CR
    rev = ART / "h4l_reveal"
    man = json.loads((rev / "manifest.json").read_text(encoding="utf-8"))
    cfgs = {}
    for key in chunk:
        P, k, C, rho_name = key.split("|")
        cfgs[key] = (P, int(k), int(C), tuple(_S.rho_of(rho_name)))
    state = {key: [0, 0] for key in chunk}
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        dctx = zstandard.ZstdDecompressor()
        raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        eps = []
        for line in raw.decode().splitlines():
            ep = json.loads(line)
            eps.append((ep["size"], ep["T0"], ep["H"]))
        for key in chunk:
            if state[key][1]:
                continue
            P, k, C, rho = cfgs[key]
            for (n, T0, H) in eps:
                a = [(x["need"], x["paid"]) for x in
                     _E.exec_counts(_E.precompute(n, T0, H), P, k, C, rho)["keeps"]]
                b = [(x["need"], x["paid"]) for x in
                     _CR.execute(n, T0, H, P, k, C, rho)["keeps"]]
                if a == b:
                    state[key][0] += 1
                else:
                    state[key][1] += 1
                    break
    return {key: {"episodes_compared": v[0], "mismatches": v[1]} for key, v in state.items()}


def _agree_unit_indexed(task):
    ci, chunk = task
    return ci, _agree_unit(chunk)


def cmd_k3(workers=4):
    import multiprocessing as mp
    assert_branch()
    step("K3", "Clean-room agreement (full revealed bank, every K2 survivor)")
    check_code_frozen()
    prev = json.loads((X / "live_k2.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    if not live:
        w(X / "agreement_k3.json", {})
        step("K3", "No K2 survivors; agreement vacuous (0/0)")
        return
    chunks = [live[i:i + 4] for i in range(0, len(live), 4)]
    agree: dict = {}
    todo = []
    for ci, ch in enumerate(chunks):
        ck = X / "checkpoints" / ("k3_chunk_%04d.json" % ci)
        if ck.exists():
            agree.update(json.loads(ck.read_text(encoding="utf-8"))["agree"])
        else:
            todo.append((ci, ch))
    step("K3", "Chunks done %d/%d" % (len(chunks) - len(todo), len(chunks)))
    done = len(chunks) - len(todo)
    if todo:
        with mp.get_context("spawn").Pool(workers) as pool:
            for ci, u in pool.imap_unordered(_agree_unit_indexed, todo, chunksize=1):
                w(X / "checkpoints" / ("k3_chunk_%04d.json" % ci), {"agree": u})
                agree.update(u)
                done += 1
                step("K3", "Progress checkpointed (%d/%d)" % (done, len(chunks)))
    bad = [k for k, v in agree.items() if v["mismatches"]]
    w(X / "agreement_k3.json", agree)
    if bad:
        step("K3", "EVALUATOR_DISAGREEMENT on %d; STOP FAIL-CLOSED" % len(bad))
        w(X / "evaluator_disagreement.json", {k: agree[k] for k in bad})
        raise ValueError("clean-room disagreement: %r" % bad[:5])
    step("K3", "Agreement: %d survivors x full revealed bank, zero mismatches" % len(agree))


def cmd_k4():
    from wp5x import gates as G
    from cleanroom import batteries as CB
    assert_branch()
    step("K4", "Large-n battery (EXACT unchanged WP-5X battery)")
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_k2.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    large = CB.large_n()
    if len(large) != 360:
        raise ValueError("large-n battery drift: %d != 360; STOP FAIL-CLOSED" % len(large))
    eps = [(e["id"], e["n"], e["T0"], e["H"]) for e in large]
    by_id = {e["id"]: e for e in large}
    res = G.run_unit_episodes(eps, live, cfg)
    live_out, kills = enrich_kills(res, by_id, cfg, "K4", "large-n")
    w(X / "kills_k4.json", kills)
    w(X / "live_k4.json", {"live": sorted(live_out), "count": len(live_out)})
    step("K4", "Killed %d; live %d" % (len(kills), len(live_out)))


def _x5_unit(eps, chunk, cfg):
    from wp5x import worker as W
    return W.run_unit(eps, list(chunk), cfg)


def cmd_k5(workers=4):
    import multiprocessing as mp
    from wp5x import gates as G
    from cleanroom import batteries as CB
    assert_branch()
    step("K5", "OOD battery (EXACT unchanged WP-5X battery, includes n192 killer)")
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_k4.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    ood = CB.ood()
    if len(ood) != 8000:
        raise ValueError("OOD battery drift: %d != 8000; STOP FAIL-CLOSED" % len(ood))
    # Verify the known n192 killer is present in the frozen OOD stream.
    n192_id = json.loads((CE_DIR / "ce_0000.json").read_text(encoding="utf-8"))["episode"]["id"]
    if n192_id not in {e["id"] for e in ood}:
        # The killer may be excluded by dedup/exclude rules in other contexts;
        # record explicitly but do not mutate the frozen battery.
        step("K5", "WARNING: n192 witness id not byte-identical in OOD stream; "
                   "running unchanged battery anyway (K1 already covers the witness)")
    eps = [(e["id"], e["n"], e["T0"], e["H"]) for e in ood]
    by_id = {e["id"]: e for e in ood}
    if not live:
        w(X / "kills_k5.json", {})
        w(X / "live_k5.json", {"live": [], "count": 0})
        step("K5", "No K4 survivors; OOD vacuous")
        return
    shards = [live[i:i + 32] for i in range(0, len(live), 32)]
    merged, done_shards = {}, 0
    for si, sh in enumerate(shards):
        ck = X / "checkpoints" / ("k5_shard_%02d.json" % si)
        if ck.exists():
            merged.update(json.loads(ck.read_text(encoding="utf-8"))["res"])
            done_shards += 1
    todo = [(si, sh) for si, sh in enumerate(shards)
            if not (X / "checkpoints" / ("k5_shard_%02d.json" % si)).exists()]
    step("K5", "Shards done %d/%d" % (done_shards, len(shards)))
    while todo:
        batch, todo = todo[:workers], todo[workers:]
        if len(batch) == 1 and len(shards) == 1:
            u = _x5_unit(eps, batch[0][1], cfg)
            units = [u]
        else:
            with mp.get_context("spawn").Pool(workers) as pool:
                units = pool.starmap(_x5_unit, [(eps, sh, cfg) for _, sh in batch])
        for (si, _), u in zip(batch, units):
            w(X / "checkpoints" / ("k5_shard_%02d.json" % si), {"res": u})
            merged.update(u)
        step("K5", "Progress %d/%d shards" % (len(shards) - len(todo), len(shards)))
    live_out, kills = enrich_kills(merged, by_id, cfg, "K5", "ood")
    w(X / "kills_k5.json", kills)
    w(X / "live_k5.json", {"live": sorted(live_out), "count": len(live_out)})
    step("K5", "Killed %d; live %d" % (len(kills), len(live_out)))


def cmd_k6():
    assert_branch()
    step("K6", "Freezing known-gate survivors + phase diagram (FINITE only)")
    check_code_frozen()
    pop = json.loads((X / "k0_population.json").read_text(encoding="utf-8"))
    k1k = json.loads((X / "kills_k1.json").read_text(encoding="utf-8"))
    k2k = json.loads((X / "kills_k2.json").read_text(encoding="utf-8"))
    agr = json.loads((X / "agreement_k3.json").read_text(encoding="utf-8"))
    k4k = json.loads((X / "kills_k4.json").read_text(encoding="utf-8"))
    k5k = json.loads((X / "kills_k5.json").read_text(encoding="utf-8"))
    live5 = json.loads((X / "live_k5.json").read_text(encoding="utf-8"))
    members = {m["key"]: m for m in pop["members"]}

    def first_kill(key):
        for stage, d in (("K1", k1k), ("K2", k2k), ("K4", k4k), ("K5", k5k)):
            if key in d:
                return stage, d[key]["kill_ep"]
        return None, None

    rows = []
    for key in sorted(members):
        m = members[key]
        gk, gep = first_kill(key)
        rows.append({
            "key": key, "P": m["P"], "k": m["k"], "C": m["C"], "rho": m["rho"],
            "label": m["label"], "rank": m["rank"],
            "wp4_eligible": True,
            "k1": "DEAD" if key in k1k else "LIVE",
            "k2": "DEAD" if key in k2k else ("LIVE" if key not in k1k else "N/A"),
            "k3_agree": (agr.get(key, {"mismatches": 0})["mismatches"] == 0
                         if key in agr else ("N/A" if key in k1k or key in k2k else "MISSING")),
            "k4": "DEAD" if key in k4k else ("LIVE" if key not in k1k and key not in k2k else "N/A"),
            "k5": "DEAD" if key in k5k else ("LIVE" if key in live5["live"] else "N/A"),
            "k6": "SURVIVOR" if key in live5["live"] else "DEAD",
            "first_kill_gate": gk, "first_kill_episode": gep,
        })
    surv = sorted(live5["live"])
    surv_hash = sha_json([{"key": k, "identity_hash": members[k]["identity_hash"]} for k in surv])
    status = ("K6C2_SPECIALIZED_SET_SURVIVES_KNOWN_FINITE_GATES" if surv
              else "K6C2_SPECIALIZED_SET_REJECTED")
    w(X / "specialized_survivors.json", {
        "status": status,
        "label": "FINITE evidence only; FRESH_H5_REQUIRED_BEFORE_WP6",
        "count": len(surv), "survivors": surv, "survivor_set_hash": surv_hash,
        "members": [{**members[k], "gate_history": next(r for r in rows if r["key"] == k)}
                    for k in surv]})
    w(X / "phase_diagram.json", {
        "rows": rows,
        "h4l_label": "REVEALED_H4L_K6C2_REPLAY",
        "note": "Finite phase diagram only; no universality claim.",
        "counts": {
            "population": pop["count"], "k1_live": pop["count"] - len(k1k),
            "k2_live": pop["count"] - len(k1k) - len([k for k in k2k if k not in k1k]),
            "k4_live": pop["count"] - len(k1k) - len(k2k) - len(k4k),
            "k5_live": len(surv)},
        "population_hash": pop["population_hash"], "survivor_set_hash": surv_hash,
        "status": status})
    step("K6", "%s: %d/%d survive known finite gates" % (status, len(surv), pop["count"]))
    # Console phase-diagram answers (finite only).
    print(json.dumps({"status": status, "survivors": surv,
                      "survivor_set_hash": surv_hash}, indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    {"k0": cmd_k0, "k1": cmd_k1, "k2": lambda: cmd_k2(workers=workers),
     "k3": lambda: cmd_k3(workers=workers), "k4": cmd_k4,
     "k5": lambda: cmd_k5(workers=workers), "k6": cmd_k6}[cmd]()
