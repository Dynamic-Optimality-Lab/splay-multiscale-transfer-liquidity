"""WP-3 STEP 90 + WP-3 REPAIR STEP R2-04: independent verifier.

Different code path from the generator (no shared helpers): re-derives everything
from secret bytes + public commitment. Never evaluates candidates. Enforces the
frozen rules: history lengths 2..8, recomputed episode IDs, sorted canonical order,
shard order, per-shard SHA, logical-stream recompute, quotas/legality, commitment
recompute. Any violation fails closed (False). Malformed hash or unsorted shard
must fail.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

HIST_MIN, HIST_MAX = 2, 8


def _keys(t):
    if t is None:
        return []
    k, l, r = t
    return _keys(l) + [k] + _keys(r)


def _valid_bst(t, lo=0, hi=10 ** 9):
    if t is None:
        return True
    k, l, r = t
    return lo < k < hi and _valid_bst(l, lo, k) and _valid_bst(r, k, hi)


def canonical_id(ep: dict) -> str:
    """WP-3 REPAIR STEP R2-04: episode ID recomputed from canonical contents."""
    content = {k: v for k, v in ep.items() if k != "hash"}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()


def check_episode(ep: dict) -> None:
    """WP-3 REPAIR STEP R2-04: per-episode frozen-rule audit; raises on violation."""
    if set(ep) != {"size", "stratum", "shape", "T0", "H", "hash"}:
        raise ValueError("episode keys %r" % sorted(ep))
    if not (_valid_bst(ep["T0"]) and all(1 <= k <= ep["size"] for k in _keys(ep["T0"]))):
        raise ValueError("illegal tree")
    if not all(m in ("KEEP", "DELETE") and 1 <= x <= ep["size"] for m, x in ep["H"]):
        raise ValueError("illegal history step")
    if not (HIST_MIN <= len(ep["H"]) <= HIST_MAX):
        raise ValueError("history length %d outside frozen 2..8" % len(ep["H"]))
    if ep["hash"] != canonical_id(ep):
        raise ValueError("stored episode ID != recomputed canonical ID")


def check_sorted(ids: list[str]) -> None:
    """WP-3 REPAIR STEP R2-04: strict ascending canonical order; raises if unsorted."""
    if any(b <= a for a, b in zip(ids, ids[1:])):
        raise ValueError("episode IDs not in required sorted order")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate episode IDs")


def verify(secret_dir: Path, commitment_path: Path) -> bool:
    """WP-3 STEP 90: returns True iff commitment + schema + legality + counts verify."""
    print("[WP-3][STEP 90] Verifying H4L bank against commitment")
    try:
        return _verify(secret_dir, commitment_path)
    except Exception as e:  # WP-5 REPAIR: any verification error (incl. corrupt
        print("[WP-3][REPAIR STEP R2-04] VERIFY FAIL: %s: %s"  # compression) fails closed.
              % (type(e).__name__, e))
        return False


def _verify(secret_dir: Path, commitment_path: Path) -> bool:
    com = json.loads(commitment_path.read_text(encoding="utf-8"))
    man = json.loads((secret_dir / "manifest.json").read_text(encoding="utf-8"))
    seed = (secret_dir / "seed.bin").read_bytes()
    if len(seed) != 32:
        raise ValueError("seed is not 256-bit")
    # WP-3 REPAIR STEP R2-04: shard order must be canonical (sorted by name).
    names = [s["name"] for s in man["shards"]]
    if names != sorted(names):
        raise ValueError("shard order not canonical")
    # Commitment recompute: sha256(seed || shards in canonical order).
    h = hashlib.sha256()
    h.update(seed)
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        blob = (secret_dir / "bank" / sh["name"]).read_bytes()
        if hashlib.sha256(blob).hexdigest() != sh["sha256"]:
            raise ValueError("per-shard SHA mismatch for %s" % sh["name"])
        h.update(blob)
    ok = h.hexdigest() == com["commitment"]
    print("[WP-3][STEP 90] commitment recompute: %s" % ("OK" if ok else "FAIL"))
    if not ok:
        return False
    # Per-episode schema + legality + ID + order audit, logical stream recompute.
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
            check_episode(ep)
            if ep["hash"] in seen:
                raise ValueError("duplicate episode ID across shards")
            seen.add(ep["hash"])
            ids.append(ep["hash"])
            logical.update(ep["hash"].encode())
            qk = "%d|%s" % (ep["size"], ep["stratum"])
            quotas[qk] = quotas.get(qk, 0) + 1
            total += 1
        check_sorted(ids)  # WP-3 REPAIR STEP R2-04: unsorted shard fails
    if logical.hexdigest() != man["logical_stream_sha256"]:
        raise ValueError("logical-stream SHA mismatch vs manifest")
    if logical.hexdigest() != com["logical_stream_sha256"]:
        raise ValueError("logical-stream SHA mismatch vs commitment")
    # Commitment self-consistency (no hardcoded totals; HOLD-01/13 bind prereg params).
    if not (total == com["total"] == com["per_size"] * len(com["sizes"])):
        raise ValueError("count inconsistency total=%d" % total)
    if sum(quotas.values()) != total:
        raise ValueError("quota sum inconsistency")
    if quotas != com["quotas"]:
        raise ValueError("quota table mismatch vs commitment")
    print("[WP-3][REPAIR STEP R2-04] episodes=%d order+IDs+shards+logical OK" % total)
    return True


if __name__ == "__main__":
    sys.exit(0 if verify(Path(sys.argv[1]), Path(sys.argv[2])) else 2)
