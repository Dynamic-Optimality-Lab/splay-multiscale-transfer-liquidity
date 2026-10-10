# VRP source semantics (authoritative, hashed in verification results)

Engines: scripts/wp6_eventflow.py (pointer splay + StepEv traces),
scripts/wp6_coarse_double.py (q/z accounting reference),
python/independent/splay.py (tuple splay), python/liquidity/legacy_embedding.py
(primitives). KEEP(x) present: (A,B)→(S_x(A),S_x(B)). DELETE(x) present:
(A,B)→(S_x(A),B); key never removed; key set fixed. a_t=⌈d_A/2⌉; KEEP
q_t=⌊d_B/2⌋; DELETE q_t=0. A=Σa, Q_B=Σq. Depths pre-access. Closure = exact
labeled BST equality both trees. A-root no-ops (a=0) may carry q>0; covered by
identical interval sums (H counts actual StepEvs).
