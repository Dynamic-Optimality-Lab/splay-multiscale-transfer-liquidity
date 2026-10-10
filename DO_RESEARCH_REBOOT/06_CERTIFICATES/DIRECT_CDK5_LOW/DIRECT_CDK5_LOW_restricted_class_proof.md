# Phase 6: CDK5-LOW restricted-class proof (PROVED)

Let W be source-valid, reachable, exactly closed with |supp(KEEP)|=5 (M) and
|Core_M(B_t)| ≤8 at every cyclic state. Arbitrary n, length, KEEP order, DELETEs.

**Projection.** Each KEEP (marked x∈M) projects by pruning commutation
(banked, arbitrary M) to a retained graph edge U→U' (valid cores; depths, root,
q agree; coordinate compression preserves comparisons hence dynamics). DELETEs
freeze B/U. Real closed B-cycle ⇒ closed projected vertex sequence (exact B
closure ⇒ same core ⇒ same compressed vertex; η returns).

**Telescoping.** Sum certified w+Δη≤0 over the projected closed walk:
Σw_t = Q_B − 2C_K ≤ 0 (1[x≠root] = KEEP-change indicator by linearizing at a
KEEP boundary, seam by closure; DELETEs contribute 0 to both sums). Hence
**Q_B ≤ 2C_K** on the class.

**A-side (banked).** C_K ≤ C_X ≤ A (subsequence contraction + per-change StepEv
charging, exact A seam). Therefore **Q_B ≤ 2C_K ≤ 2C_X ≤ 2A**. Zero-A walks
agree with the banked zero-A theorem. No finite-n residue: n entered only via
the all-size reduction; the certificate covers every projected edge.

**Boundary.** Nine-node five-key states are outside the class by definition;
the Phase-5 witness (core 9, Q−2C_K=+2) confirms the boundary is load-bearing
and that no B-only claim is made there. With CDK4-A: ≤4-key classes banked;
CDK5-LOW adds the five-key ≤8-core layer. Five-key nine-core, K≥6, universal
Coarse-Double, DO remain OPEN.
