# Independent implementation audit and its limits

All verification was operated by the same agent. Here 'independent' describes separately written physical/state and classification implementations, not an independent human, a second agent, or a formal proof assistant. Universal validity comes from the mathematical arguments in the proof files. Tests are adversarial falsification controls.

## Implementation separation

`model0.py` replays every complete original operation, including every reaching-prefix operation separately from measured work. Mutable full-pointer physical splay is checked at every access against the pre-existing independent immutable tuple/path machinery. A new immutable postorder traversal independently derives all S labels, complete physical intervals and SET multiplicities at actor boundaries. The fresh event observer maintains Counter multiplicities through every primitive edge update, so duplicate private S labels are not accidentally treated as separate SET members. Original bit IDs, real pivot/promoted/middle/external edges, signs and selected outputs are preserved.

Pre-double S frames are bound to the immutable original pre-B old-grandparent subtree; completed output labels and complete output intervals are independently bound to immutable post-B states. Lower and higher splay steps are checked against these identities. Complete states use a collision-free full labelled-tree integer codec, stored in hexadecimal pools with references; they are not represented merely by hashes. PHYS files contain full source-scoped primitives, doubles and boundaries. Their source words and full initial states are preserved in SOURCE_CATALOG.

`independent0.py` implements a new forward streaming, two-lap cyclic classifier. It records last A demotion, last B promotion and previous global same-column use, classifying every vertex at the **pre-B** boundary before processing the current B phase. This is compared vertex-by-vertex, including root donor IDs, with C05's retrospective interval-search construction in `forest5.py`. A separate queue peel from roots removes all vertices as a cycle check; it does not reuse the strict-frame topological ordering. Immediate child counts are checked per role and in total. Original donor uniqueness, actual StepEv counts, <=2A and full physical/S inclusions are checked explicitly.

Computational cuts0,1,mid,last (deduplicated on short words) retain the same original IDs, S and forest assignments. These sample cuts test the universal cyclic argument; they do not enumerate every possible cut of every word.

## Results

Twenty complete controls:31,818 measured operations,120,691 actual primitive bits across both actors,19,323 B doubles,46,673 original A StepEv and68,602 real A bits. There are18,585 roots,688 C vertices and50 P vertices. Every vertex and donor agrees between the two classifiers; all tested frame, physical inclusion, role-count, closure, prefix and cut checks pass. The largest replay has1,027 physical keys. These totals are audit inventory, not a universal coverage percentage.

Ten source records carry an archived `trace_hash`; the newly computed complete primitive stream matches each exactly. Five small C05 sources additionally match the pinned independent C05 primitive streams through the residual audit. The516-key C05 source has no such full-Pi/event-hash claim: its fresh physical replay and forest checks pass. Hash availability is recorded per source rather than inferred from a false/true aggregate. Four fresh controls have no older trace to compare.

## Residual verification scope

M0 does not independently re-enumerate all Pi windows on all twenty sources. It preserves the original complete classification archives and their verification manifests. Known exact R_* memberships are imported with explicit scope: the small C05 full-classification sources, C03B577, C041027, C0165, C03193, and mathematically empty fresh controls. The large C05 physical screen and G/H/W/mixed controls have `original_R_star:null` where M0 does not assert a newly enumerated higher membership.

For the45 known nonempty prehybrid R_* occurrences, a fresh first-edge test reconstructs the original gap endpoints from original producer g IDs, decodes the consumer's complete original pre-B tree, follows its original gap path, and selects the first fresh B primitive deleting an edge of that path. Its actual containing double equals the saved original consuming parent in every case. This checks the residual-to-vertex map without inventing a shadow adjacency.

For every control, independently measured original raw cyclic rank cost on the original S satisfies the frozen periodic threshold. The old periodic source case plus the cheap-packet quota proves its actual overflow empty even when full Pi enumeration is unavailable. WEIGHTS files therefore have exact zero prescribed weights on **every** global vertex. Positive diagnostic R_* weights are kept only in DIAGNOSTIC_PREHYBRID_WEIGHTS, never counted as overflow. No nonempty prescribed overflow is tested or certified here. The universal fiber-partition and root-exclusion proofs do not depend on finding one.

## Preservation and evidence

INPUT_MANIFEST pins C05's66-file exact delivery, C04's60-file delivery, all transitive C03B/C03/C02/C01/EXP04 manifests and older EXP01–03 inputs, plus the original three-slot source and selector implementations. M0_FOREST_WITNESSES links each original source, exact physical record, full forest assignment and current weights with hashes. FINAL_VERIFICATION records the read-only final consistency/preservation checks. M0_DELIVERY_MANIFEST seals the exact final file set, excluding itself. All writes are confined to this new stage; the active branch and tracked files are preserved.
