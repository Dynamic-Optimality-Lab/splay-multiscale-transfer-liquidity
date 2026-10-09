# PIVOT-21: GLOBAL PATH-HIT LOCK (direct, no Hall) — attempt + verdict

## A. Rotation-local Δdepth (exact)

Single rotation (u up): risers −1: {u}, kept-child subtree S (all),
transferred T (all). Fallers +1: {p}, kept-child subtree S_p (all).
Else 0. Full splay depth-d: exactly d rotations (zig 1 + doubles 2
each). Net Δd(x) = telescoping (d1−d0); per-rotation signs ±1/0 by
position (u/S/T up; p/S_p down). `r=d` EXACT ⇒ rotation-counting =
depth-counting (no new leverage — banked).

## B. Sustained regime

Maximal other-key interval (no x-access; shapes co-evolve; x never
rooted). x drifts (both trees) via others' rotations (riding/
transferred/path). Depths bounded (n−1); rootings reset (fresh starts).

## C. Sign-lock: EMPIRICAL (0/15000+, p<1e-9), NOT proved

Sustained nonzero motions all same-sign-or-still (`++,−−`;
never opposite/one-sided; n=6,7,8 + priors). Fresh roots unlock
mixing transiently (6% opposite, 23% split in independent samples).
Perturbation-seeking finds zero opposite steps (stable by absence).
Mechanism suspected (hot/cold co-evolution, mean-reversion) — unproved.

## D. Quantitative strengthening: OPEN

Same-sign nets have independent magnitudes (rotation-counts per
tree); ratio unbounded in principle (hub/positional corners coherent).
No universal `|ΔdB|≤c|ΔdA|` proved (cancellation/gross-net wall).

## E. Path-pair inventory

q-unit = one B-edge-pair consumed (triple). Outstanding pairs:
created by B-rotations (O(1)/rotation), consumed by doubles.
Closed inventory returns ⇒ created = consumed = Q exactly. But
creation capacity (rotations) vs A-work needs depth bounds (wall).
Inventory exact, non-constraining.

## F–G. Cyclic genesis / eternal edge

Periodic extension assigns every consumed edge a previous-lap builder
(U1-form); T0 is cut artifact. Eternal (never-rotated) edges: cannot be
repeatedly consumed (consumption destroys); if never consumed, no
demand. Genesis eliminated structurally — wall only relocates to
fan-in/sharing (unchanged).

## H–I. Block/global inequality; boundary cancellation

Per-regime `Q≤2A+ΔPhi` with physical inventory Phi telescopes on
closed cycles — but regime inequality itself needs depth control
(same wall). Closure cancels boundaries correctly; nothing to cancel
against without the regime bound. K>2 fallback noted (any finite K
suffices for DO) — no finite K proved either (same wall, any constant).

## J–K. Direct bound / COARSE-DOUBLE: OPEN

`Q=(D_B−Z_B)/2`, `2A=D_A+O_A` exact (no floors) ⇒ need
`D_B≤2D_A+slack` (slack `Z_B+2O_A≥0`). Suffices `D_B≤2D_A`. Starved
(LHS-only) vs DELETE (RHS-only) vs fat — same discrepancy wall
(cancellation/marginals/tails, 31 formulations). Unrefuted 900+.

## L. DO chain (conditional, unchanged)

C.ZIG AUTHOR (V1–V3 mechanical OPEN); B≤3A conditional; PIVOT-2
excision mechanical; translation parametric; LT/DO conditional.
Lean: U1 + descent kernels green; path-hit/block gap stands.
