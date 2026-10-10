# 26AO strict-novelty certificate (machine-checked + analytic)

Walk: 10-key witness, blocks 1..18, keys
[7,5,9,1,2,8,4,9,6,3,10,1,2,4,9,1,7,5], deltas
[+1,+1,−1,−3,−3,−4,0,−1,−4,−3,−3,−3,−2,−6,−4,−4,−6,−4].

## C_26AN exclusion (decisive)

`match_type1` (exact 26AN-P) tested at all 18 cyclic positions: ZERO matches
(recognizer audit). Since C_26AN requires every positive block inside a Type I
packet and blocks 1,2 admit none, γ*∉C_26AN. Q.E.D. (computational).

## Per-domain exclusions (from authoritative trace)

| Domain | K7 (r=1) fails because | K5 (r'=7) fails because |
|---|---|---|
| 26AJ | succ key 5≠1 | succ key 9≠7 |
| 26AK | i+2 key 9≠1 | i+2 key 1≠7 |
| 26AL-G/S | i+2 key 9≠1 | i+2 key 1≠7 |
| 26AM-G | δ(i+1)=+1 (G3) | i+3 key 2≠7 (G4) |
| 26AM-S | intermediates not 0 | intermediates not 0 |
| 26AN-I | slot-1 δ=+1 | slot-2 K2 δ=−3 ≠+1 |
| zero-A | A=34 | same walk |
| n≤6 | n=10 | same walk |
| depth≤5 | dB=7 | dB=6 |

K7 anchoring any 26AN packet needs slot-1 ≤−1 (K5 is +1) — impossible; K5 is
in no other positive's packet ({K7..} violates G3/I-slot-1 alike).

## Conclusions

γ*∈C_two-order (Type II @0) ∖ C_old. C_26AN⊂neqC_two-order.
C_old⊂neqC_old∪C_two-order. No C_old⊆C_26AO claim; two orderings only.
