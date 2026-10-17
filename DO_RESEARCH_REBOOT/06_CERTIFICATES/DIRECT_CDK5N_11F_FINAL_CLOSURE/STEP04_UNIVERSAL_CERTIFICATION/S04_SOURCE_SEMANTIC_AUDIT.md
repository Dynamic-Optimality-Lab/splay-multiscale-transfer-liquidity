# S04_SOURCE_SEMANTIC_AUDIT.md — implementation audit (F04-14/F04-15)

Splay/rotations: structural splay == source replay 100/100 (Step-02) + 50/50
fresh here; zig/zigzig/zigzag all exercised (adversarial rotation tally agrees).
B-controller: 9-core + 10-gap refs, NULL-safe, cycle-guarded; BState decode +
topo equality used by engine (B-BFS words all replay-agreeing). A-shadow (7
positions, kinds/S-labels/indices) derived by alpha7_of and matched per boundary
(ssertify shadow_match on every witness). Ports (127 slots, depth ≤6, frontier
depth 7, NULL refs) with wellformed/link/bound conjuncts, all True under witness
envs (conjunct audit). Inventory (attach/valid + compat + same populations):
True under witness envs; gap pools canonical. Rotations ≤4/event, nev ≤5, H ≤2
(low) enforced and measured on all witnesses. No source-semantic deviation found.
