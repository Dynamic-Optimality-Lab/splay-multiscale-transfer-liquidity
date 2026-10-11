# Recursive C23* definition, soundness, completeness

C_0^23 = Rot(B_23) ∪ Z: whole-cycle rotations banked-covered on actual
reachable states, plus certified closed zero-cost cycles (A=Q=0, single key,
no-op chain — lemma proved: A-root fixed ⇒ one key; closure forces B-root
no-ops ⇒ Q=0).
C_{k+1} = C_k ∪ CycAdd(C_k): closed W with a valid rotation along its actual
trajectory partitioned into ≥2 nonempty consecutive closed pieces, each in
C_k with its own start state/domain/rotation, exhausting accesses exactly
once with exact A/Q additivity. C_23^* = ∪_k. Least fixed point; no ZULR in
basis; no new mechanisms.

## Soundness (induction on proof depth)

C0 leaves satisfy Q≤2A (banked theorems; rotation preserves (A,Q); Z gives
0≤0). Step: W^{↺r} = U_1⋯U_m (m≥2), each closed + certified ⇒ Q(W) = ΣQ(U_i)
≤ 2ΣA(U_i) = 2A(W) (accesses partitioned once; DELETE q=0; children replayed
from actual states with lockstep agreement). Every C* certificate proves
Q≤2A from banked mathematics alone.

## Completeness (relative to bank-23)

Induction on length: W ∈ C* is in C0 (decided by complete battery + Z) or
splits at some rotation into shorter C* members. The engine enumerates ALL
rotations and ALL proper closed segments (pair-equality classes complete);
children decided by IH (memoized); canonical DP (minimax depth → origin →
pieces → lexicographic cuts) finds a tiling iff one exists among covered
edges. Abstract oracle 19/19 (incl. depth-two nested, non-flattening,
rotation-equivalence). No depth cutoff; termination by strict length
decrease (depth ≤ n); memo keys (start serials, canon word) never merge
different starts.

## H5 canonical choice

Minimum depth → canonical origin → fewest pieces → lexicographic cuts →
mechanism order. Deterministic (census byte-identical on rerun).
