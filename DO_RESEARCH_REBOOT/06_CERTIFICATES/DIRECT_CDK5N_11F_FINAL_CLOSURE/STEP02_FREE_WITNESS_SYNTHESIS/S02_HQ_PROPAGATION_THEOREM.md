# S02_HQ_PROPAGATION_THEOREM.md — exact H/q inference (Gates C2/G09)

Production law `w = 2H - q` is used as a derivation rule, never an assumption:
q is measured from the simulated terminal B-depth (`2q <= d < 2q+2`, the relation's
own constraint shape), then `H = (w+q)/2` with integrality + `0 <= H <= 2`
admissibility (relation bounds). No (H,q) pair is taken from any fixture; the
BFS enumerates all (H,q) consistent with each B-word, so case coverage is complete
over the word space. Measured derivations: E3 (H=1,q=3), E4 (H=1,q=4), plain
(H=1,q=0), delkeep (H=2,q=0), high (q=3,w=3=6-q).
