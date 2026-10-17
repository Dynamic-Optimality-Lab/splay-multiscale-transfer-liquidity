# G01_WEIGHTED_EDGE_INVENTORY.md — Phase B audit (G01-07/G01-08)

Complete inventory: OO x {-4..4} (9, all SAT-grounded in Step-02/03);
OM x {-4..6} (11 structural; verdicts: -4 UNSAT-certified; -3 UNKNOWN-timeout
(obstruction recorded); -2,-1,0,1 SAT (retained); 2..6 SAT with marked-q
correspondence); MO x {0} only (single E_mt; other w absent by construction);
MM none. Every edge family has: sort pair, weight, witness list (audited bound),
mask/signature compatibility (EQ conjuncts verified present), q constraints
(w=6-q on OM), source/destination root constraints, source proof (grounded
witnesses for realized edges; UNSAT/timeout records otherwise). No unapproved
transitions (all from the frozen relation constructors).
