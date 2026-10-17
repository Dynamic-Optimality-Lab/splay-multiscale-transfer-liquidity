# S03_TYPED_STATE_SETS.py — typed set predicates X=(X_O,X_M) + valid universes.
# A set is a dict {0: dag-node-or-None, 1: dag-node-or-None} in canonical coordinates
# (sort-0 vars for O, sort-1 vars for M). Universes U_O/U_M supplied per backend
# (production: state_valid7 / mid-universe; small graphs: hand-built predicates).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import BOOL


def norm_pair(d, X):
    """None components -> Boolean False (empty side), passthrough otherwise."""
    return {s: (X.get(s) if X.get(s) is not None else d.const_bool(False)) for s in (0, 1)}


def is_side_empty_const(d, x):
    k, t, a, e = d.nodes[x]
    return k == 'const' and t == BOOL and not e


def union(d, X, Y):
    return {s: d.OR(X.get(s) if X.get(s) is not None else d.const_bool(False),
                     Y.get(s) if Y.get(s) is not None else d.const_bool(False)) for s in (0, 1)}


def intersection(d, X, Y):
    return {s: d.AND(X.get(s) if X.get(s) is not None else d.const_bool(False),
                      Y.get(s) if Y.get(s) is not None else d.const_bool(False)) for s in (0, 1)}


def complement(d, X, U_O, U_M):
    """Relative to the valid universes (never over invalid assignments)."""
    xo = X.get(0) if X.get(0) is not None else d.const_bool(False)
    xm = X.get(1) if X.get(1) is not None else d.const_bool(False)
    return {0: d.AND(U_O, d.NOT(xo)), 1: d.AND(U_M, d.NOT(xm))}


def symdiff(d, X, Y):
    """(X∧¬Y)∨(Y∧¬X) per sort (for equivalence-by-emptiness of universe-restricted sets)."""
    out = {}
    for s in (0, 1):
        xa = X.get(s) if X.get(s) is not None else d.const_bool(False)
        ya = Y.get(s) if Y.get(s) is not None else d.const_bool(False)
        out[s] = d.OR(d.AND(xa, d.NOT(ya)), d.AND(ya, d.NOT(xa)))
    return out
