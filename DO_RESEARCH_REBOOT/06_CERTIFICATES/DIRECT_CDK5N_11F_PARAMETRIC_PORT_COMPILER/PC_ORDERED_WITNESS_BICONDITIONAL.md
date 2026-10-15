# PC_ORDERED_WITNESS_BICONDITIONAL.md — G06/G07 (reconstruction biconditional, hidden-S, same-gap order)

## Soundness (assignment -> completion)
Given satisfying `JointInventoryValid` + wellformed prefix: per port, order hidden-S ints (V-positions
from fullrank) with anonymous markers (atom/gap order); balanced build per port; Fill into exposed
skeleton. Verified per instance: inorder strictly increasing under true order; per-gap counts exact;
S-cover exact; empty ports empty. B-side: core skeleton + per-gap balanced fringe blocks from `sig`
(valid B-tree, exact gap counts, gap slots at valid NULL spans).

## Completeness (completion -> assignment)
Given valid canonical completion: cut at depth 6 (ports exact), read hidden-S per port (exact scan),
count per-cell fringe (cells partition hidden keys), exposed counts from prefix scan, `sig` = totals,
nonempty derived. Predicate checks pass by construction. 600/600 predecessor; production V8 138/138
grounded (each grounded SAT model IS a completeness instance: concrete -> satisfying assignment).

## Hidden-S placement (G06)
Strict intervals (inclusive-lo/exclusive-hi, matching slot bound semantics); fullrank order across
exposed+hidden; S-uniqueness (exact-once cover); no core key in two ports (cover counting);
anonymous keys never cross atoms except via the single rotation replay (rotations preserve inorder;
verified by replay equality per edge).

## Same-gap ordering (G07)
Visible same-gap keys (exposed fringe ranks + hidden-S fullranks) split every gap; allocation cells
are (gap,port)-grained with hidden-S exact positions inside; reconstruction sorts by V-position;
multiple anonymous same-gap keys ordered arbitrarily (interchangeable — sound: all orders valid
completions with identical observables); separated-by-visible-keys enforced by strict intervals.

## Gates G06/G07: PASS.
