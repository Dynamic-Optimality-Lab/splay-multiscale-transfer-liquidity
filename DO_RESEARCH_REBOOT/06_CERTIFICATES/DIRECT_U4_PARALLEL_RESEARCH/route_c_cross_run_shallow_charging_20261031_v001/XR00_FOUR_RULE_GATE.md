# Gate for cross run shallow batching

2026-10-31, Asia/Karachi. The user requests source charging across distinct positive runs with no reused credit. The matching-terminal line remains frozen. Old sources, statuses, artifacts, Git and Stage 11G stay read-only. All new outputs are exclusive to this versioned run.

## One restricted construction

Use the established A-root blocks, delta_i=q_i-2a_i. For a chosen cyclic block cut, scan exactly one period. Start a pending batch at the first unpaid positive block. Add EVERY subsequent positive block to it, even across nonpositive bridges. Maintain their total excess E and the intersection C of their pre-B-splay root/child key sets.

At each nonpositive block j, test its leader key y. If y is in C, every pending anchor i supplies the established delayed bound c_i(j)=floor(h_i(y)/2)+k_i(j), counting every genuine intervening B change, including zero-double zigs. Use c=min_i c_i(j), or c=0 for a KEEP-less payer. Close the pending batch at the FIRST block satisfying E+c<=2a_j. Split the actual payer pool into distinct anchor-excess slices, then pay its own B work once. Other nonpositive blocks pay locally. Reset only when the pool has closed the batch; never reset just because a positive run ended.

Reject a cut if any pending batch remains at the end of that ONE period. Try all cyclic block cuts and admit the walk if at least one complete pass succeeds. A failed cut does not borrow from another lap. A selected successful pass partitions its positive-containing intervals sequentially, so packets are disjoint by construction.

The class is this explicit cut-certified greedy procedure. No completeness for arbitrary possible packet covers or global allocation is claimed. A particular cut may fail while another succeeds; only membership is rotation-invariant. Alternative accepted certificates are not pooled together.

## Four rules

1. **Strictly smaller — PASS.** One common shallow key and one payer per sequential batch, with a concrete leader A-cost threshold. No split payers, cross-batch reuse, general matching, global potential or unknown witness. Failure of the procedure excludes the walk from this restricted class rather than reformulating universal CD.
2. **Concrete reason — PASS.** Pending anchors give sound upper bounds on the same payer q; their minimum is used once. E+c<=2a gives an explicit concatenation of disjoint credit slices. One-pass closure and reset make packet ownership disjoint. The source bound is established; no new open geometry or capacity premise is needed beyond openly restricted source admissibility.
3. **One bounded mechanism — PASS.** Prove the scan and its no-reuse theorem; audit the one fixed thirteen-key construction below and reflection, plus unchanged acceptance of all six prior SP/DS/SC source controls. No word hunt, fit, size sweep, source-state graph, optimizer or automatic successor. Stop if this fixed witness or strict coverage fails.
4. **Original connection — PASS subject to the exact witness check.** The accepted class settles an original restricted CD case and contains SP: cutting before an old positive run reproduces its first-payer closures. Strict new coverage requires distinct positive runs whose first run has no SP payer in its own gap, but the cross-run pending batch closes. Universal CD, general cut admissibility and arbitrary shared allocation are not promoted.

## Analytic strict witness

Retain the prior thirteen-key diagonal R13 and prefix D9. Insert a SINGLE DELETE11 between its first two positive KEEPs:

    K13 D11 K12 K11 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D9.

Predetermined source calculations give:

    K13: a=2,q=6,delta=2;
    D11: a=2,q=0,delta=-4;
    K12: a=1,q=3,delta=1;
    K11: a=1,q=2,delta=0;
    K2:  a=2,q=0,delta=-4.

DELETE11 changes A but freezes B, creating distinct maximal positive runs. Its key 11 is not in the first anchor's shallow set {1,2}, so the first run has no SP payer before the second positive. After the subsequent KEEP11 the full pair should equal the prior SP witness's pair after KEEP11. Its suffix therefore closes unchanged.

The common payer key remains 2. Pending excess is 3; the two source ceilings remain 2 and 1 because DELETE11 adds no B tax. Thus 3+min(2,1)=4=2a_payer. The payer must use the same distinct slices [0,2) and [2,3); neither the DELETE bridge's spare capacity nor the saturated KEEP11's pool may be lent. Check the actual source and exact closure, not just these arithmetic expectations.

This witness is analytically derived from the already-certified SP construction at the SAME size; it is not selected by a larger finite fit. Reflect it. Preserve the six old SP/DS/SC words unchanged and verify their accepted covers. Check all cut trials, including honest rejection when a cut splits an unpaid batch.

For every n>=13 the same local prefix and extra DELETE11 lift under the untouched right fringe at 13; use common scan ranges up to n, ending D9. The source pair after the local KEEP11 rejoins SP's pair, so synchronization by KEEP10 and the common-pass closure extend analytically. Prove arbitrary rigid fringes and unbounded genuine KEEP support without evaluating another n.

## Verification and stop

Verify all source rows in both orientations with the pointer engine, exact ranked BST inputs, prefix reachability, paired closure, every source bound and intervention count, earliest closure at each chosen cut, the complete positive-anchor set in each batch, and no prefix or second-lap credit. Every actual B double must have one distinct A-StepEv/bit unit. Check that rejected cuts retain unpaid anchors and are not treated as proofs.

Record BEFORE/RESULT/AFTER, restrictions and the exact restricted original case discharged. Do not count the inherited displacement facts as new advancement. No claim is made that all source walks pass the greedy cut test. Preserve all earlier counts/statuses and all old bytes; keep the matching-terminal line frozen. Pin and rehash every one of the 125 Stage 11G files and their inventory. Do not execute Stage 11G code, old status writers, Git mutations or installers. No automatic full-allocation successor is launched.
