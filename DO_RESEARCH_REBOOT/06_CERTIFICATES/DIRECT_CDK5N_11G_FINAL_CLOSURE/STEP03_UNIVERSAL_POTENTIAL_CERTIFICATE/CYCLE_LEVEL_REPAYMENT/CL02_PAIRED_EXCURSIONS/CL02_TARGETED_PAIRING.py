# CL02_TARGETED_PAIRING.py — efficient paired-excursion hunt.
# Phase 1: replay-only screen for upward proxy jumps; ssertify candidates
# until K certified 0->1 found (save CONCRETE post-states).
# Phase 2: extend each forward leg-by-leg (ssertify) until shallow (1->0).
# Result: paired 01...10 excursions with full states, or quantified miss.
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
from CRA_pointer_tuple_replay import replay, from_serial
from G03_POTENTIAL_FEATURES import eval_all


def depths_of(t):
    out = {}

    def rec(n, d):
        if n[0] == 'leaf':
            return
        _, k, l, r = n
        out[k] = d
        rec(l, d + 1)
        rec(r, d + 1)

    rec(t, 0)
    return out


def tl2list(t):
    if t == '.' or (isinstance(t, tuple) and t and t[0] == 'leaf'):
        return None
    k, l, r = t
    return [k, tl2list(l), tl2list(r)]


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def rand_tree(rng):
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
    return t


if __name__ == '__main__':
    import sys as _s
    budget = float(_s.argv[1]) if len(_s.argv) > 1 else 300
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 801
    K = int(_s.argv[3]) if len(_s.argv) > 3 else 2
    suf = _s.argv[4] if len(_s.argv) > 4 else ''
    rng = random.Random(seed)
    MSET = {1, 3, 5, 7, 9}
    SSET = set(range(1, 10))
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    entries = []  # certified 0->1 with concrete post-state
    nscr = ncert = 0
    while len(entries) < K and time.process_time() - t0 < budget * 0.6:
        A, B = rand_tree(rng), rand_tree(rng)
        x = rng.choice(sorted(MSET))
        try:
            R = replay([('K', x)], serial(A), serial(B))
        except Exception:
            continue
        if not R['agree']:
            continue
        nscr += 1
        d0 = depths_of(from_serial(R['S0'][1]))
        d1 = depths_of(from_serial(R['S1'][1]))
        if not d0 or not d1:
            continue
        if not (max(d0.values()) <= 6 and max(d1.values()) >= 7):
            continue
        H = sum(l['a'] for l in R['legs'])
        try:
            st, info = ssertify(d, L, serial(A), serial(B), SSET, MSET, [('K', x)], H)
        except Exception:
            continue
        if st != 'ok':
            continue
        ncert += 1
        env = dict(info['env'])
        fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
        ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
        if fs['b_depth_max'] > 6 or ft['b_depth_max'] < 7:
            continue
        entries.append({'sA': serial(A), 'sB': serial(B), 'x': x, 'w': int(info['w']),
                        'postA': tl2list(R['S1'][0]), 'postB': tl2list(R['S1'][1]),
                        's_full': {k[4:]: int(v) for k, v in env.items() if k.startswith('SLs_')},
                        't_full': {k[4:]: int(v) for k, v in env.items() if k.startswith('SLt_')},
                        'fs': fs, 'ft': ft})
    # Phase 2: extend each entry forward until shallow
    excursions = []
    for ei, e in enumerate(entries):
        cA, cB = e['postA'], e['postB']
        legs = [{'w': e['w'], 'pair': '01', 's': e['fs'], 't': e['ft'],
                 's_full': e['s_full'], 't_full': e['t_full']}]
        for step in range(5):
            if time.process_time() - t0 > budget:
                break
            y = rng.choice(sorted(MSET))
            try:
                R = replay([('K', y)], cA, cB)
            except Exception:
                break
            if not R['agree']:
                break
            H = sum(l['a'] for l in R['legs'])
            try:
                st, info = ssertify(d, L, cA, cB, SSET, MSET, [('K', y)], H)
            except Exception:
                break
            if st != 'ok':
                break
            env = dict(info['env'])
            fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
            ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
            if any(v is None for v in list(fs.values()) + list(ft.values())):
                break
            gs = 1 if fs['b_depth_max'] >= 7 else 0
            gt = 1 if ft['b_depth_max'] >= 7 else 0
            legs.append({'w': int(info['w']), 'pair': '%d%d' % (gs, gt), 's': fs, 't': ft,
                           's_full': {k[4:]: int(v) for k, v in env.items() if k.startswith('SLs_')},
                           't_full': {k[4:]: int(v) for k, v in env.items() if k.startswith('SLt_')},
                           'serialA': cA, 'serialB': cB, 'y': y})
            cA, cB = tl2list(R['S1'][0]), tl2list(R['S1'][1])
            if gt == 0:
                break
        # check excursion shape 01 (11)* 10
        if len(legs) >= 2 and legs[0]['pair'] == '01' and legs[-1]['pair'] == '10' and all(
                l['pair'] == '11' for l in legs[1:-1]):
            wP = sum(l['w'] for l in legs)
            RP = wP - (C5(legs[-1]['t']) - C5(legs[0]['s']))
            excursions.append({'legs': legs, 'wP': wP, 'RP': RP, 'holds': bool(RP >= 0)})
    json.dump({'n_screened': nscr, 'n_certified_01': ncert, 'n_entries': len(entries),
               'excursions': excursions, 'cpu_s': time.process_time() - t0},
              open(OUT + 'CL02_PAIRED_EXCURSIONS' + suf + '.json', 'w'), indent=1)
    print('screened=%d entries=%d excursions=%d holds=%s cpu=%.1f' % (
        nscr, len(entries), len(excursions), [e['holds'] for e in excursions], time.process_time() - t0), flush=True)
