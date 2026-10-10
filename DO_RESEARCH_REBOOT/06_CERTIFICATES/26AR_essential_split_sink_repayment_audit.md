# 26AR audit: replay + split packet + recognizer + novelty + controls

## Witness-first replay (passed — no search run)

- `06_CERTIFICATES/26AR/26AR_vine16_essential_split_sink_replay.py`; cert
  `26AR_vine16_closed_witness.json`; log `26AR_execution_log.txt`.
- Vine-16 diagonal start, independent A/B (N1/N2 ✓). 16-access mixed prefix
  (KEEPs change B — no vine assumption, N4 ✓); A_start/B_start exact (N3 ✓);
  prefix excluded (N5 threading ✓).
- 37-cycle: sweep restores both vines at #21 (N7 ✓); A/B closure PASS (N6 ✓);
  table 37/37 (N9 ✓); A=70, Q=39, W=−101 (N8: 53 transitions ✓).
- 37 accesses, all a≥1 → 37 blocks, no grouping (N10 ✓). Positives exactly
  0,1,2 (+1 ×3) (N11 ✓). r=16/s=4 source-derived (N12 ✓); keeps of blocks 1,2
  avoid 16 (N13 ✓). q_r≤3 via displacement (N14 ✓); q_s≤2 via last-root fact
  (N15 ✓, traj 2→4). dA 4/3 independently verified (N16 ✓); no aggregate
  premise (N17 ✓). Essentiality 1,1→−1 (N18/N19 ✓). 14-key control recorded
  nonessential (N20 ✓). Engines 53/53; downstream OPEN (N26 ✓).

## Split packet

(+1,+1,+1,−2,−2)=−1; p=3, u=v=2; a_r=a_s=2<3 (AR-P8 ✓); q_r=q_s=2.

## Recognizer (15/15, `26AR_recognizer_selftests.json`)

- Witness ACCEPT Split {[0,1,2],3,4} + essential ✓. 26AP/26AQ banked witnesses
  preserved (Direct p=3 / Bridge) ✓. Rotations incl. boundary crossing ✓.
  Wrong-r/s, r==s, threshold-fails ×2, old-deep-sink no-S, overlap-caught,
  uncovered/all-positive, 14-key-imessential ✓. Soundness/completeness note:
  `26AR_recognizer_soundness_completeness.md`. No total-sign shortcut (N24 ✓);
  exact-once consumption (N23 ✓); finite≠universal (N25 ✓).

## Novelty (N21/N22 + §22)

- Accurate: K7→4 one-intervening triple locally 26AL-G-compatible (K16
  genuine, δ=−2, capacity 1≤4) — but K11 (i+2 key 7≠16) and K4 (i+2 key
  16≠11) uncoverable ⟹ no GLOBAL 26AL-G cover. K11→16 two-intervening return
  exists — intermediates (+1,+1) violate 26AM-G G3; K16 triple fails G4
  (K15≠10). AJ (succ), AK (2nd succ) fail all three.
- Machine: 26AO REJECT (0/0 candidates + parity), 26AP REJECT (bad-return),
  26AQ REJECT; ARmix ACCEPT. Full table:
  `06_CERTIFICATES/26AR/26AR_complete_AJ_to_AQ_domain_audit.md`.
- ⟹ γ*∈C_ARmix∖C_old; C_AQmix⊂neqC_ARmix; union enlarged.
