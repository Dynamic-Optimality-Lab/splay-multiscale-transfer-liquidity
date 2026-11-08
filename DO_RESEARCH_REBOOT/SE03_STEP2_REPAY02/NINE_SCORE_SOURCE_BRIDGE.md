# Reusing M3 on a fixed nine-Score source tree

This is a local source embedding into the UNCHANGED original graph, not
an extension of that graph to ten or eleven Scores.

Choose nine actual present keys S forming a rooted ancestor-closed subtree
of B and five actual marked keys M0 subset S. Suppose all KEEPs in a source
segment target M0. A is arbitrary; its DELETEs may target any present key.
At each KEEP boundary A and B have the same marked root. S need not equal
the exact ancestor core C_M0; it may contain an unmarked Score leaf.

All B operands of a KEEP are in S, because its entire root-to-target path
is in S. Every component outside S has no Score, is never entered by B,
and stays rigid. Rotating only Score operands preserves an ancestor-closed
nine-Score tree with exactly the same labeled keys and Score-free gaps.
Pruning those gaps therefore commutes with the actual B replay. The actual
terminal B double cost is its Score-tree cost and is at most4.

The original predicates support precisely this local representation.
state_valid7 imposes popcount5, B validity, signature bounds and alpha
types. b_tree_valid imposes parent/ordered-tree/gap validity; it takes no
mu argument. Neither predicate asserts that every unmarked Score has a
marked descendant. build_slow imposes terminal Score/marked target,
same_keep_target, exact A/B replay, root synchronization, compatibility,
and no intermediate genuine KEEP. It does not add such a descendant test.
These source definitions were read, not imported, instantiated or executed.

The sealed arbitrary-fringe local source/witness proof needs the fixed
nine Scores, ordered gaps and Score-only B target paths. Those properties
hold here. Its bounded representation is per macro, not a population cap;
the accepted debt is independent of private inventories. Thus a genuine
macro with H<=2 maps to the same original LOW edge of price2H-q and the
same full canonical ordinary endpoints. All remaining source operations
and the original H1/H2 normalization are retained. No new edge is added.

For H>=3, q<=4 makes6-q>=2. The range0<=D<=2 itself gives

    6-q+D(after)-D(before)>=0.

This step does not need chi constancy, a new HIGH simulation, or an
assumption that the B segment closes. LOW uses its sealed chi conservation
and signed D law. Hence on every genuine fixed-Score macro, including open
source segments,

    2min(H,3)-q+D(after)-D(before)>=0.                  (1)

This supplies the uniform endpoint bound2A-Q>=D(start)-D(end)>=-2
when the segment starts/ends at synchronized KEEP boundaries. Nongenuine
retained gaps are handled exactly as RETAINED_GAP_RESERVATION.md: H0 is
an identical actual state; a positive root-return gap has H>=2 and price2
is range-safe. No scalar CD(5) theorem is applied to an unclosed word.

The full original raw graph, midpoint scopes, signatures, fields, h0 case,
and its existing certificate remain unchanged. The bridge uses a subset
of its already certified valid witnesses; it never assumes an eleven-node
controller or samples a finite source population.
