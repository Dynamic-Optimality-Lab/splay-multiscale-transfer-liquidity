# PC_DEBUG3.py — fuzz B-splay symbolic vs concrete over all patterns/depths.
import sys, random
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_B_CONTROLLER import BState, BTrace, verify_bpath, b_splay_event, NB
from PC_CONCRETIZE import BModel, serial, depths_keys

Sset = set(range(1, 10))
rng = random.Random(5)
d = DAG()
bs = BState(d, 't0')
bt = BTrace(d, 'tt')

nm = 0
for trial in range(400):
    n = 11
    ks = list(range(1, n + 1))
    t = S.LEAF
    ins = sorted(ks)
    rng.shuffle(ins)
    def _ins(t, k):
        return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
    for k in ins:
        t = _ins(t, k)
    T0 = serial(t)
    x = rng.choice(sorted(Sset))
    try:
        R = replay([('K', x)], A0=T0, B0=T0)
    except Exception:
        continue
    if not R['agree']:
        continue
    B0 = from_serial(R['pairs'][0][1])
    B1 = from_serial(R['pairs'][-1][1])
    bm0 = BModel(B0, Sset)
    bm1 = BModel(B1, Sset)
    if not (bm0.ok and bm1.ok):
        continue
    # all-core ancestors filter for exactness
    dk = depths_keys(B0)
    a = dk[x][1]
    okc = True
    while a is not None:
        if a not in Sset:
            okc = False
            break
        a = dk[a][1]
    if not okc:
        continue
    pth, drs = bm0.path_to_core(x)
    if len(pth) - 1 != dk[x][0]:
        print('DEPTH-MISMATCH', trial)
        continue
    env = {}
    from PC_CONCRETIZE import build_envB
    build_envB(env, bm0, Sset, 't0')
    env['tt_bT0'] = bm0.sidx[x]
    env['tt_bd0'] = len(pth) - 1
    for k in range(19):
        env[f'tt_bp0_{k}'] = bm0.sidx[pth[k]] if k < len(pth) else 0
    for k in range(18):
        env[f'tt_bdir0_{k}'] = drs[k] if k < len(drs) else 0
    for e in range(1, 5):
        env[f'tt_bT{e}'] = 0
        env[f'tt_bd{e}'] = 0
        for k in range(19):
            env[f'tt_bp{e}_{k}'] = 0
        for k in range(18):
            env[f'tt_bdir{e}_{k}'] = 0
    if d.ev_iter(verify_bpath(d, bs, bt, 0), env) is not True:
        print('VERIFY-FAIL', trial)
        continue
    end = b_splay_event(d, bs, bt, 0, d.const_bool(False))
    memo = {}
    bad = []
    for k in sorted(Sset):
        i = bm0.sidx[k]
        for side, kk, rr_ in ((0, d.ev_iter(end.kl[i], env, memo), d.ev_iter(end.rl[i], env, memo)),
                              (1, d.ev_iter(end.kr[i], env, memo), d.ev_iter(end.rr[i], env, memo))):
            e = bm1.sk.get((i, side))
            exp = ('C', e[1]) if e[0] == 'C' else None
            got = ('C', rr_) if kk == 0 else None
            if exp != got:
                bad.append((k, side, exp, got))
    if bad:
        print('DIVERGE trial=%d x=%d depth=%d bad=%s' % (trial, x, len(pth) - 1, bad[:4]))
    else:
        nm += 1
print('matched:', nm)
