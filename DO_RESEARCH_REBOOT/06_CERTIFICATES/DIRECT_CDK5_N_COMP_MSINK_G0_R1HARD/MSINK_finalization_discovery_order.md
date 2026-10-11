# MSINK finalization discovery-order record (task F)

1. Two authorized seeds: concat35 = S1W+VRW (35 accesses, closed 64/36/16,
   split@17) and mr33 = MR INC (33 accesses, closed 55/36/16). SHAs:
   concat `7b00897f…`, mr33 `f6476679…` (full SHAs in witness/control JSONs).
2. DELETE-only edits: removal / DELETE-key replacement (k=1..9, k≠orig) /
   insertion (gaps 0..n, k=1..9). Code: `mutants()` in `MSINK_bounded_search.py`.
3. Max six DELETE edits: authorized bound; executed layer is L1 (=1 edit).
   L2 code exists but never ran (`parents_L2.txt` absent both seeds).
4. Length 25–45 enforced at generation (filter in both census branches).
5. Budgets: 477/443 distinct (496/460 tested) per seed ≤250k; total 956 ≤500k.
6. Seed order: concat35 then mr33 (all scripts, census, rescreen, audits).
7. Candidate order: edit-distance asc, parent first-seen, op order
   (removal→replacement→insertion), gap/index asc, key asc. Verified:
   `parents_L1.txt` byte-equal to fresh `mutants()` regeneration (495/459).
8. Source-validity: tuple replay `None` on absent key; exact labeled serial
   closure both trees (pointer + tuple engines cross-checked per access).
9. Banked exclusion: census 4-recognizer screen (AO per-leg; AP/AQ/AR merged,
   unmodified banked modules, witness-ACCEPT harness-validated) + audit
   12 exact membership predicates + pointer-push AS recognizer.
10. Additive exclusion: exact S0-split subset-partition segment analysis
    (16-battery per part incl. relativized H1 domain: 5 genuine keys +
    within-part core9). CONCAT regression: partition [(0,17),(17,35)] with
    flags [['S1'],['VR']]. IN/OUT: splits=[] (see aperiodicity audit for
    interior-repeat treatment).
11/12. First valid IN = concat35-L1-7 (constructed: removal dpos15, verified
    `L1c[7]==IN_CANON`); first valid OUT = mr33-L1-173 (insert D3@gap2,
    verified `L1m[173]==OUT_CANON`). Full predecessor dispositions in
    `MSINK_finalization_order.json`.
13. Early-stop: charter R3 authorizes one IN/OUT pair within maxima budgets;
    both roles frozen at L0L1 → L2 correctly not executed. No verification
    skipped (every L0L1 word has a census disposition; every predecessor of
    each witness has an audit disposition).
14. No adaptive expansion: fixed BFS layers, frozen op order, sha-dedup;
    caps enforced in code.
15. No aperiodicity gate: see aperiodicity audit (PASS). Selection among
    eligibles followed campaign order; the only prioritization (rescreen)
    was superseded by the complete predecessor audit.

No L2 launch, no witness search, no replacement performed by this finalization.
