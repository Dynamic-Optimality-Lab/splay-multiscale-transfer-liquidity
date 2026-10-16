# CW_OPERATOR_TEST.py — Gate I: production operators (binder/units + grounded + bounded UNSAT).
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
import splay as S
from PC_TYPED_DAG import DAG
from CW_PRODUCT_COMPILER import Product, WALPHA
from CW_SYMBOLIC_OPERATORS import Operators
from PC_SOLVER_BACKEND import SAT, UNSAT, UNKNOWN, struct_order
from CW_QUANTIFIED_BACKEND import QSolver
from PC_CONCRETIZE import serial
from STRICT_CERTIFY import ssertify
from STRICT_LOW_COMPILER import build_slow

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/'

if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    P = Product(d)
    op = Operators(P)
    print('product+operators nodes=%d' % d.count(), flush=True)
    # units: binder hygiene, MinPre structure, empty target, type separation
    d2 = DAG()
    x = d2.var_bool('x')
    y = d2.var_bool('y')
    inner = d2.EXISTS(('y',), d2.AND(x, y))
    renamed = d2.subst(inner, {'x': 'x2'})
    assert d2.vars_in(renamed) == {'x2', 'y'}
    outer = d2.EXISTS(('y',), d2.AND(renamed, y))
    assert QSolver(d2).solve(outer, assume={'x2': 1, 'y': 1})[0] == SAT
    assert QSolver(d2).solve(outer, assume={'x2': 0})[0] == UNSAT
    X0 = {0: d.const_bool(True), 1: None}
    m3 = op.minpre(X0, 3)
    assert m3[0] is not None
    cone = d.topo([m3[0]])
    assert 'not' in set(d.nodes[n][0] for n in cone) and 'exists' in set(d.nodes[n][0] for n in cone)
    assert d.ev_iter(op.pre({0: None, 1: None}, 0)[0], {}) is False
    # negated existential: NOT EXISTS z (z=1) over one-bit z is FALSE (V-semantics check)
    dz = DAG()
    z = dz.var_int('z', 1)
    neg = dz.NOT(dz.EXISTS(('z',), dz.EQ(z, dz.const_int(1, 1))))
    assert QSolver(dz).solve(neg)[0] == UNSAT
    print('operator units ok', flush=True)
    # grounded membership + bounded UNSAT (micro 9-key all-S, S=C_M trivially)
    dL = DAG()
    L0 = build_slow(dL, 'SL')
    rng = random.Random(402)
    keys = list(range(1, 10))
    Sset = set(keys)
    pool = []
    for seed in range(8):
        r2 = random.Random(2100 + seed)
        ks = sorted(keys)
        r2.shuffle(ks)
        t = S.LEAF
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ks:
            t = _ins(t, k)
        pool.append(t)
    nagree = nunsat = nunk = nskip = 0
    edges = []
    for trial in range(40):
        A = rng.choice(pool)
        rA = A[1]
        M = set([rA] + [k for k in keys if k != rA][:4])
        x = rng.choice(keys)
        md = rng.choice(['K', 'D'])
        dd = S.lookup(A, x)[1]
        a = (dd + 1) // 2
        if a > 2:
            nskip += 1
            continue
        if md == 'K' and x not in M:
            M = set([x] + [k for k in keys if k != x][:4])
        word = [(md, x)]
        st, info = ssertify(dL, L0, serial(A), serial(A), Sset, M, word, a)
        if st == 'skip':
            nskip += 1
            continue
        if st == 'fail':
            print('V11 grounded FAIL', trial)
            raise AssertionError('v11-grounded')
        nagree += 1
        edges.append((info['env'], info['w']))
        if len(edges) >= 8:
            break
    print('grounded edges: %d skipped %d' % (len(edges), nskip), flush=True)

    def to_prod(e):
        o = {}
        for k, v in e.items():
            if k.startswith('SLs_'):
                o['QO_' + k[4:]] = v
            elif k.startswith('SLt_'):
                o['QO2_' + k[4:]] = v
            else:
                o[k] = v
        return o

    for (e, w0) in edges:
        ep = to_prod(e)
        XC = []
        for k, v in ep.items():
            if k.startswith('QO2_') and ('_mu' in k or '_aS' in k or '_aI' in k or '_ak' in k or '_sg' in k or '_bkl' in k or '_brl' in k or '_bkr' in k or '_brr' in k or '_broot' in k or '_blo' in k or '_bhi' in k):
                if k.endswith('_aS0') or k.endswith('_aS1') or k.endswith('_aS2') or k.endswith('_aS3') or k.endswith('_aS4') or k.endswith('_aS5') or k.endswith('_aS6'):
                    XC.append(d.EQ(d.vars[k], d.const_bool(bool(v))))
                else:
                    wdt = 9 if ('_sg' in k or '_mu' in k) else 32
                    XC.append(d.EQ(d.vars[k], d.const_int(v, wdt)))
        X = {0: d.AND(*XC), 1: None}
        pre0 = op.pre(X, w0)[0]
        # bridge unrenamed low params (CL_w weight selector, CL_H/Q...): same low compiler,
        # SL-tagged grounded values carry over (subst renaming is an isomorphism).
        fill = {}
        for v in sorted(d.vars_in(pre0) - set(ep)):
            if v == 'CL_w':
                fill[v] = w0
            elif (v.startswith('CL') or v.startswith('CH')) and ('SL' + v[2:]) in ep:
                fill[v] = ep['SL' + v[2:]]
            else:
                raise AssertionError(('unbridged product var', v))
        env2 = dict(ep)
        env2.update(fill)
        assert d.ev_iter(pre0, env2) is True, ('pre-member', w0)
        nagree += 1
        for w1 in (w0 - 1, w0 + 2):
            pins = dict(env2)
            for i in range(10, 127):
                pins[f'SLw_p{i}'] = 0
            sv = QSolver(d, node_cap=200000, time_cap=45, order=struct_order('SL'))
            pre1 = op.pre(X, w1)[0]
            r, _, _ = sv.solve(pre1, assume=pins)
            if r == UNSAT:
                nunsat += 1
            else:
                nunk += 1
    print('operators: agree=%d unsat=%d unknown=%d skipped=%d time=%.1fs' % (nagree, nunsat, nunk, nskip, time.time() - t0), flush=True)
    json.dump({'binder': True, 'minpre_struct': True, 'empty_target': True, 'neg_exists': True,
               'micro_agree': nagree, 'micro_unsat': nunsat, 'micro_unknown': nunk},
              open(PDIR + 'CW_PRE_POST_MINPRE_RESULTS.json', 'w'), indent=1)
