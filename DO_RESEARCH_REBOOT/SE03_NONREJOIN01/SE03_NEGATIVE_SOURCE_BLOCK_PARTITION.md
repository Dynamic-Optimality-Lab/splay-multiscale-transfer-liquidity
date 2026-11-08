# Exhaustive negative source blocks and the six-key residual

Status: exact source classification. Its block cost H is defined HERE from
actual original A events and is NOT an inherited symbolic LOW/HIGH coordinate.
The frozen graph, its h0 correction and all Stage11G conventions are unchanged.

## 1. A direct cyclic grouping with no lost source operations

Take an original closed walk with r>=6 genuine KEEP keys and fixed B-core
size c<=2r-1. Cut just after any genuine KEEP. Group all following requests
up to and including the next genuine KEEP into one block, cyclically.
Nongenuine KEEPs and DELETEs remain inside their actual blocks. Every
original occurrence belongs to exactly one block. B freezes until its last
occurrence, which has one genuine target x. If the preceding genuine target
was y, then y!=x, because the B root before the next genuine KEEP is y.

At block entry A also has root y; its last request ends with root x. Hence
its actual A-event total H is an integer>=1. This does not exclude any h0
case of the existing controller, whose variables/grouping are different.
Let q=floor(d_B(x)/2) be this block's only nonzero B-double charge; earlier
nongenuine KEEPs have q0. The exact original total is

    2A-Q_B = sum_blocks (2H-q).                             (1)

All original costs are retained, including positive A costs at nongenuine
KEEPs. Because every B target is in the fixed c-node core,

    q<=floor((c-1)/2)<=r-1.

A negative block therefore satisfies

    1<=H<=floor((c-3)/4)<=floor((r-2)/2),
    q>=2H+1,
    d_B(x)>=4H+2.                                         (2)

This is an exhaustive inequality partition, not a finite enumeration of
source shapes and not a claim that negative blocks cannot form a cycle.

## 2. Complete actual A source geometry for H=1 and H=2

If H=1, exactly one request in the block performs one A StepEv; all others
are root identities. Its target must be x, because no later actual event
can change the final root. Its pre-depth is1 or2. Thus the request word
is a run of root-y identities, followed by x requests, ending with the
first genuine KEEP x. Before the terminal KEEP all x requests are DELETEs;
otherwise an earlier KEEP x would have ended the block. All original
KEEP y operations are B identities. The unique real event is a ZIG or
one original double bringing x from a child or grandchild of y to root.
A rotated middle vertex may be anonymous; there is no different helper
REQUEST target in an H1 block.

If H=2, there are exactly two alternatives: one request x with two A
StepEvs (pre-depth3 or4), or two positive requests u then x, each with one
StepEv (each pre-depth1 or2). Between these requests only current-root
identities occur. The first target u may be any present key, including
an anonymous key outside S; no bounded private inventory is assumed.
If the final positive request is before the terminal KEEP, its mode is
DELETE. Original nongenuine KEEP y can occur among earlier requests and
must retain its A charge; the classification does not assume all positive
requests before the terminal one are DELETEs.

More generally the union of A search-path vertices participating in all
positive requests of one block has size at most1+2H. Start with entry root
y. Each positive splay of cost a has source depth<=2a and starts at a root
already exposed by the preceding positive request, so it introduces at
most2a new path vertices. Sum over actual requests. This is a complete
local source-term representation conditional on exact rigid hangers; it
is not a complete bounded global state after arbitrary future exposures.

## 3. Six-key negative blocks

For r=6, c<=11, so q<=5. The exhaustive negative pairs are

    H=1, q in {3,4,5};
    H=2, q=5.                                             (3)

If c<=8, only H1/q3 is possible. If c=9 or10, only H1/q3 or H1/q4 is
possible. If c=11, all pairs in (3) remain. At c11, the maximal-core
theorem additionally forces EVERY genuine B access to have even depth
and outer LL/RR. In particular q5 means depth10 and a root-to-x path
containing all ELEVEN core nodes; there is no off-path core node.

For such a c11/q5 block all six marked keys lie on that B path. An H1
block exposes at most3 A path vertices, so at least3 of those marked keys
are absent from its active A paths. An H2 block exposes at most5, leaving
at least1 marked B ancestor absent from its active A paths. These are
source cardinality consequences only. Erasing a mark does not physically
remove its B node or automatically lower q; no repayment follows from
this pigeonhole argument alone.

## 4. Exact residual after the structural reductions

The marked-leaf theorem supplies selected erased five-key/core<=8 funding
for full six-key c<=9. Full core10 and11 may leave an erased core9 and
therefore require ordinary CD(5) or another independently proved funding
mechanism. In every branch, the negative blocks in (3) must be repaid by
actual distinct source credit or signed cancellations in a source-complete
cyclic law. Neither (1), the finite list (3), nor the existence of an
unused marked ancestor proves that law.

For arbitrary r, (1)-(2) and the local1+2H path bound are uniform; the number
of permitted low-cost events grows with r. A fixed H1/H2 proof cannot be
silently promoted to unrestricted support induction. No new numerical
signature campaign or source finite test is authorized or performed here.
