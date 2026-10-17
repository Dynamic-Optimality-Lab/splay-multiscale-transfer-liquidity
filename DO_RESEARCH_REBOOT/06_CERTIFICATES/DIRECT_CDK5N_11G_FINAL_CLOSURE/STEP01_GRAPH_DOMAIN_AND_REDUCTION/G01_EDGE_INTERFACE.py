# G01_EDGE_INTERFACE.py — frozen typed edge interface (Phase H/I).
# Conceptual operations over the contracted two-sort graph, implemented as thin
# adapters over the frozen Step-01/02/03 stack (S03 projections + QOps, Tier-1/Z3,
# Step-02 engine). No new solving, no new semantics, no domain change.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')
from S03_EDGE_PROJECTIONS import build_projections


def build_graph(d, P):
    """Compile-once graph view: projected edges + audit. Caller compiles queries."""
    edges, audits = build_projections(d, P)
    return {'edges': edges, 'audits': audits, 'dag': d, 'product': P}


def edge_root(G, i, j, w):
    key = (i, j, w)
    if key not in G['edges']:
        raise AssertionError(('unknown edge family', key))
    return G['edges'][key]
