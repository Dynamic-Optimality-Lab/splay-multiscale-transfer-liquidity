# Recursive closure completeness (Gate E — relative to bank-23)

Induction on cycle length. If W ∈ C_23*: either W ∈ C0 (base tests decide:
battery + Z, both complete predicates on the given frame; rotation
invariance holds by cyclic construction + spot verification), or W ∈
CycAdd(C_k): some rotation + proper partition into shorter C_k cycles. The
engine enumerates ALL rotations and ALL proper closed segments (pair
equality classes are complete: every closed subwalk's endpoints repeat);
each child is classified by the induction hypothesis (strictly shorter ⇒
decided correctly, memoized); the canonical DP (minimax depth → origin →
pieces → lexicographic cuts) finds a tiling iff one exists among covered
edges. Hence every certifiable decomposition is found. Completeness is
relative to the declared 23-mechanism + Z basis only (abstract oracle:
19/19 incl. depth-two nested, non-flattening, rotation-equivalence cases).

## Termination (strict length decrease)

Every recursive call is on a proper closed part (≥2 nonempty pieces ⇒ each
child strictly shorter than its parent). Call-chain lengths strictly
decrease ⇒ well-founded induction; depth ≤ n always. No depth cutoff is
imposed or needed; no full-length child can recurse into itself (whole-cycle
edges excluded from every DP). Memoization by (start serials, canon word);
no rotation-normalized merging.

## H5 canonical choice

Minimum recursive depth → canonical cyclic origin → fewest pieces →
lexicographic cuts → mechanism order. Deterministic across runs.
