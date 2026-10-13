# CC_CIRCUIT_SIZE_THEOREM.md + CC_OPERATOR_CLOSURE_THEOREM.md + CC_SOURCE_TO_PRODUCT_SIMULATION.md (condensed)

Size (CC-5): measured fragments (rotation slot 51 nodes shared; order/hall/
Bcore fragments; subset-sum sharing: 1,024 sums in 1,034 nodes). Template
schemata counted (89,440 slot+S combos pre-gap-assignment; skeleton UB
12.5M loose, 16,384 placements tight-ish). Per-guard AND cost with sharing/
folding: hundreds of nodes each (measured fragments). Projection: distinct
guards (≥16k placements, hole detail splits further) × ~10² nodes ≫ 4M cap
even before transitions/operators/potential — and naive skeleton×assignment
enumeration itself timed out (20 min, no output). B_product ≤ B_max NOT
established. RC-4: FAIL (measured). No threshold/grammar changes made to
force a pass.
Operator closure: Pre/Post/MinPre construction theorems proved analytically
(shared refs + binder + overhead constants c_bind/c_min); verified on 300
random + 11 deterministic small graphs (0 mismatch), incl. negatives,
zero-mid edges, empty preimages, no-outgoing states, parallel weights.
Representation closure holds by construction (finite-domain binders).
Simulation: Stage-10 U1-U10 stands (re-audited); edgewise composition
exact-boundary; high-cost lower bound; closed-walk lifting conditional on
product existence (unbuilt). No concretes-to-abstract gaps beyond the
documented open construction.
