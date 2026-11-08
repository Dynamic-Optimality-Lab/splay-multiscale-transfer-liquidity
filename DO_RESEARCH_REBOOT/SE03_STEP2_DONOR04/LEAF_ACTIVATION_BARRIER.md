# A universal source barrier between maximum-depth packets

This theorem holds for all original reachable B-closed histories on r>=3
genuine KEEP keys with maximal full core2r-1. A and its anonymous helpers
are arbitrary. It uses no finite source or population enumeration.

Use the sealed sorted alternation and maximum-depth successor theorem.
Let a maximum-depth KEEP target x=m_k, followed by its forced genuine
q1 successor y, an extreme mark different from x. These form a packet.
In the B state immediately after that packet, the marked core leaves
are EXACTLY

    L=M minus {x,y},       |L|=r-2.                     (1)

## Source proof of (1)

After the maximum-depth access the old theorem gives the actual fan
rooted at x, with left unmarked right-spine u1,...,u_(k-1), each having
marked left child m_j, and right unmarked left-spine u_(r-1),...,u_k,
each having marked right child m_(j+1). Those marked children are core
leaves; arbitrary outside hangers contain no KEEP mark.

If y=m1, its source path is LL. Write the top actual frame as

    x(u1(y(A,B),Ltail),Rfan).

One original parent-first LL event gives

    y(A,u1(B,x(Ltail,Rfan))).                         (2)

All other marked leaves lie inside the rigid Ltail/Rfan fan arms and
remain leaves. x now has r-2 other marks below it, so is not a core leaf
for r>=3; y is root with other marks below. The case y=mr uses the actual
RR formula

    x(Lfan,u_(r-1)(Rtail,y(C,D)))
       -> y(u_(r-1)(x(Lfan,Rtail),C),D).

The same argument gives (1), without assuming any symmetry of an old
potential or private inventory. No old semantic row is replayed.

## A leaf cannot be activated without being accessed

If l is a marked core leaf, its full actual subtree contains no OTHER
KEEP mark. Until a KEEP l, every other KEEP path excludes that entire
subtree. Each splay rotates only its own root-to-target path and treats
the l subtree as a rigid hanger; no other marked key can enter its
interior. DELETEs and root repeats do not change B. Thus l remains a
marked core leaf until its own first genuine KEEP. This is a source
rotation invariant, not a count inferred from an endpoint potential.

Consider the NEXT maximum-depth packet in actual cyclic order, targeting
t. Immediately before that access every full core node lies on the
root-to-t Hamiltonian path. Its sole core leaf is t. Therefore EACH

    l in L minus {t}

must have been accessed at least once in the open gap between packets.
There are at least r-3 DISTINCT such marks; if t is not in L, there are
r-2. For r6 this gives at least THREE distinct genuine leaf activations,
or FOUR when the next target is x or y. With a single maximum-depth
packet per repeated period its next target is x, hence all four leaves
must be visited in the cyclic gap.

This rules out compensating a q5/q1 packet merely by immediately repeating
it: the B tree must first activate at least three other marked leaves.
It does not yet imply a positive amount of unclaimed auxiliary reserve.

## A source-derived, disjoint pool of actual A events

At each required leaf's first genuine full KEEP, consider its natural
full macro since the preceding genuine full KEEP. Its entry A root is
the preceding marked target, different from this leaf. Its terminal A
root is the leaf. Thus at least one positive A event occurs. Select the
LAST actual A StepEv in that macro. Its target is the leaf: otherwise
the last positive A operation would leave a different root, and later
zero operations could not change it to the leaf. This remains true if
that last event is in a DELETE l followed by an A-root KEEP l.

Different leaf activations have disjoint natural macros. Consecutive
maximum-depth packets have disjoint cyclic gaps. Thus these selected
actual A events are distinct both within and between gaps, even with
repetitions and arbitrary anonymous helpers. Give the first three such
events in each gap to its NEXT packet as a CANDIDATE_POOL, each with its
two actual bit IDs. This is an unconditional source rule with six distinct
physical units per next packet. It does not read private inventories or
the desired total cardinality inequality.

This is NOT yet a donor allocation. The selected events can be among
the first three of their auxiliary macros, or already owned by another
original receipt. No theorem here moves any common fE unit or spends
any candidate. The missing exclusion/release proof is precisely why
the six-slot pool cannot be promoted to the requested injection.

Actual period IDs use the legal Step1 bijection. If a gap or natural macro
straddles its seam, apply the cyclic source-role selection before mapping
each chosen role once to an actual occurrence in that period. No causal
loan or zero-bank claim at the gap cut is made.
