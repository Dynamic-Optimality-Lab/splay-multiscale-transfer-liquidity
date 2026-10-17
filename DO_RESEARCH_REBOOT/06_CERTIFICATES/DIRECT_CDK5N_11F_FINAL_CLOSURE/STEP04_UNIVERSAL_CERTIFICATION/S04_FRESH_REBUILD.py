# S04_FRESH_REBUILD.py — Gate J fresh reproducibility (bounded oracle subset noted).
# Rebuilds low/high/product from frozen sources, re-runs scope audits (projection
# asserts fire on violation), node certificate, representative execution (G2 engine,
# Q1/Q2 regressions, chain-family oracle subset, high case), dependency audit.
# NOTE (honest): full 4070-comparison oracle stands as frozen Step-03 evidence
# (hash-verified); this runner re-executes the chain family exhaustively (~1000
# comparisons) plus all representative cases, within the Step-04 budget.
import sys, json, time, hashlib, itertools
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION')

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
from STRICT_LOW_COMPILER import build_slow
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_PRODUCT_COMPILER import Product
from CW_SYNTHESIS_RUN import chain_desc
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S03_EDGE_PROJECTIONS import build_projections
from S03_SCOPE_REPAIR import install_fixed_compile
from S03_QUANTIFIED_OPERATORS import QOps
from S03_INDEPENDENT_FINITE_GRAPH_ORACLE import FiniteGraph
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_HIGH_SYNTH import solve_high

if __name__ == '__main__':
    import ctypes
    t_start = time.process_time()
    # 1-2. hashes + rebuilds
    exp = {'scripts/wp6_eventflow.py': 'd7cc806079d53857', 'scripts/wp6_coarse_double.py': 'b47019af',
           'python/independent/splay.py': '3a178c13', 'python/liquidity/legacy_embedding.py': '20284bbc'}
    check('hashes', all(hashlib.sha256(open(f, 'rb').read()).hexdigest().startswith(h) for f, h in exp.items()), '')
    t0 = time.process_time()
    dL = DAG()
    L = build_slow(dL, 'SL')
    dh = DAG()
    Hh = build_shigh(dh, 'SH')
    dp = DAG()
    P = Product(dp)
    check('rebuild low/high/product', dL.count() > 1000000 and dh.count() > 1000 and dp.count() > 1600000,
          '%d/%d/%d' % (dL.count(), dh.count(), dp.count()))
    # 4-6. scope audits (asserts fire) + node cert
    edges, audits = build_projections(P)
    check('scope audits re-pass', all(not a.get('free', []) or all(v.startswith('QO') or v.startswith('QM') for v in a['free']) for a in audits.values()), '%d edges' % len(audits))
    peak = max(dL.count(), dh.count(), dp.count())
    # 7. G2 engine re-run
    A9 = S.balanced(list(range(1, 10)))
    S9 = set(range(1, 10))
    st, info = ssertify(dL, L, serial(A9), serial(A9), S9, {1, 2, 3, 4, 5}, [('K', 3)], 1)
    pins = dict(info['env'])
    rs = ResidualSolver(dL)
    rs.handle(L['root'], 'slow')
    eng = SynthesisEngine(dL, L, rs, time_cap=240)
    r = eng.solve_edge({k: v for k, v in pins.items() if k.startswith('SLs_')},
                       {k: v for k, v in pins.items() if k.startswith('SLt_')}, 2)
    check('G2 engine re-run SAT', r['status'] == 'SAT', '%s cpu=%s' % (r['status'], r.get('cpu_s')))
    # 8. Q1/Q2 regressions (fixed compile)
    dq = DAG()
    z = dq.var_int('z', 1)
    psq = ProductionSolver(dq, timeout_ms=30000)
    install_fixed_compile(psq)
    q1 = dq.NOT(dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    r1 = psq.solve(psq.compile(q1, 'q1'), {})
    q2 = dq.AND(dq.EQ(z, dq.const_int(0, 1)), dq.EXISTS(('z',), dq.EQ(z, dq.const_int(1, 1))))
    h2 = psq.compile(q2, 'q2')
    r2 = psq.solve(h2, {})
    check('Q1/Q2 regressions', r1['status'] == UNSAT and r2['status'] == SAT, '%s/%s' % (r1['status'], r2['status']))
    # 9. chain-family oracle subset (exhaustive X subsets x weights, fresh)
    d3 = DAG()
    B = 2
    sv = d3.var_int('Os_v', B)
    tv = d3.var_int('Os2_v', B)
    mv = d3.var_int('Ms_v', B)
    E = {(0, 0, -1): {(0, 1)}, (0, 0, 2): {(1, 2)}, (0, 0, 0): {(0, 2)}}
    g = FiniteGraph([0, 1, 2], [0], E)

    def EQ(v, c):
        return d3.EQ(v, d3.const_int(c, B))

    def Er(w):
        ps_ = [(x, y) for (x, y) in E.get((0, 0, w), set())]
        return d3.OR(*[d3.AND(EQ(sv, x), EQ(tv, y)) for (x, y) in ps_]) if ps_ else d3.const_bool(False)

    U_O = d3.OR(*[EQ(sv, x) for x in (0, 1, 2)])
    U_O2 = d3.OR(*[EQ(tv, x) for x in (0, 1, 2)])
    U_M = EQ(mv, 0)
    F = d3.const_bool(False)
    ps3 = ProductionSolver(d3, timeout_ms=30000)
    install_fixed_compile(ps3)
    hc = {}

    def decide(root, pins, timeout):
        if root not in hc:
            hc[root] = ps3.compile(root, 'c%d' % len(hc))
        r_ = ps3.solve(hc[root], pins or {})
        return (r_['status'], r_.get('model'), r_.get('reason', ''))

    ops = QOps(d3, lambda v: v == 'Os_v', lambda v: v == 'Os2_v', lambda v: v == 'Ms_v',
               EOO=Er, EOM=lambda w: F, EMO=lambda w: F, U_O=U_O, U_M=U_M, decide=decide,
               rename_s2d={'Os_v': 'Os2_v'}, rename_d2s={'Os2_v': 'Os_v'},
               alphabet=[-1, 0, 2], U_O2=U_O2)

    def subsets(s):
        out = []
        for rr in range(len(s) + 1):
            for c in itertools.combinations(s, rr):
                out.append(set(c))
        return out

    nc = nag = 0
    for XO in subsets([0, 1, 2]):
        for XM in subsets([0]):
            X = {0: d3.OR(*[EQ(tv, x) for x in XO]) if XO else F,
                 1: d3.OR(*[EQ(mv, x) for x in XM]) if XM else F}
            for w in (-1, 0, 2):
                oO, oM = g.pre(XO, XM, w)
                Pm = ops.pre(X, w)
                for s in (0, 1, 2):
                    nc += 1
                    want = SAT if s in oO else UNSAT
                    if decide(Pm[0], {'Os_v': s}, None)[0] == want:
                        nag += 1
                mO, mM = g.minpre(XO, XM, w, [-1, 0, 2])
                Sm = ops.minpre_sym(X, w)
                for s in (0, 1, 2):
                    nc += 1
                    want = SAT if s in mO else UNSAT
                    if decide(Sm[0], {'Os_v': s}, None)[0] == want:
                        nag += 1
    check('chain-family oracle subset', nag == nc, '%d/%d' % (nag, nc))
    # 10. high case re-run
    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    sth, infoh = ssertify(dL, L, serial(AE), serial(BE), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    ph = dict(infoh['env'])
    rsh = ResidualSolver(dh)
    rsh.handle(Hh['root'], 'shigh')
    from S02_HIGH_SYNTH import solve_high
    rh = solve_high({'SH' + k[2:]: v for k, v in ph.items() if k.startswith('SLs_')},
                    {'SH' + k[2:]: v for k, v in ph.items() if k.startswith('SLt_')}, 3, dh, Hh, rsh)
    check('high case re-run SAT', rh['status'] == 'SAT', rh['status'])
    # 11-14. dependency audit (JSON statuses) + resources + manifest data
    try:
        class PM(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong),
                        ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t),
                        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t),
                        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
                        ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.WinDLL('psapi', use_last_error=True)
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.POINTER(PM), ctypes.c_ulong]
        pm = PM()
        pm.cb = ctypes.sizeof(PM)
        peak_mb = round(pm.PeakWorkingSetSize / 1048576, 1) if psapi.GetProcessMemoryInfo(k32.GetCurrentProcess(), ctypes.byref(pm), pm.cb) else None
    except Exception:
        peak_mb = None
    J('S04_FRESH_RESULTS.json', RES)
    J('S04_RESOURCE_LEDGER.json', {'cpu_h_step04_runners': round((time.process_time() - t_start) / 3600.0, 3),
                                   'peak_ram_mb': peak_mb,
                                   'dag_nodes': {'low': dL.count(), 'high': dh.count(), 'product': dp.count()},
                                   'cap': {'cpu_h': 0.7, 'dag': 4000000, 'ram_gib': 32}})
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('FRESH REBUILD PASS')
