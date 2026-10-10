# MRP novelty regression (§11) — retained at current HEAD, no superseder

Walk: 33 accesses, A=55,Q=36,C_K=16,W=−74, core 9, closure, engines agree.
Positives: K3@2 (a=1,q=3,δ=+1,r=9,h=2), K5@9 (a=1,q=3,δ=+1,r=9,h=2),
K5@22 (same). Rest ≤0 (K3@15: a=2,q=3,δ=−1 — interval debt, not source block).

- Cardinality/core/baselines: 5 keys; core 9; n=9; positive dB=6; A=55. EXCLUDED.
- CDK5NP-A: K5 debts (H=1) fail K (dA=1) and P (preceding K9 KEEP) — both.
  EXCLUDED. CDK5NS1P-A: successors (K7) H=1<2 — both. EXCLUDED. CDK5NS2P-A:
  seconds (K1) H=1<2 — both. EXCLUDED. CDK5NVRP-A: two exceptions (VR needs
  exactly one). EXCLUDED.
- AJ: successors K7≠9 (all three). AK/AL: K3a→D5 (DELETE, B-frozen)≠9;
  K5s→K1≠9. EXCLUDED (S-containment banked).
- 26AM-G: K3a packet (K3,K7,D5,K1): G2 FAIL (D5 not genuine) + G4 FAIL (K1≠9).
  K5a/K5b packets (K5,K7,K1,K9): G1–G4 pass, G5 4≥3 pass, G6 pass — LOCALLY
  COMPATIBLE (affirmed, never denied). Global: K3a uncovered ⇒ walk ∉ C_26AM-G.
- 26AM-S: K5 packets meet signed conditions (intermediates (0,0), return a=2);
  K3a fails (DELETE intervener). Global exclusion stands.
- 26AN/AO: positives at blocks 2,9,22; zero Type-I/II matches at all 33 cuts.
- 26AP: maximal runs [2],[9],[22] len-1; successors K7≠9.
- 26AQ: three isolated unit-positives; no (run,bridge,payer) triple: gaps 7/13
  with positives inside every span; Direct pieces need immediate returns (absent).
- 26AR: no run≥3 (Direct/Bridge/Split inapplicable).
- 26AS: anchors r=s=9 all three (distinctness fails).
- Executable (unmodified, hashes 4f4b40e0/9abefb16/9dc40634/8bab76f3/1b737aae):
  26AO/26AP/26AQ/26AR/26AS all REJECT.

**W_INC ∈ M_R ∖ C_banked. Rule 4 retained.** Local compatibilities (both K5s)
recorded; only global coverage matters, and it fails on K3a.
