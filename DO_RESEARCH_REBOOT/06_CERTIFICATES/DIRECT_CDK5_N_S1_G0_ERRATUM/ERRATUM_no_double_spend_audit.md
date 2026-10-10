# No-double-spend audit (PROVED)

1. Intervals I_j are disjoint by construction (each access follows one preceding
   KEEP); verified on the witness (17 blocks partition 17 accesses).
2. H_j are fixed sums over disjoint sets — credit is counted, not drawn; overlap
   of Type K/P eligibility on one interval yields one inequality w_j≤R_j.
3. The paired reserve R_*+R_k is spent once for the joint inequality; the
   successor K7 (which independently has H=2) is not separately credited.
4. Baseline StepEvs are distinct accesses (first root-changing access per
   c_j=1 interval). No StepEv funds two intervals. ∎
