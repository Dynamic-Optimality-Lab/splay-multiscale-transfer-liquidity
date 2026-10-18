# G03_GROUNDED_GRAPH_CHECK.py — exact Bellman-Ford over grounded edges (Gate G).
# Collects every verified grounded (s,t,w) edge (S02 certs + replays here),
# canonicalizes abstract states to hashable keys, detects negative cycles.
# A found cycle with all-verified edges = OUTCOME C candidate (then verify).
import sys, json
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from S03_EDGE_PROJECTIONS import build_projections


def canon_key(env, prefix):
    items = sorted((k, (int(v) if not isinstance(v, bool) else int(v))) for k, v in env.items() if k.startswith(prefix))
    return tuple(items)


if __name__ == '__main__':
    d = DAG()
    from CW_PRODUCT_COMPILER import Product
    P = Product(d)
    edges, audits = build_projections(P)
    # gather grounded edges: (s_key, t_key, w, label)
    import json as _j
    E = []
    seen = set()
    corp = _j.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_GENERALIZATION_CORPUS.json'))
    dL = DAG()
    L = build_slow(dL, 'SL')
    for c in corp:
        if c.get('grounded') != 'ok':
            continue

        def totup(x):
            if x is None or x == '.':
                return S.LEAF
            k, l, r = x
            return S.node(k, totup(l), totup(r))
        try:
            A0 = totup(c['A'])
            B0 = totup(c['B'])
            word = [tuple(w) for w in c['word']]
            st, info = ssertify(dL, L, serial(A0), serial(B0), set(c['Sset']), set(c['M']), word, int(c['H']))
        except Exception as e:
            continue
        if st != 'ok':
            continue
        env = dict(info['env'])
        sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
        ks, kt = canon_key(sp, 'SLs_'), canon_key(tp, 'SLt_')
        if (ks, kt, info['w']) not in seen:
            seen.add((ks, kt, info['w']))
            E.append({'s': ks, 't': kt, 'w': int(info['w']), 'case': c['category']})
    print('grounded edges:', len(E), flush=True)
    # Bellman-Ford over the sampled graph
    verts = sorted(set([e['s'] for e in E] + [e['t'] for e in E]), key=repr)
    idx = {v: i for i, v in enumerate(verts)}
    n = len(verts)
    el = [((idx[e['s']], idx[e['t']], e['w'])) for e in E]
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
    out = {'n_vertices': n, 'n_edges': len(el), 'negative_cycle': bool(x)}
    if x is not None:
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
        out['cycle'] = [[str(a)[:40], str(b)[:40], w] for (a, b, w) in cyc]
        out['total'] = tot
    print('NEGATIVE CYCLE:', out['negative_cycle'], out.get('total'), flush=True)
    J('G03_GROUNDED_GRAPH_CHECK.json', out)
