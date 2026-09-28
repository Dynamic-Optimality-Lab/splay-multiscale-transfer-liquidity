# WP-5X CONTRACT — exhaustive successor re-execution (all 6,099 eligible admitted)

Name: WP-5X (used consistently in code/logs/tests/artifacts).
Binding: successor of WP-5; consumes frozen WP-4 ranking + published H4L reveal.
Authority: WorkPlan.md WP-4/WP-5 + v0.4.1 spec #4/#8 + prereg + schemas + this file.
Historical WP-5 (PROMOTED_SET_REJECTED) is immutable and is never rewritten.

## Admission (no cap, no simplicity filter)
- WP-5X-REQ-001: admit EXACTLY the ranking.json entries with zero dev violations
  (rank[0]==0) that survived screen per screen_results.json. Assert count==6099 or
  STOP FAIL-CLOSED. `promoted`/`dominated` fields are ranking metadata only.
- WP-5X-REQ-002: freeze canonical ordered-set hash over exact frozen identities
  (config ID, P/k/C/rho, predicate/rho hashes, rank key, label, calculus identity);
  schema-validate every identity; zero mutation.

## Freshness honesty
- WP-5X-REQ-003: H4L is REVEALED. X2 reports REVEALED_H4L_EXHAUSTIVE_REPLAY, never
  fresh. Fresh confirmation requires the new H5L holdout (§7 below) or nothing.

## Pipeline (fail-fast; only a failing gate removes a candidate)
- X0 population reconstruction + freeze (above).
- X1 known-counterexample regression: REG-001 (n=28) + n192 OOD wealth witness
  (from ce_0000, T0 embedded), n192-first scheduling; first-kill witness preserved.
- X2 revealed-H4L replay in immutable published order (shard/file/line order),
  factored traces (8A.A, equivalence-proven), equivalence-class execution (8A.C),
  fail-fast with independent confirmation (8A.B), sharded checkpoints/resume.
- X3 clean-room agreement: FULL-BANK primary/clean-room per-KEEP equality for every
  X2 survivor (fail-fast on first mismatch; multiprocess; no sampling).
- X4 large-n battery unchanged (9 sizes x40).
- X5 OOD battery unchanged (4 sizes x2000, includes the known n=192 killer).
- X6 EXHAUSTIVE_SURVIVOR_SET (no cap) or EXHAUSTIVE_ELIGIBLE_SET_REJECTED.
  Finite evidence only; §13 claim boundary applies verbatim.

## H5L fresh holdout (§7; only if X5 survivors exist)
- Freeze ordered survivor set + hash; freeze generator/evaluator bytes by hash
  (reuse frozen h4l_generate.py unmodified with fresh seed; H5 contract committed
  pre-generation); 7 sizes x1000 = 7000, fresh secret dir, bank_id H5L; commitment
  committed BEFORE any evaluation; zero-contact assert; own lifecycle file
  (artifacts/v04/wp5x/h5_firewall.json, unlock<=1, no H4L-firewall contact);
  reveal once; evaluate EVERY frozen survivor; keep all; preserve failures.
- If no X5 survivors: H5 not applicable (nothing to test), NOT "required".

## Engineering (8/8A/9/10)
- Streaming per H4L shard; bounded memory; deterministic order; atomic checkpoints;
  compact pass records (counts/hashes); full records for kills/disagreements.
- Factored traces proven on regression sample vs end-to-end exec_full first.
- Equivalence key: (k, C, rho, per-event firing vector); representative execution +
  member list + basis + verification hash recorded per class-use.
- Multiprocessing (spawn-safe), benchmarked 1/2/4/6/8, conservative count.
- No semantic changes for performance; no heuristic pruning; no GPU rewrite.

## Failure attribution (§11)
- Panel on killing episode: single-axis escalations (k->6, C->next rung, rho->max,
  P->P_all); classify STOCK / LIQUIDITY / PREDICATE / DEMAND / MIXED / UNKNOWN.
  Pool traces (LATENT/ACTIVE pre/post, created/activated/spent, a/y/need/paid/
  margin, mode/class) preserved for kills.

## Tests (§14): tests/test_wp5x.py
- Kill implementations that: reinstate cap-3; filter by promoted; drop dominated;
  admit !=6099; regen IDs; alter ranking.json; claim H4L fresh; dominance-skip;
  stop-after-N; mutate params; omit n192; pass on disagreement; wrong resume offset;
  dup/omit shard; merge identities; reorder holdout; create H5 after outcomes.

## Provenance (§15): starting/final HEAD, files, commands, counts, population hash,
- stage counts, survivor hash, counterexample count, H4L=REVEALED, H5 status, push,
- remote equality, tree state. Append-only; WP-5 history untouched.
