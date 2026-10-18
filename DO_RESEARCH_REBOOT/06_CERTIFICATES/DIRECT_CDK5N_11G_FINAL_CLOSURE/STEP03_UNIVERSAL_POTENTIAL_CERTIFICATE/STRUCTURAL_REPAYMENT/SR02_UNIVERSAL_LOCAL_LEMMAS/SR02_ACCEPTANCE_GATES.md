# SR02 Acceptance Gates

| Gate | Requirement | Verdict |
|---|---|---|
| SR02-01 | Entry HEAD + hashes | PASS |
| SR02-02 | SR-01 imported exactly | PASS |
| SR02-03 | Graph/four-rule freeze | PASS |
| SR02-04 | CPU allocation verified | PASS (~340s ≤ 576s) |
| SR02-05 | Totality + semantics | PASS (evidence + honest symbolic gap) |
| SR02-06 | Guard algebra proved | PASS (4 identities, verified) |
| SR02-07 | Rotation identities | PASS (per-rotation exact; macro-scope corrected) |
| SR02-08 | Marked-rank/count analyzed | PASS |
| SR02-09..12 | Low 4 guard lemmas | EVIDENCE (00/10/11) / OPEN (01) — not proved |
| SR02-13..16 | High 4 guard lemmas | OPEN (no data) |
| SR02-17 | Threshold audited | PARTIAL (empirical; derivation open) |
| SR02-18 | Boundary audited | PARTIAL (01 unsampled) |
| SR02-19 | Low weights covered | PARTIAL (sampled classes) |
| SR02-20 | High weights covered | OPEN |
| SR02-21 | w=-3 retained/classified | PASS (conditional) |
| SR02-22 | SAT counterexamples verified | VACUOUS (none found) |
| SR02-23 | No promotion | PASS |
| SR02-24 | Lemma graph produced | PASS |
| SR02-25 | No hidden restriction | PASS |
| SR02-26 | Independent verification | PASS (10/10) |
| SR02-27 | Caps respected | PASS |
| SR02-28 | Delivery + HARD STOP | PASS (ad3a982 pushed; remote verified) |
