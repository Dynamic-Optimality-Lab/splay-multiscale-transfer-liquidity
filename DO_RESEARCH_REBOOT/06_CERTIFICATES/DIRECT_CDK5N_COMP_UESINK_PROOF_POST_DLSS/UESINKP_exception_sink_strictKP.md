# Exception completeness + joint sink + strict K/P (L3–L5a record)

## L3 — Unique exception complete, non-K/P

E={j:c=1,q=3,H=1} by exact scan; H2 requires |E|=1 (IN: E=[12] verified).
Each: w=3−2=1, R=2(1−1)=0. Strict K needs d_A≥3 ⇒ KEEP-leg a≥2 ⇒ H≥2≠1.
Strict P needs a≥1 DELETE + a≥1 KEEP in-interval ⇒ H≥2≠1. So the exception
satisfies neither; E-complete by definition (any (1,3,1) slot is listed).

## L4 — Joint sink (existential, full range)

∃p∉E with c=1,H≥3 (all candidates enumerated; H4-only insufficient).
R_p=2(H_p−1)≥4; w_p=q_p−2≤2. Table: q=0→−2,1→−1,2→0,3→1,4→2; need
1+w_p≤R_p: −1,0,1,2,3 ≤ R_p (R_p≥4 always; tight 3≤4 at q=4,H=3 included).
So w_e+w_p=1+w_p≤3≤R_p. IN: p=0 (H=18,q=3,w=1,R=34; 2≤34). ∎

## L5a — Strict predicates imply reserves

Strict K (d_A≥3 at KEEP) ⇒ a≥2 on that leg ⇒ H≥2; with c=1 (w>0 forces
c=1), R=2(H−1)≥2≥w (w≤2). Strict P (prev-DELETE distinct, a≥1 both, same
interval) ⇒ H≥2 ⇒ same. H≥2 is a CONSEQUENCE, never the definition
(K-erratum: H≥2 alone does not imply K — e.g., IN sink dA=0/H=18 is not K).
IN others: iv4 strict-K (dA=4), iv8 strict-K (dA=3) + strict-P (prev-D4).
