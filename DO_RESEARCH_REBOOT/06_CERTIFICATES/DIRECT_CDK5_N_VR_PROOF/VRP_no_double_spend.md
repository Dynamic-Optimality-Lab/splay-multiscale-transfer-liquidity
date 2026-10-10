# VRP no-double-spend (PROVED — L8 first half: partition)

s≥5 (five genuine keys ⇒ ≥5 KEEP occurrences) ⇒ the t+2 packet indices
(j*..j*+t+1 mod s, t+2≤s) are pairwise distinct (consecutive run of length ≤ s;
t+2=s covers the whole cycle exactly once — valid, no repetition). Partition:
{packet} + singletons — exhaustive, disjoint. Packet reserve spent once; payer
and bridges never recharged as singletons even if K/P-eligible (mandatory;
enforced). Every StepEv in exactly one H_j (disjoint I_j); R_j=2(H_j−c_j)
separates baseline from extra — nothing invented, nothing reused. Seams,
wrap-around packets, and whole-cycle packets all covered by mod-s indexing. ∎
