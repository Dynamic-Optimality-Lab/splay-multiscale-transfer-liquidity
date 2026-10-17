# S04_GLOBAL_WEIGHT_INEQUALITY.md — Gate G U15/U16 (F04-29)

Per macro j with A-cost H_j (sum of access a-values) and B-cost q_j
(floor terminal B-depth / 2): low edges carry w_j = 2H_j - q_j exactly
(relation EQ), hence w_j ≤ 2H_j - q_j. High edges carry w_j = 6 - q_j with
H_j ≥ 3, hence w_j = 6 - q_j ≤ 2H_j - q_j. Summing over the macro partition
(which preserves all operations and their costs):

  w(P) = Σ_j w_j ≤ Σ_j (2H_j - q_j) = 2A(W) - Q_B(W).

A(W) = ΣH_j is the total A-cost; Q_B(W) = Σq_j the total B-cost (genuine KEEP
costs; DELETE/nongenuine contribute 0 on both sides). Therefore every W maps to
a closed abstract walk P with w(P) ≤ 2A(W) - Q_B(W). This is the Stage 11F
existence claim (NOT the terminal inequality Q_B ≤ 2A, which needs no further
argument here and is not claimed).
