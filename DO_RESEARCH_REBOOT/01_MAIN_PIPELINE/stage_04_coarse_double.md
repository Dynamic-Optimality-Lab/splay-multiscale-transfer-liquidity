# COARSE-DOUBLE

**THEOREM ID:** CD

**NAME:** COARSE-DOUBLE

**EXACT STATEMENT:** Q_B(gamma)<=2A(gamma) for every reachable closed present-key pair walk gamma.

**QUANTIFIERS:** All finite ordered K, diagonal start T0, reachable cycles of arbitrary length.

**CONSTANTS:** 2; no startup term on cycles.

**DEFINITIONS:** Q_B counts B doubles; A counts all A StepEvs, including DELETE accesses.

**PREREQUISITES:** Either direct charging, or all-size J-SELF/ROW plus static mechanics and one shared witness.

**KNOWN PROOFS:** Conditional sufficiency reconstructed; no universal proof.

**KNOWN FINITE EVIDENCE:** n<=6 ratios and n<=9 coarse BF reported; finite only.

**KNOWN COUNTEREXAMPLES:** Q_B<=A is a different stronger refuted candidate; Q_B<=2A not refuted here.

**UNVERIFIED ASSUMPTIONS:** Global witness/row inequalities or another universal mechanism.

**CURRENT STATUS:** OPEN

**SOURCE LOCATIONS:** audits/PIVOT_COARSE_DOUBLE.md; PIVOT_DUAL_UNIVERSAL.md; scripts/wp6_j4shared.py.

**HOW IT ADVANCES DO:** Nearest original load-bearing cycle inequality.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
