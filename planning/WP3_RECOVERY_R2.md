# WP-3 RECOVERY R2 — versioned recovery after genuine human REJECT of R1 (not a weakening)

Binding: CURRENT_PHASE=WP-3, PREVIOUS_PHASE=WP-2 (LIQUIDITY_AXIS_FROZEN, revalidated).
Authority: WorkPlan.md WP-3 + spec §§4,7,8,10,11 + planning/WP3_CONTRACT.md + operator
REJECT verdict on R1 (human, never fabricated).

## R1 rejected identity (preserved history, never reused, never silently regenerated)

- generator R1: `h4l_generate.py` sha256
  `f5dd09ec3cb381e68e8c92c928e5a53a7f4092534e6d267dd93b4a4f3e81afd6`
- commitment R1: `4b33e033b9f8f23f9eb97e88080d49048d17cca797d2be56f4d896474620811b`
- R1 public files archived (bytes unchanged) at:
  `artifacts/v04/holdouts/rejected_R1/h4l_commitment_R1_REJECTED.json`
  `artifacts/v04/holdouts/rejected_R1/firewall_state_R1_REJECTED.json`
  (R1 firewall terminal: COMMITMENT_PUBLISHED; R1 lifecycle closed as REJECTED.)
- R1 secret bytes (seed + 7 shards) preserved outside the repo at
  `Temp/opencode/h4l-secret-R1-rejected` and are permanently retired: never reused,
  never revealed, never evaluated, never deleted as evidence.

## R1 defects (root causes, all in R1 implementation, none in the frozen contract)

- D-R1-01: `DRBG.randbelow` used modulo reduction (biased for n not dividing 2^256),
  violating the frozen exact-uniform {2..8} history law and uniform-draw requirements.
- D-R1-02: six strata ignored/changed sampled L (burst lengths, fixed-4 core,
  max(4,L), 4..6 drain, 5-capped nested, 2L mirror), violating len(H)==L in 2..8.
- D-R1-03: `seal_h4l.py` serialized generator/stratum order instead of the frozen
  sorted-episode-ID order; logical-stream hash covered the unsorted stream.
- D-R1-04: `h4l_verify.py` accepted 2..16, never recomputed episode IDs, never
  checked order/shard/logical-stream integrity.
- D-R1-05: HOLD suite accepted lengths through 16 and lacked forced-L coverage.

## R2 repairs (implementation -> contract; zero contract weakening)

- R-R2-01: rejection-sampled exact-uniform `randbelow` (deterministic SHA-256
  counter streams; bound = 2^256 - (2^256 mod n)).
- R-R2-02: every stratum returns exactly the once-sampled L in 2..8, motif preserved
  (burst split 1..L-1, core+periodic extension, direct alternation, (L-1)+drain,
  expanding nested offsets, half-mirror+optional center).
- R-R2-03: episode ID = sha256(canonical content JSON); shards serialize episodes
  sorted by ID; logical-stream hash covers the canonical ordered stream.
- R-R2-04: verifier enforces 2..8 + ID recompute + sorted order + shard order +
  per-shard SHA + logical-stream recompute + quotas/legality + commitment recompute.
- R-R2-05: HOLD suite extended (forced-L 12x7, RNG/modulo mutants, mini-bank
  verifier probes); old weaknesses removed.

## R2 bank identity and lifecycle authorization

- New bank identity `H4L-R2` (`"bank_id": "H4L-R2"`, `"supersedes": <R1 commitment>`).
- R2 reuses the canonical public paths
  `artifacts/v04/holdouts/{h4l_commitment.json, firewall_state.json}` because R1's
  files were archived to `rejected_R1/` first: this is a new versioned lifecycle
  (EMPTY -> ... -> COMMITMENT_PUBLISHED), NOT a backwards reset of R1's lifecycle.
- R2 uses a fresh 256-bit operator-secret seed in a fresh secret directory; the R1
  seed is never reused. Generator R2 bytes are committed BEFORE R2 generation
  (commit B1, pushed, HEAD verified). No H4L evaluation during repair.
- Downstream consumers (WP-4/WP-5/WP-6) observe only: R1 archived as rejected,
  canonical paths bound to H4L-R2, firewall COMMITMENT_PUBLISHED, zero evaluations,
  zero reveals. No frozen interface semantics are altered.

## Acceptance gate

- R2 closes REQ-008 only on a new genuine human ACCEPT of the R2 generator SHA-256
  and R2 commitment. The R1 REJECT must remain visible in Path.md forever.
