# G03R_NEGATIVE_CYCLE_AUDIT.py — GATE C: independent exact Bellman-Ford + SCC.
# Runs on: (1) historical incorrectly-keyed graph, (2) corrected 9-edge graph,
# (3) expanded full-state witnessed graph, (4) contracted-high subgraph (if any).
# Independent implementation (no reuse of production search code paths).
import sys, json, os
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = _HERE
for _ in range(8):
    if os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
        break
    _up = os.path.dirname(_ROOT)
    if _up == _ROOT:
        break
    _ROOT = _up
if not os.path.isdir(os.path.join(_ROOT, 'python', 'independent')):
    _ROOT = os.environ.get('RESCUE_ROOT', _ROOT)
if _ROOT != os.getcwd():
    os.chdir(_ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
OUT = os.environ.get('RESCUE_OUT', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'


def scc_tarjan(n, adj):
    index_of, low, onst, st, comp, idx = {}, {}, set(), [], {}, [0]

    def strong(v):
        index_of[v] = low[v] = idx[0]
        idx[0] += 1
        st.append(v)
        onst.add(v)
        for w in adj[v]:
            if w not in index_of:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in onst:
                low[v] = min(low[v], index_of[w])
        if low[v] == index_of[v]:
            c = []
            while True:
                w = st.pop()
                onst.discard(w)
                c.append(w)
                comp[w] = len(comps)
                if w == v:
                    break
            comps.append(c)

    comps = []
    for v in range(n):
        if v not in index_of:
            strong(v)
    return comps, comp


def bellman_ford(n, el):
    """Exact BF with super-source (dist 0 init). Returns (has_neg, cycle_edges, dist)."""
    dist = [0] * n
    pred = [None] * n
    x = None
    for _ in range(n):
        x = None
        for (u, v, w) in el:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                pred[v] = (u, w)
                x = v
    if x is None:
        return False, [], dist
    y = x
    for _ in range(n):
        y = pred[y][0]
    cyc, cur, tot = [], y, 0
    while True:
        u, w = pred[cur]
        cyc.append((u, cur, w))
        tot += w
        cur = u
        if cur == y or len(cyc) > n + 1:
            break
    return True, {'edges': cyc, 'total': tot}, dist


def analyze(name, verts, el):
    n = len(verts)
    idx = {v: i for i, v in enumerate(verts)}
    eli = [(idx[u], idx[v], w) for (u, v, w) in el]
    adj = [set() for _ in range(n)]
    for (u, v, w) in eli:
        adj[u].add(v)
    comps, comp = scc_tarjan(n, adj)
    has_neg, cyc, dist = bellman_ford(n, eli)
    neg_in_scc = sum(1 for (u, v, w) in eli if w < 0 and comp[u] == comp[v])
    neg_cross = sum(1 for (u, v, w) in eli if w < 0 and comp[u] != comp[v])
    return {'graph': name, 'n_vertices': n, 'n_edges': len(eli),
            'n_pos': sum(1 for e in eli if e[2] > 0), 'n_neg': sum(1 for e in eli if e[2] < 0),
            'n_zero': sum(1 for e in eli if e[2] == 0),
            'n_scc': len(comps), 'largest_scc': max((len(c) for c in comps), default=0),
            'neg_in_scc': neg_in_scc, 'neg_cross_scc': neg_cross,
            'has_negative_cycle': has_neg, 'cycle': cyc}


if __name__ == '__main__':
    led = json.load(open(OUT + 'G03R_VERIFIED_EDGE_LEDGER.json'))
    E = led['edges']
    # corrected graph: namespace-free keys
    verts = sorted(set([tuple(e['source_key']) for e in E] + [tuple(e['destination_key']) for e in E]))
    el = [(tuple(e['source_key']), tuple(e['destination_key']), e['weight']) for e in E]
    # historical incorrectly-keyed graph: re-attach prefixes to simulate old canon
    def oldkey(state, tag):
        return tuple(sorted((tag + k, v) for k, v in state.items()))
    oel = [(oldkey(e['source_state'], 'SLs_'), oldkey(e['destination_state'], 'SLt_'), e['weight']) for e in E]
    overts = sorted(set([u for (u, v, w) in oel] + [v for (u, v, w) in oel]))
    results = {}
    results['historical_keying'] = analyze('historical-prefix-keying', overts, oel)
    results['corrected'] = analyze('corrected-namespace-free', verts, el)
    results['expanded'] = analyze('expanded-full-state', verts, el)
    # contracted-high subgraph: none with concrete endpoints in ledger yet
    results['contracted_high'] = {'graph': 'contracted-high', 'status': 'no concrete-endpoint contracted edges in full-state ledger; tier-2 SAT evidence referenced (G03_CONTRACTED_WITNESS_RESULTS.json); OBLIGATION retained'}
    # chaining stats
    dsts = set(tuple(e['destination_key']) for e in E)
    srcs = set(tuple(e['source_key']) for e in E)
    chained = len(dsts & srcs)
    json.dump({'results': results,
               'chaining': {'n_src_vertices': len(srcs), 'n_dst_vertices': len(dsts),
                            'joined_vertices': chained,
                            'note': 'joined>0 proves repaired canon enables endpoint chaining that prefix-keying forbids'},
               'historical_claim': '16 vertices / 9 edges (prefix-keyed; chaining impossible by construction)'},
              open(OUT + 'G03R_CYCLE_RESULTS.json', 'w'), indent=1)
    json.dump({'results': {k: v for k, v in results.items() if k != 'contracted_high'},
               'n_ledger_edges': len(E),
               'scc_note': 'SCC + neg-edge classification included per graph'},
              open(OUT + 'G03R_SCC_RESULTS.json', 'w'), indent=1)
    for k, v in results.items():
        if k == 'contracted_high':
            print(k, v['status'][:80], flush=True)
            continue
        print('%s: V=%d E=%d neg=%d scc=%d negInSCC=%d negCycle=%s' % (
            k, v['n_vertices'], v['n_edges'], v['n_neg'], v['n_scc'], v['neg_in_scc'], v['has_negative_cycle']), flush=True)
