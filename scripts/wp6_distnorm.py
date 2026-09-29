"""WP-6 STEP ND-00: rotation-distance normalization laws (small-tree exact).

N(A,B) = exact rotation distance (BFS over BST shapes, fixed inorder).
LAW-A (DELETE x, A-only): N'-N <= 3*e_A  [triangle + R_A<=2*e_A; expect HOLD].
LAW-K (KEEP x): N'-N <= 3*e_A - e_B, i.e. dist-drop >= e_B - 3*e_A (MEASURE:
  does x-rooting-in-both resolve >= excess?).
TELESCOPE: E_B - 3*S_A + N_t <= 0? (N_0=0, N>=0).
Violation of LAW-K kills raw-dist normalization (descend: quotient/area/braid).
n<=8 present histories; unsited count (expect 0 by U=0).
"""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def tup(t):
    """Pointer tree -> nested tuple (k,l,r) with None leaves."""
    if t is None:
        return None
    r = t
    while r["p"] is not None:
        r = r["p"]

    def rec(u):
        if u is None:
            return None
        return (u["k"], rec(u["l"]), rec(u["r"]))

    return rec(r)


def rots(state):
    """All single-rotation neighbors of tuple tree (yield new tuples)."""
    # collect nodes by path
    nodes = {}

    def rec(u, p):
        if u is None:
            return
        k, l, r = u
        nodes[k] = (u, p)
        rec(l, u)
        rec(r, u)

    rec(state, None)

    def rebuild(top):
        return top

    # for each node with left child: right rotation; right child: left rotation
    out = []

    def rot_right(t, pk):
        # rotate node pk (must have left child) up
        def rec2(u):
            if u is None:
                return None
            k, l, r = u
            if k == pk:
                # u has left child x=(xk,xl,xr)
                xk, xl, xr = l
                # x up: x=(xk,xl,(k,xr,r))
                return (xk, xl, (k, xr, r))
            return (k, rec2(l), rec2(r))

        return rec2(t)

    def rot_left(t, pk):
        def rec2(u):
            if u is None:
                return None
            k, l, r = u
            if k == pk:
                xk, xl, xr = r
                return (xk, (k, l, xl), xr)
            return (k, rec2(l), rec2(r))

        return rec2(t)

    for k, (u, p) in nodes.items():
        kk, l, r = u
        if l is not None:
            out.append(rot_right(state, k))
        if r is not None:
            out.append(rot_left(state, k))
    return out


from functools import lru_cache


def bfs_dist(a, b):
    if a == b:
        return 0
    dq = deque([(a, 0)])
    seen = {a}
    while dq:
        u, d = dq.popleft()
        for w in rots(u):
            if w == b:
                return d + 1
            if w not in seen:
                seen.add(w)
                dq.append((w, d + 1))
    raise AssertionError("rotation graph disconnected?")


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


def main() -> int:
    # WP-6 STEP ND-00: rotation-distance laws.
    step("ND-00", "Rotation-distance normalization laws")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"nd|%s|%d" % (self.s, self.c)).digest()

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

    worstA = -10**18
    worstK = -10**18
    exA = exK = None
    worst_tel = -10**18
    exT = None
    unsited = 0
    n_hist = 0
    drops = []
    for t in range(200):
        rng = DRBG(("nd%d" % t).encode())
        n = rng.ch([5, 6, 7, 8])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(5, 30)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 3 == 2:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-4, -2, -1, 1, 2, 4])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ND-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        N = 0
        EB = SA = 0
        for acc in pre:
            mode, xx = acc["mode"], acc["x"]
            eA = sum(1 for z in acc["sites"] if z)
            unsited += len(acc["Aev"]) - eA
            N0 = bfs_dist(tup(B), tup(A))
            A, _ = PE.splay_trace(A, xx)
            if mode == "KEEP":
                B, _ = PE.splay_trace(B, xx)
            N1 = bfs_dist(tup(B), tup(A))
            if mode == "DELETE":
                gap = (N1 - N0) - 3 * eA
                if gap > worstA:
                    worstA, exA = gap, (t, xx, eA, N0, N1)
            else:
                eB = len(acc["Bev"])
                gap = (N1 - N0) - (3 * eA - eB)
                if gap > worstK:
                    worstK, exK = gap, (t, xx, eA, eB, N0, N1)
                drops.append((N1 - N0, eB - 3 * eA))
                EB += eB
            SA += eA
            N = N1
            tel = (EB - 3 * SA) + N
            if tel > worst_tel:
                worst_tel, exT = tel, (t, mode, xx, EB, SA, N)
        n_hist += 1
    step("ND-01", "hist=%d unsited=%d worst LAW-A gap=%s %s (want<=0)"
         % (n_hist, unsited, worstA, exA))
    step("ND-01", "worst LAW-K gap=%s %s (want<=0)" % (worstK, exK))
    step("ND-01", "worst telescope E_B-3SA+N=%s %s (want<=0)" % (worst_tel, exT))
    import statistics as _st
    pos = [d for d, x in drops if x > 0]
    step("ND-01", "excess-KEEPs=%d; dist-change on excess: min=%s med=%s max=%s" %
         (len(pos), min(pos) if pos else None,
          _st.median(pos) if pos else None, max(pos) if pos else None))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "distnorm.json").write_text(
        json.dumps({"histories": n_hist, "unsited": unsited,
                    "worst_A": worstA, "A_ex": exA,
                    "worst_K": worstK, "K_ex": exK,
                    "worst_tel": worst_tel, "tel_ex": exT},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
