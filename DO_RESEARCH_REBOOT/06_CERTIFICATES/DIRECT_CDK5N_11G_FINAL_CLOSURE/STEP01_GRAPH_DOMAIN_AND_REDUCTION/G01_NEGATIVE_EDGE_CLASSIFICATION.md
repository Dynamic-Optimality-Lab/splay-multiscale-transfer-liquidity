# G01_NEGATIVE_EDGE_CLASSIFICATION.md — Phase D (G01-13/G01-19)

Only the low OO relation can contribute negative weights among DECIDED edges
(w in -4..-1 all low; OM out-of-range UNSAT only at w=-4, others SAT-or-UNKNOWN
but all with q >= 5 outside the genuine 0..4 range; MO is zero; MM absent).
A negative closed walk must therefore contain a negative low edge (proved for
the decided fragment; out-of-range OM edges are retained, not deleted, so the
general claim awaits Step-02 classification). The 10 required cycle classes are
defined with examples from the small-graph oracle + production witnesses; no
class is asserted empty or universal beyond evidence. Positive edges are never
dropped (contraction preserves them; sector partition preserves them).
