# FE soundness, physical-unit accounting and preservation of PF

**Theorem C — PROVED—UNIVERSAL.** On every admissible finite closed Pair
Access walk, every PF-successful physical cut is FE-successful. Thus
PF is a subset of FE as closed-walk certificate classes. This theorem
alone does not assert strictness or completeness; FE04 proves strictness
on the designated inherited source family.

## 1. The separate FE procedure

Keep exactly RC01/PF01's cyclic maximal A-root blocks, capacities C_j=2a_j,
positive excess delta_j=q_j-C_j, genuine B-change clocks and all KEEP/DELETE
semantics. FE02 defines the ONLY new quantity, the source ceiling c_FE.
It refines the FIRST genuine intervening change exactly; all later ones
retain the same +2 bound. No FI/PF procedure or old certificate is edited.

Fix one physical block cut and scan one period with empty source history,
zero residual queue and no startup units. At a positive block use all C_j
actual units for its first C_j B-double demands, append its remaining
delta_j demands in source order, and retain its positive source fact.
Positive pools never lend. At a nonpositive block retain ALL encountered
positive facts, including paid anchors, and compute ONCE

    r_FE,j = min(C_j, min_encountered_i c_FE(i,j)).             (1)

With empty history put r=C_j. Each individual c_FE>=q_j by FE02; also
q_j<=C_j by nonpositivity. Hence the minimum still satisfies q_j<=r.
Pay own work from the first q_j units of [0,r). Only [r,C_j) may lend,
oldest residual first, in increasing physical-unit order. Advance demand
cursors after each loan and retire the pool after this visit. Unused
reserved positions and surplus suffix units when debt is empty are discarded.
There is no pool resurrection, banking or later recomputation of its reserve.

Choosing a smaller minimum among many valid source bounds is safe precisely
because EVERY bound dominates the same actual own q. Paid facts are valid
geometric facts, not units; retaining them neither creates nor recycles supply.
Future own demand and observed post-depth are not inputs to (1). Actual q
is used to identify/pay own demands and to check the source-derived bound.

## 2. Frozen pools, FIFO and the actual injection

Give every actual A unit identity (cycle occurrence,block occurrence,
A-event index,bit), bit0/1. Order each pool by event index then bit.
Give every B-double demand its corresponding physical cycle/block/B-event
identity; final zigs have no double demand. Repeated keys and repeated
subwords never merge physical occurrences.

Within a positive block, its distinct own units pay its first distinct C
demands; the rest enter the queue once. Within a nonpositive block, own
units are in [0,q), all loan units are in [r,C), and q<=r. Own and loan
sets are therefore disjoint. Each pool's loan slices are disjoint and it is
visited once; different pools have distinct occurrence identities. FIFO
cursors advance, so no demand is paid twice. No assignment comes from the
startup, another cut, another traversal or an undeclared additional period.

Consequently a successful FE pass gives a complete injection of all actual
B doubles into actual A units and proves Q_B<=2A. FE does not assert the
original U4 eligibility relation: this is Route C aggregate source charging.

## 3. Pointwise dominance and class inclusion

At a fixed cut, FE and PF retain the SAME positive source facts at the SAME
times independently of debt payment. Their positivity is the original
source delta, not an algorithmic residual status. FE02 gives c_FE<=c_PF
fact by fact, hence

    r_FE,j<=r_PF,j,
    S_FE,j=C_j-r_FE,j >= C_j-r_PF,j=S_PF,j.                   (2)

Both reserve C when history is empty. Positives add the same delta>0 to
both queues. Every pending anchor can receive a loan from the available
suffix under either protocol, so a nonpositive block's total-debt update is

    D_FE'=max(0,D_FE-S_FE),
    D_PF'=max(0,D_PF-S_PF).

Starting at zero, (2) and block induction prove D_FE<=D_PF at EVERY position
of the pass. Individual recipient allocations need not coincide, and this
argument never assigns private ownership of a shared payer. If PF clears at
this cut, FE clears there too. Taking the union over physical cuts proves

    PF subseteq FE.                                          (3)

This proof covers arbitrarily many retained paid/unpaid anchors and shared
payers. It is not derived from a finite corpus or from the designated word.

## 4. Boundary cases

KEEP-less payers have q=0 and every source ceiling0; their pool is counted
once in C_D. Mixed DELETE/KEEP blocks have one A pool and at most one genuine
B-changing KEEP; they are KEEP-containing, not extra DELETE pools. A B zig
advances the intervention clock even though q=0; root no-ops do not. Terminal
zig effects inside the FIRST refinement are exact as in FE02; later genuine
changes still pay the inherited +2 tax once each.

No-positive walks pay every block locally. Empty and A=0 closed walks have
Q_B=0 by the inherited fixed-root closure result. An all-positive nonempty
block cycle has no lending pool and may reject; no universal FE completeness
is asserted. Leading unfunded no-op fragments of arbitrary OPEN histories
are not covered by that closed A=0 statement. Root boundaries, repeated
coordinates, arbitrary ordered key sets, arbitrary finite lengths and both
orientations preserve the exact source and physical-unit definitions.
