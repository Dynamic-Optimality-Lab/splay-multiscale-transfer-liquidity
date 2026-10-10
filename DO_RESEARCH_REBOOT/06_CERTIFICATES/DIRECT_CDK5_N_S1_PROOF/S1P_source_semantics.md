# S1P source semantics (authoritative, hashed in verification results)

Engines: scripts/wp6_eventflow.py (pointer splay + StepEv traces),
python/independent/splay.py (tuple splay), python/liquidity/legacy_embedding.py
(rotation primitives). KEEP(x) present: (A,B)→(S_x(A),S_x(B)). DELETE(x)
present: (A,B)→(S_x(A),B); key never removed. a_t=⌈d_A/2⌉ all accesses;
KEEP q_t=⌊d_B/2⌋; DELETE q_t=0. A=Σa, Q_B=Σq. Depths pre-access. Closure =
exact labeled BST equality both trees. A-root no-ops (a=0) may carry q>0 and
are covered by the same interval sums (H counts actual StepEvs).
