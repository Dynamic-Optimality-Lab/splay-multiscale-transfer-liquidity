# G01_MIDPOINT_CONTRACTION.py — exact E^H construction (Phase C, C1/C2).
# contracted(s,t,w) = EXISTS m-vars (EOM_w(s,m) AND EM0_0(m,t)) over shared QM
# interface. C1 (expansion): every contracted edge unfolds to a witness m by
# construction. C2 (contraction): every O->M->O passage folds (same formula read
# backwards). Both hold BY CONSTRUCTION (single formula, both directions);
# C3-C5 proved in G01_NEGATIVE_CYCLE_EQUIVALENCE.md; K3/K4 test execution.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import BOOL


def contract(d, EOM_w, EMO_0, mvars):
    """E^H_w(s,t) = EXISTS m (E^OM_w(s,m) AND E^MO_0(m,t)). mvars: QM names bound."""
    body = d.AND(EOM_w, EMO_0)
    if not mvars:
        return body
    return d.EXISTS(tuple(sorted(mvars)), body)


def mid_names_of(d, root, is_mid):
    return sorted(v for v in d.vars_in(root) if is_mid(v))
