# PP_266_REPRESENTATIVE_THEOREM.md — PROVED (import + port adaptation + ledger)

## Statement
Every relevant arbitrary-fringe original low-cost transition admits a source-correlated canonical representative with at most 266 fringe keys per gap (total ≤ 9 + 10·266 = 2669 keys). T = 266 is discharged as a theorem obligation, not assumed.

## Imported base (Stage-10, UFRL_REPRESENTATIVE_CONSTRUCTION.md + UFRL_extract.py)
E1 depth-6 prefix K exact (|K|≤127); frontier F nonempty subtrees (|F|≤128). E2 positions recorded. E3 hidden-S stays in frontier. E4 S-less nonempty frontier ⇒ min-key witness. E5 E=K∪S∪witnesses, |E|≤264, non-S ≤255. E6 V_i per gap with |V_i|=min(|G_i|,266) — feasible since |E∩G_i|≤255≤266 (both cases verified in code). E7 prefix exact; per-hole balanced rebuild over retained keys; empty stays empty; attachments kept ⇒ rebuilt contents at depth ≥7. E8 |U*|=9+Σ|V_i|≤2669. Preservation L1-L8 (2,305 general + 180 adversarial + 30,773 B-side fuzz, 0 mismatch): targets/pivots retained (L1-L2); descents/costs/H agree (L3); same rotation cases, rigid blocks (L4); displacement bound, holes inert, top-3 from ≤6 (L5); shadows src/dst (L6); inventory counts min(n,266) (L7); zero-DELETE sound; B-compat: marked ancestors core ⇒ retained, q/projected-successor preserved (L8+§9). Spot re-verified this campaign: 30/30 per-gap min(n,266), non-S E ≤255.

## Port/atom adaptation (new)
The E1 prefix cut IS the §4.1 port cut (depth 6, ≤127 exposed, ≤128 ports); E4 witnesses ARE the port status witnesses (one per S-less occupied port); E7 rebuild contents at depth ≥7 ARE port interiors. The atom inventory refines holes by V-order without changing counts (L7: min(|V_i|,266) per gap; atoms only redistribute within (gap,port) cells). Destination representative shares U* (same key set); destination configuration = same-macro replay (L3-L4: same descents, same rotation cases on representative); ports ride rigidly (PP-03); destination validity with identical ξ measured 800/800 (PP_DST_SHARED_TEST.json).

## 13-item ledger (why every indispensable representative is counted)
1. S identities: E3+E5, kept exactly, never thinned.
2. Marked identities: subset of S.
3. B-core identity/configuration: §9 projected core shape.
4. A exposed causal prefix: E7 prefix exact (≤127 structural nodes).
5. Strict inorder of exposed keys: prefix exactness implies order exactness.
6. Occupied/empty A-ports: E4 witness rule (occupied certified by hidden-S or min-key witness); E7 empty-stays-empty.
7. Relevant B-fringe occupancy: L7 min(|V_i|,266) — zero stays zero (occupancy exact); saturation only merges positive counts above 266.
8. Accessed key identities: L1 (targets at depth ≤4 <6 ⇒ in K).
9. Primitive source rotations: L4 (same cases, verified step-type sequences identical).
10. Exact H: L3 (a-costs agree ⇒ sums agree).
11. Exact q: §9 B-compat (projected core shape; marked B-depths/q verified preserved over 30,773 cases under Control-F discipline: only projected outcomes compared, full-tree equality never claimed).
12. Source/destination boundary shadows: L5-L6 (top nodes from initial ≤6; S/hole/root/inventory components).
13. One consistent src/dst representative: shared U* + same-macro replay + rigid port transport (PP-03/PP_DESTINATION_SHARED).

## Why 266 suffices (not numerology)
E6 feasibility is exact: retained-in-gap |E∩G_i| ≤ |E_non-S| ≤ 255 ≤ 266 holds for every gap (both code branches verified). The 11-slot headroom per gap covers B-fringe interface occupancy witnesses and source-legal zero-cost spares (root accesses a=0 target exposed nodes already in K; E3/E4 are cost-pattern exceptions H=1,q∈{3,4}, not extra keys; DELETE targets in low-cost macros satisfy d≤4 ⇒ in K by L1). Saturation binds only above 266, where min() preserves occupancy (item 7) and all cost/shadow observables depend only on retained structure (items 8-12). The bound is per gap (hence total ≤2669), stronger than any total-266 reading.

## Gate PP-09: PASS. (T-layer: UFRL_extract reference implementation + 30/30 spot; full 33k fuzz by Stage-10 reference.)
