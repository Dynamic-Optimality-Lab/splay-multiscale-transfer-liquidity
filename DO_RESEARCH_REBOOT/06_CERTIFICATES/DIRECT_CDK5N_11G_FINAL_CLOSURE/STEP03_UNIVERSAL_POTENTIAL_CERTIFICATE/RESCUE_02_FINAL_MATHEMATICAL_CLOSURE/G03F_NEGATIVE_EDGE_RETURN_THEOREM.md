# G03F Negative-Edge Return-Path Equivalence Theorem

Let G = G_hat be the frozen directed weighted multigraph (parallel edges with
distinct weights/provenance retained; zero edges retained; contracted high
edges retained; disconnected components allowed).

Theorem. NegativeCycle(G) iff exists a negative edge u -(-r)-> v (r>0) and a
directed path v ~~c~~> u with c < r.

Proof. (=>) Let C be a negative directed closed walk. If C has a repeated
vertex, split C at the repetition into closed subwalks C1, C2 with
w(C)=w(C1)+w(C2); some piece is negative; repeat until simple (finite).
A simple negative directed cycle has >= 1 edge; some edge has negative weight
(else sum >= 0), write it u -(-r)-> v. The remainder of the cycle is a
directed path v~~c~~>u with -r+c = w(C) < 0, i.e. c < r.
(<=) Given u -(-r)-> v and v ~~c~~> u with c<r, concatenation is a closed
walk of weight -r+c < 0. If it self-intersects, split as above; some simple
piece is negative. Parallel edges: the argument uses only existence of the
named edges. Zero edges: subsumed (c<r with r>0 allows c<=0). Contracted
high edges: ordinary edges of G_hat, covered. Disconnected graphs: paths
are within one weak component; the statement is per-component valid. QED.

Corollary. To refute NonNegCycles it suffices to exhibit one negative edge
plus a cheaper return path; to certify it one must exclude such returns for
EVERY negative edge (all families: low -4..-1, anomalous high, unresolved -3
kept conditional). No liftability hypothesis is used; an abstract-only
negative cycle refutes the graph premise but not the terminal inequality.
