# Recursive closure soundness (tasks H1/H3/H4 + F3 + rotation invariance)

## H1 (C0 sound; induction base)

Rot(B) leaves: banked theorems conclude Q≤2A on their domains; rotation
preserves (A,Q) exactly (same accesses, same transitions, cyclically
reindexed — verified additively in every certificate). Z leaves: A=Q=0.
Inductive step: W^{↺r} = U_1⋯U_m (m≥2), each U_i closed + certified, so
Q(W) = ΣQ(U_i) ≤ 2ΣA(U_i) = 2A(W) (accesses partitioned exactly once;
DELETE q=0; no prefix double-charge; no T0 restart — children replayed from
actual states with pointer+tuple lockstep agreement). Hence every C*
certificate proves Q(W)≤2A(W) from banked mathematics alone.

## F3 zero-cost lemma (PROVED)

Claim: a closed A-zero cycle has Q=0. Proof: a_t=0 ⟺ d_A=0 ⟺ accessed key is
the current A-root; splaying the root is a no-op, so the A-tree never changes
and every access hits the single fixed root key x. KEEPs touch only x in B:
after the first KEEP-x, x is B-root and later KEEP-x are no-ops. If x were not
B-root initially, B would end with x at root ≠ start → contradicts closure.
Hence x was B-root throughout, all KEEPs are (dB=0,q=0) no-ops, DELETEs have
q=0, so Q=0. A cycle is Z-classified only after verifying closed + A=0 +
Q=0 + single key. No silent A=0 screening classification (code returns Z-fail
otherwise, and a closed A0 walk with Q>0 is impossible by this lemma — its
appearance would be an engine bug, treated as INDETERMINATE).

## H3 reachability

Segments are extracted from valid closed parents (or rotations thereof,
which preserve legal transitions); every recursive start state lies on an
ancestor trajectory reachable from T0. No artificial tree introduced
(pointer trees rebuilt from recorded serials, transitions re-verified).

## H4 cost preservation

Partitions split access index ranges (cyclic, exhaustive, disjoint —
additivity asserted per certificate: ΣA_seg==A, ΣQ_seg==Q). Fresh replays
cross-checked against sliced whole-word legs (xcheck True everywhere:
pre-depths, costs, genuine flags, roots equal).

## Rotation invariance (G1 basis)

All 20 predicates use cyclic constructions (mod-s intervals/scans, merged
rotation to first-a≥1 leg, recognizer all-cut searches); rotating the linear
frame permutes but never changes verdicts. Spot-verified: whole-word battery
+ strict-MSINK identical under 4 rotations on 8 control words.
