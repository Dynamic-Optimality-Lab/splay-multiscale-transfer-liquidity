# G02_POTENTIAL_OBLIGATIONS.md — Step-03 universal certificate obligations (Gate I).

For every sector G_{mu,sigma} and every edge family below, Step 03 must certify
Phi(v)-Phi(u) <= w for ALL edges (no sampling): (1) negative low edges
(w in -4..-1, all realized grounded variants incl. E3-type); (2) zero low edges;
(3) positive low edges 1..4 (return paths must be covered — nonnegativity needs
them too); (4) contracted high edges w=6-q for marked q in 0..4 (w in 2..6) with
verified midpoints; (5) anomalous OM weights -3..1: Step-02 status (UNSAT at -4;
UNKNOWN at -3 with timeout stats; SAT at -2..1 with extracted witnesses);
out-of-range edges are retained in G_star, so the Step-03 certificate must
either cover them or the Step-03 scope must be re-frozen with justification
(NOT authorized here). Candidate language: structural/piecewise/min-plus Phi
over frozen state vars; verification = edge-inequality check per family.
