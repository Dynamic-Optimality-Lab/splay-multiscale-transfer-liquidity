# S04_BOUNDARY_CONSISTENCY_THEOREM.md — Gate G U10/U12 (F04-27/F04-28)

Macro boundaries are abstract states (147-field S-vectors + weight var) satisfying
state_valid7 (U1, Tier-1 checked per boundary). Composition = pin-equality:
destination pins of macro j serve as source pins of macro j+1 (same namespace
after sort-tag relabeling; B/mu/sig skeletons field-compatible). Engine
abstract-match enforces coincidence per macro (env-derived pins == query pins).
Demonstrated executably: composed 2-chain E3(w=-1) -> edge(w=1) with verified
pin chaining (S04_ORIGINAL_TO_ABSTRACT_CHECK). Closure: exact paired closure
(A_T,B_T)=(A_0,B_0) replays to identical serials, which abstract identically
(ssertify determinism on identical inputs); hence abstract path closes. No
operation is discarded in segmentation (replay legs cover every word access;
segmentation origins are cyclic rotations preserving the access multiset).
