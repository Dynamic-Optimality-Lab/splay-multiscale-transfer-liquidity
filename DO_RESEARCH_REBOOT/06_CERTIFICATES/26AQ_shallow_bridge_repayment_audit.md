# 26AQ audit: replay + bridge packet + mixed recognizer + novelty + controls

## Witness-first replay (passed — no search run)

- `06_CERTIFICATES/26AQ/26AQ_vine16_bridge_replay.py`; cert
  `26AQ_vine16_witness_certificate.json`; log `26AQ_execution_log.txt`.
- Vine-16 diagonal start, no aliasing (N1 ✓). 9-DELETE prefix: B exact vine,
  A_start exact (N2 ✓); prefix excluded from totals (N4 threading ✓).
- 30-access cycle: A/B closure PASS (N3 ✓); table 30/30; A=50, Q=23, W=−77.
- 30 accesses → 28 blocks (2nd D6/D16 no-ops grouped, asserted) (N5 ✓).
- Positives exactly blocks 0,1,3 (1-based 1,2,4) ✓. Bridge K10: dB=2 exact,
  genuine B-change (N6 ✓), z=10≠r=1. Roots 1/11/10 from rb traces (N7 ✓).
  Interveners {9,10,16} all ≠1 (N8 ✓; AQ-P4). Trajectory 2,2,3,5 vs bound
  2(p+1)=8 (N9: surcharge +1 allowed AND bridge −1 derived separately ✓).
  Return a=4≥3 tested, not asserted (N10 ✓). Tail nonpositive ✓.
- Engines 39/39 (N18 downstream OPEN preserved).

## Bridge packet

(+1,+1,−1,+1,−6)=−4; p1=2, p2=1, p=3≥3 ✓; return δ=−6 ≤1−p=−2 ✓ (stronger).

## Mixed recognizer (N13/N14/N15)

- `26AQ_mixed_cyclic_dp_recognizer.py`: all-cuts × DP (singleton/Direct/
  Bridge), independent `verify_cert` re-validation (disjointness, signs,
  coverage). No total-sign shortcut (N15 ✓).
- Witness ACCEPT with single AQ-bridge piece {[0,1],2,[3],4,r=1}; no Direct
  pieces; singles = rest. 26AP banked witness re-run: ACCEPT Direct p=3
  (preservation §14 ✓). Self-tests: direct-p1 accept, bridge-1+2 accept,
  bridge-p2 reject, all-positive reject (N17: one bridge only ✓).
- Complexity O(m³) packet tests, documented.

## Novelty (N11/N12 + §22)

- 26AO banked (sha256 `4f4b40e0…`): REJECT, 0/0 candidates; parity 2k vs 3
  positives (N12 ✓). 26AP banked (sha256 `9abefb16…`): REJECT — run1 succ
  K10≠1, run2 (r'=10) succ K1≠10 (N11 ✓).
- AJ/AK/AL-G/S per block (successor keys 9,10,16 / 10,16,1 / 1,16,15 vs roots
  1/11/10); AM-G (K11/K9 next-+1; K16 third-succ K15≠10); AM-S; bounded
  (n=16, depths 10/6/6, A=50). Full table:
  `06_CERTIFICATES/26AQ/26AQ_prior_domain_exclusion_audit.md`.
- ⟹ γ*∈C_AQmix∖C_old; C_26AP⊂neqC_AQmix; union strictly enlarged (N16: finite
  replay ≠ universal proof — universal proof in 02_PROVED doc).
