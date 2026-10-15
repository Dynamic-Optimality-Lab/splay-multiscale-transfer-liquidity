# STRICT_QUANTIFIER_SEMANTICS.md — backend status (unchanged, characterized, not re-attempted)

## Frozen backend (R3: no switch)
PC_SOLVER_BACKEND.py: finite-domain backtracking + interval/bounds propagation + top-level EQ
pinning + assumption simplification + iterative (recursion-free) evaluation + deterministic order.
Dinic reused for inventory subproblems. No CDCL/SMT/QBF component was introduced (none needed for
the executed verification scope; all queries here are grounded-eval or bounded-UNSAT).

## Semantics status (imported from predecessor campaign, undisplaced)
- Existential quantification: solver searches bound vars; grounded models verify by evaluation.
- Negation of existentials: De Morgan over finite domains; MinPre lower-exclusion tested (20/20
  bounded UNSAT, 0 UNKNOWN at micro scope).
- Nesting/capture/shadowing: subst renaming unit-tested (binder hygiene SAT/UNSAT exact).
- Sort separation: ordinary/midpoint predicates never merge (type tests).
- SAT sound (models verify), UNSAT sound (exhaustive within bounds+caps), UNKNOWN distinct
  (returned on cap, never converted).
- Mandatory properties 1-12 (mission §8): finite domains exact; widths proved; no wraparound
  (exact-int semantics + assertions); scope/capture correct; alternation via De Morgan;
  witness reconstruction verified (V12 pattern); UNKNOWN recorded; assumptions incremental
  (pins+simplify sound); operators executable at grounded/micro scope; configuration
  reproducible (seeded, deterministic); adversarial tests green.

## What was NOT done (HARD STOP)
Free-witness synthesis beyond micro scope (predecessor UNKNOWN stands); full-domain decision
procedure termination (SC20 OPEN inherited). No new backend work performed in this campaign.

## Gate SC18: backend semantics certified at executed scope (PASS for phases 1-3 scope).
