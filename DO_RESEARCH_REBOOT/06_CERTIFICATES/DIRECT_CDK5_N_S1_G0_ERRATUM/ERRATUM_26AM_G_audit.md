# 26AM-G audit — both positives (CORRECTED: K5 locally passes; global fails via K3)

Blocks 0–16 (17 single-access blocks, m=17). Sole positives: K3 (blk 2,
δ=+1, r=9, h=2, c=3), K5 (blk 8, δ=+1, r=9, h=2, c=3). h measured from trace.

## K3 packet (2,3,4,5 = K3,K7,D5,K1)

G1 PASS. G2: K7 genuine ✓ but D5 is DELETE (genuine=False) — **FAIL** (stated
from B-state changes, not key spelling). G3 (−4,?) moot. **G4 FAIL**: fourth
leader K1≠9. → K3 has NO valid packet (anchor fixed; consecutive mandatory).

## K5 packet (8,9,10,11 = K5,K7,K1,K9)

G1 PASS. G2 PASS (both genuine, keys 7,1≠9). G3 PASS (−2,−2). G4 PASS (KEEP 9).
G5: a(K9)=2 (dA=3 authoritative) ⇒ 2a=4≥3=c — **PASS (charter §8 predicted FAIL
with a=1; corrected here)**. G6: 1≤2+2+1=5 PASS. → K5 is locally AM-G-payable.

## Global verdict

26AM-G needs every positive covered. K3 uncovered ⇒ walk ∉ C_26AM-G. 26AM-S
fails (intermediates −4,−2,−2,−2≠0; containment noted, not assumed). The G0-C
error (calling G2 false) is not repeated; the §8 G5 prediction error is
corrected openly — and the global conclusion is unchanged (exclusion now rests
on K3's double obstruction G2+G4).
