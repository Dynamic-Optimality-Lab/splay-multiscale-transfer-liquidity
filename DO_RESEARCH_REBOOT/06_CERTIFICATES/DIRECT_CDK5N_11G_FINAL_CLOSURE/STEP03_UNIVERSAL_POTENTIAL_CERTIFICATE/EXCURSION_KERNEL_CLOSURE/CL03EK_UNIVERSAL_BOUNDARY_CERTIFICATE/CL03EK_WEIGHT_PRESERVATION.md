# CL-03EK Weight Preservation (exact, both directions)

Contraction (frozen -> Q_all/Q_min): macro edge weight = sum of its
excursion edges (additivity); 00 edges kept with identical weights.
Expansion (Q_all/Q_min -> frozen): substitute each macro by its defining
excursion edges (attaining excursion for K-edges under H3); 00 edges kept.
Both directions preserve total signed weight exactly (finite sums,
commutativity/associativity only). No rounding, no approximation, no
dropped families, no merged parallels (identity of parallel macros kept
distinct in Q_all; kernel may share endpoints with different attaining
witnesses — recorded, not collapsed). Zero cycles and repeated vertices
handled by the same substitution (walk combinatorics only).
