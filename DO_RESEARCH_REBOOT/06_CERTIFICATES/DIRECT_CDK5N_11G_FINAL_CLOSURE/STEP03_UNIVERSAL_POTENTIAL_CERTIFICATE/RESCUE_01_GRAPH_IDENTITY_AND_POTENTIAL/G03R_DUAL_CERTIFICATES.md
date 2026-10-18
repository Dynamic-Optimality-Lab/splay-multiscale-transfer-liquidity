# G03R Dual Certificates

Method: exact rational rank/nullspace (Fractions), feasibility over Q (Z3
Reals, exact), unsat-core extraction where applicable, independent
Fractions re-verification of any lambda. Result: both corpora rationally
FEASIBLE, so no dual vector (lam >= 0, lam'D = 0, lam'w < 0) exists — there
is no affine impossibility proof to extract from these 78 edges. The earlier
round-4 unbounded-UNSAT observation applied to a superseded 29-edge set and
is reported as a recorded observation, not a re-verifiable certificate. The
dual-certificate machinery (`G03R_AFFINE_DUAL_CERTIFIER.py`) is retained: any
future infeasible corpus yields a minimal core automatically.
