# CW_MARKED_CORE_MONOTONICITY.md — Gate C: nine-core invariance (re-audited + proved)

## Step invariant (primitive-rotation level re-audit)
For operations in an admissible closed word (M=G(W)=K(W) by Gates A/B):
- DELETE: B unchanged → C_M identical.
- Zero-cost KEEP (root target): no rotations → identical.
- Genuine KEEP (marked target, non-root): marked-target splay ⟹ C_M nonincreasing (rotation
  induction re-audited primitive-by-primitive: only the marked target can join, and it is already
  a member; all other nodes shrink-or-hold; ancestors above keep key sets; rigid subtrees keep
  status). Nongenuine KEEPs target marked keys (Gate B) at B-root (Lemma 1) → identity → identical.
Hence `C_M(B_{t+1}) ⊆ C_M(B_t)` for every operation. No step type escapes (DELETE/zero-cost/
genuine/nongenuine exhaust R1-T operations affecting B).

## Constancy from exact closure
B_T = B_0 (exact, full-tree) gives C_M(B_T) = C_M(B_0). A nonincreasing finite-set chain with equal
endpoints is constant: `C_M(B_t) = S` for all t, where `S = C_M(B_0)`. Measured: 200/200 admissible
corpus closed walks have constant C_G (0 violations).

## Cardinality and the nine core
R1-T requires the complete marked B-ancestor core nine at every cyclic state: |C_M(B_t)| = 9.
With constancy, S is one fixed 9-set per walk. Consequences (all proved, §6 items 1-7):
1. Core identities fixed (set equality across t).
2. Marked targets stay in S (endpoints always members).
3. Every marked ancestor in S (ancestors of marked are in C_M by definition).
4. Marked search paths represented by S (paths ⊆ S).
5. No unrepresented insertion (insertion would grow C_M, forbidden by constancy).
6. Source B-depth = induced-tree depth on S (all ancestors in S; ancestor relations preserved
   in the ancestor-closed induced subtree).
7. `q_t(x) = floor(d_{B|S}(x)/2)`, `0 <= q <= 4` (|S|=9 → depths ≤8).
No inference from tests alone (200/200 corroborates; proof is the chain+closure argument).

## S vs fixed identities (representational note for Gate E)
S is walk-stable but walk-varying (200 corpus walks have varying C_G sets). The symbolic
S-indices therefore label sorted C_M members per walk (order-faithful relabeling at the
concretize mapping, not a circuit change): S-index i = i-th C_M member; masks = genuine positions;
gaps = between consecutive C_M members; fringe = complement. All order/cost machinery transfers
verbatim. "Nine fixed core identities" (§3) = nine per-walk-stable identities. No new coordinate;
no new observable; same circuit, same caps.

## Gates CW05+CW06: PASS (proved + 200/200 constancy + K=G on closed walks).
