# S03_ACCEPTANCE_GATES.md — S03-G01..G25 evaluation (all evidence-linked)

| Gate | Requirement | Verdict | Evidence |
|---|---|---|---|
| G01 | entry HEAD/hashes/freeze | PASS | 32eb946; 4/4 hashes; Z3 5.1.0 |
| G02 | Steps 01/02 reused, no edits | PASS | worktree history-clean verified mid-step; additive only |
| G03 | ledger reconciled | PASS | S03_RESOURCE_RECONCILIATION.md; conservative 0.87 carried |
| G04 | two-sort universes exact | PASS | U_O/U_M/U_O2 wired; complement relative to universes |
| G05 | weight/sort table exact | PASS | S03_WEIGHT_SORT_MATRIX (OO -4..4, OM 2..6, MM FALSE) |
| G06 | low witnesses closed | PASS | 24/24 free-var audits, zero outside |
| G07 | high witnesses closed | PASS | OM/MO/hs/hd audits; q bound in MO |
| G08 | no undeclared free witness | PASS | mechanical audit FAIL-CLOSED per edge |
| G09 | scope + domains certified | PASS | 23 projections normalize clean; in-scope bounds (B1) |
| G10 | WQ factorization certified | PASS | S03_WQ_FACTORIZATION_AUDIT; J4/J5 |
| G11 | two-sort Pre exact | PASS | 4070 agreements; J1-J3/J9/J10a |
| G12 | two-sort Post exact | PASS | 4070 agreements (namespace defect found+fixed); J1-J3 |
| G13 | MinPre negation exact | PASS | symbolic form + procedure equivalence; J7/J8 |
| G14 | Step-02 UNKNOWN never UNSAT | PASS | discipline encoded; a-incomplete/word-truncated propagate |
| G15 | complement/equiv/empty exact | PASS | 4070 comparisons; decided equivalence; distinct statuses |
| G16 | nesting correct | PASS | Pre(Post), MinPre(Pre), shadows, collisions; capture defects fixed |
| G17 | small-graph oracle PASS | PASS | 4070/4070, 4 families, exhaustive X subsets |
| G18 | E3/plain/delkeep PASS | PASS | SAT + H/q/words (1/3;1/0;2/0) |
| G19 | high + zero-midpoint PASS | PASS | J4 q=3/w=3 SAT; J5 full-env Tier-1 SAT |
| G20 | real MinPre exclusion certified | PASS | J7 FALSE via w=-1 edge (lower-weight-edge cert) |
| G21 | real MinPre positive certified | PASS | J8 TRUE (lowers -4..-2 certified absent, H>=1 proof) |
| G22 | mandatory queries executable | PASS | all decided; zero mandatory UNKNOWN |
| G23 | DAG + resource limits | PASS | 1.7M/4M; 0.9/1.5 h; 4600/1M queries; 2.5/32 GiB |
| G24 | independent verification | PASS | fresh process: re-synthesis + hashes + artifacts |
| G25 | reproducible delivery | PASS | after push + remote-HEAD + worktree check (below) |

25/25 PASS => OUTCOME A.
