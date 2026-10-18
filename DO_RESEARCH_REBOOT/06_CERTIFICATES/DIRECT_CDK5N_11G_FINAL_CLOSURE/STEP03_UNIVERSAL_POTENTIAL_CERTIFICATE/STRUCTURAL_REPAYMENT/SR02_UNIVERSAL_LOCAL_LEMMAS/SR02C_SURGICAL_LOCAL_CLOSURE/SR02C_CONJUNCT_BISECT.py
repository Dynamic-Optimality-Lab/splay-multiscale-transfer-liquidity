# SR02C_CONJUNCT_BISECT.py — for replay-valid but relation-false ('fail') edges:
# determine whether abstract endpoints are valid (A4-type failure) or the
# transition conjuncts reject valid endpoints. Proxy depth jumps included.
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
OUT = os.environ.get('RESCUE_OUT5', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay, from_serial
from G03R_CANONICAL_STATE import dict_of_env, valid_state_dict
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
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 300
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 401
    rng = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    rows = []
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
        H = sum(l['a'] for l in R['legs'])
        try:
            st, info = ssertify(d, L, serial(A), serial(B), set(range(1, 10)), M, [('K', x)], H)
        except Exception as e:
            continue
        if st != 'fail' or not isinstance(info, dict) or 'env' not in info:
            continue
        env = info['env']
        try:
            ds = dict_of_env(env, 'SLs_')
            dt = dict_of_env(env, 'SLt_')
            vs, ws = valid_state_dict(ds)
            vt, wt = valid_state_dict(dt)
        except Exception as e:
            vs, ws, vt, wt = False, 'exc', False, 'exc'
        fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
        ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
        d0 = depths_of(from_serial(R['S0'][1]))
        d1 = depths_of(from_serial(R['S1'][1]))
        rows.append({'w': info.get('w'), 'H': info.get('H'), 'q': info.get('q'),
                     's_valid': bool(vs), 's_why': ws, 't_valid': bool(vt), 't_why': wt,
                     'proxy_dmax': [max(d0.values()), max(d1.values())] if d0 and d1 else None,
                     'abstract_dmax': [fs.get('b_depth_max'), ft.get('b_depth_max')]})
        if len(rows) >= 15:
            break
    json.dump({'n_fail_analyzed': len(rows), 'rows': rows, 'cpu_s': time.process_time() - t0},
              open(OUT + 'SR02C_CONJUNCT_BISECT.json', 'w'), indent=1)
    print('fails=%d cpu=%.1f' % (len(rows), time.process_time() - t0), flush=True)
    for r in rows[:8]:
        print({k: r[k] for k in ('w', 's_valid', 's_why', 't_valid', 't_why', 'proxy_dmax', 'abstract_dmax')}, flush=True)
