# 26AP audit: replay + blocks + recognizer + novelty + controls

## Witness-first replay (passed — no search run)

- `06_CERTIFICATES/26AP/26AP_vine16_candidate_replay.py` (authoritative
  engine); cert `26AP_vine16_witness_certificate.json`; log `26AP_execution_log.txt`.
- T0 = right vine 16, A0=B0, no aliasing (N1 ✓). Prefix 9 DELETEs: B stays
  exact vine; A_start matches expected serial (N2 ✓); prefix costs excluded.
- Cycle 29 ops: A/B closure PASS + REPETITION closure PASS (N3, §17 ✓);
  table 29/29 (N4 ✓); A=46, Q=27, W=−65.
- 29 accesses → 27 blocks: two a=0 no-ops (2nd D6, 2nd D16) grouped into
  preceding same-key blocks, asserted (N5 ✓). Positives exactly blocks 0,1,2.
- K11 (a=2,q=5,δ=+1): unit-positive need not have a=1 (N6 ✓). Run genuine ×3
  (N7 roots 1/11/9 from B-root traces, not hardcoded). Trajectory 2,2,4
  (bound 2p=6 ✓). Return K1 a=3=p, q=2, δ=−4 (N9/N10 ✓).
- Engines: 38/38 shapes+depths+costs (N16 downstream untouched).

## Recognizer + cut independence (N11)

- `26AP_maximal_run_recognizer.py`: amended cut (min-index nonpositive j,
  linearize j+1..j), O(m) scan, exact-once consumption (N12 ✓).
- Witness ACCEPT: run start 0 len 3 return 3 r=1, return a=3, packet −1 (N10 ✓).
- Cut audit: all 24 nonpositive cuts tested, same decision + same cyclic
  assignment (`26AP_recognizer_selftests.json`; prose record
  `06_CERTIFICATES/26AP/26AP_recognizer_cut_independence_audit.md`).
- Self-tests 6/6: empty-positive accept, synthetic p=1 accept, all-positive /
  no-return / non-unit / short-return rejects (N15: no all-p realizability
  claim; arbitrarily long only via p=3 repetition).

## Novelty (N13/N14 — all three blocks; actual 26AO rejection)

- 26AO banked recognizer (sha256 `4f4b40e0…`), run on source-certified blocks:
  REJECT, zero Type I and zero Type II candidates
  (`26AP_26AO_rejection_certificate.json`). Parity: accepted two-order walks
  carry 2k positives (banked recognizer lines 15/39/45/78 + proved 26AN-P/
  26AO-P slot signs); witness has 3 ⟹ formal exclusion.
- Per-block: K11 (r=1; succ 9/16/1) AJ✗ AK✗ AL-G/S✗ (26AL-S⊆G per banked proof),
  AM-G✗ (next +1), AM-S✗; K9 (r=11; succ 16/1/16) same pattern; K16 (r=9;
  succ 1/16/15) AJ/AK/AL✗, AM-G✗ (third succ 15≠9), AM-S✗. n=16, depths
  10/6/6, A=46 (bounded classes ✗). Full table in
  `06_CERTIFICATES/26AP/26AP_all_three_roots_novelty_audit.md`.
- ⟹ γ*∈C_26AP∖C_old; strict union extension. No C_old⊆C_26AP claim.
