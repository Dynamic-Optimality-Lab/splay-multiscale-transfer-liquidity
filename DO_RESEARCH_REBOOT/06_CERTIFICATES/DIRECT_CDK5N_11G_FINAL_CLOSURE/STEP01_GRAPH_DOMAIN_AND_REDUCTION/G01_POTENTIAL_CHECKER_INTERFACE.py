# G01_POTENTIAL_CHECKER_INTERFACE.py — certificate condition (Phase G/H).
# check_potential_edge(phi, u, v, w): True iff phi[v]-phi[u] <= w (exact ints).
# find_potential_violation(phi, edges): first violating edge or None.
# (Candidate Phi search belongs to Step 03; this interface is frozen here.)


def check_potential_edge(phi, u, v, w):
    return phi[v] - phi[u] <= w


def find_potential_violation(phi, edges):
    """edges: iterable of (u, v, w). Returns (u,v,w) or None."""
    for (u, v, w) in edges:
        if not check_potential_edge(phi, u, v, w):
            return (u, v, w)
    return None
