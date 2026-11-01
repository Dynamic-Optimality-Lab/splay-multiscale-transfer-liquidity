# The requested two-reset coupling is impossible on this KEEP cycle

There is a source-exact obstruction for the fixed word

    W=(13,11,9, 1,2,3,4,5,6,7,8,9,10,11,12, 11,10,9,8,7,6,5,4,3,2,1).

For any one-period A/B coupling with two pure one-StepEv resets,

    E<=1<4=C_D.

Immediately after KEEP12, A has root12 and right child13. Each of the eleven descending KEEPs preserves every larger key already on A's right spine and adds its own root. Two one-StepEv resets can remove at most four counted spine vertices. Thus key13 still has depth at least eight before the next hot K13 leader, forcing a_13>=4. Its B demand is q=6, so it creates no positive excess. Only hot K11 can still be positive, with excess at most one. The necessary E=5 and a_13=a_11=1 cannot occur.

The proof covers every reset position, target key and valid A state. It also handles DELETE leaders followed by starved KEEPs without discarding the leader cost. This is a structural impossibility theorem, not a failed placement search.

A stronger cell argument proves E<=C_D for every closed coupling whose KEEP projection is W^p, with arbitrary A-only insertions, costs and reset distribution. The established DELETE-only minimum-cut theorem therefore gives an old-UD accepted cut throughout this family. Increasing the A period or adding more resets cannot rescue this word as a strict FI-only witness.

The six exact source-frame formulas prove the spine law with arbitrary fringes. Independent pointer verification passed in both orientations: 172 source calls, 344 validated BST occurrences, every event interval and zig direction. A legal diagonal closed control has exactly two pure one-StepEv resets, E=0 and C_D=4, confirming nonvacuity. No larger finite fit, reset search, new B word or FI/UD cut trial was performed.

The earlier G_B=J_B=5 B-cycle result remains valid. Its low A costs are not jointly compatible with this reset budget. This removes the fixed coupling architecture; it does not prove universal CD or establish new strict FI-only coverage. Universal Step 3/CD remains OPEN.

The four-rule gate and strategy review are complete. All 739 earlier/source files and all 125 Stage 11G files with inventory are unchanged; branch/HEAD and clean tracked state are preserved. Matching-terminal remains FROZEN. No successor campaign was launched.

Evidence: AC00_FOUR_RULE_GATE.md; AC01_SOURCE_RIGHT_SPINE_LAW.md; AC02_ALL_COUPLINGS_OBSTRUCTION.md; AC03_SOURCE_AUDIT.md; AC04_GATE_RESULT_AND_STRATEGY_REVIEW.md; spine_symbolic_certificate.json; fixed_word_and_reset_control.json; reflected_source_certificate.json; independent_audit.json; proof_status_ledger.json; final_integrity.json; delivery_manifest.json.
