# DIRECT-U1-01: universal formulation (exact)

Pair state (A,B): labeled BSTs on keys 1..n. Diagonal starts D_n={(T,T)}.
Reachable set R_n via KEEP Kx: (S_x(A),S_x(B)), and DELETE Dx: (S_x(A),B)
(present keys only; DELETE never removes keys). Per-access signed weight:
w(Kx)=⌊d_B/2⌋−2⌈d_A/2⌉; w(Dx)=−2⌈d_A/2⌉ (pre-access depths). A-root no-op
(a=0) KEEP may carry q>0, hence w>0 on single accesses — included.
W(H)=Σw_t=Q_B−2A (identity). Closed walk: exact (A,B) restoration from a
diagonal-reachable start. Block identity W(γ)=Σδ_i proved (26AJ Lemma 1);
access-level and block-level accounting are the same sum, regrouped
(no-op legs carry a=0; every access belongs to exactly one cyclic block).
Universal target: ∀n, ∀ closed γ⊆Γ_n: W(γ)≤0 ⟺ (fixed n) no positive-weight
directed cycle in the reachable pair graph. Finite-n graph facts never
promoted to all-n theorems (N20/N21).
