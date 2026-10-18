# SR02 Rank/Marked-Count Lemmas (Gate C, exact statements)

Ranks: windowed integer log2 (sizes 1|2-3|4-7|8+ -> 0|1|2|3); per rotation
only x (up) and p (down) change rank; per-rotation |Delta| <= 3 each side
(size range), exact values witness-dependent. Marked rank R_M: same with
marked-membership mask (mu bits); transitions preserve mu value (A1). Marked
count M (shadow S-positions 0..7): can jump +-2 at w=0 (killer-B verified);
no universal bound derivable from w (H opaque in abstract state). dmax:
0..8 witnessed; rotation effect +-1 per involved node, S-pushdown +1.
Composition C2/C5 deltas verified arithmetically on all stored edges
(SR02_GUARD_CASE_CHECKER: identities hold, 0 violations on 78 stored).
Universal per-family bounds: OPEN (all).
