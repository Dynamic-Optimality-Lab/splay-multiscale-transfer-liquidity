# Dynamic Optimality

**THEOREM ID:** DO

**NAME:** Dynamic Optimality

**EXACT STATEMENT:** Exists c>=1 independent of K,T0,X such that LT(X,T0)<=c OPT(X,T0).

**QUANTIFIERS:** Every finite ordered key set, valid initial BST and finite present-key sequence. Empty sequences included.

**CONSTANTS:** Universal c; no final additive term.

**DEFINITIONS:** LT is splay transition-tree/access-path cost; OPT is offline optimal transition-tree execution from the same T0.

**PREREQUISITES:** Universal eventual monotonicity plus L3 v3 reduction.

**KNOWN PROOFS:** External reduction only; no proof of the premise.

**KNOWN FINITE EVIDENCE:** Finite pair bounds do not prove DO.

**KNOWN COUNTEREXAMPLES:** No exact counterexample to DO established here.

**UNVERIFIED ASSUMPTIONS:** All universal upstream inequalities.

**CURRENT STATUS:** OPEN

**SOURCE LOCATIONS:** Local L3 pp.3-5,9-10; math/theorems/MSTL-19.md historical blocked ledger.

**HOW IT ADVANCES DO:** Final original target.

**STAGE COMPLETION:** A complete proof of the exact statement on its claimed domain, linked to established premises. Conditional conclusions stay conditional until all essential premises are discharged.

**PROOF VERIFICATION:** Check model/cost correspondence, all quantifiers/constants, empty/small cases, both orientations, signs, shared coordinates and noncircular dependencies. Bind actual working bytes. Formal-kernel certification is a separate recorded attribute; no unrun compiler result is claimed.
