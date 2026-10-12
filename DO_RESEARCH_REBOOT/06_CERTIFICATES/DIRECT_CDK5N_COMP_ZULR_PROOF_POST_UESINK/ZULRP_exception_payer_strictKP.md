# Exception completeness + unique payer + strict K/P (L3–L5a record)

## L3 — Zero exceptions complete, non-K/P vacuous

E={j:c=1,q=3,H=1} by exact scan; H2 requires |E|=0 (IN: E=[] verified).
Completeness is definitional (any (1,3,1) slot would be listed).

## L4 — Unique self-payer (existential, full case table)

U={j:w>0,¬K,¬P}; H3 requires |U|=1, U={p} (IN: U={0} verified: x=3,H=18,
q=3,w=1,R=34,dA=0 — not-K since dA<3; not-P since prev access is DELETE(3),
same key). H4 requires H_p≥2 for that same p (IN: 18≥2). With c_p=1
(w>0 forces c=1) and q_p∈{3,4}: R_p=2(H_p−1)≥2 and w_p=q_p−2≤2, so w_p≤R_p
intrinsically — no borrowed credit. Sharp case q_p=4,H_p=2: w=2,R=2,
equality 2=2 (included, not omitted). q_p=3,H_p=2: 1≤2. No H≥3 requirement
(IN H_p=18 is corroboration, not a threshold).

## L5a — Strict predicates imply reserves

Strict K (d_A≥3 at KEEP) ⇒ a≥2 on that leg ⇒ H≥2; with c=1 (w>0 forces
c=1), R=2(H−1)≥2≥w (w≤2). Strict P (prev-DELETE distinct, a≥1 both, same
interval) ⇒ H≥2 ⇒ same. H≥2 is a CONSEQUENCE, never the definition
(H≥2 alone does not imply K — e.g., a dA=0/H≥2 interval is not K).
IN others: iv4 strict-K (dA=4); iv8 strict-K (dA=3) + strict-P (prev-D4
distinct, a≥1 both); iv12 strict-K (dA=4).
