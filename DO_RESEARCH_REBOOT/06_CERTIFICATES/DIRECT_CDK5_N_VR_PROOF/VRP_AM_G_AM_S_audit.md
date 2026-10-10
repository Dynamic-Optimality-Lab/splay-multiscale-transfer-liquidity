# VRP AM-G/S local-vs-global audit (K5 locally compatible; global fails on K3)

Positives: K3 (acc idx2/blk2: a=1,q=3,δ=+1,r=9,h=2,c=3), K5 (acc idx9/blk9:
a=1,q=3,δ=+1,r=9,h=2,c=3). h measured from trace (depth(9) after each = 2).

## K3 packet (blks 2,3,4,5 = K3,K7,D5,K1)

G1 PASS. G2: K7 genuine ✓, D5 DELETE (genuine=False) — **FAIL**. G3 (−4,−4)
moot. **G4 FAIL** (K1≠9). S: DELETE intervener + nonzero intermediates — FAIL.
→ No valid packet (anchor fixed; consecutive forced).

## K5 packet (blks 9,10,11,12 = K5,K7,K1,K9)

G1 PASS. G2 PASS (genuine, keys 7,1≠9). G3 PASS (0,0): K7 (a=1,q=2,δ=0),
K1 (a=1,q=2,δ=0). G4 PASS (KEEP 9). G5: a(K9)=2 ⇒ 2a=4≥3 — **PASS**. G6:
1 ≤ 0+0+1 = 1 — **PASS (tight)**. → Locally AM-G-payable.
AM-S: intermediates (0,0) with δ=0⟺q=2a exact ✓, return a=2≥2 ✓ — **locally
AM-S-payable too**. Both local compatibilities AFFIRMED (correcting any
contrary claim).

## Global verdict

26AM-G/S need every positive covered. K3 uncovered ⇒ walk ∉ C_26AM-G/S.
Local K5 compatibility ≠ global coverage. The G0-C error (denying genuineness)
is not repeated; K5-local compatibility is affirmed, not hidden.
