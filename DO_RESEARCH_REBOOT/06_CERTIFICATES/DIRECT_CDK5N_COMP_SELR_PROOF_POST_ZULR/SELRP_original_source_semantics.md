# SELRP original source semantics + arbitrary ambient scope

T0 (witness fixture only):
[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null].
A_0=B_0=T_0. KEEP(x): splay x in A and B. DELETE(x): splay x in A, B
unchanged. No physical removal. Every target must exist (absent-key
replay raises ReplayError: fail-closed). Pre-access costs: a=ceil(dA/2);
KEEP q=floor(dB/2); DELETE q=0. A=Σa, Q=Σq. Closure = equality of
complete labeled A/B states (root equality insufficient). Universal
scope: arbitrary admissible ambient BST sizes/lengths satisfying the
marked-core condition (ancestor-closed root→marked-key path union has
nine nodes); for genuine KEEPs d_B≤8, q≤4 definitionally. No
generalization beyond frozen H1.
