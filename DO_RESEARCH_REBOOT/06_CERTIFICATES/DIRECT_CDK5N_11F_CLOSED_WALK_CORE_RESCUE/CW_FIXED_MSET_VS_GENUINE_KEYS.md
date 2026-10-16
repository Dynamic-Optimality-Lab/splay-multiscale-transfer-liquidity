# CW_FIXED_MSET_VS_GENUINE_KEYS.md — fixture coordinate vs theoretical marked set

## MSET (fixed {1,3,5,7,9})
Appears in: `core_of(ps, M=MSET)` default (core computation), CRA T0-adjacent fixtures, SELR seed
assertions (`genuine == [1,3,5,7,9]`). Role: the genuine/marked set OF THE FIXTURE UNIVERSE
(keys 1..9 with odd marked). Fixture words are constructed (or selected) so their genuine five
coincide with odds; membership tests assert this shape.

## G(W) (dynamic genuine five-set)
`genuine_keys(legs)` per word. R1-T quantifies over words with |G(W)|=5 (any five keys).
The marked B-core is `C_{G(W)}` (ancestor-closed root→genuine-target paths). The nine-count
(`cores_ok True`) applies to THIS core (with M=G(W), not M=MSET, in general).

## Non-conflation proof
MSET ≠ G(W) in general (fixed vs dynamic; explicit words with genuine evens exist — fuzz
constructs them routinely). Tests using MSET-core on non-fixture words would miscompute C_M
(paths to odds instead of paths to genuine). All new theory/tests use C_{G(W)} with G from replay.

## Relabeling impossibility (recorded, not performed)
No nontrivial order-automorphism of a finite chain exists; exact MSET normalization of arbitrary
(G,U) is impossible. The theory avoids relabeling entirely (G-native statements + abstract
S-index/mask parameterization). The 126 masks need no relabeling (positions, not key values).

## Consequence for prior work
Prior fuzz using arbitrary M (5-subsets as marked) tested the parametrized machinery, not the
R1-T domain (M must equal genuine). Prior fringe-ancestor skip censuses mixed admissible and
diagnostic cases. This campaign repartitions: admissible (M=G(W), |G|=5, core-9, closed) vs
diagnostic outsiders. No historical certificate altered (this is a new classification).
