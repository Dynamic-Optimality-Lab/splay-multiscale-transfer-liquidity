# CL-03EK Excursion Quotient Theorem (EK-1: PROVED)

Definitions: L/TYPE partition per CL-01 (shallow/only-deep/mixed); maximal
deep excursions (01...10 with 11-interior, empty interior allowed);
Q_all with L vertices, all 00 edges, and one macro edge per excursion
(w = excursion total; parallel macros preserved). THEOREM:
NonNegCycles(G_hat) iff NonNegCycles(G_D) or NonNegCycles(Q_all).
Proof (=>): negative closed walk is either deep-only (in G_D) or contains
a shallow vertex; rotate to start there; replace each maximal excursion by
its macro (same endpoints, same total by additivity); 00 edges kept;
result is a closed walk in Q_all with identical weight <0, hence contains
a negative directed cycle (finite closed walk decomposes into simple
cycles; one must be negative). (<=): a negative deep cycle is already a
negative frozen cycle; a negative Q_all closed walk expands macro-by-macro
(each macro IS its excursion edges) into a frozen closed walk of equal
weight, containing a negative cycle. All lengths/repeats/parallel/zero/
high/abstract-only/mask cases covered (no property beyond endpoint
equality and weight additivity used).
