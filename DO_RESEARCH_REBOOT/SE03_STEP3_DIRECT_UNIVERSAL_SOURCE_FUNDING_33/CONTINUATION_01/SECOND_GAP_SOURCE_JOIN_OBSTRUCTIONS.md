# Why the end-gap projection does not extend by a generic join

PROVED for three explicit candidate joins; see
second_gap_join_independent_audit.json (verify53). The physical key inventory
is ten old anchors 2,4,...,20 and the single private key 5, in the second gap.
Every original packet is an actual H1/Q2 genuine access, with price0.

The predecessor join attaches the projected right tree to the maximum of
the left tree without rearranging the left tree. The nearest-root join
recursively chooses the nearer of the two current roots (left on ties).
The smaller-side join recursively chooses the side with fewer old anchors
(left on ties). These are contractions only for evaluating debt; they never
remove a physical key or an original operation.

All three rules have a source-valid transition with old debt1 -> 0, hence
signed margin -1. Nearest-root uses BF651, target physical key10. The other
two fail on the same source with BF8944, target physical key2. Full source
words, common initial A/B/BE trees, all original operation rows and exact
paired-closed charts are in second_gap_nearest_root_closed_source.json and
second_gap_predecessor_closed_source.json. The distinct checker reconstructs
the joins with an iterative zipper, uses a separate mutable splay engine,
and composes every remaining operation from accepted complete source bases.

This refutes these join rules, not every geometry-aware projection, not
the independently proved end-gap theorem, not Coarse-Double. In particular
the complete unary-boundary theorem handles all gaps by a different source
condition; it does not assert that branchers can be erased for free.

Two further extremal full-contraction selector failures are recorded only
as raw discovery in extremal_full_geometry_contraction_candidates.json.
Their new explicit closed-source checks have not been completed. Do not
promote those raw candidates to additional certified counterexamples.
