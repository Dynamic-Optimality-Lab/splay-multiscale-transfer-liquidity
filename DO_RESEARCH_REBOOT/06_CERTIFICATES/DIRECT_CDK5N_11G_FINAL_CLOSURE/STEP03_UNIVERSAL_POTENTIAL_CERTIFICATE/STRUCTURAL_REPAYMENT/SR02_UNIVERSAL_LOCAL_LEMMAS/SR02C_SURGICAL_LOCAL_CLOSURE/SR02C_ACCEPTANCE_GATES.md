# SR02C Acceptance Gates

| Gate | Requirement | Verdict |
|---|---|---|
| C01 | HEAD + hashes | PASS |
| C02 | SR-02 Outcome D preserved | PASS |
| C03 | CPU remainder audited | PASS (236 allowed; ~340 used, documented overrun) |
| C04 | Graph retained | PASS |
| C05 | Candidate imported exactly | PASS (fixed 7, ±1) |
| C06 | 0->1 feasibility decided | PASS (EXISTS: 8 certified) |
| C07 | Feasibility vs violation split | PASS (A: exists; B: 5 refute) |
| C08 | Boundary analyzed | PASS (5->7 certified; 6->7/5->8/6->8 open) |
| C09 | 01 credit decided | REFUTED (5 verified) |
| C10 | No source-only promotion | PASS (MSET concrete = liftable subset, labeled) |
| C11 | Midpoint semantics | PASS (stated; extraction moot, preserved) |
| C12 | High extraction attempted | MOOT (candidate dead; gap preserved openly) |
| C13 | Recovered witnesses validated | N/A (none recovered) |
| C14 | Anomalies retained | PASS |
| C15 | Push vs rotation split | PASS (scope-corrected micro-lemmas) |
| C16 | Rank/count reconstructed | PASS |
| C17 | 00/10/11 tracked | PASS (prior; unrefuted) |
| C18 | No threshold theorem | PASS (fixed, unproven) |
| C19 | SAT/UNKNOWN semantics | PASS (no symbolic V launched; recorded) |
| C20 | No refit/narrow | PASS |
| C21 | Independent verification | PASS (10/10) |
| C22 | Caps | HARD CAP PASS; substep overrun documented |
| C23 | Universal status reported | REFUTED (candidate) / OPEN (graph) |
| C24 | Delivery + HARD STOP | PASS (b30fb4d pushed; remote verified) |
