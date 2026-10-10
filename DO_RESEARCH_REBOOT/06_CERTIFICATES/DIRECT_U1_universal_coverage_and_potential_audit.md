# DIRECT-U1 technical audit: coverage, potentials, finite evidence

## A–C. Safety, banked math, semantics

coarse-double-branch @88d3007, dirty only DO_RESEARCH_REBOOT; sources
eventflow d7cc806079d5, coarse_double b47019afa261, splay 3a178c131c70,
legacy 20284bbc810a; writes confined; AJ–AS preserved (26AS stays Outcome B).
KEEP/DELETE/a/q/no-op semantics per source; access≡block accounting identity.

## D. Negative controls (authoritative, both engines agree)

C1 sum-potential: T0=(1.(7(6(2.(3.(5(4..).))).))), D4 K1 D3 D6 K1 + D3:
w=−2, G 0→3, residual +1 (needs −2≤−3: FALSE). Banked failure ✓.
M max-potential: T0=(1.(2.(6(3.(4.(5..)))(7..)))), D5 D7 + K7: dA=0,dB=3,
a=0,q=1,w=+1, M 1→1, residual +1 (needs 1≤0: FALSE). Banked failure ✓
(distinct mode: transfer with unchanged max). Neither is a W>0 walk (N10 ✓).

## E–G. Graph formulation, coverage audit, frozen invariant

Pair-graph formulation filed (`DIRECT_U1_pair_graph_definition.md`).
Archive: 11,985 distinct closed positive walks regenerated from the FROZEN
26AS generator (no family change); W>0 count = 0. Selected 1000 per charter
rule; banked-covered 56, potentially-uncovered 944 (all 5 recognizers reject).
NO invariant candidate frozen — obstruction filed instead
(`DIRECT_U1_frozen_invariant_spec.md`): parametric C1-scaling trilemma;
no coefficients invented, none tuned (N11–N13 ✓).

## H–I. Proof/failure + finite-state results

No universal proof (obstruction analysis filed). n=7 BFS: 429 starts,
50,000 states (cap), 194,992 transitions (cap 700k not reached; state cap
hit), truncated (N21 ✓); SPFA longest-path screen: NO positive cycle in
explored subgraph; invariant residuals N/A (no candidate).

## J. Closed-walk classification (U-B certificates)

3 strictly-uncovered walks (26AR-seed insertions, W=−100,−100,−96):
diagonal reachability (banked seed prefix), exact A/B closure, source costs,
cycle engines verified, all 5 recognizers REJECT, AJ/AK/AL-G/AM-G analytic +
AL-S/AM-S via banked containment + AN via AO-Type-I-exhaustiveness +
baselines (n=16, dB=6, A>0) — full exclusion
(`DIRECT_U1_uncovered_closed_witness.json`). Coverage gap, NOT
counterexample (N25 ✓). No positive-weight walk found anywhere (U-D: none).

## Controls honored

N1–N32: no future-info, no bank, no oracle tables, no double-counted L1, no
restricted-Hall overuse, exact reachability/closure, no finite-to-universal
leap, AJ–AS unchanged, ZIG banked, no DO claim, no U2/26AT, no new mechanism
gate (§19 diagnostic only, no three-group theorem invented).
