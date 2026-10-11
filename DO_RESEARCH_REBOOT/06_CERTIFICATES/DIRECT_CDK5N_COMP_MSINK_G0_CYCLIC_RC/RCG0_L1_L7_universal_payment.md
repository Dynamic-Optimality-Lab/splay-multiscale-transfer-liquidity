# RCG0 L1–L7 universal payment proof (task M — reconstructed for H1–H6)

## L1 — Interval identities + baseline

Cyclic KEEP intervals partition accesses (each access follows one preceding
KEEP; seam by closure): ΣH=A, Σq=Q, Σc=C_K, Σw=Q−2C_K, ΣR=2(A−C_K) (verified
on IN-new: 64/36/16 identities hold). H≥c: c=0 trivial (same key, no A-change
needed... precisely: interval's KEEP key equals previous; A-root-change
argument gives first changing access a≥1 when c=1). Hence R≥0. A-root no-ops
(a=0) and arbitrary DELETEs allowed.

## L2 — Nine-core bound

Marked B-core nine ⇒ every B-depth d_B≤8 ⇒ q=⌊dB/2⌋≤4 (observed max q=3,
max dB=6 on corpus). c=0 ⇒ B still rooted at same key (DELETEs freeze B) ⇒
q=0 ⇒ w=0 (verified 0/384 violations). w>0 ⇒ c=1, q∈{3,4} ⇒ w∈{1,2}. No
Q≤2C_K claim made.

## L3 — Complete exceptions

E={j:c=1,q=3,H=1}, |E|=2 required. Each: w=1, R=0. H=1 excludes strict K
(needs d_A≥3 ⇒ a≥2 ⇒ H≥2) and strict P (needs two a≥1 accesses ⇒ H≥2).
E-complete by definition (every such interval listed).

## L4 — Joint sink

∃p∉E with c=1, H≥3 (all candidates enumerated; first-H4-only forbidden).
R_p=2(H_p−1)≥4; w_p=q_p−2≤2 (audited q_p∈{0..4}: w∈{−2..2}; IN-new p=0:
H=13, q=3, w=1, R=24; joint 1+1+1=3≤24). Joint: 1+1+w_p ≤ 4 ≤ R_p
(q=4/H=3 boundary: 2+2=4≤4 exactly — the frozen threshold). ∎

## L5 — Remaining singletons

j∉E∪{p}: w≤0 ⇒ w≤R (R≥0); w>0 ⇒ strict K (d_A≥3 ⇒ H≥2 ⇒ R≥2≥w) or strict P
(distinct prev-DELETE, a≥1 both ⇒ H≥2 ⇒ R≥2≥w). IN-new sole other-positive
iv8 (x=3,H=16,q=3,w=1,R=30,dA=2): strict-P via preceding D4 (a=1, both a≥1).

## L6 — Disjointness

{e1,e2,p} distinct; triple + singletons partition all intervals; sink reserve
spent once (K/P-eligible p still consumed by joint, never recharged);
exceptions never recharged; every access in exactly one interval.

## L7 — Telescoping

Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN-new: 4≤96 ⇒ 36≤128). Arbitrary n/tree
size/DELETEs/order/prefixes/divergence/seams/relay lengths/sink choices.
No aggregate premise, no witness-specific bound, no circularity.
Gate-0 certification mechanism only (NOT a promotion proof).
