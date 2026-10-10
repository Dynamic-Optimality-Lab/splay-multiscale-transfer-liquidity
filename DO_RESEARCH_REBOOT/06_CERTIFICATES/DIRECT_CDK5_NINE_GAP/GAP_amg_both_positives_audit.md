# GAP 26AM-G audits — BOTH positives fail exactly as specified

Banked G1–G7 (26AM_two_splay_signed_repayment.md). Blocks 0–16, m=17.

## K3 packet (blocks 2,3,4,5 = K3,K7,K1,D4), r=9, h=2, c=3

- G1 δ=+1>0: PASS. G2 K7,K1 genuine, keys 7,1≠9: PASS (genuineness affirmed,
  never called false). G3 δ=−4,−2≤0: PASS.
- **G4 FAIL:** fourth leader is D4 (key 4), not KEEP(9). The return key is
  absent at the required position. No regrouping possible (packets are
  consecutive by definition; anchor fixed at the positive block).
- G5/G6 moot after G4 (recorded: 2a(D4)=2<3, capacity 1≤5 would otherwise hold).

## K5 packet (blocks 8,9,10,11 = K5,K7,K1,K9), r=9, h=2, c=3

- G1 PASS (+1). G2 PASS (genuine, keys≠9). G3 PASS (−2,−2). G4 PASS (K9, KEEP(9)).
- **G5 FAIL:** a(K9)=1 ⇒ 2a=2<3=c. Repayment capacity independently
  insufficient; K9's return is not sufficient (not inferred — measured dA=3).
- G6 would read 1≤3 but is gated by G5's structural capacity premise.

## Global exclusion

26AM-G needs a valid packet per positive. K3 fails G4, K5 fails G5 — two
independent obstructions. No alternative covering decomposition exists (only
K3/K5 can anchor; forced consecutive positions). 26AM-S fails a fortiori
(intermediates −4,−2,−2,−2 ≠ 0). Walk ∉ C_26AM-G. The G0-C mistake (calling G2
false / ignoring capacity) is not repeated.
