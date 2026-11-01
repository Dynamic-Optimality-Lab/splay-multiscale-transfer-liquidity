# A strictly smaller source charging class is proved

Status: PROVED—RESTRICTED DOMAIN. For every finite reachable closed walk satisfying the two conditions below, Q_B<=2A, with arbitrary n, KEEP support, walk length, DELETEs and fringes.

Split the cycle into maximal A-root blocks, each with leader A cost a_i>=1 and B-double count q_i. Write delta_i=q_i-2a_i. For each positive block i require:

1. The next block's key y is at B depth at most 1 immediately before i's nontrivial B splay.
2. delta_i<=2a_(i+1)-1. For unit-positive blocks this is automatic.

The source carries the old B root and its children to depth at most 3. Hence the successor has at most one B double and deficit at most 1-2a_(i+1). The pair sum is nonpositive. Successors are forced negative, making the positive/successor pairs disjoint; remaining blocks pay locally. The proof includes an explicit assignment of actual two-per-A-StepEv credits with no reuse.

This strictly extends the banked 26AJ former-root successor class by admitting old children. A predeclared reachable seven-key cycle has a positive (a,q)=(1,3) followed by an old-child successor with (a,q)=(2,0). It closes with A=31,Q_B=11,Z_B=16. Independent pointer verification checks every event, all 44 cyclic cuts across both orientations and all individual credit assignments. An analytic extension has unbounded genuine KEEP support; no larger finite instance is evaluated.

The [complete theorem](SC01_RESTRICTED_CHARGING_THEOREM.md), [reachable witness and strict-coverage family](SC02_REACHABLE_WITNESS_AND_UNBOUNDED_SUPPORT.md), [independent audit](independent_audit.json), and [strategy review](SC03_STRATEGY_REVIEW.md) state the exact scope. The depth component is already implied by earlier work; the new result is the charging class, not a rebranded depth theorem. Named older-domain exclusions are checked from their pinned hypotheses, without running their recognizers.

The [four-rule gate](SC00_FOUR_RULE_GATE.md) and [preexecution analytic-family addendum](SC00A_PREEXECUTION_UNBOUNDED_SUPPORT_FAMILY.md) preceded the source audit. One restricted original CD case is now settled. Universal Step 3 and CD remain OPEN because S1-S2 have not been proved for every walk. The matching-terminal line stays frozen, no fits or graph searches were run, and all 125 Stage 11G files and old research are preserved.
