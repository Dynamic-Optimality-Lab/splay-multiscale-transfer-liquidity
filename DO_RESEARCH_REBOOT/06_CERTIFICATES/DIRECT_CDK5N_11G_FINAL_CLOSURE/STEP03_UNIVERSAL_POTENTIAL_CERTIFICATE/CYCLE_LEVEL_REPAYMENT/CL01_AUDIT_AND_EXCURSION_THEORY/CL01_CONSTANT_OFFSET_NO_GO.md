# CL-01 Constant-Offset No-Go Lemma (PROVED on certified edges)

Family Phi_K(s) = C2(s)-K if deep else C5(s), K constant. E4 edge (seed0,
certified low OO, 1->0, w=-2): C2(s)=12, C5(t)=8. Requires 8-(12-K)<=-2,
i.e. K<=2. Crossing edge idx1 (certified low OO, 0->1, w=1): C5(s)=2,
C2(t)=10. Requires 10-K-2<=1, i.e. K>=7. Conjunction K<=2 AND K>=7 is
impossible. VERIFIED by independent recompute from stored features
(SR-02C base + hunt corpora). Scope: refutes exactly the constant-offset
repair family for fixed (C2,C5,guard-7). Does NOT refute: other vertex
potentials, nonlinear/min-plus forms with state-dependent offsets,
structural decompositions, or NonNegCycles itself. (Weaker crossings give
K>=6, K>=2 — consistent subsumed bounds; the K>=7 instance carries the
contradiction.)
