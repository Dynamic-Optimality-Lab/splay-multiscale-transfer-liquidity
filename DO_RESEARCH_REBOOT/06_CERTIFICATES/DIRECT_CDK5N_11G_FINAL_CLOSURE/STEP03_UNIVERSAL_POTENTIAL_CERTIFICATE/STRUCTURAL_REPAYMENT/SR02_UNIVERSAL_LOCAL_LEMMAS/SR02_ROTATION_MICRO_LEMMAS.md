# SR02 Rotation Micro-Lemmas (exact, code-derived, scoped)

Single rotation R(x,p,gp) (x child of p; both A `single_rot` and B
`b_single_rot` verified structurally identical modulo mux/widths/empty-kind):
(R1) Depth: x −1, p +1, S-subtree (p's other child) +1 per node, middle
subtree 0, rest 0. Net ΔD = +|S| ≥ 0 per rotation (S = sibling subtree).
(R2) Size: only x (grows) and p (shrinks) change subtree size; every other
node's subtree is rigidly moved (size preserved) → only x,p ranks change.
(R3) Root case (p_was_root): x→depth 0; same ± pattern otherwise.
(R4) Composition: zig = 1 rotation; zigzig/zigzag = 2 rotations (primA+primB
wirings verified in splay_event/b_splay_event).
SCOPE CORRECTION vs SR-01: ΔD=+|S| holds PER ROTATION, not per macro —
full splays include pushes/restructuring (B `push` lists; E4 macro drops
D by 12). Macro-level depth/rank claims require push accounting (OPEN,
needed for L4). Rank discontinuity: windowed integer ranks 0..3 (sizes
1,2-3,4-7,8+); per-rotation rank deltas bounded by ±3 (size range), exact
values need concrete sizes (witness) — no universal closed form claimed.
