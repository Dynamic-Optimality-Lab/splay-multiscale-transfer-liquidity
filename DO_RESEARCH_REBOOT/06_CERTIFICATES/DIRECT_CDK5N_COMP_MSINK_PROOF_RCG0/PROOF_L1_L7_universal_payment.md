# CDK5NMSP-A universal payment proof L1–L7 (Gate A, reconstructed)

Domain: H1–H6 frozen (five genuine keys, core nine, |E|=2, mixed relays,
joint existential sink, strict K/P). Claim: Q_B ≤ 2A for every member.

## L1 — Interval identities + baseline

Cyclic KEEP intervals I_j (accesses after preceding KEEP through current
KEEP) partition accesses exactly once (cyclic seam by closure): ΣH=A,
Σq=Q_B, Σc=C_K, Σw=Q_B−2C_K, ΣR=2(A−C_K) (verified on IN-new 64/36/16).
H_j≥c_j: if c_j=0, H_j≥0=c_j. If c_j=1 and H_j=0, every access in I_j has
a=0, i.e., hits the current A-root without restructuring; the root stays
x_{j-1} (put there by the preceding KEEP splay; root splays are no-ops), so
the terminal KEEP targets x_{j-1}, i.e., x_j=x_{j-1}, contradicting c_j=1.
Hence c_j=1 ⇒ H_j≥1=c_j. So R_j=2(H_j−c_j)≥0. A-root no-ops and arbitrary
DELETEs allowed throughout.

## L2 — Nine-core debt bound

B holds exactly keys 1..9 (DELETE never removes; all keys present) ⇒ every
d_B≤8 ⇒ q=⌊dB/2⌋≤4 for KEEPs (corpus max dB=6, q=3). c_j=0 ⇒ x_j=x_{j-1}:
B was rooted at x_{j-1} by the preceding KEEP splay and frozen by the
intervening DELETEs (I_j contains no other KEEP) ⇒ d_B=0 ⇒ q_j=0 ⇒ w_j=0
(verified 0 violations corpus-wide). Thus w_j>0 ⇒ c_j=1, q_j∈{3,4} ⇒
w_j∈{1,2}. No Q≤2C_K premise.

## L3 — Complete exceptions

E={j:c=1,q=3,H=1}, |E|=2 by H2; each w=1, R=0. Strict K needs d_A≥3 ⇒ the
KEEP leg has a≥2 ⇒ H≥2, contradicting H=1. Strict P needs a preceding
a≥1 DELETE plus an a≥1 KEEP, both inside the interval ⇒ H≥2, contradiction.
So exceptions satisfy neither; E complete by definition.

## L4 — Joint sink (full q_p table)

H4/H5 give p∉E with c=1, H≥3 (existential; all candidates enumerated).
R_p=2(H_p−1)≥4; w_p=q_p−2 with q_p≤4:

| q_p | w_p | need 2+w_p≤R_p | holds (R_p≥4) |
|---|---|---|---|
| 0 | −2 | 0≤R_p | yes |
| 1 | −1 | 1≤R_p | yes |
| 2 | 0 | 2≤R_p | yes |
| 3 | 1 | 3≤R_p | yes |
| 4 | 2 | 4≤R_p | yes, tight at H_p=3 |

Hence w_{e1}+w_{e2}+w_p = 2+w_p ≤ 4 ≤ R_p = R_{e1}+R_{e2}+R_p. The H=3 bound
is exactly the q=4 tight case. IN-new: p=0, H=13, q=3, w=1, R=24 (3≤24). ∎

## L5 — Remaining singletons (strict predicates first)

Let j∉E∪{p}. If w_j≤0: w_j≤R_j by L1. If w_j>0: H5 gives strict-K or
strict-P (frozen definitions). Strict-K (d_A≥3 on the KEEP leg) ⇒ a≥2 on
that leg ⇒ H_j≥2; with c_j=1 (w>0 forces c=1 by L2 contrapositive),
R_j=2(H_j−1)≥2≥w_j. Strict-P (prev-DELETE distinct, a≥1 both, same
interval) ⇒ H_j≥2 ⇒ same R_j≥2≥w_j. IN-new sole other-positive iv8
(x=3,H=16,w=1,R=30,dA=2): strict-P via preceding D4 (both a≥1). ∎

## L6 — Disjointness

{e1,e2,p} distinct (E indices distinct; p∉E enforced). Triple + singletons
partition all intervals; sink reserve spent once (a K-eligible p is still
consumed by the joint inequality only — see K-eligibility erratum:
eligibility ≠ double charge); exceptions never recharged; every access in
exactly one H_j (Σ-identities).

## L7 — Telescoping

Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN-new: 4≤96 ⇒ 36≤128). Arbitrary n, tree
size, DELETEs, order, prefixes, divergence, seams, relays, sink choices.
No aggregate hypothesis, no witness-specific bound, no circularity.
Finite replays corroborate instances; they are not the proof.
