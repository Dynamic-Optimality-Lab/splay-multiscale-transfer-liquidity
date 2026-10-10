# S2P novelty regression (§18) — retained at current HEAD, no superseder

Same 18-access witness re-audited against current banked definitions.

- Cardinality/core/baselines: 5 keys; core 9; n=9; positive dB=6; A=29. EXCLUDED.
- CDK5NP-A: K5 debt (H=1) fails K (dA=1) and P (preceding K9 KEEP). EXCLUDED.
- CDK5NS1P-A: K5's successor K7 has H=1<2. EXCLUDED.
- AJ: successors K7≠9 (both positives). AK/AL: K3→D9 (DELETE, B-frozen)≠9;
  K5→K1≠9. EXCLUDED (S-containment banked).
- 26AM-G: K3 packet (K3,K7,D9,D5): G2 FAIL (D9 not genuine) + G4 FAIL (D5≠9).
  K5 packet (K5,K7,K1,K9): G1–G4 pass (genuine, −2/0... precisely G3=(0,−2),
  G4 KEEP 9), **G5 FAIL (2a=2<3, h=2)** — the authoritative S2 classification
  (not the S1 witness's 2a=4 case). Global: K3 uncovered ⇒ walk ∉ C_26AM-G.
  26AM-S fails (K7 δ=0 but K1 δ=−2≠0; K3's packet has a DELETE). EXCLUDED.
- 26AN/AO: positives at blocks 2,9; zero Type-I/II matches at all 18 cuts.
- 26AP: maximal runs [2],[9] len-1, successors K7≠9. 26AQ: run total 2<3.
- 26AR: no run≥3. 26AS: anchors r=s=9.
- Executable (unmodified, hashes 4f4b40e0/9abefb16/9dc40634/8bab76f3/1b737aae):
  26AO/26AP/26AQ/26AR/26AS all REJECT.

**W_INC ∈ S_2 ∖ C_banked. Rule 4 retained.** No replacement witness.
