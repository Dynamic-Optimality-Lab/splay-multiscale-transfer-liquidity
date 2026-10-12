# Exceptional interval migration traces (P5; probe tmp_omega.py + replay certs)

## Control A E3 (KEEP 5, idx19; interval j=12, H=1,c=1,q=3)

v=5 eliminated 5 positive incidences ((5,1),(5,2),(5,3),(5,4),(5,6):
1→0) + 1 negative ((5,8): −1→0); gap 4→0. 19 coordinates changed total.
Created: key1 −1→+1 (Δ+2, crosses zero: (1,z) incidences gained), key3
0→+1, key7 0→+2. Redistribution, not repayment: +5 positive units appear
elsewhere as +4+1 disappear. A-rotations: 1 (ZIG, depth 2→0); B-rotations:
6 (depth 6→0). Packets: 1 A-paid + 6 B-driven rotation records.

## Control B event (KEEP 1, idx16; a=0,q=2, non-exceptional)

v=1 eliminated 4 positive incidences at ZERO A-cost; 14 coords changed;
Γ 4→5 (net +1!). Receivers: keys 3,5,7,9 gain. All 14 changes are B-driven
packets (B depth 4→0: 4 rotations; A: none). Certified unpaid migration.

## Control C E3 (KEEP 9, idx7; interval j=1, H=1,c=1,q=3)

v=9 eliminated 5 positive incidences (gap 5→0); 16 coords changed; D_rot
8→9 (increased!). A-rotations: 1; B-rotations: 6. Receivers: keys 1,7
(+1,+1 net... key7 gap 4→3 retains T_4 membership — persistent token NOT
consumed: reuse hazard documented).

## SELR OUT E3s (regression; intervals j=4,12)

Same L0 shape (depths verified in replay certs); traces available in
MIG_replay JSONs. Both satisfy per-key elimination; net Γ drops 2 each
(5→3) — unlike Control A's net 0. Heterogeneity confirmed: E3 net effect
∈ {0(signed... observed Γ drops 0..3 across corpus) — no universal
per-interval net law at Γ level; Ω level shows universal per-key
elimination (≥4 v-incidences) with variable redistribution.

## P5 verdict

Migration TRACED on all controls (L0 + Ω-books + packet provenance).
Redistribution vs repayment DISTINGUISHED (all three cases show
redistribution; none shows certified repayment). P5 structural tracing:
COMPLETE. Compensation bridge: NOT ESTABLISHED (see MIG-C1 record).
