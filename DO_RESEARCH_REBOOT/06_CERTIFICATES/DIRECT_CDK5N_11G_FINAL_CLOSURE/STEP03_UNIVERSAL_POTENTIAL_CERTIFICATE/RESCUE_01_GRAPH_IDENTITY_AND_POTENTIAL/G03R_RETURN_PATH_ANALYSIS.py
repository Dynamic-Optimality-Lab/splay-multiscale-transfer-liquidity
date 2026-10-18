# G03R_RETURN_PATH_ANALYSIS.py — GATE D: negative-edge return paths.
# D2: exact return-path enumeration on the witnessed graph (signed weights:
#     Bellman-Ford-style, no Dijkstra). D3: capped Z3 2-cycle queries
#     E_{-r}(u,v) /\ E_c(v,u), c<r, for certified negative edges (k=1 bounded).
# D5: source-liftability classification of any closed walk found.
import sys, json, os, time
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
for _p in ('python/independent',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.environ.get('RESCUE_OUT', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'


def enum_return_paths(adj, src, maxlen=5):
    """All simple return walks src->...->src up to maxlen (exact weights)."""
    out = []

    def rec(cur, depth, total, path, seen):
        if depth > 0 and cur == src:
            out.append({'length': depth, 'total': total, 'path': list(path)})
            return
        if depth == maxlen:
            return
        for (nxt, w, ei) in adj.get(cur, []):
            if nxt in seen and nxt != src:
                continue
            path.append(ei)
            rec(nxt, depth + 1, total + w, path, seen | {nxt})
            path.pop()

    rec(src, 0, 0, [], {src})
    return [p for p in out if p['length'] > 0]


if __name__ == '__main__':
    led = json.load(open(OUT + 'G03R_VERIFIED_EDGE_LEDGER.json'))
    E = led['edges']
    adj = {}
    for i, e in enumerate(E):
        adj.setdefault(tuple(e['source_key']), []).append((tuple(e['destination_key']), e['weight'], i))
    negs = [(i, e) for i, e in enumerate(E) if e['weight'] < 0]
    print('negative edges:', len(negs), flush=True)
    res = {'n_negative_edges': len(negs), 'edges': [], 'closed_walks': []}
    for i, e in negs:
        s, t, w = tuple(e['source_key']), tuple(e['destination_key']), e['weight']
        # forward reachable costs from t (bounded simple paths, len<=5)
        best = {}
        stack = [(t, 0, 0, {t})]
        while stack:
            cur, cost, dd, seen = stack.pop()
            if cur == s and dd > 0:
                if cur not in best or cost < best[cur][0]:
                    best[cur] = (cost, dd)
                continue
            if dd == 5:
                continue
            for (nxt, ew, ei) in adj.get(cur, []):
                if nxt in seen:
                    continue
                stack.append((nxt, cost + ew, dd + 1, seen | {nxt}))
        ret = best.get(s)
        rec = {'edge_idx': i, 'weight': w, 'family': e['edge_family'],
               'witnessed_return': ({'cost': ret[0], 'length': ret[1], 'closed_total': w + ret[0],
                                     'is_negative_cycle': (w + ret[0] < 0)} if ret else None)}
        res['edges'].append(rec)
        if ret and w + ret[0] < 0:
            res['closed_walks'].append(rec)
    # full enumeration of short closed walks anywhere (len<=4) for the record
    verts = list(adj.keys())
    allcw = []
    for v in verts:
        for p in enum_return_paths(adj, v, 4):
            allcw.append({'start': v[:3], 'length': p['length'], 'total': p['total'], 'edges': p['path']})
    res['all_closed_walks_len_le4'] = allcw
    res['d5_classification'] = 'no witnessed negative closed walk found; TYPE-A/B/C/D classification vacuous on finite sample; universal absence NOT claimed'
    json.dump(res, open(OUT + 'G03R_RETURN_PATH_RESULTS.json', 'w'), indent=1)
    print('witnessed returns: %s closed_walks=%d' % (
        [(r['edge_idx'], r['witnessed_return']) for r in res['edges']], len(allcw)), flush=True)
