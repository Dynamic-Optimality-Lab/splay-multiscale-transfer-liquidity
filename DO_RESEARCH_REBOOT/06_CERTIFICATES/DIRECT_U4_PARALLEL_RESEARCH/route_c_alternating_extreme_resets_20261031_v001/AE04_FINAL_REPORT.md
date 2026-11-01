# Alternating-extreme attempt: exact budget exclusion, no A/B witness

The requested non-scanning A/B cycle with two one-StepEv resets and E>C_D was not found. One fixed alternative was tested under the four-rule gate:

    V=(9,5,13, 3,11,7,1, 2,10,6,13, 4,12,8,1).

This word alternates bursts ending at maximum13 and minimum1. It avoids the previous word's full consecutive descending scan tail and has no cyclic ABA. Nevertheless its exact recurrent B budget is insufficient:

    q_B=(2,3,1,2,3,3,1,1,2,2,1,2,2,3,1),
    G_B=sum max(q_B-2,0)=4.

Any admissible coupling with two effective pure one-StepEv resets has C_D=4 and E<=G_B=4, so E>C_D is impossible on this certified B orbit. The source gate therefore stopped before all 105 declared A reset-slot policies. None was executed, and no ineffective reset was counted as successful. This is a scoped exclusion of the fixed architecture, not a general nonexistence theorem.

The B orbit closes after one transient lap; its recurrent fifteen source states are distinct. The adjacent-helper diagnostic is also unfavorable, J_B=1: three positive queries are immediately followed by q=1 helpers. Independent pointer verification and reflection passed for all thirty source accesses: 60 pointer calls, 120 validated BST occurrences and every event interval/orientation. No larger finite fit, changed word, A-policy search or FI/UD cut trial was used.

The reset identity was corrected before execution: deleting the depth-two ancestor always costs one StepEv, but shortens the next target's path by one OR two edges depending on its fringe. It need not reduce the next grouped A cost. No hypothetical A cost or reachability-prefix credit was treated as cycle capacity.

The four-rule gate, exact exclusion and mandatory strategy review are complete for this bounded attempt. The general requested A/B construction and universal Step 3/CD remain OPEN; no new original CD subclass or strict FI-only coverage is claimed. No replacement word or automatic successor was launched.

All 758 earlier/source files and all 125 Stage 11G files with inventory remain unchanged, as do branch/HEAD and clean tracked state. Matching-terminal remains FROZEN.

Evidence: AE00_FOUR_RULE_GATE.md; AE01_EXACT_BUDGET_EXCLUSION.md; AE02_EXACT_PATH_RESET_IDENTITY.md; AE03_GATE_RESULT_AND_STRATEGY_REVIEW.md; B_preflight_certificate.json; budget_exclusion_certificate.json; reflected_B_certificate.json; independent_audit.json; proof_status_ledger.json; final_integrity.json; delivery_manifest.json.
