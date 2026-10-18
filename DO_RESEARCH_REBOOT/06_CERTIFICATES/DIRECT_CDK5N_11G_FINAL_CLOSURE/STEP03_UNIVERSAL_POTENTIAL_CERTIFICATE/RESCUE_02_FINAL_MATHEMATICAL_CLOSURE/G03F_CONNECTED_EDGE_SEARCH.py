# G03F_CONNECTED_EDGE_SEARCH.py — PHASE B/C: source-pinned symbolic successor
# enumeration + BFS from negative-edge heads. Query: AND(low_root, source pins),
# weight free; block previous destinations for enumeration. Every found edge
# stores full dest state + witness model + weight. BFS to depth cap; any return
# to a negative tail with total<0 is a verified-cycle candidate.
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
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
R1 = PDIR + 'RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/'
OUT = os.environ.get('RESCUE_OUT2', PDIR + 'RESCUE_02_FINAL_MATHEMATICAL_CLOSURE/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

WIDTHS = {'mu': 9}
for i in range(19):
    WIDTHS['b_bkl%d' % i] = 2
    WIDTHS['b_brl%d' % i] = 5
    WIDTHS['b_bkr%d' % i] = 2
    WIDTHS['b_brr%d' % i] = 5
WIDTHS['b_broot'] = 5
for i in range(19):
    WIDTHS['b_blo%d' % i] = 5
    WIDTHS['b_bhi%d' % i] = 5
for p in range(7):
    WIDTHS['ak%d' % p] = 2
    WIDTHS['aI%d' % p] = 4
for i in range(10):
    WIDTHS['sg%d' % i] = 9
BOOLS = set('aS%d' % p for p in range(7))


def successors(d, ps, Lroot, src, wtag, nmax, timeout_ms, block_dests=()):
    """Enumerate up to nmax distinct (dest,w) from concrete src. Returns list."""
    from S01_SOLVER_INTERFACE import SAT
    found = []
    blocks = []
    for b in block_dests:
        legs = []
        for f, v in b.items():
            if f in BOOLS:
                legs.append(d.vars['SLt_' + f] if v else d.NOT(d.vars['SLt_' + f]))
            else:
                legs.append(d.NOT(d.EQ(d.vars['SLt_' + f], d.const_int(v, WIDTHS[f]))))
        blocks.append(d.OR(*legs))
    for _ in range(nmax):
        C = [Lroot]
        for f, v in src.items():
            if f in BOOLS:
                C.append(d.vars['SLs_' + f] if v else d.NOT(d.vars['SLs_' + f]))
            else:
                C.append(d.EQ(d.vars['SLs_' + f], d.const_int(v, WIDTHS[f])))
        C.extend(blocks)
        q = d.AND(*C)
        h = ps.compile(q, wtag)
        r = ps.solve(h, {})
        if r.get('status') != SAT:
            return found, r.get('status')
        m = ps.extract_model(h, r)
        dst = {}
        for f in WIDTHS:
            k = 'SLt_' + f
            if k in m:
                dst[f] = int(m[k])
        for f in BOOLS:
            k = 'SLt_' + f
            if k in m:
                dst[f] = int(m[k])
        w = int(m.get('SL_w', 0))
        if w >= 16:
            w -= 32
        wit = {k: (int(v) if isinstance(v, int) else v) for k, v in m.items() if k.startswith('SLw_')}
        found.append({'dest': dst, 'w': w, 'witness': wit})
        legs = []
        for f, v in dst.items():
            if f in BOOLS:
                legs.append(d.vars['SLt_' + f] if not v else d.NOT(d.vars['SLt_' + f]))
            else:
                legs.append(d.NOT(d.EQ(d.vars['SLt_' + f], d.const_int(v, WIDTHS[f]))))
        blocks.append(d.OR(*legs))
    return found, 'CAP'


if __name__ == '__main__':
    import sys as _s
    maxq = int(_s.argv[1]) if len(_s.argv) > 1 else 25
    per = int(_s.argv[2]) if len(_s.argv) > 2 else 6
    depthmax = int(_s.argv[3]) if len(_s.argv) > 3 else 4
    os.makedirs(OUT, exist_ok=True)
    from PC_TYPED_DAG import DAG
    from STRICT_LOW_COMPILER import build_slow
    from S01_SOLVER_INTERFACE import ProductionSolver
    from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
    t0 = time.process_time()
    d = DAG()
    L = build_slow(d, 'SL')
    ps = ProductionSolver(d, timeout_ms=60000)
    install_scoped_compile(ps)
    led = json.load(open(os.path.join(os.environ.get('RESCUE_R1', _ROOT + '/' + R1), 'G03R_VERIFIED_EDGE_LEDGER.json')))
    E = led['edges']
    negs = [(i, e) for i, e in enumerate(E) if e['weight'] < 0]
    print('negative starts:', [(i, e['weight']) for i, e in negs], flush=True)
    # self-test: pin source of edge 0, expect its (t,w) among successors
    e0 = E[0]
    f0, st0 = successors(d, ps, L['root'], e0['source_state'], 'selftest', 8, 60000)
    hit = any(f['dest'] == e0['destination_state'] and f['w'] == e0['weight'] for f in f0)
    print('selftest: %d succ, known-edge recovered=%s' % (len(f0), hit), flush=True)
    # BFS
    nodes = {}   # key(tuple) -> state
    edges = []   # (skey,tkey,w,depth,from_neg)
    q = []
    for i, e in negs:
        for tag, st in (('s', e['source_state']), ('t', e['destination_state'])):
            kk = tuple(st[f] for f in sorted(st.keys()))
            nodes.setdefault(kk, st)
        q.append((tuple(e['destination_state'][f] for f in sorted(e['destination_state'].keys())), e['destination_state'], 1, i, e['weight']))
        edges.append({'s': e['source_state'], 't': e['destination_state'], 'w': e['weight'],
                      'depth': 0, 'neg_idx': i, 'verified': 'ledger'})
    nq = 0
    stat = {}
    import collections
    while q and nq < maxq and time.process_time() - t0 < 1500:
        skey, sstate, dep, negi, cost = q.pop(0)
        if dep > depthmax:
            continue
        fnd, st = successors(d, ps, L['root'], sstate, 'q%d' % nq, per, 60000)
        nq += 1
        stat[nq] = st
        for f in fnd:
            dst = f['dest']
            if len(dst) < 100:
                continue
            dkey = tuple(dst[ff] for ff in sorted(dst.keys()))
            nodes.setdefault(dkey, dst)
            edges.append({'s': sstate, 't': dst, 'w': f['w'], 'depth': dep,
                          'neg_idx': negi, 'cost_from_head': cost, 'verified': 'symbolic'})
            if dep < depthmax and dkey not in [qq[0] for qq in q]:
                q.append((dkey, dst, dep + 1, negi, cost + f['w']))
    # check returns: any edge landing on a negative tail?
    tails = {}
    for i, e in negs:
        tails[tuple(e['source_state'][f] for f in sorted(e['source_state'].keys()))] = (i, e['weight'])
    cands = []
    for e in edges:
        if e.get('verified') != 'symbolic':
            continue
        dk = tuple(e['t'][f] for f in sorted(e['t'].keys()))
        if dk in tails:
            i, r = tails[dk]
            tot = -r + e['cost_from_head']
            cands.append({'neg_idx': i, 'r': r, 'return_cost': e['cost_from_head'],
                          'depth': e['depth'], 'total': tot, 'is_negative_cycle': tot < 0})
    json.dump({'n_queries': nq, 'query_status': stat, 'n_nodes': len(nodes),
               'n_edges': len(edges), 'selftest_hit': hit,
               'return_candidates': cands, 'cpu_s': time.process_time() - t0,
               'edges': [{'s': e['s'], 't': e['t'], 'w': e['w'], 'depth': e['depth'],
                           'neg_idx': e['neg_idx'], 'verified': e['verified']} for e in edges]},
              open(OUT + 'G03F_CONNECTED_GRAPH_RESULTS.json', 'w'), indent=1)
    print('queries=%d nodes=%d edges=%d returns=%s cpu=%.1f' % (
        nq, len(nodes), len(edges), cands, time.process_time() - t0), flush=True)
