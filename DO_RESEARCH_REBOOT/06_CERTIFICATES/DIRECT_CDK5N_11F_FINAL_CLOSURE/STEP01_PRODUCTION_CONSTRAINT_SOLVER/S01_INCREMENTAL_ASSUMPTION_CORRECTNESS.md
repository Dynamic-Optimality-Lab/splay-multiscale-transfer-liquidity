# S01_INCREMENTAL_ASSUMPTION_CORRECTNESS.md

## Claim
One compiled handle answers arbitrarily many assumption sets without recompilation,
and queries are independent (no cross-query interference).

## Mechanism
- Per-query assumptions become `check(*literals)` arguments (Tier-2) or Tier-1 pins;
  nothing is asserted persistently by `solve`. Sessions use explicit push/pop with
  `pin` asserting into the pushed scope only.
- Validation: bound-name pins rejected (UNKNOWN + reason, never reinterpreted);
  out-of-cone pins ignored+counted; out-of-domain pins UNSAT (`domain-violation`).

## Evidence (S01_INCREMENTAL_RESULTS.json, 1 handle, 0 rebuilds)
- Full-env E3 -> SAT; full-env plain -> SAT; H-flipped -> UNSAT (Tier-1, ~2.5 s each).
- Session with 297 endpoint pins -> UNKNOWN `canceled` at 30 s cap (honest wall);
  same session + contradicting H -> UNSAT (session pins genuinely constrain).
- `reset_assumptions` reports assertion count; post-pop queries reproduce pre-session
  verdicts (E_session UNSAT == standalone C UNSAT). Z3 statistics recorded per handle.
