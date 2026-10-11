# DLSS L1–L7 universal proof (proof stage — reconstructed, fixture-free)

For arbitrary W satisfying frozen H1–H5 (any ambient size, length, DELETEs,
order, prefixes, divergence, seams). No Q≤2C_K premise anywhere below.

L1 (partition + baseline): cyclic KEEP intervals cut at KEEPs (seam by
closure); each access in exactly one I_j. ΣH=A, Σq=Q_B, Σc=C_K (hence
Σw=Q_B−2C_K, ΣR=2(A−C_K)). H≥c: c=0 trivial; c=1 with H=0 would make every
access an A-root no-op (root splays change nothing), freezing the root at
x_{j-1} and forcing the terminal KEEP to x_{j-1}, contradicting c=1. R≥0.

L2 (debt): marked core (ancestor-closed union of root→marked paths) has nine
nodes at every state (H1); genuine KEEP keys are marked, so d_B≤8, q≤4.
c=0 ⇒ same key as preceding KEEP: B rooted there and frozen by intervening
DELETEs (no other KEEP inside I_j) ⇒ q=0 ⇒ w=0. Hence w>0 ⇒ c=1, q∈{3,4},
w∈{1,2}.

L3 (exceptions): E complete by definition, |E|=2, each (w,R)=(1,0). Strict K
(d_A≥3 ⇒ a≥2) and strict P (two a≥1 accesses) each imply H≥2, impossible at
H=1 — so exceptions satisfy neither.

L4 (sink): joint p∉E, c=1, H≥3 (existential over all candidates). R_p≥4;
w_p=q_p−2≤2 over q_p∈{0,1,2,3,4} (tight 4≤4 at q=4,H=3 included). Joint:
1+1+w_p ≤ 4 ≤ R_p.

L5 (others): j∉E∪{p}. w≤0 ⇒ w≤R. w>0 ⇒ H5 gives strict-K (⇒a≥2⇒H≥2) or
strict-P (⇒H≥2); with c=1, R=2(H−1)≥2≥w.

L6 (disjointness): {e1,e2,p} distinct; triple + singletons partition all
intervals; sink spent once; exceptions never recharged; accesses counted once.

L7 (telescoping): Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A. Universal over the domain.
Finite replays corroborate instances; no replay step substitutes for any
implication above.
