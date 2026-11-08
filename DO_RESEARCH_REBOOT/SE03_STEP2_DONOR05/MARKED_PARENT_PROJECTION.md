# Exact marked-parent path compression in maximal closed sources

This is a consequence of the new same-side source theorem, not a new
abstract graph and not an identification of full source states.

For a full B boundary let T_B have vertex set M; the parent of a nonroot
mark is its nearest marked B ancestor. It is a rooted tree, though not
necessarily a binary BST on the marked labels. Keep the full B tree,
unmarked separators and all private hangers alongside this proof notation.

During a legal actual B splay, its source path is

    m0,u0,m1,u1,...,u_(q-1),x.

Thus its original double demand q is EXACTLY the marked-parent depth
of target x in T_B. The complete effect on T_B is:

* x becomes root;
* all of its OLD proper marked ancestors become DIRECT children of x;
* every off-path marked vertex keeps its previous marked parent.

For example, in the actual RR frame

    G(A,U(B,x(C,D))) -> x(U(G(A,B),C),D),

G and x are marked and U is unmarked. The marked parents of every mark
root in A/B remain G, and in C/D remain x. G becomes a child of x.
If the source subtree had an outside nearest marked parent H, the old
edge H->G changes to H->x. LL has the same property from its own
source formula. Induction over the original bottom-up doubles proves
the full path-compression statement, with all other marked parents fixed.

IMPORTANT: the undirected marked tree is NOT fixed. Inner doubles can
replace H->G by H->x. Treating q as distance in one immutable reference
tree would therefore be wrong. Also not every marked-tree path is a
legal B source path: the actual separator positions must satisfy the
same-side M-U-M condition. Those physical positions and event IDs are
retained in every source and ownership theorem.

This gives a compact exact description of actual B work for the core11
branch, useful for the remaining A-dependent signed completion. It
does not itself compare that work with A cost, prove a free donor, or
cover deficiency-one core10. No old source row, graph or observable
is modified by this projection.
