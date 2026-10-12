# Recursive closure soundness (Gate E — induction + Z-basis)

## Z-basis lemma (PROVED)

Claim: a closed A-zero cycle has Q=0 (hence Q≤2A as 0≤0).
Proof: a_t=0 ⟺ d_A=0 ⟺ accessed key is the current A-root; splaying the
root is a structural no-op, so the A-tree never changes and every access
hits the single fixed root key x. KEEPs touch only x in B: after the first
KEEP-x, x is B-root and later KEEP-x are no-ops. If x were not B-root
initially, B would end with x at root ≠ start, contradicting closure.
Hence x was B-root throughout, all KEEPs are (dB=0,q=0) no-ops, DELETEs
have q=0, so Q=0. ∎ Classification requires closed + A=0 + Q=0 + single
key, all verified; A0-with-Q>0 (impossible if closed) routes to
INDETERMINATE, never to uncovered.

## H1 induction (C0 + step)

C0 leaves: banked theorems conclude Q≤2A on their domains (rotation
preserves (A,Q) exactly — same accesses/transitions, cyclically reindexed,
additivity asserted per certificate); Z leaves satisfy 0≤0 by the lemma.
Step: W^{↺r} = U_1⋯U_m (m≥2), each U_i closed + certified, so
Q(W) = ΣQ(U_i) ≤ 2ΣA(U_i) = 2A(W) (accesses partitioned exactly once;
DELETE q=0; no prefix double-charge; children replayed from actual states
with pointer+tuple lockstep agreement). Hence every C* certificate proves
Q(W)≤2A(W) from banked mathematics alone. ∎

## Reachability + cost preservation

Segments descend from valid closed parents (or their rotations, which
preserve legal transitions); every recursive start lies on an ancestor
trajectory reachable from T0. No artificial tree (pointer trees rebuilt
from recorded serials, transitions re-verified). Partitions split access
ranges disjointly/exhaustively (additivity asserted); fresh replays
cross-checked against sliced legs.
