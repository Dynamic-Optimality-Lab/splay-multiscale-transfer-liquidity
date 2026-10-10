# S2-L5 triple payment (PROVED — §8: worst allowed values)

w_*+w_k+w_l ≤ 1+0+1 = 2 (exception w=1; successor w≤0; second w≤1 at q≤3).
R_*+R_k+R_l = 0+0+R_l ≥ 2. Hence w_*+w_k+w_l ≤ R_*+R_k+R_l. Joint charge, once;
covers successor-positive (w_k=1 with R_k≥2? — no: successor has R_k=0; the
pair (w_*≤1, w_k≤0-or-1?) — precisely: w_k≤0 by H3 (q≤2), so the only positive
debt the pair can carry beyond the exception is w_l≤1, paid by R_l≥2. If a
reading allowed w_k=1 it would violate H3; H3 caps q_k≤2 so w_k≤0 always.)
Worst-case arithmetic uses frozen bounds, never witness values. ∎
