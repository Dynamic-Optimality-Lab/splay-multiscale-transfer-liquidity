# Delayed shallow charging is proved without credit reuse

Status: PROVED—RESTRICTED DOMAIN. The new class strictly contains immediate shallow-successor charging and permits arbitrarily delayed private payers.

For a positive A-root block i, take a candidate payer key from B's root or children immediately before i's B splay. Let h<=3 be its actual depth immediately afterward, and let k count genuine B-changing KEEPs before the payer, including zero-double zigs. The source gives

    q_payer<=floor(h/2)+k=c.

Require the source A threshold delta_i+c<=2a_payer and choose the first qualifying payer before the next positive block. If the payer has no KEEP, use c=0. Intervening nonpositive blocks pay themselves locally. Each positive owns an interval inside its own gap, so the intervals and payer credit pools are disjoint. Explicit two-per-A-StepEv assignments pay every B double with no reused unit. This proves Q_B<=2A on the stated class.

Every old SC walk is included with k=0. The new reachable witness has a genuine intervening KEEP and fails SC's immediate depth condition. Its delayed payer has h=1,k=1,c=1,a=1 and a binding threshold 1+1=2. The cycle closes with A=30,Q_B=12,Z_B=16. Independent verification also preserves both old SC witnesses, checks every one of 90 cyclic cuts and verifies all 46 credit assignments across the four cycles.

The [full source theorem](DS01_DELAYED_PRIVATE_PAYER_THEOREM.md), [strict witness and unbounded-support family](DS02_STRICT_DELAYED_WITNESS_AND_FAMILY.md), [independent audit](independent_audit.json), and [strategy review](DS03_STRATEGY_REVIEW.md) state the scope. The [four-rule gate](DS00_FOUR_RULE_GATE.md) preceded execution. No larger finite fit, graph search or allocation optimizer was used.

One further restricted original CD case is settled. Existence of a qualifying payer in every positive gap is not proved universally; shared payers and intervening positives are not covered. Generic Step 3 and CD remain OPEN. The matching-terminal line stays frozen, all 125 Stage 11G files and previous research are preserved, and no automatic successor campaign is launched.
