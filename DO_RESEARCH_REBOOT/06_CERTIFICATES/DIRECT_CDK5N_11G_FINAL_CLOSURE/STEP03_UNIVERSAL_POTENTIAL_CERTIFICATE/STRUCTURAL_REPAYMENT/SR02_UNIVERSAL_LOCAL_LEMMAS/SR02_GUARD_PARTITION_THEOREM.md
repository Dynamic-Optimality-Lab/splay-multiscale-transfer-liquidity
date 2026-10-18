# SR02 Guard-Partition Theorem (proved: pure algebra, no solver)

Phi(s) = C5(s) + g(s)*d(s), d = C2-C5 = R_M - D + M (expand: C2-C5 =
(R-D+M)-(R-R_M) = R_M-D+M ✓). Edge (s->t,w), gs=g(s), gt=g(t):
00: Phi(t)-Phi(s) = C5(t)-C5(s) =: DC5.
11: = C2(t)-C2(s) =: DC2.
01: = C2(t)-C5(s) = DC5 + d(t).
10: = C5(t)-C2(s) = DC5 - d(s).
Single-valuedness: Phi(s) depends only on s (guard is vertex predicate);
telescoping over closed walks is arithmetic identity (sums to 0), so the
ENTIRE universal content is the four edgewise inequalities. Verified
numerically on all 166 stored grounded edges (SR02_GUARD_CASE_CHECKER).
