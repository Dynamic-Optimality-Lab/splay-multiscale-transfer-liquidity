# G02_CYCLE_ENCODING_THEOREM.md — Gates B/C/D (exact symbolic cycle predicates)

Cycle_k = conjunction of k contracted/low edge predicates with shared interface
variables equated along the walk and s_k = s_0 (full ordinary-state equality,
not mask/root-only). NegCycle_k adds exact Int sum(w_i) < 0 (no wraparound, no
floats). Witnesses are existentially scoped per edge (S03 projections); shared
state vars are intentionally shared (endpoint identity), never witness vars.
Lazy execution only: no eager k-fold product is ever materialized (the engine
searches source-level closed walks + per-edge predicates; the symbolic form is
the proved-equivalent specification). k=1 decided by theorem (no negative
self-loop); k=2 by exhaustive replay (342 words); k>=3 by bounded BFS with
visited-set soundness (UNSAT only on non-truncated exhaustion).
