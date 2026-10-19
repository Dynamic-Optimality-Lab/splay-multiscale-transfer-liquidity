# CORE-01 Marked-Core Definition (frozen)

C_M(B) = union over marked S-indices m (mu bits 0..8) of ancestor chains
to root, computed over the 19-slot parent links (core_of_env). mu is
transition-invariant (s_mu == t_mu conjuncts). Valid states: b_valid +
b_tree_valid (connectivity, BST intervals, gap-slot emptiness, root span
[0,18]). The closure is a deterministic total function of the 147-field
state (BFS ancestor walk terminates; unreachable marked nodes still counted
as themselves). Distinct from: the 9-position controller (fixed slots),
the full core S (all 9 S-indices — C_M is a SUBSET in general; fringe
ancestors may appear: C_M=S is REFUTED as universal state claim per
STRICT_MARKED_CORE_MONOTONICITY).
