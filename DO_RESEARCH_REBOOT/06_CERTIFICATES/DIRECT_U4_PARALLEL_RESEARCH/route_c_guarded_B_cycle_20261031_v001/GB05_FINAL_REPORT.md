# Source-exact recurrent B cycle: G_B=9

The requested B-only threshold is ACHIEVED at the existing thirteen-key size. A source-exact SIMPLE 24-access cycle has Q_B=38,Z_B=10 and G_B=9>=5. Its internal B states are all distinct; no repeated-period padding or fitted parameter is used.

Use local order

    1,9,5,3,11,7,2,10,6,4,12,8,

returning to guard 13 after each query. Start diagonally at T0=13(R_[1,12],empty). One guarded word reaches

    B*=13(12(8(6(4(2(1,3),5),7),10(9,11)),empty),empty),

and the next identical word returns to B*. The exact source identity gives q_query=ceil(local_depth/2) and q_return<=1, with the odd-away case retaining the local root. GB01 proves the identity; GB02 lists the full source profile and arbitrary-fringe extension.

Independent pointer verification passed in both orientations: 144 source calls, every local/global event and tree, the 24-request reachability prefix and primitive closure. The four-rule gate passed for this explicit B component. All 700 pinned earlier files and all 125 Stage 11G files with their inventory are unchanged; branch/HEAD and clean tracked status are preserved. No larger finite fit or A-reset search occurred.

There is a material coupling limitation: these guards already supply old-UD repayment. GB03 proves that only H_B=1 residual upper budget remains after their guaranteed service. Two PURE one-StepEv resets would supply C_D=4 and make the coupled class UD-covered. Thus the raw B-headroom target is met, while this particular guarded order cannot establish the desired FI-only coupling by simply inserting two pure resets.

No actual A-reset placement, E>C_D pair or FI-only closed walk is claimed. Matching-terminal work stays FROZEN. Universal Step 3/CD remains OPEN. No successor proof campaign was launched.

Evidence: GB00_FOUR_RULE_GATE.md; GB00A_COUPLING_CLAIM_AUDIT.md; GB01_GUARD_RETURN_IDENTITY.md; GB02_EXPLICIT_PRIMITIVE_B_CYCLE.md; GB03_GUARD_REPAYMENT_COUPLING_AUDIT.md; GB04_GATE_RESULT_AND_STRATEGY_REVIEW.md; guarded_B_cycle_certificate.json; reflected_cycle_certificate.json; independent_audit.json; guard_repayment_profile.json; final_integrity.json; delivery_manifest.json.
