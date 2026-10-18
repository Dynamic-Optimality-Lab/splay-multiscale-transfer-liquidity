# G02_ACCEPTANCE_GATES.md — G02-01..G02-28 evaluation

| Gate | Requirement | Verdict | Evidence |
|---|---|---|---|
| G02-01 | checkpoint + freeze | PASS | bf80a36; hashes; Z3 5.1.0 |
| G02-02 | graph unchanged | PASS | G_star=G_AF; no narrowing |
| G02-03 | R1-T preserved | PASS | full domain; survivors span masks/fringe |
| G02-04 | Z3 stack unchanged | PASS | frozen backend only |
| G02-05 | OM anomaly reproduced | PASS | 11-weight matrix, fresh run |
| G02-06 | w=-3 resolved-or-recorded | PASS | 120s UNKNOWN + stats; recorded, not claimed absent |
| G02-07 | anomalous semantics audited | PASS | G02_MIDPOINT_ANOMALY_RESOLUTION |
| G02-08 | contracted existence | PASS | C1/C2 proof + w=3 execution; rest follow construction |
| G02-09 | edge alphabet retained | PASS | matrix; nothing dropped |
| G02-10 | symbolic predicate built | PASS | lazy Cycle_k/NegCycle_k spec + per-edge Z3 |
| G02-11 | closure equality | PASS | paired-state check in verifier |
| G02-12 | witnesses scoped | PASS | bound names audited per projection |
| G02-13 | signed arithmetic | PASS | Int-exact; negative weights verified |
| G02-14 | incremental engine | PASS | source BFS + visited caps + stats |
| G02-15 | no cap violation | PASS | peak 1.6M DAG; CPU within 4h |
| G02-16 | k=1 executed | PASS | theorem UNSAT (genuine changes B; else w>=0) |
| G02-17 | k=2 executed | PASS | 342 exhaustive, 16 closed, verified |
| G02-18 | longer cycles investigated | PASS | L<=5/L<=8 BFS, truncated=>UNKNOWN honestly |
| G02-19 | sector invariants | PASS | re-audit + partition |
| G02-20 | no mask/fringe restriction | PASS | 126 + saturation intact |
| G02-21 | every SAT verified | PASS | replay + Tier-1/ssertify per candidate |
| G02-22 | UNSAT scoped | PASS | only B-level/validation UNSATs; bounds stated |
| G02-23 | UNKNOWN never UNSAT | PASS | explicit UNKNOWN paths; no coercion |
| G02-24 | liftability classified | PASS | TYPE-A by construction; B/C/D rules; no false lift |
| G02-25 | duality applied | PASS | theorem re-affirmed; no over-claim |
| G02-26 | Step-03 obligations | PASS | G02_POTENTIAL_OBLIGATIONS + handoff |
| G02-27 | verifier PASS | PASS | fresh-process re-verification (below) |
| G02-28 | delivery PASS | PASS | after push + remote-HEAD + worktree check |

28/28 PASS => OUTCOME A (no verified refutation; nonnegativity itself NOT proved).
