# CORE-01 Cyclic Flatness Theorem (CONDITIONAL — Gate F)

ASSUME universal monotonicity: forall e=(s,t), C(t) subset C(s) (hence
rho(t) <= rho(s)). Let C be any closed walk s0->...->sn=s0. Then
rho(s0) >= rho(s1) >= ... >= rho(sn) = rho(s0), so rho(s_i) = rho(s_0)
for all i. Therefore every edge of every closed walk satisfies
rho(t) = rho(s) — strict-descent edges (rho(t) < rho(s)) occur in NO
closed walk. Define E_flat = {e : rho(t)==rho(s)}, G_flat =
(V, E_flat). Then ClosedWalks(G_hat) = ClosedWalks(G_flat) with identical
edge sequences and signed weights (nothing merged, no zero-weight
omission, midpoints untouched). PROOF STATUS: valid conditional theorem;
PREMISE OPEN (low multi-event hole). Instantiation available TODAY for
the high-edge subgraph (proved universal there): high-only closed walks
admit no strict-descent edge.
