# S2-L2 baseline + debt bound (PROVED — §5)

**Baseline.** H_j≥c_j ∀j: c_j=0 trivial (nonnegative costs); c_j=1 ⇒ x_j≠x_{j−1};
A rooted at x_{j−1} after KEEP j−1 (KEEP splays A) and at x_j after KEEP j ⇒
some access in I_j changes the A-root ⇒ pre-depth ≥1 ⇒ a≥1 there ⇒ H_j≥1.
Seam covered by exact A closure. First such StepEv per c_j=1 interval is the
baseline; intervals disjoint ⇒ baselines distinct ⇒ no double reservation.
R_j≥0 ∀j. A-root no-ops allowed (baseline is interval-level, not per-KEEP).

**Debt bound.** Marked root-paths lie in the nine-core (banked CDK5L-A geometry;
labels may permute) ⇒ d_B(x_j)≤8 ⇒ q_j≤4 for marked KEEPs, regardless of outside
nodes. c_j=0 ⇒ same key as prev KEEP, B continuously rooted there (DELETEs
freeze B) ⇒ d_B=0 ⇒ q_j=0, w_j=0. w_j>0 ⇒ c_j=1, q_j∈{3,4} ⇒ w_j∈{1,2}.
Q_B≤2C_K NOT claimed (nine-node +2 refutation banked and cited).
