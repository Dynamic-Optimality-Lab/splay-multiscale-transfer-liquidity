# LT cost comparison

**THEOREM ID:** LT-7

**NAME:** LT cost comparison

**EXACT STATEMENT:** E_B<=3S_A+g(T0) implies LT(Y,T0)<=7LT(X,T0)+2g(T0).

**QUANTIFIERS:** Every present-key X,Y subsequence,T0; same initial tree.

**CONSTANTS:** 7 and 2; more generally 2C+1 and2.

**DEFINITIONS:** e=ceil(d/2); LT=d+1; E_B retained B events, S_A all A events under P_all.

**PREREQUISITES:** Universal prefix bound, |Y|<=|X|, S_A<=LT(X), LT(Y)<=2E_B+|Y|.

**KNOWN PROOFS:** 02_PROVED/COST_TRANSLATION_CONDITIONAL.md; Lean arithmetic source.

**KNOWN FINITE EVIDENCE:** No finite premise used.

**KNOWN COUNTEREXAMPLES:** None for the arithmetic implication.

**UNVERIFIED ASSUMPTIONS:** The prefix inequality remains open.

**CURRENT STATUS:** CONDITIONAL

**SOURCE LOCATIONS:** lean/WP6/GCStaticKeep2Step.lean:703-716; present_domain_mapping.

**HOW IT ADVANCES DO:** Establishes eventual monotonicity in the exact LT model.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
