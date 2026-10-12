# SELRP universal L1–L10 proof (fixture-independent; correct IN accounting)

For arbitrary W satisfying frozen H1–H5. No Q≤2C_K premise. Mechanism
(exactly one): bare exception e + distinct q=3/H≥2 donor p jointly from
R_p; all other positives strict-K/P locally. No sink/transfer/packet.

L1 (partition): cyclic KEEP intervals cut at KEEPs (seam by closure);
each access in exactly one I_j. ΣH=A, Σq=Q, Σc=C_K; Σw=Q−2C_K,
ΣR=2(A−C_K).

L2 (baseline): H≥c. c=0 by nonnegativity. c=1 with H=0 would freeze the
A-root at the previous key (all accesses A-root no-ops), contradicting a
different-key KEEP. Hence R=2(H−c)≥0. Marked core (ancestor-closed,
nine nodes) contains every genuine KEEP root path: ≤8 edges, d_B≤8, q≤4
(arbitrary ambient). c=0 ⇒ B rooted+frozen ⇒ q=0 ⇒ w=0.

L3 (debt bound): w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}.

L4 (exception): E={e} gives c_e=1,q_e=3,H_e=1,w_e=1,R_e=0. Strict K needs
a≥2 on the KEEP (d_A≥3); strict P needs a≥1 on two consecutive accesses;
either gives H_e≥2, contradicting H_e=1. So ¬K_e, ¬P_e: e untyped positive.

L5 (donor): U={e,p}, p≠e; c_p=1,q_p=3,H_p≥2 ⇒ w_p=1, R_p=2(H_p−1)≥2.
Paired debt w_e+w_p=1+1=2≤R_p from R_p alone. No extra reserve/sink/donor.

L6 (sharp boundary): H_p=2,q_p=3 ⇒ w_p=1,R_p=2 ⇒ w_e+w_p=R_p=2, valid
algebraic equality. Frozen IN has H_p=18 (no physical H=2 witness
claimed). q_p=4,H_p=2 would give w_p=2,R_p=2, w_e+w_p=3>2 — H4's q_p=3
correctly excludes it.

L7 (others): j∉{e,p}. w≤0 ⇒ w≤R. w>0 ⇒ K (d_A≥3⇒a≥2⇒H≥2) or P (a≥1
both⇒H≥2) by H5; c=1 ⇒ R=2(H−1)≥2≥w. H≥2 consequence, never definition.
IN: j=8 K(dA=3)+P; j=12 K(dA=4).

L8 (disjoint groups): {e,p} + singletons. e≠p. Full cover, no overlap
(K/P overlap counts once), no A-cost double-count, R_p funds w_e+w_p
only, other positives use own R_j, relay pays nothing.

L9 (telescoping): Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A. Correct IN numbers:
Σw=4, ΣR=74, 4≤74, 36−32≤106−32, 36≤106 (Erratum A). OUT: 36≤104.

L10 (scope/redundancy/noncircularity): H3 classifies only (short relay
bounds the exceptional neighborhood; relay w>0 still needs K/P via H5).
H5 retained though implied by exact U-classification. H4 q_p=3 essential
(two-unit debt); H_p≥2 essential (two-unit reserve). Exception unique,
donor distinct, no further untyped positives. No aggregate premise, no
universal-Coarse-Double assumption, no DO invocation, no post-hoc
generalization (even where arithmetic would allow more). ∎
