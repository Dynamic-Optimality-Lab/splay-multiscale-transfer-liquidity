# Phase 7: strict novelty + boundary + regression audit

## New coverage (Rule 4 discharged at Gate 0, reconfirmed)

Five-key witness `ins1-1-K2` (A=19,Q=9,W=−29, exact closure, engines agree,
keys {1,2,3,5,7} all genuine, max core 7≤8): inside CDK5-LOW; outside RT2-A /
CDK4-A (5 keys); outside AJ (succ 2≠1), AK/AL-G (2nd succ 2≠1; K2 genuine but
wrong key), AM-G (3rd succ 4≠1), AN/AO/AP/AQ/AR/AS (single positive; all five
executable recognizers REJECT); outside baselines (n=7, dB=6, A=19). Strictly
new: no prior domain covers it (complete union exclusion).

## Boundary 8 vs 9

Inside: witness max core 7 (margin 1). Outside: nine-node word (core 9 every
state, Q−2C_K=+2) — B-only certification correctly fails there; the class
theorem does not claim it. The eight-core layer itself (max exactly 8) is
covered by the same certificate (all ≤8 edges verified); no witness attains
exactly 8, which is fine (coverage ≠ tightness obligation).

## Regressions

- Nine-node word: depths/totals/closure/engines revalidated; Q−2C_K=+2 stands.
- CDK4 finite verifier untouched; AJ–AS recognizers unmodified (hashes match
  banked: 26AO 4f4b40e0…, 26AP 9abefb16…, 26AQ 9dc40634… — versions used above).
- No earlier theorem weakened or generalized; ledger addenda append-only.
- A/B costs and seam conventions: C_K (KEEP-only) vs C_X (full word) kept
  distinct throughout; no double-counted StepEvs.

## Independence

The theorem survives discarding all AJ–AS machinery (uses only K4-L1, pruning,
graph certificate, A-charging). The finite certificate plus valid reduction
proves the class; the witness proves novelty. Distinct claims, both banked.
