# Cycle-to-prefix

**THEOREM ID:** PIVOT-2

**NAME:** Cycle-to-prefix

**EXACT STATEMENT:** If every reachable closed pair walk has B<=3A, then every present prefix satisfies E_B<=3S_A+g(T0).

**QUANTIFIERS:** Every finite K,T0 and every finite present-legal KEEP/DELETE history from (T0,T0).

**CONSTANTS:** 3; conservative g=(Cat_n^2−1)floor(n/2). Source g is maximum simple-path reward.

**DEFINITIONS:** Reward W=B−3A additive; pair graph has at most Cat_n² states.

**PREREQUISITES:** Nonpositive reachable cycles; finite fixed key universe.

**KNOWN PROOFS:** 02_PROVED/PIVOT2_CONDITIONAL_REDUCTION.md.

**KNOWN FINITE EVIDENCE:** Small graphs source-reported; not necessary to prove conditional excision.

**KNOWN COUNTEREXAMPLES:** A positive reachable cycle refutes any tree-only bound at that C.

**UNVERIFIED ASSUMPTIONS:** Universal cycle premise; formal list-excision assembly not completed.

**CURRENT STATUS:** CONDITIONAL

**SOURCE LOCATIONS:** audits/PIVOT_RECURRENT_EXCESS.md:12-20; scripts/wp6_cycle_ratio.py:58-100.

**HOW IT ADVANCES DO:** Moves closed-cycle counts to the full sequence comparison.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
