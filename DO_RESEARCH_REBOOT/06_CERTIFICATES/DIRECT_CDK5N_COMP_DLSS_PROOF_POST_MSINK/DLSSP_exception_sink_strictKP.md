# DLSS exception completeness (L3) + joint sink audit (L4) + strict K/P (L5a)

## L3 — Exceptions complete, non-K/P

E={j:c=1,q=3,H=1}, |E|=2 by H2 (IN: E=[4,12], verified complete by scan).
Each: w=3−2=1, R=2(1−1)=0. Strict K needs d_A≥3 ⇒ KEEP-leg a≥2 ⇒ that leg
alone contributes ≥2 to H ⇒ H≥2≠1. Strict P needs a≥1 DELETE + a≥1 KEEP in
the interval ⇒ H≥2≠1. So no exception satisfies K/P; E lists all such slots.

## L4 — Joint sink with full q_p table

H4/H5 (joint existential, all candidates enumerated): p∉E, c=1, H≥3.
R_p=2(H_p−1)≥4; w_p=q_p−2≤2:

| q_p | w_p | need 2+w_p ≤ R_p (R_p≥4) |
|---|---|---|
| 0 | −2 | 0 ≤ R_p ✓ |
| 1 | −1 | 1 ≤ R_p ✓ |
| 2 | 0 | 2 ≤ R_p ✓ |
| 3 | 1 | 3 ≤ R_p ✓ (IN: p=0, H=18, R=34: 3≤34) |
| 4 | 2 | 4 ≤ R_p ✓ (tight at H_p=3: 4≤4 — included, not omitted) |

Thus w_{e1}+w_{e2}+w_p = 2+w_p ≤ 4 ≤ R_p. ∎

## L5a — Strict predicates imply reserves

Strict K (d_A≥3 at the KEEP leg) ⇒ a≥2 on that leg ⇒ H≥2; with c=1
(w>0 forces c=1 by L2), R=2(H−1)≥2≥w (w≤2). Strict P (immediately preceding
access DELETE(y≠x), a≥1 both, same interval) ⇒ H≥2 ⇒ same R≥2≥w.
H≥2 is a CONSEQUENCE of the frozen predicates, never their definition
(K-erratum: "H≥2 ⇒ K" shorthand retired; d_A≥3 is the only K test).
IN other-positive iv8 (H=4): dA=3 (K ✓) and prev-D4 distinct a≥1 both (P ✓).
