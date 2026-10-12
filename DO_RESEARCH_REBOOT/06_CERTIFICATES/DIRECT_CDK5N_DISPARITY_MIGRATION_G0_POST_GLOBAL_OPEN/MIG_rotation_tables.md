# Primitive splay rotation transformation tables (P2) + verification

## Splay step inventory (from python/independent/splay.py _rebuild)

Frames outermost-first; while frames remain: LL / RR / LR / RL double steps
(consume 2 frames), else single ZIG (1 frame). Each step rebuilds cur as
node(x,...) with fixed subtree reattachment (code lines 98–152). A splay at
depth d uses exactly ⌈d/2⌉ steps and exactly d rotations: double steps
contribute 2 rotations each, final zig 1 iff d odd.

## Ancestor-incidence effects (proved by code inspection + exhaustive check)

For a single rotation at node k (right rotation with left child lk, resp.
left rotation with right child rk), ONLY ancestor relations involving keys
in the rotated triple {k, lk/rk} ∪ attached subtrees can change; keys
outside keep identical ancestor sets. Precisely (right rotation):
- lk gains no new ancestors except k's former ancestors (lk rises one level);
  k gains lk as ancestor (+1 depth); keys in lr gain k (was lk) — their
  ancestor set swaps lk↔k at that position; keys in ll, q, c unchanged sets.
- Hence per rotation, Ω(x,z) can change only for x in {k,lk} ∪ lr-subtree
  keys and z in {k,lk} ∪ their ancestor chain. All other coordinates fixed.
Mirror statement for left rotation. Double steps (zig-zig/zig-zag) are two
such rotations composed; zig-zag additionally swaps subtree sides (code
lines 118–137), affecting the same bounded key set (x, kp, kg + subtrees
t1,t2 + outer frames untouched).

## Verified bounds (exhaustive, script MIG_rotation_tables.py)

- Exhaustive single-rotation ancestor-incidence changes: n=3→3, n=4→4,
  n=5→5, n=6→6, n=7→7 (shapes 5/14/42/132/429; maxima over all rotations).
  Pattern max1(n)=n.
- Analytic lifting: effects are local to the rotated subtree (frames above
  untouched — _rebuild pops only the step's frames, _plug reattaches the
  remainder identically); each affected key gains/loses at most the swapped
  pair ⇒ ≤2n coordinate changes per rotation at ambient size n (measured n
  for n≤7).
- Splay at depth d: exactly d rotations ⇒ ≤2nd gross coordinate changes
  (NOT paid surplus — see ledgers + double-spend audit).

## Status

P2 transformation rules: PROVED (code-derived case analysis + exhaustive
small-tree verification). Usability for net surplus: NONE established
(gross counts only; see P3/P4 + double-spend audit).
