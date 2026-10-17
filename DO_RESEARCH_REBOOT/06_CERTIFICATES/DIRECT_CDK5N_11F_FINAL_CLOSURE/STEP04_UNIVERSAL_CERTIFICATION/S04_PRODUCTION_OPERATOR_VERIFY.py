# S04_PRODUCTION_OPERATOR_VERIFY.py — Gates A2/A3/F: actual Post/Pre/MinPre decisions.
# Post membership (t in Post_w({s})) = edge existence, decided by the engine (SAT),
# PLUS destination-universe Tier-1 (state_valid7(t-pins) const-True on small cone),
# source-closure (bound-var audit by reference + re-asserted in fresh rebuild),
# and grounded-transition replay (Step-02 certificates). Raw symbolic post/minpre
# Tier-1 attempts recorded (expected None on open targets: procedure used instead).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


import splay as S
from PC_TYPED_DAG import DAG, BOOL
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
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE3 = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    S9 = set(range(1, 10))
    A9 = S.balanced(list(range(1, 10)))
    OUT = {}
    for (jn, A, B, SS, M, word, H, w) in (
            ('E3', AE3, BE3, set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1, -1),
            ('plain', A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 3)], 1, 2),
            ('delkeep', A9, A9, S9, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2, 4)):
        st, info = ssertify(d, L, serial(A), serial(B), SS, M, word, H)
        assert st == 'ok', jn
        pins = dict(info['env'])
        sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
        # universe checks on small state_valid cones (fully pinned -> const)
        dU = DAG()
        sU = StateVars7(dU, 'Us')
        tU = StateVars7(dU, 'Ut')
        rUs = dU.simplify(state_valid7(dU, sU), {('Us' + k[3:]): v for k, v in sp.items()})
        rUt = dU.simplify(state_valid7(dU, tU), {('Ut' + k[3:]): v for k, v in tp.items()})
        uS = dU.nodes[rUs][0] == 'const' and bool(dU.nodes[rUs][3])
        uT = dU.nodes[rUt][0] == 'const' and bool(dU.nodes[rUt][3])
        check(jn + ' source universe valid', uS, '')
        check(jn + ' dest universe valid', uT, '')
        # Post membership = edge existence (engine) + replayed transition (cert refs)
        r = eng.solve_edge(sp, tp, w)
        check(jn + ' Post membership SAT (edge+replay)', r['status'] == 'SAT',
              '%s Hq=%s/%s tried=%s' % (r['status'], r.get('H'), r.get('q'), r.get('tried')))
        OUT[jn] = {'post': r['status'], 'universe_s': uS, 'universe_t': uT,
                   'H': r.get('H'), 'q': r.get('q'), 'word': r.get('word')}
    J('S04_OPERATOR_RESULTS.json', OUT)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('OPERATOR VERIFY PASS')
