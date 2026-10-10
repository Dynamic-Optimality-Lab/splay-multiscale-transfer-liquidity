# S1P failure-attack audit (§20) — all discharged

A. **Seam.** Cyclic intervals partition all accesses (each follows one preceding
   KEEP); wraparound interval verified in IV tables (K3 H=16 includes DELETE
   suffix). PASS (no omission/double-count).
B. **Prefix.** Theorem accounts cycle only; prefix excluded by definition; witness
   has no prefix (diagonal start) and proof never assumes A=B mid-cycle. PASS.
C. **Projection.** Nine-core ⇒ d_B≤8 via marked root-paths (labels may permute;
   depths count ancestors). Core-size conservation banked (CDK5L-A). PASS.
D. **c=0 with q>0.** Impossible: same key as prev KEEP ⇒ B still rooted there
   (DELETEs freeze B) ⇒ d_B=0. PASS.
E. **Two exceptions.** S1-H3 pins exactly one j*; verifier asserts unique
   (H=1,q=3,w=1,R=0) interval on controls. PASS.
F. **Successor double-spend.** Pair inequality charged once; successor never
   recharged as singleton (partition + §9 enforcement). PASS.
G. **w_k=1.** Covered: w_*+w_k≤2≤R_*+R_k for q_k≤3 (w_k∈{−2..1}). PASS.
H. **K/P overlap.** One inequality per interval; H fixed. PASS.
I. **DELETE count.** Unbounded; H sums exact. PASS.
J. **Hidden aggregate.** Hypotheses are per-interval costs/geometry; no total
   inequality assumed (Q_B≤2C_K explicitly refused). PASS.
K. **AM-G misclassification.** K5-local-pass affirmed AND global-fail via K3
   proved; neither direction misstated. PASS.
L. **Fixture contamination.** SHA gates accept ff156d94/753bb211, reject c920…;
   indexed guards pass. PASS.

No defect. Promotion may proceed.
