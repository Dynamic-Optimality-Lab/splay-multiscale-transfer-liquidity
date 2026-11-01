# Exact amplification and return found, below the requested bounds

There is now a source-exact non-scanning amplification-and-return identity for the seed. From(R13,R13), execute

    D3,D5,K7,
    K6,K5,K3,K7,K1,K4,
    K2,K6,K4,K1,K3,K2,K5,K4,K2,K1.

It returns exactly to(R13,R13) after19 actions, with exactly two pure one-StepEv resets. The six-KEEP middle extension raises positive excess from one to two; its final K4 has a_A=1,q_B=3. The final ten KEEPs supply an explicit shared return, without a full consecutive-key core scan. The paired cycle has19 distinct source states before closing.

The actual totals are

    A=24, Q_B=21, Z_B=8,
    E=2, C_D=4, G_B=2, J_B=0.

Thus this is a BELOW-THRESHOLD control, not the requested E>C_D,G_B,J_B>=5 witness. Both positive queries are followed by q_B=1 helpers, and the cycle contains diagonal states. It is already covered by the existing DELETE-budget/helper results. Repeating the whole word adds resets and cannot fix either inequality or J_B=0.

The exact source audit covers all429 seven-core shapes and3,003 query contexts embedded in the existing thirteen-key tree and its reflection. The complete pre-synchronization relation has18,450 states and109,410 edges, including324 positive transitions. This REFUTES the proposed claim that no further excess can occur inside the seven-key core. It does not compute maximum accumulated excess or identify a higher-budget recurrent amplifier.

Independent pointer verification and reflection pass for6,038 source calls and12,076 validated BST occurrences. The literal return is composed from that same independently verified complete transition table, with no new engine calls or word-class search. The source identities commute with arbitrary untouched outer-fringe substitution, so no larger finite fit is used.

The four-rule gate and strategy review are complete for the source-graph refutation and its counterexample certificate. The requested stronger amplification-and-return identity and universal Step3/CD remain OPEN. No SCC/maximum-excess search, new clock, terminal formula or automatic successor was launched.

All820 earlier/source files and all125 Stage11G files with exact inventory remain unchanged; branch/HEAD and clean tracked state are preserved. Matching-terminal remains FROZEN.

Evidence: KC00_FOUR_RULE_GATE.md; KC00A_LITERAL_RETURN_COMPLETION_SCOPE.md; KC01_COMPLETE_SOURCE_RELATION.md; KC02_EXACT_AMPLIFICATION_AND_RETURN.md; KC03_SOURCE_AUDIT_AND_REPRODUCIBILITY.md; KC04_GATE_RESULT_AND_STRATEGY_REVIEW.md; source_transition_table.json; reachable_relation_certificate.json; positive_extension_certificate.json; verified_amplification_certificate.json; literal_return_certificate.json; independent_audit.json; proof_status_ledger.json; final_integrity.json; delivery_manifest.json.
