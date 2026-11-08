# Uniform subtree density and maximal-core label alternation

Status: universal structural theorem about actual closed B histories.
It does not prove signed A repayment or Step2. No graph, original edge,
raw mask, observable, or inherited certificate is changed or filtered.

Let M be the nonempty KEEP support of an original B-closed word. By the
sealed support-normalization theorem it equals genuine KEEP support.
The fixed labeled marked ancestor core is S. Every boundary root belongs
to M. For a subtree T of S at any boundary let c_T be its node count and
m_T its marked node count. Then

    c_T <= 2m_T - I[root(T) is marked].                  (1)

This improves the whole-core count to a constraint at EVERY source subtree.

## Set-growth lemma, stronger than size growth

For any nonempty marked set V and any present target x, write C=C_V(B).
If x belongs to C, all rotating operands lie in C and every hanging
subtree outside C is V-free. Rigid reattachment cannot create a marked
descendant inside any of those subtrees. Hence the new V-core is a
subset of C, even if x itself is unmarked.

If x does not belong to C, let g be the last C node on the original
root-to-x path, and p its next child. The entire subtree at p is V-free.
All bottom pairs strictly below g therefore manipulate only V-free terms.
Immediately before the first source event touching g, the rebuilt subtree
at x and all its proper hanging subtrees are still V-free.

If this first event consumes g as grandparent, its other ancestor is the
original p; the event can add only x and p to the V-core. If it consumes
g as parent with its old-core parent h, only x is new. If it is a root
zig at g, again only x is new. These exhaust the parity cases. Each rule
reattaches whole hanging subtrees and does not insert a marked node into
their interior, so no deeper processed V-free node becomes an ancestor
of V. After that first event, x has a V descendant (formerly at g or
its off-path branch). All remaining operands are on its old-core prefix
and in the current V-core; they add no further outside node. Thus

    C_V(S_x(B)) subset C union {x,p},
    |C_V(S_x(B)) minus C| <=2.                           (2)

The p term is omitted in the parent/zig cases. If x is then adjoined
to V, it is the whole-tree root and already belongs to the nonempty
new V-core, so this adjunction adds no further vertex.

This argument is a source-frame induction. It does not infer (2) merely
from the inherited size increment bound; a size bound alone would be
insufficient because lost old nodes could conceal new ones.

## Counting first visits into an actual source subtree

First suppose T is proper and its root is unmarked. Initialize V to all
marks outside T. It is nonempty because the whole-tree root is marked
and lies outside T. Its initial core is disjoint from T. Traverse one
actual complete B period. Outside targets already belong to V and add
no nodes. At each first visit of a mark inside T, apply (2), then adjoin
that mark; at most two distinct new labels are introduced. There are
m_T such first visits. At the end V=M and B has returned, so its core
is the original S and includes all c_T labels of T. Each of these labels
must have entered at some first visit. Thus c_T<=2m_T.

If the root u of T is marked, initialize V to all marks outside T plus u.
The initial V-core intersects T in exactly {u}. There are m_T-1 remaining
first visits into T, giving c_T<=1+2(m_T-1)=2m_T-1. This also works when
T is the whole core: initialize V={u}. These arguments establish (1).
Moving or splitting T during the period is irrelevant: T denotes its
initial fixed label set, and (2) bounds introductions by label identity.

## A uniform signed-mass representation

Give a marked core node weight+1 and an unmarked core node weight-1.
For every source subtree its mass is2m_T-c_T. Equation(1) states that
all subtree masses are nonnegative, and a marked-rooted subtree has
mass at least1. This holds at every boundary of the actual closed word,
not merely at the selected counting cut.

Let r=|M|, c=|S|, delta=2r-1-c. Total mass is1+delta. At a boundary whose
root is the jth marked key m_j in sorted order, the left and right core
subtrees have nonnegative masses whose sum is delta. The left subtree
contains exactly all S labels below m_j. Consequently

    0 <= P_j := (j-1)-#unmarked S labels below m_j <=delta. (3)

Every marked key becomes root somewhere in the closed word, and S and M
are fixed label sets. Thus (3) holds simultaneously for every j. There
are no S labels outside [m_1,m_r], because at the extreme marked root
the exterior child subtree has no mark and hence no core node. Therefore

    P_1=0, P_r=delta,
    u_j=1+P_j-P_(j+1)>=0,                               (4)

where u_j is the number of unmarked core labels in (m_j,m_(j+1)).

In particular, delta0 forces P_j=0 and u_j=1 for every j. Hence

    a closed maximal core2r-1 has sorted labels
    marked,unmarked,marked,...,unmarked,marked.            (5)

For six keys/core11 this leaves the single sorted mask {1,3,5,7,9,11}.
For core10, delta1, the internal P_j are bits with P_1=0,P_6=1;
there are at most2^4=16 label masks, with gap counts0,1 or2 as in(4).
This is an analytic complete constraint on actual source masks, not an
exhaustion of masks, tree shapes, cycles, or helper inventories. Not every
mask satisfying (3)-(4) is claimed realizable.

The frozen five-key/nine-core graph still retains every original mask
and raw state. Its existing certificates remain sufficient on their old
overapproximation. Equation(5) is a new source theorem used prospectively,
not a retroactive edit or acceptance filter for any certificate.

## What this does and does not settle

The theorem is uniform in r, ambient populations, arbitrary BST hangers,
length and repetitions. It rules out source geometries with too many
permanently retained unmarked nodes in a subtree. It supplies no inequality
between A cost and full B doubles and no proof that a width3 D6 exists.
The signed repayment and the original Step2 completion gate remain OPEN.
