# MRP AM-G/S local-vs-global audit (K5-local compatibility affirmed twice)

All three positives have r=9, h=2 (measured post-splay depths), c=3.

## K3a packet (2,3,4,5 = K3,K7,D5,K1)

G1 PASS. G2: K7 genuine ✓, D5 DELETE (genuine=False) — **FAIL**. G3 (−4,−4)
moot. **G4 FAIL** (K1≠9). S fails (DELETE intervener). → Uncovered.

## K5a packet (9,10,11,12 = K5,K7,K1,K9)

G1–G4 PASS (genuine, keys≠9, intermediates (0,0), KEEP 9). G5: a=2 ⇒ 4≥3 PASS.
G6: 1≤0+0+1 PASS. → Locally AM-G-payable. AM-S: intermediates (0,0) exact,
return a=2 — locally AM-S-payable too. Both AFFIRMED.

## K5b packet (22,23,24,25 = K5,K7,K1,K9)

Identical local structure (measured costs equal): G1–G6 PASS, S PASS locally.
AFFIRMED.

## Global verdict

26AM-G/S need every positive covered. K3a uncovered ⇒ walk ∉ C_26AM-G/S.
Local K5 compatibilities ≠ global coverage. The G0-C error (denying genuineness)
is not repeated; K5-local compatibility is affirmed, not hidden.
