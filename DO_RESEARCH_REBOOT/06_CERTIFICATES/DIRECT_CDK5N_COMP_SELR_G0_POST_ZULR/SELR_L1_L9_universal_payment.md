# SELR universal paired-payment proof L1–L9 (Gate C; fixture-free)

For arbitrary W satisfying frozen H1–H5 (any ambient size, length, DELETEs,
order, prefixes, divergence, seams). No Q≤2C_K premise anywhere below.
Mechanism (exactly one): the bare exception e and one distinct unit-debt
donor p are jointly repaid from R_p; every other positive debt is paid
locally by strict K/P. No sink. No transfer. No packet.

L1 (partition): cyclic KEEP intervals cut at KEEPs (seam by closure); each
access in exactly one I_j. ΣH=A, Σq=Q, Σc=C_K (hence Σw=Q−2C_K,
ΣR=2(A−C_K)).

L2 (baseline): H≥c (c=0 trivial; c=1 with H=0 would freeze the A-root at
the previous key — all accesses A-root no-ops — contradicting a
different-key KEEP); so R≥0. Marked core (ancestor-closed root→marked-key
paths, nine nodes by H1) contains every genuine KEEP root path: ≤8 edges,
d_B≤8, q≤4 (ambient size unrestricted). c=0 ⇒ B rooted + frozen ⇒ q=0 ⇒
w=0. Hence w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}.

L3 (debt bound): w>0 implies w∈{1,2} (L2). This bound is used by L5/L6;
no membership conclusion is drawn from it.

L4 (exceptional unit debt): E={e} (H2): w_e=1, R_e=0. Strict K needs
d_A≥3 ⇒ a≥2 ⇒ H≥2, contradicting H_e=1, so ¬K_e. Strict P needs a≥1 on
both the DELETE and the KEEP ⇒ H_e≥2, contradicting H_e=1, so ¬P_e. Hence
e∈U (e is untyped positive).

L5 (donor joint payment): U={e,p}, p≠e (H4); at p: c_p=1, q_p=3, H_p≥2.
Thus w_p=1 and R_p=2(H_p−1)≥2, so w_e+w_p=1+1=2≤R_p jointly from R_p.
Sharp boundary H_p=2, q_p=3: w_e+w_p=R_p=2, equality (algebraically
included; no physical H=2 witness claimed — see sharp-case audit). A
q_p=4 donor is NOT admitted: it would give w_p=2, needing R_p≥3, which
H_p=2 does not supply (R_p=2 < 1+2=3); H4 pins q_p=3.

L6 (others, predicates first): j∉{e,p}. w≤0 ⇒ w≤R. w>0 ⇒ strict-K
(d_A≥3 ⇒ a≥2 ⇒ H≥2) or strict-P (a≥1 both ⇒ H≥2) by H5; with c=1,
R=2(H−1)≥2≥w. IN: j=8 K (dA=3) + P; j=12 K (dA=4). H≥2 is a CONSEQUENCE,
never the definition.

L7 (disjoint payment): groups are the pair {e,p} plus every other interval
as a singleton. No interval appears twice; no A-cost double-counted; no
reserve reused; no second credit source.

L8 (telescoping): Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN: 4≤74 ⇒ 36≤104).

L9 (noncircularity/hypothesis audit): H3 relay length classifies only —
never counted as repayment (relay intervals with w>0 still need K/P via
H5; t_e=0/1 bounds the exceptional neighborhood, it pays nothing). H4
q_p=3 essential (two-unit debt bound); H4 H_p≥2 essential (two-unit
reserve). H5 supplies strict local repayment elsewhere. No global target
assumed; no second donor; no H3-free claim; no q_p=4 donor admitted. ∎
