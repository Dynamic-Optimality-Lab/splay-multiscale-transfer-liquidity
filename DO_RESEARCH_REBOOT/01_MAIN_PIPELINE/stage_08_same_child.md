# SAME-CHILD

**THEOREM ID:** SC

**NAME:** SAME-CHILD

**EXACT STATEMENT:** For all B=[p,T,S] (or mirror), u!=v in T, |D_J(B;u,v)|<=2 under the same admissible J.

**QUANTIFIERS:** Arbitrary T,S, row depths, pairs and both orientations, globally shared J.

**CONSTANTS:** 2.

**DEFINITIONS:** D_J=R(v)−R(u)+4(subsize(v)−subsize(u))+J_u−J_v.

**PREREQUISITES:** Base width and global assignment; other structural cases needed for full ROW.

**KNOWN PROOFS:** Equal-signature sibling erasure proved; full width not proved.

**KNOWN FINITE EVIDENCE:** 19,404 row formulas and2,232 erasure pairs exactly checked; supporting only.

**KNOWN COUNTEREXAMPLES:** Different signatures give different insertion atoms, so no automatic cancellation.

**UNVERIFIED ASSUMPTIONS:** Arbitrary-T empty-sibling bases, unequal depths/folds, global compatibility.

**CURRENT STATUS:** OPEN; restricted reduction PROVED

**SOURCE LOCATIONS:** 02_PROVED/REBOOT_01_SIBLING_ERASURE.md; scripts/wp6_context.py/context2.py; j4shared.py.

**HOW IT ADVANCES DO:** Closes one part of nonroot row diameter once the actual width is proved.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
