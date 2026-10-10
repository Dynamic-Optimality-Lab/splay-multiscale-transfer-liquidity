# VRP 32-point completeness audit — 32/32 PASS (with proof references)

1. Semantics pinned (hashes in verification JSON) ✓. 2. Keys present/fixed ✓
(assert absent→fail; DELETE never removes). 3. Depths pre-access ✓ (measured
before splay in both engines). 4. Closure labeled-exact, both trees ✓.
5. Prefix/cycle: no prefix in fixtures; theorem is cycle-only by definition ✓.
6. Partition disjoint/exhaustive (each access follows one preceding KEEP) ✓.
7. Seam DELETEs in K3's H=13 interval, counted once (ΣH=A verified) ✓.
8. ΣH=A ✓. 9. Σq=Q_B ✓ (DELETEs q=0). 10. Σc=C_K ✓. 11. Σw=Q_B−2C_K ✓.
12. ΣR=2(A−C_K) ✓ (all machine-checked in verifier output).
13. Baseline H≥c (root-change argument; no-op-tolerant) ✓.
14. Nine-core ⇒ d_B≤8 (marked paths; labels permute) ✓.
15. c=0⇒q=0 (B-root + frozen DELETEs) ✓. 16. w∈{1,2} for positives ✓.
17. Exception (1,0) exact (K5 measured) ✓. 18. H=1 excludes K/P (H≥2 needed) ✓.
19. Maximal scan terminates deterministically (finite s; exact predicates) ✓.
20. One exception ⇒ one relay start (H2 uniqueness) ✓.
21. Bridges w≤0,R=0 (q=0,1,2 exhausted) ✓. 22. Finite-t summation (addition) ✓.
23. Payer ∀q≤3 (w≤1,R≥2) ✓. 24. Relay inequality at worst values ✓.
25. Others via K/P ✓. 26. Overlap-once (fixed H) ✓. 27. t+2≤s distinctness
(consecutive mod-s run; t+2=s covers cycle exactly once) ✓. 28. t+2=s handled
(valid partition, no singletons) ✓. 29. Exhaustive disjoint partition ✓.
30. Telescoping ⇒ Q_B≤2A, arbitrary eligible walks ✓. 31. Novelty retained
(full audit + five REJECTs + no superseder) ✓. 32. Scope excludes full
five-key/universal/DO ✓ (theorem states VR class only).
