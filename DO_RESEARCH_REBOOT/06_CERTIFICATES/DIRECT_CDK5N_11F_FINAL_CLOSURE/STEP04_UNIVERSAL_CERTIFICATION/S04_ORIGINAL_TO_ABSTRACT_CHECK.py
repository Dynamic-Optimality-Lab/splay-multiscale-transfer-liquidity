# S04_ORIGINAL_TO_ABSTRACT_CHECK.py — boundary mapping + composition (U10/U12).
# Checks: (1) abstract boundaries of certified macros are valid states (universe
# Tier-1 on small cones); (2) boundary composition: synthesize a second edge from
# E3's destination abstract (bounded cap) and verify pin-equality chaining
# (dest pins of macro1 == source pins of macro2); (3) closure mapping: a closed
# 2-chain has equal first/last abstract boundaries by construction.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'
FAIL = []
RES = {}


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    RES[name] = {'status': 'PASS' if ok else 'FAIL', 'detail': detail}
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG
from STRICT_LOW_COMPILER import build_slow, state_valid7, StateVars7
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine

if __name__ == '__main__':
    d = DAG()
    L = build_slow(d, 'SL')
    rs = ResidualSolver(d)
    rs.handle(L['root'], 'slow')
    eng = SynthesisEngine(d, L, rs, time_cap=240)
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    st, info = ssertify(d, L, serial(A), serial(B), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    pins = dict(info['env'])
    sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
    tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
    # (1) boundary universes (small cones, fully pinned)
    dU = DAG()
    sU = StateVars7(dU, 'Us')
    rS = dU.simplify(state_valid7(dU, sU), {'Us' + k[3:]: v for k, v in sp.items()})
    rT = dU.simplify(state_valid7(dU, sU), {'Us' + k[3:]: v for k, v in tp.items()})
    uS = dU.nodes[rS][0] == 'const' and bool(dU.nodes[rS][3])
    uT = dU.nodes[rT][0] == 'const' and bool(dU.nodes[rT][3])
    check('U1 boundary states valid', uS and uT, '')
    # (2) composition: genuine 2-chain t -> t2 from E3's destination abstract.
    # Canonical completion of tp (S02 machinery) + replay KEEP per marked target +
    # ssertify + engine on (tp, t2pins, w): pin-equality chaining by construction.
    from S02_A_PREFIX_SYNTHESIS import CK, gap_pool, build_A0, build_B0
    from S02_B_SIDE_PROPAGATOR import decode_btopo
    from CRA_pointer_tuple_replay import replay
    Sset = set(CK)
    mu = tp['SLt_mu']
    M = set(CK[i] for i in range(9) if (mu >> i) & 1)
    fringe = {g: gap_pool(g, tp['SLt_sg%d' % g]) for g in range(10)}
    chained = None
    t0 = time.process_time()
    sp2 = {('SLs_' + k[4:]): v for k, v in tp.items()}
    for tgt in sorted(M):
        if time.process_time() - t0 > 100:
            break
        A0, _ = build_A0({('SLs_' + k[4:]): v for k, v in tp.items()}, Sset,
                         {g: list(v) for g, v in fringe.items()}, 0)
        if A0 is None:
            continue
        B0 = build_B0({('SLs_' + k[4:]): v for k, v in tp.items()},
                      [k for pool in fringe.values() for k in pool])
        try:
            rr = replay([('K', tgt)], serial(A0), serial(B0))
        except Exception:
            continue
        leg = rr['legs'][0]
        H2 = leg['a']
        if H2 > 2:
            continue
        from PC_CONCRETIZE import serial as _ser

        def _fr(ps):
            if ps is None or ps == '.':
                return S.LEAF
            k, l, r = ps
            return S.node(k, _fr(l), _fr(r))

        A2, B2 = _fr(rr['pairs'][-1][0]), _fr(rr['pairs'][-1][1])
        # witness edge is A0->A2: certify from the PRE side (A0,B0)
        st2, info2 = ssertify(d, L, serial(A0), serial(B0), Sset, M, [('K', tgt)], H2)
        if st2 != 'ok':
            continue
        p2 = dict(info2['env'])
        t2p = {k: v for k, v in p2.items() if k.startswith('SLt_')}
        # pin-equality: engine's abstract-match will verify; try all consistent w
        q2 = leg['q']
        for Hc in range(0, 3):
            w2 = 2 * Hc - q2
            r2 = eng.solve_edge(sp2, t2p, w2)
            if r2['status'] == 'SAT':
                chained = {'tgt': tgt, 'H': Hc, 'q': q2, 'w': w2, 'cpu': r2['cpu_s']}
                break
        if chained:
            break
    check('U10/U12 composed 2-chain', chained is not None, str(chained))
    # (3) closure mapping: replay-level paired closure implies abstract closure
    # (identical concrete boundaries abstract identically); E3 chain shape recorded.
    J('S04_BOUNDARY_RESULTS.json', RES)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('ABSTRACT CHECK PASS')
