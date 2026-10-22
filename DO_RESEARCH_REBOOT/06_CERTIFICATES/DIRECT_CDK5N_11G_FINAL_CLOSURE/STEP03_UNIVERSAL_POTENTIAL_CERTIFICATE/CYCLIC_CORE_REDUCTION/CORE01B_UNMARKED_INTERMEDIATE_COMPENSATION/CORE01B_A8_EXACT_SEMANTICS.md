# CORE-01B A8 Exact Semantics (Gate A4/A6)

A8 (STRICT_SOURCE_REPAIRS.no_intermediate_genuine): for every active
non-terminal event e, NOT(isK[e] AND tisS[e] AND marked[e] AND Bchanged[e]),
where tisS = A-slot isS flag, marked = mu-membership of sidx, Bchanged =
any B-array/root difference bs[e] vs bs[e+1]. Terminal event: genuine marked
B-changing KEEP enforced separately (tisS + mu + chg conjuncts). DELETE and
inactive events: B-identity via b_blend. CONSEQUENCE: the only
B-changing intermediate KEEPs the predicate admits are unmarked-target
ones. No other intermediate restriction exists (A-shadow only constrains
endpoints; H sums A-costs without bounding B-event count; zero-A-cost
B-changing events possible since dd_A=0 does not imply dd_B=0).
