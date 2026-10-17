# S02_ACCEPTANCE_GATES.md — S02-G01..G24 evaluation

| Gate | Obligation | Verdict | Evidence |
|---|---|---|---|
| G01 | checkpoint + freeze | PASS | e9a801c; 4/4 hashes (legacy erratum `bbb`->`bbc` recorded) |
| G02 | Z3 5.1.0 unchanged | PASS | 5.1.0 at entry; same encoding; no switch |
| G03 | rules + domain | PASS | four-rule freeze intact; canonical-representative argument |
| G04 | strict s/t/w interface | PASS | S02_PIN_AUDIT (295 pins, sha16 `6622c3…`) |
| G05 | no H/q/hidden pins | PASS | engine allowlist; `no_hidden_pins` in evidence |
| G06 | quantifier bounds | PASS | B1 confirmed x2, repaired, nested, regressions unchanged |
| G07 | Tier-1 session soundness | PASS | 3 session tests (completion + 2 contradictions) |
| G08 | B-side propagation sound | PASS | 100/100 + 20/20 xval vs source replay |
| G09 | H/q exact + exhaustive | PASS | derived per word; all corpus H/q measured |
| G10 | skeleton search complete | PASS | 31-family coverage + BFS word exhaustiveness |
| G11 | A-prefix sound | PASS | canonical + replay filter + ssertify decides |
| G12 | inventory sound | PASS | same-populations; Tier-1 decides; no flow invented |
| G13 | incremental frozen Z3 | PASS | compile-once; ResidualSolver stats; S02_SOLVER_PROFILING |
| G14 | E3 SAT replayed | PASS | H=1,q=3,w=-1; 18-item cert; replay agrees |
| G15 | plain SAT replayed | PASS | H=1,q=0,w=2; cert; replay agrees |
| G16 | delkeep SAT replayed | PASS | H=2,q=0,w=4; cert; replay agrees |
| G17 | corpus 10/10 + replay | PASS | E4/negw/zerocost/repeat/macro3/gap0/multigap/mask5/balB/saturated all SAT + 18-item certs + replay |
| G18 | high-cost certified | PASS | q=3,w=3=6-q; fiber; replay-agrees; A-items N/A (B-relation) |
| G19 | negatives correct | PASS | 5/5 UNSAT (w-impossible, marked-count, cyclic, sig, cost) |
| G20 | no hardcoding/hidden gaps | PASS | fixture-divergent words/keys; limits documented (J doc) |
| G21 | model extraction + reconstruction | PASS | 18-item certs (3+10) + high cert; all replay-verified |
| G22 | resource limits | PASS | 0.4/4.0 h; 1.8M/4M nodes; 312/1M queries; 2.5/32 GiB |
| G23 | independent verifier | PASS | fresh process: re-synthesis + 13/13 replay + hashes |
| G24 | reproducible delivery | PASS | after push + remote-HEAD + worktree verification (below) |

ALL 24 PASS => OUTCOME A.
