# SR02C_COUNTEREXAMPLE_HUNT.py — targeted 0->1 capture with FULL states.
# Screen replay-only for proxy (5|6)->(7|8) jumps; ssertify each; save full
# envs + features + Phi verdict. A verified Phi(t)-Phi(s)>w = refutation.
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
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
OUT = os.environ.get('RESCUE_OUT5', 'x')
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


def C2(f):
    return f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def Phi(f):
    return C2(f) if f['b_depth_max'] >= 7 else C5(f)


if __name__ == '__main__':
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 2000
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 601
    rng = random.Random(seed)
    t0 = time.process_time()
    d = DAG()
    L = build_slow(d, 'SL')
    found = []
    nscr = 0
    for i in range(n):
        ks = list(range(1, 10))
        rng.shuffle(ks)
        A = S.LEAF

        def ins(nn, k):
            if nn[0] == 'leaf':
                return S.node(k, S.LEAF, S.LEAF)
            _, kk, l, rr = nn
            return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

        for k in ks:
            A = ins(A, k)
        ks2 = list(range(1, 10))
        rng.shuffle(ks2)
        B = S.LEAF
        for k in ks2:
            B = ins(B, k)
        M = {1, 3, 5, 7, 9}
        x = rng.choice(sorted(M))
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
        m0, m1 = max(d0.values()), max(d1.values())
        if not (m0 in (5, 6) and m1 in (7, 8) and m1 > m0):
            continue
        H = sum(l['a'] for l in R['legs'])
        try:
            st, info = ssertify(d, L, serial(A), serial(B), set(range(1, 10)), M, [('K', x)], H)
        except Exception:
            continue
        if st != 'ok':
            continue
        env = dict(info['env'])
        sp = {k: v for k, v in env.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in env.items() if k.startswith('SLt_')}
        fs = eval_all(sp, 'SLs')
        ft = eval_all(tp, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        if not (fs['b_depth_max'] <= 6 and ft['b_depth_max'] >= 7):
            continue
        w = int(info['w'])
        lhs = Phi(ft) - Phi(fs)
        found.append({'w': w, 'lhs': lhs, 'holds': bool(lhs <= w),
                      'C2s': C2(fs), 'C2t': C2(ft), 'C5s': C5(fs), 'C5t': C5(ft),
                      's': fs, 't': ft,
                      'source_state': {k[4:]: int(v) for k, v in sp.items()},
                      'destination_state': {k[4:]: int(v) for k, v in tp.items()},
                      'provenance': 'seed=%d x=%d H=%d' % (seed, x, H)})
        if len(found) >= 6:
            break
    json.dump({'n_screened': nscr, 'n_captured': len(found), 'counterexamples': found,
               'cpu_s': time.process_time() - t0},
              open(OUT + 'SR02C_COUNTEREXAMPLE_CERTIFICATES.json', 'w'), indent=1)
    print('screened=%d captured=%d viol=%s cpu=%.1f' % (
        nscr, len(found), [(c['w'], c['lhs']) for c in found], time.process_time() - t0), flush=True)
