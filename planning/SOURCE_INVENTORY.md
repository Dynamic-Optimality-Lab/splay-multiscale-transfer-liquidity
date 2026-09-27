# SOURCE_INVENTORY — study-first record (Rule 0)

## Normative
1. `IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt` — supplied LIQ-v0.4 spec, 53398 bytes, SHA-256 `0E2C166E1B721DFC8A7E5327ED33AF29A1B4AC539CB71849F3C7231B32A8055B`. Read in full (prompt-supplied text + local byte copy). Status: NORMATIVE, controlling.
2. Architecture parent live repo `Dynamic-Optimality-Lab/splay-multiscale-transfer` — HEAD `895889169772087e391e84c33228648c84684e1e` (matches spec navigation HEAD; verified via GitHub API 2026-09-27). Studied: file tree, `WorkPlan.md` (7 WPs + §8 matrices), `TRANSFER_CALCULUS_LEDGER.md` (MSTC-0001/0002/0003, T7/T5/T6, TRANSFER_CALCULUS_FROZEN), `THEOREM_STATUS_REPORT.md` (9/5/3/3/6). Status: NORMATIVE-PARENT (read-only ancestor). Full seal pin (seal/manifest/archive/Path/WorkPlan/ledger/status/candidate-set hashes) is a WP-0 execution obligation.
3. Obstruction parent live repo `Dynamic-Optimality-Lab/Universal-Pair-Access-Closure-and-Dynamic-Optimality-Decision-Program-` — latest `19ef254dfc48c7b909c646f959e2d7364865b777` (2026-09-27, n=28 witness + triple replay per commit message). Studied: `WorkPlan.md` v1.7 excerpt, `Path.md` excerpts. Status: NORMATIVE-PARENT evidence. Exact sealed commit pin is `TO_BE_PINNED_FULL_SHA_BEFORE_FOUNDATION_FROZEN` per LIQ spec — WP-0 execution obligation.
4. Parent reference copies (local, read-only): `parent_IMPLEMENTATION_SPEC_v0.3.reference.md` (SHA `462676E1…D1E12F`, 120420 bytes, 4601 lines, header studied), `parent_IMPLEMENTATION_SPEC_DECIDE-v0.4.reference.md` (SHA `30ACC6F9…5F9`, 85888 bytes, header studied). Status: REFERENCE (exact-source embodiments of parent specs).

## Non-normative / evidence-only / excluded
- `Downloads/WorkPlan.md`, `Downloads/WorkPlan (1).md`, `Downloads/Path.md`, `Downloads/Path (1).md`, `Downloads/Path (2).md` — MAVS Chapter 10B robustness program (1094-line WorkPlan inspected, §§0–... on corruption families). Unrelated to SPLAY. Status: NON-NORMATIVE, excluded.
- All other Downloads binaries/docs (images, videos, installers, CVs, unrelated specs). Status: NON-NORMATIVE, excluded.

## Missing (blocked, never invented)
- MISSING-01: exact architecture-parent scientific seal bundle (final seal, manifest, archive bytes, candidate-set commitment hash, normative-spec hash set) at the pinned commit. Blocks: WP-0 `FOUNDATION_FROZEN`. Action: WP-0 execution clones by full SHA and hash-verifies; until then planning records navigation HEAD only.
- MISSING-02: exact obstruction-parent sealed/refutation-closure commit (`TO_BE_PINNED_FULL_SHA_BEFORE_FOUNDATION_FROZEN`) + independent-replay bundle bytes. Blocks: WP-0 obstruction pin + WP-1 n=28 reproduction input. Action: WP-0 execution pins `19ef254…` (or newer sealed head) by full SHA after content verification; planning proposes but does not claim.
- No SPEC_CONFLICT found: LIQ-v0.4 sections are internally consistent at planning-read; v0.3/DECIDE lineage headers corroborate (MSTC-0002 identity, H3T verdicts, blocker DAG). No PREREG_INTERFACE_UNDERSPECIFIED beyond the two pins above.

## Hashes recomputed locally (PowerShell Get-FileHash, SHA-256)
- LIQ spec: `0E2C166E…055B` (matches planning record).
- v0.3 ref: `462676E1…D1E12F`. DECIDE ref: `30ACC6F9…5F9`.
