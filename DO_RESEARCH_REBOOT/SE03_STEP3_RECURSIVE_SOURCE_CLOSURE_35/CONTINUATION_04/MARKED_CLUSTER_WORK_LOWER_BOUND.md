# MC35 — source work lower bound independent of unary inventories

For any original A tree let J_M(A) be the SET of nonempty marked-descendant
sets of its nodes. Each member is a contiguous interval of ordered M.
Mark-free nodes contribute nothing. An unmarked unary core node has the
same marked-descendant set as its sole marked-carrying child, so pruning
mark-free hangers and contracting unmarked unary nodes leaves J unchanged.
Thus J is exactly computable from the retained branch quotient.

One ordinary SINGLE rotation changes only the descendant sets of its
pivot and promoted child (inherited AR1). The old pivot's complete marked
set becomes the promoted child's new set; the promoted child's old set
may disappear and the demoted pivot's new set may appear. Every other
node's set is unchanged. After ignoring empty sets and duplicates, at
most ONE member of J is removed and at most ONE is added.

Consequently any original source interval from s to t containing R actual
single rotations satisfies

 max(|J(s) minus J(t)|, |J(t) minus J(s)|) <= R <= 2H.

The last inequality uses every actual A StepEv, with zig one rotation and
double two. Root repeats contribute zero and are retained. Therefore

 H >= ceil(max(lost_clusters,gained_clusters)/2).

This theorem is uniform in support, source length, unary populations,
private BSTs, helper targets, charts and orientation. It is a necessary
SOURCE work bound, not a debt formula involving distance(A,B), and is
not the previously refuted rotation-distance geometric debt. No donor
is inferred solely from this lower bound until actual unowned A-bit
locations and ownership are supplied by a funding construction.
