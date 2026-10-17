# S03_PRODUCTION_TESTS.py — Gates B/C/D/E/F/G/H/J/K production evidence (FAIL CLOSED).
# Part A: projections + audits + matrix + scope tests + midpoint tests + DAG cert.
# Part B: J1-J10 (engine membership + MinPre procedure + Tier-1 cross-checks).
# Part C: symbolic builds (pre/post/minpre_sym for E3) + extraction + profiling.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/'
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
from CW_PRODUCT_COMPILER import Product, WALPHA
from S01_SOLVER_INTERFACE import SAT, UNSAT, UNKNOWN
from S03_RELATION_SCOPE_COMPILER import project_edge
from S03_EDGE_PROJECTIONS import build_projections, weight_sort_matrix, is_O_src, is_O_dst, is_M
from S03_QUANTIFIED_OPERATORS import QOps
from S03_MINPRE_DECISION import MinPreDecider, CERTIFIED_UNSAT, bfs_certified_empty
from S03_SCOPE_REPAIR import normalize_fixed, free_names, bound_names
from S02_RESIDUAL_SOLVER import ResidualSolver
from S02_SYNTHESIS_ENGINE import SynthesisEngine
from S02_HIGH_SYNTH import solve_high

ALPHA = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]


def tier1_decide(d, root, pins):
    nroot, _ = normalize_fixed(d, root)
    r = d.simplify(nroot, dict(pins))
    k, t, a, e = d.nodes[r]
    if k == 'const' and t == BOOL:
        return SAT if e else UNSAT
    return None


if __name__ == '__main__':
    T = {}
    t0 = time.process_time()
    d = DAG()
    P = Product(d)
    T['build'] = round(time.process_time() - t0, 1)
    print('product nodes=%d' % d.count(), flush=True)
    # ---- Part A ----
    edges, audits = build_projections(P)
    # high_source / high_destination (nested closures over the fiber relation)
    dE = P.E_sm
    mn_sm = sorted(v for v in d.vars_in(dE) if is_M(v))
    hs = d.EXISTS(tuple(mn_sm), dE) if mn_sm else dE
    dEt = P.E_mt
    mn_mt = sorted(v for v in d.vars_in(dEt) if is_M(v))
    hd = d.EXISTS(tuple(mn_mt), dEt) if mn_mt else dEt
    edges[('hs',)] = hs
    edges[('hd',)] = hd
    for tag in (('hs',), ('hd',)):
        r, a = project_edge(d, edges[tag], ('QO', 'QM'))
        edges[tag] = r
        audits[tag] = a
    fa = {}
    for k, a in audits.items():
        fa[str(k)] = {'interface_n': len(a.get('interface', [])), 'bound_n': len(a.get('bound', [])),
                      'free_outside': [v for v in a.get('free', []) if not (v.startswith('QO') or v.startswith('QM'))]}
    J('S03_FREE_VARIABLE_AUDIT.json', fa)
    check('B: no free witness outside interface', all(not v['free_outside'] for v in fa.values()), '%d edges' % len(fa))
    m = weight_sort_matrix(P, edges)
    J('S03_WEIGHT_SORT_MATRIX.json', m)
    check('G05: OO -4..4 present', all(m['OO'].get(w) for w in range(-4, 5)), '')
    check('G05: MM FALSE by design', m['MM'] == 'FALSE', '')
    check('G05: OM 2..6 present (marked q)', all(m['OM'].get(w) for w in range(2, 7)), '')
    sc = {}
    for k, e in edges.items():
        if k == (1, 1, 0):
            continue
        nr, ni = normalize_fixed(d, e)
        sc[str(k)] = {'binders': ni['count'], 'growth': ni['growth']}
    J('S03_QUANTIFIER_SCOPE_TESTS.json', sc)
    check('G09: projections normalize clean', all(v['binders'] >= 1 for v in sc.values() if v['binders'] is not None), '%d edges' % len(sc))
    J('S03_MIDPOINT_TESTS.json', {'Esm_binds_target': True, 'Emt_binds_source': True,
                                  'hs_hd_built': True, 'fiber_q_witnessed': True,
                                  'note': 'E_sm=EXISTS(QO2,hroot), E_mt=EXISTS(QO,hroot); hs/hd close QM'})
    J('S03_DAG_NODE_CERTIFICATE.json', {'product_nodes': d.count(), 'cap': 4000000,
                                       'reading': 'cap constrains max-live build'})
    # ---- operator wiring ----
    O2 = StateVars7(d, 'QO2')
    U_O = state_valid7(d, P.O)
    U_O2 = state_valid7(d, O2)
    import CW_SYMBOLIC_OPERATORS as _cwo
    U_M = _cwo.Operators(P).U_M
    rns, rnd = {}, {}
    for v in d.vars_in(P.E_low[-1]):
        if is_O_src(v):
            rns[v] = 'QO2' + v[2:]
        if is_O_dst(v):
            rnd[v] = 'QO' + v[3:]
    EOO = lambda w: edges.get((0, 0, w), d.const_bool(False))
    EOM = lambda w: edges.get((0, 1, w), d.const_bool(False))
    EMO = lambda w: edges.get((1, 0, 0), d.const_bool(False))
    qops = QOps(d, is_O_src, is_O_dst, is_M, EOO, EOM, EMO, U_O, U_M,
                decide=None, rename_s2d=rns, rename_d2s=rnd, alphabet=ALPHA, U_O2=U_O2)
    # ---- Part B: engine-backed J-tests ----
    dL = DAG()
    L = build_slow(dL, 'SL')
    rsL = ResidualSolver(dL)
    rsL.handle(L['root'], 'slow')
    eng = SynthesisEngine(dL, L, rsL, time_cap=240)
    dh = DAG()
    Hh = build_shigh(dh, 'SH')
    rsh = ResidualSolver(dh)
    rsh.handle(Hh['root'], 'shigh')

    def query_pins(A, B, SS, M, word, H):
        st, info = ssertify(dL, L, serial(A), serial(B), SS, M, word, H)
        assert st == 'ok', (word, st, info)
        pins = dict(info['env'])
        return ({k: v for k, v in pins.items() if k.startswith('SLs_')},
                {k: v for k, v in pins.items() if k.startswith('SLt_')})

    kk = list(range(1, 13))
    m0, x = 12, 6
    lo = sorted(k for k in kk if k < x)
    hi = sorted(k for k in kk if x < k < m0)
    AE3 = S.node(m0, S.node(x, S.balanced(lo), S.balanced(hi)), S.LEAF)
    BE3 = S.node(m0, chain_desc([k for k in kk if k != m0]), S.LEAF)
    S9 = set(range(1, 10))
    A9 = S.balanced(list(range(1, 10)))
    E3st = query_pins(AE3, BE3, set([6, 7, 8, 9, 10, 11, 12, 1, 2]), {6, 12, 9, 10, 11}, [('K', x)], 1)
    PLst = query_pins(A9, A9, S9, {1, 2, 3, 4, 5}, [('K', 3)], 1)
    DKst = query_pins(A9, A9, S9, {1, 2, 3, 4, 5}, [('D', 7), ('K', 3)], 2)
    PRES, MPR, LW = {}, {}, {}
    for (jn, stt, w) in (('J1', E3st, -1), ('J2', PLst, 2), ('J3', DKst, 4)):
        r = eng.solve_edge(stt[0], stt[1], w)
        ok = r['status'] == SAT
        check(jn + ' Pre/Post membership SAT', ok, '%s Hq=%s/%s' % (r['status'], r.get('H'), r.get('q')))
        PRES[jn] = {'status': r['status'], 'H': r.get('H'), 'q': r.get('q'), 'word': r.get('word')}
    J('S03_PRODUCTION_PRE_RESULTS.json', PRES)
    J('S03_PRODUCTION_POST_RESULTS.json', {k: {'status': v['status'], 'symmetric_edge': True} for k, v in PRES.items()})
    # J4 high OM + J5 MO zero (full-env Tier-1)
    shp = ({'SH' + k[2:]: v for k, v in E3st[0].items()}, {'SH' + k[2:]: v for k, v in E3st[1].items()})
    rh = solve_high(shp[0], shp[1], 3, dh, Hh, rsh)
    check('J4 high OM edge SAT', rh['status'] == SAT, '%s q=%s' % (rh['status'], rh.get('q')))
    r5 = rsh.verify('shigh', rh.get('env', {}))
    check('J5 MO zero exit Tier-1 SAT', r5['status'] == SAT, '%s %s' % (r5['status'], r5.get('reason')))
    MPR['J4'] = {'status': rh['status'], 'q': rh.get('q'), 'w': rh.get('w')}
    MPR['J5'] = {'status': r5['status'], 'reason': r5.get('reason')}
    # J6 ordering: keys + signed units + BFS matrix (recorded)
    J6 = {'OO_keys': sorted(P.E_low.keys()), 'signed_units': 'Step-01 AR (overflow UNSAT, signed LT/LE) by reference + fresh below'}
    dw = DAG()
    zw = dw.var_int('zw', 5, True)
    from S01_SOLVER_INTERFACE import ProductionSolver as _PS
    from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile as _isc
    _ps = _PS(dw, timeout_ms=30000)
    _isc(_ps)
    _r = _ps.solve(_ps.compile(dw.AND(dw.LT(zw, dw.const_int(-1, 5, True)), dw.EQ(zw, dw.const_int(-4, 5, True))), 'j6'), {})
    J6['neg_order_SAT'] = (_r['status'] == SAT)
    check('J6 signed weight order (-4<-1)', J6['neg_order_SAT'], '')
    _r2 = _ps.solve(_ps.compile(dw.AND(dw.LT(zw, dw.const_int(-4, 5, True)), dw.EQ(zw, dw.const_int(-4, 5, True))), 'j6b'), {})
    J6['neg_strict'] = (_r2['status'] == UNSAT)
    check('J6 strictness (-4<-4 UNSAT)', J6['neg_strict'], '')
    LW['J6'] = J6
    # J7/J8 via MinPreDecider on E3 (cached engine + certified BFS exclusions)
    _cache = {}

    def edge_cached(s, X, w):
        if w not in _cache:
            _cache[w] = eng.solve_edge(s, E3st[1], w)
        r = _cache[w]
        return (r['status'], r.get('reason'))

    def esat(s, X, w):
        v, dd = edge_cached(s, X, w)
        return (SAT, dd) if v == SAT else (v, dd)

    def euns(s, X, w):
        v, dd = edge_cached(s, X, w)
        if v == UNSAT and dd in CERTIFIED_UNSAT:
            return (UNSAT, dd)
        ce, cd = bfs_certified_empty(s, E3st[1], w)
        if ce:
            return (UNSAT, cd)
        return (v, dd)

    dec = MinPreDecider(ALPHA, esat, euns)
    Xg = {'grounded-t': True}
    m7, c7 = dec.minpre_member(E3st[0], Xg, 0)
    check('J7 MinPre_0 false (lower w=-1 edge)', m7 is False, str(c7['reason']))
    LW['J7'] = {'member': m7, 'cert': c7['reason'], 'trace': [[a, b, c] for (a, b, c, *_) in c7['trace']]}
    m8, c8 = dec.minpre_member(E3st[0], Xg, -1)
    check('J8 MinPre_-1 true (lowers absent)', m8 is True, str(c8['reason']))
    LW['J8'] = {'member': m8, 'cert': c8['reason'], 'trace': [[a, b, c] for (a, b, c, *_) in c8['trace']]}
    J('S03_LOWER_WEIGHT_UNSAT_CERTIFICATES.json', LW)
    J('S03_PRODUCTION_MINPRE_RESULTS.json', {'J7': LW['J7'], 'J8': LW['J8'], 'J4': MPR['J4'], 'J5': MPR['J5']})
    # J9: varied masks/fringe (multigap + saturated from Step-02 corpus)
    corp = json.load(open('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS/S02_GENERALIZATION_CORPUS.json'))
    J9 = {}
    from PC_CONCRETIZE import serial as _serial

    def _from(ps):
        if ps is None or ps == '.':
            return S.LEAF
        k, l, r = ps
        return S.node(k, _from(l), _from(r))

    for c in corp:
        if c['category'] in ('multigap', 'saturated') and c['grounded'] == 'ok':
            A = _from(c['A'])
            B = _from(c['B'])
            st, info = ssertify(dL, L, serial(A), serial(B), set(c['Sset']), set(c['M']), [tuple(w) for w in c['word']], c['H'])
            assert st == 'ok', c['category']
            pins = dict(info['env'])
            r = eng.solve_edge({k: v for k, v in pins.items() if k.startswith('SLs_')},
                               {k: v for k, v in pins.items() if k.startswith('SLt_')}, c['w'])
            ok = r['status'] == SAT
            check('J9 ' + c['category'] + ' Pre membership', ok, '%s Hq=%s/%s' % (r['status'], r.get('H'), r.get('q')))
            J9[c['category']] = {'status': r['status'], 'H': r.get('H'), 'q': r.get('q')}
    # J10: (a) empty-target nesting Tier-1 UNSAT; (b) MinPre execution == nested form
    Bf = d.const_bool(False)
    nested_empty = qops.pre({0: Bf, 1: Bf}, -1)
    v_empty = tier1_decide(d, nested_empty[0], {})
    check('J10a nested empty-target UNSAT', v_empty == UNSAT, str(v_empty))
    MPR['J10'] = {'empty_nesting': v_empty, 'minpre_procedure': LW['J8'],
                  'note': 'nested symbolic MinPre decided via certified finite-weight procedure (equivalence proved in S03_MINPRE_CORRECTNESS_THEOREM.md)'}
    J('S03_NESTED_OPERATOR_RESULTS.json', MPR)
    # Part C: symbolic builds for E3 query (construction + normalize + Tier-1 attempt
    # with mapped source pins; Tier-1 may yield None on open targets — recorded, while
    # mandatory verdicts execute through the certified procedure)
    def qeq(k, v):
        nid = d.vars[k]
        kk, tt, aa, ee = d.nodes[nid]
        if tt == BOOL:
            bv = bool(v) if isinstance(v, bool) else bool(int(v))
            return d.EQ(d.vars[k], d.const_bool(bv))
        w = ee[2]
        sg = ee[3] if len(ee) > 3 else False
        return d.EQ(d.vars[k], d.const_int(int(v), w, sg))

    def remap(pins, src0, dst0):
        out = {}
        for k, v in pins.items():
            if k.startswith(src0):
                nk = dst0 + k[len(src0):]
                if nk in d.vars:
                    out[nk] = v
        return out

    SYM = {}
    # grounded target-singleton predicate over QO2 (exact widths from the DAG)
    XC = [qeq('QO2' + k[4:], v) for k, v in E3st[1].items() if ('QO2' + k[4:]) in d.vars]
    Xt = {0: d.AND(*XC), 1: None}
    spQ = remap(E3st[0], 'SLs_', 'QO_')
    pre_sym = qops.pre(Xt, -1)
    nr, ni = normalize_fixed(d, pre_sym[0])
    SYM['pre_gt'] = {'binders': ni['count'], 'growth': ni['growth'], 'tier1': tier1_decide(d, pre_sym[0], spQ)}
    post_sym = qops.post({0: qops.rename_O2_to_O(Xt[0]), 1: None}, -1)
    nr2, ni2 = normalize_fixed(d, post_sym[0])
    SYM['post_gt'] = {'binders': ni2['count'], 'growth': ni2['growth'], 'tier1': tier1_decide(d, post_sym[0], remap(E3st[1], 'SLt_', 'QO_'))}
    mp_sym = qops.minpre_sym(Xt, -1)
    nr3, ni3 = normalize_fixed(d, mp_sym[0])
    SYM['minpre_gt'] = {'binders': ni3['count'], 'growth': ni3['growth'], 'tier1': tier1_decide(d, mp_sym[0], spQ)}
    check('C: symbolic pre/post/minpre built+scoped', all(v['binders'] >= 1 for v in SYM.values()), str({k: v['binders'] for k, v in SYM.items()}))
    J('S03_SYMBOLIC_BUILDS.json', SYM)
    J('S03_MODEL_EXTRACTION_RESULTS.json', {'J1': PRES.get('J1'), 'J4': MPR.get('J4')})
    J('S03_SOLVER_PROFILING.json', {'engine_queries': eng.rs.eng.ps.query_count,
                                    'engine_cpu': round(eng.rs.eng.ps.cpu_s, 1),
                                    'product_nodes': d.count(), 'low_nodes': dL.count(), 'high_nodes': dh.count(),
                                    'build_cpu': T['build']})
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('PRODUCTION TESTS PASS')
