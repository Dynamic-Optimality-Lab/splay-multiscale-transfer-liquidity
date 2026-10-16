# S01_BACKEND_RATIONALE.md — why this single stack

## Candidates examined (actual environment)
- **Z3 5.1.0 (z3-solver wheel, present)**: native SAT/SMT, incremental push/pop +
  assumption literals, model extraction, timeouts + memory cap, BV/Int/quantifiers,
  deterministic seeds. No install needed; version pinned.
- **Standalone SAT (MiniSat/CaDiCaL/Glucose)**: no binaries present; a DIMACS pipeline
  would sacrifice native incrementality and require a new bit-blasting frontend —
  larger trusted base, weaker interface. Rejected.
- **QBF solvers**: none available. Rejected.
- **Bit-vector encoding inside Z3**: decidable but bit-blasts 32-bit adders across
  ~1.6M nodes — CNF-size risk with no semantic benefit, since historical semantics is
  exact mathematical integer arithmetic. Rejected as primary (kept out of the freeze).
- **Python DPLL (QSolver)**: the measured bottleneck (~2 s/visit). Rejected as engine;
  retained as cross-check oracle only.

## Why Z3 + Int-exact
1. **Semantic identity**: `z3.Int` IS mathematical-integer arithmetic — the encoding
   equals the historical `ev_iter` semantics by construction, so no wraparound theorem
   is owed; the width audit only records ranges and signedness.
2. **Quantifiers**: native `Exists`/`Forall` with scope-correct normalization ahead of
   compilation; no binder-dropping, no global name-stripping as semantics.
3. **Incrementality**: compile once, then push/pop + assumption literals per query with
   retained learning — the exact S6 requirement.
4. **Arithmetic propagation**: LIA Simplex propagates arithmetic-heavy constraints far
   better than bit-blasting or interpreted interval eval.

## Risk carried openly
Z3 may return `unknown` (quantifier incompleteness, resource caps) — reported as UNKNOWN
per R2, never coerced. If the full product exceeds memory/time budgets, OUTCOME B with
measured bottleneck (no stack switch per R3).
