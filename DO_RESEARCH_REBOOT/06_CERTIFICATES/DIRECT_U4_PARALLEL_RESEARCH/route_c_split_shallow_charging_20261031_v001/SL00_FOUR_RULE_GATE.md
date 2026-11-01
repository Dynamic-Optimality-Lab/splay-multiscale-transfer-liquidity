# Gate for split shallow payers

2026-10-31, Asia/Karachi. Extend cut-certified cross-run shallow charging to partial repayment by multiple payer pools, without reused credits. The matching-terminal line remains frozen. Old source/research/status/Git/Stage 11G files are read-only. New outputs are exclusive to this run.

## One explicit ledger construction

Scan one cyclic A-root-block period from a chosen cut. Positive block i pays its first 2a_i B doubles locally and leaves delta_i=q_i-2a_i individual demands. Record those demands and retain i's pre-B root/child set and actual post-B heights as source-bound facts. Keep those facts even after its demands are fully paid; they are not credits.

At each nonpositive block j, take all already-seen positive anchors whose shallow set contains j's key, including paid anchors. Their valid delayed bounds on the SAME q_j give c_j as their minimum. If there is no such fact, reserve the whole 2a_j pool and lend nothing. Otherwise reserve r_j=min(2a_j,c_j) units for own work and let S_j=2a_j-r_j. Since q_j<=2a_j and q_j<=c_j, own q_j fits in the reserved prefix.

Freeze that reservation ONCE for j. Lend at most S_j to currently unpaid, eligible anchors, oldest eligible first. Advance each anchor's residual-demand cursor and j's outgoing-unit cursor. Ignore unused capacity after j; no reusable bank or promised pool is retained. No pool is processed a second time. Accept a cut exactly when all residual demands are paid at the end of one period; try all cuts. Failed cuts receive no prefix or next-lap credit.

Retaining paid source facts is load-bearing for preservation of XR: partial repayment must not remove the best own-work bound at a later old XR closing payer. The history is complete and untruncated; only debts are removed. All source bounds are actual whole-splay bounds, counting zero-double B-changing zigs as interventions.

## Four rules

1. **Strictly smaller — PASS.** One deterministic oldest-eligible partial-repayment procedure with source-shallow eligibility and conservative per-pool reservations. No general matching, flow, backtracking, optimal allocation, potential or claim that every walk succeeds. It is a restricted source class, not full CD in new variables.
2. **Concrete reason — PASS.** The established depth bounds certify own work. The reserved prefix and outgoing suffix are disjoint; demand cursors are monotone and pools occur once. An exact conservation invariant accounts for every source unit and residual demand. Full source history gives a direct induction preserving every successful XR cut, without an additional open capacity lemma.
3. **One bounded audit — PASS.** Prove the ledger, its no-reuse and XR-containment theorem. Audit the fixed thirteen-key source word below and reflection, preserve the eight prior XR/SP/DS/SC controls, and check all cuts honestly. No word search, larger finite key size, fit, graph, allocation optimizer or automatic successor. If the fixed strict witness fails or XR already accepts it, stop promotion rather than search for a replacement.
4. **Original connection — PASS subject to the exact strict check.** Success settles CD on a strictly larger cut-certified source class. Strict coverage requires a reachable word with one anchor actually split across distinct pools and no successful XR single-payer cut. Universal cut success, unrestricted allocation, Stage 11G and global CD remain OPEN.

## Fixed cross-run essential-split witness

Start diagonally at R13. Prefix D13,D12 reaches A=S_12(S_13 R13), B=R13. Freeze

    K13 D11 K12 K2 D1 D2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D13 D12.

Predetermined source calculations:

    K13: a=1,q=6,delta=4;
    D11: a=3,q=0,delta=-6;
    K12: a=1,q=3,delta=1;
    K2:  a=1,q=0,delta=-2;
    D1:  a=1,q=0,delta=-2;
    D2:  a=1,q=0,delta=-2.

The bridge separates the positive anchors. It lends nothing because key 11 is not eligible. At KEEP2 the late anchor's h=1,k=0 gives own-work ceiling 0; its two units pay two of the first anchor's four residual demands. DELETE1 lends its two units only to the first anchor (key 1 is absent from the second anchor's shallow set). DELETE2 lends one unit to the second anchor. Thus the first anchor is split across two pools, and no pool clears the entire pending batch.

Subsequent B depths at KEEP3,...,KEEP13 are expected to give q<=2; A changes root at every such request, so no extra positive is created. The common ascending scan synchronizes both trees by KEEP13. Full common scans restore R13; final D13,D12 restore the cycle's initial A. Verify rather than assume all of this.

XR should reject every cut: a cut that encounters the first positive must also retain the following positive before any qualifying one-pool closure. Their common key is 2 and total excess is 5. Early eligible pools have only two units; later key-2 source ceilings defeat the single-pool threshold. A cut ending between the anchors leaves the first one unpaid. Check the complete finite cut list; do not infer rejection from only cut 0.

The construction uses the same thirteen-key size already audited, with no fit. For n>=13, prefix D13,D12 and fixed requests <=13 commute with the untouched right fringe. Use common scan ranges up to n and end D13,D12. This proves an unbounded-support family analytically, without evaluating another finite n. The fixed <=13 word also commutes with an arbitrary unrequested BST graft at key 13's right child.

## Required accounting and stop

Verify every raw BST, source event, prefix, full paired closure, intervention count, reservation, own-demand placement, partial transfer, per-anchor cursor and per-payer unit. Account for all seen source facts even when their debt is zero; never turn retained facts into spendable resources. Every accepted cut has one complete budget; rejected cuts retain explicit unpaid demands. Alternative certificates are not pooled.

Check every prior successful XR cut remains successful and old source rows/totals stay unchanged. New allocations may differ because own-work reservations now precede lending. No old recognizer is imported. Record the exact restricted case removed, assumptions, BEFORE/RESULT/AFTER and the remaining complement. Preserve all earlier counts/statuses and all 125 Stage 11G files and their inventory. No Stage 11G code, old status writer, Git mutation or installer is used. No automatic unrestricted-allocation campaign follows.
