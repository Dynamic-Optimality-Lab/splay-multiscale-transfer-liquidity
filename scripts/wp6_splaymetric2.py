"""WP-6 STEP SM2-00: validate tuple-splay + reachable-pair TSRC.

1. Equivalence: tuple splay_cost_events vs legacy pointer splay_trace
   (costs + canonical trees) on random (T,x), n<=16.
2. Pair-reachability: BFS pair-states (A,B) from every diagonal (T0,T0)
   via Pair-Access steps (DELETE: A-only; KEEP: both). Union over T0.
3. TSRC GAP + lambda interval on REACHABLE pairs only (n<=7).
A reachable positive GAP kills TSRC; unreachable-only gaps do not.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import shapes, splay_cost_events
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


def canon_ptr(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def canon_tup(t):
    if t is None:
        return "."
    return "(%d%s%s)" % (t[0], canon_tup(t[1]), canon_tup(t[2]))


def main() -> int:
    # WP-6 STEP SM2-00.
    step("SM2-00", "Validate tuple-splay + reachable-pair TSRC")
    import hashlib
    import random
    from collections import deque

    def R(tag, c):
        return int.from_bytes(hashlib.sha256(b"sm2|%s|%d" % (tag, c)).digest(), "big")

    # 1. equivalence
    mism = 0
    for t in range(500):
        r = R(("e%d" % t).encode(), 0)
        n = 4 + r % 13
        rr = random.Random(10000 + t)
        ks = list(range(1, n + 1))
        rr.shuffle(ks)
        T0 = None

        def ins(T, k):
            if T is None:
                return [k, None, None]
            if k < T[0]:
                T[1] = ins(T[1], k)
            else:
                T[2] = ins(T[2], k)
            return T

        for k in ks:
            T0 = ins(T0, k)

        def totup(T):
            if T is None:
                return None
            return (T[0], totup(T[1]), totup(T[2]))

        Tt = totup(T0)
        x = 1 + (r >> 7) % n
        Tt2, c = splay_cost_events(Tt, x)
        P = to_ptr(T0)
        P2, evs = PE.splay_trace(P, x)
        if c != len(evs) or canon_tup(Tt2) != canon_ptr(P2):
            mism += 1
    step("SM2-01", "tuple-vs-legacy mismatches=%d/500" % mism)
    if mism:
        step("SM2-FAIL", "tuple splay wrong; TSRC numbers invalid")
        return 2
    # 2-3. reachable pairs + TSRC (n<=7)
    import heapq
    from fractions import Fraction
    for n in (4, 5, 6, 7):
        S = shapes(n)
        nxt = {}
        cst = {}
        for t in S:
            for x in range(1, n + 1):
                t2, c = splay_cost_events(t, x)
                nxt[(t, x)] = t2
                cst[(t, x)] = c
        # pair BFS from all diagonals
        seen = set()
        dq = deque()
        for t0 in S:
            seen.add((t0, t0))
            dq.append((t0, t0))
        while dq:
            A, B = dq.popleft()
            for x in range(1, n + 1):
                # DELETE x: A-only
                s = (nxt[(A, x)], B)
                if s not in seen:
                    seen.add(s)
                    dq.append(s)
                # KEEP x: both
                s = (nxt[(A, x)], nxt[(B, x)])
                if s not in seen:
                    seen.add(s)
                    dq.append(s)
        # Dijkstra Delta (reuse: full all-pairs already validated structurally;
        # recompute here for self-containment)
        INF = 10 ** 18
        Delta = {}
        for s in S:
            dist = {s: 0}
            pq = [(0, s)]
            while pq:
                d, u = heapq.heappop(pq)
                if d > dist[u]:
                    continue
                for x in range(1, n + 1):
                    v = nxt[(u, x)]
                    nd = d + cst[(u, x)]
                    if nd < dist.get(v, INF):
                        dist[v] = nd
                        heapq.heappush(pq, (nd, v))
            for t2, dd in dist.items():
                Delta[(s, t2)] = dd
        worst = -10**18
        ex = None
        loF, hiF = Fraction(0), Fraction(3)
        for (A, B) in seen:
            if (B, A) not in Delta:
                continue
            dBA = Delta[(B, A)]
            for x in range(1, n + 1):
                Ap = nxt[(A, x)]
                Bp = nxt[(B, x)]
                eA, eB = cst[(A, x)], cst[(B, x)]
                if (Bp, Ap) not in Delta:
                    continue
                d2 = Delta[(Bp, Ap)]
                gap = eB + 3 * d2 - 3 * eA - 3 * dBA
                if gap > worst:
                    worst = gap
                    ex = (str(A), str(B), x, eA, eB, dBA, d2)
                dd = d2 - dBA
                rhs = 3 * eA - eB
                if dd > 0:
                    hiF = min(hiF, Fraction(rhs, dd))
                elif dd < 0:
                    loF = max(loF, Fraction(rhs, dd))
                elif rhs < 0:
                    loF, hiF = Fraction(1), Fraction(0)
        step("SM2-n%d" % n, "reachable=%d worstGAP=%s lambda=[%s,%s] ex=%s"
             % (len(seen), worst, loF, hiF, str(ex)[:220]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
