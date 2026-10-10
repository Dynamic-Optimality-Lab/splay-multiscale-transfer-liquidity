# Interval partition lemma (PROVED — exact identities with cyclic seam)

Cyclic KEEP list K_1..K_s (s≥1; s=0 impossible with five genuine keys).
I_j = accesses strictly after KEEP j−1 (mod s) through KEEP j inclusive.

- **Disjoint cover.** Every full-word occurrence has a unique preceding KEEP
  (cyclically), hence belongs to exactly one I_j. The seam (last→first) is an
  ordinary interval by cyclic indexing; exact closure makes start=end consistent.
- **ΣH_j=A.** H_j sums a_t over I_j; partition ⇒ sum is A. DELETE StepEvs counted
  once (each DELETE lies in one I_j). No double-count by construction.
- **Σq_j=Q_B.** KEEP q's (DELETEs q=0, whether inside intervals or not — all
  accesses are inside some interval, so nothing is silently excluded).
- **Σc_j=C_K.** c_j is the cyclic KEEP-word change indicator by definition.
- Hence **Σw_j=Q_B−2C_K**, **ΣR_j=2(A−C_K)**. C_X is never substituted for C_K;
  DELETE StepEvs are counted exactly once in H_j (never duplicated).
