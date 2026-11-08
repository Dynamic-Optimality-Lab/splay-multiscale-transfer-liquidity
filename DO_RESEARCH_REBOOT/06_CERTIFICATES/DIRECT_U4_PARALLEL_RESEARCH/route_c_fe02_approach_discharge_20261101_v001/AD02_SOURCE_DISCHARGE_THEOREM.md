# Source-exact discharge after approaching and overlapping transfers

PROVED—UNIVERSAL: the equal-pair and one-rotation lemmas below, on their
stated structural domains. PROVED—RESTRICTED DOMAIN: the explicit
all-size overlap family, all its common ordered fringes, reflections and
arbitrary closed continuations. This is not unrestricted FE02-RIGIDITY.

Use the inherited original cyclic A-root blocks. A nontrivial block has
a>=1; its A work belongs to its actual leader and its B work to its first
KEEP, if any. Intermediate DELETEs at the same root have zero A work.
B remains fixed until the first KEEP. Subsequent same-key KEEP/DELETE
followers do nothing. The inherited costed endpoint projection to a
common KEEP therefore preserves a,q and the complete block boundary
pair, but does not move physical event owners to a different occurrence.

## 1. Universal local discharge lemmas

**Equal-pair lemma.** From A=B, a KEEP-containing nontrivial block has
source depths d_A=d_B=d, a=ceil(d/2), q=floor(d/2)<=a. Hence
delta=q-2a<=-a<=-1. A KEEP-less nontrivial block has q=0 and delta=-2a.
This includes a DELETE leader followed later by the first KEEP.

**One-rotation lemma.** Suppose the complete post-positive trees have the
same root and differ by a single internal ordinary rotation. Every next
nontrivial block has delta<=-a<=-1, whatever target or KEEP/DELETE mask.

Proof: the source right rotation

    g(p(L,M),R) -> p(L,g(M,R))

changes relative depths of p,g by-1,+1, every key of L by-1, every key
of M by0, and every key of R by+1. Keys outside the rotation subtree
have shift0. The reverse/left orientation has the opposite shifts.
Therefore d_B(x)<=d_A(x)+1 for EVERY key, including arbitrarily deep
fringe keys, irrespective of which of the two trees is A. For a
KEEP-containing block,

    q=floor(d_B/2)<=floor((d_A+1)/2)=ceil(d_A/2)=a.

For a KEEP-less block q=0. This proves the claim. It assumes a single
rotation between full trees; it assumes no nonexpansion of rotation
distance under future splays.

**Closed-walk consequence.** If a positive block is followed by an equal
pair or a one-rotation pair, a later negative block is mandatory in its
same closed traversal. The positive changed A's root from r to y!=r.
Exact return to its pre-block source requires at least one subsequent
nontrivial A-root block. Zero-cost root followers cannot accomplish this.
The first such block is negative by the relevant lemma. No bound on
return gap, key support or total walk length is used. This excludes ALL
single-positive saturated returns with either post-positive structure,
on arbitrary BSTs, not just the13-core construction below.

## 2. The explicit overlapping source family

Use B0,U,R,C from AD01. Let A_u be the actual A output of

    D8,D7,[Du if u=2 or4],D1,D13

from diagonal B0; u=0 denotes omission. This is a source definition
with the following literal identities (all common gaps suppressed):

    A_0=13(1(.,8(7(U,.),R)),.),
    A_4=13(4(1(.,3(2,.)),8(7(6(5,.),.),R)),.),
    A_2=13(2(1,8(7(3(.,4(.,6(5,.))),.),R)),.).

For each u, two KEEP-containing root blocks8,7, entering at(A_u,B0),
have costs(1,2),(1,3). Original masks and root followers are allowed
through the costed endpoint theorem. Their full post-positive pairs are

    u=0: (C,C),
    u=4: (P4,C),
    u=2: (P2,C),

where, writing V=8(.,13(R,.)),

    C =7(1(.,4(3(2,.),6(5,.))),V),
    P4=7(4(1(.,3(2,.)),6(5,.)),V),
    P2=7(2(1,3(.,4(.,6(5,.)))),V).

These are direct LR/RR source identities, independently checked with
all14 ordered gap subtrees opaque. A full paired source, not only these
depth values, is required as a hypothesis. Arbitrary histories before
and after this span are allowed; the displayed diagonal prefixes prove
reachability and need not occur inside every walk to which the theorem
applies.

The u=0 case is covered by the equal-pair lemma. In u=4 a right rotation
of node4 over its child1 inside P4 gives exactly C; thus the one-rotation
lemma covers EVERY possible next target, not only core targets.

## 3. Complete u=2 successor classification

The shared current root is7. The following source table covers every
other core target. It computes q from the ORIGINAL B source, not an
observed destination or a future payer demand.

|Target|d_A|d_B|a|q|delta|
|---:|---:|---:|---:|---:|---:|
|1|2|1|1|0|-2|
|2|1|4|1|2|0|
|3|2|3|1|1|-1|
|4|3|2|2|1|-3|
|5|5|4|3|2|-4|
|6|4|3|2|1|-3|
|8|1|1|1|0|-2|
|9|4|4|2|2|-2|
|10|5|5|3|2|-4|
|11|3|3|2|1|-3|
|12|4|4|2|2|-2|
|13|2|2|1|1|-1|

For completeness, let F_i be the common subtree in the gap after core
key i, with F_0 below1 and F_13 above13. The depths alpha,beta of each
gap root in P2,C are:

|Gap i|0|1|2|3|4|5|6|7|8|9|10|11|12|13|
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|alpha|3|3|3|4|6|6|5|2|5|6|6|5|5|3|
|beta|2|5|5|4|5|5|4|2|5|6|6|5|5|3|

An arbitrary target in a nonempty F_i has internal depth f=2v+p,
v>=0,p in{0,1}, identical in both copies. Consequently

    a=v+ceil((alpha+p)/2),
    q=v+floor((beta+p)/2),
    delta=-v+floor((beta+p)/2)-2ceil((alpha+p)/2).

For every column and BOTH parities the last constant is<=-1. Thus
EVERY fringe target, at EVERY internal depth in EVERY valid common
fringe tree, is strictly negative. No finite depth cutoff is used.
Empty fringes contribute no target. A KEEP-less block is negative
regardless of this table. A same-root7 follower cannot be a nontrivial
successor. These cases exhaust the entire key set.

The sole possible nonnegative successor is therefore a KEEP-containing
block at2. It has delta=0 and synchronizes the FULL trees:

    S_2(P2)=S_2(C)
       =2(1,7(3(.,4(.,6(5,.))),V)).

In P2 this is one right zig. In C the path is7,1,4,3,2,
with an inner LL followed by an outer LR. The destination identity
also holds for all14 common opaque gap subtrees. A DELETE-led block
that later KEEP2s has the same endpoint, with A work at its original
leader. A KEEP-less block at2 instead supplies negative slack directly.

If this saturated successor occurs, the next nontrivial block is
negative by the equal-pair lemma. Exact source closure forces its
existence, since root2 is different from the entering root13 (and from
the pre-positive root8). A closed continuation cannot terminate solely
with zero-cost root2 followers. This reasoning never assumes that an
arbitrary closed walk has a short return or a retreat-only interval.

## 4. Repay-or-synchronize theorem and upward consequence

For any increasing relabeling of this13-core scaffold, substitute an
arbitrary finite valid common BST at EACH ordered external gap, empty
allowed. Include its reflected orientation. Consider ANY original
exactly closed reachable history that contains the stated8,7 block
span at(A_u,B0), u in{0,4,2}, with arbitrary support and mixed masks
elsewhere. After the positive7 block, the first nontrivial block is
negative, except possibly for u=2 and a KEEP-containing block2. That
exception is saturated and synchronizes; its next nontrivial block is
negative. Hence a genuine negative block occurs within AT MOST TWO
subsequent nontrivial blocks.

If the whole walk meets FE02's one-positive hypothesis, this compulsory
delta_j<=-1 gives sum delta<=1-1=0 and Q<=2A. It rules out the
single-positive saturated-return obstruction throughout THIS source
class. The classification uses complete source structures, not a
finite set of depth signatures. Arbitrary unequal fringe pairs and
unclassified overlapping cores are outside the structural theorem.

## 5. Distinct-unit physical payment

For every nonpositive block assign its own q B doubles to the first q
units in the ordered list(A-event0 bit0,bit1,event1 bit0,bit1,...).
The unique positive block uses its own two units for its first two
B doubles. At the forced negative block j, q_j<=2a_j-1 certifies that
the last actual A-event's bit1 is not in its own-work prefix. Assign
that bit to the positive block's third double. It is not assigned to
any other block. The positive block has exactly one such unpaid demand;
all other assignments stay within their own physical block.

Take one traversal beginning at the positive block. The forced donor
occurs later in that traversal, within at most two nontrivial blocks,
and no unit from startup or another traversal is used. In a mixed block
the source certification of q uses the B source that stays unchanged
until its first KEEP; the chosen A unit remains at its actual earlier
leader. This is a direct injection, not an altered FI/PF/FE algorithm
or a reservation selected from future observed demands. The negative
block exists by the source theorem; no successful-cut premise is used.

## Scope of the proof

The one-rotation and equal-pair conclusions apply to arbitrary full
BST pairs satisfying those explicit structural relations. The two-step
overlap classification proves a further all-size source family, not
all possible near-target transfers. No theorem here forces an arbitrary
FE02 exposure into one of these classes. That missing source reduction
is recorded in AD04; FE02-RIGIDITY, FE02-CD and Universal Coarse-Double
remain OPEN. No strict new FI/PF/FE coverage is asserted.
