# Prior-domain exclusions — INC outside the complete banked union (PROVED)

Walk: 18 accesses, A=31,Q=18,C_K=8,W=−44, core 9, closure, engines agree.
Positives: K3 (blk2, r=9), K5 (blk9, r=9). Rest ≤0 (only other debt: none —
full census: K3 Type P, K5 exception; all else w≤0).

- RT2-A/CDK4-A: 5 keys. CDK5L-A: core 9. CDK5NP-A: K5 debt fails K (H=1,dA=1)
  and P (preceding K9 KEEP). CDK5NS1P-A: K7 succ H=1<2. CDK5NS2P-A: second
  succ K1 H=1<2 (S2 needs H≥2 there; payer K9 sits third — VR shape).
- Baselines: n=9 keys; positive dB=6; A=31. All fail.
- 26AJ: successors K7≠9 (both). 26AK/AL: K3→D5 (DELETE, B-frozen)≠9; K5→K1≠9.
- 26AM-G/S: K3 G2+G4 fail; K5 locally G-compatible but S fails (0,−2) and
  global needs K3 (see AM file).
- 26AN/AO: positives at blocks 2,9; zero Type-I/II matches at all 18 cuts.
- 26AP: maximal runs [2],[9] len-1; successors K7≠9.
- 26AQ: positive-run total 2<3 (Direct pieces need immediate returns — absent).
- 26AR: no run≥3 (Direct/Bridge/Split inapplicable).
- 26AS: anchors r=s=9 (distinctness fails).
- Executable (unmodified, hashed): 26AO/26AP/26AQ/26AR/26AS all REJECT.

**W_INC ∈ VR ∖ C_banked. Rule 4 satisfied.** Local compatibilities (K5 AM-G
packet) reported, never promoted.
