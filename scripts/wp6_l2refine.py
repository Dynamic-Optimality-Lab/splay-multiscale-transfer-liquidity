"""PIVOT-25R L2: refined-summary feasibility with twin-only baseline.

Phi(s) = -2*twin(s) + P_alpha(s),  alpha(s) = (rootA, rootB, isVineB),
P_c FREE unknowns. Every concrete edge (ALL 2.58M, both modes) imposes
P[U]-P[V] >= c(e), c(e) = w(e) - 2*(twin(s')-twin(s)).
Abstract max-c per (U,V); Bellman-Ford on costs -c.
"""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[L2R %s] %s" % (sid, msg), flush=True)


def is_vine(t):
    stack = [t]
    while stack:
        nd = stack.pop()
        if nd is None:
            continue
        if nd[1] is not None and nd[2] is not None:
            return False
        stack.append(nd[1])
        stack.append(nd[2])
    return True


def path_to(t, y):
    """Root-to-y node list on list-shape (None if absent)."""
    p, nd = [], t
    while nd is not None and nd[0] != y:
        p.append(nd[0])
        nd = nd[1] if y < nd[0] else nd[2]
    if nd is None:
        return None
    p.append(y)
    return p


def lca_of(t, a, b):
    pa, sb = path_to(t, a), set(path_to(t, b))
    return next(u for u in reversed(pa) if u in sb)  # deepest-first


def maxdepth(t):
    mx = 0
    st = [(t, 0)]
    while st:
        nd, d = st.pop()
        if nd is None:
            continue
        mx = max(mx, d)
        st.append((nd[1], d + 1))
        st.append((nd[2], d + 1))
    return mx


def bf_feasible(best):
    nodes = sorted(set([u for u, _ in best] + [v for _, v in best]))
    idx = {v: i for i, v in enumerate(nodes)}
    N = len(nodes)
    E = [(idx[u], idx[v], -c) for (u, v), (c, _) in best.items()]
    dist = [0] * N
    parent = [-1] * N
    for i in range(N):
        changed = False
        for (u, v, c) in E:
            if dist[u] + c < dist[v]:
                dist[v] = dist[u] + c
                parent[v] = u
                changed = True
        if not changed:
            # dist satisfies dist[v] <= dist[u]+cost; with cost=-c this is
            # P[v] <= P[u]-c, i.e. P[u]-P[v] >= c. So P=dist (NOT -dist).
            return {"feasible": True, "passes": i + 1, "nodes": nodes,
                    "pot": {str(k): dist[idx[k]] for k in nodes}}
    y = -1
    for (u, v, c) in E:
        if dist[u] + c < dist[v]:
            dist[v] = dist[u] + c
            parent[v] = u
            y = v
    for _ in range(N):
        y = parent[y]
    cyc, cur = [], y
    while True:
        cyc.append(nodes[cur])
        cur = parent[cur]
        if cur == y or len(cyc) > N + 5:
            break
    wit, cur = {}, y
    while True:
        nxt = parent[cur]
        for (u, v), (c, w2) in best.items():
            if idx[u] == nxt and idx[v] == cur:
                wit[str((u, v))] = (c, w2)
                break
        cur = nxt
        if cur == y or len(wit) > N + 5:
            break
    return {"feasible": False, "cycle": cyc, "witnesses": wit}


def main():
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 7
    bits = _s.argv[2] if len(_s.argv) > 2 else "B"  # B,AB,ABF,POS
    tag = {"B": "l2", "AB": "l3", "ABF": "l4", "POS": "lpos",
           "POSA": "lposa"}[bits]
    # POS adds (depth_A(n), depth_B(n), LCA_A(2,n)): stitch-justified
    # positional triple (L4 S1/S3 separated on all three coords).
    Sh = O.build(n)["Sh"]
    nS = len(Sh)
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    Atrans, Btrans = D["Atrans"], D["Btrans"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd, vine, md, da8, lc8 = {}, {}, {}, {}, {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
        vine[ia] = is_vine(Sh[ia])
        md[ia] = maxdepth(Sh[ia])
        # positional triple for key n (n=1 base: single shape, vacuous)
        da8[ia] = dd[ia].get(n, 0)
        lc8[ia] = lca_of(Sh[ia], 2, n) if n >= 2 else 1
    # full a==ceil(dA/2) + q-table consistency (ALL shapes, not samples)
    A2t, At, B2t, Qt = {}, {}, {}, {}
    for ia in range(nS):
        for x in range(1, n + 1):
            ia2, a = Atrans[(ia, x)]
            assert a == (dd[ia].get(x, 0) + 1) // 2, (ia, x)
            A2t[(ia, x)] = ia2
            At[(ia, x)] = a
            ib2, _ = Btrans[(ia, x)]
            B2t[(ia, x)] = ib2
            Qt[(ia, x)] = dd[ia].get(x, 0) // 2
    step("T", "tables consistent: a==ceil(dA/2) all %d" % (nS * n))

    def cls(ra, rb, vb, va=0, fb=0, pa8=None, ma4=0):
        if bits == "POSA":
            da, db, lc = pa8
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0,
                    da, db, lc, 1 if ma4 else 0)
        if bits == "POS":
            da, db, lc = pa8
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0,
                    da, db, lc)
        if bits == "ABF":
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0)
        if bits == "AB":
            return (ra, rb, 1 if vb else 0, 1 if va else 0)
        return (ra, rb, 1 if vb else 0)

    best = {}
    concrete = 0
    for ia in range(nS):
        ra = rt[ia]
        va0 = vine[ia]
        for ib in range(nS):
            rb, vb = rt[ib], vine[ib]
            fb0 = md[ib] >= 6
            U = cls(ra, rb, vb, va0, fb0,
                    (da8[ia], dd[ib].get(n, 0), lc8[ia]), md[ia] >= 4)
            tw = 1 if ra == rb else 0
            for x in range(1, n + 1):
                ia2, a = A2t[(ia, x)], At[(ia, x)]
                # DELETE: B frozen
                Vd = cls(rt[ia2], rb, vb, vine[ia2], fb0,
                         (da8[ia2], dd[ib].get(n, 0), lc8[ia2]),
                         md[ia2] >= 4)
                twd = 1 if rt[ia2] == rb else 0
                c = -2 * a - 2 * (twd - tw)
                k = (U, Vd)
                if k not in best or c > best[k][0]:
                    best[k] = (c, (ia, ib, x, "D"))
                concrete += 1
                # KEEP
                ib2, q = B2t[(ib, x)], Qt[(ib, x)]
                Vk = cls(rt[ia2], rt[ib2], vine[ib2], vine[ia2],
                         md[ib2] >= 6,
                         (da8[ia2], dd[ib2].get(n, 0), lc8[ia2]),
                         md[ia2] >= 4)
                twk = 1 if rt[ia2] == rt[ib2] else 0
                c = q - 2 * a - 2 * (twk - tw)
                k = (U, Vk)
                if k not in best or c > best[k][0]:
                    best[k] = (c, (ia, ib, x, "K"))
                concrete += 1
        if (ia + 1) % 60 == 0:
            step("G", "%d/%d abstract_edges=%d" % (ia + 1, nS, len(best)))
    classes = sorted(set([u for u, _ in best] + [v for _, v in best]))
    step("G", "concrete=%d classes_present=%d/%d abstract_edges=%d" %
         (concrete, len(classes),
          {"B": 2, "AB": 4, "ABF": 8,
           "POS": 8 * n * n * n,
           "POSA": 16 * n * n * n}[bits] * n * n, len(best)))
    r = bf_feasible(best)
    step("BF", "feasible=%s %s" %
         (r["feasible"],
          ("passes=%d" % r["passes"]) if r["feasible"]
          else ("cycle=%s" % (r["cycle"],))))
    alpha_s = {"B": "(rootA,rootB,isVineB)",
                 "AB": "(rootA,rootB,isVineB,isVineA)",
                 "ABF": "(rootA,rootB,isVineB,isVineA,fuelB)",
                 "POS": "(rootA,rootB,isVineB,isVineA,fuelB,"
                        "dA(n),dB(n),LCA_A(2,n))",
                 "POSA": "(rootA,rootB,isVineB,isVineA,fuelB,"
                         "dA(n),dB(n),LCA_A(2,n),mdA4)"}[bits]
    out = {"n": n, "nS": nS, "alpha": alpha_s,
           "baseline": "Phi=-2*twin+P_alpha, P FREE",
           "concrete_edges": concrete,
           "classes_present": len(classes),
           "classes_max": {"B": 2, "AB": 4, "ABF": 8,
                           "POS": 8 * n * n * n,
                           "POSA": 16 * n * n * n}[bits] * n * n,
           "abstract_edges": len(best), "result": r}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("%s_refine%d.json" % (tag, n))).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    step("S", "wrote dual_mine/%s_refine%d.json" % (tag, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
