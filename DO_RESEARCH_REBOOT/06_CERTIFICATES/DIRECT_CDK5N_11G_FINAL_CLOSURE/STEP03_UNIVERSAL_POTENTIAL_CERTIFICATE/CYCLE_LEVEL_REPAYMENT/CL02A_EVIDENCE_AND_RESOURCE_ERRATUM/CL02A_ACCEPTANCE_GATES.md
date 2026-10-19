# CL-02A Acceptance Gates

| Gate | Requirement | Verdict |
|---|---|---|
| A01 | Entry HEAD + hashes | PASS |
| A02 | CL-02 artifacts preserved | PASS (read-only; no modification) |
| A03 | All excursion JSONs inspected | PASS (7 files + verifier) |
| A04 | Duplicates identified | PASS (base==S802 bytes; S801/FULL same excursion) |
| A05 | Distinct count grounded | PASS (2 distinct: P1, P2) |
| A06 | P1 full-state certificate audited | PASS (147 fields, canon, validity, features) |
| A07 | P2 state completeness audited | PASS (feature-only; PARTIAL recorded) |
| A08 | Chaining scope recorded | PASS (P1 verified; P2 builder-only) |
| A09 | Verifier coverage identified | PASS (FULL-only; X02 record-only; same code path) |
| A10 | Unconditional PASS documented | PASS (X02 record-only; X04 conditional gate) |
| A11 | Certification vs re-solve distinguished | PASS (4-level table) |
| A12 | Weights/residuals rechecked | PASS (from stored data) |
| A13 | No fabrication | PASS |
| A14 | Pre-CL-02 ledger reconciled/stated | PASS (reported-estimates, uncertainty flagged) |
| A15 | CL-02 CPU inventory reconstructed | PASS (~1205s measured) |
| A16 | Duplicates vs disjoint distinguished | PASS (copies counted once) |
| A17 | 1400-vs-1320 adjudicated | PASS (1320 parts; +80 unexplained; use 1205) |
| A18 | 480s substep classified | CONDITIONAL (authorization unevidenced; IF applied: exceeded ~724s) |
| A19 | Hard-cap classified | UNRESOLVED leaning BREACH (~540s over on point estimates; baseline uncertainty dominates) |
| A20 | Conclusions match evidence | PASS (H2 first evidence; universal open) |
| A21 | H1/H2/H3 + theorem OPEN | PASS |
| A22 | No new solver/replay/search | PASS (audit ran reads + arithmetic only) |
| A23 | Independent audit completed | PASS (10/10) |
| A24 | Delivery + HARD STOP | PASS (f753306 pushed; remote verified) |
