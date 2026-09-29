"""WP-6 STEP RK3-00: tight-only rank check, exact steps (pointer clones).

For reward-positive KEEPs at n=32/64/128: V_1-tightness
(q + V_1(s') == V_1(s)?) + exact-steps maxAcc/hazKeys/maxHaz/divKeys deltas
iff tight. Rank survives iff NO tight rises. V_1 via clone-scans
(max over 2n accesses of immediate reward). maxAcc via clone-scans.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


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


def clone(t):
    r = t
    while r["p"] is not None:
        r = r["p"]

    def rec(u, p):
        if u is None:
            return None
        nd = PE.mknode(u["k"])
        nd["p"] = p
        nd["l"] = rec(u["l"], nd)
        nd["r"] = rec(u["r"], nd)
        return nd

    return rec(r, None)


def evcounts(t, x):
    c, _ = PE.splay_trace(clone(t), x)
    return len(c)


def V1(A, B, n):
    best = 0
    for x in range(1, n + 1):
        r = evcounts(B, x) - 3 * evcounts(A, x)
        if r > best:
            best = r
        r = -3 * evcounts(A, x)
        if r > best:
            best = r
    return best


def maxacc(A, B, n):
    best = -10**18
    for x in range(1, n + 1):
        r = evcounts(B, x) - 3 * evcounts(A, x)
        if r > best:
            best = r
    return best


def main() -> int:
    # WP-6 STEP RK3-00.
    step("RK3-00", "Tight-only rank check (exact steps)")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"rk|%s|%d" % (self.s, self.c)).digest()

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

    for n in (32, 64):
        tight_rise = 0
        tight_tot = 0
        worst = -10**18
        ex = None
        for t in range(25):
            rng = DRBG(("rk%d" % t).encode())
            T0 = vine(n, rng.below(2) == 0)
            L = rng.ir(6, 16)
            x = rng.ir(1, n)
            H = []
            for i in range(L):
                if i % 4 == 3:
                    y = min(n, max(1, x + rng.ch([-16, -8, 8, 16])))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
                x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
            pre = E.precompute(n, T0, H)
            res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
            if res["violations"]:
                step("RK3-KILL", "present kill n=%d t=%d" % (n, t))
                return 2
            A, B = to_ptr(T0), to_ptr(T0)
            for acc in pre:
                mode, xx = acc["mode"], acc["x"]
                if mode == "KEEP":
                    eA = sum(1 for z in acc["sites"] if z)
                    eB = len(acc["Bev"])
                    if eB - 3 * eA <= 0:
                        A, _ = PE.splay_trace(A, xx)
                        B, _ = PE.splay_trace(B, xx)
                        continue
                    q = eB - 3 * eA
                    v0 = V1(A, B, n)
                    m0 = maxacc(A, B, n)
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
                    v1 = V1(A, B, n)
                    m1 = maxacc(A, B, n)
                    if q + v1 == v0:
                        tight_tot += 1
                        d = m1 - m0
                        if d > 0:
                            tight_rise += 1
                        if d > worst:
                            worst, ex = d, (t, xx, eA, eB, m0, m1)
                else:
                    A, _ = PE.splay_trace(A, xx)
        step("RK3-n%d" % n, "tight=%d tight-rises=%d worst=%s %s" %
             (tight_tot, tight_rise, worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "ranktight.json").write_text(
        json.dumps({"note": "see log"}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
