# GATE B: historical control substitution — exact record (append-only)

Committed `9396c19` artifacts used (from `MR_G0_authoritative_replay.py` +
`MR_G0_fixture_manifest.json` + replay log):

| Historical label | Executed word (SHA prefix) | Length |
|---|---|---|
| CTL-A | single-S2 `753bb211…` | 18 |
| CTL-B | single-S1 `ff156d94…` | 17 |
| CTL-C | doubled-S2 `3f64f758…` | 36 (SHA-checked only in manifest; replay loop covered INC/CTL-A/CTL-B paths — CTL-C doubled-S2 full replay absent) |

Original charter required:

| Role | Required word | SHA prefix | Length |
|---|---|---|---|
| ORIG_CTL_A_SINGLE_VR | VR 18-access | `b4165259…` | 18 |
| ORIG_CTL_B_DOUBLE_VR | VR×2 | `90eec8ce…` | 36 |
| ORIG_CTL_C_DOUBLE_S2 | S2×2 | `3f64f758…` | 36 |

Findings: original CTL-A never executed (single-S2 substituted); original CTL-B
never executed (single-S1 substituted; doubled-VR anti-novelty control omitted);
original CTL-C SHA-pinned but not fully replayed/classified. These are evidence
defects, not mathematical refutations — the INC witness and MR-L1–L9 mechanism
are unaffected. Nomenclature: ORIG_* (corrective) vs HIST_* (supplementary).
No historical file modified; this record lives in the new erratum directory.
