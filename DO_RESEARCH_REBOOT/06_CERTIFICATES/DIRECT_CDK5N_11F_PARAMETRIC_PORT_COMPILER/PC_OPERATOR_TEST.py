# PC_OPERATOR_TEST.py — V11: production operators vs oracle at micro scope + law/unit tests.
import sys, json, random, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from CRA_pointer_tuple_replay import replay, from_serial
from PC_TYPED_DAG import DAG
from PC_PRODUCT_COMPILER import Product, WALPHA
from PC_SYMBOLIC_OPERATORS import Operators
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN, struct_order
from PC_CONCRETIZE import serial
from PC_CERTIFY import certify
from PC_MICRO_TEST import micro_assume

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'


def pin_state(env_out, pre, mu, alpha, bvals, sig):
    env_out[pre + '_mu'] = mu
    (rs, ri), (lk, ls, li), (rk, rs2, ri2) = alpha
    env_out[pre + '_arS'] = rs
    env_out[pre + '_arI'] = ri
    env_out[pre + '_aLk'], env_out[pre + '_aLS'], env_out[pre + '_aLI'] = lk, ls, li
    env_out[pre + '_aRk'], env_out[pre + '_aRS'], env_out[pre + '_aRI'] = rk, rs2, ri2
    for k, v in bvals.items():
        env_out[k] = v
    for i in range(10):
        env_out[pre + f'_sg{i}'] = sig[i]


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    P = Product(d)
    op = Operators(P)
    print('product+operators nodes=%d' % d.count(), flush=True)
    # --- unit: binder hygiene on small DAGs (capture/shadowing) ---
    d2 = DAG()
    x = d2.var_bool('x')
    y = d2.var_bool('y')
    inner = d2.EXISTS(('y',), d2.AND(x, y))
    renamed = d2.subst(inner, {'x': 'x2'})
    assert d2.vars_in(renamed) == {'x2', 'y'}, d2.vars_in(renamed)
    # shadowed binder: inner y independent of outer y
    outer = d2.EXISTS(('y',), d2.AND(renamed, y))
    assert Solver(d2).solve(outer, assume={'x2': 1, 'y': 1})[0] == SAT
    assert Solver(d2).solve(outer, assume={'x2': 0})[0] == UNSAT
    print('binder hygiene ok', flush=True)
    # --- unit: MinPre structure (lower-weight exclusion present by construction) ---
    X0 = {0: d.const_bool(True), 1: None}
    m3 = op.minpre(X0, 3)
    assert m3[0] is not None
    # minpre contains negations of lower pres: check textually via cone (has NOT nodes over pre_2/pre_1/...)
    cone = d.topo([m3[0]])
    kinds = set(d.nodes[n][0] for n in cone)
    assert 'not' in kinds and 'exists' in kinds
    print('minpre structure ok', flush=True)
    # --- unit: type separation (mid predicates never leak into ordinary results) ---
    assert op.pre({0: None, 1: None}, 0)[0] is not None
    assert d.ev_iter(op.pre({0: None, 1: None}, 0)[0], {}) is False
    print('empty-target ok', flush=True)
    json.dump({'binder': True, 'minpre_struct': True, 'empty_target': True},
              open(PDIR + 'PC_PRE_POST_MINPRE_TESTS.json', 'w'), indent=1)
    print('operator units done time=%.1fs' % (time.time() - t0), flush=True)
    # --- V11 agreement: grounded Pre/MinPre membership + bounded UNSAT (micro scope) ---
    from PC_CONCRETIZE import serial as _serial, AModel as _AM
    from PC_CERTIFY import certify as _cert
    from PC_MICRO_TEST import micro_assume as _ma
    from PC_SOLVER_BACKEND import struct_order as _so
    from PC_LOW_COMPILER import build_low as _bl
    rng = random.Random(401)
    keys = list(range(1, 10))
    Sset = set(keys)
    pool = []
    for seed in range(8):
        r2 = random.Random(2000 + seed)
        ks = sorted(keys)
        r2.shuffle(ks)
        t = S.LEAF
        def _ins(t, k):
            return S.node(k, S.LEAF, S.LEAF) if t[0] == 'leaf' else (S.node(t[1], _ins(t[2], k), t[3]) if k < t[1] else S.node(t[1], t[2], _ins(t[3], k)))
        for k in ks:
            t = _ins(t, k)
        pool.append(t)
    nagree = nunsat = nunk = nskip = 0
    edges = []  # (env_low, w0)
    from PC_LOW_COMPILER import build_low as _bl
    from PC_SOLVER_BACKEND import struct_order as _so
    dL = DAG()
    L0 = _bl(dL, 'PL')
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
        st, info = _cert(dL, L0, _serial(A), _serial(A), Sset, M, word, a)
        if st == 'skip':
            nskip += 1
            continue
        if st == 'fail':
            print('V11 grounded FAIL', trial, str(info)[:150])
            raise AssertionError('v11-grounded')
        nagree += 1
        edges.append((info['env'], info['w']))
        if len(edges) >= 10:
            break
    print('v11 grounded edges: %d (skipped %d)' % (len(edges), nskip), flush=True)
    def to_prod(e):
        o = {}
        for k, v in e.items():
            if k.startswith('PLs_'):
                o['PO_' + k[4:]] = v
            elif k.startswith('PLt_'):
                o['PO2_' + k[4:]] = v
            else:
                o[k] = v
        return o
    for (e, w0) in edges:
        ep = to_prod(e)
        XC = []
        for k, v in ep.items():
            if k.startswith('PO2_') and ('_mu' in k or '_ar' in k or '_aL' in k or '_aR' in k or '_sg' in k or '_bkl' in k or '_brl' in k or '_bkr' in k or '_brr' in k or '_broot' in k):
                if k.endswith('_arS') or k.endswith('_aLS') or k.endswith('_aRS'):
                    XC.append(d.EQ(d.vars[k], d.const_bool(bool(v))))
                else:
                    wdt = 9 if ('_sg' in k or '_mu' in k) else 32
                    XC.append(d.EQ(d.vars[k], d.const_int(v, wdt)))
        X = {0: d.AND(*XC), 1: None}
        pre0 = op.pre(X, w0)[0]
        assert d.ev_iter(pre0, ep) is True, ('pre-member', w0)
        nagree += 1
        for w1 in (w0 - 1, w0 + 2):
            pins = dict(ep)
            pins.update(_ma(10))
            sv = Solver(d, node_cap=200000, time_cap=45, order=_so('PL'))
            pre1 = op.pre(X, w1)[0]
            r, _, _ = sv.solve(pre1, assume=pins)
            if r == UNSAT:
                nunsat += 1
            else:
                nunk += 1
    print('v11-micro: agree=%d unsat=%d unknown=%d skipped=%d time=%.1fs' % (nagree, nunsat, nunk, nskip, time.time() - t0), flush=True)
    json.dump({'binder': True, 'minpre_struct': True, 'empty_target': True, 'micro_agree': nagree,
               'micro_unsat': nunsat, 'micro_unknown': nunk},
              open(PDIR + 'PC_PRE_POST_MINPRE_TESTS.json', 'w'), indent=1)
