# Shared delayed payer charging is proved without reused credit

Status: PROVED—RESTRICTED DOMAIN. The new theorem lets one physical payer cover several consecutive positive A-root blocks and strictly contains delayed private-payer charging.

For a maximal positive run R, let E_R=sum delta_i. The payer key must have been at B's root or a child before every anchor's B splay. Each anchor supplies a source delayed bound c_i=floor(h_i/2)+k_i on the SAME payer B-double count. Use their minimum c_R, and require the actual leader A threshold

    E_R+c_R<=2a_payer.

Choose the first qualifying payer in the following nonpositive gap. Reserve the payer pool once for the run's total excess; give each anchor its own contiguous slice, then pay the payer's own B demands once. Intervening blocks pay locally. Maximal-run cells are disjoint, so neither a pool nor an individual A unit is reused. This proves Q_B<=2A on the stated class.

The analytically specified thirteen-key witness has positive deficits 2 and 1, a saturated intervening KEEP and one four-unit payer. Its shared ceiling is min(2,1)=1, so 3+1=4 binds the source threshold. The anchors receive disjoint slices [0,2) and [2,3). The cycle is genuinely reachable and closes with A=60,Q_B=35,Z_B=28. DS rejects it because the positives are consecutive. An analytic extension has unbounded KEEP support; no size sweep, finite fit or graph search selected this construction.

Independent verification checks all 172 cyclic cuts and 116 credit assignments across new/reflected and preserved DS/SC controls. Source-domain validation also passes. See the [proof](SP01_SHARED_RUN_PAYER_THEOREM.md), [witness and family](SP02_SHARED_WITNESS_AND_UNBOUNDED_FAMILY_v002.md), [independent audit](independent_audit.json), and [strategy review](SP03_STRATEGY_REVIEW.md).

The [four-rule gate](SP00_FOUR_RULE_GATE.md) preceded execution. One further restricted CD case is settled; common-payer availability for all walks and sharing across different runs are not proved. Universal Step 3 and CD remain OPEN. The matching-terminal line remains frozen, all 125 Stage 11G files and old research are preserved, and no automatic successor campaign is launched.
