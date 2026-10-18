# G03R_CHAINED_WALKS.py — GATE D3-concrete: ssertify each leg of 2-KEEP chains
# separately on replayed intermediate states; detect exact 2-cycles / returns
# with signed totals. All edges full-state verified via repaired canon.
import sys, json, os, time, random
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
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER',
           'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE'):
    _ap = os.path.join(_ROOT, *_p.split('/'))
    if _ap not in sys.path:
        sys.path.insert(0, _ap)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

OUT = os.environ.get('RESCUE_OUT', 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/RESCUE_01_GRAPH_IDENTITY_AND_POTENTIAL/')
if OUT and not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03R_CANONICAL_STATE import canon_key, CanonError


def tl2list(t):
    if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
        return None
    k, l, r = t
    return [k, tl2list(l), tl2list(r)]


if __name__ == '__main__':
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 12
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 21
    rng = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    chains, two_cycles, neg_totals = [], [], []
    tried = 0
    while len(chains) < n and tried < n * 15 and time.process_time() - t0 < 1400:
        tried += 1
        keys = list(range(1, 10))
        ks = list(keys)
        rng.shuffle(ks)
        t = S.LEAF

        def ins(nn, k):
            if nn[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk, l, rr = nn
            return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

        for k in ks:
            t = ins(t, k)
        A, B = t, t
        # independent B shape
        ks2 = list(keys)
        rng.shuffle(ks2)
        B = S.LEAF
        for k in ks2:
            B = ins(B, k)
        M = set(rng.sample(keys, 5))
        Sset = set(keys)
        x1 = rng.choice(sorted(M))
        try:
            R1 = replay([('K', x1)], serial(A), serial(B))
        except Exception:
            continue
        if not R1['agree']:
            continue
        H1 = sum(l['a'] for l in R1['legs'])
        try:
            st1, info1 = ssertify(d, L, serial(A), serial(B), Sset, M, [('K', x1)], H1)
        except Exception:
            continue
        if st1 != 'ok':
            continue
        S1A, S1B = tl2list(R1['S1'][0]), tl2list(R1['S1'][1])
        x2 = rng.choice(sorted(M))
        try:
            R2 = replay([('K', x2)], S1A, S1B)
        except Exception:
            continue
        if not R2['agree']:
            continue
        H2 = sum(l['a'] for l in R2['legs'])
        try:
            st2, info2 = ssertify(d, L, S1A, S1B, Sset, M, [('K', x2)], H2)
        except Exception:
            continue
        if st2 != 'ok':
            continue
        e1 = dict(info1['env'])
        e2 = dict(info2['env'])
        try:
            s1 = canon_key({k: v for k, v in e1.items() if k.startswith('SLs_')}, 'SLs_')
            t1 = canon_key({k: v for k, v in e1.items() if k.startswith('SLt_')}, 'SLt_')
            s2 = canon_key({k: v for k, v in e2.items() if k.startswith('SLs_')}, 'SLs_')
            t2 = canon_key({k: v for k, v in e2.items() if k.startswith('SLt_')}, 'SLt_')
        except CanonError:
            continue
        w1, w2 = int(info1['w']), int(info2['w'])
        chained = (t1 == s2)
        closed = chained and (t2 == s1)
        chains.append({'chained': bool(chained), 'w1': w1, 'w2': w2,
                       'total': w1 + w2 if chained else None,
                       'closed_2cycle': bool(closed)})
        if closed:
            two_cycles.append({'w1': w1, 'w2': w2, 'total': w1 + w2})
            if w1 + w2 < 0:
                neg_totals.append(w1 + w2)
    json.dump({'n_chains': len(chains), 'chained_ok': sum(1 for c in chains if c['chained']),
               'two_cycles': two_cycles, 'negative_2cycle_totals': neg_totals,
               'chains': chains, 'cpu_s': time.process_time() - t0,
               'note': 't1==s2 join rate measures repaired-canon chaining on real continuations'},
              open(OUT + 'G03R_CHAINED_WALKS.json', 'w'), indent=1)
    print('chains=%d joined=%d 2cycles=%d neg2=%s cpu=%.1f' % (
        len(chains), sum(1 for c in chains if c['chained']), len(two_cycles),
        neg_totals, time.process_time() - t0), flush=True)
