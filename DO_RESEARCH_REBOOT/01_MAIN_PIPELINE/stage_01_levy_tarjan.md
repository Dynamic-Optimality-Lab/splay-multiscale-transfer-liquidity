# Levy–Tarjan reduction

**THEOREM ID:** LT-RED

**NAME:** Levy–Tarjan reduction

**EXACT STATEMENT:** If Splay is eventually monotone then Splay is dynamically optimal (v3 Theorem4.3).

**QUANTIFIERS:** All finite instances (X,T0), all occurrence subsequences Y, one universal monotonicity factor and tree-only startup overhead.

**CONSTANTS:** Input factor b universal; g(T0) integer-valued. This paper does not set the project factor7.

**DEFINITIONS:** Eventual monotonicity allows cost(Y,T0)<=b cost(X,T0)+g(T0).

**PREREQUISITES:** Splay-specific coercibility/repeatability supplied by the paper; exact cost/domain correspondence.

**KNOWN PROOFS:** Published v3 Theorem4.3 pp.9-10; Theorem3.5 covers the zero-overhead case.

**KNOWN FINITE EVIDENCE:** None needed for the external implication.

**KNOWN COUNTEREXAMPLES:** No refutation of the reduction; crossing lower bounds do not discharge its premise.

**UNVERIFIED ASSUMPTIONS:** Project universal eventual bound; original v1/L2 ledger gates not silently replaced.

**CURRENT STATUS:** CONDITIONAL application; established external theorem

**SOURCE LOCATIONS:** v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf; prereg/bridge_manifest.yaml; https://arxiv.org/html/1907.06310v3

**HOW IT ADVANCES DO:** Converts the completed LT subsequence bound to the final conjecture.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
