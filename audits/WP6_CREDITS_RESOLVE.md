# N-FIRST / N-AUG resolution: outcome B both (SUPERSEDED_BY_GC_STATIC)

Date: 2026-09-30 (C40). Status labels exact (§25).

## 1. Inventory (grep-verified, no freestanding theorems exist)

- No `math/theorems/`, `planning/`, or contract file states an N-FIRST or N-AUG
  theorem. The labels denote attempt-families only.
- Sole exact lemma: genesis first-divergence 1:1 (`first_divergence.json`,
  subsequent OPEN "need pool/global E_B-link"). AR-14/15/16 kernel-checked.
- Queued ideas only (`Path.md:1012-1013`): N-AUG exchange, N-FIRST normal form.
- Old formulations and verdicts (reconstruction §6, route_kills):
  global-slack (circular), interval (tenure-cargo 39%), reset/segment (R-link
  dead 1.58), setup-attribution (unattributed 95:2), X-RETURN (FALSE +16,
  conditional tautology), borderline-as-killer (1/126 dead),
  sterilization-strong (FALSE 90/150 +22), residual-rank/Bellman (vaulted
  small-n, dead at scale), SOD-single (dead c*=12), TSRC (dead).

## 2. Downstream-needs audit (§14: prefix counts only, no persistent matching)

- `math/theorems/MSTL-14P.md`: ACTIVE_pre_discharge ≥ need per present KEEP.
  Depends on: ledger semantics (LIQ0-01..10 REVIEWED + kernel parts — engine,
  determinism, boundedness rho, conservation, support, books-split LIQ0-09),
  D2 need≤2e_B (banked), D6 stock (needs GC — OPEN). No N-FIRST/N-AUG edge
  anywhere (no theorem file, no proof file, no contract, no consumer rule).
- D6 = D2 + GC is pure prefix-count arithmetic (AR-13 kernel for the numbers).
- Service at KEEP t consumes prefix-t stock counts (that prefix's D6) +
  ledger semantics; matchings may differ per prefix (each prefix inequality
  independently valid). NO cross-prefix matching consistency needed.
- Verdict: downstream consumes prefix count inequalities + banked ledger
  semantics ONLY. No separate N-FIRST/N-AUG lemma has any consumer.

## 3. Obligation mapping (every genuine content → GC-STATIC or banked unit)

N-FIRST side:
- First-cash funding (e_B=e_0 ≤ 3e_0): first-cash B-events are ordinary B(t)
  vertices, matched cap-3 inside GC-STATIC like all others; the stronger AR
  1:1 fragment stands independently (consistent special case, still banked).
- Subsequent/reshaped funding (pool/marginal/sharing): exactly GC-STATIC's
  assignment (E2/E3/E4 edges ARE the pool/sharing structure, capped).
- Tenure-cargo (+16 X-RETURN witness): cross-key E2/E3 edges (represented).
N-AUG side (flow-construction properties, true by construction given the graph):
- Source identities genuine historical A-StepEvs (vertices = aev ids,
  DELETE-generated included; `build_tagged`/`build2` id assignment).
- Dormancy ≠ new identity (edge absence changes nothing about vertices).
- Re-entry ≠ clone/capacity (re-entry edges reuse the SAME aev id;
  S→a capacity exactly 3 in flow construction).
- Sharing = graph edges (E2/E3/E4/E7); cap enforced per genuine identity.
- Past-only edges (builder construction + C30 causality snapshots).
- Residuals/borderline (+22, crossings, bystanders): tree STATES, not demand;
  B-events (demand) counted in E_B regardless; sterilization-failure cannot
  break event assignment (assignment ranges over events, cap per identity).
- Old war's open_core maps exactly: `stock` = GC counting; `eligible_service`
  (support/provenance: which LATENT each B-event may activate) = matching
  edges. Both reduce to GC-STATIC (+D2). Nothing else is owed.

## 4. Disposition (outcome B both)

- N-FIRST-CREDIT / N-AUG-CREDIT as statements = the §3 properties: corollaries
  AUTOMATIC with GC-STATIC (no independent content; nothing to prove separately).
  Status: OPEN (pending GC-STATIC — conditional, honest).
- Old formulations: stay REFUTED as stated; labels SUPERSEDED_BY_GC_STATIC
  (their genuine obligations live inside GC-STATIC; their machinery stays dead).
- Do NOT revive: exclusive setup ownership, per-key pump attribution, interval
  self-funding, run/tenure budget, X-RETURN, last-safe accounting, strong
  sterilization, residual scalar mode, Bellman/cycles, cash→V=0, local reset,
  per-key residual ownership (all in DO-NOT-RESURRECT).
