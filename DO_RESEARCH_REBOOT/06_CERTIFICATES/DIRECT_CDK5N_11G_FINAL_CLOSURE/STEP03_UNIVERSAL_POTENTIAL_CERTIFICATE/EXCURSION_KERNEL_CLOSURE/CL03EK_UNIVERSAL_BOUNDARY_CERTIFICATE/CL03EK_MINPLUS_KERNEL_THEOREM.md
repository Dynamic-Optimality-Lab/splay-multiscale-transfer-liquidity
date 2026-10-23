# CL-03EK Min-Plus Kernel Theorem (EK-3: PROVED, conditional on H3)

Define Q_min on shallow vertices: all 00 edges + one kernel edge u->v per
pair with K(u,v) finite, weight K(u,v), where K = E_01 (x) E_11* (x) E_10
in min-plus arithmetic (E_11* = reflexive-transitive min-plus closure
including the empty interior path; no numeric approximation). THEOREM:
NonNegCycles(G_hat) iff [NonNegCycles(G_D) and NonNegCycles(Q_min)].
Proof (=>): G_D cycles are frozen cycles; for Q_min, expand each kernel
edge to an attaining excursion (EK-2) and each 00 edge to itself: a
negative Q_min closed walk becomes a negative frozen closed walk.
(<=): a negative frozen closed walk is deep-only (done) or mixed;
contract maximal excursions to kernel edges: each contraction replaces
w(P) by K(u,v) <= w(P) (minimum), so the contracted shallow closed walk
has weight <= original < 0. Exact in both directions; parallel kernel
edges retained (attaining excursions may differ).
