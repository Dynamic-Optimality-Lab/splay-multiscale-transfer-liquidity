# Recursive closure completeness (tasks H2/G4/G5 + canonical H5)

## H2 (completeness relative to the banked library)

Induction on cycle length. If W ∈ C_*: either W ∈ C0 (base tests decide it:
battery + Z, both complete predicates), or W ∈ CycAdd(C_k): some rotation +
proper partition into shorter C_k cycles. The algorithm enumerates ALL
rotations and ALL proper closed segments (pair-state equality classes are
complete: every closed subwalk's endpoints repeat); each child is classified
by the induction hypothesis (shorter ⇒ already decided correctly, memoized);
the partition DP (two-phase canonical: Dijkstra min-(maxdepth,nparts) +
lex-smallest tight path) finds a tiling iff one exists among covered edges.
Hence every certifiable decomposition is found. Completeness is relative to
the declared 20-mechanism + Z basis only (abstract oracle: 19/19 incl.
depth-two nested, non-flattening, rotation-equivalence cases).

## G4 termination (strict length decrease)

Every recursive call is on a proper closed part (≥2 nonempty pieces ⇒ each
child strictly shorter than its parent). Call-chain lengths strictly
decrease ⇒ well-founded induction; depth ≤ n always. No depth cutoff is
imposed or needed; no full-length child can recurse into itself (whole-cycle
edges excluded from every DP). Memoization by (start serials, canon word):
same-string-different-start never merged (G5); rotation-normalized merging
never performed.

## G5 memoization

Key = (exact starting labeled pair state, exact access word). Verified
trajectory identity is inherent (states recomputed by fresh replay).
No hash-only equality (canonical content compared; SHA recorded alongside).

## H5 canonical choice

Minimum recursive depth → canonical cyclic origin → fewest pieces →
lexicographic cuts → mechanism order. Deterministic across runs (census
reproduced byte-identical classifications on rerun).
