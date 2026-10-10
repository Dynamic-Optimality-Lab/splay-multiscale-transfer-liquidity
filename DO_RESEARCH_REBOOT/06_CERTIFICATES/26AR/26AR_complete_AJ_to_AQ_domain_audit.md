# 26AR complete AJ→AQ domain audit (authoritative traces)

Blocks (37): K11,K4,K7,K16,K4,K16,K15,K14,K13,K12,K11,K10,K9,K8,K7,K6,K5,K4,
K3,K2,K1,K3,K6,K15,K9,K1,K14,K13,K16,D3,D11,D4,D13,D3,D15,D4,D7.
Positives: 0 (K11,+1,r=16), 1 (K4,+1,r=11), 2 (K7,+1,r=4).

| Domain | K11 (next K4,K7,K16) | K4 (next K7,K16,K4) | K7 (next K16,K4,K16) |
|---|---|---|---|
| 26AJ | K4≠16 ✗ | K7≠11 ✗ | K16≠4 ✗ |
| 26AK/AL-G/S | K7≠16 ✗ | K16≠11 ✗ | triple locally compatible* |
| 26AM-G | next +1 (G3) ✗ | next +1 (G3) ✗ | G4: K15≠10 ✗ (G3 vacuous pass noted) |
| 26AM-S | intermed +1 ✗ | intermed +1 ✗ | intermed −2,−1 ✗ |
| 26AN/AO | 0 candidates walk-wide; parity ✗ | — | — |
| 26AP | succ K16 key=16=r BUT a=2<3 ✗ | (in run) | (in run) |
| 26AQ | consecutive positives, no bridge ✗ | — | — |
| base | n=16, dB=6, A=70 ✗ | dB=6 ✗ | dB=6 ✗ |

*K7 honesty note (N21): (K7,K16,K4) meets local 26AL-G triple arithmetic
(K16 genuine, δ=−2≤0, capacity 1≤(4−2)+(4−2)=4) — but 26AL-G GLOBAL cover
needs K11 (2nd succ K7≠16 ✗) and K4 (2nd succ K16≠11 ✗) too. No GLOBAL old
certificate exists. K11's two-intervening return (K16) is real but its
intermediates (+1,+1) violate 26AM-G G3 — reported, not hidden.

Machine: 26AO REJECT (sha 4f4b40e0, 0/0 candidates); 26AP REJECT (sha
9abefb16, bad-return); 26AQ REJECT (sha 9dc40634); ARmix ACCEPT (Split).
