# STRICT_A_SHADOW_EQUIVALENCE.md — A6 (authoritative depth-two shadow implemented)

## Audit finding
Authoritative `canonical_shadow` (AFSP_canonical.py): levels 0,1,2 (7 positions) + S-rank/fringe-beta
descriptors + holes. Predecessor alpha: levels 0,1 only. Discrepancy REPRODUCED (fidelity gap, not
a soundness counterexample: coarser partition is simulation-consistent but lineage-incompatible).

## Implementation (exact)
Alpha-7: positions root,L,R,LL,LR,RL,RR × (kind, isS, S-index); port/empty coarse-prefix children
propagate opaquely; canonical beta DERIVED (fringe inorder ordinal, no search vars; implied by
pattern, available for lineage). Holes remain witness-level (hidden-S + allocation + intervals).
R3 justification: same coordinate completed to authoritative content (A6 explicit mandate); no new
coordinate; T/depths/bounds unchanged.

## Equivalence note
Beta is a function of (positions, S/fringe pattern) both sides; pattern match implies beta match.
State identity = 7-position pattern (canonical, deterministic). Cross-campaign shadow compatibility
restored (7-position vis + holes/inventory split as authoritative).

## Gate A6: REPRODUCED + REPAIRED (regression: alpha-7 matching on all grounded edges).
