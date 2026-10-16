# S01_PRODUCTION_SMOKE.py — Step 01 production smoke + regressions + adversarial (FAIL CLOSED
# with evidence persisted even on failure). Writes all S01_* execution JSONs.
import sys, json, time, itertools, ctypes
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER/'
RES = {}
FAIL = []


def rec(section, name, ok, detail=''):
    RES.setdefault(section, []).append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'detail': detail})
    print('%-10s %-46s %s %s' % (section, name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append((section, name, detail))


def proc_peak_mb():
    try:
        class PM(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                        ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
        pm = PM()
        pm.cb = ctypes.sizeof(PM)
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        h = k32.GetCurrentProcess()
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PM), ctypes.c_ulong]
        if psapi.GetProcessMemoryInfo(h, ctypes.byref(pm), pm.cb):
            return round(pm.PeakWorkingSetSize / 1048576, 1)
    except Exception:
        pass
    return None


import splay as S
from PC_TYPED_DAG import DAG, BOOL
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S01_INCREMENTAL_ENGINE import IncrementalEngine
from S01_INDEPENDENT_ORACLE import scoped_truth, witness_check
from S01_MODEL_EXTRACTION import extract_and_verify
from S01_SCOPED_BINDERS import forall as FA, normalize, cone_subst

T_CPU = {'build': 0.0, 'compile': 0.0, 'solve': 0.0}


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


if __name__ == '__main__':
    # ---------- S1: full product build + compile ----------
    from CW_PRODUCT_COMPILER import Product, WALPHA
    t0 = time.process_time()
    d = DAG()
    P = Product(d)
    T_CPU['build'] += time.process_time() - t0
    prod_nodes = d.count()
    print('product nodes=%d build_cpu=%.1fs' % (prod_nodes, T_CPU['build']), flush=True)
    eng = IncrementalEngine(d, seed=17, timeout_ms=120000)
    metrics = {'product_nodes': prod_nodes, 'handles': {}}
    t0 = time.process_time()
    h_low = eng.compile_once(P.low['root'], 'low')
    h_high = eng.compile_once(P.high['root'], 'high')
    h_sm = eng.compile_once(P.E_sm, 'Esm')
    h_mt = eng.compile_once(P.E_mt, 'Emt')
    h_e1 = eng.compile_once(P.E_low[-1], 'Elow-1')
    T_CPU['compile'] += time.process_time() - t0
    for tag, h in (('low', h_low), ('high', h_high), ('Esm', h_sm), ('Emt', h_mt), ('Elow-1', h_e1)):
        st = h['comp']['stats']
        metrics['handles'][tag] = {'decls': st['decls'], 'int_bounds': st['int_bounds'],
                                   'exists': st['exists'], 'forall': st['forall'],
                                   'qdepth': st['qdepth'], 'dag_cone': st['dag_nodes'],
                                   'translate_s': st['translate_s'],
                                   'norm_binders': h['ninfo']['count'],
                                   'norm_growth': h['ninfo']['growth'],
                                   'compile_cpu_s': h['compile_cpu_s'],
                                   'free': len(h['free']), 'bound': len(h['bound'])}
    metrics['peak_ram_mb'] = proc_peak_mb()
    J('S01_FULL_PRODUCT_BUILD.json', metrics)
    rec('S1', 'product builds 1.6M', prod_nodes >= 1600000, str(prod_nodes))
    rec('S1', 'low/high/Esm/Emt/Elow compile', all(k in metrics['handles'] for k in ('low', 'high', 'Esm', 'Emt', 'Elow-1')), str({k: v['decls'] for k, v in metrics['handles'].items()}))
    # sharing preserved: cone nodes vs distinct (topo dedups by construction); report
    # hash-cons reuse factor = total parent-links / distinct cone nodes on low root
    cone = d.topo([P.low['root']])
    links = sum(len(d.nodes[n][2]) for n in cone)
    metrics['sharing'] = {'cone_nodes': len(cone), 'parent_links': links, 'reuse_factor': round(links / max(1, len(cone)), 3)}
    J('S01_FULL_PRODUCT_BUILD.json', metrics)

    # ---------- Q1-Q8 quantifier regressions (compiled backend, no hardcoding) ----------
    QR = []
    dq = DAG()
    z = dq.var_int('z', 1)
    psq = ProductionSolver(dq)
    q1 = dq.NOT(dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    r1 = psq.solve(psq.compile(q1, 'q1'), {})
    QR.append(('Q1 neg-exists UNSAT', r1['status'] == UNSAT and scoped_truth(dq, q1, {}) == ('b', False)))
    q2 = dq.AND(dq.EQ(z, dq.const_int(0, 1)), dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    hq2 = psq.compile(q2, 'q2')
    r2 = psq.solve(hq2, {})
    m2 = psq.extract_model(hq2, r2) if r2['status'] == SAT else {}
    QR.append(('Q2 collision SAT z=0', r2['status'] == SAT and m2.get('z') == 0 and scoped_truth(dq, q2, {'z': 0}) == ('b', True)))
    d3 = DAG()
    a = d3.var_int('a', 1)
    q3 = d3.EXISTS(('a',), d3.AND(d3.EQ(a, d3.const_int(1, 1)), d3.EXISTS(('a',), d3.EQ(a, d3.const_int(0, 1)))))
    ps3 = ProductionSolver(d3)
    r3 = ps3.solve(ps3.compile(q3, 'q3'), {})
    QR.append(('Q3 shadowed SAT', r3['status'] == SAT and scoped_truth(d3, q3, {}) == ('b', True)))
    d4 = DAG()
    x = d4.var_bool('x')
    y = d4.var_bool('y')
    ps4 = ProductionSolver(d4)
    q4 = d4.EXISTS(('x',), FA(d4, ('y',), d4.EQ(x, y)))
    r4 = ps4.solve(ps4.compile(q4, 'q4'), {})
    QR.append(('Q4 exists-forall UNSAT', r4['status'] == UNSAT and scoped_truth(d4, q4, {}) == ('b', False)))
    q5 = FA(d4, ('y',), d4.EXISTS(('x',), d4.EQ(x, y)))
    r5 = ps4.solve(ps4.compile(q5, 'q5'), {})
    QR.append(('Q5 forall-exists SAT', r5['status'] == SAT and scoped_truth(d4, q5, {}) == ('b', True)))
    # Q6: two-weight MinPre exclusion on a hand-built finite graph
    d6 = DAG()
    s = d6.var_int('s', 2)
    tt = d6.var_int('t', 2)
    E0 = d6.AND(d6.EQ(s, d6.const_int(0, 2)), d6.EQ(tt, d6.const_int(0, 2)))
    E1 = d6.AND(d6.EQ(s, d6.const_int(0, 2)), d6.EQ(tt, d6.const_int(0, 2)))
    X = d6.EQ(tt, d6.const_int(0, 2))
    pre0 = d6.EXISTS(('t',), d6.AND(E0, X))
    pre1 = d6.EXISTS(('t',), d6.AND(E1, X))
    minpre1 = d6.AND(pre1, d6.NOT(pre0))
    ps6 = ProductionSolver(d6)
    hm = ps6.compile(minpre1, 'minpre1')
    r6 = ps6.solve(hm, {'s': 0})
    o6 = scoped_truth(d6, minpre1, {'s': 0})
    QR.append(('Q6 MinPre1 exclusion UNSAT', r6['status'] == UNSAT and o6 == ('b', False)))
    # Q6 positive control: MinPre0 contains s=0 (no weight<0 edge)
    preN = d6.const_bool(False)
    minpre0 = d6.AND(pre0, d6.NOT(preN))
    r6b = ps6.solve(ps6.compile(minpre0, 'minpre0'), {'s': 0})
    QR.append(('Q6 control MinPre0 SAT', r6b['status'] == SAT and scoped_truth(d6, minpre0, {'s': 0}) == ('b', True)))
    # Q7 vacuous
    d7 = DAG()
    p = d7.var_bool('p')
    ps7 = ProductionSolver(d7)
    q7 = d7.AND(p, d7.EXISTS(('zz9',), p))
    r7 = ps7.solve(ps7.compile(q7, 'q7'), {})
    QR.append(('Q7 vacuous identity', r7['status'] == SAT and scoped_truth(d7, q7, {'p': True}) == ('b', True)))
    # Q8 alpha-renaming: rename free z->z2 in Q2-shape, verdicts + oracle must match
    da = DAG()
    za = da.var_int('za', 1)
    qa = da.AND(da.EQ(za, da.const_int(0, 1)), da.EXISTS(('za',), da.EQ(za, da.const_int(1, 1))))
    psa = ProductionSolver(da)
    ha = psa.compile(qa, 'qa')
    ra = psa.solve(ha, {})
    ma = psa.extract_model(ha, ra) if ra['status'] == SAT else {}
    QR.append(('Q8 alpha-equivalence', ra['status'] == r2['status'] and ma.get('za') == 0 and scoped_truth(da, qa, {'za': 0}) == ('b', True)))
    for name, ok in QR:
        rec('Q', name, ok)
    J('S01_QUANTIFIER_REGRESSIONS.json', [{'name': n, 'pass': bool(o)} for n, o in QR])

    # ---------- arithmetic regressions + exhaustive small-domain operator agreement ----------
    AR = []
    dar = DAG()
    psar = ProductionSolver(dar, timeout_ms=30000)
    # overflow attempt must stay false under exact semantics
    big = dar.var_int('v', 32)
    ov = dar.EQ(dar.ADD(big, dar.const_int(1, 32), 33), dar.const_int(0, 32))
    rov = psar.solve(psar.compile(dar.AND(ov, dar.EQ(big, dar.const_int((1 << 32) - 1, 32))), 'ov'), {})
    AR.append(('add-overflow-attempt UNSAT', rov['status'] == UNSAT))
    # signed weight comparisons
    w = dar.var_int('w', 5, True)
    rlt = psar.solve(psar.compile(dar.AND(dar.LT(w, dar.const_int(0, 5, True)), dar.EQ(w, dar.const_int(-4, 5, True))), 'slt'), {})
    AR.append(('signed LT -4<0 SAT', rlt['status'] == SAT))
    rle = psar.solve(psar.compile(dar.LE(dar.const_int(-3, 5, True), w), 'sle'), {'w': -4})
    AR.append(('signed LE -3<=-4 UNSAT', rle['status'] == UNSAT))
    rsub = psar.solve(psar.compile(dar.EQ(dar.SUB(dar.const_int(6, 4), dar.const_int(9, 4), 5), dar.const_int(-3, 5, True)), 'ssub'), {})
    AR.append(('sub 6-9==-3 SAT', rsub['status'] == SAT))
    # exhaustive agreement: ops x {bool,2-bit} x all assignments, oracle vs compiled
    ex = DAG()
    b1 = ex.var_bool('b1')
    b2 = ex.var_bool('b2')
    i1 = ex.var_int('i1', 2)
    i2 = ex.var_int('i2', 2)
    c0 = ex.const_int(0, 2)
    c3 = ex.const_int(3, 2)
    formulas = {
        'and': ex.AND(b1, b2), 'or': ex.OR(b1, b2), 'xor': ex.XOR(b1, b2),
        'not1': ex.NOT(b1), 'eqB': ex.EQ(b1, b2), 'eqI': ex.EQ(i1, i2),
        'lt': ex.LT(i1, i2), 'le': ex.LE(i1, i2),
        'add0': ex.EQ(ex.ADD(i1, i2, 3), c3), 'sub0': ex.EQ(ex.SUB(i1, c0, 3), i1),
        'iteT': ex.EQ(ex.ITE(b1, i1, i2), i1), 'iteF': ex.EQ(ex.ITE(b1, i1, i2), i2),
    }
    pex = ProductionSolver(ex, timeout_ms=30000)
    nagree = ntot = 0
    for fname, F in formulas.items():
        hx = pex.compile(F, 'ex_' + fname)
        vnames = sorted(ex.vars_in(F))
        pools = []
        for v in vnames:
            nn = ex.vars[v]
            if ex.nodes[nn][1] == BOOL:
                pools.append([False, True])
            else:
                pools.append([0, 1, 2, 3])
        for combo in itertools.product(*pools):
            env = dict(zip(vnames, combo))
            o = scoped_truth(ex, F, env)
            assert o[0] == 'b' and o[1] is not None, (fname, env, o)
            rr = pex.solve(hx, {k: (bool(v) if isinstance(v, bool) else v) for k, v in env.items()})
            want = SAT if o[1] is True else UNSAT
            ntot += 1
            if rr['status'] == want:
                nagree += 1
            else:
                FAIL.append(('AR-exhaustive', fname, (env, o, rr['status'])))
    AR.append(('exhaustive op agreement %d/%d' % (nagree, ntot), nagree == ntot))
    # adversarial extras (small, compiled backend, oracle cross-checked)
    dad = DAG()
    psad = ProductionSolver(dad, timeout_ms=30000)
    pa = dad.var_bool('pa')
    rcf = psad.solve(psad.compile(dad.AND(pa, dad.NOT(pa)), 'cf'), {})
    AR.append(('const-false UNSAT', rcf['status'] == UNSAT and scoped_truth(dad, dad.AND(pa, dad.NOT(pa)), {'pa': True}) == ('b', False)))
    rne = psad.solve(psad.compile(dad.const_bool(False), 'ne'), {})
    AR.append(('nonexistent-target (False root) UNSAT', rne['status'] == UNSAT))
    # canonical renaming roundtrip: F over QO vars vs QO2-renamed copy
    dcn = DAG()
    so = dcn.var_int('QO_sg0', 9)
    to = dcn.var_int('QO2_sg0', 9)
    F = dcn.AND(dcn.EQ(so, dcn.const_int(7, 9)), dcn.EXISTS(('QO2_sg0',), dcn.EQ(to, so)))
    G = dcn.subst(F, {'QO_sg0': 'QO2_sg0'})
    pscn = ProductionSolver(dcn, timeout_ms=30000)
    rF = pscn.solve(pscn.compile(F, 'cnF'), {'QO_sg0': 7})
    rG = pscn.solve(pscn.compile(G, 'cnG'), {'QO2_sg0': 7})
    AR.append(('canonical rename verdict-stable', rF['status'] == rG['status'] == SAT and scoped_truth(dcn, F, {'QO_sg0': 7}) == ('b', True)))
    # ordinary/midpoint capture analogue: outer binder over names incl. inner-bound ones
    ddb = DAG()
    u = ddb.var_int('u', 2)
    v = ddb.var_int('v', 2)
    shared = ddb.EQ(v, u)
    innerb = ddb.EXISTS(('v',), shared)
    outerb = ddb.EXISTS(('v',), ddb.AND(innerb, ddb.EQ(v, ddb.const_int(1, 2))))
    psdb = ProductionSolver(ddb, timeout_ms=30000)
    rdb = psdb.solve(psdb.compile(outerb, 'db'), {'u': 1})
    odb = scoped_truth(ddb, outerb, {'u': 1})
    AR.append(('double-bind capture SAT agrees', rdb['status'] == SAT and odb == ('b', True)))
    rdb2 = psdb.solve(psdb.compile(outerb, 'db2'), {'u': 0})
    odb2 = scoped_truth(ddb, outerb, {'u': 0})
    # lexical: outer v indep. of inner: EXISTS v_outer ( (EXISTS v_inner v_inner==u) AND v_outer==1 )
    # with u=0: inner SAT (v_inner=0), outer SAT (v_outer=1) => SAT
    AR.append(('double-bind capture u=0 agrees', rdb2['status'] == (SAT if odb2 == ('b', True) else UNSAT) and odb2 == ('b', True)))
    # invalid B-core: popcount(mu)==5 with 4-bits-set mu
    from PC_LOW_COMPILER import popcount5
    dpc = DAG()
    mu = dpc.var_int('mu', 9)
    pspc = ProductionSolver(dpc, timeout_ms=30000)
    rpc = pspc.solve(pspc.compile(dpc.EQ(popcount5(dpc, mu), dpc.const_int(5, 4)), 'pc'), {'mu': 15})
    AR.append(('invalid B-core popcount rejected', rpc['status'] == UNSAT and scoped_truth(dpc, dpc.EQ(popcount5(dpc, mu), dpc.const_int(5, 4)), {'mu': 15}) == ('b', False)))
    rpc2 = pspc.solve(pspc.compile(dpc.EQ(popcount5(dpc, mu), dpc.const_int(5, 4)), 'pc2'), {'mu': 31})
    AR.append(('valid B-core popcount SAT', rpc2['status'] == SAT))
    for name, ok in AR:
        rec('AR', name, ok if isinstance(ok, bool) else ok)
    J('S01_ARITHMETIC_REGRESSIONS.json', [{'name': n, 'pass': bool(o)} for n, o in AR])

    J('S01_PARTIAL.json', {'RES': RES, 'FAIL': FAIL})
    print('PART1 done cpu=%s peak=%s' % (T_CPU, proc_peak_mb()), flush=True)
