# 26AP all-three-roots novelty audit (authoritative B-root traces)

Cycle block keys: K11,K9,K16,K1,K16,K15,K14,K13,K12,K11,K10,K9,K8,K7,K6,K5,
K4,K3,K2,K1,D9,D8,D6,D11,D9,D16,D5 (27 blocks; D6/D16 no-ops grouped).

| Block | Key | δ | Former B-root (rb trace) | Next 3 block keys |
|---|---|---|---|---|
| 0 | K11 | +1 | 1 | K9,K16,K1 |
| 1 | K9 | +1 | 11 | K16,K1,K16 |
| 2 | K16 | +1 | 9 | K1,K16,K15 |

## 26AJ (successor must access r): K9≠1; K16≠11; K1≠9 — all FAIL.
## 26AK/26AL-G (2nd successor must be r): K16≠1; K1≠11; K16≠9 — all FAIL.
(26AL-S⊆26AL-G by banked containment proof — no separate check needed.)
## 26AM-G: K11 next δ=+1 (G3 FAIL); K9 next δ=+1 (G3 FAIL); K16 third
successor K15≠9 (G4 FAIL). 26AM-S (needs δ=0 intermediates): all FAIL
(+1/+1/−4,−1 intermediates).
## 26AN/26AO two-order: banked recognizer REJECT, 0 Type I + 0 Type II
candidates anywhere; parity (2k) confirms odd-3 exclusion.
## Bounded: n=16; positive B-depths 10,6,6; A=46 — zero-A/n≤6/depth≤5 FAIL.
