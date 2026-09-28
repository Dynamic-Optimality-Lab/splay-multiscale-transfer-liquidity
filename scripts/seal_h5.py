"""H5 seal: one-shot fresh seed + secret bank generation + public commitment.

Reads/creates $H5_SECRET/seed.bin (os.urandom(32) exactly once). Writes bank
shards + manifest to secret dir ONLY. Writes public commitment
artifacts/v04/h5/h5_commitment.json + firewall transitions to the repo.
Single-shot: refuses if the commitment exists. Candidate-blind: never imports
solver/cleanroom/independent/candidate namespaces and never reads K6 survivor
artifacts (binding happens at reveal_h5.py bind time, not here).
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from holdout import h5_generate as G
from holdout import h5_firewall as FW
import zstandard

BRANCH_REQUIRED = "wp5x-k6c2-specialized"


def _guard_branch() -> bool:
    import subprocess
    try:
        b = subprocess.check_output(["git", "branch", "--show-current"],
                                    cwd=str(ROOT), text=True).strip()
    except Exception:
        return False
    return b == BRANCH_REQUIRED


def main() -> int:
    print("[H5] Sealing H5 bank %s (one-shot)" % G.BANK_ID)
    if not _guard_branch():
        print("[H5] Refuses: branch guard (must be %s)" % BRANCH_REQUIRED)
        return 2
    secret = FW._default_secret()
    com_p = ROOT / "artifacts" / "v04" / "h5" / "h5_commitment.json"
    if com_p.exists():
        print("[H5] Commitment exists; regeneration refused")
        return 2
    st = FW.read_state()
    if st["state"] != "GENERATOR_FROZEN":
        print("[H5] Generator not frozen; refuses (state=%s)" % st["state"])
        return 2
    secret.mkdir(parents=True, exist_ok=True)
    (secret / "bank").mkdir(exist_ok=True)
    seed_p = secret / "seed.bin"
    if seed_p.exists():
        print("[H5] Refuses: seed already exists (no seed-shopping, no regen)")
        return 2
    seed_p.write_bytes(os.urandom(32))
    print("[H5] Fresh secret seed created (os.urandom, operator-held, never committed)")
    seed = seed_p.read_bytes()
    assert len(seed) == 32
    bank = G.generate_bank(seed)
    cctx = zstandard.ZstdCompressor(level=G.ZSTD_LEVEL)
    shards = []
    logical = hashlib.sha256()
    quotas = {}
    for n in G.SIZES:
        ordered = sorted(bank[n], key=lambda e: e["hash"])
        assert [e["hash"] for e in ordered] == sorted(e["hash"] for e in ordered)
        assert len({e["hash"] for e in ordered}) == len(ordered)
        lines = []
        for ep in ordered:
            line = json.dumps(ep, sort_keys=True)
            lines.append(line)
            logical.update(ep["hash"].encode())
            quotas["%d|%s" % (n, ep["stratum"])] = quotas.get("%d|%s" % (n, ep["stratum"]), 0) + 1
        raw = ("\n".join(lines)).encode()
        blob = cctx.compress(raw)
        name = "h5_n%d.json.zst" % n
        (secret / "bank" / name).write_bytes(blob)
        shards.append({"name": name, "sha256": hashlib.sha256(blob).hexdigest(),
                       "bytes": len(blob), "episodes": len(lines),
                       "zstd_level": G.ZSTD_LEVEL})
        print("[H5] shard %s: %d episodes sorted by ID, %d bytes" % (name, len(lines), len(blob)))
    man = {"bank": "H5", "bank_id": G.BANK_ID,
           "shards": sorted(shards, key=lambda s: s["name"]),
           "logical_stream_sha256": logical.hexdigest(),
           "generator": G.generator_hash(),
           "inherited_h4l_generator_sha256": G.inherited_hash()}
    (secret / "manifest.json").write_text(json.dumps(man, indent=2, sort_keys=True), encoding="utf-8")
    h = hashlib.sha256()
    h.update(seed)
    for sh in sorted(shards, key=lambda s: s["name"]):
        h.update((secret / "bank" / sh["name"]).read_bytes())
    total = sum(s["episodes"] for s in shards)
    com = {"bank": "H5", "bank_id": G.BANK_ID,
           "commitment": h.hexdigest(), "total": total,
           "sizes": G.SIZES, "per_size": G.PER_SIZE, "quotas": quotas,
           "shards": [{"name": s["name"], "sha256": s["sha256"]} for s in shards],
           "logical_stream_sha256": man["logical_stream_sha256"],
           "generator_sha256": man["generator"],
           "inherited_h4l_generator_sha256": man["inherited_h4l_generator_sha256"],
           "strata": G.STRATA, "seed_status": "OPERATOR_SECRET (never in repo)"}
    (ROOT / "artifacts" / "v04" / "h5").mkdir(parents=True, exist_ok=True)
    com_p.write_text(json.dumps(com, indent=2, sort_keys=True), encoding="utf-8")
    FW.transition("BANK_GENERATED_SECRET", "70k H5 episodes to secret storage")
    FW.transition("COMMITMENT_PUBLISHED", "H5 commitment %s" % com["commitment"][:16])
    print("[H5] Commitment published: %s" % com["commitment"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
