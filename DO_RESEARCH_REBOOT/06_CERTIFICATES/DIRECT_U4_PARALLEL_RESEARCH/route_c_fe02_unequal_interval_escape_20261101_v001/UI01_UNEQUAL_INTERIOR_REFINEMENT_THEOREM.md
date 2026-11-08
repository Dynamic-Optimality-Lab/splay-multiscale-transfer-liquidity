# Unequal-interior source refinement and the exact escape alternative

Status: PROVED—UNIVERSAL at the explicit source/parity domains below.
Unequal A/B interiors are arbitrary; no matched-fringe or small-support
hypothesis is imposed. The final alternative includes an odd boundary
entry and is NOT an unconditional eventual-discharge theorem.
FE02-RIGIDITY, FE02-CD and Universal Coarse-Double remain OPEN.

## 1. Canonical source intervals

Let A,B be valid BSTs on the same finite ordered key set S, |S|=n.
Define their common prefix as follows. At a pair of equal root keys,
include that key and recurse on the left and right subtree pairs.
At differing root keys stop: this is a disagreement interval. Its two
trees have the SAME KEY SET S intersected with the interval delimited
by the preceding common search ancestors, but can have completely
unrelated shapes, roots, depths and internal fringes. If both subtrees
are empty, stop without a key or a disagreement. The construction is
canonical, finite, and requires no existence theorem or future history.

Write K(A,B) for the set of exposed common keys and c(A,B)=|K(A,B)|.
This is a prefix condition on common SEARCH ANCESTORS, not the count
of every agreeing ancestor relation, not ordinary rotation distance,
and not the previously refuted scalar discordance D.

For x outside K, let I be its unique first disagreement interval.
The source search path from the global root to I is identical in A
and B and has length h. Let u_A,u_B be the internal edge depths of x
from the two roots of I. Then

    d_A(x)=h+u_A,        d_B(x)=h+u_B.

The interiors of ALL other disagreement intervals also remain arbitrary.
If the global roots differ, K is empty, I is the whole tree and h=0.
That empty-external-context case is the identity base of the same proof.
In a recurrent all-nonnegative block walk the roots agree at boundaries,
as every nontrivial block must contain a KEEP; h=0 is not needed to
impose any additional hypothesis on that reduction.

## 2. Every common-key nontrivial block is negative

Use the inherited costed block projection, without moving physical event
owners. A KEEP-containing block at x has a=ceil(d_A/2), q=floor(d_B/2).
If x belongs to K, both source paths and depths equal d. Thus

    q=floor(d/2)<=ceil(d/2)=a,
    delta=q-2a<=-a<=-1

for a nontrivial A-root block, a>=1. A KEEP-less block has q=0 and
delta=-2a<=-2. Therefore every nonnegative nontrivial block must enter
a genuine disagreement interval and have a KEEP. This is a necessary
source fact on arbitrary pairs, not an assumed donor criterion.

## 3. Even/even interval refinement lemma

**Lemma.** Let x lie in a disagreement interval and suppose BOTH u_A
and u_B are even (zero allowed). Let

    A'=S_x(A), B'=S_x(B)

be the original parent-first source splays. Then

    K(A',B') contains K(A,B) union {x},
    c(A',B')>=c(A,B)+1.

**Proof from the original frames.** Split each source path into the
common external path and its internal path in I. Original bottom-up
splay consumes frames in pairs. Since u_A and u_B are both even,
all INTERNAL frames are consumed by doubles before either tree uses
an external frame. No odd internal frame can be paired with the last
external ancestor. This statement holds when one or both internal
depths are0, and for every sequence of LL,RR,LR,RL internal cases.

At that point the current subtree in each execution is rooted at x.
Its children are arbitrary paired trees on I intersected with(-infinity,x)
and(x,infinity), respectively. No equality of those children is assumed.
The remaining external frame words have the SAME directions and named
ancestor keys in both executions. Sibling subtrees can still have their
arbitrary paired disagreement interiors.

Represent the original common prefix as a partial tree with a hole for
each disagreement interval. Replace the accessed hole by the NEW common
node x, with two new holes for the two internal key intervals. Apply
the original external frame word to this partial tree. Each of the
four double identities and either terminal zig permutes its named
common nodes and reattaches its holes as whole subtrees. It erases
no named common node and places no hole above a named common node.
This is precisely the literal original source rebuild in both trees.
Consequently its output is another shared partial tree containing all
old common nodes and x. Expanding the paired holes back to their actual
arbitrary subtrees cannot hide any of those partial-tree nodes. Further
matching roots inside the new holes can only enlarge the canonical
common prefix. This proves the set inclusion and the strict count.

The empty external word h=0 needs no rebuild: the common new root x
alone gives the claimed gain. Reversing key order interchanges LL/RR
and LR/RL and preserves the proof. Empty child intervals and terminal
external zigs are included. No source output or observed payer demand
selects the initial interval or its parity. QED.

The six fixed opaque primitive contexts in primitive_context_certificate.json
verify the outer identities with arbitrary PAIRED, UNEQUAL children and
siblings. They are checks of the source implementation. The general
proof is the frame split and partial-tree argument, not finite enumeration
of arbitrary path length or arbitrary interior BSTs.

## 4. Uniform progress-or-escape theorem

Consider any original sequence of nontrivial A-root blocks on S. Project
each KEEP-containing complete block to its cost-equivalent common KEEP
only for boundary-tree analysis. Let its current canonical common count
be c. Within any n-c+1 subsequent nontrivial blocks, at least one of
the following occurs, PROVIDED that many blocks actually occur:

1. A genuine negative block, delta<=-1.
2. A nonnegative block that enters its canonical disagreement interval
   with at least ONE ODD internal source depth u_A or u_B.

Proof: a KEEP-less block already has negative excess. If neither event
occurs, every block enters a disagreement interval at even/even depths
and raises c by at least1. This cannot happen n-c+1 times because c<=n.
Zero-cost same-root followers are not additional nontrivial blocks.

This is an explicit all-size theorem about source histories with arbitrary
overlap and unrelated interiors. It gives a negative block OR a named
source boundary frame. It does not prove that the latter frame repays.
For a short open history, finite support alone does not require it to
continue; no event beyond its length is asserted. Nor may a bound that
crosses into the next period be used as imported physical credit.

## 5. Closed-walk exclusion at the source-even domain

No nonempty exactly closed original walk of nontrivial blocks can have
BOTH:

    every block has delta>=0,
    every block's canonical internal depths are even/even.

Indeed all blocks contain KEEP, so their costed paired boundary projection
closes exactly. If its block count is M>=1, the refinement lemma gives
c_final>=c_initial+M, contradicting equality of the FULL paired source.
This is a closure contradiction without a short-return or successful-cut
premise. It holds for all valid source states, including all reachable
ones, and arbitrary support and walk length.

**Restricted FE02 consequence.** Suppose an actual FE02 walk has one
positive block of type(1,3), all others delta<=0, and every NONNEGATIVE
block has even/even canonical internal depths. Then it has a negative
block and Q<=2A. To prove this, assume it has no negative block; every
block is then nonnegative and even/even, contradicting the preceding
source-closure theorem. The parity predicate INCLUDES the positive
block. It is a genuine source restriction, not proved automatic for
arbitrary FE02 transfers. Omitting it on the positive would invalidate
this argument.

The existing base13 closed control has precisely two nonnegative blocks:
helper8 with internal depths(0,2), and positive7 with(0,4). Thus the
restricted source domain has actual reachable closed instances. This
is nonvacuity, not a strict-coverage assertion relative to older criteria.

## 6. Exact necessary eviction balance for an arbitrary candidate

For a hypothetical FE02 saturated return let K_j be the canonical common
key set just before block j in its closed costed macro projection. Put

    g_j=|K_(j+1) minus K_j|,  l_j=|K_j minus K_(j+1)|.

Every block is nonnegative, so its target x_j is outside K_j and belongs
to K_(j+1). Thus g_j>=1. Exact closure gives sum g_j=sum l_j. On every
even/even entry, the proved set inclusion gives l_j=0. Consequently

    sum_(odd-boundary entries j) l_j = sum_all_j g_j >= M.

Every actual common-key eviction is named by its SOURCE KEY and block
occurrence. Repeated eviction of the same key at different blocks is
counted with that multiplicity; these are not M distinct physical keys
or A units. This identity is a necessary structural constraint on the
full arbitrary-interior candidate, not an upper bound on evictions or
a proof that they must repay. UI02 shows why treating such evictions
as individual credit demands would manufacture unsupported debt.

## 7. Actual physical injection on the proved FE02 subclass

At each nonpositive block pay its own q demands with the first q actual
A units in event-index/bit order. At the unique positive block pay its
first two B doubles with its two units. Choose the first genuinely
negative block encountered later in a single traversal starting at the
positive. Its source has q<=2a-1, so its LAST A-event bit1 is outside
its own-work prefix. Use that one real unit for the positive's third
B double. No other loan is needed and no unit is reused.

The negative block exists by the source-even closed theorem, not by an
assumed successful cut. In a mixed block the A event stays at its actual
leader; B demand stays at its actual first KEEP, while B's source remains
unchanged until that KEEP. No startup or future-period credit is used.
This is a direct injection and does not change FI/PF/FE reservations.

Degenerate n<=1 or single-root closed histories have no positive(1,3)
block: exact closure forbids the sole possible one-time B-root change.
They require no separate donor. Terminal B zigs are genuine changes but
not double demands, as in the inherited definitions.

## Precise limit

Odd-boundary entries are allowed in the full FE02 domain. The lemma
does not say they are negative, finite in number, mutually disjoint,
or bounded in their evicted common mass. UI02 gives an exact unbounded
zero-spare-capacity counteredge to that unrestricted extension. Full
eventual discharge through such entries remains OPEN.
