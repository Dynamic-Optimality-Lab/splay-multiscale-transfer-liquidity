# S01_SUPPORTED_LOGIC.md — frozen formula language (no silent fallbacks)

| DAG kind | Compiled form | Notes |
|---|---|---|
| const (Bool/Int) | BoolVal / IntVal | exact values incl. negatives |
| var Bool | z3.Bool | |
| var Int (w, signed?) | z3.Int + `lo<=v<=hi` bound | bound table = `width_domain` = historical `Solver.domain` |
| not/and/or/xor | Not/And/Or/Xor | |
| ite | If (cond Bool; branches DAG-typed equal) | |
| eq/lt/le | ==/</<= (Int math; Bool equality) | signedness structural (Int has none) |
| add/sub | +/- on Int (exact, unbounded) | width metadata carried, never wraps |
| exists | z3.Exists over normalized binders | skolemized SAT, complete on finite domains |
| forall | z3.ForAll (Q4/Q5 regressions only) | finite-domain instances decided or unknown |

Any other node kind raises `AssertionError` at translation (no TRUE/FALSE fallback).
Non-Bool roots rejected at `compile`. Out-of-domain pins -> UNSAT `domain-violation`.
Bound-name pins rejected (`api-validation`); out-of-cone pins ignored+counted
(historical behavior). UNKNOWN reasons preserved verbatim (`timeout`/`canceled`/
`incomplete`/validation). No UNKNOWN->SAT/UNSAT coercion anywhere.
