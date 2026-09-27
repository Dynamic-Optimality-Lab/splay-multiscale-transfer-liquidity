"""WP-3 STEP 90: independent verifier — commitment recompute + schema/legality/counts audit.

Different code path from the generator (no shared helpers): re-derives everything
from secret bytes + public commitment. Never evaluates candidates.
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


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


def verify(secret_dir: Path, commitment_path: Path) -> bool:
    """WP-3 STEP 90: returns True iff commitment + schema + legality + counts verify."""
    print("[WP-3][STEP 90] Verifying H4L bank against commitment")
    com = json.loads(commitment_path.read_text(encoding="utf-8"))
    man = json.loads((secret_dir / "manifest.json").read_text(encoding="utf-8"))
    seed = (secret_dir / "seed.bin").read_bytes()
    # Commitment recompute: sha256(seed || shards in canonical order).
    h = hashlib.sha256()
    h.update(seed)
    for sh in sorted(man["shards"], key=lambda s: s["name"]):
        h.update((secret_dir / "bank" / sh["name"]).read_bytes())
    ok = h.hexdigest() == com["commitment"]
    print("[WP-3][STEP 90] commitment recompute: %s" % ("OK" if ok else "FAIL"))
    # Per-episode schema + legality + quota audit (streaming over shards).
    import zstandard
    total, seen = 0, set()
    quotas = {}
    for sh in man["shards"]:
        dctx = zstandard.ZstdDecompressor()
        raw = dctx.decompress((secret_dir / "bank" / sh["name"]).read_bytes(), max_output_size=1 << 31)
        for line in raw.decode("utf-8").splitlines():
            ep = json.loads(line)
            assert set(ep) == {"size", "stratum", "shape", "T0", "H", "hash"}, ep.keys()
            assert _valid_bst(ep["T0"]) and all(1 <= k <= ep["size"] for k in _keys(ep["T0"]))
            assert all(m in ("KEEP", "DELETE") and 1 <= x <= ep["size"] for m, x in ep["H"])
            assert 2 <= len(ep["H"]) <= 16
            assert ep["hash"] not in seen
            seen.add(ep["hash"])
            quotas[(ep["size"], ep["stratum"])] = quotas.get((ep["size"], ep["stratum"]), 0) + 1
            total += 1
    ok = ok and total == com["total"] == 70000
    ok = ok and all(v == com["quotas"]["%d|%s" % k] for k, v in quotas.items())
    print("[WP-3][STEP 90] episodes=%d quotas_match=%s" % (total, ok))
    return ok


if __name__ == "__main__":
    sys.exit(0 if verify(Path(sys.argv[1]), Path(sys.argv[2])) else 2)
