# PC_DEBUG2.py — isolate single B-splay: symbolic (b_single_rot chain) vs concrete replay.
import sys
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_B_CONTROLLER import BState, BTrace, b_valid, verify_bpath, b_splay_event, muxb, NB
from PC_CONCRETIZE import BModel, serial, depths_keys, build_envB, gap_of

# concrete: small fixed case — S=1..9 in an 11-key tree, KEEP a marked key
Sset = set(range(1, 10))
Ss = sorted(Sset)
t = S.LEAF
for k in [6, 3, 9, 1, 5, 11, 2, 4, 7, 8, 10]:
    def _ins(t, k):
        return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
    t = _ins(t, k)
T0 = serial(t)
Rw = replay([('K', 5)], A0=T0, B0=T0)
assert Rw['agree'] and Rw['legs'][0]['chg']
T1B = Rw['pairs'][-1][1]
B0 = from_serial(T1B)
print('B0 root:', [k for k, (dd, p, s) in depths_keys(B0).items() if p is None])
R = replay([('K', 3)], A0=serial(from_serial(Rw['pairs'][-1][0])), B0=serial(B0))
assert R['agree']
B1 = from_serial(R['pairs'][-1][1])
print('B1 root:', [k for k, (dd, p, s) in depths_keys(B1).items() if p is None])
print('chg:', R['legs'][0]['chg'], 'dB:', R['legs'][0]['dB'])
bm0 = BModel(B0, Sset)
bm1 = BModel(B1, Sset)
print('bm0 ok:', bm0.ok, 'bm1 ok:', bm1.ok)
# symbolic: assign bm0 vars, path for target 3, one b_splay_event
d = DAG()
bs = BState(d, 't0')
bt = BTrace(d, 'tt')
env = {}
build_envB(env, bm0, Sset, 't0')
# path of target sidx(3)=2 in bm0
pth, drs = bm0.path_to_core(3)
print('path:', pth, 'dirs:', drs, 'depth:', len(pth) - 1, 'concrete dB:', S.lookup(B0, 3)[1])
env['tt_bT0'] = 2
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
print('verify:', d.ev_iter(verify_bpath(d, bs, bt, 0), env))
end = b_splay_event(d, bs, bt, 0, d.const_bool(False))
memo = {}
kl = [d.ev_iter(n, env, memo) for n in end.kl]
rl = [d.ev_iter(n, env, memo) for n in end.rl]
kr = [d.ev_iter(n, env, memo) for n in end.kr]
rr = [d.ev_iter(n, env, memo) for n in end.rr]
print('sym root:', d.ev_iter(end.root, env, memo))
# compare core links with bm1.sk
ok = True
for k in Ss:
    i = bm0.sidx[k]
    for side, kk, rr_ in ((0, kl[i], rl[i]), (1, kr[i], rr[i])):
        e = bm1.sk.get((i, side))
        exp = ('C', e[1]) if e[0] == 'C' else None
        got = ('C', rr_) if kk == 0 else None
        if exp != got:
            print('MISMATCH core', k, 'side', side, 'expected', exp, 'got', got)
            ok = False
print('MATCH' if ok else 'DIVERGED')
