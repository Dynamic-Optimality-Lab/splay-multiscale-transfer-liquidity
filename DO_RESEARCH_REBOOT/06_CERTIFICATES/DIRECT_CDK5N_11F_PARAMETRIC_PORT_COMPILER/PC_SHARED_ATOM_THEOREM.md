# PC_SHARED_ATOM_THEOREM.md — G05 (structural ports + shared inventory, sound and complete)

## Representation (PC_STRUCTURAL_WITNESS.py + PC_ATOM_INVENTORY.py)
Prefix slots 0..126 (present/parent/side/depth/label/rank/interval/children), ports identified by
immutable cut-labels `(slot,side)` (pinned refs, unique by construction, ride rotations as opaque pairs).
Allocation cells `z[i][s][b]` (gap x port fringe counts) + hidden-S bools + hidden-S ranks (existential,
interval-checked) + per-gap signature `sig` (shared with abstract states).

## One atomic population vector
Conservation per gap: `sum_{s,b} z[i][s][b] = sig_i - p_i` (exact equality; `p_i` exposed fringe computed
in-circuit). S-cover exact-once (exposed XOR one hidden claim). Inactive ports carry nothing.
`sig_i <= 266`; totals `<= 2660` in 12-bit exact arithmetic (widths sufficient by bound).

## Order fidelity (the strictness requirement)
Port interiors contain no exposed slots (BST argument: an exposed slot inorder-inside a port range would
be a depth>=7 descendant, contradiction). Hence within a (gap,port) cell, order is: hidden-S keys at
exact V-positions + mutually order-free anonymous fillers. Reconstruction sorts these — faithful.
Visible same-gap keys split gaps (fullrank S-ranks order all S keys exposed-or-hidden; exposed fringe
ranks partition atoms implicitly). No coarse ten-gap collapse: hidden-S exact positions + strict
interval endpoints enforced per key.

## Soundness/completeness (witness-carries-values/circuit-verifies)
Sound: satisfying assignment -> ordered BST completion (reconstruct per port: hidden-S ints at exact
V-positions + anonymous markers; position-order verified) + B fringe inventory (gap blocks per `sig`).
Tested 600/600 both directions in predecessor + 138 grounded production transitions here (V8).
Complete: every valid canonical completion induces a satisfying assignment (read off cut/hidden-S/
allocation; conservation is an identity). Destination sharing: labels ride rigidly; same `z`/hidden-S
valid at destination (800/800 predecessor both-views; production destination equality checked per edge).

## Gates G05 (atoms sound+complete): PASS (construction + V8/V9 evidence).
