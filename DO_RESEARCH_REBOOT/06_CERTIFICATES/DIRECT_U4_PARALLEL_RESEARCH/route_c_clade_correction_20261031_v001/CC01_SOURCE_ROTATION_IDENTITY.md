# Subtree key set identities for source rotations

A primitive rotation replaces exactly one nonempty subtree key set. This identity gives a DELETE bound and a root-conditioned B decrease for an explicit structural function, with no bound on key count or fringe size.

## Definitions and multiplicity

Let C(T) contain the exact sets of keys in all nonempty node-rooted subtrees of a finite ordered BST T. Include the full key set. A singleton occurs only for a leaf node; do not add a singleton for every key. Internal shape and the label of the subtree root are not part of the set's identity.

For n-node T, |C(T)|=n. Subtrees at different nodes are disjoint or strictly nested. Strict containment follows because the ancestor's key is absent from its descendant's subtree. Thus there are no duplicate sets within C(T). For same-key A,B define

    F(A,B)=n-|C(A) intersection C(B)|
          =(1/2)|C(A) symmetric-difference C(B)|.

The full key set is always shared, so 0<=F<=n-1 when n>=1. At n=1, F=0. Set F=0 for empty trees, which have no present-key accesses. C(T) is a family of node-key sets, not a family of external-leaf clusters or exact subtree shapes.

## The exact primitive identity

Consider a left rotation

    p(L,x(M,R))  ->  x(p(L,M),R).

The key set of the whole local subtree is retained, now rooted at x instead of p. All outside subtree sets and the internal sets of L,M,R remain unchanged. The only replaced sets are

    J={x} union keys(M) union keys(R),
    K={p} union keys(L) union keys(M).

J contains x and excludes p, while K contains p and excludes x, so they are distinct. They cannot equal any retained set of the same tree. Consequently, with B fixed,

    F(A_after,B)-F(A_before,B)
      = indicator(J in C(B))-indicator(K in C(B)).          (1)

In particular, the absolute change is at most one. Right rotations give the same formula after exchanging left and right. Empty fringe slots cause no exception.

## The actual source ordering of a B splay

Let x be the accessed key. At every primitive rotation in an ordinary bottom-up source splay, the removed proper subtree set J contains x and the added set K excludes x. For a final zig the promoted child is x. In an LL or RR double, the first promoted child is the parent of x, whose old subtree contains x; the second promoted child is x itself. For an LR or RL double both rotations promote x. In each case the demoted-node subtree created by the rotation excludes x.

This covers the exact same-side order in python/liquidity/legacy_embedding.py and the LL/RR/LR/RL frame reconstructions in python/independent/splay.py. In particular, it does not treat a same-side double as two consecutive rotations both promoting x. Earlier rebuilt x subtrees and arbitrary fringes are carried as actual subtrees, so the argument continues at all later operation sites.

Assume now root(A)=x while B splays x and A is frozen. Every proper A subtree excludes x. A removed proper B set J containing x therefore belongs to no C(A). Formula (1), applied with the moving side B, becomes

    Delta_primitive F = -indicator(K in C(A)) <= 0.         (2)

No common set is ever lost. This is an exact structural cancellation, not a bound on a fitted depth histogram.

## At least one new shared set for a nontrivial B access

Suppose d_B(x)>0 and let y be B's old root. Choose the side of x containing y:

    I={k:k<x}, if y<x; otherwise I={k:k>x}.

I is nonempty and proper. It is the entire corresponding child-subtree key set of A because root(A)=x. It becomes the same child-subtree key set in S_x B. It was NOT in C(B): I contains the old B root y but is a proper set, and a proper node-rooted subtree cannot contain the global root.

Thus at least this one set is newly shared. Since none are lost,

    F(A,S_x B)-F(A,B) <= -1, root(A)=x, d_B(x)>0.         (3)

For d_B(x)=0, B is unchanged. More precisely, the whole difference equals minus the number of newly shared B subtree key sets. Nothing here implies one new shared set per B double; that stronger claim is false (CC03).
