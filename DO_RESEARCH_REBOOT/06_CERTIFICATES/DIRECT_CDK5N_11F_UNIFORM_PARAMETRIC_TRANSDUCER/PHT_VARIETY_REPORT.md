# PHT variety census report (11F-UNIFORM probe results)

## Method
- `PHT_shadowcensus.py`: canonicalize post-KEEP A-boundaries (corpus 150 words + 300 random fringe trials) via `AFSP_canonical.canonical_shadow` with rank-canonical S relabel + inorder fringe anonymization.
- `PHT_shadowcensus2.py`: joint (A-shadow, B-shadow) census over 20000-state random sample of the 1.31M-state UFRL multimask graph (all 126 masks) + 500 explicit-S9 fringe trials (S9 = M5 + 4, words over S9+fringe).
- Lift test: 20 closed 9-key corpus words replayed verbatim in 12-key trees (same word, larger initial tree).
- Fringe search: 2000 random words (len 6-14, 85% over S9 / 15% fringe) in 12-key trees, checking `S1==S0 and agree`.

## Results
| Probe | Result |
|---|---|
| A-shadow only (corpus) | 2416 boundaries -> **51** distinct (mask, shadow) |
| Joint (A,B) shadows (20k multimask sample) | 20000 -> **11222** distinct (56% distinct rate) |
| Explicit-S9 fringe trials added | **0** usable (filter `Mchg<=S9x`, len 5 never passed in 500 trials) |
| 9-key word lifted to 12-key tree | **0/20** stayed closed |
| Random fringe closed-universe search | **0/2000** closed |

## Interpretation
1. A-side alone abstracts beautifully (51 classes), but costs live B-side; joint variety retains ~56% distinctness — symbolic BFS over joint shadows would reproduce concrete-graph scale (~700k+ for 9-key alone), no savings.
2. Fringe context destroys 9-key closure (0/20 lift); fringe closed universes are rare (0/2000 random) and must be found by dedicated search per (n, S9) — unmeasured variety on top.
3. Symbolic fringe representation (holes with S-subsets + opaque presence) is unvalidated: no evidence reachable fringe variety is small, and no macro enumeration exists over it.
4. Conclusion: uniform parametric closure does not fit budget. Recorded as direct blocker data for verdict E.
