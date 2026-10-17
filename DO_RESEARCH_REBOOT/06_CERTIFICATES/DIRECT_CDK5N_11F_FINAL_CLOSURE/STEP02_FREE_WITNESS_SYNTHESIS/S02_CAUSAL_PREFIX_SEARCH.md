# S02_CAUSAL_PREFIX_SEARCH.md — A-side reconstruction (Gates D/G11)

Abstract pins carry no key values (S-indices/refs/counts only), so canonical keys
(S-index i -> 100*(i+1); gap pools by sig counts) always fit. A_0 = 7-position
shadow skeleton (S-positions take core keys; non-S take rank-fitting pool keys;
opaque positions decided by key-range occupancy) + BST-inserted remainder
(asc/desc/balanced orders; exact-once by construction; bounded alternatives).
Candidates filtered by authoritative replay (key presence, A-depth<=4 relation
macro legality, q cross-check). No inverse-splay lemma is invented: forward replay
decides. Slots are never allocated blindly (skeleton-first, remainder by BST
insert); BST ordering + root termination enforced by construction + ssertify.
