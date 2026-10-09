# Same-row transport

**THEOREM ID:** J-SELF

**NAME:** Same-row transport

**EXACT STATEMENT:** H_x(B)−H_x(S_xB)>=R_static(B,x)−2(1−b_x), for every B,x under the same globally shared J.

**QUANTIFIERS:** All finite valid BSTs and present x; root case included.

**CONSTANTS:** Kappa4; root correction2.

**DEFINITIONS:** S_x ordinary splay; b_x indicates old B root.

**PREREQUISITES:** Source mechanics, shared all-size row assignment compatible with DIAM.

**KNOWN PROOFS:** Source reports absorbed H0 self-control; joint all-size witness not constructed.

**KNOWN FINITE EVIDENCE:** Generated finite rows and LP checks only.

**KNOWN COUNTEREXAMPLES:** No general self theorem for an unknown joint witness; arbitrary assignments need not satisfy it.

**UNVERIFIED ASSUMPTIONS:** Joint compatibility with ROW; source mechanics formal closure.

**CURRENT STATUS:** OPEN as joint admissibility obligation

**SOURCE LOCATIONS:** scripts/wp6_j4shared.py:94-117; audits/PIVOT_CONSTRAINT_GUIDED_DUAL.md:1310 onward.

**HOW IT ADVANCES DO:** Pays pointed-B splay transport; combining with ROW pays KEEP/DELETE.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
