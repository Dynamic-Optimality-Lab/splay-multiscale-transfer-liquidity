# TP-DEPTH3: complete canonical terminal-pair exclusion

Status: PROVED by a complete symbolic source-case certificate, independently
recomputed with a different immutable splay engine. This is a computer-assisted
proof with an explicit lifting argument, not an inference from finite populations.
The audits are by the same research agent; no external peer review or formal
proof-assistant verification is represented.

## 1. Exact theorem

Take an original reachable, exactly A/BF/BE-closed six-genuine-KEEP history
with full marked core11. All costs and packets are the original ones. Let t
be the actual target of a cold weight-minus-two packet. Follow any finite
consecutive packet path P from t, with every weight in {0,1} and w(P)<=1.
Suppose its last two packets are genuine H1/Q2 singletons, the first lowering
marked leaves3->2 and the second preserving2->2. At their final state f, let
x be the ACTUAL least-recent mark. Suppose BF admits the physical depth8,
all-same-side four-double access to x. Then

                         depth_A(f,x) >= 3.                 (TP)

No restriction is placed on earlier lowering, regeneration, orientation,
private inventories, erasure choice, or the placement of the optional +1.
Both E0 and E1 provenance branches are included. A, BF, BE and actual charts
are the original ones. The result is at a whole-packet boundary.

Consequently this canonical-pair class cannot complete a cheap return into
a genuine NEG2-S forced-zero source. This does not establish any debt formula,
Step2, CD(6), uniform support descent, Universal CD or Dynamic Optimality.

## 2. Inherited source facts and the projection used

Closed-source core constancy and subtree density give fixed normalized Scores
1,...,11 and marked set M={1,3,5,7,9,11}. At every source subtree C,

              |C| <= 2|C intersect M| - [root(C) in M].       (SD)

Every actual BF double is LL or RR with marked grandparent and unmarked
parent; there is no terminal BF zig. The actual q5 macro is paired with its
actual q1 successor, with all intervening operations retained. Marked-parent
compression makes every old marked ancestor a child of the accessed mark;
other marked-parent edges are retained. The marked-parent tree is a strict
heap of last-KEEP recency, so a cold mark is a marked leaf.

Affordable packets are exactly:

| Weight | Actual H,Q |
|---|---|
|0|1,2; 2,4; paired3,6|
|1|1,1; 2,3|

A genuine full macro has H>=1 because its synchronized root changes. H0
operations remain actual operations and cannot be a genuine root change.
An H1 macro has the same A endpoints as a single ordinary access to its
terminal mark. H2 has either a single two-event terminal access or two
one-event accesses, the second to the terminal mark. These are event-count
normal forms, not physical deletion of intervening source operations.

The proof forgets BE, chart observations and physical event IDs ONLY in a
one-way necessary projection to (actual A, actual BF, actual recent-six order).
Every original history has such a projected history with exactly its original
H,Q and packet order. Proving exclusion in a superset of these projections
excludes the original full states. No converse realization, state splicing,
credit allocation, or inference qE0=>qF0 is used.

## 3. Cold negative-two targets always have four marked leaves

For NEG2-S, the cold q4 target y is an old marked leaf. There are four proper
marked ancestors on its BF path and one other mark v. The new root y has
those four ancestors as marked children. The one off-path mark v retains
its old marked parent. That parent cannot have been y, since y was a marked
leaf. Thus one ancestor has v as a descendant and the other three are
leaves; v is the fourth leaf. The target has L=4. In particular the older
S5 overapproximation is unnecessary for COLD singleton targets.

For NEG2-P, q5 visits a six-mark chain. Its target has five marked leaf
children. Its ACTUAL next genuine q1 access may be to ANY of those children,
not only an extreme label. It yields a root whose sole marked child is the
previous root, with the other four marks beneath it. Again L=4.

Therefore every possible starting t in (TP) has L(t.BF)=4. This statement
uses no debt formula and no A/private restriction. The independent source
algebra also checks all128 cold singleton contexts and all62 q5/q1 contexts.
Those counts are controls on the complete symbolic calculus, not its lifting.

## 4. Complete symbolic representation of BF and A

This section is the finite-to-universal bridge, not a population assumption.

For BF define G(l,r) recursively. G(l,r) is the single free ordered gap Q_l
when l>r. Otherwise it contains every term k(L,R) with l<=k<=r,
L in G(l,k-1), R in G(k+1,r), satisfying

 r-l+1 <= 2*#{odd Scores in [l,r]} - [k odd].

At the whole core require a marked root. By induction on interval length,
this is EXACTLY the ordered eleven-Score core contexts satisfying (SD) at
every subtree. There are2394. Every gap denotes an arbitrary ordered BST
of any finite private population. It is not required to be empty or unary.
Every actual BF belongs to this grammar by (SD). BF never searches inside
a gap. All ordinary marked-target rotations therefore commute with ANY
gap substitution, with identical operands and costs.

No admitted SS probe is lost through a destination test. For an RR frame
g(+1),p(-1),x(+1), write the hanging core masses as a,b,c,d>=0. After the
rotation the new g subtree has mass1+a+b>=1, the p subtree has mass
-1+(1+a+b)+c>=0, and the x subtree has the old marked-root mass>=1.
LL is the reflected identity. Every path core vertex stays an ancestor of
a mark (in particular p retains g); no mark-free gap becomes marked.
Thus SS preserves the labeled core and (SD). The interface audit checks
this identity on every term transition: all3698 legal SS edges remain in G.

For A a partial term has explicit named nodes and free interval slots.
To analyze an H1 access to x, descend only as far as its actual depth1/2.
If a slot is reached, either x occupies that slot, or (only at depth1)
a parent p and then x occupy it. A fresh p is classified by its order
cell among all fixed future word keys and existing explicit nodes; it
may also equal an unused fixed key. Within a cell one rational midpoint
represents the order variable. Subsequent insertions split the cell again.
Every other subtree remains a universally free slot.

Induction on accesses proves completeness: any actual completion either
already exposes x, or has one of exactly those root/parent placements.
An order isomorphism fixing the word keys maps its fresh parent to the
chosen cell representative. The six ordinary source rotation identities
preserve every slot and its ordered interval. Conversely every resulting
term is valid for every permitted slot substitution. Hence exhausting these
frames is an exact algebraic case proof for the word, over ALL private
populations. There is no finite-fringe extrapolation or prefix-length bound.
When retaining fixed Score identities the same construction partitions by
all eleven Scores, including equal-gap anonymous alternatives.

## 5. A uniform two-event old-root lemma

If an A macro changes synchronized root g to x using H<=2 events, then g
lies on the all-left spine of the destination when g<x, and on its all-right
spine when g>x. At H1 its depth is1/2; at H2 its depth is at most4.

For one ordinary access, the last root event gives g at L/R/LL/RR directly
from the six source identities, independent of earlier lower events. For
two one-event accesses g->y->x, use the complete frame decomposition above
on the three distinct root keys. The six order cases have respectively
9,4,2,2,4,9 universally parameterized frames, in increasing lexicographic
order of the rank word. Every frame places g on the stated outer spine;
the maximum depths are4,2,1,1,2,4. This proves the claim by exhaustive
symbolic rotation identities, not by testing thirty concrete A trees.
All unnamed subtrees and both anonymous-parent choices are unrestricted.
The independent engine reconstructs all thirty frames from forward accesses.

The lemma is uniform in support size and private inventory. It is not a
new potential, a private counter, or a frozen graph observable.

## 6. Reduction to two reflected root orders

Assume for contradiction depth_A(f,x)<=2. Since the synchronized root at f
is a different mark, an ordinary A access to x has exactly one event.
It can be used as a mathematical probe without spending any donor credit.

Write a,b for the last two H1/Q2 targets, and g for their starting root.
Their BF terms are the inherited J2->Fork41 canonical tail. Its L3 source
has marked root degree2. It cannot be t, since t has L4. Thus there is an
actual affordable packet immediately before this tail; let its starting
root be u. An H2/Q3 destination has marked root degree>=3, H2/Q4 has
degree>=4, and a paired H3/Q6 destination has L4. Consequently that preceding
packet MUST be H1/Q1 or H1/Q2. In A we have the root word

                              u,g,a,b,x

with four one-event accesses. Its BF contexts are completely obtained by
the grammar in section4 and the source SS identities. Without assuming x
was cold before the tail, the tail identities already make x a marked
leaf there. The adversarial audit removes that filter and derives it.
The old root u cannot be x: only three other targets occur afterwards,
which cannot make that last-accessed root oldest among six distinct marks.

The complete case inventory has144 universally free BF contexts and32
rank-word profiles. Applying the complete A frame calculus eliminates30
profiles. The ONLY survivors, ranks starting at0, are

                       (0,4,2,3,1), (4,0,2,1,3).

The independent audit regenerates all32 profiles and all A identities;
CASE_LEDGER.md records the full table. These two profiles contain eight
BF contexts in total. No source-realizability claim for a context is needed:
using all such necessary contexts strengthens the exclusion.

For the decreasing-extreme profile, the actual words are
11,1,5,3,x with x=7 or9, with preceding Q=1 or2. Their unique initial
A skeleton is

                   11( x( 1(U,5(3(V,W),X)),Y ), Z ).

Every letter U,...,Z denotes an arbitrary correctly ordered subtree and
contains any required remaining physical Scores. The other four contexts
are the exact reflection: 1,11,7,9,x with x=3 or5. This is a complete
derivation of the skeleton, not a selection of a convenient A source.

## 7. The backward language closes before any L4 source

Attach the ACTUAL recent-six permutation r and the remaining prefix price
budget b to each skeleton. These are proof labels for word accounting,
not source controller coordinates or a debt function. If the known
preceding Q is1 then b=0; if Q is2 then b=1. Enumerate ALL permutations
having the correct root, the inherited recency heap, and cold x after
the three known packet targets. There are240 parameterized seed frames.

The inverse of a genuine target k has exactly the following recency rule:
the new order starts k,oldroot; remove k and insert it at any nonfirst
position to obtain the old order. Heap compatibility is a necessary source
condition, never an asserted realization converse. Root repeats only
refresh the already first root, so they change none of this logic.

Take all affordable predecessors of these languages in the COMPLETE2394
context BF grammar, including contexts with no closed-source realization.
The exact backward closure consists of:

| BF leaves | Marked root degree | Remaining budget | Parameterized recent frames |
|---|---|---|---:|
|3|3|0|120|
|3|3|1|120|
|2|2|0|20|

There are only twelve distinct (A term,BF context,budget) patterns; the
larger count retains every actual recent permutation. The twenty additions
are H1/Q2 zero predecessors of the first row. No pattern subsumption or
unproved anonymous pumping is required for this final certificate.

Here is the complete predecessor exclusion used to close the table:

* H2/Q4 and paired H3/Q6 destinations have at least four leaves and cannot
  enter ANY listed row. All actual q1 successor labels are included.
* H2/Q3 can enter only the budget1 row. For every possible BF old root
  satisfying the actual recent-root rule, that root is absent from the
  possible A outer spine. Section5 therefore excludes every direct H2
  access and EVERY anonymous helper, including unbounded private gaps.
  There are48 such source-context/recency incidences in the symbolic table.
* For H1/Q1 or H1/Q2, the old A root must be at L/R/LL/RR. All compatible
  cases in the seed row put it at depth2 on a same-side ray. The unique
  inverse SS identity produces precisely the twenty additional frames,
  after applying the exact recency rule. No available predecessor enters
  the budget1 seed row. The twenty budget0 frames admit no further zero
  predecessor: the necessary BF old roots are absent from their A rays.

saturation3.json gives every term/permutation and the twenty edges.
audit_independent.py does not trust the primary predecessor engine: it
reconstructs the full BF grammar, derives A skeletons by FORWARD independent
splays, uses the proved outer-spine necessary condition for H2, and checks
every H1 predecessor by the unique inverse identity and independent replay.
All240 seeds are included, all260 records have L2/3, and every affordable
predecessor is included or excluded by one of the cases just listed.

By induction on the length of ANY actual finite affordable prefix, every
source that can reach one of these seeds within its budget belongs to this
backward language. All its states have L2/3. But the actual initial t has
L4 by section3. This contradiction proves (TP).

## 8. Full-state, seam, and proof-status consequences

Earlier regeneration and upper-crossing helpers have NOT been declared
impossible or free. They are covered because the predecessor language is
closed under every affordable packet, for any finite prefix length. No
fixed-chart debt or normalized old M3 value is used. Actual recency is
retained; BE and charts need no invented realization bridge in this
necessary exclusion projection.

Natural packets still partition the actual occurrences once, including
nongenuine KEEPs, root identities, and q5/q1 seams. The backward induction
can cross any legal cycle cut, or several periods, while retaining the
original packet costs. It borrows no event from another period and performs
no debt telescoping or allocation exchange. Existing physical owners,
Step1 fE/gE distinction, protected reserve, Bank25 and R1-R4 remain unchanged.

The final implication is: cold NEG2 target L4 -> any supposed cheap
canonical-tail completion with A-shallow cold x gives one of the240 seeds
-> exact affordable predecessor closure has only L2/3 -> contradiction.
Hence the next cold q4 macro needs H>=2, even with helpers, and cannot be
NEG2-S. Both orientations and every private completion are covered.

The old Hamiltonian-Hhidden changing-chart normalization remains REFUTED.
The result closes ONLY the declared canonical terminal-pair exposure gap.
Other entry classes, final +1 alternatives, negative-one compatibility,
core9/10, the global donor injection and uniform support descent remain
separate obligations. No stronger Step2 or Coarse-Double claim follows.

The initial gap-name-mismatched saturation.json run is INVALID and is not
evidence. The corrected saturation3.json uses the whole density grammar;
the earlier SCC restriction is also unnecessary to the final proof. Failed
bounded countercertificate searches and the local two-packet challenge
contribute no positive premise to this theorem.
