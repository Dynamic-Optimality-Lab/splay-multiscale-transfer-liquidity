# CORE-01B Reference Identity (Gate A3/B5)

Core slot i IS S-index i (NCORE=9, mu 9-bit, crank mapping; consistent
across BState, canon_key, ssertify envs, and T-A tests). Gap slots 9-18
carry fringe/gap refs (b_valid forces kl=kr=2 there). The marked closure
uses slots only; no physical-key claim beyond the compiler's own indexing,
which the frozen validity predicates already assume. Ancestor links from
b_parent_of muxes over all 19 slots. No new coordinate introduced; the
147-field interface is the sole state representation.
