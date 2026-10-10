# CDK5N-DP source semantics (authoritative implementations pinned)

Engines: `scripts/wp6_eventflow.py` (pointer splay + StepEv traces),
`python/independent/splay.py` (tuple splay), `python/liquidity/legacy_embedding.py`
(rotation primitives). Hashes recorded in verification results JSON.

- KEEP(x), x present: (A,B)→(S_x(A),S_x(B)).
- DELETE(x), x present: (A,B)→(S_x(A),B); key never removed; key set fixed.
- a_t=⌈d_A(x_t)/2⌉ every access; KEEP q_t=⌊d_B(x_t)/2⌋; DELETE q_t=0.
- A(W)=Σa_t; Q_B(W)=Σq_t (DELETEs contribute q=0).
- Depths measured pre-access (edge counts). Closure = exact labeled BST
  equality of both trees (roots/inorder insufficient).
- A-root no-op (a=0) KEEPs may carry q>0 (control K3: a=0,q=3) — covered by the
  same interval analysis (H_j counts actual StepEvs, possibly 0 from the KEEP).
