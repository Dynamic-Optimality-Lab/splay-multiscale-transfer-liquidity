# FINAL_CLOSURE_FOUR_RULE_FREEZE.md — one frozen four-step campaign (R1-T/R2/R3/R4)

## Frozen scope (Steps 01–04, immutable)
- R1-T: `∀W∈W_5^9, Q_B(W)≤2A(W)` — five genuine B-changing KEEPs, nine-node marked B-core,
  126 masks, arbitrary fringe, KEEP/DELETE, zero-cost accesses, nongenuine KEEPs, E3/E4,
  arbitrary legal word lengths, exact paired-state closure, diagonal reachability.
- Representation: `s=(μ,b,α,σ)`; nine-core B-controller; 7-position A-shadow; 10 saturated
  fringe-signature coordinates; five-of-nine marked mask; low persistent-port relation
  (w∈[-4,4]); high WQ midpoint (w=6-q s→m, 0 m→t); genuine abstract endpoints.
- Sources (SHA256): eventflow `d7cc8060…30053`, coarse_double `b47019af…00365f`,
  splay `3a178c13…3f91d2f01`, legacy_embedding `20284bbb…543e1cb2`.
- Baseline: 1,603,069-node shared product at `a76354b` (branch `coarse-double-branch`).
- Solver stack (Step 01 freeze, no switching): Z3 5.1.0 via z3-solver 5.1.0.0, Int-exact
  encoding, native Exists/Forall, push/pop + assumption literals (see STEP01 freeze docs).
- Caps (cumulative, no reset): 12 CPU-h · 32 GiB · 4M DAG nodes · 2M states · 5M edges ·
  1M solver queries · ≥15% CPU reserve for independent verification.
- Preregistered CPU plan: Step01 4.0h · Step02 4.0h · Step03 1.5h · Step04 0.7h · reserve 1.8h.

## Freeze rules
- No solver-family switching after `S01_BACKEND_FREEZE.json`. No new state coordinate,
  observable, saturation threshold, causal depth, cap increase, or architecture pivot.
- Additive artifacts only. No history modification. No 11G / terminal claim / Bank25 change
  without separate explicit authorization (Steps 02–04 authorized separately).
