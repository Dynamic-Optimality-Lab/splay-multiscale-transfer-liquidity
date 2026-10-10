# 26AQ prior-domain exclusion audit (authoritative traces)

Blocks (28): K11,K9,K10,K16,K1,K16,K15,K14,K13,K12,K11,K10,K9,K8,K7,K6,K5,K4,
K3,K2,K1,D9,D8,D6,D11,D9,D16,D5. Positives: idx 0 (K11,+1,r=1), 1 (K9,+1,r=11),
3 (K16,+1,r=10).

| Domain | K11 (r=1; next K9,K10,K16) | K9 (r=11; next K10,K16,K1) | K16 (r=10; next K1,K16,K15) |
|---|---|---|---|
| 26AJ | K9≠1 ✗ | K10≠11 ✗ | K1≠10 ✗ |
| 26AK/26AL-G/S | K10≠1 ✗ | K16≠11 ✗ | K16≠10 ✗ |
| 26AM-G | next +1 (G3) ✗ | next +1 (G3) ✗ | 3rd succ K15≠10 (G4) ✗ |
| 26AM-S | intermed not 0 ✗ | intermed not 0 ✗ | intermed not 0 ✗ |
| 26AN/26AO | 0 Type I/II candidates walk-wide; parity 2k vs 3 ✗ | — | — |
| 26AP | run [K11,K9] succ K10≠1 ✗ | (in run 1) | run [K16] succ K1≠10 ✗ |
| zero-A/n≤6/depth≤5 | A=50, n=16, dB=10 ✗ | dB=6 ✗ | dB=6 ✗ |

Machine: 26AO REJECT (`26AQ_26AO_rejection_certificate.json`), 26AP REJECT
(`26AQ_26AP_rejection_certificate.json`); mixed 26AQ ACCEPT (bridge piece).
