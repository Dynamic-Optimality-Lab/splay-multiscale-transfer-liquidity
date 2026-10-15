# STRICT_ROOT_PATH_THEOREM.md — A2 (root-terminated, simple, exact-depth paths)

## Statement
Every active A-event path has `path[dd] == current root`, pairwise distinct entries, exact
parent-child adjacency with correct sides, target at position zero, and `dd` = actual depth
(= charged depth via the `a = ceil(d/2)` table). Same for B (KEEP events; DELETE vacuous).

## Proof vs implementation
Adjacency+sides+rank-order (verify_path_dyn against evolved states) + root termination
(path[dd]==root selects the full chain: a chain of dd verified parent-links ending at root has
length dd, and target depth is dd) + no-repeat (pairwise disequality) jointly imply the path is
exactly the source access path (unique simple root path in a tree). Depth correctness follows
(length dd+1 ending at root ⟹ target depth dd ⟹ charged a exact).

## Adversarial confirmation
Shortened paths (evd decremented: path no longer root-terminated) UNSAT; duplicated nodes UNSAT;
both verified as circuit rejections (not test-harness filters).

## Gate A2: REPRODUCED + REPAIRED.
