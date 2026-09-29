"""WP-6 STEP SD-00: single-omission damage (SOD-3 kill-hunt + reconvergence).

SOD-3: E(W,T) <= E(W,S_x(T)) + 3*d(T,x) for ALL T,x,W (E = total StepEvs).
damage(T,x,W) = E(W,T) - E(W,S_xT) - 3*d. Kill: damage > 0.
W[0]=x is trivial (L synchronizes immediately, damage=-2d); interesting W
has W[0]!=x (divergent start). Reconvergence test: same-W pair from T,T':
do trees resynchronize (when/how fast)? Persistent O(1)/access difference
=> damage linear in |W| => SOD-3 FALSE. Damage-vs-|W| decides.
Shapes: vines/balanced/shuffled; W: alternating/extremes/repeats/long.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def exec_count(t, W):
    """Total StepEvs executing key-sequence W from tree t (returns cost, tree)."""
    c = 0
    cur = t
    for x in W:
        cur, evs = PE.splay_trace(cur, x)
        c += len(evs)
    while cur["p"] is not None:
        cur = cur["p"]
    return c, cur


def canon(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def main() -> int:
    # WP-6 STEP SD-00: SOD-3 hunt + reconvergence.
    step("SD-00", "Single-omission damage hunt + reconvergence")
    import hashlib
    import random

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"sd|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    def shuffled_shape(n, seed):
        r = random.Random(seed)
        ks = list(range(1, n + 1))
        r.shuffle(ks)
        t = None

        def ins(t, k):
            if t is None:
                return [k, None, None]
            if k < t[0]:
                t[1] = ins(t[1], k)
            else:
                t[2] = ins(t[2], k)
            return t

        for k in ks:
            t = ins(t, k)
        return t

    worst = -10**18
    ex = None
    n_reconv = []
    n_noreconv = 0
    n_cases = 0
    for t in range(400):
        rng = DRBG(("sd%d" % t).encode())
        n = rng.ch([8, 16, 32])
        shape = rng.below(3)
        if shape == 0:
            T0 = vine(n, rng.below(2) == 0)
        elif shape == 1:
            # balanced-ish: median root recursion
            def bal(ks):
                if not ks:
                    return None
                m = len(ks) // 2
                return [ks[m], bal(ks[:m]), bal(ks[m + 1:])]

            T0 = bal(list(range(1, n + 1)))
        else:
            T0 = shuffled_shape(n, 5000 + t)
        x = rng.ir(1, n)
        # W variants: alternating extremes / repeats / random long / pump-like
        wv = rng.below(4)
        L = rng.ir(4, 40)
        if wv == 0:
            W = [1, n] * (L // 2 + 1)
            W = W[:L]
        elif wv == 1:
            W = [x] * L
        elif wv == 2:
            a = rng.ir(1, n)
            b = rng.ir(1, n)
            W = [a, b] * (L // 2 + 1)
            W = W[:L]
        else:
            W = [rng.ir(1, n) for _ in range(L)]
        if W and W[0] == x:
            W[0] = 1 if x != 1 else n
        T = to_ptr(T0)
        Tp, evx = PE.splay_trace(to_ptr(T0), x)
        d = len(evx)
        cL, TL = exec_count(to_ptr(T0), W)
        cR, TR = exec_count(Tp, W)  # R starts from S_x(T) (Tp already rooted)
        dmg = cL - cR - 3 * d
        if dmg > worst:
            worst, ex = dmg, (t, n, shape, x, wv, L, d, cL, cR)
        # reconvergence: same trees after full W?
        if canon(TL) == canon(TR):
            # find first sync index (replay prefix comparison is costly;
            # record sync-at-end only + cost-difference profile skip)
            n_reconv.append(L)
        else:
            n_noreconv += 1
        n_cases += 1
    step("SD-01", "cases=%d worst damage=%d %s (want<=0)" % (n_cases, worst, ex))
    step("SD-01", "resync-at-end=%d/%d; never-resync=%d" %
         (len(n_reconv), n_cases, n_noreconv))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "sod3.json").write_text(
        json.dumps({"cases": n_cases, "worst_damage": worst, "ex": ex,
                    "resync": len(n_reconv), "noresync": n_noreconv},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
