# 26AO audit: replay + recognizer + packet + novelty + controls

## Witness-first replay (passed — no search run)

- Script `06_CERTIFICATES/26AO/26AO_ten_key_replay.py` (authoritative
  `wp6_eventflow`); cert `26AO_ten_key_witness_certificate.json`; log
  `26AO_execution_log.txt`.
- T0 `(2(1..)(3.(6(4.(5..))(9(8(7..).)(10..)))))` exact, BST-validated, 10 keys
  (N1 ✓). Prefix K10,D6,D8,D9,D5,D9,K1,D7,D5 from A0=B0 (N2 ✓) reaches the
  expected A/B pair states exactly (serial-compared).
- Cycle (18 ops): A/B closure PASS (N3 ✓); table 18/18 (N4 ✓); A=34, Q_B=19,
  W=−49; all a≥1 (18 blocks); rotation counts recorded per access.
- Independent engine: 9/9 prefix + 18/18 cycle = 27/27 (depths, costs, shapes).

## Packet (anchors [0], Type II)

- Positives exactly blocks 1,2 (K7: 1,7,1,3,+1; K5: 1,6,1,3,+1) (N10 ✓).
- r=1 (B-root before K7, N6 ✓; r' =7 before K5 recorded separately, not the
  repayment target); trajectory depth(1) = 1,1,2 after K7/K5/K9 (≤6 bound ✓).
- K5,K9 genuine B-changes (N5 ✓); K9 dB=3 ⟹ δ=−1 derived (N8 ✓); K1 (a=2,
  dB=2, q=1) δ=−3 ≤−1 derived (N8 ✓). Packet (+1,+1,−1,−3)=−2; tail blocks
  5–18 all ≤0 (incl. block 7 δ=0); cycle −49. No total-sign shortcut (N9 ✓).

## Recognizer (mandatory §16)

- `26AO_two_order_recognizer.py`: match_type1 = 26AN-P verbatim; match_type2 =
  AO-P1–P7; DP-per-cut, O(m²), deterministic (cuts ascending, fixed option
  order), emits cut/anchors/types/singletons; no deficit-total acceptance.
- Self-tests 5/5 (`26AO_recognizer_audit.json`): witness→Type II@[0] (T1);
  synthetic Type I accepted (T2); wrong-r and all-positive rejected (T3,T4);
  m<4 edge cases correct (T5). C_26AN⊆C_two-order by construction+DP
  completeness (proved in 02_PROVED doc, not asserted).

## Novelty (N7, both positives; N11 two-order only)

- Machine-checked: Type I matches nowhere on the witness (⟹ ∉C_26AN); sole
  Type II match at 0. K7 vs AJ/AK/AL-G/AL-S/AM-G/AM-S/26AN-I: all fail on
  successor keys / δ(i+1)=+1. K5 (r'=7) vs same: succ 9,1,2; AM-G G4 (2≠7);
  Type I anchor fails (slot-2 K2 δ=−3). n=10, depths 7/6, A=34.
- ⟹ C_26AN⊂neqC_two-order; C_old⊂neqC_old∪C_two-order. No order-independence
  claim (N11 ✓). Downstream unchanged (N12 ✓). 26AM Outcome B preserved.
