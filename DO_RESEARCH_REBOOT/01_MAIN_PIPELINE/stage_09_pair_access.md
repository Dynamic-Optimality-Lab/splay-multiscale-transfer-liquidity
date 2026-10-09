# Pair Access representation

**THEOREM ID:** PA

**NAME:** Pair Access representation

**EXACT STATEMENT:** A_i equals full-X splay prefix; B_i equals retained-Y splay prefix, keys both remain K.

**QUANTIFIERS:** All finite present-key histories, T0, occurrence-index masks, repeated keys.

**CONSTANTS:** No competitive constant; exact encoding.

**DEFINITIONS:** KEEP splays both; DELETE splays A only; shared initial T0.

**PREREQUISITES:** Ordinary splay preserves keys and order.

**KNOWN PROOFS:** Induction on occurrences, following definitions; mapping source gives C1-C3.

**KNOWN FINITE EVIDENCE:** Differential replay tests source-reported, not universal proof basis.

**KNOWN COUNTEREXAMPLES:** Value-set masks fail with duplicates; absent-key route is a different domain.

**UNVERIFIED ASSUMPTIONS:** No missing encoding premise on present domain.

**CURRENT STATUS:** PROVED universal mathematical encoding

**SOURCE LOCATIONS:** artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md:1-42; IMPLEMENTATION_SPEC...v0.4.txt:256-280.

**HOW IT ADVANCES DO:** Links pair histories to the original LT subsequence target.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
