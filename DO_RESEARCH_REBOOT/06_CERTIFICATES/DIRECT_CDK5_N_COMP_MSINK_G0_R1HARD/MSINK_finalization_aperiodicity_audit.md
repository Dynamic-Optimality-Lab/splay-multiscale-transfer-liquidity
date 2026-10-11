# MSINK finalization aperiodicity audit (task C) — PASS

## Original discovery predicates (frozen)

Charter `MSINK_four_rule_charter.md` R3/R4 + frozen H1–H6
(`DIRECT_CDK5N_COMP_MSINK_G0_R1HARD/MSINK_frozen_theorem.md`, unchanged):
source-validity (present keys, engine replay); exact labeled A/B closure;
five genuine KEEP keys; nine-node marked B-core at all states; MSINK H1–H6
(role-dependent); complete banked-domain exclusion (17 mechanisms); complete
additive-coverage exclusion (no certified banked closed-segment partition);
frozen deterministic order and budget (2 seeds, DELETE-only edits ≤6,
length 25–45, ≤250k/seed, ≤500k total). **No periodicity predicate exists
anywhere in the frozen contract.** `nsplits`/`npos`/`np` appear in no charter,
theorem, or proof file as eligibility conditions.

## Actually executed predicates

- Census `process_word` (`MSINK_bounded_search.py`): replay-valid, exact
  closure, R5 (5 genuine keys + all-boundary core9), 4-recognizer screen
  (AO/AP/AQ/AR), MSINK predicate. No splits/np filter in code paths.
- Rescreen `MSINK_rescreen.py`: role filter + `nsplits==0` + `np==False` +
  full 16-battery. This is an **audit-order prioritization**, not an
  eligibility predicate: it selects which survivors get pointer-audited first.
- Pointer audit + worksheets: engines, AS (push+snaps), full battery,
  pair-splits, msink recheck. Same original predicates, deeper engines.

## Periodicity-related filtering

None in eligibility. The `nsplits==0`/`np==False` rescreen gates never
rejected a candidate from the campaign: every enumerated word kept its census
disposition, and the final order audit below re-evaluates **all**
predecessors under original predicates with **no** nsplits/np filter.

## Decomposition-impossibility lemma (why S0-splits decide additive coverage)

Claim: a linear closed word (from T0) admitting a partition into ≥2
nonempty parts, each a certified banked closed walk, has a proper S0-split.
Proof: the first part starts at T0; closed ⇒ ends at T0; shorter than the
whole ⇒ proper S0 pair-state repeat. ∎ Contrapositive: `splits==[]` ⇒ no
certified banked additive decomposition exists — regardless of interior
repeats, rotations, or subwalk shapes. Rotated access strings executed from
T0 are different campaign objects with different trajectories, outside the
frozen contract (which classifies linear words from the diagonal start).

## Interior repeats found (reported, not concealed)

- IN (`19ff110a`): pre-closure repeats at (1,17),(2,18),(3,19),(4,20),(5,21),
  (6,22) and (15,32); no S0-split. Loop batteries: [1,17) S1-covered from P1
  (domain 5 keys + core9 hold); [15,32) VR-covered from P15. These are the
  S1/VR-half ghosts (both halves share the D5,D4,K3,K7,D5,K1 prefix). By the
  lemma they cannot host a decomposition (no S0-split exists to anchor one),
  and no banked theorem covers open walks or padded loops. Novelty claim
  rests on the original predicates, never on aperiodicity.
- OUT (`b8b02be7`): 34/34 pre-closure states distinct (fully primitive).
- CONCAT: split@[17], covered partition ([0,17) S1, [17,35) VR) — regression PASS.

## Candidate ordering and first-qualifying selection

Order: concat35-L0, concat35-L1[0..494], mr33-L0, mr33-L1[0..458]
(`parents_L1.txt` byte-equal to regenerated `mutants()` order for both seeds).
- IN: L0 additive-covered (partition [17] PROVED); L1[0..6] all non-closed;
  L1[7] ELIGIBLE. First-eligible = frozen IN. ✓
- OUT: 671 predecessors audited word-by-word (Counter: non-closed 435,
  MSINK-member 164, banked-VR 23, banked-MR 17, banked-S1 12,
  additive-covered-[17] 6, banked-AMG+AMS+MR 5, banked-NP 4, banked-AMG+NP 3,
  banked-AMG+AMS+VR 1); single ELIGIBLE = mr33-L1-173 = frozen OUT. ✓
Evidence: `MSINK_finalization_order.json` (per-word dispositions + loop batteries).

## Census dedup erratum (disclosed)

`cmd_census` did not update the in-memory seen-set inside the generation loop,
so 19 (concat35) + 17 (mr33) words were processed twice (seen.txt 496/460
lines vs 477/443 distinct; survivors.jsonl 420 rows vs 384 distinct).
`process_word` is a pure deterministic function of the word, so dispositions
are identical on reprocessing; enumeration order and earliest-index selection
are unaffected (no duplicate precedes either frozen witness; IN idx7 and OUT
idx173 are first occurrences). Script fixed (`seen.add` in-loop); historical
state preserved as-run. Caps hold on both countings (distinct 477/443 ≤250k;
tested 496/460; total 956 ≤500k).

## Decision

**APERIODICITY AUDIT — PASS.** No post-freeze predicate was imposed; no
candidate was skipped for periodicity; the first qualifying candidates were
selected consistently under the original contract. R3 certified on this point.
