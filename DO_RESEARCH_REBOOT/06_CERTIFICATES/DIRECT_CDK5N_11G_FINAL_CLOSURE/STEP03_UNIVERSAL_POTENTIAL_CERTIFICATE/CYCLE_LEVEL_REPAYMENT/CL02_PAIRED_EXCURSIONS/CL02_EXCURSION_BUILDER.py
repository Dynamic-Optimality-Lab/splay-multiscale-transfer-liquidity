# CL02_EXCURSION_BUILDER.py — concrete paired-excursion construction.
# Random starts, replay KEEP words (len 3-6, MSET keys), ssertify EACH leg on
# intermediate serial states, canon-verify chaining, compute guards, extract
# maximal 01...10 excursions with full states. Tests R(P)>=0 per excursion.
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
sys.path.insert(0, os.path.join(_ROOT, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE'))
sys.path.insert(0, os.environ.get('RESCUE_R1', 'R:/'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get('RESCUE_OUT7', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03R_CANONICAL_STATE import canon_key, CanonError
from G03_POTENTIAL_FEATURES import eval_all


def tl2list(t):
    if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
        return None
    k, l, r = t
    return [k, tl2list(l), tl2list(r)]


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def Phi(f):
    C2 = f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']
    return C2 if f['b_depth_max'] >= 7 else C5(f)


if __name__ == '__main__':
    import sys as _s
    budget = float(_s.argv[1]) if len(_s.argv) > 1 else 700
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 701
    maxlegs = int(_s.argv[3]) if len(_s.argv) > 3 else 6
    rng = random.Random(seed)
    MSET = {1, 3, 5, 7, 9}
    SSET = set(range(1, 10))
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    excursions = []
    nchains = nlegs = 0
    while time.process_time() - t0 < budget and len(excursions) < 15:
        ks = list(range(1, 10))
        rng.shuffle(ks)
        t = S.LEAF

        def ins(n, k):
            if n[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk, l, rr = n
            return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

        for k in ks:
            t = ins(t, k)
        A, B = t, t
        ks2 = list(range(1, 10))
        rng.shuffle(ks2)
        B = S.LEAF
        for k in ks2:
            B = ins(B, k)
        word = [rng.choice(sorted(MSET)) for _ in range(rng.randint(3, maxlegs))]
        # replay whole word first (agreement), then per-leg ssertify
        try:
            R = replay([('K', x) for x in word], serial(A), serial(B))
        except Exception:
            continue
        if not R['agree']:
            continue
        # walk legs with serial states
        cA, cB = serial(A), serial(B)
        legs = []
        okchain = True
        for x in word:
            try:
                R1 = replay([('K', x)], cA, cB)
            except Exception:
                okchain = False
                break
            if not R1['agree']:
                okchain = False
                break
            H = sum(l['a'] for l in R1['legs'])
            try:
                st, info = ssertify(d, L, cA, cB, SSET, MSET, [('K', x)], H)
            except Exception:
                okchain = False
                break
            if st != 'ok':
                okchain = False
                break
            env = dict(info['env'])
            sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
            tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
            try:
                sk = canon_key(sp, 'SLs_')
                tk = canon_key(tp, 'SLt_')
            except CanonError:
                okchain = False
                break
            fs = eval_all(sp, 'SLs')
            ft = eval_all(tp, 'SLt')
            if any(v is None for v in list(fs.values()) + list(ft.values())):
                okchain = False
                break
            legs.append({'s': {k[4:]: int(v) for k, v in sp.items()},
                         't': {k[4:]: int(v) for k, v in tp.items()},
                         'w': int(info['w']), 'x': x})
            nlegs += 1
            cA, cB = tl2list(R1['S1'][0]), tl2list(R1['S1'][1])
        if not okchain or not legs:
            continue
        nchains += 1
        # verify chaining + guards
        gs = []
        chained = True
        for i, lg in enumerate(legs):
            se = {'SLs_' + k: v for k, v in lg['s'].items()}
            te = {'SLt_' + k: v for k, v in lg['t'].items()}
            try:
                sk = canon_key(se, 'SLs_')
                tk = canon_key(te, 'SLt_')
            except CanonError:
                chained = False
                break
            if i > 0:
                pse = {'SLs_' + k: v for k, v in legs[i - 1]['t'].items()}
                try:
                    pk = canon_key(pse, 'SLs_')
                except CanonError:
                    chained = False
                    break
                if pk != sk:
                    chained = False
                    break
            fs = eval_all(se, 'SLs')
            ft = eval_all(te, 'SLt')
            gs.append((1 if fs['b_depth_max'] >= 7 else 0, 1 if ft['b_depth_max'] >= 7 else 0,
                       fs, ft, lg['w']))
        if not chained:
            continue
        # extract maximal 01...10 excursions
        i = 0
        while i < len(gs):
            if gs[i][0] == 0 and gs[i][1] == 1:
                j = i
                while j + 1 < len(gs) and gs[j + 1][0] == 1 and gs[j + 1][1] == 1:
                    j += 1
                # excursion = legs[i..k]: legs[i] is 01, middle are 11, legs[k] is 10
                k = j + 1
                if k < len(gs) and gs[k][0] == 1 and gs[k][1] == 0:
                    segs = gs[i:k + 1]
                    u0, u1 = segs[0][2], segs[-1][3]
                    wP = sum(s[4] for s in segs)
                    RP = wP - (C5(u1) - C5(u0))
                    excursions.append({'legs': [{'w': s[4], 'pair': '%d%d' % (s[0], s[1]),
                                                 's': s[2], 't': s[3]} for s in segs],
                                       'wP': wP, 'RP': RP, 'holds': bool(RP >= 0),
                                       'entry_viol': (C2t := (segs[0][3]['b_rank_sum'] - segs[0][3]['b_depth_max'] + segs[0][3]['a_marked_count'])) - (C5(segs[0][2])) > segs[0][4]})
                    i = k + 1
                    continue
            i += 1
    json.dump({'nchains': nchains, 'nlegs': nlegs, 'nexcursions': len(excursions),
               'excursions': excursions, 'cpu_s': time.process_time() - t0},
              open(OUT + 'CL02_EXCURSIONS.json', 'w'), indent=1)
    print('chains=%d legs=%d excursions=%d holds=%s cpu=%.1f' % (
        nchains, nlegs, len(excursions),
        [e['holds'] for e in excursions], time.process_time() - t0), flush=True)
