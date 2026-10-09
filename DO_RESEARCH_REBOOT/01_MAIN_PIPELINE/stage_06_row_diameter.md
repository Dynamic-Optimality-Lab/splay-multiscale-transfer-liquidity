# Adjusted ROW-DIAMETER

**THEOREM ID:** ROW

**NAME:** Adjusted ROW-DIAMETER

**EXACT STATEMENT:** For every BST B and r!=x, H_r(B)−H_x(B)>=−2+2(b_r−b_x) under one shared J; equivalently diameter(H−2b)<=2.

**QUANTIFIERS:** Every finite valid BST, every ordered distinct node pair, all depths/sizes.

**CONSTANTS:** 2 adjusted width; raw root/nonroot range[0,4].

**DEFINITIONS:** H source-defined; b_y=[root(B)=y]; j/rho globally shared.

**PREREQUISITES:** Construct shared admissible assignment; same-child, cross-child, root/child cases and bases.

**KNOWN PROOFS:** REBOOT-01 removes sibling variation for equal-signature same-child pairs only.

**KNOWN FINITE EVIDENCE:** Finite SELF/DIAM LPs; no universal extrapolation.

**KNOWN COUNTEREXAMPLES:** Absorbed H with J=0 reported refuted for row switch; unrestricted J not refuted.

**UNVERIFIED ASSUMPTIONS:** All remaining bases/cases/global compatibility.

**CURRENT STATUS:** OPEN

**SOURCE LOCATIONS:** scripts/wp6_j4shared.py:125-150; 02_PROVED/J4_CONDITIONAL_SUFFICIENCY.md.

**HOW IT ADVANCES DO:** Pays A-root row switching in the sufficient residual potential.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
