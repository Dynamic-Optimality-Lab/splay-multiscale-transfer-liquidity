# RC-01 Structural Packet Construction (ATTEMPTED; blocked at transport)

Attempt: q units = B-depth layer pairs of the accessed key's ancestor
chain (source-derived objects: consecutive ancestor pairs along the
witnessed splay path, q = floor(d/2) of them). Payments: 2H_e A-event
layers per low edge, 6 units per high edge (formal capacities). Local
matching within a single edge is arithmetically possible but meaningless
(it restates w = capacity - debt). Cross-edge transport attempted via:
(a) vertex-carried packets — REFUTED as a general mechanism: debt is
history-dependent (same vertex reachable with different outstanding needs
along different histories; the 147-field interface carries no history),
so no vertex function can own all packets; (b) history-carried packets
along fixed witnessed walks — well-defined per walk but the required
uniform invariant (payment forced before closure) does not follow from
endpoint equality alone, since zero/negative-cost restoration steps are
admissible and q'-credits offset H'-costs in the weight formula.
CONCLUSION: no justified cross-edge ownership rule found; charging stops
at the interface. (Gate D1-D5 attempted; D: no valid injection constructed.)
