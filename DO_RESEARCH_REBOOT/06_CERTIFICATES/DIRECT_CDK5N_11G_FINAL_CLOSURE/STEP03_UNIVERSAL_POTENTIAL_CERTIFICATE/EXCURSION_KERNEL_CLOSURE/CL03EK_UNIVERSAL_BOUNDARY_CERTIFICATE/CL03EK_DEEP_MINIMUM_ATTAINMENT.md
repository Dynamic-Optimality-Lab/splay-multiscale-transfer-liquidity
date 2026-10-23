# CL-03EK Deep Minimum Attainment (EK-2: PROVED, conditional on H3)

Assume NonNegCycles(G_D). For shallow u,v let E(u,v) be complete deep
excursions u->..->v and K(u,v) = inf weight (or +inf if empty). CLAIM:
every nonempty E(u,v) attains its minimum. Proof: take any P in E(u,v)
with a repeated deep vertex (interior repetition); the subwalk between
repetitions is a deep-only closed walk, hence weight >= 0 by H3; excising
it yields a strictly shorter excursion with weight <= w(P). Repeat until
no deep vertex repeats (terminates: finite vertices, each excision removes
>=1 edge). The resulting simple-interior excursion has weight <= original.
Since only finitely many simple-interior walks exist (finite vertex set),
the infimum over E(u,v) equals a minimum over this finite subset (nonempty
because excision preserves endpoints/membership). No computability claim;
no bound on which excursion attains it.
