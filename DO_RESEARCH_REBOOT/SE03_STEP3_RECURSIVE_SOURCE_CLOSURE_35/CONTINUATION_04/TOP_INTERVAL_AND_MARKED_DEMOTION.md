# TI35 and MD35 — source interval ranks and marked demotion ownership

Status: new uniform mathematical derivations; independent source checks
and proof review are tracked separately. These do not close JR35.

## TI35 IAGS Box

Target: source-derived potential decrease slots that see nonmatching
subtree shapes, and a precise branch obstruction to their universality.
Conditions: original finite paired-closed source; fixed actual BF core S;
all original A operations and all actual B rotations.
Inheritance: fixed carrier, ND35 unit slots, PC35, JR35-N0, C14 source
transport, original StepEv formulas.
Ambiguity: branch-bearing neutral doubles can survive the new measure.
Bridge: replace exact label equality by A's top vertex of a B interval.

### 1. The A-top of a full ordered interval

For each actual B subtree rooted at an S vertex let I be the closed
interval from its least to its greatest S descendant. It is nonempty.
Consider ALL physical A keys in that ordered interval, not just S.
There is a unique shallowest A vertex top_A(I). Indeed the LCA of its
two endpoint keys belongs to the interval, and every key in the
interval is its descendant. This holds for a singleton interval.

Let L(A,B) be the set of these top_A(I) values over all S vertices,
and T(A,B)=|S|-|L(A,B)|. The root interval is included. The range is
0..|S|-1; no ambient/private population cap is used.

In an actual A rotation promoting y over p, an interval's top can
change only from p to y. If the interval meets different frame
hangers, its convexity places at least one separating operand in it.
An interval containing neither operand stays in one rigid hanger
(unless its top is above the frame, which is also unchanged).
An interval containing only one operand keeps that operand as top
within the frame; the other cannot become top. With both operands,
and no top outside the frame, the old top p becomes y. Equivalently
this follows by looking for the first search-tree vertex whose key
lies in the interval. Thus any number of simultaneous changes
p->y alters the cardinality of the top SET by at most one.
Every actual A single rotation has Delta T in{-1,0,1}.

In an actual B rotation after A has splayed x, the removed proper
B interval is the promoted child's old descendant interval and
contains x. Its A-top is x. The whole frame interval is unchanged,
and the FULL S interval always has top x, so this removal cannot
remove x from the set. The new pivot interval supplies one top.
Thus every actual B rotation has Delta T in{-1,0}. This proves
the ND35 level-matching and access-slot laws for T by the same
physical-bit construction. As before, this is a partial comparison
until every demand, frozen owner, and Bank25 interface is justified.

### 2. A source-uniform same-side supply class

In an original LL/RR double let G be its old grandparent and P
its old parent. During the first rotation the new G subtree uses
only G and the two old off-path hangers at G/P. The other old B
subtrees that contain G are ancestors of G (including the whole
frame) and contain x. A B interval of an S subtree not containing
G cannot straddle G: the full BST subtree is a convex key interval
and G is an actual S key. Hence before this rotation no interval
has A-top G, since every such interval containing G has A-top x.

If the new G interval has A-top G, the first rotation decreases T.
In particular, if both original off-path hangers are S-free, the
new interval is {G}; the double is nonneutral, independently of
every private A/B hanger. This applies in both LL and RR.
If a same-side double is T-neutral, at least one of those two
original off-path hangers has an S descendant. Choose a witness
from it by a fixed rule. Different doubles in one access have
disjoint original off-path hanger pairs; their witnesses are
distinct within that access. Repetition across accesses is not
new physical capacity.

Consequently an original source class in which every double is
same-side with A-top G in its new G interval has a full independent
comparison by the JR35-N0 grouping/streaming construction, with
T in place of Psi. The hypothesis is geometric and checkable on
actual original frames. There is no claim that it holds universally.

### 3. The exact relation to PC35

In PC35's fully marked right-vine packet, each newly created
grandparent singleton is a new A-top. Thus every double of that
packet decreases T, even though PC35 has only one B decrease.
This pays analytical level slots for that deep packet, not a
claim that all other doubles or all existing owners are covered.

Clarify the PC35 countercut: the exact two-bit neighborhood of
the four neutral demands is for DOUBLE-SPECIFIC decrease edges
plus same-macro bits. Under ACCESS-LEVEL reassignment a neutral
demand can use that access's one decrease slot, but this slot
has unit capacity. The whole five-demand macro then has capacity
at most three under that rule. This does not refute arbitrarily
adding new nonlocal source-licensed donor edges.

### 4. A simultaneous obstruction to both state summaries

Let n=4k+1, k>=4, with every physical key genuine, so M=C=S=[n].
BF starts at a right spine on odd keys 1,3,...,n; every odd key
j>=3 has the singleton left child j-1. Let U be the right spine
on the even keys 2,4,...,n-1; every even key j>=4 has the
singleton left child j-1. Start A at 1(empty,n(U,empty)).
The next operation is KEEP n, with H=1, Q=k, all B doubles RR.

In bottom-up order the old B grandparents G are n-4,n-8,...,1.
For G>=5 the new G and P labels are [G-1,G+1] and [G-1,n-1]:
the first uses the original two even side leaves and G; the
second adds P and the target's already accumulated left subtree.
At G=1 the two labels are [1,2] and [1,n-1].

After the A zig its proper labels are [1,n-1], [2,n-1],
[j-1,n-1] for even j>=4, and the odd singleton leaves of U.
No inner new G/P label matches; G-1 is even and at least4.
At the final double only [1,n-1] matches. Initially the only
proper PC35 match is [2,n], which the A zig loses. Thus PC35
increases by1 in A and decreases by1 in B, giving equal endpoints.

For T, the original B leaf tops are the even keys and remain
present throughout the B splay. The original B spine intervals
have top n except for the full interval, whose initial top is1.
The A zig changes that full top from1 to n, increasing T by1.
Each inner new G/P interval has A-top G-1, an already present even
leaf top. At the final double the new G interval adds top1, and
the new P interval has that same top. T decreases by1 and also
has equal endpoints. The inner k-1 doubles are neutral under
BOTH rules. The macro has price 2-k<0. Any state function of only
this pair of scalar summaries has equal endpoints as well.

This packet embeds in an original paired-closed history for
each k. Start diagonally at the displayed BF, prepare the exact
A source by an A-only ordinary-splay word. After the designated
KEEP n, include a genuine full tour 1,2,...,n. Use the inherited
all-BST ordinary-splay realization theorem to return BF from there
to the displayed tree, stopping at the first hit. This word is
finite and its final access 1 is genuine: a root-repeat cannot
give the first hit. Before that final KEEP insert an A-only
ordinary-splay word to the displayed A source. That KEEP costs
zero in A; it restores both full states at the natural boundary.
Repeat until actual erased B and finite chart recurrence, taking
its actual preperiod/period as in C14. All original source costs
of the preparation and return operations stay in the history.
The original reachability theorem applies because n>=17.

Thus this is a symbolic closed-source counterfamily to the
T/PC35-summary signed law and to the combined DOUBLE-SPECIFIC
slot rule with own bits: k-1>=3 common-neutral demands have
only two local units under those edges. It is not a refutation
of a new nonlocal donor rule, all full-state potentials, JR35,
or Coarse-Double. No explicit n>=17 search/replay is assumed.

## MD35 IAGS Box

Target: isolate a source-defined nonlocal physical supplier relation
for maximal-core B doubles, with exact source collisions.
Conditions: actual paired-closed source, |S|=2r-1; original genuine
marks; no restriction on A private nodes/helpers/costs.
Inheritance: CLOSED_MAXIMAL_SAME_SIDE, actual ordinals/h0, original
period/cut, basic finite alternating-matching theorem.
Ambiguity: simultaneous matching beyond collisions, and extension to
nonmaximal cores, are not yet established.
Bridge: both trees start a marked key's tenure with that key at root;
each B demotion loses its target, so actual A must have lost that
ancestor relation by then.

### 1. Marked B descendants shrink between genuine accesses to the mark

Fix a mark G. Between consecutive genuine full KEEPs of G, its
physical descendant set in B can only shrink. In maximal-core
source grammar every original double is LL/RR, with marked old
grandparent and unmarked old parent, no zig. The only promoted
vertices are that unmarked parent and the accessed mark. With
target different from G, G can be a demoted grandparent only;
if outside the two rotation operands its descendant set is fixed.
The first rotation of its double removes the target x from G's
descendants. Later outer frames preserve the processed subtree.

Every future double with this same G before its next genuine
access loses a different genuine target. The targets on G's
left side occur in strictly increasing key order; those on its
right in strictly decreasing order. For LL the retained new G
subtree excludes every old descendant <=P (in particular x<P<G);
RR has the reversed threshold. Subsequent shrinks cannot recover
those keys. This statement is within one actual G-to-G cyclic
tenure; it does not say that the same target cannot recur after
another genuine KEEP G.

### 2. Actual A loss-event relation

For original demand d=(t,k), take its exact marked grandparent G
and target x. Let s be the immediately preceding original
genuine full KEEP G in cyclic order. At the end of s, A root is
G and G is a proper ancestor of x. At the A part of t, root is
x; G no longer has x as a descendant. Therefore within this
actual tenure there is at least one original A rotation losing
G->x. A single rotation can shrink only its demoted pivot's
subtree, so every such loss has pivot exactly G. The witness
remains valid if the final KEEP has a=0 after a positive helper.
Use every intervening original operation, including DELETE.

Define MD(d) to be the actual StepEv IDs (v,j) containing any
such loss within (s,t] on the ONE actual period. Either of an
event's two bits is real, even when its rotation is a zig.
This supplies a nonempty source-defined candidate set, not a
promise that a bit is unowned or that all demands can use it.

If two demands choose the same LOSS ROTATION, their marked
grandparent must be the same physical G and their B events
belong to the same actual G tenure. Its loss-set lies on one
side of G, so all colliding targets form the strictly monotone
sequence proved above. Collisions across the two rotations of
one StepEv can additionally share that event's two-bit capacity.
There is no collision across separate marked G tenure copies
or a license to use the same bit twice.

### 3. Exact completion criterion for this source relation

For any independently specified loss-event selection ell(d) in
MD(d), if each original event receives at most TWO claims,
use its bit0/1 for those claims in actual demand order. This
is an explicit independent full comparison. Alternate with
literal h0; all unmatched starts terminate at distinct h0-free
bits. This proves ownership within the independent comparison.
The condition concerns individual event loads, not the desired
aggregate capacity inequality. It is not asserted on every
maximal-core source.

For the original static block license, use disjoint genuine-
boundary groups containing the source-certified selected loss
intervals. One may merge across all crossed boundaries; if a
group is the whole period the same source theorem still proves
its budget by distinct actual event ordinals, independently
of CD or a presumed matching. Select all actual units, include
h0, and apply the inherited K=0 streaming constructor.
Use both-endpoint actual-period transport, no new auxiliary
cut. This is not a stronger online endpoint-bank statement.
Additional fixed fE reservation remains the separate interface.

The universal remaining issue is to repay collisions (or show
source-forced escape) with nonoverlapping eligible bits. The
monotone G-tenure order is a concrete source restriction on
their interaction, not a completed donor assignment. No root
or reservation promotion follows.
