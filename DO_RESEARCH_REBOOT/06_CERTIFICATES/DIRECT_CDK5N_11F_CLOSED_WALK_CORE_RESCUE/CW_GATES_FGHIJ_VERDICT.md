# CW_GATES_FGHIJ_VERDICT.md — Gates F–J verdict + campaign outcome (FAIL CLOSED)

## Gate F (high relation): PASS
- `CW_HIGH_EDGE_RESULTS.json`: grounded=319, fibers=5, skipped=0.
- Live anchor CW09: preregistered E3 re-grounded on a fresh SL build → ok, H=1 q=3 w=-1.
- Fringe-q correspondence CLOSED (Gate E theorem + 266 re-audit).

## Gate G (product): PASS
- Fresh live build: 1,603,069 nodes (operator-test DAG 1,603,081 incl. operator universes).
- 9/9 low weight edges present (w=-4..4); out-of-band w=5 is Boolean False.
- `E_sm`/`E_mt` quantified (exists in cone); high src/dst quantified.
- Renaming soundness: SL→CL bridge is a tag isomorphism; 16/16 membership agrees via
  `ev_iter` on bridged envs (CW11); unbridged-var guard raises (no silent partial envs).

## Gate H (free-witness synthesis): PASS-WITH-REMAINDER (wall stands)
- 3/3 preregistered cases grounded ok (E3 H=1 q=3 w=-1; plain H=1 q=0 w=2; delkeep H=2 q=0 w=4).
- 3/3 free-witness searches UNKNOWN at 240 s caps (visits 120/132/138; ~2 s/visit over
  1.4M nodes). QSolver used throughout; root is quantifier-free so behavior is parity
  with the historical backend. The synthesis wall is MEASURED, not moved.

## Gate I (operators): PASS
- New deliverable `CW_QUANTIFIED_BACKEND.py` (QSolver): pin-stripping of capture pins,
  bound exclusion from splitting, leaf sub-solving with shared caps; UNKNOWN on
  exhaustion, never a wrong claim. No historical file modified (verified via git status).
- Units: binder shadow pair, MinPre not+exists structure, empty target, neg-exists UNSAT.
- Micro battery: agree=16, unsat=16, unknown=0 (bounded 45 s / 200 k nodes).
- Cross-backend parity on quantifier-free formulas: SAT/SAT with identical models.
- `CW_SYMBOLIC_OPERATORS.py` `is_empty`/`extract_witness`/`extract_edge_witness` now
  default to QSolver.

## Gate J (universal CW01–CW25): PASS 25/25 in 42 s (`CW_UNIVERSAL_RESULTS.json`)

## Campaign outcome: OUTCOME B (partial closure, remainder recorded)
- Rescued: domain equivalence (A), K=G (B), nine-core invariance (C), counterexample
  classification (D), fringe-q closure (E), high grounding (F), product (G), operators (I),
  universal battery (J).
- Remainder: free-witness synthesis (H) UNKNOWN at all tested scopes.
- Stage 11F stays OPEN; terminal `CDK5N-TERMINAL-A` stays OPEN. No 11G/successor/promotion.
- STOP after commit + push + remote-HEAD verification.
