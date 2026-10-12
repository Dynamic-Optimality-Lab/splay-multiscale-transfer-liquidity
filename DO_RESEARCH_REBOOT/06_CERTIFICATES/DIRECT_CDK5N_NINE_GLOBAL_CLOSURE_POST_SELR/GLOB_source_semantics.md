# GLOB original source semantics (§4)

Key universe K finite ordered. A_0=B_0=T_0 (admissible diagonal).
KEEP(x): splay x in A and B. DELETE(x): splay x in A, B unchanged.
No physical removal. Every target present (absent ⇒ ReplayError, fail-closed;
engines: wp6_eventflow.splay_A/splay_B_push + independent splay.trace, cross-checked per access).
Pre-access costs: a=ceil(d_A/2); KEEP q=floor(d_B/2); DELETE q=0.
A=Σa, Q=Σq. Closure = full labeled A/B equality (root-only insufficient);
reachable via actual ops from diagonal init. Marked B-core = ancestor-closed
union of B-root→genuine-KEEP-target paths; complete nine-core ⇒ d_B≤8 for
genuine KEEPs (path length ≤8 edges). Ambient may hold unmarked nodes; no
inference about them without proof.
