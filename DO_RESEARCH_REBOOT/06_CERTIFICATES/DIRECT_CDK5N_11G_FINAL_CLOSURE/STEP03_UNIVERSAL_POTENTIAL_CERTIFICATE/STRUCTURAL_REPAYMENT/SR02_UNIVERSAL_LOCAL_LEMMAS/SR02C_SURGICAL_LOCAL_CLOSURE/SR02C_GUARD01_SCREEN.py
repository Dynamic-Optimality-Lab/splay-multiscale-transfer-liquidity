# SR02C_GUARD01_SCREEN.py — PHASE A: replay-only 0->1 screen (cheap).
# For N random single-KEEP concrete edges: B-depths pre/post from tuple
# trees (proxy dmax = max depth over keys). Flag upward jumps into deep
# zone (post>=6 & post>pre); ssertify-certify top candidates (exact abstract
# dmax via features) and evaluate guarded Phi edgewise.
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


def rtree(rng):
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


def C2(f):
    return f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def Phi(f):
    return C2(f) if f['b_depth_max'] >= 7 else C5(f)


if __name__ == '__main__':
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 1500
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 301
    rng = random.Random(seed)
    t0 = time.process_time()
    pairs = {}
    cands = []
    maxjump = 0
    for i in range(n):
        A, B = rtree(rng), rtree(rng)
        M = {1, 3, 5, 7, 9} if i % 2 == 0 else {1, 2, 3, 4, 5}
        x = rng.choice(sorted(M))
        try:
            R = replay([('K', x)], serial(A), serial(B))
        except Exception:
            continue
        if not R['agree']:
            continue
        d0 = depths_of(from_serial(R['S0'][1]))
        d1 = depths_of(from_serial(R['S1'][1]))
        if not d0 or not d1:
            continue
        m0, m1 = max(d0.values()), max(d1.values())
        maxjump = max(maxjump, m1 - m0)
        if m1 >= 6 and m1 > m0:
            cands.append((m0, m1, serial(A), serial(B), M, x, R['S1']))
    # certify top candidates by jump
    cands.sort(reverse=True)
    d = DAG()
    L = build_slow(d, 'SL')
    cert = []
    for (m0, m1, sA, sB, M, x, S1) in cands[:12]:
        try:
            R2 = replay([('K', x)], sA, sB)
            H = sum(l['a'] for l in R2['legs'])
            st, info = ssertify(d, L, sA, sB, set(range(1, 10)), M, [('K', x)], H)
        except Exception as e:
            cert.append({'proxy': [m0, m1], 'ssertify': 'exc %s' % str(e)[:80]})
            continue
        if st != 'ok':
            cert.append({'proxy': [m0, m1], 'ssertify': st, 'reason': str(info)[:100]})
            continue
        env = dict(info['env'])
        fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
        ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        w = int(info['w'])
        lhs = Phi(ft) - Phi(fs)
        cert.append({'proxy': [m0, m1], 'abstract_dmax': [fs['b_depth_max'], ft['b_depth_max']],
                     'w': w, 'lhs': lhs, 'holds': bool(lhs <= w),
                     'pair': '%d%d' % (1 if fs['b_depth_max'] >= 7 else 0, 1 if ft['b_depth_max'] >= 7 else 0)})
    json.dump({'n_screened': n, 'n_candidates': len(cands), 'max_upward_jump': maxjump,
               'certified': cert, 'cpu_s': time.process_time() - t0,
               'note': 'proxy=max concrete B-depth; abstract dmax via ssertify features on hits'},
              open(OUT + 'SR02C_GUARD01_RESULTS.json', 'w'), indent=1)
    print('screened=%d cands=%d maxjump=%d certified=%s cpu=%.1f' % (
        n, len(cands), maxjump,
        [(c.get('abstract_dmax'), c.get('w'), c.get('holds')) for c in cert],
        time.process_time() - t0), flush=True)
