# CL-01 Excursion Deficit Identity (PROVED, exact algebra)

With alpha=C5, beta=C2, Phi = alpha + g*(beta-alpha), delta = beta-alpha
= R_M - D + M: for edge (s->t,w), r(e) = w-(Phi(t)-Phi(s)).
Guard cases: 00: r = w-DeltaC5; 11: r = w-DeltaC2; 01: r = w-DeltaC5-d(t);
10: r = w-DeltaC5+d(s). For excursion P = u0-01->v1-11->...-11->vk-10->u1,
R(P) = w(P)-[alpha(u1)-alpha(u0)] telescopes to
R(P) = r_entry + sum r_i^11 + r_exit (entry: w-[beta(v1)-alpha(u0)];
interior: w_i-[beta-diffs]; exit: w-[alpha(u1)-beta(vk)]),
by exact cancellation of interior beta terms. Closed-walk identity:
w(C) = sum_{e in C} r(e) holds for ANY single-valued vertex Phi
(telescoping), refuted or not — algebra, no positivity assumed. Expanded
01-coupling: DeltaC5 + d(t) = R(t)-R(s)+R_M(s)-D(t)+M(t) (verified
symbolically by expansion; used to state H2 precisely).
