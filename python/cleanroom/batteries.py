"""WP-5 STEP 134: large-n + OOD batteries (seeded, deterministic, self-contained).

Large-n: sizes 16..4096 x40 (vine/balanced/random mix, short histories) with
per-KEEP diagnostics support. OOD: sizes 24/48/96/192 x2000 = 8000, long-range
random-walk histories + spine-heavy trees, disjoint stream, labeled OOD (never
fresh-holdout). Own DRBG; never H4L bytes, never H4L streams.
"""
from __future__ import annotations
import hashlib

LARGE_SIZES = [16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
LARGE_PER_SIZE = 40
OOD_SIZES = [24, 48, 96, 192]
OOD_PER_SIZE = 2000


class DRBG:
    """WP-5 STEP 134: battery-local exact-uniform DRBG."""

    def __init__(self, stream: bytes):
        self.seed = b"wp5-battery-frozen-v1"
        self.stream = stream
        self.ctr = 0

    def _block(self) -> bytes:
        self.ctr += 1
        return hashlib.sha256(self.seed + b"|" + self.stream + b"|"
                              + self.ctr.to_bytes(8, "big")).digest()

    def below(self, n: int) -> int:
        assert n > 0
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self._block(), "big")
            if v < bound:
                return v % n

    def irange(self, lo: int, hi: int) -> int:
        return lo + self.below(hi - lo + 1)

    def choice(self, seq):
        return seq[self.below(len(seq))]


def _balanced(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], _balanced(keys[:m]), _balanced(keys[m + 1:])]


def _vine_right(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t]
    return t


def _vine_left(n):
    t = None
    for k in range(1, n + 1):
        t = [k, t, None]
    return t


def _insert(t, k):
    if t is None:
        return [k, None, None]
    if k < t[0]:
        return [t[0], _insert(t[1], k), t[2]]
    return [t[0], t[1], _insert(t[2], k)]


def _rtree(n, rng):
    keys = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = rng.below(i + 1)
        keys[i], keys[j] = keys[j], keys[i]
    t = None
    for k in keys:
        t = _insert(t, k)
    return t


def _check(n, T0, H) -> None:
    def keys(t):
        return [] if t is None else keys(t[1]) + [t[0]] + keys(t[2])

    def bst(t, lo=0, hi=10 ** 9):
        return True if t is None else (
            lo < t[0] < hi and bst(t[1], lo, t[0]) and bst(t[2], t[0], hi))

    if not bst(T0) or any(not (1 <= k <= n) for k in keys(T0)):
        raise ValueError("illegal T0")
    for m, x in H:
        if m not in ("KEEP", "DELETE") or not (1 <= x <= n):
            raise ValueError("illegal access")


def _eid(n, T0, H) -> str:
    import json
    return hashlib.sha256(json.dumps({"n": n, "T0": T0, "H": H},
                                     sort_keys=True).encode()).hexdigest()


def _mk(n, T0, H, battery, motif):
    _check(n, T0, H)
    return {"n": n, "T0": T0, "H": H, "battery": battery, "motif": motif,
            "id": _eid(n, T0, H)}


def large_n():
    """WP-5 STEP 134: large-n attack battery (9 sizes x40)."""
    print("[WP-5][STEP 134] Building large-n battery", flush=True)
    out = []
    for n in LARGE_SIZES:
        for j in range(LARGE_PER_SIZE):
            rng = DRBG(b"wp5-large|%d|%d" % (n, j))
            shape = ("vine-right", "balanced", "random-bst")[rng.below(3)]
            T0 = {"vine-right": _vine_right(n), "vine-left": _vine_left(n),
                  "balanced": _balanced(list(range(1, n + 1)))}[shape] \
                if shape != "random-bst" else _rtree(n, rng)
            L = rng.irange(2, 6)
            H = [[rng.choice(["KEEP", "DELETE"]), rng.irange(1, n)] for _ in range(L)]
            out.append(_mk(n, T0, H, "large-n", shape))
    print("[WP-5][STEP 134] large-n episodes: %d" % len(out), flush=True)
    return out


def ood(exclude=()):
    """WP-5 STEP 134: OOD battery (4 sizes x2000 = 8000, labeled OOD)."""
    print("[WP-5][STEP 134] Building OOD battery", flush=True)
    out = []
    for n in OOD_SIZES:
        made, j = 0, 0
        while made < OOD_PER_SIZE:
            rng = DRBG(b"wp5-ood|%d|%d" % (n, j))
            j += 1
            # Spine-heavy trees: vine-left/right dominate the mix.
            shape = ("vine-right", "vine-left", "vine-right", "vine-left", "balanced")[rng.below(5)]
            T0 = {"vine-right": _vine_right(n), "vine-left": _vine_left(n),
                  "balanced": _balanced(list(range(1, n + 1)))}[shape]
            # Long-range random-walk histories (distinct distribution from H4L strata).
            x = rng.irange(1, n)
            L = rng.irange(4, 10)
            H = []
            for _ in range(L):
                H.append([rng.choice(["KEEP", "DELETE"]), x])
                x = min(n, max(1, x + rng.choice([-16, -8, -4, -1, 1, 4, 8, 16])))
            ep = _mk(n, T0, H, "ood", "RANGE_WALK_SPINE")
            if ep["id"] in exclude or any(e["id"] == ep["id"] for e in out):
                continue
            out.append(ep)
            made += 1
    print("[WP-5][STEP 134] OOD episodes: %d" % len(out), flush=True)
    return out
