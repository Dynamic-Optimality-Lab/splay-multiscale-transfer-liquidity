# CL-01 Acceptance Gates

| Gate | Requirement | Verdict |
|---|---|---|
| CL01-01 | Entry HEAD + hashes | PASS |
| CL01-02 | History preserved | PASS |
| CL01-03 | SR-02C CPU reconciled (340 vs 501.6) | PASS (erratum: ~555.7s actual) |
| CL01-04 | Cumulative budget stated | PASS (~3.10h/3.5h; caps respected) |
| CL01-05 | Substep overrun classified | DOCUMENTED OVERAGE (allowance 236s; used ~555s) |
| CL01-06 | Depth record repaired | PASS (5->7 x6, 6->7 x3 +1 hold) |
| CL01-07 | Counterexample scope stated | PASS (4-level: 1-2 recomputed, 3 original, 4 open) |
| CL01-08 | Potential stays refuted | PASS |
| CL01-09 | Offset obstruction checked | PASS (K<=2 AND K>=7 verified) |
| CL01-10 | Crossing count proved | PASS |
| CL01-11 | Decomposition proved | PASS |
| CL01-12 | Deficit identity proved | PASS |
| CL01-13 | Conditional criterion proved | PASS (H1/H2/H3 open, labeled) |
| CL01-14 | No conditional misreport | PASS |
| CL01-15 | Repayment investigated | PASS (B-core/A-shadow/push; no premise found) |
| CL01-16 | Pushes included | PASS |
| CL01-17 | Historical 0->1 tested | PASS (8 crossings + 1 hold evaluated) |
| CL01-18 | Graph scope retained | PASS |
| CL01-19 | Anomalies retained | PASS |
| CL01-20 | Cycle-level candidate or impossibility | PASS (R(P)>=0 candidate + offset no-go) |
| CL01-21 | Statuses distinguished | PASS |
| CL01-22 | Independent review | PASS (9/9) |
| CL01-23 | No unauthorized expenditure | CL-01 CLEAN (arithmetic only); SR-02C overage documented, not repeated |
| CL01-24 | Delivery + HARD STOP | PENDING (this commit) |
