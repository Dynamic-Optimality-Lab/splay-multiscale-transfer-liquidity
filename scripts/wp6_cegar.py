"""PIVOT-25 CEGAR: abstract-dual feasibility on structural summaries.

Level 0: twin-bit (2 nodes). Level 1: root-pair (n^2 nodes).
For each: max-w per abstract edge, BF feasibility, positive-cycle extraction.
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
    print("[CEGAR %s] %s" % (sid, msg), flush=True)


def load_all(n):
    G = O.build(n)
    nS, Sh = G["nS"], G["Sh"]
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    Atrans, Btrans = D["Atrans"], D["Btrans"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt, dd = {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
    return n, nS, Sh, Atrans, Btrans, rt, dd


def abstract_graph(n, nS, Atrans, Btrans, rt, dd, alpha):
    """alpha(ia,ib) -> hashable. Returns edges dict (U,V)->(maxw, witness).

    maxw = max concrete reward w=q-2a over edges mapping to (U,V).
    Dual feasibility (potentials P with P(U)-P(V)>=w) is tested by
    Bellman-Ford on costs c=-w (negative-c cycle <=> positive-w cycle).
    """
    best = {}
    for ia in range(nS):
        for ib in range(nS):
            U = alpha(ia, ib)
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                k = (U, alpha(ia2, ib))
                w = -2 * a
                if k not in best or w > best[k][0]:
                    best[k] = (w, (ia, ib, x, "D"))
                ib2, _ = Btrans[(ib, x)]
                k = (U, alpha(ia2, ib2))
                w = dd[ib].get(x, 0) // 2 - 2 * a
                if k not in best or w > best[k][0]:
                    best[k] = (w, (ia, ib, x, "K"))
    return best


def bf_feasible(best):
    """Feasibility of P(U)-P(V)>=w, i.e. no positive-w abstract cycle.

    Bellman-Ford on costs c=-w from super-source (dist 0): negative-c
    cycle <=> positive-w cycle (the obstruction). Returns potentials or
    the positive abstract cycle + per-edge witnesses.
    """
    nodes = sorted(set([u for u, _ in best] + [v for _, v in best]))
    idx = {v: i for i, v in enumerate(nodes)}
    N = len(nodes)
    # E as (u, v, c=-w)
    E = [(idx[u], idx[v], -w) for (u, v), (w, _) in best.items()]
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
            pot = {nodes[i]: -dist[i] for i in range(N)}
            return {"feasible": True, "passes": i + 1, "nodes": nodes,
                    "pot": pot}
    # negative-c cycle => positive-w abstract cycle. Extract + witnesses.
    y = -1
    for (u, v, c) in E:
        if dist[u] + c < dist[v]:
            dist[v] = dist[u] + c
            parent[v] = u
            y = v
    for _ in range(N):
        y = parent[y]
    cyc = []
    cur = y
    while True:
        cyc.append(nodes[cur])
        cur = parent[cur]
        if cur == y or len(cyc) > N + 5:
            break
    # witnesses per abstract edge in cycle
    wit = {}
    cur = y
    while True:
        nxt = parent[cur]
        # edge nxt->cur in abstract graph; find its key + witness
        for (u, v), (w, w2) in best.items():
            if idx[u] == nxt and idx[v] == cur:
                wit[(u, v)] = (w, w2)
                break
        cur = nxt
        if cur == y or len(wit) > N + 5:
            break
    return {"feasible": False, "cycle": cyc, "witnesses": wit}


def main():
    n = 7
    n, nS, Sh, Atrans, Btrans, rt, dd = load_all(n)
    # Level 0: twin-bit
    best = abstract_graph(n, nS, Atrans, Btrans, rt, dd,
                          lambda ia, ib: rt[ia] == rt[ib])
    r = bf_feasible(best)
    step("L0", "twin-bit: edges=%d feasible=%s %s" %
         (len(best), r["feasible"],
          ("cycle=" + str(r.get("cycle"))) if not r["feasible"] else ""))
    # Level 1: root-pair
    best = abstract_graph(n, nS, Atrans, Btrans, rt, dd,
                          lambda ia, ib: (rt[ia], rt[ib]))
    r = bf_feasible(best)
    step("L1", "root-pair: edges=%d feasible=%s %s" %
         (len(best), r["feasible"],
          ("cycle=" + str(r.get("cycle"))) if not r["feasible"] else ""))
    import json as J
    out = {"twin": None, "rootpair_feasible": r["feasible"],
           "rootpair_cycle": r.get("cycle"),
           "rootpair_witnesses": {str(k): v for k, v in
                                  r.get("witnesses", {}).items()}}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "cegar.json").write_text(
         J.dumps(out, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
