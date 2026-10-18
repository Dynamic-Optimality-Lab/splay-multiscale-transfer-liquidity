# SR02_GUARDED_FALSIFY.py — concrete falsification of the SR-01 guarded candidate
# Phi(s) = C2(s) if dmax>=7 else C5(s). Fresh ssertify-ok single-KEEP edges
# (mix/root/deep + crossing bias), exact edgewise check per guard pair.
# A verified violation (ssertify-ok + repaired-canon endpoints) REFUTES the
# candidate universally (Outcome B). No violation = stronger evidence only.
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
OUT = os.environ.get('RESCUE_OUT4', 'x')
if not OUT.endswith('/') and not OUT.endswith('\\'):
    OUT = OUT + '/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03_POTENTIAL_FEATURES import eval_all


def C2(f):
    return f['b_rank_sum'] - f['b_depth_max'] + f['a_marked_count']


def C5(f):
    return f['b_rank_sum'] - f['b_rank_marked']


def Phi(f):
    return C2(f) if f['b_depth_max'] >= 7 else C5(f)


def guard(f):
    return 1 if f['b_depth_max'] >= 7 else 0


def rand_tree(rng, mode):
    ks = list(range(1, 10)) if mode != 'chain' else sorted(range(1, 10))
    if mode == 'zigzag':
        ks = sorted(ks)
        lo, hi, ks2, flip = 0, len(ks) - 1, [], True
        while lo <= hi:
            if flip:
                ks2.append(ks[lo]); lo += 1
            else:
                ks2.append(ks[hi]); hi -= 1
            flip = not flip
        ks = ks2
    elif mode != 'chain':
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
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 40
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 101
    rng = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    t0 = time.process_time()
    tried = ok = 0
    viol = []
    pairs = {'00': 0, '01': 0, '10': 0, '11': 0}
    while tried < n and time.process_time() - t0 < 1500:
        u = rng.random()
        mk = 'rand' if u < 0.6 else ('chain' if u < 0.8 else 'zigzag')
        A, B = rand_tree(rng, mk), rand_tree(rng, mk)
        M = set(rng.sample(list(range(1, 10)), 5))
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
        except Exception:
            continue
        if st != 'ok':
            continue
        env = dict(info['env'])
        fs = eval_all({k: v for k, v in env.items() if k.startswith('SLs_')}, 'SLs')
        ft = eval_all({k: v for k, v in env.items() if k.startswith('SLt_')}, 'SLt')
        if any(v is None for v in list(fs.values()) + list(ft.values())):
            continue
        tried += 1
        gs, gt = guard(fs), guard(ft)
        pairs['%d%d' % (gs, gt)] += 1
        lhs = Phi(ft) - Phi(fs)
        w = int(info['w'])
        if lhs <= w:
            ok += 1
        else:
            viol.append({'w': w, 'lhs': lhs, 'pair': '%d%d' % (gs, gt),
                         's': fs, 't': ft,
                         'C2s': C2(fs), 'C2t': C2(ft), 'C5s': C5(fs), 'C5t': C5(ft)})
    json.dump({'tried': tried, 'ok': ok, 'nviol': len(viol), 'pairs': pairs,
               'violations': viol, 'cpu_s': time.process_time() - t0},
              open(OUT + 'SR02_GUARDED_FALSIFY.json', 'w'), indent=1)
    print('tried=%d ok=%d viol=%d pairs=%s cpu=%.1f' % (tried, ok, len(viol), pairs, time.process_time() - t0), flush=True)
