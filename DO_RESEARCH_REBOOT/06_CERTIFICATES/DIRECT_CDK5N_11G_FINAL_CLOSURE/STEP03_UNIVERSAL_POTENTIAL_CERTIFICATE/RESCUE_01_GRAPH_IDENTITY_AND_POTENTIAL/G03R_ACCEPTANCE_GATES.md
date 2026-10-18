# G03R Acceptance Gates R03-01..R03-21

| Gate | Requirement | Verdict |
|---|---|---|
| R03-01 | HEAD + frozen source hashes verified | PASS (163047d; sha manifest) |
| R03-02 | Historical Step-03 verdict preserved | PASS (IV22, file untouched) |
| R03-03 | Canon corrected | PASS (T-A1..T-A10) |
| R03-04 | Full ordinary-state schema | PASS (147 fields, IV04) |
| R03-05 | T-A1..T-A10 | PASS (12/12) |
| R03-06 | Missing/malformed rejected | PASS (T-A6) |
| R03-07 | Historical graph recomputed | PASS (prefix vs corrected) |
| R03-08 | Full-state graph rebuilt | PASS (40 edges, provenance) |
| R03-09 | Provenance retained | PASS (IV09) |
| R03-10 | SCC + BF executed | PASS (IV10-13) |
| R03-11 | Cycles independently verified | PASS (controls; none found) |
| R03-12 | Return paths investigated | PASS (D2+D3-concrete; symbolic open) |
| R03-13 | SAT/UNSAT/UNKNOWN scoped | PASS (IV19-20) |
| R03-14 | Feature semantics audited | PASS (Gate F) |
| R03-15 | Feature matrix constructed | PASS (rank 11, nullity 4) |
| R03-16 | Infeasibility claims certified | PASS (honest: none exists; recorded) |
| R03-17 | No circulation-as-cycle | PASS (IV17) |
| R03-18 | Ledger reconciled | PASS (G03R_RESOURCE_LEDGER.json) |
| R03-19 | Rules + freeze preserved | PASS (IV02, additive only) |
| R03-20 | Independent verifier PASS | PASS (25/25) |
| R03-21 | Additive commit + remote PASS | PENDING (this commit) |

Repair complete iff all PASS after push verification.
