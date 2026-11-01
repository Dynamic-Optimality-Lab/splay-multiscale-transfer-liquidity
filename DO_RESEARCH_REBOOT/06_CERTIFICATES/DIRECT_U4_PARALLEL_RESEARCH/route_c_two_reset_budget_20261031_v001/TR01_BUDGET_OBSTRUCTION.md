# B-only upper excess and a multi-reset obstruction

Status: PROVED—UNIVERSAL for the block inequality E<=G_B on finite closed actual source walks. PROVED—RESTRICTED DOMAIN for the resulting exclusion on the two fixed recurrent B orders below and their stated fringe families. No requested FI-only closed walk is obtained, and universal CD remains OPEN.

## The source inequality

KEEP x splays A and B. DELETE x splays A only and leaves the key set intact. Use cyclic maximal A-root blocks: every nontrivial block i has an actual leader cost a_i>=1, measured in grouped A StepEvs, and B-double count q_i. Put delta_i=q_i-2a_i and

    E=sum_i max(delta_i,0).

While A's root stays fixed, every request is that same key. Therefore at most one KEEP in a block changes B; further KEEPs are B-root no-ops and contribute no B doubles. For a positive block, that unique B request has q=q_i>=3. Distinct positive blocks correspond to distinct actual KEEP occurrences. Consequently

    E=sum_(positive i)(q_i-2a_i)
     <=sum_(positive i)(q_i-2)
     <=sum_(all KEEP requests t) max(q_B(t)-2,0)
      =G_B.                                   (1)

This is independent of A's shape, reset targets, sharing, frame ceilings, initial setup owners or credit choices. A starved KEEP with a=0 at the request level is still part of its positive-cost cyclic leader block; it does not invalidate the deduction of two units per positive block. Multiple zero-cost requests and zero-double B zigs retain their actual event identities and contribute zero to the right-hand maximum when appropriate.

If A=0 in a closed walk, every request uses one fixed A root. B can change at most once and exact closure forces no change, so Q_B=E=G_B=0. Empty/one-key cases follow. Thus (1) holds throughout the stated closed-walk domain without an unfunded open-prefix exception.

Let C_D=sum 2a_j over KEEP-less blocks. CW01 proves constructively that E<=C_D implies an old-UD accepted physical cut. Combining it with (1) gives an independently necessary condition for strict FI-only coverage:

    FI accepted AND every UD cut rejected
      implies E>C_D and therefore G_B>C_D.     (2)

This is not an assertion that G_B>C_D is sufficient or that it holds on all walks. It is an A-independent necessary budget filter.

## Reset count versus available B excess

Every positive-cost KEEP-less block has a_j>=1 and hence at least two actual A units. If a cycle contains r such blocks,

    C_D>=2r.                                  (3)

For a complete recurrent B round repeated p times, two effective pure resets per round give r>=2p, so C_D>=4p. The gated path-reset policy is the cheapest exact case: each effective DELETE accesses a depth-two proper ancestor of the next KEEP target, so a_D=ceil(2/2)=1 and two slots provide exactly 4p. If a slot falls back to a root no-op it does not qualify as an effective two-reset cycle. More expensive or more numerous pure reset blocks only increase (3).

Thus a cheapest two-reset construction needs G_B>4 per B round, at least FIVE integer B-surplus units. A total B cost increase alone is insufficient: the relevant quantity is the positive part above two doubles per contributing KEEP.

## The old recurrent order cannot support two pure resets

For the old KEEP skeleton

    W=13,11,12,9,10,7,8,5,6,3,4,1,2,

the exact recurrent B double counts are

    5,3,1,2,1,2,1,2,1,2,1,1,1.

Only the first two positions can supply positive surplus, with maxima three and one. Its G_B is four per round. Hence for ANY A trajectory and ANY A-only reset choices on a closed cycle containing p complete recurrent rounds and at least 2p positive-cost KEEP-less blocks,

    E<=4p<=C_D.                               (4)

Old UD accepts some cut. This rules out strictness for multiple pure resets on that source B cycle without enumerating reset positions, keys or A trees. It is stronger in quantified scope than the earlier single-reset finite classification, but remains restricted to that B orbit/funding density.

## The fixed new order also fails the necessary budget

The predeclared four-bit-reversal order restricted to thirteen keys is

    V=1,9,5,13,3,11,7,2,10,6,4,12,8.

From R13, its B source reaches a fixed whole-round state after one round. The exact recurrent double counts are

    1,2,3,2,2,3,2,1,2,2,2,2,3.

Only keys 5,11,8 have q=3, each supplying at most one positive unit. All other positions have q<=2. Therefore G_B=3, even though its total Q_B=27 exceeds the old order's 23. For any source closed A/B cycle with p complete recurrent V rounds and at least 2p positive-cost KEEP-less blocks,

    E<=3p<4p<=C_D.                             (5)

This excludes every admissible member of the gated 78-policy family. No A-policy recurrence or FI/UD all-cut search is needed: each possible successful two-reset cycle would already have an accepted UD cut by (5). The predeclared B-budget stop applies, so zero A-policy cases were executed. This conclusion does not assert that non-diagonal cycles are absent; their requested E>C_D condition is impossible in this architecture.

## Why the resulting old coverage has no credit reuse

For completeness, CW's source-unit construction uses a positive debt step +delta_i, a KEEP-less capacity step -2a_i and zero for other nonpositive blocks. When E<=C_D, cut after a MINIMUM cumulative sum; every suffix sum is nonpositive, so D'=max(0,D+v_i) ends at zero. Unused capacity is retired, never banked.

Each positive pays its first 2a_i doubles locally. Residual cursors then use consecutive units of each actual KEEP-less pool once. Other nonpositive KEEP blocks pay their own work locally. Units are (physical occurrence,A-event index,bit), and B demands are (physical occurrence,B-event index). Distinct pools, disjoint unit slices and monotone demand tails give an explicit injection. Old UD can use at least this much repayment capacity, since every pending KEEP-less payer has ceiling zero. No upper-bound slack such as 4p-3p is a new spendable pool.

No reachability-prefix, second-lap or alternative-certificate credit is used. Current B-only validation does not claim a newly executed A map or a new source pair cycle; the conditional old coverage follows from this established construction for any actual A cycle satisfying the source counts.

## Exact scope and limits

The theorem applies to complete recurrent B periods and their rotations/powers with the stated reset-count density. It does not classify arbitrary transient fragments, cycles with fewer effective KEEP-less blocks, different B initial orbits, other KEEP skeletons or all multi-reset walks. In particular, two syntactic DELETE requests are not enough to infer (3) with r=2: they must be distinct positive-cost KEEP-less leader blocks, as the gated effective resets would be.

The B profiles are finite-exact source identities, independently replayed in both orientations. TR02 lifts them structurally to arbitrary unrequested fringes without evaluating a larger finite n. Strict FI-only existence and universal Step 3/CD remain OPEN. No matching-terminal work or Stage 11G artifact is changed.
