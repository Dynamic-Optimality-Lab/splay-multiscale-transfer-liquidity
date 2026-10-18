# G03_GROUNDED_FALSIFY.py — CEGIS falsification: random grounded single-KEEP edges.
# For each: random A/B trees + marked set, replay KEEP, ssertify env, features,
# check Phi(t)-Phi(s) <= w. Violations return as new seeds (or refutation evidence).
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'

import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CRA_pointer_tuple_replay import replay
from G03_POTENTIAL_FEATURES import eval_all
from G03_CANDIDATE_SYNTHESIS import RANK_FEATS as FEATS


def rand_tree(keys, rng):
    ks = list(keys)
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


def chain_tree(keys, rng):
    ks = sorted(keys)
    t = S.LEAF

    def ins(n, k):
        if n[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = n
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in ks:
        t = ins(t, k)
    return t


def zigzag_tree(keys, rng):
    ks = sorted(keys)
    # alternate low/high to force zigzag shape
    lo, hi, order = 0, len(ks) - 1, []
    flip = True
    while lo <= hi:
        if flip:
            order.append(ks[lo])
            lo += 1
        else:
            order.append(ks[hi])
            hi -= 1
        flip = not flip
    t = S.LEAF

    def ins(n, k):
        if n[0] == 'leaf':
            return S.node(k, S.LEAF, S.LEAF)
        _, kk, l, rr = n
        return S.node(kk, ins(l, k), rr) if k < kk else S.node(kk, l, ins(rr, k))

    for k in order:
        t = ins(t, k)
    return t


def eval_phi(theta, c0, fenv):
    tot = c0
    for f, v in theta.items():
        if v:
            tot += v * fenv[f]
    return tot


def _root_key(t):
    return None if t[0] == 'leaf' else t[1]


def _deepest_key(t, M):
    best = [None, -1]

    def rec(n, d):
        if n[0] == 'leaf':
            return
        _, k, l, rr = n
        if k in M and d > best[1]:
            best[0], best[1] = k, d
        rec(l, d + 1)
        rec(rr, d + 1)

    rec(t, 0)
    return best[0]


if __name__ == '__main__':
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 40
    seed = int(_s.argv[2]) if len(_s.argv) > 2 else 1
    _s.modules['__main__']._XMODE = _s.argv[3] if len(_s.argv) > 3 else 'mix'
    cand = json.load(open(PDIR + 'G03_CANDIDATE_POTENTIAL.json'))
    th, c0 = cand['theta'], cand['c']
    r = random.Random(seed)
    d = DAG()
    L = build_slow(d, 'SL')
    viol = []
    tried = ok = 0
    hdist = {}
    t0 = time.process_time()
    while tried < n and time.process_time() - t0 < 1500:
        keys = list(range(1, 10))
        u = r.random()
        mk = rand_tree if u < 0.6 else (chain_tree if u < 0.8 else zigzag_tree)
        A = mk(keys, r)
        B = mk(keys, r)
        M = set(r.sample(keys, 5))
        Sset = set(keys)
        # targeted x: root (H~0), deepest (H large), or random member
        _mode = _s.modules['__main__']._XMODE
        if _mode == 'root':
            _rk = _root_key(A)
            x = _rk if _rk in M else r.choice(sorted(M))
        elif _mode == 'deep':
            _dk = _deepest_key(A, M)
            x = _dk if _dk is not None else r.choice(sorted(M))
        else:
            v = r.random()
            if v < 0.25:
                _rk = _root_key(A)
                x = _rk if _rk in M else r.choice(sorted(M))
            elif v < 0.5:
                _dk = _deepest_key(A, M)
                x = _dk if _dk is not None else r.choice(sorted(M))
            else:
                x = r.choice(sorted(M))
        try:
            R = replay([('K', x)], serial(A), serial(B))
        except Exception:
            continue
        if not R['agree']:
            continue
        H = sum(l['a'] for l in R['legs'])
        if H > 9:
            continue
        try:
            st, info = ssertify(d, L, serial(A), serial(B), Sset, M, [('K', x)], H)
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
        tried += 1
        hdist[H] = hdist.get(H, 0) + 1
        w = int(info['w'])
        lhs = eval_phi(th, c0, ft) - eval_phi(th, c0, fs)
        if lhs <= w:
            ok += 1
        else:
            viol.append({'s': fs, 't': ft, 'w': w, 'lhs': lhs})
    print('tried=%d ok=%d viol=%d cpu=%.1f hdist=%s' % (tried, ok, len(viol), time.process_time() - t0, hdist), flush=True)
    json.dump({'tried': tried, 'ok': ok, 'hdist': hdist, 'violations': viol[:20]}, open(PDIR + 'G03_FALSIFY_RUN.json', 'w'), indent=1)
