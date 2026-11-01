# Route C analytic continuation — uniform identity and exact obstruction

Started 2026-10-30; completed following the updated client date 2026-10-31, Asia/Karachi.

**Uniform source rotation transport is proved. It does not yet extend the seven-key potential to a universal signed invariant.**

For a B right rotation of child x over parent p, with outer subtrees L=x.left and R=p.right, and H the complete joint A/B depth polynomial,

    Delta H = (w^{-1}-1)(e_x+H_L)+(w-1)(e_p+H_R).

The middle subtree contributes zero. For A rotations replace w by z. The exact LL/RR/LR/RL transport table is in RA01, derived in source order with arbitrary hanging profiles.

The decisive analytic test is an arbitrary-fringe family of zero-weight helpers. Two source pairs have the same n, roots, COMPLETE joint-depth histogram, accessed key and costs dA1,dB4,a1,q2. Their successor histograms differ by

    HR-HL=(w-1)[C+z^2*w^2*(z-1)],

where C is the profile of an arbitrary paired fringe. The two possibilities come from LR/LL versus LL/LL bottom-up B rotations. This refutes a deterministic histogram-only successor recurrence. It does NOT refute an arbitrary nonlinear histogram potential that handles both successors.

For a fringe with m nodes, both helpers have Delta D_A=-1; their B total-depth changes are -6 and m-6. Hence ANY fixed positive B-depth coefficient plus a uniformly bounded joint correction fails the required inequality for large enough m. RA03 gives the full all-size proof and its precise limits. An unbounded nonlinear repair or a different structural potential remains possible.

Verification:16 prescribed whole-access controls,48 exact StepEv profile identities covering both zigs and all four double orientations, two fully closed physical six-key walks, and independent polynomial/source replay all PASS. Existing Phi7 values were only READ at the m=1 points: -2->-3 on both branches. No finite fit, graph enlargement, solver invocation or Stage11G edit occurred.

The four-rule audit is preserved in RA00 and RA04. The unresolved universal step is an explicit F with signed bounds for all legal profile transports. The identity alone is not such a bound; no equivalent conjecture is substituted. Universal Coarse-Double and Dynamic Optimality remain OPEN.

Primary files: RA01_UNIFORM_ROTATION_IDENTITY.md; RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md; RA03_UNIFORM_MOMENT_REPAIR_OBSTRUCTION.md; RA04_NECESSARY_PROFILE_TESTS_AND_GATE.md; profile_transport_controls.json; six_key_closed_controls.json; independent_audit.json; proof_status_ledger.json; final_integrity.json.
