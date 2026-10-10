# GAP two-positive audit + Type K/P eligibility (PROVED for this witness)

Word (17): D5,D4,K3,K7,K1,D4,K9,D6,K5,K7,K1,K9,D8,D2,D1,D6,D9. All 17 accesses
have a≥1 ⇒ 17 A-root blocks, no followers (verified from trace).

## Debt-event census (complete)

KEEP order K3,K7,K1,K9,K5,K7,K1,K9 (all consecutive differ ⇒ c=1 throughout).
q: K3=3, K5=3, all others 2. Hence w=q−2c: K3 w=1, K5 w=1, rest w=0. Exactly
two positive B-only debt events; no other KEEP needs payment.

## K3 (idx 2): Type P

dA=2/a=1, dB=6/q=3, δ=+1, genuine (B changes), former root r=9, h=2. Preceding
occurrence D4 (idx 1): DELETE, key 4≠3, a=1≥1; a(K3)=1≥1. Two distinct accesses
in I_{K3} ⇒ H≥2. Type P SATISFIED (Type K correctly absent: dA=2<3).

## K5 (idx 8): Type P

dA=2/a=1, dB=6/q=3, δ=+1, genuine, r=9, h=2. Preceding D6 (idx 7): DELETE, key
6≠5, a=2≥1; a(K5)=1≥1 ⇒ H≥2. Type P SATISFIED (Type K absent: dA=2<3).

## Coverage

Both debt events covered; non-debt KEEPs need nothing. Frozen predicate holds
for every positive event not merely the selected two (there are only two).
Nonshadow: A≠B serials after all 8 KEEPs (recorded per access).
