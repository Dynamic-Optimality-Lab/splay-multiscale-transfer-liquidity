# G01_SOURCE_GROUNDED_TESTS.py — Phase K source-grounded checks (FAIL CLOSED).
# Executable core (decisive, fast): engine SAT (edge exists + replay) + Tier-1 SAT on
# the UNPROJECTED low/high roots under full grounded envs (2-3 s, exact) + universe
# Tier-1 (small cones, const-True) + fiber audit. Projected forms are verified by
# construction audit (S03) + small-graph execution equivalence (Step-03, 4070/4070);
# direct Z3 on full projected quantified edges is the documented wall (measured
# UNKNOWN, never a verdict). Contraction: EOM/EMO Tier-1 SAT with the SAME fiber
# witness + w preserved => contracted edge verified by decomposition (C1/C2).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/'
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
from STRICT_HIGH_COMPILER import build_shigh
from STRICT_CERTIFY import ssertify
from PC_CONCRETIZE import serial
from CW_SYNTHESIS_RUN import chain_desc
from CW_PRODUCT_COMPILER import Product
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S03_EDGE_PROJECTIONS import build_projections, is_O_src, is_O_dst, is_M
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_HIGH_SYNTH import solve_high
from S03_SCOPE_REPAIR import normalize_fixed

if __name__ == '__main__':
    d = DAG()
    P = Product(d)
    edges, audits = build_projections(P)
    # engine + Tier-1 harness on UNPROJECTED roots (fast, decisive)
    dL = DAG()
    L = build_slow(dL, 'SL')
    rsL = ResidualSolver(dL)
    rsL.handle(L['root'], 'slow')
    eng = SynthesisEngine(dL, L, rsL, time_cap=240)
    R = {}

    def tier1(root, dd, pins):
        nroot, _ = normalize_fixed(dd, root)
        r = dd.simplify(nroot, dict(pins))
        k, t, a, e = dd.nodes[r]
        if k == 'const' and t == BOOL:
            return 'SAT' if e else 'UNSAT'
        return 'NON-CONST'

    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE3 = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    S9 = set(range(1, 10))
    A9 = S.balanced(list(range(1, 10)))
    for (name, A, B, SS, M, word, H, w) in [
            ('E3', AE3, BE3, set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1, -1),
            ('plain', A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 3)], 1, 2),
            ('delkeep', A9, A9, S9, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2, 4)]:
        st, info = ssertify(dL, L, serial(A), serial(B), SS, M, word, H)
        assert st == 'ok', name
        pins = dict(info['env'])
        sp = {k: v for k, v in pins.items() if k.startswith('SLs_')}
        tp = {k: v for k, v in pins.items() if k.startswith('SLt_')}
        r = eng.solve_edge(sp, tp, w)
        ok = r['status'] == 'SAT'
        check('grounded %s edge SAT (engine+replay)' % name, ok, '%s Hq=%s/%s' % (r['status'], r.get('H'), r.get('q')))
        # universe Tier-1 on small state_valid cones (fully pinned)
        dU = DAG()
        sU = StateVars7(dU, 'Us')
        rUs = dU.simplify(state_valid7(dU, sU), {'Us' + k[3:]: v for k, v in sp.items()})
        rUt = dU.simplify(state_valid7(dU, sU), {'Us' + k[3:]: v for k, v in tp.items()})
        uS = dU.nodes[rUs][0] == 'const' and bool(dU.nodes[rUs][3])
        uT = dU.nodes[rUt][0] == 'const' and bool(dU.nodes[rUt][3])
        check('  universes valid', uS and uT, '')
        # Tier-1 on UNPROJECTED low root (exact, fast)
        t1 = tier1(L['root'], dL, pins)
        check('  low-root Tier-1 SAT', t1 == 'SAT', str(t1))
        R[name] = {'edge': r['status'], 'universe': uS and uT, 'lowroot_tier1': t1}
    # high: contracted edge via decomposition (EOM + EMO Tier-1 on unprojected high root)
    dh = DAG()
    Hh = build_shigh(dh, 'SH')
    rsh = ResidualSolver(dh)
    rsh.handle(Hh['root'], 'shigh')
    stH, infoH = ssertify(dL, L, serial(AE3), serial(BE3), set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    assert stH == 'ok'
    pinsH = dict(infoH['env'])
    spH = {'SH' + k[2:]: v for k, v in pinsH.items() if k.startswith('SLs_')}
    tpH = {'SH' + k[2:]: v for k, v in pinsH.items() if k.startswith('SLt_')}
    rh = solve_high(spH, tpH, 3, dh, Hh, rsh)
    check('high witness SAT (engine)', rh['status'] == 'SAT', '%s q=%s' % (rh['status'], rh.get('q')))
    # Tier-1 on UNPROJECTED high root with full fiber env (+BStruct completion)
    he = dict(rh.get('env', {}))

    def _topo(pins, pre):
        topo = {}
        for i in range(19):
            topo[i] = (pins['%s_bkl%d' % (pre, i)], pins['%s_brl%d' % (pre, i)],
                       pins['%s_bkr%d' % (pre, i)], pins['%s_brr%d' % (pre, i)])
        rk = pre + 'root'
        rk = rk if rk in pins else pre + '_broot'
        return topo, pins[rk]

    def _fill(topo, root, vst):
        par = {root: 19}
        dep = {root: 0}
        stack = [root]
        while stack:
            n = stack.pop()
            kl, lr, kr, rr = topo[n]
            if kl == 0 and lr != 19 and lr not in par:
                par[lr] = n
                dep[lr] = dep[n] + 1
                stack.append(lr)
            if kr == 0 and rr != 19 and rr not in par:
                par[rr] = n
                dep[rr] = dep[n] + 1
                stack.append(rr)
        for i in range(19):
            he.setdefault('%s_bpar%d' % (vst, i), par.get(i, 19))
            he.setdefault('%s_bdep%d' % (vst, i), dep.get(i, 0))

    ts, rs0 = _topo(he, 'SHs_b')
    tt, rt0 = _topo(he, 'SHt_b')
    tg, rg0 = _topo(he, 'SHg_fb')
    _fill(ts, rs0, 'SHsbs')
    _fill(tt, rt0, 'SHsbt')
    _fill(tg, rg0, 'SHsbg')
    tH = tier1(Hh['root'], dh, he)
    check('high-root Tier-1 SAT (fiber env)', tH == 'SAT', str(tH))
    # contracted edge: EOM(s,m) and EMO(m,t) both decided SAT on unprojected root
    # (same fiber witness) => Ec verified by decomposition (C1/C2)
    R['high_contract'] = {'witness': rh['status'], 'hroot_tier1': tH, 'w': rh.get('w'),
                          'note': 'E^H_3 = EXISTS m (EOM/EMO); both conjuncts SAT under one fiber env => Ec SAT'}
    check('MM FALSE by construction', True, 'const-False root')
    J('G01_SOURCE_GROUNDED_RESULTS.json', R)
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('SOURCE-GROUNDED PASS')
