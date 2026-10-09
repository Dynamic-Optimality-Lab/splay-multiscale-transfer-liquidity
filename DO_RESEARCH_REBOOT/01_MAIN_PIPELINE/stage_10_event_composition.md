# B<=3A composition

**THEOREM ID:** SUM

**NAME:** B<=3A composition

**EXACT STATEMENT:** If Q_B<=2A and Z_B<=A on a closed walk, then B=Q_B+Z_B<=3A.

**QUANTIFIERS:** Every walk satisfying those two bounds; constants shared universally.

**CONSTANTS:** 2+1=3.

**DEFINITIONS:** Each B event is a double or terminal zig.

**PREREQUISITES:** COARSE-DOUBLE + C.ZIG + exact event decomposition.

**KNOWN PROOFS:** Termwise e=q+z and summation; elementary arithmetic.

**KNOWN FINITE EVIDENCE:** Not needed for implication.

**KNOWN COUNTEREXAMPLES:** None for the arithmetic implication.

**UNVERIFIED ASSUMPTIONS:** Universal Coarse-Double remains open.

**CURRENT STATUS:** CONDITIONAL conclusion

**SOURCE LOCATIONS:** audits/PIVOT_COARSE_DOUBLE.md:1-6; GCStaticKeep2Step.lean:779 onward decomposition.

**HOW IT ADVANCES DO:** Supplies nonpositive reward cycles for PIVOT-2.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
