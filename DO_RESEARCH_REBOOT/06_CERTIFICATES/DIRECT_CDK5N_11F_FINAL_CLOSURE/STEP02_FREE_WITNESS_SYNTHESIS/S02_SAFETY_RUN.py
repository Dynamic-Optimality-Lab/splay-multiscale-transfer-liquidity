# S02_SAFETY_RUN.py — Gate B hazard confirmation + repair verification (FAIL CLOSED).
import sys, json
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/'
RES = []
FAIL = []


def rec(name, ok, detail=''):
    RES.append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


from PC_TYPED_DAG import DAG
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S01_INDEPENDENT_ORACLE import scoped_truth
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile

if __name__ == '__main__':
    # ---- B1: confirm hazard on Step-01 compiler ----
    d = DAG()
    x = d.var_int('x', 1)
    f1 = d.EXISTS(('x',), d.EQ(x, d.const_int(3, 2)))
    ps0 = ProductionSolver(d, timeout_ms=30000)
    r_old = ps0.solve(ps0.compile(f1, 'old'), {})
    o1 = scoped_truth(d, f1, {})
    rec('B1 hazard confirmed (old SAT vs oracle False)', r_old['status'] == SAT and o1 == ('b', False),
        '%s vs %s' % (r_old['status'], o1))
    from S01_SCOPED_BINDERS import forall as FA
    f2 = FA(d, ('x',), d.LE(x, d.const_int(1, 1)))
    r_old2 = ps0.solve(ps0.compile(f2, 'old2'), {})
    o2 = scoped_truth(d, f2, {})
    rec('B1 forall hazard confirmed (old UNSAT vs oracle True)', r_old2['status'] == UNSAT and o2 == ('b', True),
        '%s vs %s' % (r_old2['status'], o2))
    # ---- B1: repair ----
    ps = ProductionSolver(d, timeout_ms=30000)
    install_scoped_compile(ps)
    r1 = ps.solve(ps.compile(f1, 'new'), {})
    rec('B1 exists-bounded UNSAT', r1['status'] == UNSAT and o1 == ('b', False), r1['status'])
    r2 = ps.solve(ps.compile(f2, 'new2'), {})
    rec('B1 forall-bounded SAT', r2['status'] == SAT and o2 == ('b', True), r2['status'])
    # nested mixed scopes vs oracle
    y = d.var_int('y', 1)
    f3 = FA(d, ('x',), d.EXISTS(('y',), d.EQ(x, y)))
    r3 = ps.solve(ps.compile(f3, 'new3'), {})
    o3 = scoped_truth(d, f3, {})
    rec('B1 nested forall-exists SAT', r3['status'] == SAT and o3 == ('b', True), '%s %s' % (r3['status'], o3))
    f4 = d.EXISTS(('x',), FA(d, ('y',), d.EQ(x, y)))
    r4 = ps.solve(ps.compile(f4, 'new4'), {})
    o4 = scoped_truth(d, f4, {})
    rec('B1 nested exists-forall UNSAT', r4['status'] == UNSAT and o4 == ('b', False), '%s %s' % (r4['status'], o4))
    # ---- Step-01 regression re-runs under patch (must be unchanged) ----
    dq = DAG()
    z = dq.var_int('z', 1)
    psq = ProductionSolver(dq, timeout_ms=30000)
    install_scoped_compile(psq)
    q1 = dq.NOT(dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    rec('B1 patch Q1 still UNSAT', psq.solve(psq.compile(q1, 'pq1'), {})['status'] == UNSAT, '')
    q2 = dq.AND(dq.EQ(z, dq.const_int(0, 1)), dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    hq2 = psq.compile(q2, 'pq2')
    rr2 = psq.solve(hq2, {})
    rec('B1 patch Q2 still SAT z=0', rr2['status'] == SAT and psq.extract_model(hq2, rr2).get('z') == 0, '')
    # ---- B2: session-aware Tier-1 ----
    ds = DAG()
    yy = ds.var_int('yy', 2)
    F = ds.OR(ds.EQ(yy, ds.const_int(1, 2)), ds.NOT(ds.EQ(yy, ds.const_int(1, 2))))
    pss = ProductionSolver(ds, timeout_ms=30000)
    install_scoped_compile(pss)
    hs = pss.compile(F, 'sess')
    hs['_session_stack'].append({'yy': 3})
    rs = pss.solve(hs, {})
    ms = pss.extract_model(hs, rs) if rs['status'] == SAT else {}
    rec('B2 session-aware completion respects session', rs['status'] == SAT and ms.get('yy') == 3, '%s %s' % (rs['status'], ms))
    hs['_session_stack'].append({'yy': 2})
    rs2 = pss.solve(hs, {})
    rec('B2 session-session contradiction UNSAT', rs2['status'] == UNSAT and 'session-contradiction' in rs2.get('reason', ''), rs2.get('reason', ''))
    hs['_session_stack'] = [{'yy': 1}]
    rs3 = pss.solve(hs, {'yy': 2})
    rec('B2 session-call contradiction UNSAT', rs3['status'] == UNSAT and 'session-call-contradiction' in rs3.get('reason', ''), rs3.get('reason', ''))
    json.dump(RES, open(PDIR + 'S02_SEMANTIC_SAFETY_RESULTS.json', 'w'), indent=1)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('SAFETY PASS')
