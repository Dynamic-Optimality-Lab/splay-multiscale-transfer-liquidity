# GAPMULTI01 — Exact failure of literal shared hidden-core splitting

Status: **REFUTED—EXACT** for the proposed deterministic literal port
completion bridge. M3 on multiple positive gaps remains **OPEN**.

At mu=341, sigma=(1,1,0,...,0), two full original LOW witnesses have
identical complete source states and identical complete destination
states. Both execute terminal KEEP6 with H=1, actual q=2 and weight 0.
Both original roots are TRUE and independently replayed. Original low
DAG: 1400081 nodes; audit CPU 12.016 seconds.

At the shared source, root S2 has a visible anonymous left child f,
whose two children are opaque ports. The same right core subtree and
the same B state are used in both witnesses. In witness0, f is in gap0;
its left port contains no S key, its right port contains S0 and S1.
The gap1 unit is hidden there. In witness1, f is in gap1; its left port
contains S0 and the hidden gap0 unit, and its right port contains S1.
All original mu, sigma, alpha, B child refs/kinds and lo/hi agree.

Thus the hidden S bills are respectively ([],[0,1]) and ([0],[1]).
The fixed-gap0 and fixed-gap1 literal completion images differ, although
the full shared state cannot distinguish the witnesses. This disproves
the first required identity for directly extending the fixed-gap
completion mechanism. It does not disprove an allocation-invariant or
branch-robust potential, and two copies of the same weight0 edge do not
give a negative cycle.

BEFORE: a multi-gap extension needed deterministic hidden-S port sets.
RESULT: exact original equal-state witness pair refutes that premise.
AFTER: stop this completion route as required by PRE_EXECUTION.md.
NET ORIGINAL THEOREM ADVANCEMENT: 0 from this obstruction; strategic
elimination only. The separately proved single-gap families survive.
No additional coordinate, private observable or graph modification is
authorized or introduced. No original negative mixed cycle is certified.
R1–R4 and the high h=0 correction are preserved. A fresh multi-gap
mechanism needs its own four-rule gate; an unknown completion existence
premise cannot be treated as a proof.
