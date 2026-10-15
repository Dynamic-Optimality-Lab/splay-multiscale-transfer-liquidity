# PC_PORT_COMMUTATION_CORRECTED.md — re-audit under primitive-rotation counting (C3)

## Correction applied
One `_rebuild` iteration ≠ one primitive rotation. Zig-zig/zig-zag = 2 primitive rotations; zig = 1. Per access at depth d: exactly d primitive rotations (measured identity `prim_count(fr)==d`, 3000/3000). Per macro: Σd_i ≤ Σ2a_i = 2H ≤ 4 (measured max 4 — bound tight and attained).

## Re-audited displacement and shadow claims
- Displacement ≤ 1 per primitive rotation (rotation locality) ⇒ ≤ 4 per macro (measured max 4, `disp ≤ P` verified 3000/3000).
- Ports (initial depth ≥ 7) end at depth ≥ 7−4 = 3 > 2. The depth-2 destination shadow NEVER contains ports (exclusion re-proved under corrected budget).
- Final depth-≤2 nodes originate at initial depth ≤ 2+4 = 6 = exposed prefix (inclusion re-proved; tight).
- L5 "top-3 from ≤6" clause: SUPERSEDED. Under corrected counting, final-depth-3 nodes may originate at depth 7 (frontier). Status: depth-3+ may intersect frontier (unused by this construction); depth-2 claims above are exact. UFRL L5 displacement sentence ("≤4 total rotations (2H≤4)") already states the corrected number and survives verbatim; only the top-3 corollary is narrowed to top-2.
- AFSP "output cone D+2h": displacement ≤ 2H preserved (h = macro H); for H≤2 the cone is D+4. Depth-2 shadow (D=2) resolves inside the exposed prefix (≤6). ✓

## Commutation theorem (unchanged statement, corrected budget)
Splay_ω(Fill(P,F)) = Fill(RotatePorts_ω(P),F) for H≤2 macros. Induction steps re-verified: (1) accessed keys at depth ≤4 <7 (H≤2 ⇒ d_i≤4); (2) total primitive rotations ≤4 (corrected unit); (3) rotation operands exposed (depth ≤4, moving up only); (4) rigid subtree moves (code fact, `splay.py:98-152`); (5-8) as before. Prior 4000-trial replay stands (engine behavior unchanged; only the accounting unit is corrected).

## Gates G03 (four-rotation bound) + G04 (commutation): PASS. Evidence: PC_C3_AUDIT.json + prior PP_PORT_SMOKE.json (re-read under corrected units).
