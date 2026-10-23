# DH-01 High-to-Low Substitution (OPEN; exact criterion stated, no instance proved)

Required: for every deep high edge e (u->v, w_H), a low-only deep path
P_e with w(P_e) <= w_H(e) (same endpoints, all vertices deep). Status:
NO such path constructed for any high edge (would require ssertify/Z3
search: forbidden here). Obstructions identified: (a) decomposition needs
intermediate deep states with A-shadow compatibility (unverified);
(b) low witnesses for the pieces must exist with total weight <= w_H
(unverified); (c) the natural candidate (expand OM splay into low
rotations) fails weight-parity (a low splay of the same key costs
2H-q with H from A-events, unrelated to the high 6-q); (d) deep-only
restriction may strand the return (no verified deep connector).
The criterion is exact and falsifiable (one certified dominating path
per high edge would advance it); it is not proved, refuted, or
approximated here.
