# WP-4 CONTRACT (compiled before implementation; immutable for WP-4)

Binding: CURRENT_PHASE=WP-4, PREVIOUS_PHASE=WP-3 (revalidated COMPLETE 2026-09-27:
COMMITMENT_PUBLISHED + TRANSFER_GRAMMAR_FROZEN, zero evaluations, genuine ACCEPT).
Mode: initial execution (never claimed complete; no audit findings supplied).
Authority: WorkPlan.md WP-4 + v0.4.1 spec #4 (scope/objective/baseline/labels/wording),
#12 gates 5-8 + prereg/{liquidity_search_space,predicate_family,h4l_holdout}.yaml
+ schemas/{candidate,counterexample,keep_record}.json.

## Entry predicate
- WP-4-REQ-001: grammar lock + commitment published (zero H4L evaluations) + axis
  frozen + solver stdlib-only (versions recorded, no external binaries); SYN-00
  reproduces LIQ-REG-001 immutably on FLAT(1) before any promotion claim.

## Scope (no H4L/OOD/clean-room-fresh contact, no universality, no ID mutation)
- WP-4-REQ-002: closed grid search 16 P x k 0..6 x C {2,3,4,6,8,12,16,24,32,64} x
  12-profile ladder = 13,440 configs, staged funnel (screen -> dev-full), REG-001 first.
- WP-4-REQ-003: matched rho=FLAT(1) baseline over same space/pipeline/corpora.
- WP-4-REQ-004: dev battery (contaminated-labeled: REG-001 + REG-FAM-001 + motifs,
  seeded structural, deterministic) + validation split (sizes 7,8,10,12,16 x1000 =
  5000, disjoint stream, ID-disjoint masks recorded) + 9 budgeted adversarial engines.
- WP-4-REQ-005: labels RHO_REQUIRED / RHO_NOT_REQUIRED / C_ONLY_REPAIR /
  K_OR_P_REPAIR / MIXED_AXIS_REPAIR / NO_SURVIVOR via baseline/reference comparisons.
- WP-4-REQ-006: promote every eligible survivor (cap 3 only with domination
  certificate); per-candidate frozen identity (schema-required fields; prose says
  29 but schemas/candidate.schema.json requires 30 — the schema governs) + outline
  + eligibility; append-only counterexamples with minimization levels L0/L1.
- WP-4-REQ-007: MSTL-13/14 dev forms + MSTL-23/24 guard notes (no status changes).

## Files (exact paths)
- WP-4-REQ-008: planning/WP4_CONTRACT.md (this file).
- WP-4-REQ-009: python/solver/{predicates.py, legality.py, encode.py, battery.py,
  search.py, promote.py} (stdlib-only; must NOT import holdout/adversary internals).
- WP-4-REQ-010: python/adversary/engines.py (9 engines + run records).
- WP-4-REQ-011: python/independent/config_exec.py (share-nothing violation replay;
  imports independent siblings only, never liquidity/solver).
- WP-4-REQ-012: artifacts/v04/{development,validation,counterexamples}/ (sharded
  results + ID registries + ranking + outlines + identities) + candidates/branchA/.
- WP-4-REQ-013: tests/test_synthesis.py (SYN-00..12) + scripts/{run_phase04.py,
  emit_wp4_runlog.py, test_wp4_mutants.py}.

## Evaluator semantics (exact, count-faithful)
- WP-4-REQ-014: splay mechanics from frozen engines (traces precomputed once per
  episode; tree evolution config-independent); ledger simulated as exact integer
  pools (LATENT/ACTIVE/SPENT) — T7 injects k per A-event when sites nonempty,
  T5 activates min(eligible,cap) with closed-predicate gating, T6 discharges
  min(ACTIVE,need), need=max(y-C*a,0). Violation = legal KEEP with paid<need.
- WP-4-REQ-015: count-simulation proven equal to list-simulation on the fidelity
  corpus (differential SYN test); independent tuple-engine replay of violations.

## Objective order (lexicographic; operationalized, deterministic)
- WP-4-REQ-016: legality -> conservation -> REG-001 satisfied -> dev-zero ->
  validation-zero -> smaller C -> simpler rho (FLAT<ROT, then r asc; "base" = rung r)
  -> smaller k -> simpler P (fewer firing pairs, then ID) -> calculus_id.
- WP-4-REQ-017: attribution decision tree: baseline (P,k,C,FLAT(1)) violates but S
  clean => RHO_REQUIRED; baseline clean => RHO_NOT_REQUIRED; survives only via
  larger C (fails at all smaller C same P,k,rho) => C_ONLY_REPAIR; differs from a
  failing config only in k or P => K_OR_P_REPAIR; else MIXED_AXIS_REPAIR; no
  survivors => NO_SURVIVOR (terminal LIQUIDITY_CALCULUS_REJECTED path).

## Adversarial budgets (frozen table + WP-4 operationalized episode counts)
- WP-4-REQ-018: uniform draws=50000 seed=101; structured 12 families x 4 sizes x
  250 = 12000 seed=102; hillclimb steps=20000 restarts=5 seed=103; anneal steps=20000
  restarts=5 seed=104; genetic pop=100 gens=200 restarts=3 seed=105; rotneigh
  neighborhoods=10000 seed=106; splice splices=5000 seed=107; motif 4 scales x 1000
  seed=108; generalize per_witness=8 seed=109; wall_cap_s=7200 mem_cap_gb=4;
  reduction sorted canonical tie-break smallest (n,H). Engines propose, exact
  evaluator disposes; violations demote + append counterexample.

## Named-test contract
- SYN-00: REG-001 fidelity (P_all,6,2,FLAT(1)) reproduces (2,15,11,10,-1) + Q=2.
- SYN-01: count-sim == list-sim on fidelity corpus (need/paid per KEEP).
- SYN-02: legality gate (illegal episodes rejected: bad mode/key/tree).
- SYN-03: closed-predicate table binds prereg IDs (16/16, semantics spot-checked).
- SYN-04: dev/validation ID-disjointness (registries recorded, zero overlap).
- SYN-05: baseline parallelism (every survivor has matched FLAT(1) record).
- SYN-06: attribution labels exact (decision-tree unit fixtures).
- SYN-07: promotion eligibility + domination certificate (if capped).
- SYN-08: counterexample append-only + minimization L0/L1 + schema.
- SYN-09: determinism (rerun hash match of ranking).
- SYN-10: leakage audit (solver/adversary never import holdout; independent never
  imports liquidity/solver; no H4L/OOD/clean-room contact; AST scans).
- SYN-11: firewall still COMMITMENT_PUBLISHED, unlocks 0, zero evaluations.
- SYN-12: 29-field identity schema conformance for every promoted candidate.

## Mutants (each introduced + killed by scripts/test_wp4_mutants.py)
M-WP4-01 need off-by-one; -02 paid overcount; -03 early-termination skip (missed
late violation); -04 baseline config mismatch; -05 REG-gate bypass; -06 flipped
label; -07 counterexample overwrite (append-only violated); -08 nondeterministic
order in reduce.

## Logging/Path/exit
- STEP 110+ logs + inventory; WP-4 runlog (phase PHASE-09-13); Path WP-4 entry.
- Exit: PROMOTED_SET_SURVIVES_DEV (>=1 + outlines) or honest
  PROMOTED_CANDIDATE_SET_REJECTED / LIQUIDITY_CALCULUS_REJECTED. Resource over
  cap => RESOURCE_LIMIT_NO_CLAIM record, never impossibility.
- MUST NOT: touch H4L/OOD/clean-room-fresh, claim universality/C-minimality,
  mutate IDs, synthesize post-freeze predicates.
