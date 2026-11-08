# Exact recency heap on marked ancestors

Theorem. In any original closed maximal-core history with r>=2 genuine
KEEP marks, every proper marked B ancestor of a mark x has a STRICTLY
more recent genuine KEEP occurrence than x, in the cyclic recent order.
Consequently a genuine target of recent rank k has q<=k-1. This is a
source structural theorem, not a donor assignment or signed potential.

## Source premises and periodic recent order

Reuse CLOSED_MAXIMAL_SAME_SIDE.md and MARKED_PARENT_PROJECTION.md from
DONOR05. For the actual full B tree let T have the marks as vertices and
nearest marked B ancestry as its rooted edges. A genuine target x at
depth q in T is splayed by exactly q actual same-side B doubles. The
endpoint operation makes x the root, makes all its OLD proper T ancestors
direct children of x, and leaves every off-path marked parent unchanged.
All original unmarked separators and rigid gap BSTs remain in the source.

Give a mark its last genuine KEEP time in the periodically extended
original word. Root repeats do not change the relative order of marks:
the repeated root is already the most recent mark. DELETEs do not alter
B or that relative order. Since every genuine mark occurs in the period,
after one whole period the strict relative recent order is well defined
and agrees at the actual cyclic seam. Times are proof labels only; no
original state coordinate, source operation or demand ID is changed.

## Birth-of-edge proof

Every NEW marked-parent edge is x->u for the JUST accessed x and one of
its old marked ancestors u. At birth x is newer than u. An existing edge
p->v cannot survive a subsequent access of v: that access makes v root
and removes its incoming edge. If p is accessed without removing the
edge it only becomes newer; accesses of other marks do not reverse the
relative order of p and v. Thus every born edge stays newer-parent ordered
for as long as it survives.

No arbitrary initial edge survives one complete period. Its child is a
genuine mark and is accessed somewhere in that period, removing the edge.
It might later be recreated, but then it has the certified new birth.
Therefore every edge at every boundary after one period is newer-parent
ordered. Periodicity transports that statement to EVERY boundary of the
actual full closed history. It is full B closure that licenses this
transport, not the unsupported concatenation of different A contexts.

Transitivity gives the same strict order on every ancestor path. A target
of recent rank k has only k-1 more recent marks available, so q<=k-1.
The proof is uniform in r, word length, arbitrary A helpers and fringes.

## Separate induction check

Alternatively, mark an edge certified if it was created by a target
access. The exact path-compression law preserves certification of all
off-path edges and creates only newer-parent certified edges on the path.
Accessing the child of any uncertified edge deletes it. After all marks
have been accessed there are no uncertified edges. This is induction on
the actual sequence, independent of the birth-time argument's notation.

## Six-key consequences and the surviving gap

At core11, q5 targets are exactly the least recent mark; q4 targets are
among the two least recent marks; q3 targets are among the three least
recent. In particular every access to one of the three most recent marks
has q<=2 and cannot itself be a negative singleton. This holds on arbitrary
actual core11 orders, not merely extreme sweeps.

It gives no bound on unused A units. Last A access can differ from last
B KEEP because DELETEs are actual A accesses. Even when a recent rank
certifies a cold B target, it does not identify a distinct unused donor.
It must not be substituted for the A-dependent zero/+1 preservation rule.
Nor is the marked-path compression premise asserted for core10.
