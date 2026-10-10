# 26AS audit: coupled conservation + dual-push + Hall + recognizer + hunt

## L1 coupled displacement (PROVED universally)

d_{S_y}(r)+d_{S_y}(s) ≤ d(r)+d(s)+2 for r<y<s. Rotation-case tables +
entering-step composition (`26AS_coupled_root_universal_proof.md`).
Evidence: 18136 triples exhaustive (0 violations, max exactly +2, engines
agree); 5448-step region audit (single-side V1✓, enter V2✓, max-2 V4✓);
threat probes mechanism-consistent. Two table corrections made openly during
verification (zig far-side 0; RL-T0 beside-0).

## L2/parity/E (PROVED)

L2 by induction (+4 non-straddling, +2 straddling via L1). Parity identity
proved arithmetically + fuzz-verified. Push_B = exact proper-ancestor set
(all shapes n≤7 corpus); dual-push detector + Tests B (eligible ✓),
C (between-key off-path REJECTED ✓), D (parity ✓), E (double-spend ✓);
explicit integral-flow construction fuzz-verified
(`26AS_eligibility_allocation.py`, `26AS_dual_push_trace_tests.json`).

## Hall + allocation + global (PROVED)

Cuts 1/2 from declared A-restrictions + shallow credit; union cut from
coupled bound (κ strengthens private bounds only — never a sink).
A-depth thresholds openly labeled restrictions with stated equivalence.
ASmix global theorem; recognizer (all-cuts × DP, banked validators imported)
self-tests 10/10 incl. AP/AQ/AR preservation.

## Bounded hunt (COMPLETE, NEGATIVE)

Manifest precommitted (`26AS_search_manifest.json`): 14742 heads, budget cap
40000, two vine-16 seeds, deterministic enumeration — fully exhausted, no
expansion. Result: 14645 closed, 2410 two-run, 0 qualifiers
(`26AS_bounded_search_summary.json`, empty qualifier log). Stage census
(`26AS_hunt_stage_census.json`): bottleneck is layout anatomy (no W-slot /
positive returns / wrong second key); zero candidates reach W validation.
A block-grouping edge case (leading a=0 accesses attach cyclically to last
block) was found and fixed mid-hunt; hunt re-run clean after fix.

## Outcome

Universal restricted theorems PROVED; strict novelty NOT certified → OUTCOME B.
No 26AT. General allocation + universal coverage remain OPEN.
