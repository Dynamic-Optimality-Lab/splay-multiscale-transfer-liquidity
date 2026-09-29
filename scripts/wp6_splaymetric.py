"""WP-6 STEP SM-00: exact splay state graph + Delta + TSRC + lambda + hazard.

Trees: tuples (k,l,r), BST shapes on 1..n (Catalan(n) states).
Edges: T --x--> S_x(T) with StepEv cost c(T,x) (tuple splay, mirrors
legacy_embedding bottom-up cases ZIG/LL/RR/LR/RL).
Delta(U,V) = min-cost splay-word U->V (Dijkstra, directed).
  connectivity/SCCs; restrict to diagonal-reachable if needed.
TSRC GAP per (A,B,x): e_B + 3*D(B',A') - 3*e_A - 3*D(B,A) <= 0?
Lambda: intersect e_B + l*D' <= 3*e_A + l*D over 0<=l<=3 (exact interval).
Hazard H(A,B)=max_y max(0,c(B,y)-3*c(A,y)): DELETE/KEEP laws.
Pair-reachability: pair-states from diagonal via Pair-Access steps.
Escalate n while feasible; report worst GAP + argmax + equalities.
"""
from __future__ import annotations
import sys
import heapq
from pathlib import Path


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def shapes(n):
    """All BST tuples on keys lo..hi (memoized)."""
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def gen(lo, hi):
        if lo > hi:
            return (None,)
        out = []
        for r in range(lo, hi + 1):
            for l in gen(lo, r - 1):
                for rr in gen(r + 1, hi):
                    out.append((r, l, rr))
        return tuple(out)

    return list(gen(1, n))


def find(t, x):
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if x == cur[0]:
            return path
        cur = cur[1] if x < cur[0] else cur[2]
    return None


def rot_at(t, pk, right):
    """Single rotation of node pk (must have appropriate child)."""
    def rec(u):
        if u is None:
            return None
        k, l, r = u
        if k == pk:
            if right:
                xk, xl, xr = l
                return (xk, xl, (k, xr, r))
            else:
                xk, xl, xr = r
                return (xk, (k, l, xl), xr)
        return (k, rec(l), rec(r))

    return rec(t)


def splay_cost_events(t, x):
    """Bottom-up splay; return (new_tree, step_count). Mirrors legacy cases."""
    path = find(t, x)
    if path is None or path[-1][0] != x:
        return t, 0
    cur = t
    steps = 0
    # node key sequence from x upward
    keys = [u[0] for u in path]
    nodek = x
    while True:
        p = parent_of(cur, nodek)
        if p is None:
            break
        g = parent_of(cur, p)
        if g is None:
            # ZIG
            if left_child(cur, p) == nodek:
                cur = rot_at(cur, p, True)
            else:
                cur = rot_at(cur, p, False)
            steps += 1
        else:
            pl = left_child(cur, p) == nodek
            gp = left_child(cur, g) == p
            if pl and gp:
                cur = rot_at(cur, g, True)
                cur = rot_at(cur, p, True)
            elif (not pl) and (not gp):
                cur = rot_at(cur, g, False)
                cur = rot_at(cur, p, False)
            elif (not pl) and gp:
                cur = rot_at(cur, p, False)
                cur = rot_at(cur, g, True)
            else:
                cur = rot_at(cur, p, True)
                cur = rot_at(cur, g, False)
            steps += 1
    return cur, steps


def parent_of(t, k):
    if t is None or t[0] == k:
        return None
    kk, l, r = t
    if l is not None and l[0] == k:
        return kk
    if r is not None and r[0] == k:
        return kk
    if k < kk:
        return parent_of(l, k)
    # need parent key: search
    def rec(u, p):
        if u is None:
            return None
        kk2, l2, r2 = u
        if kk2 == k:
            return p
        if k < kk2:
            return rec(l2, kk2)
        return rec(r2, kk2)

    return rec(t, None)


def left_child(t, pk):
    def rec(u):
        if u is None:
            return None
        k, l, r = u
        if k == pk:
            return l[0] if l is not None else None
        f = rec(l)
        return f if f is not None else rec(r)

    return rec(t)


def main() -> int:
    # WP-6 STEP SM-00: state graph + Delta + TSRC.
    step("SM-00", "Exact splay state graph + Delta + TSRC")
    import json
    ROOT = Path(__file__).resolve().parents[1]
    out_all = {}
    for n in (4, 5, 6, 7):
        S = shapes(n)
        idx = {t: i for i, t in enumerate(S)}
        m = len(S)
        # transitions + costs
        nxt = {}
        cst = {}
        for t in S:
            for x in range(1, n + 1):
                t2, c = splay_cost_events(t, x)
                nxt[(t, x)] = t2
                cst[(t, x)] = c
        # Dijkstra from every state (directed Delta)
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
        reach = len(Delta)
        # connectivity: states reachable from first shape
        # TSRC GAP over all (A,B,x) [+ pair-reachable flag later]
        worst = -10**18
        ex = None
        neq = 0
        # lambda interval [lo,hi] intersected
        lo, hi = 0.0, 3.0
        from fractions import Fraction
        loF, hiF = Fraction(0), Fraction(3)
        for A in S:
            for B in S:
                if (B, A) not in Delta:
                    continue
                dBA = Delta[(B, A)]
                for x in range(1, n + 1):
                    Ap = nxt[(A, x)]
                    Bp = nxt[(B, x)]
                    eA = cst[(A, x)]
                    eB = cst[(B, x)]
                    if (Bp, Ap) not in Delta:
                        continue
                    dBA2 = Delta[(Bp, Ap)]
                    gap = eB + 3 * dBA2 - 3 * eA - 3 * dBA
                    if gap > worst:
                        worst = gap
                        ex = {"A": str(A), "B": str(B), "x": x,
                              "eA": eA, "eB": eB, "dBA": dBA, "dBA2": dBA2}
                    if gap == 0:
                        neq += 1
                    # lambda: eB + l*dBA2 <= 3*eA + l*dBA
                    # (dBA2-dBA)*l <= 3*eA-eB
                    dd = dBA2 - dBA
                    rhs = 3 * eA - eB
                    if dd > 0:
                        hiF = min(hiF, Fraction(rhs, dd))
                    elif dd < 0:
                        loF = max(loF, Fraction(rhs, dd))
                    else:
                        if rhs < 0:
                            loF, hiF = Fraction(1), Fraction(0)  # infeasible
        step("SM-n%d" % n, "states=%d pairs=%d worstGAP=%s eq=%d lambda=[%s,%s]"
             % (m, reach, worst, neq, loF, hiF))
        out_all[str(n)] = {"states": m, "pairs": reach, "worst": worst,
                           "ex": ex, "eq": neq,
                           "lambda": [str(loF), str(hiF)]}
        if worst > 0:
            step("SM-KILL", "TSRC refuted at n=%d" % n)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "splaymetric.json").write_text(
        json.dumps(out_all, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
