# G02_SYMBOLIC_CYCLE_ENCODER.py — lazy cycle predicates (Gate B/C2, no eager unrolling).
# A k-edge cycle predicate is NEVER built as k copies of the 1.6M-node circuit.
# Instead: per-edge roots (shared, compile-once) + time-indexed interface equalities
# + incremental weight accumulator. Execution goes through the incremental solver,
# which decides edge-by-edge with early UNSAT propagation.
# k=1 theorem (no solver needed): a genuine single-KEEP closed walk is impossible
# (genuine KEEP changes B by definition => B_T != B_0); nongenuine single KEEPs have
# dB=0 => q=0, and macro H = a >= 0 with w = 2H - 0 = 2H >= 0. Hence no negative
# 1-edge closed walk exists. (Proved, not merely searched.)
# Simple-cycle lemma: a negative closed walk exists iff a negative SIMPLE directed
# cycle exists (decompose into simple cycles; a negative total forces a negative
# part). Proof by the standard decomposition argument (doc).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL


def edge_vars(d, tag):
    """Time-indexed interface var set for one step (caller allocates per k lazily)."""
    return tag


def cycle_predicate_lazy(E_funcs, U, k, alpha):
    """Specification of Cycle_k as data (NOT a built formula):
    {'edges': [(E_w, i) for i in range(k)], 'closure': True, 'weights': alpha}.
    Executed incrementally by G02_INCREMENTAL_CYCLE_SOLVER."""
    return {'kind': 'Cycle', 'k': k, 'alphabet': list(alpha),
            'edge_families': ['EOO', 'EOM', 'EMO'],
            'closure': 's_k == s_0 (full interface equality)'}


def neg_cycle_predicate_lazy(E_funcs, U, k, alpha):
    return {'kind': 'NegCycle', 'k': k, 'alphabet': list(alpha),
            'extra': 'sum(w_i) < 0 (exact Int arithmetic)'}
