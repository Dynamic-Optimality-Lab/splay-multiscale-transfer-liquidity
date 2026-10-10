# S1-L6: disjointness, no-double-spend, telescoping (PROVED)

s≥5 (five genuine keys) ⇒ j*≠k=j*+1 mod s. Partition: {pair} + singletons —
exhaustive, disjoint. Pair paid once (R_*+R_k); successor never recharged;
singletons use own reserves; every StepEv in one interval (disjoint I_j);
R_j=2(H_j−c_j) separates baseline (2c_j... precisely baseline 1 StepEv per
c_j=1) from extra credit — nothing invented. Sum: Σw≤ΣR ⇒ Q_B−2C_K≤2(A−C_K)
⇒ **Q_B≤2A**. Independence: no dependence on outside-core size (marked paths),
length (finite sums), DELETE count (exact H), KEEP order (cyclic), diagonal
start (cycle-only), AJ–AS packets (none used), enumeration/potentials/lifting
(none used). ∎
