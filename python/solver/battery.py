"""WP-4 STEP 113: dev + validation batteries (seeded structural, deterministic).

Own SHA-256 DRBG with domain-separated streams (never the H4L generator, never
H4L bytes). REG-001 + REG-FAM-001 labeled KNOWN/CONTAMINATED and placed FIRST so
the funnel kills early. Validation uses a disjoint stream; ID-disjointness from
dev is recorded and asserted (SYN-04). OOD is never generated here.
"""
from __future__ import annotations
import hashlib
import json

from solver import legality as LG

DEV_SIZES = [8, 16, 32]
VAL_SIZES = [7, 8, 10, 12, 16]
VAL_PER_SIZE = 1000
MOTIFS = ("DDKK", "DELETE_BURST", "KEEP_DRAIN", "ALTERNATING", "BOUNDARY",
          "MIRROR", "SPINE_MIX", "NESTED", "REPEAT_DELETE", "RANDOM_LEGAL")


class DRBG:
    """WP-4 STEP 113: exact-uniform SHA-256 counter DRBG (rejection sampling)."""

    def __init__(self, seed: bytes, stream: bytes):
        self.seed = seed
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


SEED = b"wp4-battery-frozen-v1"


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


def _random_bst(n, rng):
    keys = list(range(1, n + 1))
    for i in range(n - 1, 0, -1):
        j = rng.below(i + 1)
        keys[i], keys[j] = keys[j], keys[i]
    t = None
    for k in keys:
        t = _insert(t, k)
    return t


def _tree(shape, n, rng):
    if shape == "balanced":
        return _balanced(list(range(1, n + 1)))
    if shape == "vine-right":
        return _vine_right(n)
    if shape == "vine-left":
        return _vine_left(n)
    return _random_bst(n, rng)


def _motif_history(motif, n, rng):
    K = lambda: rng.irange(1, n)
    L = rng.irange(2, 8)
    if motif == "DDKK":
        a = rng.irange(1, n - 1)
        return [["DELETE", a], ["DELETE", a + 1], ["KEEP", a + 1], ["KEEP", a]]
    if motif == "DELETE_BURST":
        d = rng.irange(2, 5)
        return [["DELETE", K()] for _ in range(d)] + [["KEEP", K()] for _ in range(max(1, L - d))]
    if motif == "KEEP_DRAIN":
        x = K()
        return [["KEEP", x]] * rng.irange(3, 5) + [["KEEP", min(n, x + 1)]]
    if motif == "ALTERNATING":
        return [[["KEEP", "DELETE"][i % 2], K()] for i in range(max(4, L))]
    if motif == "BOUNDARY":
        return [[rng.choice(["KEEP", "DELETE"]), rng.choice([1, n])] for _ in range(L)]
    if motif == "MIRROR":
        H = [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(L)]
        return [[m, n + 1 - x] for m, x in H] + [[m, x] for m, x in H]
    if motif == "SPINE_MIX":
        return [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(L)]
    if motif == "NESTED":
        c = rng.irange(3, n - 2)
        seq = [c, c - 1, c + 1, c - 2, c + 2][:L]
        return [["KEEP" if i % 2 == 0 else "DELETE", x] for i, x in enumerate(seq)]
    if motif == "REPEAT_DELETE":
        x = K()
        return [["DELETE", x]] * rng.irange(2, 6) + [["KEEP", x]]
    return [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(L)]


def _mk(n, T0, H, battery, motif, contaminated):
    LG.check(n, T0, H)
    ep = {"n": n, "T0": T0, "H": H, "battery": battery, "motif": motif,
          "contaminated": contaminated}
    ep["id"] = LG.episode_id(n, T0, H)
    return ep


def reg_family():
    """WP-4 STEP 113: immutable REG episodes (KNOWN/CONTAMINATED), always first."""
    out = [_mk(28, _vine_right(28),
               [["DELETE", 27], ["DELETE", 28], ["KEEP", 28], ["KEEP", 27]],
               "dev", "REG-001", True)]
    for n in (8, 16, 32, 64):
        a = n // 2
        out.append(_mk(n, _vine_right(n),
                      [["DELETE", a], ["DELETE", a + 1], ["KEEP", a + 1], ["KEEP", a]],
                      "dev", "REG-FAM-001", True))
    return out


def _motif_episodes(stream: bytes, sizes, per_motif: int, battery: str, exclude=()):
    out = []
    for n in sizes:
        for motif in MOTIFS:
            made, j = 0, 0
            while made < per_motif:
                rng = DRBG(SEED, b"%s|%d|%s|%d" % (stream, n, motif.encode(), j))
                j += 1
                shape = ("balanced", "vine-right", "vine-left", "random-bst")[rng.below(4)]
                T0 = _tree(shape, n, rng)
                H = _motif_history(motif, n, rng)
                ep = _mk(n, T0, H, battery, motif, False)
                if ep["id"] in exclude or any(e["id"] == ep["id"] for e in out):
                    continue  # WP-4 STEP 113: ID-disjointness by deterministic resample
                out.append(ep)
                made += 1
    return out


def dev_screen():
    """WP-4 STEP 113: screen battery (REG first for early death)."""
    print("[WP-4][STEP 113] Building dev-screen battery", flush=True)
    eps = reg_family() + _motif_episodes(b"wp4-dev-screen", [8, 16], 6, "dev-screen")
    print("[WP-4][STEP 113] dev-screen episodes: %d" % len(eps), flush=True)
    return eps


def dev_extra(exclude=()):
    """WP-4 STEP 113: dev-full extension (disjoint stream + resample vs screen)."""
    print("[WP-4][STEP 113] Building dev-full extension", flush=True)
    eps = _motif_episodes(b"wp4-dev-full", DEV_SIZES, 20, "dev-full", exclude)
    print("[WP-4][STEP 113] dev-full extension episodes: %d" % len(eps), flush=True)
    return eps


def validation(exclude=()):
    """WP-4 STEP 113: validation split (disjoint stream + resample vs dev IDs)."""
    print("[WP-4][STEP 113] Building validation split", flush=True)
    eps = _motif_episodes(b"wp4-val", VAL_SIZES, VAL_PER_SIZE // len(MOTIFS),
                          "validation", exclude)
    assert len(eps) == VAL_PER_SIZE * len(VAL_SIZES)
    print("[WP-4][STEP 113] validation episodes: %d" % len(eps), flush=True)
    return eps


def ids(eps) -> list:
    return sorted(e["id"] for e in eps)
