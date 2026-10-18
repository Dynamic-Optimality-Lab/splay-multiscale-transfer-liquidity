# SR02C_BASE_RATES.py — base ok/skip/fail rates + upward-jump certification rate.
import sys, json, os, time, random, collections
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


if __name__ == '__main__':
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 400
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 501
    rng = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    stat = collections.Counter()
    skipr = collections.Counter()
    up_ok = up_fail = up_skip = 0
    okpairs = collections.Counter()
    saved = []
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
            stat['replay-exc'] += 1
            continue
        if not R['agree']:
            stat['disagree'] += 1
            continue
        H = sum(l['a'] for l in R['legs'])
        try:
            st, info = ssertify(d, L, serial(A), serial(B), set(range(1, 10)), M, [('K', x)], H)
        except Exception:
            stat['ssertify-exc'] += 1
            continue
        d0 = depths_of(from_serial(R['S0'][1]))
        d1 = depths_of(from_serial(R['S1'][1]))
        up = (d1 and d0 and max(d1.values()) > max(d0.values()))
        if st == 'ok':
            stat['ok'] += 1
            if up:
                up_ok += 1
            env = dict(info['env'])
            fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
            ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
            gp = '%d%d' % (1 if fs['b_depth_max'] >= 7 else 0, 1 if ft['b_depth_max'] >= 7 else 0)
            okpairs[gp] += 1
            if gp == '01':
                saved.append({'s': fs, 't': ft, 'w': int(info['w'])})
        elif st == 'skip':
            stat['skip'] += 1
            skipr[str(info)[:40]] += 1
            if up:
                up_skip += 1
        else:
            stat['fail'] += 1
            if up:
                up_fail += 1
    json.dump({'n': n, 'status': dict(stat), 'skip_reasons': dict(skipr),
               'upward': {'ok': up_ok, 'skip': up_skip, 'fail': up_fail},
               'ok_pairs': dict(okpairs), 'ok_01_edges': saved,
               'cpu_s': time.process_time() - t0},
              open(OUT + 'SR02C_BASE_RATES.json', 'w'), indent=1)
    print(dict(stat), dict(skipr), 'up:', up_ok, up_skip, up_fail, dict(okpairs), flush=True)
