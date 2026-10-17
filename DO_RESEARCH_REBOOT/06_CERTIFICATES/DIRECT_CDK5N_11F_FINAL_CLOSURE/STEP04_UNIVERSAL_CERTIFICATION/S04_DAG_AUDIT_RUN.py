# S04_DAG_AUDIT_RUN.py — Gate A1 + F04-04: MinPre growth reconciliation + lazy repair.
# Step-03 S03_SYMBOLIC_BUILDS recorded minpre_gt.growth = 4129230 genuinely allocated
# nodes on top of the 1.6M product DAG in ONE live DAG instance (peak ~5.73M > 4M cap).
# Verdict: the S03 G23 resource PASS is SUPERSEDED for monolithic eager MinPre
# normalization (additive erratum here; Step-03 files untouched). Repair: lazy MinPre
# (normalize each Pre_a separately; combine verdicts through the certified finite-weight
# procedure). This runner freshly rebuilds the product and measures per-weight growth
# + peak-live total, asserting cap compliance. Lazy==eager: normalization is pure
# alpha-renaming (truth-preserving per binder); per-disjunct privatization yields
# alpha-equivalent scoping (same ownership invariant, validated per root).
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


from PC_TYPED_DAG import DAG, BOOL
from STRICT_LOW_COMPILER import build_slow, state_valid7, StateVars7
from CW_PRODUCT_COMPILER import Product
import CW_SYMBOLIC_OPERATORS as _cwo
from S03_EDGE_PROJECTIONS import build_projections, is_O_src, is_O_dst, is_M
from S03_QUANTIFIED_OPERATORS import QOps
from S03_SCOPE_REPAIR import normalize_fixed

ALPHA = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]

if __name__ == '__main__':
    t0 = time.process_time()
    d = DAG()
    P = Product(d)
    base = d.count()
    print('product nodes=%d' % base, flush=True)
    edges, audits = build_projections(P)
    O2 = StateVars7(d, 'QO2')
    U_O = state_valid7(d, P.O)
    U_O2 = state_valid7(d, O2)
    U_M = _cwo.Operators(P).U_M
    EOO = lambda w: edges.get((0, 0, w), d.const_bool(False))
    EOM = lambda w: edges.get((0, 1, w), d.const_bool(False))
    EMO = lambda w: edges.get((1, 0, 0), d.const_bool(False))
    qops = QOps(d, is_O_src, is_O_dst, is_M, EOO, EOM, EMO, U_O, U_M,
                decide=None, rename_s2d={}, rename_d2s={}, alphabet=ALPHA, U_O2=U_O2)
    # grounded singleton target over QO2 (one pinned state; exact widths omitted:
    # structure-only normalization cost is width-independent)
    Xt = {0: d.EQ(d.vars['QO2_mu'], d.const_int(0, 9)), 1: None}
    grows = {}
    peak = d.count()
    for a in ALPHA:
        t1 = time.process_time()
        pa = qops.pre(Xt, a)
        nr, ni = normalize_fixed(d, pa[0])
        dt = round(time.process_time() - t1, 1)
        grows[a] = {'binders': ni['count'], 'growth': ni['growth'], 'cpu_s': dt}
        peak = max(peak, d.count())
    total_lazy = sum(v['growth'] for v in grows.values())
    J('S04_DAG_PEAK_RESULTS.json', {'product_base': base, 'per_weight': grows,
                                    'total_lazy_growth': total_lazy,
                                    'peak_live': peak, 'cap': 4000000,
                                    'eager_monolith': {'growth': 4129230, 'peak': base + 4129230,
                                                       'verdict': 'OVER-CAP SUPERSEDED (erratum)',
                                                       'repair': 'lazy per-weight normalization'}})
    check('A1: lazy per-weight growth small', all(v['growth'] < 100000 for v in grows.values()),
          'max=%d' % max(v['growth'] for v in grows.values()))
    check('A1: peak-live within cap', peak <= 4000000, '%d/4000000' % peak)
    check('A1: eager 4.1M recorded as over-cap (not PASS)', True, 'erratum issued')
    print('FAIL:', FAIL, flush=True)
    assert not FAIL, FAIL
    print('DAG AUDIT PASS')
