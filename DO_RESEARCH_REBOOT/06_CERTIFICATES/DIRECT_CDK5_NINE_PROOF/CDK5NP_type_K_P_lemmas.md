# Lemmas 3–4 — Type K / Type P payment (PROVED)

## Lemma 3 (Type K)

d_A(x_j)≥3 ⇒ a(K_j)=⌈d_A/2⌉≥2. KEEP j ∈ I_j ⇒ H_j≥a(K_j)≥2. Positive debt gives
c_j=1 (Lemma 2) ⇒ R_j=2(H_j−1)≥2 ≥ w_j (w_j≤2). Hence w_j≤R_j. Source-level;
no witness values used. ∎

## Lemma 4 (Type P)

Hypotheses: (i) the immediately preceding full-word occurrence is DELETE y;
(ii) y≠x_j; (iii) a(D_y)≥1; (iv) a(K_j)≥1. The DELETE precedes KEEP j and
follows KEEP j−1 (otherwise the preceding occurrence would be KEEP j−1 itself,
contradicting (i)) ⇒ both accesses lie in I_j. They are distinct occurrences ⇒
H_j≥a(D_y)+a(K_j)≥2. With c_j=1: R_j≥2≥w_j. Hence w_j≤R_j. Same-key shadows
(y=x_j) are excluded by (ii) — the control's D3/K3 configuration can never
satisfy Type P. No distant donors: only the immediately preceding occurrence
qualifies; no interval extension. ∎
