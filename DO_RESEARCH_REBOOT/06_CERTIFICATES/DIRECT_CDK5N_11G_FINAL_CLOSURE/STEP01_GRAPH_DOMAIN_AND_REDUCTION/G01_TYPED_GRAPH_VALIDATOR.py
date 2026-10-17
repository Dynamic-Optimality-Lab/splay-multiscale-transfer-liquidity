# G01_TYPED_GRAPH_VALIDATOR.py — sort/domain validation (Phase H/I).
# valid_state(sort, pins): domain + universe checks WITHOUT solving (syntactic +
# Tier-1 on small universe cones where supplied). classify_edge(i,j,w).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')


def classify_edge(i, j, w, matrix):
    if (i, j) == (1, 1):
        return (False, 'MM always FALSE')
    if i == 0 and j == 0:
        return (bool(matrix.get('OO', {}).get(w)), 'low alphabet -4..4')
    if i == 0 and j == 1:
        return (bool(matrix.get('OM', {}).get(w)), 'high w=6-q (audited range)')
    if i == 1 and j == 0:
        return (w == 0, 'zero midpoint exit only')
    return (False, 'unknown sort pair')
