# Fixed HIGH truncation cannot be extended by enlarging the core alone

## Precise theorem

Fix any integer C>=1. Consider the proposed unrestricted analogue of the
current macro simulation: each macro ends at the next genuine KEEP, preserves
its original terminal q, maps full paired closure to full abstract closure,
and assigns HIGH weight2C-q whenever H>=C. Such a graph covering all original
closed walks cannot have nonnegative cycles. This is an obstruction to this
particular sign proof, not to unrestricted CD.

For the current HIGH price6-q, take C=3. The frozen nine-core graph is not
changed, compiled, or claimed to contain the larger-core cycle below. The
theorem concerns the attempted enlargement with the same price rule.

## All-size node-count argument

A binary tree whose maximum edge-depth is at most d-1 has at most2^d-1 nodes.
Proof by induction on d: level j has at most2^j nodes; summing gives2^d-1.
Consequently every n-node BST with n>=2^d has a node at depth exactly d: some
node has depth>=d, and its depth-d ancestor supplies one. This is a universal
counting argument, not enumeration of n-node trees.

Set d=4C+2 and choose any finite ordered key set of size n>=2^(4C+2). On each
BST choose deterministically the least key at depth exactly d and KEEP it.
Run this policy from any diagonal (T,T). Both trees remain identical, every
access is present and nonroot, and after every step the result is another
n-node BST. There is always a next depth-d target by the node-count argument.

There are only Cat_n BSTs on this fixed ordered set. Iterating the deterministic
policy therefore has a finite reaching prefix followed by a fully closed
period of length ell>=1. No enumeration, orbit, or finite instance is executed
here. Both full labeled trees repeat because they are identical throughout;
the periodic paired walk is source-valid and diagonally reachable.

Every occurrence in that period has

    d_A=d_B=4C+2,
    a=H=ceil((4C+2)/2)=2C+1,
    q=floor((4C+2)/2)=2C+1.

Each KEEP is genuinely B-changing. There are no intermediates or DELETEs, so
each original next-genuine-KEEP macro consists of exactly this one access.
The hypothetical preserved HIGH rule gives, term by term,

    w_HIGH=2C-(2C+1)=-1,
    sum w_HIGH=-ell<0.

Mapping the full period with closure preserved would produce a negative
surrogate closed walk. No state potential can make every such surrogate edge
nonnegative after adjustment, because its differences sum to0 on that period.

By contrast the ORIGINAL CD weight at each occurrence is

    2a-q=2(2C+1)-(2C+1)=2C+1>0.

Thus the actual period has A=Q_B=(2C+1)ell and Q_B<=2A with positive slack.
There is no negative original CD cycle and no refutation of CD(5) or M3.

## Exact current specialization and scope

For C=3: d=14, q=H=7, surrogate weight-1, actual CD weight7. Every n>=2^14
admits such a reachable closed periodic walk. Notice q7 is within the current
declared q<=9 range; the missing feature is core/support, not a new high-depth
sentinel convention. If r is its genuine support size, the reused core bound
|S|<=2r-1 and a marked access path of15 nodes imply r>=8. Hence it lies beyond
the sealed CD(5) domain. It is not an example in the frozen nine-core graph.

The proof is existential via deterministic finite-map recurrence, not an
explicit machine-listed negative cycle and not an executed search. It is a
universal analytic obstruction to a hypothetical forward image with the stated
price/segmentation rules. Changing macro grouping, restoring full2H-q, or adding
other information would require a separately justified strategy; none is
silently assumed here. No compiler, graph, h, coordinate, observable or cap is
modified. The source/saturation constraints of the original frozen graph are
not asserted to cover arbitrary larger cores.

This deletes the naive inference that a uniform extension of M3 with the same
fixed HIGH truncation will automatically prove unrestricted CD. It does not
delete the unrestricted signed support-lifting obligation.
