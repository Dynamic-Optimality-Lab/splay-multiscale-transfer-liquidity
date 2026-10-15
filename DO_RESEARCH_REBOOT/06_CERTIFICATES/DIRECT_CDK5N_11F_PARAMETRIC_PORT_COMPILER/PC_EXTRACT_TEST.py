# PC_EXTRACT_TEST.py — production SAT: pin abstract endpoints+costs, solver finds xi.
# Graded: full-scope first (honest cap), then slot-bounded scopes to map the feasible frontier.
import sys, json, time
sys.setrecursionlimit(1000000)
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from PC_TYPED_DAG import DAG
from PC_LOW_COMPILER import build_low
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN
from PC_CONCRETIZE import serial

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def chain_desc(ks):
    t = S.LEAF
    for k in sorted(ks):
        t = S.node(k, t, S.LEAF)
    return t


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    L = build_low(d, 'PL')
    print('built low: nodes=%d vars=%d' % (d.count(), len(d.vars)), flush=True)
    # deterministic E3 transition (phase-0 case 1)
    keys = list(range(1, 13))
    m0, x = 12, 6
    Sset = set([6, 7, 8, 9, 10, 11, 12, 1, 2])
    M = {6, 12, 9, 10, 11}
    lo = sorted(k for k in keys if k < x)
    hi = sorted(k for k in keys if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in keys if k != m0]), S.LEAF)
    from PC_CERTIFY import certify
    st, info = certify(d, L, serial(A), serial(B), Sset, M, [('K', x)], 1)
    print('grounded:', st, info if st != 'ok' else (info['H'], info['q'], info['w']), flush=True)
    assert st == 'ok'
    # pin abstract endpoints: rebuild env fully then KEEP only abstract+cost pins
    # (re-derive by re-running certify internals? simpler: pin via a fresh grounded env)
    # We reconstruct the pin set from a full env by selecting abstract var names.
    import PC_LOW_TEST_RUN as _t  # noqa (ensures same construction)
    # rebuild full env for pin extraction
    from PC_CONCRETIZE import (AModel, BModel, depths_keys, build_envA, build_envB, build_envBT,
                               build_envW, build_envI, shadow_of)
    from CRA_pointer_tuple_replay import replay, from_serial
    R = replay([('K', x)], A0=serial(A), B0=serial(B))
    A0 = from_serial(R['pairs'][0][0])
    Ad = from_serial(R['pairs'][-1][0])
    Bd = from_serial(R['pairs'][-1][1])
    am = AModel(A0, Sset)
    Ss = sorted(Sset)
    mu = sum(1 << Ss.index(m) for m in M)
    env_full = {}
    build_envA(env_full, am, Sset, 'PLw')
    build_envI(env_full, am, Sset, 'PLv')
    env_full['PL_H'] = 1
    env_full['PL_w'] = info['w']
    env_full['PLbt_q'] = info['q']
    env_full['PLs_mu'] = mu
    env_full['PLt_mu'] = mu
    for pre, T in (('PLs', A0), ('PLt', Ad)):
        sh = shadow_of(T)
        rk, (lk, lr), (rk2, rr) = sh
        env_full[pre + '_arS'] = 1 if rk in Sset else 0
        env_full[pre + '_arI'] = Ss.index(rk) if rk in Sset else 0
        for kk, ref, cS, cI, cK in ((lk, lr, pre + '_aLS', pre + '_aLI', pre + '_aLk'),
                                    (rk2, rr, pre + '_aRS', pre + '_aRI', pre + '_aRk')):
            env_full[cK] = kk
            env_full[cS] = 1 if (ref is not None and ref in Sset) else 0
            env_full[cI] = Ss.index(ref) if (ref is not None and ref in Sset) else 0
    for pre, BB in (('PLs', BModel(from_serial(R['pairs'][0][1]), Sset)), ('PLt', BModel(Bd, Sset))):
        build_envB(env_full, BB, Sset, pre + '_b')
    for pre in ('PLs', 'PLt'):
        am2 = am if pre == 'PLs' else AModel(Ad, Sset)
        for i in range(10):
            env_full[pre + f'_sg{i}'] = am2.sig[i]
    # pin names: abstract endpoints + H/w/q (NOT witness vars PLw_*/PLv_*/PLbt_*/PL_b0_*)
    pins = {k: v for k, v in env_full.items()
            if k.startswith('PLs_') or k.startswith('PLt_') or k in ('PL_H', 'PL_w', 'PLbt_q')}
    print('pins: %d (abstract+costs)' % len(pins), flush=True)
    results = {}
    # grade 1: full scope, 300s
    sv = Solver(d, node_cap=3000000, time_cap=300)
    r, menv, stats = sv.solve(L['root'], assume=pins)
    print('full-scope extraction:', r, stats, flush=True)
    results['full'] = {'result': r, 'stats': stats}
    if r == SAT:
        # verify model satisfies root
        print('model verifies:', d.ev_iter(L['root'], menv), flush=True)
    json.dump(results, open(PDIR + 'PC_EXTRACT_TEST.json', 'w'), indent=1)
    print('time=%.1fs' % (time.time() - t0), flush=True)
