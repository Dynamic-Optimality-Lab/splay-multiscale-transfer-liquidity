"""PIVOT-25R-V §2-4: canonical residual integrator on FULL graph.

States: all nS^2 BST pairs. Edges: n KEEP (D=R_B-2a-2(1-t)) + n DELETE
(D^DEL=-2a-2(t'-t), proved <=0 everywhere: asserted).
Howard max-mean (exact Fractions, adapted nbr) -> mu*; if mu*>0 STOP.
Bias h -> V = h - min(h) (proved: satisfies both Bellman checks);
fallback gaps filled + exact verify (sigma>=0 all edges; fixed point
all states). Tight graph + Tarjan SCC + stats saved.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path
from fractions import Fraction

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list


def step(sid, msg):
    print("[VIG %s] %s" % (sid, msg), flush=True)


def build(n):
    import json as J
    import wp6_cycle_ratio as O
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {J.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd = {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
    # adj[u] = list of (v, mode, x, D). D KEEP exact; D^DEL asserted <=0.
    adj = {}
    import random
    for ia in range(nS):
        if ia % 20 == 0:
            step("G", "build ia=%d/%d" % (ia, nS))
        for ib in range(nS):
            u = ia * nS + ib
            el = []
            t = 1 if rt[ia] == rt[ib] else 0
            for x in range(1, n + 1):
                rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
                ia2 = idx[J.dumps(rep["endA"], sort_keys=True)]
                ib2 = idx[J.dumps(rep["endB"], sort_keys=True)]
                a = (dd[ia][x] + 1) // 2
                d = R_static(Sh[ib], x) - 2 * a - 2 * (1 - t)
                el.append((ia2 * nS + ib2, "K", x, d))
                rep2 = V.replay(Sh[ia], Sh[ib], [("D", x)])
                ja2 = idx[J.dumps(rep2["endA"], sort_keys=True)]
                t2 = 1 if rep2["endA"][0] == Sh[ib][0] else 0
                dd2 = R_static(Sh[ib], x)  # unused (B frozen, sanity)
                ddel = -2 * a - 2 * (t2 - t)
                assert ddel <= 0, (ia, ib, x, a, t, t2)
                el.append((ja2 * nS + ib, "D", x, ddel))
            adj[u] = el
    return Sh, nS, adj


def howard(adj, Vcount, N, maxit=300, seed=0):
    import random
    rng = random.Random(seed)
    pi = [0] * Vcount
    for u in range(Vcount):
        best, bk = None, 0
        for k, (_, _, _, w) in enumerate(adj[u]):
            if best is None or w > best:
                best, bk = w, k
        pi[u] = bk
    mu_num, mu_den = None, None
    h = [None] * Vcount
    for it in range(maxit):
        # evaluate: cycles under pi
        seen = {}
        cycs = []
        for s in range(Vcount):
            u = s
            path = []
            pos = {}
            while u not in pos and u not in seen:
                pos[u] = len(path)
                path.append(u)
                u = adj[u][pi[u]][0]
            if u in pos:
                cycs.append(path[pos[u]:])
            for w in path:
                seen[w] = True
        mu_num, mu_den = None, None
        for cyc in cycs:
            tot = sum(adj[w][pi[w]][3] for w in cyc)
            L = len(cyc)
            if mu_num is None or tot * mu_den > mu_num * L:
                mu_num, mu_den = tot, L
        # values backward from max-mean cycles
        h = [None] * Vcount
        rev = [[] for _ in range(Vcount)]
        for u in range(Vcount):
            rev[adj[u][pi[u]][0]].append(u)
        from collections import deque
        dq = deque()
        for cyc in cycs:
            tot = sum(adj[w][pi[w]][3] for w in cyc)
            L = len(cyc)
            if tot * mu_den == mu_num * L:
                rep = min(cyc)
                if h[rep] is None:
                    h[rep] = Fraction(0)
                    dq.append(rep)
        while dq:
            v = dq.popleft()
            for u in rev[v]:
                if h[u] is None:
                    to, _, _, w = adj[u][pi[u]]
                    assert to == v
                    h[u] = Fraction(w) - Fraction(mu_num, mu_den) + h[v]
                    dq.append(u)
        switches = 0
        for u in range(Vcount):
            cur = None if h[u] is None else Fraction(mu_num, mu_den) + h[u]
            best, bk = cur, pi[u]
            for k, (to, _, _, w) in enumerate(adj[u]):
                if h[to] is None:
                    continue
                val = Fraction(w) + h[to]
                if best is None or val > best:
                    best, bk = val, k
            if bk != pi[u]:
                pi[u] = bk
                switches += 1
        step("IT-%d" % it, "mu=%s/%s switches=%d" %
             (mu_num, mu_den, switches))
        if switches == 0:
            break
    return (mu_num, mu_den), pi, h


def main():
    import sys as _s
    import json as J
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh, nS, adj = build(n)
    Vcount = nS * nS
    step("G", "n=%d states=%d edges=%d (KEEP+DELETE)" %
         (n, Vcount, sum(len(v) for v in adj.values())))
    (mu_num, mu_den), pi, h = howard(adj, Vcount, 2 * n)
    step("H", "max-mean mu=%s/%s" % (mu_num, mu_den))
    if mu_num > 0:
        step("H", "POSITIVE-D CYCLE: profile approach IMPOSSIBLE. STOP.")
        (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
         "dual_mine" / ("vfull%d.json" % n)).write_text(
            J.dumps({"mu": [mu_num, mu_den], "infeasible": True},
                    indent=1), encoding="utf-8")
        return 2
    gaps = sum(1 for v in h if v is None)
    step("H", "bias gaps (None): %d/%d" % (gaps, Vcount))
    m = min(v for v in h if v is not None)
    # fill gaps (if any) by longest-path reverse BFS from decided states
    from collections import deque
    rev = [[] for _ in range(Vcount)]
    for u in range(Vcount):
        for (to, _, _, _) in adj[u]:
            rev[to].append(u)
    dq = deque([v for v in range(Vcount) if h[v] is not None])
    inset = set(dq)
    while dq:
        v = dq.popleft()
        for u in rev[v]:
            if h[u] is None:
                # longest incoming: max over decided successors
                best = None
                for (to, _, _, w) in adj[u]:
                    if h[to] is not None:
                        c = Fraction(w) + h[to]
                        if best is None or c > best:
                            best = c
                if best is not None:
                    h[u] = best
                    dq.append(u)
    gaps2 = sum(1 for v in h if v is None)
    step("H", "after fill gaps: %d" % gaps2)
    assert gaps2 == 0
    m = min(h)
    Vf = [v - m for v in h]
    # exact verify: sigma>=0 all edges; fixed point all states
    bad = 0
    for u in range(Vcount):
        for (to, _, _, w) in adj[u]:
            if Vf[u] - Vf[to] - w < 0:
                bad += 1
    step("V", "sigma violations: %d/%d" %
         (bad, sum(len(v) for v in adj.values())))
    badfp = 0
    for u in range(Vcount):
        rhs = 0
        for (to, _, _, w) in adj[u]:
            if w + Vf[to] > rhs:
                rhs = w + Vf[to]
        if Vf[u] != rhs:
            badfp += 1
    step("V", "fixed-point violations: %d/%d" % (badfp, Vcount))
    assert bad == 0 and badfp == 0
    from collections import Counter
    hist = Counter(int(v) for v in Vf)
    step("V", "V range=[%d,%d] zeros=%d distinct=%d" %
         (min(Vf), max(Vf), hist[0], len(hist)))
    # tight graph
    tight = [[] for _ in range(Vcount)]
    nt = 0
    for u in range(Vcount):
        for (to, mo, x, w) in adj[u]:
            if Vf[u] - Vf[to] - w == 0:
                tight[u].append((to, mo, x, w))
                nt += 1
    step("T", "tight edges=%d" % nt)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("vfull%d.json" % n)).write_text(
        J.dumps({"mu": [mu_num, mu_den], "Vmin": int(min(Vf)),
                 "Vmax": int(max(Vf)), "zeros": hist[0],
                 "distinct": len(hist), "tight": nt,
                 "V": [int(v) for v in Vf]}, indent=1), encoding="utf-8")
    step("S", "saved vfull%d.json" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
