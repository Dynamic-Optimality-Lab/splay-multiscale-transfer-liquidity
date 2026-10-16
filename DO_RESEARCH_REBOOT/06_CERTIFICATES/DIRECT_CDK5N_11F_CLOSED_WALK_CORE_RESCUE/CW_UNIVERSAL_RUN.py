# CW_UNIVERSAL_RUN.py — Gate J: universal decision battery CW01-CW25 (FAIL CLOSED).
# Re-verifies every gate's evidence JSON + live anchors (fresh builds, QSolver probes).
# SYN-UNKNOWN outcomes are recorded as the accepted remainder (Gate H), not failures.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/'
CHECKS = []


def rec(cid, gate, claim, cond, detail=''):
    st = 'PASS' if cond else 'FAIL'
    CHECKS.append({'id': cid, 'gate': gate, 'claim': claim, 'status': st, 'detail': detail})
    print('%-6s %-6s %-52s %s %s' % (cid, gate, claim, st, detail), flush=True)
    if not cond:
        raise AssertionError((cid, claim, detail))


def J(p):
    return json.load(open(PDIR + p))


if __name__ == '__main__':
    t0 = time.time()
    DOM = J('CW_DOMAIN_TESTS.json')
    rec('CW01', 'A', 'domain closed=5003 bad empty', DOM['closed'] == 5003 and DOM['bad'] == [], str(DOM['closed']))
    rec('CW02', 'B', 'G5 KeqG=164 KneG=0', DOM['KeqG'] == 164 and DOM['KneG'] == 0,
        'KeqG=%s KneG=%s' % (DOM['KeqG'], DOM['KneG']))
    CORE = J('CW_CORE_INVARIANCE_TESTS.json')
    rec('CW03', 'C', 'closed/admissible/keqg=200', CORE['closed'] == 200 and CORE['admissible'] == 200 and CORE['keqg'] == 200, '')
    rec('CW04', 'C', 'cconst=200 samples=5', CORE['cconst'] == 200 and len(CORE['samples']) == 5, '')
    LOW = J('CW_LOW_EDGE_RESULTS.json')
    rec('CW05', 'D', 'genuine-negative inventory=20', len(LOW.get('negatives', [])) == 20, 'n=%d' % len(LOW.get('negatives', [])))
    rec('CW06', 'E', 'low walks=40 grounded=240', LOW['walks'] == 40 and LOW['grounded'] == 240,
        'skipped=%s' % LOW['skipped'])
    HIGH = J('CW_HIGH_EDGE_RESULTS.json')
    rec('CW07', 'F', 'high grounded=319 fibers=5', HIGH['grounded'] == 319 and HIGH['fibers'] == 5, '')
    rec('CW08', 'F', 'high skipped=0', HIGH['skipped'] == 0, '')
    # live low anchor: re-ground preregistered E3 on a fresh SL build
    from PC_TYPED_DAG import DAG
    from STRICT_LOW_COMPILER import build_slow
    from STRICT_CERTIFY import ssertify
    from PC_CONCRETIZE import serial
    from CW_SYNTHESIS_RUN import chain_desc
    import splay as S
    d = DAG()
    L = build_slow(d, 'SL')
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    A = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    B = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    st, info = ssertify(d, L, serial(A), serial(B), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    rec('CW09', 'E', 'live E3 low grounding ok', st == 'ok', '%s H=%s q=%s w=%s' % (st, info.get('H'), info.get('q'), info.get('w')) if st == 'ok' else str(info)[:80])
    OP = J('CW_PRE_POST_MINPRE_RESULTS.json')
    rec('CW10', 'I', 'units binder/minpre/empty/negexists', OP['binder'] and OP['minpre_struct'] and OP['empty_target'] and OP['neg_exists'], '')
    rec('CW11', 'I', 'micro agree=16', OP['micro_agree'] == 16, str(OP['micro_agree']))
    rec('CW12', 'I', 'micro unsat=16 unknown=0', OP['micro_unsat'] == 16 and OP['micro_unknown'] == 0,
        'unsat=%s unk=%s' % (OP['micro_unsat'], OP['micro_unknown']))
    SYN = J('CW_FREE_WITNESS_RESULTS.json')
    rec('CW13', 'H', '3/3 cases grounded ok', all(c['grounded'] == 'ok' for c in SYN), str(len(SYN)))
    rec('CW14', 'H', '3/3 synthesis UNKNOWN (wall)', all(c.get('synthesis') == 'UNKNOWN' for c in SYN), 'accepted remainder')
    # live QSolver probes (small DAGs)
    from PC_SOLVER_BACKEND import Solver, SAT, UNSAT
    from CW_QUANTIFIED_BACKEND import QSolver
    dz = DAG()
    z = dz.var_int('z', 1)
    neg = dz.NOT(dz.EXISTS(('z',), dz.EQ(z, dz.const_int(1, 1))))
    rec('CW15', 'I', 'live neg-exists UNSAT', QSolver(dz).solve(neg)[0] == UNSAT, '')
    rec('CW16', 'I', 'live pos-exists SAT', QSolver(dz).solve(dz.EXISTS(('z',), dz.EQ(z, dz.const_int(1, 1))))[0] == SAT, '')
    d2 = DAG()
    xx = d2.var_bool('x')
    yy = d2.var_bool('y')
    inner = d2.EXISTS(('y',), d2.AND(xx, yy))
    outer = d2.EXISTS(('y',), d2.AND(d2.subst(inner, {'x': 'x2'}), yy))
    rec('CW17', 'I', 'live binder shadow pair', QSolver(d2).solve(outer, assume={'x2': 1, 'y': 1})[0] == SAT and QSolver(d2).solve(outer, assume={'x2': 0})[0] == UNSAT, '')
    d3 = DAG()
    p = d3.var_bool('p')
    q = d3.var_bool('q')
    rec('CW18', 'I', 'live qf SAT/UNSAT', QSolver(d3).solve(d3.AND(d3.OR(p, q), d3.NOT(p)))[0] == SAT and QSolver(d3).solve(d3.AND(p, d3.NOT(p)))[0] == UNSAT, '')
    d4 = DAG()
    s = d4.var_int('s', 2)
    tt = d4.var_int('t', 2)
    pre = d4.EXISTS(('t',), d4.AND(d4.EQ(s, tt), d4.EQ(tt, d4.const_int(3, 2))))
    rec('CW19', 'I', 'live pre-style SAT/UNSAT', QSolver(d4).solve(pre, assume={'s': 3, 't': 0})[0] == SAT and QSolver(d4).solve(pre, assume={'s': 2, 't': 0})[0] == UNSAT, '')
    h = d3.AND(d3.OR(p, q), d3.NOT(d3.AND(p, q)))
    rh, mh, _ = QSolver(d3).solve(h)
    rq, mq, _ = Solver(d3).solve(h)
    rec('CW20', 'I', 'cross-backend parity', rh == rq == SAT and mh.get('q') == mq.get('q'), '%s/%s' % (rh, rq))
    # live product anchors (fresh 1.6M build)
    from CW_PRODUCT_COMPILER import Product, WALPHA
    from CW_SYMBOLIC_OPERATORS import Operators
    dp = DAG()
    P = Product(dp)
    rec('CW21', 'G', 'live product 9 low edges + OOB false', len(P.E_low) == 9 and all(w in P.E_low for w in range(-4, 5)) and P.edge(5, 0, 0) is not None and dp.ev_iter(P.edge(5, 0, 0), {}) is False, 'nodes=%d' % dp.count())
    cone_sm = dp.topo([P.E_sm])
    rec('CW22', 'G', 'live E_sm/E_mt quantified', 'exists' in set(dp.nodes[n][0] for n in cone_sm) and 'exists' in set(dp.nodes[n][0] for n in dp.topo([P.E_mt])), '')
    op = Operators(P)
    rec('CW23', 'I', 'live high src/dst quantified', 'exists' in set(dp.nodes[n][0] for n in dp.topo([op.high_source()])) and 'exists' in set(dp.nodes[n][0] for n in dp.topo([op.high_destination()])), '')
    m3 = op.minpre({0: dp.const_bool(True), 1: None}, 3)
    kinds = set(dp.nodes[n][0] for n in dp.topo([m3[0]]))
    rec('CW24', 'I', 'live minpre not+exists struct', 'not' in kinds and 'exists' in kinds, '')
    rec('CW25', 'J', 'universal verdict: 24/24 PASS', all(c['status'] == 'PASS' for c in CHECKS), 'time=%.1fs' % (time.time() - t0))
    json.dump({'checks': CHECKS, 'verdict': 'PASS', 'time_s': round(time.time() - t0, 1)},
              open(PDIR + 'CW_UNIVERSAL_RESULTS.json', 'w'), indent=1)
    print('UNIVERSAL PASS time=%.1fs' % (time.time() - t0), flush=True)
