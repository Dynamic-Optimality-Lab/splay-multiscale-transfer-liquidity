# S03_EDGE_PROJECTIONS.py — production edge projections (Gates B/G05/G06-G08).
# Wraps CW_PRODUCT_COMPILER edges with top-level EXISTS over every non-interface
# variable (S03_RELATION_SCOPE_COMPILER.project_edge) + mechanical free-var audit.
# Interfaces: OO keeps QO*/QO2*; OM keeps QO*/QM*; MO keeps QM*/QO2*.
# Weight alphabet preserved structurally (incl. unrealized weights as FALSE).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
from PC_TYPED_DAG import DAG, BOOL
from S03_RELATION_SCOPE_COMPILER import project_edge


def is_O_src(v):
    return v.startswith('QO') and not v.startswith('QO2')


def is_O_dst(v):
    return v.startswith('QO2')


def is_M(v):
    return v.startswith('QM')


OO_KEEP = ('QO',)   # includes QO2 by prefix; split below
OM_KEEP = ('QO', 'QM')
MO_KEEP = ('QM', 'QO2')


def oo_keep(v):
    return is_O_src(v) or is_O_dst(v)


def build_projections(P):
    """P: CW Product. Returns (edges, audits): edges[(i,j,w)] with EMM=FALSE consts."""
    d = P.d
    edges, audits = {}, {}
    for w, e in P.E_low.items():
        r, a = project_edge(d, e, ('QO',))
        # project_edge keeps by prefix; OO interface = QO* (src+dst). Hidden bound.
        edges[(0, 0, w)] = r
        audits[(0, 0, w)] = a
    for w in range(-4, 7):
        try:
            e = P._sm_w(w)
        except Exception:
            continue
        r, a = project_edge(d, e, ('QO', 'QM'))
        edges[(0, 1, w)] = r
        audits[(0, 1, w)] = a
    r, a = project_edge(d, P.E_mt, ('QM', 'QO2'))
    edges[(1, 0, 0)] = r
    audits[(1, 0, 0)] = a
    edges[(1, 1, 0)] = d.const_bool(False)
    audits[(1, 1, 0)] = {'interface': [], 'bound': [], 'free': [], 'false_by_design': True}
    return edges, audits


def weight_sort_matrix(P, edges):
    m = {'OO': {}, 'OM': {}, 'MO': [0], 'MM': 'FALSE'}
    for w in range(-4, 7):
        m['OO'][w] = (0, 0, w) in edges and edges[(0, 0, w)] is not None
    for w in range(-4, 7):
        m['OM'][w] = (0, 1, w) in edges
    return m
