# SELRP corrected recursive C24* definition (rotation-aware base)

C_0^24 = Rot(B_24) ∪ Z: every exactly closed subword is first tested at
ALL n whole-cycle rotations (true boundary starts, fresh replays,
closure verified, all 24 predicates + zero-cost basis per rotation).
Z = certified zero-cost exactly closed leaves (A=0,Q=0,single key).
C_{k+1} = C_k ∪ CycAdd(C_k): valid compositions partition the parent
into ≥2 proper nonempty exactly closed children (actual child starts,
exact additive A/Q, strictly shorter). C24* = union over k.

Soundness (induction on depth): rotated bank bases prove Q≤2A per their
promoted theorems on the actual replayed subwalk; Z leaves are
universally valid; additive steps preserve exact costs. Hence COVERED ⇒
Q≤2A for the parent walk. Engine: SELRP_recursive_checker.coverP
(DP over pair-closed boundaries); independent: SELRP_alt_checker.coverA
(top-down DFS enumeration). Shared (disclosed): replay_from/canon,
bank24_checked semantics, memo key format.

Completeness (relative to calculus): all rotations as bases at every
level; all proper pair-closed segments; all valid partitions; nested
finite proofs; child-specific states/rotations/support/core; Z leaves.
Finite subword states per fixed word (strictly shorter children). Depth
caps are resource guards (INDETERMINATE), never completeness. Missing
recognizers/unknowns propagate INDETERMINATE (bank24_checked coerces only
exact bools; None/exception/malformed ⇒ unknown).

Primitivity connection: n distinct pre-closure states ⇒ no proper
closed child at any rotation ⇒ recursion reduces to the rotation census;
with all rotations excluded ⇒ UNCOVERED (both witnesses: 31/31, 30/30,
744+720 EXCLUDED, 15/15 cross-validation).
