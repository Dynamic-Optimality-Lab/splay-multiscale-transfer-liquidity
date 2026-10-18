# SR02C 0->1 Credit Inequality (REFUTED with exact counterexamples)

Required: DC5 + d(t) <= w with DC5 = R(t)-R(s)-(R_M(t)-R_M(s)),
d(t) = R_M(t)-D(t)+M(t). Falsified: 5 independently verified edges
(violation = lhs-w in {3,7,4,1,5}; weights 2,1,1,3,1; all dmax 5->7).
Mechanism: shallow->deep transitions EXPLODE rank (+3/+4) while C5(s) is
small (balanced regime) and C2(t) is huge (chain regime rank-mass) —
the crossing term d(t) cannot compensate because D(t)>=7 subtracts at
most the depth while R(t) grows unboundedly in mass. Minimal confirmed
case: idx3 (w=3, lhs=4, violation 1). The fixed SR-01 candidate is NOT a
universal vertex potential. No threshold change, no added terms, no
narrowing (decisive failure policy). This refutes the POTENTIAL ONLY;
NonNegCycles(G_star) remains open (a negative POTENTIAL violation is not
a negative graph cycle: all confirmed edges have w>0).
