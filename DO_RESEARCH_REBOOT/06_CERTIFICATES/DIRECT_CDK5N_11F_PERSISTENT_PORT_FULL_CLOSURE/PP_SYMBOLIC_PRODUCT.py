# PP_SYMBOLIC_PRODUCT.py — explicit diagnostic product at small scope + full-scope representation.
# Full (mu,b,alpha,sigma) scope: representation fixed; materialization blocked (measured guard
# growth ~1/macro in fringe scope, PP_GUARD_CENSUS.json). 9-key counts by reference (WQ 4.29M).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE')
import splay as S
from CRA_pointer_tuple_replay import replay
from PP_LOW_RELATION import S_to_list, all_bsts, decide
from PP_HIGH_MIDPOINT import fibers_for

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PERSISTENT_PORT_FULL_CLOSURE/'


def build_product(keys, Sset, M, seeds, q_terms):
    """Explicit diagnostic product: nodes=(A,B) serial pairs reachable via 1-access macros;
    edges=low (decide) + high (fiber, expanded per covered transition for diagnosis only)."""
    from CRA_pointer_tuple_replay import from_serial
    nodes = set()
    edges = {}  # (s,w,t)
    prov = {}  # (s,w,t) -> 'low' | 'high'
    for (A0, B0) in seeds:
        nodes.add((str(S_to_list(A0)), str(S_to_list(B0))))
    highs = []
    for (A0, B0) in seeds:
        for x in keys:
            for md in ('K', 'D'):
                if md == 'K' and S.lookup(B0, x)[1] < 0:
                    continue
                d = S.lookup(A0, x)[1]
                a = (d + 1) // 2
                for q in q_terms:
                    if a <= 2:
                        e, why = decide(A0, B0, Sset, M, [(md, x)], q)
                        if e is None:
                            continue
                        s = (str(S_to_list(A0)), str(S_to_list(B0)))
                        t = (str(e['Ad']), str(e['Bd']))
                        nodes.add(t)
                        edges.setdefault((s, e['w'], t), 0)
                        edges[(s, e['w'], t)] += 1
                        prov.setdefault((s, e['w'], t), 'low')
                    else:
                        if q == q_terms[0]:
                            highs.append((A0, B0, Sset, M, [(md, x)]))
    if highs:
        mids, cover, _ = fibers_for(highs)
        for idx, (g, qd, t_id) in cover.items():
            A0, B0, _, _, _ = highs[idx]
            s = (str(S_to_list(A0)), str(S_to_list(B0)))
            t = (str(S_to_list(t_id[0])), str(t_id[1]))
            nodes.add(t)
            w = 6 - qd
            edges.setdefault((s, w, t), 0)
            edges[(s, w, t)] += 1
            prov.setdefault((s, w, t), 'high')
    return nodes, edges, prov


def bellman_ford(nodes, edges):
    dist = {v: 0 for v in nodes}
    E = [(s, w, t) for (s, w, t) in edges]
    V = list(nodes)
    for _ in range(len(V)):
        upd = False
        for (s, w, t) in E:
            if dist[s] + w < dist[t]:
                dist[t] = dist[s] + w
                upd = True
        if not upd:
            return False, dist
    return True, dist  # True = negative cycle reachable


if __name__ == '__main__':
    t0 = time.time()
    keys = [1, 2, 3, 4, 5, 6, 7]
    Sset = set(keys)
    M = {1, 2}
    trees = list(all_bsts(keys))
    seeds = [(A, A) for A in trees]  # closed-walk starts: A0=B0
    nodes, edges, prov = build_product(keys, Sset, M, seeds, [0, 1, 2, 3])
    nlow = sum(1 for k, v in prov.items() if v == 'low')
    nhigh = sum(1 for k, v in prov.items() if v == 'high')
    neg, dist = bellman_ford(nodes, edges)
    print('product: nodes=%d edges=%d (low=%d high=%d) negcycle=%s time=%.1fs' % (len(nodes), len(edges), nlow, nhigh, neg, time.time() - t0), flush=True)
    json.dump({'nodes': len(nodes), 'edges': len(edges), 'low': nlow, 'high': nhigh, 'negcycle': neg,
               'scope': '7-key diagnostic (A0=B0 seeds, 1-access macros, q in 0..3)'},
              open(PDIR + 'PP_PRODUCT_TEST.json', 'w'), indent=1)
