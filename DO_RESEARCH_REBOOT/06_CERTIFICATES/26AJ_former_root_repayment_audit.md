# 26AJ former-root repayment audit (certificate companion)

## Source authority
- Costs/semantics: `scripts/wp6_coarse_double.py:28-53` (replay: a/q/z branches,
  KEEP-splays-both, DELETE-freezes-B, fixed key set); `wp6_eventflow.py:84-182`
  (`to_ptr`, `splay_A`, `splay_B_push` bottom-up zig/zig-zig/zig-zag;
  `root_key`, `depths_of` via `wp6_adv`).
- Run structure: banked `02_PROVED/C_ZIG_RECONSTRUCTED.md` (same block shape,
  proved for zigs; doubles version proved here, not assumed).

## Gate 1 — block decomposition (universal proof in 02_PROVED doc)
A(γ)=0 ⇒ banked zero-A ⇒ Q=0. Else cyclic leaders + same-key followers
(a=0 ⟺ current A-root; leader roots its key; DELETE touches A only);
≤1 nontrivial B splay per block (first-KEEP-or-none argument);
`A(B_i)=a_i≥1`, `Q_B(B_i)=q_i`, `Σδ_i = Q−2A`. Cyclic boundary by modular indexing.

## Gate 2 — former-root depth lemma (universal proof + falsification probe)
Rotation-case analysis of both engines (final op involves original root by
innermost-first frame consumption + depth counting; old root lands ≤2 in
zig/zig-zig/zig-zag/no-op cases). Probe: 2952 splays, 0 violations, maxdepth 2
(`26AJ_depth_lemma_probe.json`). No counterexample exists in source mechanics.

## Pairing/capacity/degeneracy (exact)
Successor map injective mod m; successors (δ≤−1) never positive ⇒ pairs disjoint;
leftovers nonpositive. m=1 positive impossible under hypotheses (x_1=r_1 vs
nontrivial splay contradiction) — proved, not assumed away. Wraparound pairing
(m,1) covered by modularity. Capacity form needs no extra lemma (same pairing).

## Witness validation (all §12 items)
Diagonal start; present keys throughout (asserted per access); both trees exactly
restored (serial equality); per-access costs match table; leaders all 8; blocks
single-key + ≤1 nontrivial KEEP; deficits [+1,−3,−3,−1,−2,−1,−6,−4]; sole positive
δ=+1 with successor KEEP 1 = former root 1 (root_key verified); former-root depth
2 ≤ 2 (legs[1] dB=2); B-depth max 6; totals 14/9/−19; `replay()` identical.
Records: `06_CERTIFICATES/26AJ/aj_witness.py`, `26AJ_witness_replay.json`.

## Novelty (exact, not grep-only)
Outside zero-A (A=14); outside n≤6 analytic closure (n=7, PIVOT-12); genuine
overflow (block0: 3>2·1, δ=+1 — not q_i≤2a_i ∀i); B-depth 6; ROW/J4-independent
mechanism (no J4 premise anywhere). Not subsumed by C.ZIG (zig-only),
bounded-depth charging, 26AE/26AF ROW identities (different domain), or zero-A.

## Failure protocol (none triggered)
Decomposition semantics hold; depth lemma true; B frozen correctly across
DELETE/follower spans; no shared successors possible (injectivity + sign);
witness valid (no correction needed). No obstruction; no replacement pivot.
