# RC-01 Core-Balance Identity (proved; algebraic)

For closed C = e1...en with a fixed valid witness per occurrence:
sum_e delta_rho(e) = 0 by telescoping (endpoint-defined). Split by the
S/U occurrence partition: sum_U delta = -sum_S delta. Since S occurrences
satisfy delta <= 0 (conditional theorems), sum_U >= 0. Immediate
consequence: any closed walk containing an S strict descent contains a U
occurrence with positive core growth. This is arithmetic + CORE-01 lemmas
only. It does NOT imply w(C)>=0, does not bound U weights, does not pair
gains to payments, and does not exclude flat negative cycles.
