# 26AN audit: witness replay + packet + novelty + negative controls

## Authoritative replay (FIRST gate, passed — no search run)

- Script: `06_CERTIFICATES/26AN/26AN_vine8_candidate_replay.py` (authoritative
  `wp6_eventflow.to_ptr/splay_A/splay_B_push`); certificate:
  `26AN_vine8_witness_certificate.json`; log: `26AN_execution_log.txt`.
- T0 `(1.(2.(3.(4.(5.(8(7(6..).).))))))` built exactly (N1 ✓ — not a vine).
- Prefix D2,D8,D4,D6,D3 from diagonal A0=B0, DELETEs A-only (N2 ✓):
  A_start/B_start match expected serials exactly.
- Cycle K6,K8,K4,K1,K2,K5,K8,K2,K3,K1,D6,D4,D3: EXACT A/B closure PASS (N3 ✓);
  cost table 13/13 (N4 ✓); A=20, Q_B=14, W=−26; all a≥1 (13 blocks).
- Independent `python/independent/splay.py` comparison: 18/18 depths, costs,
  shapes (N9: universal proof separate, in 02_PROVED doc).

## Packet certificate (PACKET_ANCHORS=[1], 1-based)

- Positives exactly blocks 1 (K6: dA=2,dB=7,a=1,q=3,δ=+1) and 3 (K4:
  dA=2,dB=6,a=1,q=3,δ=+1). No unaccounted positives (N10 ✓).
- P1: r=1 recovered as B-root before K6 (N6 ✓), h=1 after (≤2 ✓).
- P2: K8 genuine B-change (N5 ✓), dB=2∈[1,3], y=8≠6,1 ⟹ δ=−1 derived (N8 ✓).
- P3: K4 genuine B-change (N5 ✓), δ=+1 source-computed — the novelty.
- P4/P5: block 4 leader K1=r, a=2, dB=1, q=0, δ=−4 (≤−1 required; N8 ✓).
- Packet total (+1,−1,+1,−4)=−3; blocks 5–13 deficits
  −1,−2,−1,−3,−3,−1,−6,−4,−2 (all ≤0); cycle total −26.

## Strict novelty (N7, N11)

- K6 vs 26AJ (succ 8≠1 ✗), 26AK/26AL-G/26AL-S (i+2 key 4≠1 ✗), 26AM-G (G3 ✗),
  26AM-S (✗). K4 (r'=8) vs 26AJ/26AK/26AL-G/26AL-S (succ 1,2,5 ≠8 ✗),
  26AM-G (i+3 key 5≠8, G4 ✗). n=8, depths 7/6, A=20 (other classes ✗).
- 26AL post-gate same-side certificate does not alter 26AL-G hypotheses;
  exclusion stands on former-root positions, not geometry.
- Conclusion: γ*∈C_26AN∖C_old. No C_old⊆C_26AN claim. 26AM Outcome B untouched;
  seven-key 26AM-G post-gate note remains separate work (§17).

## Downstream (N12)

Unrestricted Coarse-Double, PIVOT-2, LT, Dynamic Optimality: unchanged (OPEN/CONDITIONAL).
