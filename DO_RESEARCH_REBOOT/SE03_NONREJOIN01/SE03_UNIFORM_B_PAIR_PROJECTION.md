# Exact full and erased B projection on one fixed labeled core

This is a representation lemma, not a signed repayment theorem. It extends
the inherited pruning argument to the ALIGNED PAIR of B histories while
retaining every original core label. No finite quotient completeness is
assumed and no frozen graph is enlarged.

Let gamma be original, reachable and fully closed, with M=G nonempty and
fixed labeled full B-core S, c<=2|M|-1. At its starting boundary every
component hanging off S is a rigid BST with no key of M. Regard each as
an exact term F_i in one of the inorder gaps of S. All original B targets
are in M subset S. After erasing z, all erased B targets remain in S.

Every search to a key of S stays on S vertices: a component F_i contains
no S vertex and hence cannot lie on such a search path. Every rotation
therefore has both pivot operands in S, with the F_i moved only as intact
subtrees. Induct on either history's operations. All S labels remain in
the raw skeleton, even if some cease to lie in the smaller retained core.
Every F_i retains its internal shape and its fixed inorder gap. DELETEs
and erased Kz are B identities in the appropriate history.

Thus pruning only the ORIGINAL F_i commutes with EVERY operation of both
histories, preserves all queried pre-depths and charges, and represents
both raw B states by BSTs on the SAME at-most2r-1 labeled vertices S.
Do not prune the erased history to a changing smaller core and then share
its coordinates with the full history; all original labels S are retained.

Conversely each actual skeleton state uniquely determines its full tree
after substituting the fixed F_i in inorder order. Exact equality of
skeleton endpoints therefore implies equality of the full labeled B trees,
with all arbitrary F_i restored. Closure in the skeleton is source-full
closure, not just agreement of roots or queried depths. This statement
applies to the actual projected histories; no claim is made that every
arbitrary pair of S-BSTs is diagonally reachable with the actual A tree.

The erased recurrence lives on this common c-label skeleton. Its own
marked core is a subset of S and has size<=2r-3 on its closed recurrent
block. The original full core is constant; the erased raw skeleton still
contains all c labels, including its private unaccessed S nodes.

This removes arbitrary B fringe inventories from discrepancy transport
without changing source semantics. It does not remove unbounded r, the
ordered arrangements of S, or anonymous nodes encountered by A-only
requests. A must retain its real source trajectory and full closure.
No uniform J formula follows merely from this complete B representation.
