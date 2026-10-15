# STRICT_KEEP_IDENTITY_THEOREM.md — A1 (same KEEP key + fringe fungibility)

## Exact binding (implemented)
Active KEEP e with A-target slot T and B-target id U: `(isS_A <=> isCore_B)`; if S: `sidx_A == U`;
if fringe: `gap_A == U-9` where `gap_A` from fullrank order. DELETE: no B-target (B identity enforced
separately). Enforced per active event in the repaired relation; adversarial S/gap mismatches rejected.

## Fringe fungibility theorem (the "independently justified common fringe-key identity")
Claim: for canonical (balanced-block) B, splaying any two fringe keys of the same gap yields
identical S-visible outcomes (core topology evolution, destination S-skeleton, costs affecting w).
Proof: intra-block rotations are S-invisible (permute fringe within the gap; S-nodes untouched);
once the accessed key reaches the block root, subsequent evolution depends only on (core topology,
gap slot, block nonemptiness) — never on which block key. Hence same-gap fringe keys are
abstractly interchangeable: abstract edge identical. Consequence: gap-level binding is EXACT (not
approximate) for canonical representatives; same-gap different-key witnesses are legitimate
(fungible), cross-gap/S-mismatch witnesses are phantom (rejected).

## Scope note
Fungibility is proved for canonical balanced blocks (per-edge representatives). Deformed blocks
mid-walk are re-canonicalized per edge (§11 per-edge representatives). Non-canonical direct
reasoning is not claimed.

## Gate A1: REPRODUCED + REPAIRED (binding implemented, fungibility proved, adversarial tests pass).
