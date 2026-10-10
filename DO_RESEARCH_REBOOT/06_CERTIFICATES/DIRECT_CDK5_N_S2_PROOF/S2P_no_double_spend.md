# S2-L7 disjointness + no-double-spend (PROVED — §10)

s≥5 (five genuine keys ⇒ ≥5 KEEP occurrences) ⇒ j*,k=j*+1,l=j*+2 distinct mod s
(consecutive mod s≥5 cannot collide). Partition: {triple} + singletons —
exhaustive, disjoint. Triple reserve spent once; k,l never recharged as
singletons even if K/P-eligible (mandatory; enforced). Every StepEv in exactly
one H_j (disjoint I_j); R_j=2(H_j−c_j) separates baseline from extra — nothing
invented, nothing reused. Witness check: ΣR=42=2(29−8) exact. ∎
