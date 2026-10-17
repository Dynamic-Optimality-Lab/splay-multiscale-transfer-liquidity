# S04_MASK_SIGNATURE_UNIVERSALITY.md — Gate C (F04-10)

126 five-of-nine masks enumerated here (combinatorial, 126/126); mu bitmask
roundtrips exactly (popcount(mu)==5 enforced in state_valid7). The symbolic
machinery is mask-parametric: mubit/mask checks index S-positions, with NO
mask-specific branches anywhere (construction uniform in mu). Signatures are
gap-population counts, parametric over all 266^10 saturated values (relations
constrain sig[i]<=266 only). Tested: empty/single/near-saturated/saturated gaps,
multi-gap, ports, varied masks/M-sets, varied B-topologies, E3/E4 (corpus +
adversarial gap units). Parametricity is structural (no case splits on masks or
signatures in compilers or relations), so tests corroborate rather than exhaust.
