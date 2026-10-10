# Anti-padding + primitivity audit (PROVED genuine)

- Exact closure both trees (labeled serials); all keys present; five KEEP keys
  genuine each (B-changing ≥1, traced).
- Core 9 at all 19 states. DELETEs freeze B (traced); A StepEvs exact; no a=0
  accesses (18 blocks = 18 accesses).
- Primitivity: 18 distinct pre-closure boundary pair-states (start=end is
  closure itself); word aperiodic (no L|18 with uniform L-blocks); hence no
  proper pair-closed subcycle — not a concatenation of banked cycles.
- DELETE tail (D8,D2,D6,D1,D9, all a≥1) is closure-necessary (without it the
  trees don't return) and funds K3's seam reserve with real StepEvs; the class
  predicate (exception+relay+payer) doesn't involve the tail. Costly-DELETE
  loops manufacture nothing: removing any occurrence breaks closure or the
  relay structure (verified: relay/payer positions are KEEP-anchored).
- D5 (idx4, a=2) genuinely splays A before K1; no same-key shadows anywhere.
- No banked DELETE-removal invariance exists (checked) — none assumed either way.
