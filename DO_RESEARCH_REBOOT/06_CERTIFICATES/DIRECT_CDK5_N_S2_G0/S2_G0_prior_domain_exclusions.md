# Prior-domain exclusions — INC outside the complete banked union (PROVED)

Walk: 18 accesses, A=29,Q=18,C_K=8,W=−40, core 9, closure, engines agree.
Positives: K3 (blk2: a=1,q=3,δ=+1,r=9), K5 (blk9: a=1,q=3,δ=+1,r=9). Rest ≤0.

- RT2-A/CDK4-A: 5 keys. CDK5L-A: core 9. CDK5NP-A: K5 debt fails K (dA=1) and P
  (preceding K9 KEEP). CDK5NS1P-A: K5's successor K7 has H=1<2.
- Baselines: n=9 keys; positive dB=6; A=29. All fail.
- 26AJ: successors K7≠9 (both). 26AK/AL: K3→D9≠9 (DELETE, not B-changing);
  K5→K1≠9. S-containment banked.
- 26AM-G: K3 packet (K3,K7,D9,D5): G2 FAIL (D9 DELETE) + G4 FAIL (D5≠9).
  K5 packet (K5,K7,K1,K9): G1–G4 pass, **G5 FAIL (2a=2<3, h=2, a(K9 idx12)=1)**,
  G6 moot. Global needs both ⇒ walk ∉ C_26AM-G. 26AM-S fails (K7 δ=0? — K5's
  intermediates (0,−2): S needs δ=0 BOTH; K1 −2≠0 ⇒ S fails; K3's intermediates
  include DELETE ⇒ S fails).
- 26AN/AO: positives at blocks 2,9; zero Type-I/II matches at all 18 cuts.
- 26AP: maximal runs [2],[9] len-1; successors K7≠9.
- 26AQ: positive-run total 2<3 (Direct pieces: no valid immediate returns either).
- 26AR: no run≥3 (Direct/Bridge/Split all inapplicable).
- 26AS: anchors r=s=9 (distinctness fails).
- Executable (unmodified, hashed): 26AO/26AP/26AQ/26AR/26AS all REJECT.

**W_INC ∈ S_2 ∖ C_banked. Rule 4 satisfied.** K5-local AM-G compatibility
(G1–G4 pass) reported honestly; global exclusion rests on K5-G5 + K3-G2/G4.
