"""WP-3 STEP 80: H4L target-blind generator (frozen contract implementation).

Contract: prereg/h4l_holdout.yaml. Blindness: inputs are (seed, size, stratum,
counter) ONLY. No candidate/pool/rho/solver/kill information exists in this module.
RNG: SHA-256 counter DRBG, domain-separated per stream.

WP-3 REPAIR STEP R2-01: randbelow is exact-uniform via deterministic rejection
sampling (no modulo bias). WP-3 REPAIR STEP R2-02: every stratum returns exactly
the once-sampled L in 2..8, motif preserved. Episode ID = sha256(canonical
content JSON); shards serialize episodes sorted by ID (see seal_h4l.py).
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

SIZES = [18, 26, 34, 46, 58, 74, 98]
PER_SIZE = 10000
STRATA = ["RANDOM_LEGAL", "DELETE_BURST_THEN_KEEP", "DOUBLE_DELETE_DOUBLE_KEEP",
          "ALTERNATING_KEEP_DELETE", "REPEATED_KEEP_DRAIN", "SPINE_VS_BALANCED",
          "OPPOSITE_SPINE", "DOUBLE_ROTATION_ENRICHED", "TERMINAL_ZIG_ENRICHED",
          "NESTED_INTERVAL", "MIRROR_PAIRED", "MOTIF_BLIND_RANDOM_WALK"]
# WP-3 STEP 80: deterministic quota schedule (833 each + first 4 strata +1 = 10000).
QUOTA = {s: 833 + (1 if i < 4 else 0) for i, s in enumerate(STRATA)}
assert sum(QUOTA.values()) == PER_SIZE
HIST_MIN, HIST_MAX = 2, 8
SHAPES = ("balanced", "vine-right", "vine-left", "random-bst")
# WP-3 STEP 81: per-stratum tree-shape mix (structural only).
SHAPE_MIX = {
    "RANDOM_LEGAL": ("random-bst", "balanced", "vine-right", "vine-left"),
    "DELETE_BURST_THEN_KEEP": ("balanced", "random-bst", "vine-right", "vine-left"),
    "DOUBLE_DELETE_DOUBLE_KEEP": ("balanced", "vine-right", "vine-left", "random-bst"),
    "ALTERNATING_KEEP_DELETE": ("random-bst", "balanced", "vine-right", "vine-left"),
    "REPEATED_KEEP_DRAIN": ("balanced", "vine-right", "random-bst", "vine-left"),
    "SPINE_VS_BALANCED": ("vine-right", "balanced", "vine-right", "balanced"),
    "OPPOSITE_SPINE": ("vine-left", "balanced", "vine-left", "balanced"),
    "DOUBLE_ROTATION_ENRICHED": ("random-bst", "vine-right", "vine-left", "balanced"),
    "TERMINAL_ZIG_ENRICHED": ("random-bst", "vine-left", "vine-right", "balanced"),
    "NESTED_INTERVAL": ("balanced", "random-bst", "vine-right", "vine-left"),
    "MIRROR_PAIRED": ("balanced", "vine-right", "vine-left", "random-bst"),
    "MOTIF_BLIND_RANDOM_WALK": ("random-bst", "balanced", "vine-right", "vine-left"),
}


class DRBG:
    """WP-3 STEP 82 + WP-3 REPAIR STEP R2-01: SHA-256 counter DRBG with
    exact-uniform rejection sampling. Deterministic: block counter advances on
    every draw attempt, so identical (seed, stream) replays identically."""

    def __init__(self, seed: bytes, stream: bytes):
        self.seed = seed
        self.stream = stream
        self.ctr = 0

    def _block(self) -> bytes:
        self.ctr += 1
        return hashlib.sha256(self.seed + b"|" + self.stream + b"|" + self.ctr.to_bytes(8, "big")).digest()

    def randbelow(self, n: int) -> int:
        # WP-3 REPAIR STEP R2-01: reject blocks >= bound so v % n is exactly uniform.
        assert n > 0
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self._block(), "big")
            if v < bound:
                return v % n

    def choice(self, seq):
        return seq[self.randbelow(len(seq))]

    def randint(self, lo: int, hi: int):
        return lo + self.randbelow(hi - lo + 1)


def build_tree(shape: str, n: int, rng: DRBG):
    """WP-3 STEP 83: structural tree builder (nested [k, L, R], null leaves)."""
    if shape == "balanced":
        return _balanced(list(range(1, n + 1)))
    if shape == "vine-right":
        t = None
        for k in range(n, 0, -1):
            t = [k, None, t]
        return t
    if shape == "vine-left":
        t = None
        for k in range(1, n + 1):
            t = [k, t, None]
        return t
    if shape == "random-bst":
        keys = list(range(1, n + 1))
        for i in range(n - 1, 0, -1):
            j = rng.randbelow(i + 1)
            keys[i], keys[j] = keys[j], keys[i]
        t = None
        for k in keys:
            t = _insert(t, k)
        return t
    raise ValueError(shape)


def _balanced(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], _balanced(keys[:m]), _balanced(keys[m + 1:])]


def _insert(t, k):
    if t is None:
        return [k, None, None]
    if k < t[0]:
        return [t[0], _insert(t[1], k), t[2]]
    return [t[0], t[1], _insert(t[2], k)]


def _depths(t, d=0, out=None):
    if out is None:
        out = {}
    if t is None:
        return out
    out[t[0]] = d
    _depths(t[1], d + 1, out)
    _depths(t[2], d + 1, out)
    return out


def gen_history(stratum: str, n: int, T0, rng: DRBG, L: int | None = None):
    """WP-3 STEP 84 + WP-3 REPAIR STEP R2-02: per-stratum history templates.

    L is sampled exactly once from exact-uniform {2..8} when not forced; every
    branch returns exactly L entries while preserving its stratum motif.
    """
    if L is None:
        L = rng.randint(HIST_MIN, HIST_MAX)
    assert HIST_MIN <= L <= HIST_MAX, L
    K = lambda: rng.randint(1, n)
    if stratum == "RANDOM_LEGAL":
        return [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(L)]
    if stratum == "DELETE_BURST_THEN_KEEP":
        # WP-3 REPAIR STEP R2-02: burst d in 1..L-1, then keeps; total exactly L.
        d = 1 + rng.randbelow(L - 1)
        return [["DELETE", K()] for _ in range(d)] + [["KEEP", K()] for _ in range(L - d)]
    if stratum == "DOUBLE_DELETE_DOUBLE_KEEP":
        # WP-3 REPAIR STEP R2-02: 4-core opens, periodic extension, truncated to L.
        a = rng.randint(1, n - 1)
        core = [["DELETE", a], ["DELETE", a + 1], ["KEEP", a + 1], ["KEEP", a]]
        ext = [["KEEP", a + 1], ["KEEP", a], ["DELETE", a + 1], ["DELETE", a]]
        return (core + ext * ((L // 4) + 1))[:L]
    if stratum == "ALTERNATING_KEEP_DELETE":
        # WP-3 REPAIR STEP R2-02: direct alternation of exactly L.
        return [[["KEEP", "DELETE"][i % 2], K()] for i in range(L)]
    if stratum == "REPEATED_KEEP_DRAIN":
        # WP-3 REPAIR STEP R2-02: L-1 repeats on x, then drain to y.
        x = K()
        y = min(n, x + 1)
        return [["KEEP", x]] * (L - 1) + [["KEEP", y]]
    if stratum in ("SPINE_VS_BALANCED", "OPPOSITE_SPINE"):
        return [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(L)]
    if stratum == "MIRROR_PAIRED":
        # WP-3 REPAIR STEP R2-02: mirrored halves around an optional center; total L.
        j = L // 2
        A = [[rng.choice(["KEEP", "DELETE"]), K()] for _ in range(j)]
        mid = [[rng.choice(["KEEP", "DELETE"]), K()]] if L % 2 else []
        return [[m, n + 1 - x] for m, x in A] + mid + [[m, x] for m, x in A]
    if stratum in ("DOUBLE_ROTATION_ENRICHED", "TERMINAL_ZIG_ENRICHED"):
        depths = _depths(T0)
        deep = [k for k, d in depths.items() if d >= 3] or list(range(1, n + 1))
        odd = [k for k, d in depths.items() if d % 2 == 1] or list(range(1, n + 1))
        pool = deep if stratum == "DOUBLE_ROTATION_ENRICHED" else odd
        return [[rng.choice(["KEEP", "DELETE"]), rng.choice(pool)] for _ in range(L)]
    if stratum == "NESTED_INTERVAL":
        # WP-3 REPAIR STEP R2-02: expanding nested offsets around c, exactly L.
        c = rng.randint(3, n - 2)
        offs = [0]
        dd = 1
        while len(offs) < L:
            offs += [-dd, dd]
            dd += 1
        H = []
        for i, o in enumerate(offs[:L]):
            x = min(n, max(1, c + o))
            H.append([["KEEP", "DELETE"][i % 2], x])
        return H
    if stratum == "MOTIF_BLIND_RANDOM_WALK":
        x = K()
        H = []
        for _ in range(L):
            H.append([rng.choice(["KEEP", "DELETE"]), x])
            x = min(n, max(1, x + rng.choice([-3, -2, -1, 1, 2, 3])))
        return H
    raise ValueError(stratum)


def episode_hash(ep: dict) -> str:
    """Episode ID: sha256 over canonical content JSON (excludes the stored id field)."""
    content = {k: v for k, v in ep.items() if k != "hash"}
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()


def generate_bank(seed: bytes, sizes=SIZES, quotas=None):
    """WP-3 STEP 85: full bank generation. Returns (episodes_by_size, stats)."""
    print("[WP-3][STEP 85] Generating H4L bank: sizes=%s" % (sizes,))
    quotas = quotas or QUOTA
    out = {}
    for n in sizes:
        eps = []
        seen = set()
        for s in STRATA:
            q = quotas[s]
            got = 0
            ctr = 0
            resamples = 0
            while got < q:
                ctr += 1
                rng = DRBG(seed, ("h4l|%d|%s|%d" % (n, s, ctr)).encode())
                shape = SHAPE_MIX[s][rng.randbelow(4)]
                T0 = build_tree(shape, n, rng)
                H = gen_history(s, n, T0, rng)
                ep = {"size": n, "stratum": s, "shape": shape, "T0": T0, "H": H}
                h = episode_hash(ep)
                if h in seen:
                    resamples += 1
                    if resamples > 100 * q:
                        raise RuntimeError("dedup resample cap exceeded")
                    continue
                seen.add(h)
                ep["hash"] = h
                eps.append(ep)
                got += 1
        out[n] = eps
        print("[WP-3][STEP 85] size %d: %d episodes" % (n, len(eps)))
    return out
