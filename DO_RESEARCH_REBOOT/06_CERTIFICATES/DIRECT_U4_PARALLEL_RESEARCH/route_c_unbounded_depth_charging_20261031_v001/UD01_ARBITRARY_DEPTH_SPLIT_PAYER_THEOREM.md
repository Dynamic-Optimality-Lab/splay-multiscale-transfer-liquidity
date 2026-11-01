# Split payers at arbitrary source depth

Status: PROVED—RESTRICTED DOMAIN. For every finite ordered key set and reachable closed actual A/B source walk accepted by the specified procedure UD below, Q_B<=2A. Every successful cut of SL's split shallow procedure remains successful. UD02 supplies a strict reachable source witness and an analytic family with unbounded genuine KEEP support.

Shallow eligibility is removed completely. Post-anchor depths may be zero or arbitrarily large. The source ceilings and accepted-cut restriction remain explicit; no theorem asserts that every reachable closed walk succeeds. Matching-terminal work stays FROZEN. Universal Step 3/CD and Stage 11G statuses are unchanged.

## Source blocks and unit identities

KEEP x splays A and B. DELETE x splays A alone, leaving B frozen and the key set intact. All requests are present keys. With edge depths, grouped A cost is ceil(d_A/2), B-double count is floor(d_B/2), and a B zig has zero double count but can change B.

Use cyclic maximal A-root blocks: leader i has a_i>=1 actual A StepEvs, followed by zero-A-cost requests of the same key. A block has at most one genuine B-changing KEEP. Let q_i count all its B doubles and delta_i=q_i-2a_i. Then

    sum_i delta_i=Q_B-2A.                        (1)

Each A event contributes two distinguishable units (cycle occurrence, event index, bit), bit 0 or 1. Each B double is a distinct demand (cycle occurrence, B-event index). Repeated keys or event shapes do not identify their occurrences. This proof concerns scalar closed-walk charging, not an online service guarantee or creator/setup ownership.

If A=0 in a closed walk, every request uses the same fixed A root. B can change at most once before staying fixed at that key; exact B closure forces no change, so Q_B=0. Empty walks, empty key sets and one-key cases follow. Otherwise the cyclic block decomposition exists, including a block crossing the input seam.

## The all-key source bound

For every BST T, present accessed key x and present tracked key y, the established whole-splay displacement lemma states

    d_(S_x T)(y)<=d_T(y)+2.                     (2)

It is already proved in 26AL and restated with arbitrary-fringe source rotation tables in DS01. It is not restricted to roots or children. The first rebuilt site containing y increases its depth by at most 2. If y is not x, later outer rebuilds put y in a fringe of the rebuilt target-rooted unit, with nonpositive subsequent shifts. A final zig contributes at most +1. If y=x, its final depth is zero. The source LL/RR formulas are parent-first; no replacement rotation convention is used.

For a positive block i, let B_i^+ be B immediately after its genuine B splay. For EVERY present key y define

    h_i(y)=d_(B_i^+)(y).                        (3)

There is no eligibility set. In particular h_i(x_i)=0; no positive lower bound or constant upper bound on h_i is imposed.

Fix a single one-period block order. For later block j with key y, let k_i(j) count genuine B-changing KEEPs strictly between i and j in that order. Count zero-double zigs and omit DELETEs and B-root no-ops. Repeated application of (2) gives

    d_before_j_KEEP(y)<=h_i(y)+2k_i(j).

The block's initial DELETEs leave B unchanged before its first KEEP. At most one KEEP can change B, so the whole block's q_j is the first KEEP's floor(depth/2). Hence

    q_j<=c_i(j),
    c_i(j)=floor(h_i(y)/2)+k_i(j) if j has KEEP,
    c_i(j)=0                         otherwise. (4)

The identity floor((h+2k)/2)=floor(h/2)+k holds for all nonnegative integers, including h=0. Intermediate splays may access y; (2) remains true and no noninterference premise is needed. Exact paired closure makes the same argument valid when this order crosses the input seam.

These bounds constrain the SAME q_j and combine by minimum, not addition. Their validity does not depend on whether the originating anchor has been paid. A retained fact is never an additional pool or spendable unit.

## Explicit one-period procedure UD

Choose a physical A-root-block cut and scan exactly one period. Maintain all encountered positive identities in chronological history H, retained after payment. Each has its residual-demand list and a monotone cursor p_i, initially zero.

At positive block i, pay its first 2a_i B doubles from its own actual units. Append its remaining delta_i demands, with cursor zero, and append i to H. Positive pools do not lend.

At nonpositive block j, let C=2a_j. If H is empty, reserve r_j=C and lend nothing. Otherwise compute

    c_j=min_(i in H)c_i(j),
    r_j=min(C,c_j),
    S_j=C-r_j.                                 (5)

The history includes ALL encountered positives, whether paid or unpaid, and all of them give a bound for j's key. Nonpositivity gives q_j<=C, and (4) gives q_j<=c_j. Thus q_j<=r_j. Freeze the reservation once for this physical pool.

Number its units by event and bit, 0,...,C-1. Pay own demands from the first q_j units of [0,r_j). Keep unused positions in this reserved prefix unavailable for loans. From the suffix [r_j,C), lend to oldest unpaid anchors in order, with no key or depth filter. A loan of t uses the next t suffix units and the next t residual demands of its recipient, and advances both cursors. Continue until the suffix is exhausted or no debt remains. Retire the pool, including unused units; never revisit it or lend it to a future anchor.

Accept a cut if and only if all residual demands are paid at the end of that one period. UD consists of the source walks with at least one successful physical block cut. The construction is deterministic for each cut; all cuts are finite alternatives, not jointly available budgets.

Actual q_j is used to identify source signs and verify own demands, but it is NOT substituted for the reservation ceiling. The rule may decline actual spare units when the historical ceiling is loose. This is not exact aggregate surplus allocation in renamed notation. Successful-cut availability remains unproved on arbitrary walks; there is no new unknown allocation witness or optimizer in the definition.

## No credit reuse, even with arbitrary sharing

Positive-local pools are distinct, and later loans touch only their residual tails. A recipient's residual cursor advances through disjoint half-open intervals, so different payers cannot pay the same B demand. A single payer can help several anchors and a single anchor can receive from several payers, with no change to this cursor argument.

Each nonpositive physical pool is visited once. Its own work occupies [0,q_j), within [0,r_j). All outgoing loans occupy disjoint consecutive slices of [r_j,C). Bounds from multiple anchors produce only one minimum, one reservation and one outgoing cursor. Spent units never reappear when a fact is retained or used again. All identities include physical source occurrences, not merely keys or depths.

At the end of a pass let D be the sum of all unpaid residual lengths. Every other B demand is paid once, using distinct actual A units, so

    paid B demands=Q_B-D,
    unused A units=2A-(Q_B-D).                 (6)

When the pass accepts, D=0. Its explicit injection proves Q_B<=2A. A rejected pass retains its unpaid tails and supplies no full-cycle certificate. No prefix, earlier lap, later lap or alternative-cut unit can fill that gap.

This argument is uniform in tree size, fringe shape, tracked depth, number of positives, number of runs, delay, and all sharing multiplicities. No bound on h_i, no root alignment potential and no terminal matching is required.

## Containment of the shallow procedure by total debt

Removing eligibility can change which anchor receives a particular earlier pool. It would be invalid simply to assume that each individual debt is no larger than under SL. Instead compare TOTAL remaining debt after every scanned block, on the same physical cut.

Both algorithms encounter the same source positive blocks and retain all of them. At a nonpositive block j, SL's history facts for its key form a subset of UD's facts. Where the SL subset is nonempty, the UD minimum is no larger; therefore r_UD<=r_SL and S_UD>=S_SL. With no eligible SL fact, S_SL=0, and the latter inequality still holds. This comparison is independent of how previous loans were allocated, because neither algorithm deletes paid source facts.

Let D_U and D_S be total unpaid debt just before a block. Initially both are zero. At a positive block both add the same delta_i. At a nonpositive block, every UD pending anchor is eligible, so UD exhausts its certified spare until either the pool or total debt is exhausted:

    D_U'=max(0,D_U-S_UD).                       (7)

SL can use no more than S_SL, possibly less because of its eligibility restrictions. Hence

    D_S'>=max(0,D_S-S_SL).                      (8)

If D_U<=D_S, monotonicity and S_UD>=S_SL imply

    D_U'<=max(0,D_S-S_SL)<=D_S'.                (9)

This inductive invariant holds throughout the period. Every successful SL cut has final D_S=0, so UD's nonnegative D_U is also zero. Thus EVERY successful old cut remains successful, and SL is a subclass of UD. No claim that old individual recipient allocations remain unchanged is needed; the fixed controls actually exhibit changed allocations.

UD02 shows a reachable source cycle rejected by SL at every cut and accepted by UD. Consequently SL is strictly contained in UD, and the original CD case UD\SL is now settled by this construction.

## Boundary cases and limits

With no positive blocks all own demands pay locally. If every block is positive and the period is nonempty there is no lender and every cut rejects. An empty history retires a nonpositive pool without banking it for future positives. Zero post-height, KEEP-less payers, zero-double genuine B zigs, root no-ops, repeated keys, blocks crossing the input seam and arbitrary fringes are all covered by (2)-(9).

Rotation of a source cycle permutes physical block cuts, so membership is rotation-invariant. Success of every cut and uniqueness of its allocation are not asserted. The criterion applies to the actual paired source walk; projection closure or a borrowed setup credit is insufficient.

The remaining complement is walks where no prescribed conservative one-period pass clears all debt. No universal bound on that complement or universal successful-cut theorem is established. The four-rule gate authorizes this one restricted extension, not an automatic campaign to settle that remaining issue. Stage 11G, old proof statuses, the frozen matching-terminal line and all source files remain unchanged.
