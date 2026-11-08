# FD35 — no fixed-depth A summary can give the universal small-packet law

MATHEMATICAL DERIVATION COMPLETE, using the inspected source transformation
dependency. This is an impossibility theorem for a specified potential
architecture, NOT an impossibility of Joint Repayment or Coarse-Double.
Distinct implementation source controls and proof-review status are recorded
separately; no external review or proof-assistant verification is claimed.

## Frozen Box

Target: determine how much A information a universal source-state debt must
retain. Conditions: a fixed integer d>=0; all physical keys are genuine
KEEP keys in the containing period; arbitrary original reachable exactly
paired-closed histories. At natural boundaries retain the entire A prefix
through depth d, including actual labels, marked flags, full frontier
marked-set intervals/counts and the static physical key inventory. Retain
the entire B-only state Z (full BF, actual BE and finite recent-key charts).
Allow ANY real nonlinear function J(prefix_d(A),Z), with coefficients and
range depending arbitrarily on r and the fixed inventory.

Inheritance: exact splay frames with rigid ordered payloads; source macro
costs; the inspected ordinary-splay transformation Gamma on any fixed
backbone of >=4 keys; and the prescribed-B-state source embedding proved
in SP35 section4. Every extra source operation and physical cost remains.

Ambiguities: no assertion about debts using full A geometry, arbitrary
source history/owners, or a larger block grammar. A complete full-source
injection can exist even though this small-packet potential does not.

Bridge: source-valid packets with a COMMON A prefix, separately restored
exactly, induce inconsistent differences on one closed B-only state walk.
The actual A representatives differ below the retained prefix. This is
not an actual concatenated negative source cycle.

## Theorem

For each fixed d, at some finite genuine support r (indeed at every
sufficiently large r), no such J can satisfy

    2H(P)-Q(P)+J(prefix_d(A_end),Z_end)
                -J(prefix_d(A_start),Z_start) >= 0

for EVERY original source-valid two-genuine-macro root-return packet.
For d=1 it already suffices to allow r>=1027. Hence increasing the range,
using arbitrary B dependence, or applying a nonlinear fit cannot repair
a uniformly bounded-depth representation of A for this packet law.

## 1. A common shallow frame and variable hidden target

First d>=1. Fix consecutive anchor keys

    w=1, g=2, v1=3, ..., vd=d+2,

and a larger interval E of m further keys. Mark EVERY physical key:
M=K={w,g,v1,...,vd} union E. Thus r=m+d+2. For every x in E choose A_x
with root g, left child w and the right chain v1,...,vd,x. Put every other
E key into two arbitrary ordered payload trees at x's left/right child.
There are no other keys to place.

Every A_x has the SAME labeled prefix through depth d. Its visible subtree
marked sets/counts and all frontier intervals are also identical: only
the hidden shape on E differs. Since all keys are marked, this statement
also holds for a prefix of the full A branch quotient; there is no
anonymous unary contraction hiding a marked chain.

The fixed backbone on {w,g,v1,...,vd,x} has d+3>=4 keys. Its ordered shape
and the relative position of x (largest backbone key) are independent of
the choice of x. Use the inspected ordinary-splay transformation theorem
to fix ONE word Gamma_d transforming S_x(A_backbone) back to A_backbone.
For definiteness choose a shortest-length lexicographically first word;
finiteness and existence, not a numerical search, justify this definition.
All targets of Gamma_d are backbone keys. Source splaying commutes with
substitution of the two untouched ordered payloads; their global gap
identities are fixed by inorder order. Thus Gamma_d restores the FULL
A_x, including every other genuine key, not just its prefix.

Let M_d be the actual StepEv cost of KEEP x followed by DELETE Gamma_d
on this fixed backbone. It is a finite positive integer independent of
m and of x. The final KEEP g has a=0, since Gamma_d already restored root
g. The natural packet is

    KEEP x; DELETE Gamma_d; KEEP g.

It has actual H=M_d and restores all of A_x exactly. Do not drop the
zero-event terminal KEEP or miscount the positive DELETE gap. The packet
contains two actual consecutive genuine full-B macros, with every helper.

## 2. The remaining anchor targets also have the common prefix

Fix x0 in E and A_*=A_x0. For each anchor y in {w,v1,...,vd}, first KEEP y
in A_*, then use an ordinary A-only fixed-backbone transformation from
S_y(A_*) back to A_* and finally KEEP g. This again has finite exact cost
C_{d,y}, independent of m by rigid-payload substitution, and restores A_*
with the SAME prefix as all A_x. No numerical bound on C_{d,y} is needed.
These are actual helpers, not hypothetical donated credits.

Thus EVERY B-only choice (KEEP y,KEEP g), y!=g, has a source packet
realization with this common A prefix at both ends. Its cost is M_d for
y in E and the fixed C_{d,y} for an anchor. In B the A-only helpers do
nothing, including in the erased execution and both charts.

## 3. A closed B-only walk with strictly negative total prices

Choose m>=2^(4M_d+2). In ANY BF tree on K rooted at g, some key of E has
depth at least4M_d+2: otherwise at most2^(4M_d+2)-1 nodes could accommodate
all m distinct keys of E at depths at most4M_d+1. This is a binary-tree
capacity statement, independent of A, marked mass, or any BST shape.

Choose a deepest E key with an order tie break. For its actual pair
(KEEP x,KEEP g),

    Q >= floor(depth_BF(x)/2) >= 2M_d+1,
    2M_d-Q <= -1.

Lift the actual B-only state graph to include full BF, actual erased BE
for the fixed erasure, and both finite recent-key charts. Restrict to
states reachable from a common diagonal by the literal root-return pairs.
It is finite and closed under every choice y!=g. A sink strongly connected
component therefore exists and is closed under all those choices.

Inside it, the deepest-E policy has a cycle L consisting only of the
strictly negative-price choices above. From a vertex z of L construct a
closed walk V which takes each choice y!=g at least once and returns to z,
using strong connectivity between choices. It visits EVERY genuine key
of K, including the anchors. Its total price is finite, with costs assigned
by sections1–2. Repeat L enough times that w(L^N V)<0. This is an actual
closed BF/BE/chart walk with genuine support exactly K. Root-return choices
always have two genuine KEEPs; the helpers are A-only and do not change Z.

## 4. Each inequality has an original paired-closed source realization

Use the prescribed-state embedding of SP35 section4 separately for each
edge of L^N V, choosing its A_x or A_* and its ORIGINAL helper packet.
Prepare A before the preceding genuine KEEP g, not after the macro cut.
That preceding KEEP costs A0 and ends the preparation macro. Execute the
tested packet with its exact H and Q; follow the remainder of the fixed
closed B word; reset A by an actual A-only Gamma before the next copy of
the preceding genuine g. A, BF, BE and charts close on one actual period.
Every extra cost lies outside the tested packet. No fresh credit is
assumed present in any other existing history.

This proves source-validity with the specified B-only endpoint states.
The finite-graph closure premise is established before applying Gamma.
No arbitrary transient B mask is silently called recurrent. No BE phase
is replaced by an independently selected recurrence.

## 5. Contradiction and the explicit depth-one constants

All A endpoints have the same retained prefix P_d. If J existed, summing
the separately valid inequalities around this closed Z walk would give

    0 <= w(L^N V) + sum [J(P_d,Z_next)-J(P_d,Z_old)]
       = w(L^N V) < 0.

Contradiction. All ranges and all nonlinear dependence on the retained
information are excluded at once. The A representatives are NOT asserted
equal between different edges.

For d=1, M_1=2 can be given without Gamma. Write A_x as

    g(L,v(C,x(D,E))) -> x(v(g(L,C),D),E)
                     -> g(L,v(C,x(D,E))).

The first move is the original RR double at x; the second the LL double
at g. Each costs one A event. L contains w; the gap C may be empty.
For anchor w or v, two opposite zigs restore A_* and also cost H=2.
Thus m=1024 and r=m+3=1027 suffice, and extra E keys preserve the bound.
Reflection is literal reversal of keys and child pointers in every source
formula; both original costs and the common-prefix argument are preserved.

For d=0 the exact child-root return construction of SP35 already gives
the same impossibility for r>=1024. QED using the pinned transformation
dependency and the explicitly proved prescribed-state embedding.

## Consequence

This rules out universalization by a fixed visible A depth, even together
with the entire B state and exact static inventory. It leaves full A
branch geometry, source memory and different block architectures available.
It does not imply failure of the maximal-seven certificate or of JR35.
The open root is still a source-derived joint donor rule valid at every
required support, followed by the separately deferred reservation theorem.
