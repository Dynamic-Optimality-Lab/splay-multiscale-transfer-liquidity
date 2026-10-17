# G01_MIDPOINT_CONTRACTION_THEOREM.md — Phase C C1-C5 (G01-10/G01-11)

E^H_w(s,t) = EXISTS m (E^OM_w(s,m) AND E^MO_0(m,t)) over shared QM vars
(G01_MIDPOINT_CONTRACTION.py; verified by construction + K3/K8 oracle tests).

C1 (expansion): every derived s-t high edge unfolds to its bound midpoint
witness (the EXISTS witnesses its own m by definition).
C2 (contraction): every valid s->m->t passage folds to the same formula
(same conjunction read backwards).
C3 (closed-walk preservation): a closed walk in G cannot consist exclusively of
M vertices (every M has only zero out-edges to O and MM is FALSE; an M-vertex
on a closed walk has an incoming edge, which must come from O since in-neighbors
of M are O (OM) and M (nonexistent)). Replacing each maximal O->M->O segment by
its contracted O->O edge (same endpoints, same total weight w+0) yields a closed
walk in the contracted graph with identical total weight. O-only segments
transfer unchanged.
C4 (reverse expansion): expand each contracted edge with its own witness m
(chosen per edge); O-O edges transfer unchanged; endpoints match by
construction; total weight preserved termwise.
C5 (negative-cycle equivalence): a negative closed walk exists in one iff it
exists in the other (C3/C4 transfer witnesses both directions with equal
weight; emptiness of MM-only cycles proved in C3).
Scope: the equivalence is proved for G_star = full G_AF (closed under the
reduction: contraction of an in-region passage stays in-region; expansion m
witnesses are ordinary fiber states of the same graph).
