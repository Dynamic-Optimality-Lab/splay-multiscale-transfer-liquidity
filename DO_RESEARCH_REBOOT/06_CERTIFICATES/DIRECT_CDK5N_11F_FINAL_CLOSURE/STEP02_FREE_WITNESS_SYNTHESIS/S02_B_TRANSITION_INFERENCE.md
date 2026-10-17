# S02_B_TRANSITION_INFERENCE.md — source-derived B-side filter (Gates C1/G08)

Structural splay on S-index ref-topologies (no concrete keys: splay cases are
structural; BST order rides initial inorder labels), cross-validated 100/100
against the untouched source replay (`splay_B_push`), plus 20/20 in evidence.
BFS over abstract B-states (KEEP S-index targets, DELETE = identity, nongenuine
KEEP-at-root = identity loop) to max 5 events; terminal must be genuine
(marked + B-changing); q = floor(terminal depth/2). Every rejection is
splay-semantic (unreachable topology, unmarked/nongenuine terminal, malformed or
cyclic input topology). Cycle-guarded + step-capped (no hangs on adversarial pins).
