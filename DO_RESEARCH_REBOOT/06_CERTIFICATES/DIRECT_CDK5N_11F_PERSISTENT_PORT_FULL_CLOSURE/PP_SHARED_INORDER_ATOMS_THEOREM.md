# PP_SHARED_INORDER_ATOMS_THEOREM.md — PROVED (construction + 600+800 trials)

## Statement
One source structural witness ξ = (P, hidden, c, F) defines one globally consistent anonymous-key population across source A-prefix, source A-frontier ports, nine-node B-core, ten B-fringe gaps, and every destination A-port attachment. One inventory, one port assignment, one rotation replay.

## Construction
V = S ∪ exposed-A-prefix keys (|V| ≤ 9+127 = 136). Common total order → ≤137 open inorder atoms; atom j = (lo,hi) with S-gap i(j) ∈ 0..9, owning port r(j) (unique: port ranges disjoint; port-less atoms forced empty — any key there would be a non-V key at depth ≤6, i.e. exposed, i.e. in V: contradiction), forced-empty flags. Conserved inventory per gap: Σ_{j:i(j)=i} c_j = σ̂_i − p_i (p_i = exposed fringe in gap i; σ̂ = bounded representative signature). Port occupancy: EMPTY ⇒ zero atoms + zero hidden-S; S-less NONEMPTY ⇒ ≥1 fringe (exact lower bound); hidden-S placement consistent with strict intervals, no duplicate core keys (S uniqueness), anonymous keys never cross atoms except via the single rotation replay (inorder invariance of rotations).

## JointInventoryValid(P,≺,c,σ) — exact predicate (PP_JOINT_INVENTORY.py:joint_valid)
Checks (a) atom order/well-formedness, (b) per-gap conservation (equality), (c) occupancy both directions, (d) S-cover/uniqueness/interval placement, (e) forced-empty atoms zero. Feasibility of the integer system decided by shared integer-flow (AFSP_allocate lower-bound circulation, reused): gap-supply d_i with exact demands, port lower bounds, interval compat — sound+complete vs brute force 80/80 by reference (AFSP_AF2_SELFTEST + WQ ordered-hole 67/67 reconstruction).

## Scope honesty (the §8 tripwire, restated)
The old ten-gap Hall inequalities alone are NOT asserted sufficient: visible same-gap keys split gaps into atoms with stricter containment (an atom's fringe cannot serve a neighboring atom's port). The predicate enforces atom granularity, which implies hole-level feasibility but not conversely. No silent tripwire: 600 randomized instances pass both predicate directions + flow agreement + reconstruction.

## Evidence
- Completeness: 600/600 real trees induce satisfying assignments.
- Flow: 600/600 feasible instances solved with exact equation agreement.
- Soundness: 600/600 flow-redistributed assignments reconstruct valid ordered BST completions (position-order verified) with exact gap counts.
- Destination sharing (PP_DESTINATION_SHARED.py): 800/800 carried-view validity with byte-identical ξ (V stable across replay); 800/800 fresh-cut validity; S-union + σ̂ conserved.

## Gates PP-05 (shared-inventory proved) + PP-08 (same-gap ordering preserved): PASS.
