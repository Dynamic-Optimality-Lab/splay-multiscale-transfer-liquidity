# Beyond single resets: the two-reset B-budget gate fails

No strict FI-only closed walk was established. The proposed two-reset construction is ruled out by an A-independent source-budget obstruction before any policy search.

For every closed source walk,

    E<=G_B=sum_KEEP max(q_B-2,0).

Each positive A-root block pays at least two own units and has at most one B-changing KEEP, which proves the inequality without fitted parameters. Two effective pure resets per B period supply at least four actual units. A strict FI-only example therefore needs G_B>C_D, at least five B-surplus units for two cheapest resets.

The old recurrent KEEP order has G_B=4; it cannot support multi-reset strictness at that funding density. The new fixed thirteen-key bit-reversal order has G_B=3, with three unit-positive opportunities. Hence every admissible two-reset cycle over p rounds has E<=3p<4p<=C_D and is already UD-covered. This holds regardless of A shape or reset choices. The 78 conditional A policies were not run, as required by the predeclared gate.

Independent pointer replay confirms both B recurrences and their reflections: 104 source accesses and 208 raw BST occurrences. The proof extends to arbitrary unrequested fringes structurally. No larger finite fit, new FI/UD rule, virtual credit pool, reused unit or new paired-cycle certificate was used.

The four-rule gate's strictness target was not met; TR03 records the strategy review and stop. All 683 pinned earlier files and all 125 Stage 11G files, including their inventory, remain unchanged. Branch/HEAD and clean tracked status are preserved. Matching-terminal work stays FROZEN. Strict FI-only coverage and universal Step 3/CD remain OPEN.

Evidence: TR00_FOUR_RULE_GATE.md; TR00A_OUTPUT_PATH_CORRECTION.md; TR01_BUDGET_OBSTRUCTION.md; TR02_EXACT_B_PROFILE_AND_FRINGE_LIFT.md; TR03_GATE_RESULT_AND_STRATEGY_REVIEW.md; B_budget_certificate.json; old_B_budget_replay.json; independent_audit.json; final_integrity.json; delivery_manifest.json. No new Lean verification claim is made.
