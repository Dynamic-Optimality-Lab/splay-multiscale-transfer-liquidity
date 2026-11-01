# Cross run shallow batching is proved without reused credit

Status: PROVED—RESTRICTED DOMAIN. The new source class allows one delayed payer to cover positives from distinct maximal positive runs and strictly contains SP's per-run class.

For a chosen cyclic cut, process one period. Retain every unpaid positive block across nonpositive bridges; maintain total excess E and the intersection of their source root/child sets. Close at the first nonpositive block whose key is common and whose actual leader A pool satisfies E+min_i c_i<=2a. Assign separate slices of that pool to all pending anchors, then pay the payer's own B work once. Other blocks pay locally. Sequential closure/reset gives disjoint packets and no reused units.

A cut succeeds only if no pending work remains after that one period. Test all block cuts and admit the walk if one succeeds. Membership is rotation-invariant; individual cuts may fail. Failed cuts receive no second-lap or prefix credit. This is the stated restricted procedure, not a complete arbitrary allocation algorithm.

The strict thirteen-key witness has deficits 2 and 1 separated by DELETE11. The first run has no SP payer before the second positive, so SP rejects. The batch retains both and closes at KEEP2 with a four-unit pool and binding threshold 3+1=4. The cycle is reachable and closes with A=62,Q_B=35,Z_B=28. Its 38 successful and four rejected cuts are independently checked. An analytic extension has unbounded KEEP support, with no new finite key size or fitting campaign.

Across new/reflected and preserved controls, independent verification checks 256 cut trials and 186 selected-cover credit assignments. All six prior SP/DS/SC words are unchanged and remain accepted. See the [source theorem](XR01_CROSS_RUN_BATCHING_THEOREM.md), [strict witness and family](XR02_DISTINCT_RUN_WITNESS_AND_FAMILY.md), [independent audit](independent_audit.json), and [strategy review](XR03_STRATEGY_REVIEW.md).

The [four-rule gate](XR00_FOUR_RULE_GATE.md) preceded execution. One further restricted original CD case is settled. Universal successful-cut availability and general shared allocation are not proved; universal Step 3 and CD remain OPEN. The matching-terminal line remains frozen, all 125 Stage 11G files and previous research are preserved, and no automatic successor campaign is launched.
