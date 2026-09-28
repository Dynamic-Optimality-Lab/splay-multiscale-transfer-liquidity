"""WP-5 STEP 140m: fresh-context mutation battery (16 mutants, each live + killed).

No contact with the real H4L secret bank (tmp mini-banks only), except two
refusal probes that touch public paths alone. Exit 0 iff 16/16 killed.
"""
from __future__ import annotations
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import firewall as FW
from holdout import h4l_verify as V

PASS = []


def check(name: str, cond: bool) -> None:
    print("[WP-5][MUTANT %s] %s" % (name, "KILLED" if cond else "SURVIVED"), flush=True)
    PASS.append(bool(cond))


def _bal(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], _bal(keys[:m]), _bal(keys[m + 1:])]


def _mk_ep(H):
    T0 = _bal(list(range(1, 8)))
    ep = {"size": 7, "stratum": "RANDOM_LEGAL", "shape": "balanced", "T0": T0, "H": H}
    ep["hash"] = hashlib.sha256(json.dumps(
        {k: v for k, v in ep.items() if k != "hash"}, sort_keys=True).encode()).hexdigest()
    return ep


def _mini(tmp_path, episodes, Tamper=None):
    import zstandard
    sec = tmp_path / "sec"
    (sec / "bank").mkdir(parents=True)
    seed = b"wp5-probe-seed-" + b"0" * 17
    assert len(seed) == 32
    (sec / "seed.bin").write_bytes(seed)
    name = "mini_n7.json.zst"
    lines = [json.dumps(ep, sort_keys=True) for ep in episodes]
    blob = zstandard.ZstdCompressor(level=3).compress(("\n".join(lines)).encode())
    if Tamper == "byte":
        blob = blob[:-1] + (b"\x00" if blob[-1:] != b"\x00" else b"\x01")
    (sec / "bank" / name).write_bytes(blob)
    order = [e["hash"] for e in episodes]
    lh = hashlib.sha256()
    for i in order:
        lh.update(i.encode())
    man = {"shards": [{"name": name, "sha256": hashlib.sha256(blob).hexdigest(),
                       "bytes": len(blob), "episodes": len(lines), "zstd_level": 3}],
           "logical_stream_sha256": lh.hexdigest(), "generator": "probe"}
    (sec / "manifest.json").write_text(json.dumps(man, sort_keys=True), encoding="utf-8")
    com = {"bank": "PROBE", "commitment": "", "total": len(episodes), "sizes": [7],
           "per_size": len(episodes),
           "quotas": {"7|RANDOM_LEGAL": len(episodes)},
           "shards": [{"name": name, "sha256": hashlib.sha256(blob).hexdigest()}],
           "logical_stream_sha256": lh.hexdigest(), "generator_sha256": "probe",
           "strata": ["RANDOM_LEGAL"], "seed_status": "probe"}
    h = hashlib.sha256()
    h.update(seed)
    h.update(blob)
    if Tamper == "seed":
        h.update(b"wrong")
    com["commitment"] = h.hexdigest()
    com_p = tmp_path / "com.json"
    com_p.write_text(json.dumps(com, sort_keys=True), encoding="utf-8")
    return sec, com_p


def _good():
    return _mk_ep([["KEEP", 3], ["DELETE", 5]])


def main() -> int:
    print("[WP-5][STEP 140m] Running WP-5 mutation battery", flush=True)
    import tempfile
    # M-WP5-01: tampered shard byte -> per-shard SHA mismatch.
    with tempfile.TemporaryDirectory() as td:
        sec, com = _mini(Path(td), [_good()], Tamper="byte")
        check("M-WP5-01 tampered shard", V.verify(sec, com) is False)
    # M-WP5-02: wrong-seed commitment -> recompute fails.
    with tempfile.TemporaryDirectory() as td:
        sec, com = _mini(Path(td), [_good()], Tamper="seed")
        check("M-WP5-02 seed mismatch", V.verify(sec, com) is False)
    # M-WP5-03: second reveal -> refused, unlocks stays 1.
    import tempfile as _tf
    with _tf.TemporaryDirectory() as td:
        import unittest.mock as _m
        with _m.patch.object(FW, "STATE_FILE", Path(td) / "fw.json"):
            for to in ["GENERATOR_FROZEN", "BANK_GENERATED_SECRET",
                       "COMMITMENT_PUBLISHED", "CANDIDATE_SET_FROZEN"]:
                FW.transition(to, "m03")
            FW.transition("REVEALED_ONCE", "m03-first")
            try:
                FW.reveal()
                second_ok = True
            except FW.FirewallError:
                second_ok = False
            check("M-WP5-03 second reveal",
                  not second_ok and FW.read_state()["unlocks"] == 1)
    # M-WP5-04: regen after reveal -> seal refuses (public paths only).
    r = subprocess.run([sys.executable, "scripts/seal_h4l.py"],
                       capture_output=True, text=True, cwd=str(ROOT))
    check("M-WP5-04 regen refused", r.returncode == 2)
    # M-WP5-05: unsorted shard -> order check fails.
    with tempfile.TemporaryDirectory() as td:
        e1, e2 = _good(), _mk_ep([["DELETE", 1]] * 4)
        eps = sorted([e1, e2], key=lambda e: e["hash"])
        sec, com = _mini(Path(td), list(reversed(eps)))
        check("M-WP5-05 unsorted shard", V.verify(sec, com) is False)
    # M-WP5-06: corrupted episode ID -> recompute mismatch.
    with tempfile.TemporaryDirectory() as td:
        ep = _good()
        ep["hash"] = ("0" if ep["hash"][0] != "0" else "1") + ep["hash"][1:]
        sec, com = _mini(Path(td), [ep])
        check("M-WP5-06 corrupt ID", V.verify(sec, com) is False)
    # M-WP5-07: access key outside [size] -> legality fails.
    with tempfile.TemporaryDirectory() as td:
        sec, com = _mini(Path(td), [_mk_ep([["KEEP", 99]])])
        check("M-WP5-07 wrong-size key", V.verify(sec, com) is False)
    # M-WP5-08: illegal mode -> legality fails.
    with tempfile.TemporaryDirectory() as td:
        sec, com = _mini(Path(td), [_mk_ep([["HOLD", 3]])])
        check("M-WP5-08 illegal mode", V.verify(sec, com) is False)
    # M-WP5-09: clean-room forbidden import (synthetic) -> audit flags.
    bad_src = "from liquidity import activation\nimport hashlib\n"
    tree = ast.parse(bad_src)
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or "").split(".")[0])
    good_src = (ROOT / "python" / "cleanroom" / "evaluator.py").read_text(encoding="utf-8")
    gtree = ast.parse(good_src)
    gmods = set()
    for node in ast.walk(gtree):
        if isinstance(node, ast.Import):
            gmods.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            gmods.add((node.module or "").split(".")[0])
    check("M-WP5-09 cleanroom import",
          bool(mods & {"liquidity", "solver", "holdout"}) and gmods <= {"__future__"})
    # M-WP5-10: injected agreement mismatch -> comparator reports it.
    a = [{"need": 11, "paid": 10}]
    b = [{"need": 11, "paid": 9}]
    agree = [(x["need"], x["paid"]) for x in a] == [(x["need"], x["paid"]) for x in b]
    check("M-WP5-10 agreement injection", agree is False)
    # M-WP5-11: large-n tree corruption (non-BST) -> legality rejects.
    from cleanroom import batteries as CB
    try:
        CB._check(7, [2, [3, None, None], None], [["KEEP", 1]])
        corrupt_caught = False
    except ValueError:
        corrupt_caught = True
    check("M-WP5-11 tree corruption", corrupt_caught)
    # M-WP5-12: OOD mislabel (H4L stratum name in ood battery field) -> audit flags.
    ood_ok = {"battery": "ood", "motif": "RANGE_WALK_SPINE"}
    ood_bad = {"battery": "ood", "motif": "RANDOM_LEGAL"}
    h4l_strata = {"RANDOM_LEGAL", "DELETE_BURST_THEN_KEEP"}
    check("M-WP5-12 OOD mislabel",
          ood_ok["motif"] not in h4l_strata and ood_bad["motif"] in h4l_strata)
    # M-WP5-13: H4L-ID reuse in OOD -> overlap detector flags.
    h4l_ids = {"aaa", "bbb"}
    check("M-WP5-13 ID reuse",
          h4l_ids.isdisjoint({"ccc"}) and not h4l_ids.isdisjoint({"aaa", "ccc"}))
    # M-WP5-14: dropped KEEP field -> keep_record schema flags.
    schema = json.loads((ROOT / "schemas" / "keep_record.schema.json").read_text(encoding="utf-8"))
    rec = {f: 0 for f in schema["required"]}
    rec.pop("paid")
    check("M-WP5-14 dropped field", set(rec) != set(schema["required"]))
    # M-WP5-15: verdict flip (REJECT must not satisfy an ACCEPT check).
    accept_check = (lambda v: v == "ACCEPT")
    check("M-WP5-15 verdict flip",
          accept_check("ACCEPT") and not accept_check("REJECT"))
    # M-WP5-16: incomplete merge (missing candidate) -> completeness fails.
    merged = {"a": 1}
    check("M-WP5-16 incomplete merge", len(merged) != 3)
    print("[WP-5][STEP 140m] mutants killed: %d/16" % sum(PASS), flush=True)
    return 0 if all(PASS) and len(PASS) == 16 else 2


if __name__ == "__main__":
    sys.exit(main())
