# WP6 Cold Reconstruction — full repo / proof-state recovery

Sealed against HEAD `f44982c` on branch `wp5x-k6c2-specialized`.
Companion machine-readable ledger: `audits/WP6_COLD_RECONSTRUCTION.json` (same directory).
Status vocabulary: `PROVED_AUTHOR` / `PROVED_KERNEL` / `FINITE_EVIDENCE` / `REFUTED` /
`OPEN` / `BLOCKED_EXTERNAL` / `SUPERSEDED`. Finite evidence is NEVER a theorem.

---

## 1. Repository / branch / HEAD / remote / cleanliness

- Repo: `Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity` (verified via `git remote -v`).
  - `origin  https://github.com/Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity.git (fetch/push)`.
- Local dir: `splay-multiscale-transfer-liquidity-k6c2` (verified).
- Branch: `wp5x-k6c2-specialized` (verified via `git branch --show-current`).
  - Tracking: up to date with `origin/wp5x-k6c2-specialized` at reconstruction time.
- HEAD: `f44982c8791cff71d952597b7bd9c9540c1cbab1` — matches the prompt's
  "latest known sealed commit `f44982c`" EXACTLY. Message:
  `E3 ordered-family: not nested (55% incomp), expands +0.6/step (triple-motion refresh); UNPROVED`.
- Cleanliness: tree clean EXCEPT one untracked file, `scripts/wp6_breaking.py`
  (7495 B, created 2026-09-29 22:57:55, `??` in `git status --porcelain`).
  It is a WP-6 STEP BR-00 breaking-shape hunt (shrink+overflow+thin E2E4) that was
  NEVER committed and is NOT part of the sealed state. Left untouched in place.
- Git safety observed: stayed on `wp5x-k6c2-specialized`; no checkout of master/main,
  no merge, no history rewrite, no artifact deletion. Reconstruction ADDS exactly two
  files under new top-level `audits/` (which did not previously exist).

## 2. Current target theorem stack

Surviving chain (present-domain salvage of the broad MSTL program):

```
MSTL-14P -> MSTL-15P -> MSTL-17P -> MSTL-18P -> MSTL-19 (bridge, BLOCKED_BY_SOURCE/L2)
```

- `MSTL-14P` (`math/theorems/MSTL-14P.md`): synchronous KEEP repayment on
  `PresentLegalPairInstance`: `ACTIVE_pre_discharge >= need` at every legal present KEEP,
  `need = max(y-2a,0)`, `a = d_A(x)+1`, `y = d_B(x)+1`.
  Status: **UNPROVED / NO_WITNESS** (`math/proof_status.json`).
- `MSTL-15P`: global integrability on present domain. UNPROVED / NO_WITNESS.
- `MSTL-17P`: universal present Pair Access `Splay(Y,T)+E_m-E_0 <= C*Splay(X,T)`, `A(n)=0`. UNPROVED / NO_WITNESS.
- `MSTL-18P`: telescope / approximate monotonicity, `A(n)=0`, present domain. UNPROVED / NO_WITNESS.
- `MSTL-19`: exact Levy–Tarjan bridge, NO P-variant, `BLOCKED_BY_SOURCE` until L2 bytes pinned. UNPROVED / NO_WITNESS.
- Broad `MSTL-14`: **REFUTED** (`refute_track=WITNESS_FOUND`, `truth=UNPROVED`);
  statement/domain frozen, witness stands, never silently weakened.
- Reductions banked: L1 `sum(need)<=R^B` PROVEN; Case-A `L0>=2*e_B` CLOSED;
  reduction to cumulative `6*S_A>=sum(need)` PROVED; therefore the surviving global
  bottleneck is the GC prefix bound `E_B(t) <= 3*S_A(t)` (OPEN), since
  `D2`-sum gives `N<=2X` and `X<=3*S_A` would give stock `N<=6*S_A` (k=6).
  (`lean/WP6/MSTL14PArith.lean:138-143` `stock_composition`; `scripts/wp6_rotbudget.py:1-9`.)

## 3. Exact definitions (source-pinned, not paraphrased)

- **Pair Access** (`IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.txt:256-280`;
  parent pin `parent_IMPLEMENTATION_SPEC_DECIDE-v0.4.reference.md:430-446`;
  present restatement `artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md:20-24`):
  - `KEEP: (A,B) -> (S_x A, S_x B)`, `a = c(A,x)`, `y = c(B,x)`.
  - `DELETE: (A,B) -> (S_x A, B)`, `a = c(A,x)`, `y = 0`.
  - Cost: `c(T,x) = depth_T(x)+1`. `A_0 = B_0 = T`; `S_x` = ordinary bottom-up splay.
- **StepEv counting** (`python/liquidity/multiplicity.py:1-38`; emitter
  `python/liquidity/legacy_embedding.py:107-143`; mirror `python/independent/splay.py:92-161`;
  spec freeze `IMPLEMENTATION_SPEC_SPLAY-AM-MST-LIQ-v0.4.1.md:15-16`):
  - Classes `ROOT/ZIG/LL/RR/LR/RL`; `mu`: ROOT/no-event 0, ZIG 1, LL/RR/LR/RL 2;
    `trace_sum = sum mu`; `sum mu(ev) = depth_T(x)` present-key; absent-key trace empty.
  - Capacity from class only (`python/liquidity/profiles.py:30-41`,
    `python/solver/encode.py:85-92`): ROOT 0, ZIG `rho_ZIG`, doubles `rho_DOUBLE`.
- **Present-key domain** (`math/theorems/MSTL-14P.md:3-6`; law `WorkPlan.md:25`;
  closure `pair_access_domain_mapping.md:36-38`; tests `tests/test_present_domain.py`):
  - `PresentLegalPairInstance`: `LegalPairInstance(T0,H)` with EVERY occurrence
    `(mode_i,x_i)` satisfying `x_i in keys(T0)`. By `FIXED_KEY_PAIR_ACCESS_CLOSURE`
    every requested key is present in both A and B when its occurrence executes;
    `keys(A_i)=keys(B_i)=K` for all `i`. No absent/falloff semantics occur.
- **Candidate** (`artifacts/v04/wp5x_k6c2/h5/wp6_entry_set.json:1-23`,
  `artifacts/v04/wp6_present/0909c74a/activation.json:1-14`,
  `planning/WP6_CONTRACT.md:32-35`, `Path.md:820-824`):
  - `P = P_all`, `k = 6`, `C = 2`, `rho = FLAT(2) = (2,2)`
    (`python/liquidity/profiles.py:47-50`; `LADDER[1]==(2,2)` per `tests/test_wp5x_k6c2.py:99`).
  - Key `P_all|6|2|FLAT(2)`, identity `0909c74a…b7fd`, entry-set hash `9dcdea2b…`; candidate #1 of 63.
- **GC bottleneck**: `E_B(t) <= 3*S_A(t)` for every present-key legal prefix;
  if GC then `D <= 2E_B <= 6S_A` (k=6 stock). Status OPEN/UNPROVED (§10, GC-01).
- **D2 / per-KEEP bound**: `need = max(y-2a,0) <= y-1 (a>=1) <= 2*e_B`
  (`b_event_count_lemma.md:7-21`; `tests/test_present_mechanics.py:67-76`;
  `MSTL14PArith.lean:74-76` `service_bound`). Banked author-level (raw only).
- **U=0 / sited identity**: `S_A = E_A` identically under exact sited A-StepEv
  definition (`artifacts/v04/wp6/0909c74a/lemma_sited_identity.json`; 87699/87699 events).
- **E1/E2/E3/E4** (causal-credit ancestry, §10 Stage B):
  - E1 same-access (`scripts/wp6_eventflow.py:5`): all A-StepEvs of access `t` -> all B-StepEvs of access `t`.
  - E2 pump-ancestry (`wp6_eventflow.py:7-8`; `wp6_eventflow2.py:76-81`): A-StepEvs of past
    KEEPs `u` that PUSHED `z` (M1-traced p/g sets), `u` strictly after `z`'s last KEEP.
  - E4 setup-adoption (`wp6_eventflow.py:9-10`; `wp6_eventflow2.py:44-45,71-75`): A-StepEvs of
    `z`'s setup access (last A-root-arrival) -> `z`'s B-StepEvs. Covers genesis-depth.
  - E3 triple-overlap (`wp6_eventflow2.py:101-104`; `wp6_causalcredit.py:6-7`): past-or-same
    (`ai<=idx`) sited A-StepEv whose rotated set meets B triple `P|{x}`. Structural/tight.
  - `N(b)` per B-StepEv `b_j=(idx,tri)`: `E1_j ∪ E2_j ∪ E3_j ∪ E4_j`, sited-filtered (U=0).
    E7 pumps-of-pumps excluded from Stage B core (ablation +2 marginal).
  - Allocator (`scripts/wp6_leastload.py:1-11,86-95`): chronological, online, deterministic;
    each A-StepEv source capacity 3; each B-StepEv takes 1 token from eligible `a in N(b)`
    of smallest current load, tie-break smallest `(acc_idx,step_idx)`; no reallocation.
  - **Stage B theorem (OPEN)**: `min_{a in N(b)} load_before_b(a) <= 2` for every legal
    present-key execution and every B-StepEv `b` (never starves at capacity 3).

## 4. Dependency DAG

```
U=0 (sited identity) ──┐
M1 (ancestor-only B-depth pushes) ──┤
B-freeze (B moves only at KEEPs) ───┤
root-dislodge + tenure T1/T2/T3 ────┤
A0=B0=T0 genesis + present domain ──┘
        │
        ▼
TRICHOTOMY (E1|E2|E4 or vacuous genesis-root; E3 bonus)  [PROVED_AUTHOR, Lean pending]
        │
        ▼
STAGE B (least-loaded min load_before<=2, cap 3)  [OPEN — needs load-diversity]
        │  IF proved, with D2-sum:
        ▼
GC: E_B(t)<=3*S_A(t) all present prefixes  [OPEN — the global bottleneck]
        │
        ▼
STOCK D<=2E_B<=6S_A (k=6) ──► MSTL-14P ──► 15P ──► 17P ──► 18P ──► 19 (BLOCKED_BY_SOURCE)
```

Feeder rule (`present_route_DAG.json`): broad upstream (08U/09/11/13/22), once proved
broad, implies present restriction; restricted theorems feed only present consumers.
Per-node: 15/17/18 created P-variants; 19 kept (no P-variant), L2 gate unchanged.
Broad MSTL-14 refute_track=WITNESS_FOUND untouched; broad deaths are not MSTL-14P deaths
unless witnesses satisfy `PresentLegalPairInstance`.

## 5. Every banked theorem (author-level unless noted)

| ID | Statement | Status | Source |
|---|---|---|---|
| LIQ0-01..10 | liquidity axis base | REVIEWED (human-ACCEPT-2026-09-27) | `math/proof_status.json`, `math/proofs/LIQ0-*.md`, `math/reviews/` |
| U=0 | `S_A = E_A` identically; every A-event injects exactly k=6 | PROVED_AUTHOR (code proof + 87699/87699) | `artifacts/v04/wp6/0909c74a/lemma_sited_identity.json` |
| D2 | `ceil((y-1)/2)<=e_B`, `2*e_B>=need` (raw bandwidth only) | PROVED_AUTHOR | `.../wp6_present/0909c74a/b_event_count_lemma.md`, `tests/test_present_mechanics.py` |
| D1 | present positive debt implies B work | PROVED_AUTHOR (3/3 tests) | `.../local_present_mechanics.md`, `MSTL14P_PROVE_notes.json` |
| T1/T2/T3 | tenure: rotations iff parent; other-with-rotations dislodges; B frozen tenure = x-DELETEs only | PROVED_AUTHOR (+0/2000 audit) | `artifacts/v04/wp6/0909c74a/lemma_tenure.json` |
| TENURE-NEED | `a=1` demand characterized (KEEP-start⇒need0 else max(D-1,0), pre-tenure L2-open) | PROVED_AUTHOR present-only | `.../lemma_tenure_need.json` |
| RUN-NEED | needs@first-KEEPs, `S_A`@run-starts, tenure==run (0/1292 viol over 2000 hist) | PROVED_AUTHOR | `.../lemma_run_localization.json` |
| GENESIS 1:1 | first-divergence tenures exactly self-funding; e_B=e_0, need covered | PROVED_AUTHOR modulo U=0/tenure/determinism; AR-14/15/16 Lean PENDING; subsequent OPEN | `.../first_divergence.json`, `lean/WP6/MSTL14PArith.lean:145-164`, commit `bfc366a` |
| L1/CASE-A/REDUCTION | `sum(need)<=R^B`; Case-A `L0>=2*e_B` closed; reduction to cumulative stock proved | PROVED_AUTHOR | `.../wp6/0909c74a/cumulative_lemma.json`, `MSTL-14_PROVE_notes.json` |
| M1 | B-depth changes only via B-rotation-as-p/g or reset-to-0 | PROVED_AUTHOR | `MSTL14P_PROVE_notes.json`, `Path.md` C7 |
| #cash<=S_A | cash bound mod U=0 | PROVED_AUTHOR | same notes |
| K3-tightness | deficit-2 = shortfall characterization | PROVED_AUTHOR | `.../lemma_k3_tightness.json` |
| Lemma A | O(1) interval records, worst 2/3 over 4067 events | LOCAL-O1-VERIFIED (aggregation dead) | `.../lemmaA_intervals.json` |
| Lemma B | exposure valid, 0 viol, max swing 343/920 keeps (aggregation dead) | PROVED_AUTHOR (diagnostic only) | `.../lemmaB_pathdefect.json` |
| TSTAR-COND | T1 M=2E, T2 ACTIVE_pre=T*++M-SPENT, T3>=2E-N; gap G_tstar FALSE general | CONDITIONAL banked, open gap | `.../tstar_conditional.md`, commit `53bc453` |
| TRICHOTOMY | genuine B-StepEv ⇒ sited E1\|E2\|E4 ancestry, else vacuous genesis-root; N(b) never empty | PROVED_AUTHOR modulo banked deps; Lean PENDING (needs splay model) | `.../trichotomy.json`, commit `c59c22d` |
| AR-01..05 | need_le_pred, rots_le, mob_exact, service_bound | PROVED_KERNEL (lean exit 0, no sorry — per file header; re-check required) | `lean/WP6/MSTL14PArith.lean:1-76` |
| V3=V4=0 | bounded-horizon exhaustive (3M paths) + D5/6 exhaustive (8M paths n=6/8) | FINITE_EVIDENCE (exhaustive in scope) | `badhorizon.json`, `depth56.json`, commits `74c0033`, `8a9fc10` |

## 6. Every refuted theorem/route (with ledger key + witness; DO NOT resurrect)

Broad: `MSTL-14` REFUTED — absent-key KEEP battery: `death_00.json`
(`P_all|6|2|FLAT(2)`, n64, absent_key 10, battery 11 KEEPs, kill keep #11,
need 1 paid 0 margin −1, triple-confirmed primary==independent==cleanroom);
cascades to `ALL_63_CANDIDATES_REFUTED` (`cascade_summary.json`, `death_00..62.json`;
commit `ebbc5de`). Mechanism: absent KEEPs demand T6 `need=max(y-2a,0)` with empty
trace (zero T7/T5), drains ANY finite ACTIVE.

`route_kills.json` kill ledger (exact keys; counts are finite witnesses, not theorems):

- `killed_routes` (22): per-access need gap 186; linear IPL best 246; max-IPL excess<=10
  bystander-rise; sum-divergence Theta(n) PROVED; balance circular; per-key intervals
  #keys blowup; Z-term uncontrollable; log dimensional; pool LAT/ACT wrong-dir VERIFIED;
  minimal-counterexample no-descent; rotation-correspondence unfunded; backward-charging
  190:1; frozen-order overlap; M<=1 hits 128; `R^B<=3S_A` +7 kill; `max(0,2dB-2dA)`
  others-rise 20; post-KEEP absent-bound need 2 post-KEEP; `R^B<=6S_A` ALIVE ce_0000 −187;
  k-monotonicity insufficient.
- `killed_routes_2` (10): `R^B<=3R^A` incomparable; root-chain multiplicity unbounded;
  perceptron feasible-train BUT 1241 fresh viol gap<=18 (overfit);
  `E_B<=3S_A` needs exact-6; frozen-order blowup; per-KEEP `R^B` vs `e_A` 95-vs-1;
  subsequence-vs-full diverge (×2).
- `killed_routes_3_quotient_war_2026-09-29` (6): M1/M2/M5 gaps 57/29/62; M3 B-leak+2
  KEEP-gap 23; CAP2 B-leak+4 gap 30; depth-CAP creation FAIL 20>6 B-leak+11 gap 36;
  per-run 6-budget FALSE 58:1 (DELETE 15:1); impossible-triangle (`mass_autopsy.json`).
- `killed_routes_4_vault_descent_2026-09-29` (9): involvement FALSE gap 48
  (need60/involve6); subtree FALSE gap 60; zig/doubles FALSE 1.22; cash/setup +13 vs
  noncash 709≫cash 286; `D<=E_B` FALSE 1.94; `R<=1.5Q` FALSE 1.58 (R218/Q138 n128-L19);
  Psi 1243-gap REVELATION; pure-mass triangle; rotation-word explosion/push-backing sharing.
- `killed_routes_5_eventflow_2026-09-29` (4): E1+E2+E4 capacity SHORT (86/120 prefix,
  371/486 min-cut 0, gap +210 saturated); duality-blocked; epoch/nested 700× shortfall
  vs 1.57× global; FOUR DUALITIES.
- `killed_routes_6_tracecorridor_2026-09-29` (5): raw-dist LAW-K FALSE +3
  (dist5→5, e_B3/e_A0, median −2); word/shape splay-invariant; E3 80/0 dens 8.5
  flow==counts diagnostic; top/bottom restates; matching residual-fundamental.
- `killed_routes_7_sod_2026-09-29` (2): SOD-3 FALSE damage+9 c*12 (285/400 never resync,
  unbounded); per-deletion +11 vs +2 batch survives (`sod_tail.json` med 0.33, tail 0.83%).
- `killed_routes_8_tsrc_hazard_2026-09-29` (4): TSRC Delta GAP +5/+11/+15/+18 NO
  lambda[0,3]; hazard n≤7 zero BUT +1/+4/+5/+21 at n16/32/64/128; vector LP infeasible
  n5/6/7; pair-PHI teleport-infeasible.
- `killed_routes_9_rankcycle_2026-09-29` (2): depth-proxy rises n32/64/128 non-tight
  inconclusive; V1-tight 0 found, greedy dominates 99.9%.
- `killed_routes_10_sterile_2026-09-29` (1): CASH-RESET STRONG FALSE — 90/150 worst +22
  (`sterile.json`; residual pumped B-deep/A-shallow bystanders; n≤6 V=0 was artifact).
- `killed_routes_11_corridor_2026-09-29` (1): greedy cumulative-max stalls (diagonal, chains 0).
- `killed_routes_12_anatomy_2026-09-29` (1): greedy falsifier stalls (depth≥2 needed).
- `killed_routes_13_borderline_2026-09-29` (1): borderline-crossing 1/126 transient 3:1
  windows 0.8%, parity dead, leak 0.5 absorbed 5–50×.
- `killed_routes_14_firstcross_2026-09-29` (1): FC-FIRST FALSE — 39% tenure-frozen
  (pay 0, D predates = tenure-need L2-open), sharing persists.
- `killed_routes_15_xreturn_2026-09-29` (2): X-RETURN universal FALSE +16
  (`xreturn.json` blocks 3073, ex [232,30,6,7,16], others-tenure cargo KEEP38 B47/A4 +18);
  conditional form tautological (R(t*)≤0), interval version unprovable — N-FIRST closed both ways.
- `killed_routes_16_tokens_2026-09-29` (6): per-key / B-depth-closed / recency-overdrawn O(n)× /
  interval sharing-or-choice / edge-level-path overdrawn / Psi 1243-gap token shapings dead.
- `killed_routes_17_loaddiv_2026-09-29` (1): greedy-optimality no-matroid (E1+E4 fails 38).
- `killed_routes_18_tiers_2026-09-29` (1): deep-tier shared fanout O(n).
- `killed_routes_19_refresh_2026-09-29` (1): per-transition rank proxy rises unconfirmed,
  V1-tight absent.
- `killed_routes_20_e3order_2026-09-29` (2): E3 laminar FALSE (incomp 930/1703 = 55%,
  sub+super 10%); ordered-chain no-monotone-saviors, oldest-spread.

## 7. Every finite-only empirical observation (MUST NOT be promoted)

- Genealogy (`genealogy.json`): B_events 7114, min 1, med 11.0, p90 27, max 89, never empty.
- Least-loaded (`leastload.json`): B 2331, maxload 2 (cap 3), starved 0.
- Forced singletons (`singleton.json`): B 6009, singletons 6 (0.0998%), worst shared load 1.
- Minload (`minload.json`): 0/2010 minload-2; worst_ml 1; adversarial best 1 over 860 evals (kill≥3 untouched).
- Minload anatomy (`minload_anat.json`): B 3852, m1 72 (1.87%), 25 specimens; overflow-to-oldest pattern.
- Tiers (`tiers.json`): top 200, top_e1cov 189 (94.5%); deep 1623, deep_pump 521 (32.1%).
- E3 order (`e3order.json`): 351 splays; equal 593, incomp 930 (54.6%), sub 64, super 116;
  turnover new ~2.63 / lost ~2.01 / net ~+0.6 per B-StepEv is LEDGER-ONLY
  (`alive_e3order_2026-09-29`, Path.md C27, script stdout) — NOT in `e3order.json` (§15).
- Stock/raw-stock: `D<=6S_A` best 0.47, 153k+ attacks 0 kills (incl. 152777 present-refute);
  raw `sum(need)<=6*S_A` 25× slack — UNPROVED.
- GC ratios: `E_B<=3S_A` best 1.57/3 over ~15k+8k+9.3k hunts; n≤7 orbit-BF verifies, minslack 0;
  scale-invariant 1.0–1.7 n8..512 — UNPROVED at arbitrary n.
- Coverage/funding: Vm+F>=Vp min 0.00, excess/C≤0.36; funding 20× (anti 5× + DEL 15×);
  slack 5–50× ≫ q; new-hazard 0/12 — all FINITE.
- Bellman/rank small-n: V==V1 1.000, h*≤1, maxV 2,2,3 (n4/5/6); rank never-rises on tight
  positives; 1296 cycles 0 positive — small-n only.
- `sterile.json` `pump:0 gen:90` is UNRELIABLE (script-side approximation, §15); residual
  existence (90/150, worst +22) is exact.

## 8. Every exact counterexample/witness

- `artifacts/v04/wp6/absent_refutation/death_00.json`: broad MSTL-14 kill vs
  `P_all|6|2|FLAT(2)` (need1 paid0 margin−1, absent_key 10, battery 11, keep #11, n64;
  witness_hash `24975de3…`; triple-confirmed). `death_01..62.json`: all 63 candidates
  (all absent_key 10, need1 paid0 margin−1; e.g. 01 FLAT3 L*16; 57 `P_keep|6|2|ROT(1)` L*3;
  62 `P_keep|6|2|ROT(6)` L*7). `cascade_summary.json`: 63/63 refuted, active [], terminal.
- `artifacts/v04/obstruction_import/MST0-14R_LEGAL_WITNESS.json`: n28 H[D27,D28,K28,K27]
  a2 y15 need11 paid10 margin−1, residual growth to n512 (need253 paid131); + replay files.
- `artifacts/v04/counterexamples/ce_0000.json`: k3 n192 H[DELETE129,KEEP134,KEEP130,KEEP129]
  S_A 70 sumNeed 212 R^B 233 deficit +2; `ce_0001.json` (P_keep doubles k3); `ce_0002.json`.
- `xreturn.json` ex [232,30,6,7,16]: +16 others-tenure witness. `sterile.json` ex
  [11,100,2,50,96,1,25]: +22 residual witness. `resetdepth` n128-L19 R218/Q138: 1.58 kill.
  `hazard_scale`: +1/+4/+5/+21 scale kills of one-step hazard. `psi_anatomy`: 1243-gap.
  `involve.json` worst_key_gap 46 / interval 48; `subtree_presence` worst 60.
- Present domain: NO WITNESS against MSTL-14P (`present_refute/present_refute_summary.json`:
  152777 histories, 0 kills, ATTACKED-NOT-REFUTED; `refute/refute_summary.json` 8096, 0 kills).

## 9. Every kernel-pending item (Lean)

File `lean/WP6/MSTL14PArith.lean` (arith-only; header: NO splay/ledger/history-induction model):

- Kernel-checked per header (re-check required in a Lean env): AR-01 `need_le_pred`,
  AR-02 `rots_le_two_events`, AR-03/03b/04 mob exactness, AR-05 `service_bound`.
- SKELETON, MUST be kernel-checked before citing as Layer B: AR-06 div_rise_A (+4),
  AR-07 div_rise_B (+1), AR-08 capped_gain, AR-09 poolAux+pool_step, AR-10 steps_le_depth,
  AR-11 depth_le_two_steps, AR-12 genesis_need_zero, AR-13 `stock_composition`,
  AR-14 `first_div_need`, AR-15 `same_shape_funded`, AR-16 `strict_D2`.
- Trichotomy formalization PENDING (needs splay model beyond arith-only file).
- Toolchain pin `lean-toolchain`: v4.21.0. No `sorry`/`admit`/axioms permitted.

## 10. Every live open lemma (the live region)

- **STAGE B (LIVE, OPEN)**: chronological least-loaded never starves at capacity 3
  (`min load_before ≤ 2`). Blocked on load-diversity: needs counts=claim +
  greedy-optimality without matroid; E2/E3 sharing breaks laminar structure while
  E1+E4-only fails 38 histories.
- **GC / E_B-link (LIVE, OPEN)**: `E_B(t)<=3*S_A(t)` every present prefix. Sole survivor
  (global-count prefix induction, slack 0.33, reason unknown, possibly emergent).
- **C27 triple-motion REFRESH candidate (LIVE, UNPROVED)**: E3 sets expand net +0.6/step
  (growth ≥ consumption universally — unproved); may replenish eligible ancestry faster
  than least-loaded consumption.
- Supporting opens: B-source lemma (THE open core); suffix bound `2E>=sum(need)` + t*
  location; M3-creation micro-lemma (AR-06, tight 1252 hits); residual-chain law;
  N-AUG exchange + N-FIRST normal form (QUEUED); machine nonlinear potentials;
  multi-session amortization; L2 `R^B<=6S_A` prepayment theorem.
- Alive-but-open ledger keys retained verbatim in JSON: `alive_but_open` (4),
  `alive_but_open_2_quotient_war_2026-09-29` (3), `alive_tracecorridor_2026-09-29` (3),
  `alive_ts_corroboration_2026-09-29` (4), `alive_vault_2026-09-29` (6),
  `alive_eventflow_2026-09-29` (5), `alive_sod_2026-09-29` (3), `alive_sterile_2026-09-29` (2),
  `alive_rankcycle_2026-09-29` (5), `alive_corridor_2026-09-29` (2),
  `alive_anatomy_2026-09-29` (3), `alive_firstdiv/firstcross/borderline/tokens/loaddiv/tiers/refresh/e3order/xreturn`.

## 11. Every relevant script and artifact (canonical paths discovered)

- Canonical live artifact dir: `artifacts/v04/wp6_present/0909c74a/` (81 items: 78 files + 3
  subdirs `periodic/`, `present_refute/`, `quotient/`). Legacy/route dir:
  `artifacts/v04/wp6/0909c74a/` (15 items: 9 files incl. `route_kills.json` + 6 subdirs
  `cumrefute/`, `margin_probe/`, `perceptron/`, `refute/`, `refute_absent/`, `refute_absent2/`).
  BOTH exist; neither is assumed — recorded here. Domain audit:
  `artifacts/v04/wp6_present/present_domain_audit/` (4 files). Route DAG:
  `artifacts/v04/wp6_present/present_route_DAG.json`.
- Scripts (`scripts/wp6_*.py`, 81 files): absent_attack/cascade/hunter, badhorizon, beamhunt,
  bellman, borderline, **breaking (UNTRACKED, unsealed)**, cashchain, causalcredit, corpse,
  coverage, cumrefute, cycles, depth56, discharge, dissect, distnorm, doubles, drain_absent,
  e3order, eb_hillclimb(+2), eventflow(+2/abl/cut), freshness, funding, gdel_one, hazard(+scale),
  horizon, involve, lastsafe, leastload, lemmaA, lemmaB, margin_probe, mass_capped(+size/screen),
  minload(+anatomy), mstl14_refute, need_eb, neutral(+2), orbitbf, pairing, pairlp(+2),
  perceptron, periodic, phi_screen, prefix_eb, present_refute, psi_anatomy, purepump, quotient,
  rankmine/rankscale/ranktight, ratio_hunt, resetdepth, rotbudget, run_attack, scaling,
  singleton, slack, sod3/sod_hill/sod_tail, splaymetric(+2), sterile, stock_sweep, subtree,
  tiers, xreturn, zeroanat. Non-wp6 runners: `run_phase00..05.py`, `run_wp5x*.py`,
  `run_h5_k6c2.py`, `reveal_h4l.py`, `seal_h4l.py`, `check_*.py`, `emit_wp*.py`, `build_closure*.py`.
- Code: `python/solver/` (battery/encode/legality/predicates/promote/search);
  `python/liquidity/` (activation/diagnostics/legacy_embedding/multiplicity/profiles);
  `python/{adversary,audit,cleanroom,holdout,independent,wp5x}/`; `python/independent/ledger.py`
  (independent ledger+replay). NO top-level `solver/` or `theorem/` (discrepancy, §15).
- Lean: `lean/Liquidity/` (4 files), `lean/WP6/MSTL14PArith.lean`. Theorems:
  `math/theorems/` (31 files incl. MSTL-14P/15P/17P/18P/19). Proofs: `math/proofs/` (20).
  Status: `math/proof_status.json`. Contracts: `planning/WP6_CONTRACT.md` (+17 files),
  `WorkPlan.md` (28 lines), `Path.md` (1184 lines, append-only execution ledger).
  Schemas: `schemas/` (7). Prereg: `prereg/` (13). Tests: `tests/` (12 test files).
- Key artifacts: `genealogy.json`, `leastload.json`, `singleton.json`, `minload.json`,
  `minload_anat.json`, `tiers.json`, `e3order.json`, `trichotomy.json`, `first_divergence.json`,
  `lemma_tenure_need.json`, `lemma_run_localization.json`, `tstar_conditional.md`,
  `b_event_count_lemma.md`, `local_present_mechanics.md`, `MSTL14P_PROVE_notes.json`
  (all under `wp6_present/0909c74a/`); `lemma_sited_identity.json`, `lemma_tenure.json`,
  `lemma_k3_tightness.json`, `cumulative_lemma.json`, `route_kills.json` (under `wp6/0909c74a/`);
  `death_00..62.json` + `cascade_summary.json` (under `wp6/absent_refutation/`);
  `ce_0000..0002.json`, `large_n/`, `h4l_reveal/`, `logs/run_*.json`.

## 12. Every relevant commit (recoverable history, newest first)

- `f44982c` E3 ordered-family (C27): not nested (55% incomp), expands +0.6/step; UNPROVED.
- `678f911` REFRESH anatomy (C26): overflow-to-oldest-abundant, 72 minload-1 specimens; UNPROVED.
- `5995eec` Two-tier diversity (C25): top closed-ish (zig-limit+setup, margin 1), deep open; UNPROVED.
- `c59c22d` Trichotomy banked (C24); load-diversity minload≤1, kill untouched; UNPROVED.
- `616aec2` Causal-credit tokens (C23): genealogy abundant, maxload-2, singletons rare; UNPROVED.
- `24714c5` X-RETURN (C22): universal FALSE (+16), conditional tautology; N-FIRST closed; UNPROVED.
- `3748efb` First-crossing surgery (C21): last-safe 61/39, tenure-open=L2, no circularity; UNPROVED.
- `bfc366a` First-divergence 1:1 (C20): AR-14/15/16 skeleton; subsequent open; UNPROVED.
- `663fc59` Borderline (C19): common 126, crossing 1 (transient windows); allowance; UNPROVED.
- `8a9fc10` Depth-5/6 exhaustive V=0 (8M paths n=6/8); beam D8 holds.
- `48073d3` Anatomy (C18): new-hazard zero, slack≫q, coupled-3×; beam D8; UNPROVED.
- `74c0033` Corridor (C17): V3=V4=0 exhaustive (3M), greedy stalls, serialization; UNPROVED.
- `b05dc63` Sterilization CASE R (C16): +22 residual pumped bystanders; UNPROVED.
- `089ab85` Rank/cycle/Bellman vault (C15): V==V1 h*≤1 n≤6, rank valid small-n; UNPROVED.
- `01c80d2` TSRC/hazard (C14): batch FALSE(+1), Delta/LP/vector dead, scale-dead; n≤7; UNPROVED.
- `4e1ef69` SOD lane; `5b515d8` trace-corridor; `b9a52d0` vault-descent/event-flow;
  `cc6bd58` quotient war 1–8; `eaace7b` Lemma A/B; `5b91902` run-need; `e29e3bc` tenure-need;
  `f5aaeeb` MSTL-14P war (R=0, 6=2×3 killed); `c196ca9` w6e_18 lawful; `53bc453` tstar+Lean backbone;
  `cda784a` PR-03 repair + D1/D2; `8fe6db9` present-route candidate-1 binding;
  `2ae7f2a` present WorkPlan amendment; `1db7c7e` present source audit PASS;
  `0a02f6f` perceptron screen; `ebbc5de` MSTL-14 REFUTED (absent battery → ALL_63);
  `0f20523` lemma artillery (R≤0 152k, U=0, tenure, k3-tight); `cf0cb77` 8096eps 0 kills +
  Case-A closed; `4ed2760` H5 entry; `bdb71f1` H5-successor route; `1f43527` WP-6 entry blocked;
  `e1b02f1…2ef7539` H5-R1 seal/reveal chain (see `git log --oneline --decorate`).

## 13. Current immediate proof target

**Stage B**: for every legal present-key execution and every B-StepEv `b`,
`min_{a in N(b)} load_before_b(a) <= 2` under the chronological deterministic
least-loaded allocator at capacity 3 (E1+E2+E3+E4 ancestry; trichotomy supplies
nonemptiness; load-diversity is the missing piece). Stage B + D2-sum is the on-ramp to
GC (`E_B<=3S_A`), hence to k=6 stock and MSTL-14P.

## 14. Explicit DO NOT RESURRECT list

Raw rotation bound; local per-key attribution; local intervals; depth/IPL potentials;
scalar Psi; operational splay distance; one-step hazard; (strong) sterilization/CASH-RESET;
X-RETURN (universal false, conditional tautology); old N-FIRST forms (global-slack as proof,
interval-only, reset/segment link, setup-attribution as attribution, borderline-as-killer);
residual-rank/Bellman at scale; SOD single-omission; trace-corridor raw-dist; quotient-war
pure masses / per-run budgets; TSRC Delta/LP/vector; corridor greedy; perceptron family;
rank-proxy transitions; E3-laminar/ordered-chain; E1+E4-only allocation; greedy-optimality
(matroid-free); any finite-evidence→theorem promotion; any silent broad-domain weakening
(broad MSTL-14 witness stands; absent witnesses never count against MSTL-14P).

## 15. Exact next action recommended by current state

Attack Stage B load-diversity via the C27 triple-motion REFRESH candidate WITHOUT marking
anything proved: (a) commit this reconstruction first; (b) run the unsealed
`scripts/wp6_breaking.py` (BR-00) hunt for shrink+overflow+thin-E2E4 shapes and record
whether min-load ≥ 2 is ever reached — a hit is a Stage-B counterexample, a miss pattern
is finite evidence only; (c) persist E3 turnover (new/lost/net) into `e3order.json`
schema (currently ledger-only) and test growth ≥ consumption universally; (d) then attempt
the triple-motion/overlap-expansion lemma that would discharge Stage B, hence GC, hence stock.

---

## Appendix A. Prompt-vs-repo discrepancies

1. `audits/` did not exist (no top-level README either). Reconstruction CREATES
   `audits/WP6_COLD_RECONSTRUCTION.{md,json}` per the prompt's preferred names.
2. No top-level `solver/` (canonical: `python/solver/`), no `theorem/` (theorems in
   `math/theorems/`, Lean in `lean/`), no `specs/` or `current-paper/` (statements in
   `math/theorems/`, `planning/`, `Path.md`, `WorkPlan.md`).
3. C27 turnover (new ~2.63 / lost ~2.01 / net ~+0.6) is NOT in `e3order.json` (which stores
   only `{splays:351, nest:{equal:593,incomp:930,sub:64,super:116}}`); it lives in
   `alive_e3order_2026-09-29`, Path.md C27, and `wp6_e3order.py` stdout only (script computes
   but does not persist `new_tot/lost_tot`).
4. `sterile.json` `pump:0 gen:90` is a script-side approximation (`wp6_sterile.py:149-160`
   uses empty pumped set); residual existence/worst-+22 exact regardless.
5. Untracked `scripts/wp6_breaking.py` (BR-00) postdates the sealed HEAD; uncommitted, unsealed.
6. `lean/WP6/MSTL14PArith.lean` shell rendering shows encoding artifacts here; file itself
   untouched (read-only this run); kernel re-check still required.

## Appendix B. Verification performed before sealing

- `git status / branch --show-current / remote -v / log --oneline --decorate -n 15 / rev-parse HEAD`.
- `route_kills.json` top-level keys enumerated (42 keys) and every key packaged in JSON §6/§10 entries.
- Referenced scripts existence: all 7 causal-credit scripts + E-definitions confirmed on disk.
- Referenced artifacts existence: `genealogy/leastload/singleton/minload/minload_anat/tiers/e3order/trichotomy/first_divergence.json`,
  `present_route_DAG.json`, `cascade_summary.json`, `death_00.json`, `math/proof_status.json` — all read back.
- Status-label discipline: proof vs finite evidence vs refutation vs Lean-pending kept distinct
  throughout; C27 candidate NOT marked proved; GC and MSTL-14P remain UNPROVED/NO_WITNESS
  (broad MSTL-14 alone is WITNESS_FOUND).
