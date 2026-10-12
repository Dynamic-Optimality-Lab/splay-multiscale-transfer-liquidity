# CC_FINITE_CAUSAL_CONE.md — bounded-cost finite causal-cone lemma (STEP 06)

## Lemma (fixed h ≥ 0; campaign uses h = 2, 4)

Let an original A interval have total A-cost H ≤ h (KEEP/DELETE mix,
terminal operation included).

**(a) Rotation budget.** Access i at A-depth d_i performs exactly d_i
primitive rotations (STEP-01 D: 15,521/15,521 verified; splay
decomposition). d_i ≤ 2a_i (a=ceil(d/2)). Total rotations ≤ Σd_i ≤ 2H ≤ 2h.

**(b) Depth-displacement.** One primitive rotation changes every node's
depth by at most 1 (rotation at (p,c): c −1, p +1, middle subtree 0,
others 0; verified 3,456/3,456 rotations on all shapes n≤7).

**(c) Accessed-node bound.** Effective target x at step i: current depth
d_i ≤ 2a_i; prior rotations ≤ 2Σ_{k<i}a_k each displacing ≤1 ⇒
initial_depth(x) ≤ d_i + 2Σ_{k<i}a_k ≤ 2Σ_{k≤i}a_k ≤ 2H ≤ 2h. Verified
747/747 random targets. Same bound for rotation pivots (ancestors of x:
current depth < d_i; same backward walk).

**(d) Output cone.** A node at final depth ≤ D was initially at depth ≤
D+2h (backward displacement over ≤2h rotations). For D=2: initial depth ≤
R(h)=2+2h. Hence the initial rooted prefix through depth R(h) determines
the final top-three-level structure: nodes below R(h) provably cannot
enter final top 3 and ride as rigid ordered blocks (opaque holes).

**(e) Zero-op normalization.** A-cost-zero access ⟺ current root ⟹ empty
splay frames ⟹ structural identity (625/625 verified). Such DELETEs change
neither tree and are erased from effective words.

**(f) Nontrivial bound.** Nontrivial ⟺ a≥1; Σa ≤ h ⇒ at most h nontrivial
A accesses per cost-≤h interval (300/300).

## Corollary (finite macro grammar)

Cost-≤h intervals have effective words over targets initially within
depth 2h, with ≤h nontrivial accesses, simulable on the R(h)-prefix with
opaque holes — a FINITE grammar per fixed h and fixed boundary shadow.
Universal over ambient size (no cutoff; holes carry the unbounded fringe).
∎
