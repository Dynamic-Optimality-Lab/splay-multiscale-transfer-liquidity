# Every double in a closed maximal core is same-side

Theorem. Let an original B-closed history have r>=2 genuine KEEP keys M
and fixed full marked core S of size2r-1. All ambient keys and off-core
BSTs are arbitrary. At EVERY boundary:

1. Every marked node has signed core-subtree mass1, every unmarked
   core node has mass0.
2. Every genuine KEEP has an even source depth, and EVERY original
   double in its B splay is LL or RR with marked original grandparent
   and unmarked original parent. There are no inner mixed doubles.

This strengthens the inherited outer-double and maximum-depth theorems
on actual closed maximal sources. It does not filter the frozen graph,
change a mark mask, or assert any A-cost repayment.

## Premises reused

The completed density theorem gives signed mass>=0 at every unmarked
core subtree and>=1 at every marked subtree, at every source boundary.
The completed label theorem gives the fixed inorder sequence

    m1,u1,m2,u2,...,u_(r-1),mr.

Give each marked label weight+1 and each unmarked label weight-1. A
rooted core subtree is an inorder interval. Alternation bounds its mass
by1 above. Thus marked subtrees have mass EXACTLY1, and unmarked
subtrees have mass0 or1. Define, for this proof only,

    K(B)=#{unmarked core vertices whose subtree has mass1}.        (1)

K is a mathematical function of the actual full B tree and fixed marks,
not a new controller coordinate or a certificate substituted for M3.

## Persistence of processed subtrees in one actual splay

Work bottom-up in a genuine KEEP of marked x. Once an original ancestor
G or P is consumed by its double, it is below the rebuilt target x.
All later outer frames reattach x's proper subtrees as whole hangers;
none enters a processed G/P subtree. Consequently the label set and
mass of each processed G/P rooted subtree is ALREADY its final value.
This follows directly from all four original double formulas, and also
holds for x's original proper subtrees. Private off-core keys stay rigid.

Every current proper child subtree of rebuilt x is either an original
off-path hanger or such a processed subtree. Its signed mass is therefore
nonnegative, using initial or FINAL density as appropriate. The rebuilt
target subtree has mass>=1. Its label set is the original subtree of the
last consumed source ancestor (or initially x), whose source mass<=1.
Hence throughout the replay its mass is EXACTLY1 and both its proper
child subtrees have mass0. No density assumption on unprocessed arbitrary
intermediate trees is being made.

## Complete actual pair classification

The next original parent P has the rebuilt marked subtree of mass1 as
one child and an original off-path hanger of nonnegative mass c as the
other. If P were marked, its source mass would be at least2, impossible.
So P is unmarked; its source mass is c in{0,1}.

For LL write the actual frame as

    G(P(x(A,B),C),D) -> x(A,P(B,G(C,D))).              (2)

Mass(A)=mass(B)=0 by the preceding argument. Put g=weight(G),
c=mass(C),d=mass(D). The whole rebuilt mass after the double is1, so

    g+c+d=1,              0<=c,d<=1.                 (3)

If G is marked, g=1 forces c=d=0. P is source mass0; the final G
has mass1 and final P mass0. Thus K does not change.

If G is unmarked, g=-1 forces c=d=1. Both original G and P have
source mass1. Final G has mass1 and final P mass0. Thus K decreases1.

RR has the same classification with the actual left/right hangers
interchanged, as verified independently by its own source formula.

For LR write

    G(P(A,x(B,C)),D) -> x(P(A,B),G(C,D)).              (4)

Here mass(B)=mass(C)=0. P is again unmarked. Final P has mass a-1,
where a=mass(A), so final density requires a=1. The source whole mass
g+a+d=1 now forces G unmarked and d=1. Original G,P both have mass1;
final G,P both have mass0. Thus K decreases2. RL gives the same strict
decrease, independently from its own formula.

There is no possible terminal zig. Its old root is marked of source
mass1, but would contain the rebuilt x subtree of mass1 plus its own
weight1 and a nonnegative off-path hanger, total at least2.

These cases are exhaustive. All untouched subtree masses are unchanged.
Thus every genuine KEEP has K(after)<=K(before); a mixed double or an
unmarked grandparent makes the inequality STRICT. DELETEs and root
KEEPs fix B and K.

## Full closure forces the claimed source language

On the original full B period K returns to its exact initial value.
Every decrement is nonnegative, so no strict decrement occurs anywhere.
Every double must therefore be the zero-change case: LL/RR with marked
G and unmarked source-mass0 P.

There can be no source unmarked mass1 vertex v. Until the first KEEP
inside its original marked-descendant set, outside target paths exclude
its entire subtree and leave it rigid. Such a KEEP exists since every
marked key is visited in the period. Its path contains v, so v is
consumed by an actual double. As grandparent it is forbidden unmarked;
as parent it is forbidden mass1. A terminal zig is impossible. This
contradicts the zero-change source classification. Hence K=0 everywhere,
giving both claims of the theorem.

The proof is uniform in r, word length, repetitions and all finite
private fringes. It uses exact B closure, not root equality or A/B
equality, and retains all original operations. A may perform arbitrary
DELETE helpers; none changes B. Bank25 and all original fields stay fixed.

## A compact exact representation consequence

An unmarked mass0 node has child masses summing1. Since every marked
node has mass1 and every unmarked node mass0, it has exactly ONE marked
child; its other child is unmarked or empty. Every nonroot marked node
has an unmarked parent, because marked children would contribute positive
mass to a marked parent's mass0 proper side. These edges pair each of
the r-1 unmarked nodes with one of the r-1 nonroot marks.

Grouping each such two-node pair gives an exact ordered two-key block
with three child ports. The global marked root is a one-key block with
two ports. Each original B double is the original same-side root exchange
across one such block. This is proof notation for the actual labeled
tree and its rigid gap BSTs, not node deletion or a new simulator.

This theorem does not prove Step2, a width-two full debt, or that any
identified A event is unused. Core10 has deficiency1 and is outside
this maximal-core theorem. The frozen M3 graph retains all original
masks/rows, including those not realized by these closed sources.
