# VRP novelty regression (§11) — retained at current HEAD, no superseder

Walk: 18 accesses, A=31,Q=18,C_K=8,W=−44, core 9, closure, engines agree.
Positives: K3 (blk2: a=1,q=3,δ=+1,r=9,h=2), K5 (blk9: a=1,q=3,δ=+1,r=9,h=2).

- Cardinality/core/baselines: 5 keys; core 9; n=9; positive dB=6; A=31. EXCLUDED.
- CDK5NP-A: K5 debt (H=1) fails K (dA=1) and P (preceding K9 KEEP). EXCLUDED.
- CDK5NS1P-A: K7 succ H=1<2. CDK5NS2P-A: second succ K1 H=1<2. EXCLUDED.
- AJ: successors K7≠9 (both). AK/AL: K3→D5 (DELETE, B-frozen)≠9; K5→K1≠9. EXCLUDED.
- 26AM-G: K3 packet (K3,K7,D5,K1): G2 FAIL (D5 not genuine) + G4 FAIL (K1≠9).
  K5 packet (K5,K7,K1,K9): G1–G4 pass, G5 4≥3 pass, G6 pass — LOCALLY COMPATIBLE
  (affirmed, never denied). Global: K3 uncovered ⇒ walk ∉ C_26AM-G.
- 26AM-S: K5's packet meets the signed conditions too (intermediates (0,0),
  return a=2≥2) — LOCALLY COMPATIBLE (corrects any claim to the contrary); K3
  fails (DELETE intervener, nonzero intermediates) ⇒ global exclusion stands.
- 26AN/AO: positives at blocks 2,9; zero Type-I/II matches at all 18 cuts.
- 26AP: maximal runs [2],[9] len-1, successors K7≠9. 26AQ: run total 2<3.
- 26AR: no run≥3. 26AS: anchors r=s=9.
- Executable (unmodified, hashes 4f4b40e0/9abefb16/9dc40634/8bab76f3/1b737aae):
  26AO/26AP/26AQ/26AR/26AS all REJECT.

**W_INC ∈ V_R ∖ C_banked. Rule 4 retained.** Local compatibilities (K5 AM-G/S)
recorded; only global coverage matters, and it fails on K3.
