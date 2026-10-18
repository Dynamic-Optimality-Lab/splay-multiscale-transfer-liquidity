# G03_UNIVERSAL_VERIFY.py — Gate H/D: per-weight universal violation queries.
# V_w(Phi) = EXISTS s,t (E_w(s,t) AND Phi(t)-Phi(s) > w) compiled on the frozen
# product DAG with scoped quantifiers. Phi built from DAG vars (QO/QO2-tagged).
# Returns SAT (counterexample model) / UNSAT (certified family) / UNKNOWN+reason.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/'
FAIL = []


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def check(name, ok, detail=''):
    print('%-52s %s %s' % (name, 'PASS' if ok else 'FAIL', detail), flush=True)
    if not ok:
        FAIL.append(name)


from PC_TYPED_DAG import DAG, BOOL, INT
from CW_PRODUCT_COMPILER import Product
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S03_EDGE_PROJECTIONS import build_projections, is_O_src, is_O_dst
from S03_SCOPE_REPAIR import normalize_fixed, free_names
from S03_QUANTIFIED_OPERATORS import QOps
from S03_TYPED_STATE_SETS import norm_pair


def phi_dag(d, theta, c, tag):
    """Affine Phi over QO(tag)-tagged vars. Returns DAG node (Int)."""
    from PC_LOW_COMPILER import mubit
    tot = d.const_int(c, 32)

    def I(v, w):
        return d.var_int(v, w)

    def B(name):
        return d.vars[tag + name]

    terms = []
    # b_depth_max via ITE chain over bdep (BState depths are NOT vars; compute
    # structurally? No: use per-node depth vars where available. Fallback: use
    # mu/sig-free structural proxies below.)
    return tot, {}


if __name__ == '__main__':
    print('G03_UNIVERSAL_VERIFY: see G03_CEGIS.py driver (consolidated)', flush=True)
