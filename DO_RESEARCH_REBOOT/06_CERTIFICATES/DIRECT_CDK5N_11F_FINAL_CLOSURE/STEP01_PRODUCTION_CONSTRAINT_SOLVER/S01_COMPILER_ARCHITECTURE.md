# S01_COMPILER_ARCHITECTURE.md — frozen Step-01 stack dataflow

```
PC_TYPED_DAG (authoritative, untouched, 1.6M nodes, hash-consed)
  │  S01_SCOPED_BINDERS.normalize (per compiled root)
  │    outermost-first privatize_binder_pass: duplicate only boundary-shared
  │    scope-carrying nodes (REPLACE-not-add record update = pure alpha-renaming);
  │    validate: each bound name occurs only inside its binder (FAIL CLOSED)
  ▼
S01_DAG_COMPILER.compile_root (single topo pass, cache nid->z3)
  │  Bool->Bool, Int->Int (math-exact), width/signedness -> explicit [lo,hi] bounds,
  │  EXISTS->Exists, FORALL->ForAll, vacuous binders soundly Bool-defaulted
  ▼
S01_SOLVER_INTERFACE.ProductionSolver (one z3.Solver per compiled root)
  │  solve = Tier-1 exact simplify-under-pins (decides grounded queries in ~3 s)
  │          -> Tier-2 check(*assumption-literals), learning retained, no rebuild
  │  extract_model (free vars only) -> S01_MODEL_EXTRACTION.extract_and_verify
  │  (oracle re-check before any downstream use)
  ▼
S01_INCREMENTAL_ENGINE (compile-once registry + push/pop sessions)
```

Two-tier rationale (measured): Tier-2 alone cannot propagate the 1.4M pinned formula
within 120 s (LIA churns 85k rows, reason `canceled`); Tier-1 decides the same query
in ~2.5 s by exact constant folding. Tier-1 is R2-exact (historical partial evaluator);
Tier-2 handles genuinely under-constrained queries (UNKNOWN with reason preserved).
Per-query Tier-1 cost (~3 s at 1.4M nodes) is the documented price of exactness (O5).
