# Post-MSINK 384-word census (independent reconstruction)

Engine: bank-21 direct battery (20 + MSINK-exists at every test) + recursive
C21* DP (nested rotations, memo-exact, budgets untouched). Strict DLSS also
recorded per word (exists-sinks).

## Result: 375 DIRECT-BANKED + 7 CYCLIC-ADDITIVE-BANKED + 2 RESIDUAL = 384.

Covered: 382. Uncovered: 2. Matches the §0 expectation exactly
(reconstructed, not assumed). Disjoint categories, sums verified.
- 160 words carry MSINK among direct mechanisms (29 strict-MSINK residuals
  now directly covered + multi-memberships).
- 125 strict-DLSS members corpus-wide (123 covered, 2 residual).
- 7 cyclic (all depth 1; S1/VR/AMG/S2 part mechanisms).
- 2 residuals: b8b02be7 (IN; strict-DLSS member) + 6b242e23 (spare;
  strict-DLSS member). Both t=(2,2) dual-long pair-state-primitive words.
- 0 INDETERMINATE, 0 SOURCE-INVALID, 0 budget hits.
- Strict-vs-old MSINK discrepancies: 0 (CRA finding stands).

Record: `DLSS_post_msink_census.json` (per-word status + MSINK flags).
