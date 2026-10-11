# OUT provenance audit (Gate F — read-only; no search launched)

Declared: seed frozen IN (a7c6504c), L1, candidate idx8, op rm19 (remove
DELETE at zero-based position 19), SHA 593b3f3ac5…44945b9.
Reconstruction (committed UESINK_search.mutants grammar, fixed order
removal→replacement→insertion, index asc, key asc): IN-L1 enumeration has
459 raw candidates (17 removals + 136 replacements + 306 insertions) →
442 distinct after insertion-collision dedup beside existing identical
DELETEs. Index 4 in the committed parents file is rm7;
index 8 is rm19 — wait, indices count DISTINCT parents in order: rm0(0),
rm1(1), rm2(2), rm5(3), rm7(4), rm13(5), rm14(6), rm17(7), rm19(8). ✓
rm19 removes IN[19]=D9; result canon matches frozen OUT exactly; full SHA
matches 593b3f3ac5…44945b9 (recomputed in adversarial attack 61/62).
Earlier dispositions re-verified: idx0 rm0 non-closed; idx1 rm1 non-closed;
idx2 rm2 UESINK-member; idx3 rm5 UESINK-member; idx4 rm7 MSINK-banked;
idx5 rm13, idx6 rm14, idx7 rm17 non-closed. First qualifying residual OUT
is idx8. No earlier candidate skipped (all decided; 0 indeterminate).
Distance-zero seeds classified before any mutant (record). No L2, no other
seed, no substitution, no theorem change. Concurrent-screening note: only
in-L1 state exists (usearch_in/); no other seed ran in this campaign.
