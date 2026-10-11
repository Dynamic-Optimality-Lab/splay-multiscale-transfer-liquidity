# UESINK L1–L7 universal proof (proof stage — reconstructed, fixture-free)

For arbitrary W satisfying frozen H1–H5 (any ambient size, length, DELETEs,
order, prefixes, divergence, seams). No Q≤2C_K premise anywhere below.

L1 (partition + baseline): cyclic KEEP intervals cut at KEEPs (seam by
closure); each access in exactly one I_j. ΣH=A, Σq=Q, Σc=C_K (hence
Σw=Q−2C_K, ΣR=2(A−C_K)). H≥c: c=0 trivial; c=1 with H=0 would make every
access an A-root no-op (root splays change nothing), freezing the root at
the previous key and forcing the terminal KEEP there — contradicting c=1.
So R≥0.

L2 (debt): marked core (ancestor-closed union of root→marked-key paths) has
nine nodes at every state (H1); genuine KEEP keys are marked, so root paths
lie inside the core: ≤8 edges, d_B≤8, q≤4. c=0 ⇒ B still rooted (DELETEs
freeze; single KEEP per interval) ⇒ q=0 ⇒ w=0. Hence w>0 ⇒ c=1, q∈{3,4},
w∈{1,2}.

L3 (unique exception): |E|=1, (c,q,H)=(1,3,1): w=1, R=0. Strict K (d_A≥3 ⇒
a≥2) and strict P (two a≥1 accesses) each imply H≥2, never 1 — the exception
satisfies neither. E complete by definition.

L4 (joint sink, full q_p table): ∃p∉E (c=1,H≥3, enumerated): R_p≥4;
w_p=q_p−2≤2. Table: q=0→w=−2 (need −1≤R ✓); 1→−1 (0≤R ✓); 2→0 (1≤R ✓);
3→1 (2≤R ✓); 4→2 (3≤R ✓, tight at H=3: 3≤4 included). So w_e+w_p = 1+w_p
≤ 3 ≤ R_p. IN: p=0, H=18, q=3, w=1, R=34 (2≤34). ∎

L5 (others, predicates first): j∉{e,p}. w≤0 ⇒ w≤R. w>0 ⇒ strict-K
(d_A≥3 ⇒ a≥2 ⇒ H≥2) or strict-P (a≥1 both ⇒ H≥2) by H5; with c=1,
R=2(H−1)≥2≥w. IN: iv4 strict-K (dA=4), iv8 strict-K (dA=3) + strict-P.

L6 (disjointness): {e,p} distinct; pair + singletons partition intervals;
sink spent once; exception never recharged; accesses counted once.

L7 (telescoping): Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A (IN: 4≤80 ⇒ 36≤112).

## L8 — Relay-independence audit

Payment steps C1–C7/L1–L7 never query t_e. Bridges are ordinary w≤R
singletons; the t≥2 gate is domain membership only. No short-relay
assumption; no H3 change. An H3-free single-exception variant is NOT
claimed here. ∎
