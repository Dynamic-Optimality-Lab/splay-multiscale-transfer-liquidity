# Shallow charging across distinct positive runs

Status: PROVED—RESTRICTED DOMAIN. The cut-certified greedy batching class below admits one payer shared by positives from distinct maximal positive runs, with no reused credit. It strictly contains SP's one-payer-per-positive-run class.

The source restrictions remain explicit: one common shallow key and one sufficient physical A pool per closed batch. No claim is made that every reachable walk admits this construction. No terminal potential, global matching, optimizer or unrestricted allocation theorem is introduced. The matching-terminal line stays frozen.

## Source blocks and inherited depth bounds

Use cyclic maximal A-root blocks. Each block i has one leader of cost a_i>=1, followed by zero-A-cost requests of its key, and at most one nontrivial B splay. Let q_i count its B doubles and delta_i=q_i-2a_i. Then sum_i delta_i=Q_B-2A.

For a positive block i let T_i be B immediately before its nontrivial B splay. Let C_i contain T_i's root and its original nonempty children. For y in C_i, let h_i(y) be its actual depth immediately after the splay. The source root/child theorem gives h_i(y)<=3. If k_i(j) counts all genuine B-changing KEEPs strictly between i and proposed payer j, the source one-splay displacement bound gives

    q_j<=c_i(j)=floor(h_i(y)/2)+k_i(j).

Count zero-double zigs; omit DELETEs and B-root no-ops. If j has no KEEP, put c_i(j)=0. These are the already-established SC/DS source facts; their proof is not replaced by a fit or counted as new advancement here.

All bounds refer to the same physical key y at the same payer access. For a pending positive-anchor set P, require y in C_P=intersection_(i in P) C_i and use

    E_P=sum_(i in P) delta_i,
    c_P(j)=min_(i in P) c_i(j).

Then q_j<=c_P(j). The minimum is an own-work ceiling, not spendable credit or multiple copies of the pool. An empty intersection permits no payer under this rule.

## One-period scan for a chosen block cut

Fix a cyclic A-root block cut. Process exactly m distinct blocks, once each, in their cyclic order. Initialize an empty pending batch.

At a positive block, retain its complete identity, add its delta to E and intersect its shallow set into C. Start a new pending interval if the batch was empty. Ending a maximal positive run does NOT reset the pending batch.

At a nonpositive block j:

- With no pending anchors, pay j locally.
- With pending anchors, test whether its leader key is in C and whether

      E+c_P(j)<=2a_j.                             (B)

- If the test fails, j pays locally and its unused capacity is not carried forward. Retain every pending positive.
- If the test passes, close the batch immediately at this first qualifying payer, assign its pool as below, and reset the pending batch to empty.

Positive blocks cannot be payers. The actual threshold (B) derives delta_j=q_j-2a_j<=-E<0. Its A cost is the actual block LEADER cost, which may be a DELETE; a later starved KEEP does not replace that cost.

At the end of exactly one period, accept this cut only if the pending batch is empty. An unfinished batch rejects the cut. No startup, prefix or second-lap credit is available to clear it.

The cyclic walk belongs to the new restricted class if at least one of the finitely many block cuts yields an accepted pass. Try the cuts explicitly; a certificate records its selected cut. This is a concrete finite trace test, not an assumed global capacity witness.

## Sequential ownership replaces the old run-gap argument

A closed batch contains all positive blocks encountered since the preceding closure, plus the intervening nonpositive blocks and its payer. It may contain multiple distinct positive runs. No positive is skipped merely because a negative bridge occurred.

For a fixed accepted pass, closed batch intervals are disjoint in the one-period order: after closing at j, processing resumes strictly after j with an empty batch. The next batch cannot own any block of a completed one. Nonpositive blocks outside batches pay locally. Every positive is covered, since otherwise pending work would remain at the end and the pass would reject.

This does not assume the old SP cells remain disjoint after crossing positive runs. The one-pass ownership rule supplies a new disjoint partition directly. Every physical source block and event occurs only once in the selected period, including when its interval crosses the original input seam.

## Explicit shared-pool slices and no reuse

Give every actual A StepEv two distinguishable units. Each pending positive i pays its first 2a_i B doubles locally; exactly delta_i demands remain. At closure, list pending anchors in encounter order and concatenate their residual demands, totaling E.

Number the payer's 2a_j units by A event and bit. Assign successive disjoint slices of lengths delta_i to the anchors, occupying [0,E). Pay payer j's own q_j demands from [E,E+q_j). These fit because

    E+q_j<=E+c_P(j)<=2a_j.

Every other nonpositive block pays locally with q_i<=2a_i; its unused units are not lent. Closed batches are disjoint, positive-local pools are distinct, and all slices within the single payer pool are disjoint. Thus every B double receives exactly one actual unit and every A unit is used at most once.

The payer's own B demand and actual A pool are each counted once, irrespective of how many anchors produced source bounds. Repeated intervention histories in those bounds do not create credits. Alternative accepted cut certificates are also alternatives, not additional resource pools to combine.

Summing these assignments proves Q_B<=2A for every reachable closed walk in the accepted class. This is scalar closed-walk charging, not an online guarantee or a claim about the refuted creator/setup eligibility graph.

## Cut semantics and boundary cases

Membership is invariant under rotation of the source cycle: all physical block cuts are tested, and rotating the input simply permutes that set. A particular linear pass may reject when the cut divides an unpaid batch. The selected cover may depend on which successful cut is chosen. Neither all-cut success nor a unique physical greedy cover is claimed.

Every successful cut has its own complete one-period no-reuse proof. A rejected pass can have closed some earlier batches; its remaining unpaid anchors prevent promotion to a full-cycle certificate. Unrolling another period would add another resource budget and is not permitted.

With no positive blocks, all demands pay locally. With A=0, the closed-walk same-root argument gives Q_B=0. Empty/one-key/empty-walk cases follow. An all-positive pass has no payer and rejects. Empty common sets, insufficient leader cost or debt stranded at the end likewise reject the cut rather than imply a CD counterexample.

The procedure is deterministic for a fixed cut. Its success is sufficient, and is the defining restriction of this class. No completeness for arbitrary possible packet covers, global optimality or backtracking allocation is claimed.

## Containment of SP and strict new coverage

For an SP member, choose a cut at the start of one of its maximal positive runs. While scanning that run, the pending set and total excess become exactly SP's run anchors and excess. The first qualifying payer in its following nonpositive gap is the same SP payer. The batch closes before the next positive run. Repeating through the period clears all pending work before returning to the initial cut. Thus every SP walk has an accepted cut, and zero-positive cases agree.

XR02 supplies a reachable strict witness: a DELETE separates deficits 2 and 1 into distinct runs; the first run has no eligible payer in its own gap, so SP rejects. The new scan retains it, adds the second run and closes both at one later common payer. Six earlier SP/DS/SC witness controls are preserved exactly. An analytic extension has unbounded genuine KEEP support.

The original restricted CD case for this cut-certified cross-run class is settled. Universal Step 3 and CD remain OPEN. General successful-cut availability, arbitrary split payers, backtracking covers and unrestricted shared allocation are not established. No Stage 11G graph, predicate, certificate or status is changed.
