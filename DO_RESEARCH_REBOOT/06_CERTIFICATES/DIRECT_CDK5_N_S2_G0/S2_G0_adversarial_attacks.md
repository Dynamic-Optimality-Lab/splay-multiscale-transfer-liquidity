# Adversarial attacks §10 — all discharged (18/18)

1. Seam DELETE loss: wraparound interval in IV sums (K3 H=13 incl. tail); ΣH=A ✓. FAILS (attack).
2. a=0 no-op with q>0: 18 blocks = 18 accesses, all a≥1. FAILS.
3. Same-key miscount: consecutive KEEPs all differ (C_K=8 verified vs KEEP list). FAILS.
4. w=2 outside triple: only debts are K3,K5 (w=1 each); rest w≤0. FAILS.
5. Successor q=2 no reserve: H=1,R=0,w=0 — needs nothing; pair inequality holds. FAILS.
6. Second successor q=3 worst: covered (w≤1,R≥2 ⇒ 1+1≤0+2); witness has q=2. FAILS.
7. Second successor needing K/P: paid jointly, never separately — by partition. FAILS.
8. K∧P same interval: one inequality per fixed H. FAILS.
9. Exception at final index: cyclic mod-s arithmetic; witness exception interior anyway. FAILS.
10. Second exception: exactly-one is definitional (H1–H5); CTL-B shows two-exception walks excluded (replayed, closes, A=58/Q=36/C_K=16). FAILS.
11. Uncovered extra debts: full census (only K3 Type P + K5 exception). FAILS.
12. Wrong core size: core 9 at all 19 states (initial + 18). FAILS.
13. A/B divergence after DELETE: serials recorded per access; nonshadow verified. FAILS.
14. S1-control-as-theorem-witness: CTL-A is S1-banked, never used for S2 novelty. FAILS.
15. S1/AM-G K5 error repeat: K5-local AM-G pass AFFIRMED here (G5 fail verified: 2<3); global exclusion via K3 + K5-G5. FAILS (attack).
16. Forbidden fixture: SHA gate rejects c920…; indexed guards pin INC/CTL. FAILS.
17. Banked acceptance: full audit above — none accepts. FAILS.
18. Five-key-full/universal promotion: never claimed; S2-H5 + exception keep it narrow. FAILS.

No unresolved attack. Gate 0 may pass.
