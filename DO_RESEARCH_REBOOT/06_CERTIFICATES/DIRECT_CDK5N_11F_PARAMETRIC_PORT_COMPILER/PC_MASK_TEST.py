# PC_MASK_TEST.py — V6/G09: all 126 masks via the single parametric 9-bit mask variable.
import sys, json, itertools, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
import splay as S
from PC_TYPED_DAG import DAG
from PC_PRODUCT_COMPILER import Product
from PC_SOLVER_BACKEND import Solver, SAT, UNSAT, UNKNOWN
from PC_CONCRETIZE import serial
from PC_CERTIFY import certify
from PC_LOW_COMPILER import build_low

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/'
MASKS = list(itertools.combinations(range(9), 5))
assert len(MASKS) == 126


def mu_of(mask):
    v = 0
    for k in mask:
        v |= 1 << k
    return v


if __name__ == '__main__':
    t0 = time.time()
    d = DAG()
    P = Product(d)
    from PC_SYMBOLIC_OPERATORS import Operators
    op = Operators(P)
    # V6a: valid_state SAT for each of the 126 masks (single parametric variable, no copies)
    n_sat = 0
    for m in MASKS:
        sv = Solver(d, node_cap=50000, time_cap=20)
        r, _, _ = sv.solve(op.U_O, assume={'PO_mu': mu_of(m)})
        assert r == SAT, ('mask-unsat', m, r)
        n_sat += 1
    print('masks valid_state SAT: %d/126 time=%.1fs' % (n_sat, time.time() - t0), flush=True)
    json.dump({'masks_sat': n_sat, 'mask_transitions': 'pending'}, open(PDIR + 'PC_ALL_126_MASKS.json', 'w'), indent=1)
    # V6b: one certified transition per mask (single KEEP on first marked key, 9-key all-S)
    dL = DAG()
    L0 = build_low(dL, 'PL')
    keys = list(range(1, 10))
    Sset = set(keys)
    ntr = 0
    for m in MASKS:
        M = set(i + 1 for i in m)
        done = False
        for x in sorted(M):
            A = S.balanced(keys)
            word = [('K', x)]
            a = (S.lookup(A, x)[1] + 1) // 2
            if a > 2:
                continue
            st, info = certify(dL, L0, serial(A), serial(A), Sset, M, word, a)
            if st == 'skip':
                continue
            assert st == 'ok', ('mask-transition', m, x, info)
            done = True
            break
        if done:
            ntr += 1
    print('mask transitions certified: %d/126 time=%.1fs' % (ntr, time.time() - t0), flush=True)
    json.dump({'masks_sat': n_sat, 'mask_transitions': ntr}, open(PDIR + 'PC_ALL_126_MASKS.json', 'w'), indent=1)
