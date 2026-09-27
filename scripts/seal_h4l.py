"""WP-3 STEP 93: one-shot H4L generation -> secret storage -> public commitment.

Reads secret seed from $H4L_SECRET/seed.bin (creates it with os.urandom once if absent).
Writes bank shards + manifest to secret dir ONLY. Writes public commitment +
firewall transitions to the repo. Single-shot: refuses if commitment exists.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import h4l_generate as G
from holdout import firewall as FW
import zstandard


def main() -> int:
    print("[WP-3][STEP 93] Sealing H4L bank (one-shot)")
    secret = Path(os.environ.get("H4L_SECRET", r"C:\Users\SAIFMA~1\AppData\Local\Temp\opencode\h4l-secret"))
    com_p = ROOT / "artifacts" / "v04" / "holdouts" / "h4l_commitment.json"
    if com_p.exists():
        print("[WP-3][STEP 93] Commitment exists; regeneration refused (LIQ-STOP-14)")
        return 2
    if FW.read_state()["state"] != "GENERATOR_FROZEN":
        print("[WP-3][STEP 93] Generator not frozen; refuses (state=%s)" % FW.read_state()["state"])
        return 2
    secret.mkdir(parents=True, exist_ok=True)
    (secret / "bank").mkdir(exist_ok=True)
    seed_p = secret / "seed.bin"
    if not seed_p.exists():
        seed_p.write_bytes(os.urandom(32))
        print("[WP-3][STEP 93] Secret seed created (operator-held, never committed)")
    seed = seed_p.read_bytes()
    assert len(seed) == 32
    bank = G.generate_bank(seed)
    cctx = zstandard.ZstdCompressor(level=3)
    shards = []
    logical = hashlib.sha256()
    quotas = {}
    for n in G.SIZES:
        lines = []
        for ep in bank[n]:
            line = json.dumps(ep, sort_keys=True)
            lines.append(line)
            logical.update(ep["hash"].encode())
            quotas["%d|%s" % (n, ep["stratum"])] = quotas.get("%d|%s" % (n, ep["stratum"]), 0) + 1
        raw = ("\n".join(lines)).encode()
        blob = cctx.compress(raw)
        name = "h4l_n%d.json.zst" % n
        (secret / "bank" / name).write_bytes(blob)
        shards.append({"name": name, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob),
                       "episodes": len(lines), "zstd_level": 3})
        print("[WP-3][STEP 93] shard %s: %d episodes, %d bytes" % (name, len(lines), len(blob)))
    man = {"shards": sorted(shards, key=lambda s: s["name"]), "logical_stream_sha256": logical.hexdigest(),
           "generator": hashlib.sha256((ROOT / "python" / "holdout" / "h4l_generate.py").read_bytes()).hexdigest()}
    (secret / "manifest.json").write_text(json.dumps(man, indent=2, sort_keys=True), encoding="utf-8")
    h = hashlib.sha256()
    h.update(seed)
    for sh in sorted(shards, key=lambda s: s["name"]):
        h.update((secret / "bank" / sh["name"]).read_bytes())
    total = sum(s["episodes"] for s in shards)
    com = {"bank": "H4L", "commitment": h.hexdigest(), "total": total,
           "sizes": G.SIZES, "per_size": G.PER_SIZE, "quotas": quotas,
           "shards": [{"name": s["name"], "sha256": s["sha256"]} for s in shards],
           "logical_stream_sha256": man["logical_stream_sha256"],
           "generator_sha256": man["generator"],
           "strata": G.STRATA, "seed_status": "OPERATOR_SECRET (never in repo)"}
    (ROOT / "artifacts" / "v04" / "holdouts").mkdir(parents=True, exist_ok=True)
    com_p.write_text(json.dumps(com, indent=2, sort_keys=True), encoding="utf-8")
    FW.transition("BANK_GENERATED_SECRET", "70k episodes to secret storage")
    FW.transition("COMMITMENT_PUBLISHED", "commitment %s" % com["commitment"][:16])
    print("[WP-3][STEP 93] Commitment published: %s" % com["commitment"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
