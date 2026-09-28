"""H5 verifier: independent audit of the secret H5 bank against its commitment.

Reuses the frozen H4L verification semantics (different code path from the
generator: no shared helpers beyond the episode-ID canonicalization already
frozen in h4l_verify). Enforces: 256-bit seed, canonical shard order,
per-shard SHA, commitment recompute sha256(seed || shards), per-episode
schema/legality/ID/order audit, logical-stream recompute, quota/total
consistency. Additionally binds bank_id == H5-R1. Never evaluates candidates.
Any violation fails closed (False).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

from holdout import h4l_verify as HV

BANK_ID_REQUIRED = "H5-R1"


def verify(secret_dir: Path, commitment_path: Path) -> bool:
    print("[H5] Verifying H5 bank against commitment")
    try:
        return _verify(secret_dir, commitment_path)
    except Exception as e:
        print("[H5] VERIFY FAIL: %s: %s" % (type(e).__name__, e))
        return False


def _verify(secret_dir: Path, commitment_path: Path) -> bool:
    com = json.loads(commitment_path.read_text(encoding="utf-8"))
    if com.get("bank_id") != BANK_ID_REQUIRED:
        raise ValueError("bank_id %r != H5-R1" % com.get("bank_id"))
    if com.get("bank") != "H5":
        raise ValueError("bank %r != H5" % com.get("bank"))
    man = json.loads((secret_dir / "manifest.json").read_text(encoding="utf-8"))
    if man.get("bank_id") != BANK_ID_REQUIRED:
        raise ValueError("manifest bank_id mismatch")
    seed = (secret_dir / "seed.bin").read_bytes()
    if len(seed) != 32:
        raise ValueError("seed is not 256-bit")
    names = [s["name"] for s in man["shards"]]
    if names != sorted(names):
        raise ValueError("shard order not canonical")
    for sh in man["shards"]:
        if not (sh["name"].startswith("h5_n") and sh["name"].endswith(".json.zst")):
            raise ValueError("H5 shard namespace violation: %s" % sh["name"])
    h = hashlib.sha256()
    h.update(seed)
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        blob = (secret_dir / "bank" / sh["name"]).read_bytes()
        if hashlib.sha256(blob).hexdigest() != sh["sha256"]:
            raise ValueError("per-shard SHA mismatch for %s" % sh["name"])
        h.update(blob)
    ok = h.hexdigest() == com["commitment"]
    print("[H5] commitment recompute: %s" % ("OK" if ok else "FAIL"))
    if not ok:
        return False
    import zstandard
    logical = hashlib.sha256()
    total, seen = 0, set()
    quotas = {}
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        dctx = zstandard.ZstdDecompressor()
        raw = dctx.decompress((secret_dir / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        lines = raw.decode("utf-8").splitlines()
        if len(lines) != sh["episodes"]:
            raise ValueError("shard episode count mismatch for %s" % sh["name"])
        ids = []
        for line in lines:
            ep = json.loads(line)
            HV.check_episode(ep)
            if ep["hash"] in seen:
                raise ValueError("duplicate episode ID across shards")
            seen.add(ep["hash"])
            ids.append(ep["hash"])
            logical.update(ep["hash"].encode())
            qk = "%d|%s" % (ep["size"], ep["stratum"])
            quotas[qk] = quotas.get(qk, 0) + 1
            total += 1
        HV.check_sorted(ids)
    if logical.hexdigest() != man["logical_stream_sha256"]:
        raise ValueError("logical-stream SHA mismatch vs manifest")
    if logical.hexdigest() != com["logical_stream_sha256"]:
        raise ValueError("logical-stream SHA mismatch vs commitment")
    if not (total == com["total"] == com["per_size"] * len(com["sizes"])):
        raise ValueError("count inconsistency total=%d" % total)
    if quotas != com["quotas"]:
        raise ValueError("quota table mismatch vs commitment")
    print("[H5] episodes=%d order+IDs+shards+logical OK" % total)
    return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if verify(Path(sys.argv[1]), Path(sys.argv[2])) else 2)
