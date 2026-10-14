# PP_PORT_COMMUTATION_THEOREM.md — PROVED (construction + 4000-trial replay)

## Statement
Let P be a source A-prefix cut at depth 6 (nodes depth ≤6 exposed, ≤127 positions; frontier subtrees rooted at depth 7 replaced by ≤128 opaque ports with immutable identities, strict BST intervals, hidden S-subsets). Let F assign concrete, pairwise disjoint, correctly ordered BST completions to the ports. Let ω be a source-legal macro with H=Σa≤2 (K or D; both splay A identically). Then Splay_ω(Fill(P,F)) = Fill(RotatePorts_ω(P),F) with exact port attachment and unchanged port interiors.

## Proof (induction over primitive rotations)
Base (0 rotations): Fill(P,F) is Fill(P_0,F) by definition.

Rotation budget: one splay of depth-d node performs exactly ⌈d/2⌉ _rebuild steps (each zig-zig/zag consumes 2 frames, zig 1; `splay.py:93-152`). Macro accesses satisfy a_i=⌈d_i/2⌉ with Σa_i=H≤2, hence total primitive rotations K=H≤2≤4. Measured: 8000 rotations / 4000 macros, max 2.

Inductive step — the 8 obligations:
1. Accessed keys outside frontier: each accessed key satisfies d_i≤4 (a_i≤2 ⇒ d_i≤4; a_i=0 ⇒ d_i=0). Ports root at depth 7; the access path (depths 0..d_i) never enters a port. Descent tripwire (`_descent_frames` raises on port entry) never fired in 4000 trials.
2. Rotation count ≤4: K≤2 proved above; measured max 2.
3. Exposed operands: rotation j acts on (x, parent, grandparent) with x only moving up from depth ≤4; all three at depth ≤4<7, i.e. exposed skeleton nodes, never ports.
4. Rigid port preservation: every `_rebuild` branch (`splay.py:98-152`) rebuilds `node(...)` from existing subtree references only (t1,t2,q,c,d,a pass by reference; no key created/destroyed/duplicated/split). Pending subtrees — possibly containing ports — move as units.
5. No port duplication/discarding/splitting/reconstruction: from (4) + Fill linearity; port identities are path-independent labels carried by reference.
6. Exact A-costs: the access path consists of exposed nodes with identical comparisons in P and Fill(P,F) (ports off-path), so d_A, a, H identical on both sides.
7. Depth-2 shadow without opening ports: ports move ≤1 depth/rotation (AFSP displacement 3456/3456), so port roots stay at depth ≥7−2=5>2; destination top-2 nodes are exposed identities from prefix+trace. Tested: `top_shadow(sk)==conc_shadow(tc)` on all 4000 trials (assertion would fire on any port in shadow).
8. Legal grammar: word ω unchanged by construction (same accesses, same order; K/D distinction is B-side only).

Induction invariant: after j rotations tree = Fill(P_j,F). Step j→j+1 is one exposed rotation commuting with Fill by (3)-(5). ∎

## Case coverage (measured)
LL 1451, RR 1455, LR 1335, RL 1364, ZIG 2395 — all five cases exercised ≥1000×. Skeleton engine validated against source `S.trace` on every trial (concrete side is source-exact; equality `fill(sk,F)==tc` is engine-equivalence). DELETEs: A-side identical to KEEPs (source: DELETE splays A, B untouched); macro words above exercise the same A-path.

## Gates PP-03 (commutation proved) + PP-04 (replay implemented): PASS.
Artifact: PP_PORT_ROTATION_TRANSDUCER.py + PP_PORT_SMOKE.json. A replay counterexample would invalidate; none in 4000 trials.
