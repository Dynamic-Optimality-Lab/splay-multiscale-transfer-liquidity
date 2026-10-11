# UESINK original source semantics + universal scope (proof stage)

T0 (witness fixture only): `[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],
null]]],[8,[7,null,null],null]],null]` with A_0=B_0=T_0.
KEEP(x): splay x in A and B. DELETE(x): splay x in A; B unchanged; keys never
removed; all accessed keys present. a_t=ceil(d_A/2) pre-access; KEEP
q_t=floor(d_B/2); DELETE q_t=0. A=Σa, Q_B=Σq. Closure = full labeled A/B
equality (root equality insufficient).

Universal scope: the nine-node T0 is a FIXTURE, not a hypothesis. The theorem
ranges over arbitrary ambient BST sizes and admissible reachable pair states.
The operative structural condition is the marked B-ancestor core (union of
root-to-marked-KEEP-key paths, ancestor-closed) having exactly nine nodes
throughout: every genuine KEEP key is marked, so its root path lies inside
the nine-node core and has ≤8 edges, giving d_B≤8 for arbitrary ambient
trees. Recursive subwalks start at actual reachable states (never T0).
c=1 ⇒ the current KEEP changes B's root from the preceding KEEP key
(intervening DELETEs freeze B), hence genuine with path in core. c=0 ⇒
same key, B frozen ⇒ d_B=0. Finite replay corroborates instances; the L1–L7
argument (pure interval arithmetic from H1–H5) is the universal proof.
