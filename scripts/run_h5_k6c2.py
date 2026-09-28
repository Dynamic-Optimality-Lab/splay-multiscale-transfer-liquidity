"""H5 evaluation for the frozen 63 K6 survivors (WP-5X-K6C2, FRESH_H5_K6C2).

Uses the EXACT frozen primary semantics already used in WP-5X-K6C2 by
delegating evaluation to python/wp5x/{worker,gates,stages,factored} via the
frozen K6C2 helpers (import run_wp5x_k6c2 for orchestration: w, ST_roll,
enrich_kills, load_cfg, check_code_frozen, assert_branch). No semantic
modifications, no candidate mutation, no H5 retuning.

Commands:
  eval [workers]   primary FRESH_H5_K6C2 evaluation (fail-fast, independent
                   confirm, resumable per-shard checkpoints)
  agree [workers]  clean-room full-H5-bank verification per H5 survivor
  freeze           H5 survivor-set freeze + terminal + WP6 entry fact

Output ONLY under artifacts/v04/wp5x_k6c2/h5/. H4L is never touched here.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import run_wp5x_k6c2 as K

ART = ROOT / "artifacts" / "v04"
H5REV = ART / "h5_reveal"
XH5 = ART / "wp5x_k6c2" / "h5"

K6_HASH = "9dcdea2b7926cf94765e1fd818a73f0459c72404b4f4bf5c36b3ec65a27e5748"
K6_COUNT = 63
BRANCH_REQUIRED = "wp5x-k6c2-specialized"
assert BRANCH_REQUIRED == K.BRANCH_REQUIRED


def step(sid: str, msg: str) -> None:
    print("[H5-K6C2][STEP %s] %s" % (sid, msg), flush=True)


def check_k6_frozen():
    k6 = json.loads((ART / "wp5x_k6c2" / "specialized_survivors.json").read_text(encoding="utf-8"))
    if k6.get("survivor_set_hash") != K6_HASH or k6.get("count") != K6_COUNT:
        raise ValueError("K6 survivor set drift; STOP FAIL-CLOSED")
    if sorted(k6["survivors"]) != k6["survivors"]:
        raise ValueError("K6 ordering drift; STOP FAIL-CLOSED")
    return sorted(k6["survivors"])


def h5_shards():
    import zstandard
    man = json.loads((H5REV / "manifest.json").read_text(encoding="utf-8"))
    if man.get("bank_id") != "H5-R1":
        raise ValueError("H5 manifest bank_id drift; STOP FAIL-CLOSED")
    dctx = zstandard.ZstdDecompressor()
    out = []
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        raw = dctx.decompress((H5REV / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        eps = []
        for line in raw.decode().splitlines():
            ep = json.loads(line)
            eps.append((ep["hash"], ep["size"], ep["T0"], ep["H"]))
        out.append((sh["name"], eps))
    total = sum(len(eps) for _, eps in out)
    if total != 70000:
        raise ValueError("H5 bank size drift: %d != 70000; STOP FAIL-CLOSED" % total)
    return out, man


def cmd_eval(workers=4, chunk=32):
    import multiprocessing as mp
    from wp5x import worker as W
    K.assert_branch()
    step("HE", "FRESH_H5_K6C2 primary evaluation (workers=%d)" % workers)
    K.check_code_frozen()
    live0 = check_k6_frozen()
    rec, cfg = K.load_cfg()
    cfg = {k: v for k, v in cfg.items() if k in set(live0)}
    if sorted(cfg) != live0:
        raise ValueError("cfg/K6 coverage mismatch; STOP FAIL-CLOSED")
    live, dead, roll = list(live0), {}, "GENESIS"
    shards, man = h5_shards()
    for si, (name, eps) in enumerate(shards):
        ck = XH5 / "checkpoints" / ("h5_shard_%02d.json" % si)
        if ck.exists():
            c = json.loads(ck.read_text(encoding="utf-8"))
            dead.update(c["dead"])
            live = sorted(c["live"])
            roll = c["roll"]
            step("HE", "Shard %s resumed (%d live, %d dead-cum)" % (name, len(live), len(dead)))
            continue
        by_id = {e[0]: {"n": e[1], "T0": e[2], "H": e[3], "battery": "fresh-H5",
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
        new_live, kills = K.enrich_kills(res, by_id, cfg, "H5", "fresh-H5")
        for key in sorted(kills):
            roll = K.ST_roll(roll, key, kills[key]["kill_ep"], "DEAD")
            dead[key] = kills[key]
        live = sorted(new_live)
        K.w(ck, {"shard": name, "dead": dead, "live": live, "roll": roll,
                 "label": "FRESH_H5_K6C2"})
        step("HE", "Shard %s: live %d dead-cum %d" % (name, len(live), len(dead)))
    K.w(XH5 / "h5_kills.json", dead)
    K.w(XH5 / "h5_live.json", {"live": live, "count": len(live), "roll": roll,
                               "label": "FRESH_H5_K6C2"})
    step("HE", "FRESH_H5_K6C2 primary done: live %d/%d" % (len(live), len(live0)))


def _h5_agree_unit(chunk):
    import zstandard
    from solver import encode as _E
    from solver import search as _S
    from cleanroom import evaluator as _CR
    man = json.loads((H5REV / "manifest.json").read_text(encoding="utf-8"))
    cfgs = {}
    for key in chunk:
        P, k, C, rho_name = key.split("|")
        cfgs[key] = (P, int(k), int(C), tuple(_S.rho_of(rho_name)))
    state = {key: [0, 0] for key in chunk}
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        dctx = zstandard.ZstdDecompressor()
        raw = dctx.decompress((H5REV / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
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


def _h5_agree_indexed(task):
    ci, chunk = task
    return ci, _h5_agree_unit(chunk)


def cmd_agree(workers=8):
    import multiprocessing as mp
    K.assert_branch()
    step("HA", "Clean-room H5 verification (full fresh bank per H5 survivor)")
    K.check_code_frozen()
    check_k6_frozen()
    prev = json.loads((XH5 / "h5_live.json").read_text(encoding="utf-8"))
    live = sorted(prev["live"])
    if not live:
        K.w(XH5 / "h5_agreement.json", {})
        step("HA", "No H5 survivors; agreement vacuous (0/0)")
        return
    chunks = [live[i:i + 4] for i in range(0, len(live), 4)]
    agree: dict = {}
    todo = []
    for ci, ch in enumerate(chunks):
        ck = XH5 / "checkpoints" / ("h5a_chunk_%04d.json" % ci)
        if ck.exists():
            agree.update(json.loads(ck.read_text(encoding="utf-8"))["agree"])
        else:
            todo.append((ci, ch))
    step("HA", "Chunks done %d/%d" % (len(chunks) - len(todo), len(chunks)))
    done = len(chunks) - len(todo)
    if todo:
        with mp.get_context("spawn").Pool(workers) as pool:
            for ci, u in pool.imap_unordered(_h5_agree_indexed, todo, chunksize=1):
                K.w(XH5 / "checkpoints" / ("h5a_chunk_%04d.json" % ci), {"agree": u})
                agree.update(u)
                done += 1
                step("HA", "Progress checkpointed (%d/%d)" % (done, len(chunks)))
    bad = [k for k, v in agree.items() if v["mismatches"]]
    K.w(XH5 / "h5_agreement.json", agree)
    if bad:
        step("HA", "H5_EVALUATOR_DISAGREEMENT on %d; STOP FAIL-CLOSED" % len(bad))
        K.w(XH5 / "h5_evaluator_disagreement.json", {k: agree[k] for k in bad})
        raise ValueError("H5 clean-room disagreement: %r" % bad[:5])
    step("HA", "Agreement: %d H5 survivors x full fresh bank, zero mismatches" % len(agree))


def cmd_freeze():
    import hashlib
    K.assert_branch()
    step("HF", "Freezing H5 survivor set (FINITE falsification only)")
    K.check_code_frozen()
    k6_live = check_k6_frozen()
    kills = json.loads((XH5 / "h5_kills.json").read_text(encoding="utf-8"))
    live = json.loads((XH5 / "h5_live.json").read_text(encoding="utf-8"))
    agree = json.loads((XH5 / "h5_agreement.json").read_text(encoding="utf-8"))
    if set(kills) | set(live["live"]) != set(k6_live):
        raise ValueError("H5 partition != frozen K6 set; STOP FAIL-CLOSED")
    if set(agree) != set(live["live"]):
        raise ValueError("H5 agreement coverage != H5 survivors; STOP FAIL-CLOSED")
    pop = json.loads((ART / "wp5x_k6c2" / "k0_population.json").read_text(encoding="utf-8"))
    members = {m["key"]: m for m in pop["members"]}
    surv = sorted(live["live"])
    surv_hash = hashlib.sha256(json.dumps(
        [{"key": k, "identity_hash": members[k]["identity_hash"]} for k in surv],
        sort_keys=True).encode()).hexdigest()
    status = ("H5_K6C2_SET_SURVIVES_FRESH_HOLDOUT" if surv else "H5_K6C2_SET_REJECTED")
    man = json.loads((H5REV / "manifest.json").read_text(encoding="utf-8"))
    com = json.loads((ART / "h5" / "h5_commitment.json").read_text(encoding="utf-8"))
    K.w(XH5 / "h5_results.json", {
        "label": "FRESH_H5_K6C2",
        "entry_count": K6_COUNT, "evaluated": K6_COUNT,
        "killed": len(kills), "survived": len(surv),
        "status": status,
        "note": "Finite falsification only; not evidence for MSTL-14 or any universal claim."})
    K.w(XH5 / "h5_survivors.json", {
        "status": status, "count": len(surv), "survivors": surv,
        "survivor_set_hash": surv_hash,
        "members": [{**members[k]} for k in surv]})
    K.w(XH5 / "h5_manifest.json", {
        "bank": "H5", "bank_id": "H5-R1",
        "h5_shards": man["shards"], "logical_stream_sha256": man["logical_stream_sha256"],
        "commitment": com["commitment"],
        "generator_sha256": man["generator"],
        "inherited_h4l_generator_sha256": man.get("inherited_h4l_generator_sha256"),
        "k6_entry_hash": K6_HASH, "k6_entry_count": K6_COUNT,
        "h5_survivor_set_hash": surv_hash, "h5_survivor_count": len(surv),
        "status": status})
    if surv:
        K.w(XH5 / "wp6_entry_set.json", {
            "status": "WP6_ENTRY_SET_FROZEN",
            "note": "These candidates survived the specified genuinely fresh H5 finite "
                    "holdout. Finite evidence only; MSTL-14 remains UNPROVED.",
            "count": len(surv), "survivors": surv, "survivor_set_hash": surv_hash,
            "members": [{**members[k]} for k in surv]})
    step("HF", "%s: %d/%d survive fresh H5" % (status, len(surv), K6_COUNT))
    print(json.dumps({"status": status, "survivors": surv,
                      "survivor_set_hash": surv_hash}, indent=2))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    {"eval": lambda: cmd_eval(workers=workers),
     "agree": lambda: cmd_agree(workers=workers),
     "freeze": cmd_freeze}[cmd]()
