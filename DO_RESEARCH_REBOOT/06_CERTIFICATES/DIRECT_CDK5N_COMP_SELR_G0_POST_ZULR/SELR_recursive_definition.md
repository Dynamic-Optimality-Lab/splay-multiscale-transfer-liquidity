# SELR recursive C24* soundness and completeness

Definition: C_0^24 = Rot(B_24) ∪ Z (zero-cost exactly closed leaves);
C_{k+1}^24 = C_k^24 ∪ CycAdd(C_k^24); C24* = union over k. Engine
(SELR_recursive.cover24): root rotation + bank24 base (all 24 domains at
EVERY level) + exhaustive simple-path enumeration over all pair-equal
segmentations with minimax-depth canonical choice; exact (start,canon)
memo keys; every child strictly shorter with exact additive costs;
certified zero-cost leaves only (A=0,Q=0 single-key).

Soundness (induction on proof depth): base cases are exact bank24 domain
hits on exactly closed replayed segments or certified zero-cost leaves;
inductive steps compose strictly shorter exactly closed children with
exact additive A/Q, so a covered root satisfies the same closure and
accounting. No step widens the word or borrows credit.

Completeness (relative to the frozen calculus): for each rotation, ALL
proper pair-closed segments are enumerated (pair-equality classes complete
by construction from the replayed pair sequence); every valid partition
into covered children is considered (Bellman-Ford over the full covered
edge set); recursion descends on all of them with child-specific reachable
starts/rotations/support/core. A fixed depth cap is not used for
completeness (CAP24 is a resource guard whose hit is INDETERMINATE, never
a negative). A missing recognizer yields battery-none INDETERMINATE, never
uncovered.

Primitive shortcut: certified complete pair-state distinctness (31/31 IN,
30/30 OUT) implies no nonempty proper exactly closed cyclic subwalk, hence
no proper additive decomposition exists at the root; with all direct
rotations excluded, noncoverage is established.
