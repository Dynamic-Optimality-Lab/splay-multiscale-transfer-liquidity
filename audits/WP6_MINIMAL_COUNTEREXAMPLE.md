# WP6 GC-STATIC — whole minimal-counterexample proof, holes marked (C56)

Status: CONDITIONAL PROOF (banked steps rigorous; exactly one load-bearing hole + two sub-holes).
Date: 2026-09-30. Branch: `wp5x-k6c2-specialized`. Candidate: `P_all|6|2|FLAT(2)=(2,2)`, `0909c74a`.
Method: present-legal pair instances only (`PresentLegalPairInstance`: `LegalPairInstance(T0,H)` + `x_i in keys(T0)`).
Graph: left B = demand events (1 unit), right A = sited StepEvs (cap 3). Edges = past-only causal
`E1+E2+E3+E4+E7` (sited only). `N(Q)` = distinct adjacent A ids. `Delta(Q)=|Q|-3|N(Q)|`.
`Q_j` = B-events of Q at access `j`. `f_j` = fresh slots (`|E1(j)|` case (a); pristine-`|E4(j)|` case (b)).

## Theorem (GC-STATIC, OPEN)

For every present-legal history, offline cap-3 causal assignment saturates:
for all `Q ⊆ B`, `|Q| ≤ 3|N(Q)|` (shortfall 0, GC-gap 0).

## Proof attempt (minimal counterexample, end to end)

Assume for contradiction some `Q` is deficient: `Delta(Q) > 0`.
Take inclusion-minimal deficient `Q` (finite descent; exists).

Step 1 — deficit exactly one [BANKED 8A, AR-20 kernel].
For every `b ∈ Q`, `Q\{b}` is non-deficient: `|Q|-1 ≤ 3|N(Q\{b\})| ≤ 3|N(Q)|`.
With `|Q| ≥ 3|N(Q)|+1` forces `|Q| = 3|N(Q)|+1`, `Delta(Q)=1`.

Step 2 — min source degree ≥ 4 [BANKED 8B, AR-21 kernel].
If some `a ∈ N(Q)` has `r=deg_Q(a) ≤ 3`, `R` its `Q`-neighborhood, `Q'=Q\R` has
`|N(Q')| ≤ |N(Q)|-1` (`a` absent), so `Delta(Q') ≥ |Q|-r-3(|N(Q)|-1) = Delta(Q)+3-r ≥ 1`,
a smaller deficient set (`Q'` nonempty automatically: else `Delta=0` contradicts `≥1`).

Step 3 — connected core [BANKED 8C].
Components have disjoint source neighborhoods (else connected); deficit additive
`Delta(Q)=Σ Delta(Q_i)`; every vertex has an edge (A-side by N-definition; B-side by
trichotomy nonemptiness). Positive total ⟹ some component positive ⟹ unique by minimality.

Step 4 — latest-access shape [BANKED 8E + 8J].
Let `L` = latest access in `Q`, `Q_L ≠ ∅`, `Q_<L` strict subset, `U_L = N(Q_L)\N(Q_<L)`.
Then `|N(Q)| = |N(Q_<L)|+|U_L|` (disjoint by def).
Minimality: `Delta(Q_<L) ≤ 0`, `Delta(Q)=1`, so `1 = Delta(Q_<L)+|Q_L|-3|U_L| ≤ |Q_L|-3|U_L|`,
i.e. `|Q_L| ≥ 3|U_L|+1` (8J-necessary, no circularity).
`U_L` = aev with `ai=L` in `N(Q_L)` (E2/E4/K/W all `ai<L`; E3-same-access non-E1 impossible
since E1 = all sited `accA[idx]`). Hence `U_L ⊇ E1(L)` (complete edges, disjoint from earlier),
` |U_L| ≥ e_A(L)`. If `E1(L)≠∅` then `|Q_L| ≥ 3e_A(L)+1` (Q-heavy AND whole-B-heavy);
if `E1(L)=∅` (repeat-`L`) only `Q_L≠∅` forced — demand-without-supply habitat (8E).

Step 5 — non-heavy zone done [BANKED 8H+8I, FRESH-CHANNEL+RUN].
Fresh sets `F_j` pairwise-disjoint (E1 fresh ids per access; pristine-E4 distinct setup
accesses across runs; mixed E1/E4 double-duty with BOTH demanding impossible by RUN
`≤1 demanding KEEP/x-run`; genesis-T0-root demands nothing). Each `F_j ⊆ N(Q)`.
Hence `Delta(Q) ≤ Σ_j(|Q_j|-3f_j) ≤ Σ_{heavy}(e_B(j)-3f_j)`.
Corollary: violators REQUIRE B-heavy accesses. Non-heavy `Q` never violates.
Q-specific form (8I): `Delta(Q) ≤ Σ_j q_j(Q)`, `q_j=|Q_j|-3|F_j∩N(Q)|`; only B-heavy-Q
blocks (`q_j>0`) contribute positively; danger = heavy-block overflow exceeding shared-old.

Step 6 — reverse-induction frame [BANKED 8K shape; 8L circularity noted].
Strong induction on `|Q|`: `|Q|=|Q_<L|+|Q_L|`, `|N(Q)|=|N(Q_<L)|+|U_L|`; IH gives
`|Q_<L| ≤ 3|N(Q_<L)|` (strictly smaller). Suffices `|Q_L| ≤ 3|U_L|`.
Since `|U_L| ≥ e_A(L)`, non-heavy `Q_L` closes free. B-heavy `Q_L` needs old-new
entries (W-first-overlaps, E2-window, intervening young) covering overflow/3.
8L autopsy: carry-sufficiency `d_L ≤ sigma_prev ⟺ Hall(Q)` (biconditional) is CIRCULAR
as strategy — DEAD. What stands: 8J-necessary + sigma-transfer identity + IH on strict
subsets (legitimate). The ONLY missing lemma is access-local: old-new sufficiency at
B-heavy Q-blocks (≡ old-abundance §10). No circularity in stating it; circularity only
if we assume carry to prove itself.

**HOLE-1 (FIRST HOLE, LOAD-BEARING, OPEN): OLD-ABUNDANCE AT B-HEAVY Q-BLOCKS.**
Formal: let `L` be B-heavy-Q (`|Q_L| > 3|U_L|`-candidate, i.e. `e_B(L) > 3f(L)` shape with
thin `U_L`). Then shared-old `R_old = N(Q)\F` (or access-local old-new `U_L`-beyond-`E1`
plus cross-access old) absorbs overflow: `|Q_L|-3|U_L| ≤ 3|R_old|-available` globally,
resp. `|Q_L| ≤ 3|U_L|` after counting old-new first-overlaps at `L`. Equivalently:
B-heavy demand cannot outrun distinct-old-union by more than fresh covers.
This is EXACTLY the wall (C28–C56): E1-CAP/FRESH-CAP close non-heavy; everything heavy
reduces to this. Conditional mindeg-safety 8Q shows Hall ⇐ smaller-Hall + `mindeg≤3`,
so the remainder IS `mindeg≥4` = violator zone = HOLE-1 zone (consistent, not closing).

Assuming HOLE-1, contradiction is immediate: IH + HOLE-1 step gives `|Q| ≤ 3|N(Q)|`,
contradicting `Delta(Q)=1`. Hence no minimal violator exists; GC-STATIC holds. ∎ (conditional)

## HOLE-1 assault (spend tokens here; exactly this hole)

Decompose HOLE-1 into falsifiable conjunctions (supply avenues mapped 8O, 15 avenues):

1a. Sustained sterile B-heavy (multi-access pressure chaining).
1b. Single-access pressure elevation (one heavy block alone kills).
1c. Repeat-hole (W-inc≥4 all-later-repeat + E4-early + no-returners).
1d. E2-hole + K-thin + sterile-E3 triple conjunction (8G+C41).
1e. Sterile-rebuild sustain (fresh-far pool vs stall-or-save, 8R residual).

Evidence against each (finite, not theorems; kill = shortfall>0 or gap>0):

- 1a: CHASE maxpush 22 then B-bottom stall; tags 95% impure (supply-creating), pure 115
  singly, 0 pure-sustain; SG/SG2 8k+10k clean, best slack 34/27; strike diagnostic e_B≥8
  NEVER under avoidance (300 hist); FULLSPLIT sustain 28 (zone-bleed break) slack 44–53
  never converts; RUNDRAIN best cumulative -24, worst single -29, saturates via shared-old.
- 1b: PRESSURE 1144 KEEPs: heavy 53 (4.6%), pressure[B-heavy+old≤2] 17 (1.5%, eB med 28
  max 64), minload@pressure always 0 (fresh absorbs first picks); TIGHTEST/LARGETIGHT
  best slack 2 (degenerate singleton)/Q3; 2.28M exhaustive + 60k+ targeted zero shortfall.
- 1c: FOURTH 3045 Qs, 31,331 deg≥4: W-inc≥4 ⟹ multi-episode 7943/7943, companions 7943/7943,
  nocomp 0, rephole 0 finite; repeat-hole universal OPEN (needs W-ladder proof).
- 1d: E2-hole structurally possible (DELETE-then-KEEP pushers, E2 records pump-KEEPs only)
  + sterile-E3 + thin-K/E4 + B-heavy conjunction; C41 BOUND: pure e_A=0 chains cannot push
  (repeats B-no-ops/skips); every push chain contains real splays; repeat-cycles anchor
  supply at run-start (E1 fresh or pristine-E4 via FRESH-CHANNEL-b); E12 covers 106/150,
  +E4 +0 marginal here (case-b rare), +K +22, +W +22 (E2 carries bulk).
- 1e: 8R pinning-impossible 2661/2661 (supply-free pushes single-shot; rebuilds supply);
  PUSH-INCOMPAT + BIGN (B to 611, E2 tracks) + DELHEAVY (15k supply-rich) + WASTE 44.9%
  (online-only transient-diversion, NOT Hall-applicable) + SPLITZONE/CHASE/SURGICAL2.

C56 WALLMAX (this continuation, direct optimizer on pressure):
`scripts/wp6_wallmax.py → wallmax.json`: first-x + nearby-below pure pushers + run-repeat
drain + far-key avoidance, hillclimb on (shortfall, gap, pressure, eB/f), 10k evals:
bestpress 2 per history (seeds best 1, ratio 9.67; it90 ratio 34 slack 20; it583 press 2),
final bestpress 2, bestratio 12.0, bestslack 32 (`acc14 Q1 N11`), zero shortfall, zero gap.
Even MAXIMIZED, pressure stays ≤2/history isolated and slack stays ≥32. Wall-pressure cannot
be sustained/elevated by any generator in the arsenal. Finite face of 1a+1b.

Verdict on HOLE-1: NEITHER PROVED NOR KILLED. No Hall violator (kill fails 70k+ runs);
no abundance theorem (proof fails: DAG/aggregate dead via E1-maximals/sharing-∞; fluid/
counting forbidden ≡GC; augmenting circular; induction circular 8L; hub counts-nil 8M;
pool-deficit restatement 8O; fourth-use maps but doesn't close 8N; displacement-coupling
finite only 8P; pinning leaves overlap open 8R). Residual narrowed to: isolated single-access
pressure exists (1.5%) but never elevates; sustained pressure impossible by impurity (finite).
HOLE-1 STANDS as the single load-bearing gap.

## Resume proof from HOLE-1 (same proof, next hole)

Assume HOLE-1 as lemma → Step 6 closes → contradiction → GC-STATIC conditional-QED above.
Unconditional resume requires HOLE-1 proof. Split HOLE-1:

**HOLE-2 (SECOND HOLE, OPEN): ONE-ACCESS HALL 8F + OVERLAP (8R residual).**
`Q_j` (one access): `E1(j) ⊆ N(Q_j)` always so `|N| ≥ e_A`; Hall fails unless B-heavy with
sterile-thin old (same wall, fractal at access scale). 26k+ offline evals subsuming one-access
violations clean. Overlap sub-hole: supply-free pushes rebuild via zone-overlap for x?
Pinning forces rebuild accesses; whether they must overlap x-zone (save) vs can stay disjoint
(kill-sustain) is OPEN; FULLSPLIT shows disjointness sustains 28 but bleeds at boundaries and
never converts (fresh+dilution absorb). HOLE-2 assault = WALLMAX + FULLSPLIT + SG2 + PRESSURE
above: single-pressure slack ≥32 even maximized; disjoint sustain never converts. Verdict: OPEN,
finite-supported safe.

Resume again: assume HOLE-2 → HOLE-1a/1b close → HOLE-1 closes → main contradiction closes.
Remaining:

**HOLE-3 (THIRD HOLE, OPEN): REPEAT-HOLE UNIVERSAL + E2/K TAX UNIVERSALS.**
W-inc≥4 with all-later-episodes-repeats + E4-early + no-returners: 0 finite instances, universal
proof needs repeat-episode W-ladder (each repeat episode consumes finite stale-B pool or
re-anchors supply — sketch only). E2/K episode-companion taxes: companions 7943/7943 finite,
universal needs dormancy + window formalization (W-window tightening queued). Verdict: OPEN.

## End state (honest)

- Conditional theorem: HOLE-1 (≡ HOLE-2+HOLE-3 conjunction) ⟹ GC-STATIC ⟹ GC ⟹ D≤6S_A ⟹ MSTL-14P
  (conditional chain C0–C4 banked).
- Unconditional: GC-STATIC OPEN/NO_WITNESS (70k+ targeted + 2.28M exhaustive, zero shortfall/gap;
  best slack 2 degenerate; large-tight Q3; wallmax press≤2 slack≥32).
- Arsenal exhausted (8O): fresh done; E1/E4-complete exempt; E2 bounded-hole; K ratchet/dilute;
  W transient/sterile + OCC/STEPS; hub narrow-only; pushes 95% impure; runs miskeyed; induction
  circular; fluid/counting forbidden; augmenting circular; DAG/aggregate dead; fourth-use mapped;
  deficit restatement. New idea or violator required.
- Next: old-abundance theorem (bare wall) / splay-model Lean core (aux) / spread-3 (aux).
  Concrete next falsifier: overlap-census at scale (pure-push → next-access rebuild overlap rate)
  + W-ladder formalization attempt (repeat-episode consumption invariant).

## Pointers (sealed files untouched; new: wallmax.json + this file)

- `scripts/wp6_wallmax.py → artifacts/v04/wp6_present/0909c74a/wallmax.json`
  (10k evals, bestpress 2, bestratio 12.0, bestslack 32, zero kill).
- Prior: `pressure.json` (1.5% pressure, ml 0), `fullsplit.json` (sustain 28), `chase.json`
  (95% impure, 0 pure-sustain), `surgical2.json` (10k, slack 27), `rundrain.json` (-24/-29),
  `fourth.json` (7943/7943 multi+companion), `pooldef.json`, `tightest.json`, `offline.json`.
- Lemmas: `hall_lemmas.md` 8A/8B/8C/8E/8H/8I/8J/8K/8L/8N/8O/8P/8Q/8R; AR-01..21 kernel exit 0.
- Ledger: `audits/WP6_BEHAVIOR_VAULT.md/json`, `audits/WP6_PROOF_DAG.md`.
