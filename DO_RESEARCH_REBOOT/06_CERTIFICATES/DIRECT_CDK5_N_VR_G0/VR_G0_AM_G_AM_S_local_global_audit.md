# AM-G/S local-vs-global audit — INC (honest both directions)

Positives: K3 (blk2, a=1,q=3,δ=+1,r=9,h=2,c=3), K5 (blk9, a=1,q=3,δ=+1,r=9,h=2,c=3).

## K3 packet (2,3,4,5 = K3,K7,D5,K1)

G1 PASS. G2: K7 genuine ✓ but D5 DELETE (genuine=False) — **FAIL**. G3 (−4,−4)
moot. **G4 FAIL** (K1≠9). → No valid packet (anchor fixed, consecutive forced).
AM-S fails (DELETE intervener).

## K5 packet (9,10,11,12 = K5,K7,K1,K9)

G1 PASS. G2 PASS (both genuine, keys 7,1≠9). G3 PASS (0,−2 — K7 δ=0, K1 δ=−2).
G4 PASS (KEEP 9). G5: a(K9 idx12)=2 ⇒ 2a=4≥3=c — **PASS**. G6: 1≤0+0+1=1 — PASS.
→ K5 locally AM-G-payable. AM-S: intermediates (0,−2)≠(0,0) — **FAIL** (K1 −2).

## Global verdict

26AM-G needs every positive covered. K3 uncovered ⇒ walk ∉ C_26AM-G. K5's local
compatibility affirmed (never denied); local≠global. No alternative decomposition
(only K3/K5 anchor; forced positions). S-containment banked, checked separately.
