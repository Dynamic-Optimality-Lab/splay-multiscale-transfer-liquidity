# Pruning commutation (PROVED for x∈M)

**Claim.** Core_M(S_x(B)) = Core_M(S_x(Core_M(B))) as labeled BSTs (right side
may drop new unmarked-only hangers; in fact none arise since rotations create
no nodes — both sides have exactly the core-node keys).

**Proof.** The root→x path lies in Core_M(B) (x marked). Every rotation's pivot
nodes are path nodes (in core); hanging children containing marks are on marked
paths (their roots are ancestors of those marks ⇒ in core); mark-free hanging
subtrees are absent on the right (pruned) and ride rigidly on the left.
Rotation orientation (left/right) depends only on path shape and key comparisons
among path nodes — identical on both sides since path keys/geometry agree.
Induction over the bottom-up StepEvs: after each StepEv, the core-node-labeled
subtrees agree (path nodes permuted identically; marked hangers reattached at
identical structural positions; pruned hangers reattached mirror-symmetrically
on the left and dropped on the right). Marked depths agree: ancestors of marked
keys are all in the core (ancestor of a mark ⇒ on its root path), so pruning
removes no ancestor of any mark, and depths count only core nodes on both sides.
Parent-child geometry among marked keys and LCA structure agree for the same
reason. BST validity of the pruned input holds (deleting whole subtrees keeps
order). ∎

**Scope.** Only x∈M is needed or claimed (all reduced-core transitions in §7
use marked accesses, matching KEEP keys ⊆ M). Unmarked-x commutation is not
asserted.
