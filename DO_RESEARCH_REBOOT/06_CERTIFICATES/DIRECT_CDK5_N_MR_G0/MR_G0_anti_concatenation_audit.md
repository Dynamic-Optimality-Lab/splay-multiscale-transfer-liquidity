# Anti-concatenation audit (PROVED primitive, not VR+VR)

- 33 distinct pre-closure boundary pair-states (start=end is closure itself);
  word aperiodic (no L|33 uniform L-blocks) ⇒ no proper pair-closed subcycle.
- B-only closure at access 13/26 does NOT imply pair closure (A differs there —
  verified True/True differ-from-start).
- KEEP order second half (K3,K7,K1,K9,K5,...) resembles VR's, but pair STATES
  differ throughout (different A/B trees: replay serials compared) — same key
  subsequence ≠ same walk; no banked VR cycle is embedded as a pair-closed
  component.
- DELETE tail (D8,D4,D2,D5,D6,D1,D9, all a≥1) is closure-necessary with genuine
  StepEv costs; relay/payer positions are KEEP-anchored, not padding artifacts.
- No banked DELETE-removal invariance exists (checked) — none assumed either way.
