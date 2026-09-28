"""WP-5X orchestrator: benchmark | x0 | x1 | x2 | x3 | x4 | x5 | report.

Deterministic, resumable, crash-safe. Never mutates frozen artifacts, never
touches H4L secret material (reads only the published reveal), never claims
freshness for H4L. Artifact root: artifacts/v04/wp5x/.
"""
from __future__ import annotations
import hashlib
import json
import sys
import time
import tracemalloc
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = sys.executable
sys.path.insert(0, str(ROOT / "python"))
from wp5x import population as POP
from wp5x import factored as F
from wp5x import stages as ST

ART = ROOT / "artifacts" / "v04"
X = ART / "wp5x"
DEV = ART / "development"


def step(sid: str, msg: str) -> None:
    print("[WP-5X][STEP %s] %s" % (sid, msg), flush=True)


def w(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def sha_bytes(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def code_hashes() -> dict:
    return {"encode": sha_bytes(ROOT / "python" / "solver" / "encode.py"),
            "cleanroom": sha_bytes(ROOT / "python" / "cleanroom" / "evaluator.py"),
            "independent": sha_bytes(ROOT / "python" / "independent" / "config_exec.py"),
            "predicates": sha_bytes(ROOT / "python" / "solver" / "predicates.py")}


def check_code_frozen() -> None:
    """WP-5X: no semantic bytes may change mid-run (STOP otherwise)."""
    rec = json.loads((X / "x0_population.json").read_text(encoding="utf-8"))
    if code_hashes() != rec["code_hashes"]:
        raise ValueError("code bytes changed mid-run; STOP FAIL-CLOSED")


def load_population():
    rec = json.loads((X / "x0_population.json").read_text(encoding="utf-8"))
    if rec["count"] != 6099:
        raise ValueError("population drift; STOP FAIL-CLOSED")
    return rec


def cmd_benchmark():
    import zstandard
    from solver import search as S
    step("B1", "Equivalence regression proof (sample)")
    rev = ART / "h4l_reveal"
    man = json.loads((rev / "manifest.json").read_text(encoding="utf-8"))
    dctx = zstandard.ZstdDecompressor()
    sample = []
    for sh in sorted(man["shards"], key=lambda s: s["name"])[:1]:
        raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        for line in raw.decode().splitlines()[:30]:
            ep = json.loads(line)
            sample.append((ep["size"], ep["T0"], ep["H"]))
    rk = json.loads((DEV / "ranking.json").read_text(encoding="utf-8"))
    cfgs = []
    for t in rk[::100][:60]:
        P, k, C, rho = t["key"].split("|")
        cfgs.append((P, int(k), int(C), S.rho_of(rho)))
    proof = F.prove_equivalence(sample, cfgs)
    w(X / "benchmark" / "equivalence_proof.json", proof)
    step("B2", "Worker scaling (1 H4L shard x 300 candidates)")
    import multiprocessing as mp
    from wp5x import worker as W
    raw_eps = []
    for sh in sorted(man["shards"], key=lambda s: s["name"])[:1]:
        raw = dctx.decompress((rev / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        for line in raw.decode().splitlines()[:1000]:
            ep = json.loads(line)
            raw_eps.append((ep["hash"], ep["size"], ep["T0"], ep["H"]))
    cand = rk[:300]
    cfg = {}
    for t in cand:
        P, k, C, rho = t["key"].split("|")
        cfg[t["key"]] = (P, int(k), int(C), tuple(S.rho_of(rho)))
    chunk = [t["key"] for t in cand]
    tracemalloc.start()
    res = {}
    t0 = time.time()
    W.run_unit(raw_eps, chunk, cfg)
    t1 = time.time()
    _, peak = tracemalloc.get_traced_memory()
    res["workers_1"] = {"wall_s": t1 - t0, "units": len(raw_eps) * len(chunk),
                        "eps_per_s": len(raw_eps) * len(chunk) / max(t1 - t0, 1e-9),
                        "peak_ram_mb": peak / 2 ** 20}
    for workers in (2, 4, 6, 8):
        t0 = time.time()
        with mp.get_context("spawn").Pool(workers) as pool:
            pool.starmap(W.run_unit, [(raw_eps, chunk, cfg)])
        t1 = time.time()
        res["workers_%d" % workers] = {"wall_s": t1 - t0,
                                       "eps_per_s": len(raw_eps) * len(chunk) / max(t1 - t0, 1e-9)}
    w(X / "benchmark" / "scaling.json", res)
    best = max(res, key=lambda k: res[k]["eps_per_s"])
    proj = 6099 * 70000 / res[best]["eps_per_s"]
    est = {"best": best, "best_eps_per_s": res[best]["eps_per_s"],
           "projected_H4L_full_s": proj, "projected_H4L_full_h": proj / 3600,
           "note": "fail-fast + equivalence classes reduce this substantially"}
    w(X / "benchmark" / "estimate.json", est)
    step("B3", "Best %s: %.0f ep/s; H4L-full projection %.1fh (pre-fail-fast)" %
         (best, res[best]["eps_per_s"], proj / 3600))
    print(json.dumps(est, indent=2))


def cmd_x0():
    import yaml
    step("X0", "Population reconstruction + freeze")
    elig = POP.load_eligible(DEV)
    pred = {p["id"]: p["hash"] for p in yaml.safe_load(
        open(ROOT / "prereg" / "predicate_family_v0.4.1.yaml").read())["predicates"]}
    elig = POP.freeze_identities(elig, pred, X)
    import json as _j
    schema = _j.loads(open(ROOT / "schemas" / "candidate.schema.json").read())
    for e in elig:
        if set(e["identity"]) != set(schema["required"]):
            raise ValueError("identity schema fail: %s" % e["key"])
    rec = {"count": len(elig), "population_hash": POP.population_hash(elig),
           "code_hashes": code_hashes(),
           "members": [{"key": e["key"], "label": e["label"], "rank": e["rank"],
                        "identity_hash": e["identity_hash"]} for e in elig]}
    w(X / "x0_population.json", rec)
    with open(X / "x0_identities.jsonl", "w", encoding="utf-8") as f:
        for e in elig:
            f.write(_j.dumps({"key": e["key"], "identity": e["identity"]},
                             sort_keys=True) + "\n")
    step("X0", "Frozen %d identities hash=%s" % (len(elig), rec["population_hash"][:16]))


def load_cfg():
    rec = load_population()
    cfg = {}
    for m in rec["members"]:
        P, k, C, rho = m["key"].split("|")
        cfg[m["key"]] = (P, int(k), int(C), tuple(__import__(
            "solver.search", fromlist=["rho_of"]).rho_of(rho)))
    return rec, cfg


def live_after(stage: str):
    """Live set after a completed stage (from its checkpoint/output)."""
    if stage == "x0":
        return sorted(load_population()["members"] and [m["key"] for m in load_population()["members"]])
    d = json.loads((X / ("live_%s.json" % stage)).read_text(encoding="utf-8"))
    return sorted(d["live"])


def cmd_x1():
    from wp5x import gates as G
    step("X1", "Known-counterexample regression (n192 first, then REG-001)")
    check_code_frozen()
    rec, cfg = load_cfg()
    live = [m["key"] for m in rec["members"]]
    ce = json.load(open(ART / "counterexamples" / "ce_0000.json"))
    n192 = dict(ce["episode"])
    n192["battery"] = "x1-n192-witness"

    def vine(n):
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t

    reg = {"eid": "REG-001", "n": 28, "T0": vine(28),
           "H": [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]],
           "battery": "x1-REG-001"}
    eps = [(n192["id"], n192["n"], n192["T0"], n192["H"]),
           ("REG-001", reg["n"], reg["T0"], reg["H"])]
    by_id = {n192["id"]: n192, "REG-001": reg}
    res = G.run_unit_episodes(eps, live, cfg)
    live_out, kills = G.finalize_kills(res, by_id, cfg, "X1", "known-regression")
    w(X / "kills_x1.json", kills)
    w(X / "live_x1.json", {"live": live_out, "count": len(live_out)})
    step("X1", "Killed %d on known witnesses; live %d" % (len(kills), len(live_out)))


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
    return out


def cmd_x2(workers=4, chunk=128):
    import multiprocessing as mp
    from wp5x import worker as W
    from wp5x import gates as G
    step("X2", "Revealed-H4L exhaustive replay (workers=%d)" % workers)
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_x1.json").read_text(encoding="utf-8"))
    live, dead, roll = sorted(prev["live"]), {}, "GENESIS"
    shards = h4l_shards()
    for si, (name, eps) in enumerate(shards):
        ck = X / "checkpoints" / ("x2_shard_%02d.json" % si)
        if ck.exists():
            c = json.loads(ck.read_text(encoding="utf-8"))
            dead.update(c["dead"])
            live = sorted(c["live"])
            roll = c["roll"]
            step("X2", "Shard %s resumed (%d live)" % (name, len(live)))
            continue
        by_id = {e[0]: {"n": e[1], "T0": e[2], "H": e[3]} for e in eps}
        chunks = [live[i:i + chunk] for i in range(0, len(live), chunk)]
        with mp.get_context("spawn").Pool(workers) as pool:
            units = pool.starmap(W.run_unit, [(eps, ch, cfg) for ch in chunks])
        res = {}
        for u in units:
            res.update(u)
        new_live, kills = G.finalize_kills(res, by_id, cfg, "X2", "revealed-H4L")
        for key in sorted(kills):
            roll = ST_roll(roll, key, kills[key]["kill_ep"], "DEAD")
            dead[key] = kills[key]
        live = sorted(new_live)
        w(ck, {"shard": name, "dead": dead, "live": live, "roll": roll})
        step("X2", "Shard %s: live %d dead-cum %d" % (name, len(live), len(dead)))
    w(X / "kills_x2.json", dead)
    w(X / "live_x2.json", {"live": live, "count": len(live), "roll": roll})
    step("X2", "REVEALED_H4L_EXHAUSTIVE_REPLAY done: live %d" % len(live))


def ST_roll(prev: str, key: str, eid: str, verdict: str) -> str:
    import hashlib
    return hashlib.sha256((prev + "|" + key + "|" + eid + "|" + verdict).encode()).hexdigest()


def cmd_x3(workers=6):
    import multiprocessing as mp
    step("X3", "Clean-room agreement (full bank, every X2 survivor)")
    check_code_frozen()
    prev = json.loads((X / "live_x2.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    chunks = [live[i:i + 16] for i in range(0, len(live), 16)]
    agree = {}
    todo = []
    for ci, ch in enumerate(chunks):
        ck = X / "checkpoints" / ("x3_chunk_%04d.json" % ci)
        if ck.exists():
            agree.update(json.loads(ck.read_text(encoding="utf-8"))["agree"])
        else:
            todo.append((ci, ch))
    step("X3", "Chunks done %d/%d" % (len(chunks) - len(todo), len(chunks)))
    # WP-5X: ONE persistent pool; imap_unordered streams results so every
    # completed chunk checkpoints immediately (crash-safe resume).
    done = len(chunks) - len(todo)
    with mp.get_context("spawn").Pool(workers) as pool:
        for ci, u in pool.imap_unordered(_agree_unit_indexed, [t for t in todo], chunksize=1):
            w(X / "checkpoints" / ("x3_chunk_%04d.json" % ci), {"agree": u})
            agree.update(u)
            done += 1
            if done % 8 == 0:
                step("X3", "Progress %d/%d chunks" % (done, len(chunks)))
    bad = [k for k, v in agree.items() if v["mismatches"]]
    w(X / "agreement_x3.json", agree)
    if bad:
        step("X3", "DISAGREEMENT on %d; STOP FAIL-CLOSED" % len(bad))
        raise ValueError("clean-room disagreement: %r" % bad[:5])
    step("X3", "Agreement: %d survivors x full bank, zero mismatches" % len(agree))


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
    # WP-5X: parse each shard ONCE per chunk; all candidates share parsed episodes.
    state = {key: [0, 0] for key in chunk}  # key -> [match, mismatch]
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


def cmd_x4():
    from wp5x import gates as G
    from cleanroom import batteries as CB
    step("X4", "Large-n battery (unchanged)")
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_x2.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    large = CB.large_n()
    eps = [(e["id"], e["n"], e["T0"], e["H"]) for e in large]
    by_id = {e["id"]: e for e in large}
    res = G.run_unit_episodes(eps, live, cfg)
    live_out, kills = G.finalize_kills(res, by_id, cfg, "X4", "large-n")
    w(X / "kills_x4.json", kills)
    w(X / "live_x4.json", {"live": live_out, "count": len(live_out)})
    step("X4", "Killed %d; live %d" % (len(kills), len(live_out)))


def cmd_x5(workers=4):
    import multiprocessing as mp
    from wp5x import gates as G
    from cleanroom import batteries as CB
    step("X5", "OOD battery (unchanged, includes known n192 killer)")
    check_code_frozen()
    rec, cfg = load_cfg()
    prev = json.loads((X / "live_x4.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    ood = CB.ood()
    eps = [(e["id"], e["n"], e["T0"], e["H"]) for e in ood]
    by_id = {e["id"]: e for e in ood}
    shards = [live[i:i + 512] for i in range(0, len(live), 512)]
    merged, done_shards = {}, 0
    for si, sh in enumerate(shards):
        ck = X / "checkpoints" / ("x5_shard_%02d.json" % si)
        if ck.exists():
            merged.update(json.loads(ck.read_text(encoding="utf-8"))["res"])
            done_shards += 1
            continue
    todo = [(si, sh) for si, sh in enumerate(shards)
            if not (X / "checkpoints" / ("x5_shard_%02d.json" % si)).exists()]
    step("X5", "Shards done %d/%d" % (done_shards, len(shards)))
    while todo:
        batch, todo = todo[:workers], todo[workers:]
        with mp.get_context("spawn").Pool(workers) as pool:
            units = pool.starmap(_x5_unit, [(eps, sh, cfg) for _, sh in batch])
        for (si, _), u in zip(batch, units):
            w(X / "checkpoints" / ("x5_shard_%02d.json" % si), {"res": u})
            merged.update(u)
        step("X5", "Progress %d/%d shards" % (len(shards) - len(todo), len(shards)))
    live_out, kills = G.finalize_kills(merged, by_id, cfg, "X5", "ood")
    w(X / "kills_x5.json", kills)
    w(X / "live_x5.json", {"live": live_out, "count": len(live_out)})
    step("X5", "Killed %d; live %d" % (len(kills), len(live_out)))


def _agree_unit_indexed(task):
    ci, chunk = task
    return ci, _agree_unit(chunk)


def _x5_unit(eps, chunk, cfg):
    from wp5x import worker as W
    return W.run_unit(eps, list(chunk), cfg)
    from wp5x import worker as W
    return W.run_unit(eps, list(chunk), cfg)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    {"benchmark": cmd_benchmark, "x0": cmd_x0, "x1": cmd_x1, "x2": cmd_x2,
     "x3": cmd_x3, "x4": cmd_x4, "x5": cmd_x5}[cmd]()
