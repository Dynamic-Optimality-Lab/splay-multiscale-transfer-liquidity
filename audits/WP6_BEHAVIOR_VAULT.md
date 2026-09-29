# WP6 Behavior Vault — persistent proof-search package (Stage B → GC → MSTL-14P)

Companion: `audits/WP6_BEHAVIOR_VAULT.json` (machine-readable, same entries).
Prior state: `audits/WP6_COLD_RECONSTRUCTION.{md,json}` (sealed f44982c, commit 6f89b8b).
Live ledger: `artifacts/v04/wp6/0909c74a/route_kills.json` (append-only this run).
Proof DAG: `audits/WP6_PROOF_DAG.md`.
Status vocab: PROVED_AUTHOR / PROVED_KERNEL / FINITE_EVIDENCE / REFUTED / OPEN /
BLOCKED_EXTERNAL / SUPERSEDED. Finite evidence is NEVER a theorem.

## Prior bank (C14–C27, compact; full detail in reconstruction package)

- Broad MSTL-14 REFUTED (absent battery death_00, ALL_63 cascade) — sealed.
- U=0, D2-raw, tenure T123/need/run-need, L1/Case-A/reduction, M1, K3, Lemma A/B,
  TSTAR-COND, GENESIS-11 (AR-14/15/16 Lean-pending), TRICHOTOMY (Lean-pending) — banked.
- Dead (never resurrect): raw-rotation, per-key attribution, intervals, depth/IPL,
  Psi, splay-distance, one-step hazard, sterilization-strong, X-RETURN-universal,
  old N-FIRST (slack/interval/reset/setup/borderline-as-killer), rank/Bellman@scale,
  SOD-single, raw-dist, quotient-masses/per-run, TSRC, corridor-greedy, perceptron,
  rank-proxy, E3-laminar, E1+E4-only, matroid-free-greedy, per-key-GC (now: dem/3sup
  2.03×, LS-00). Finite: genealogy/ leastload/ singleton/ minload/ anatomy/ tiers/
  e3order(+0.6 ledger-only)/ stock+GC ratios/ coverage/ Bellman-small-n.

## C28 — Stage-B assault (this continuation, HEAD 6f89b8b → new)

### C28-1 ST-00 saturation frame + load-aware turnover [FINITE_EVIDENCE]
Script `scripts/wp6_saturation.py` → `saturation.json`. MA corpus (100 hist, B=3852):
FIRST minload≥2 events: 0/100 histories (stronger minload≤1 holds here).
Entry loads: low0 8494 / low1 6162 / low2 142 / saturated 0. **No saturated source
ever enters** (0/14796). Lost loads: 4014/8337/198/0.
Deep trace t=5 acc6 (x=26): bev33 E3 6→17 explosion (+13 all load-1, hub-hit),
bev34 collapse 17→6 (11 lost all load-1, unconsumed), bev35–38 conveyor (2-in/2-out,
consumed saviors exit at 2), bev39 fresh load-0 entry (aev43), ml→0.
Implication: transient W is a conveyor (enter@1, ~0 picks, exit@1); hub-hit inflates
counts without capacity; drain-then-refresh is the observed rhythm.
Next: MW-00 (find the drain that reaches 2).

### C28-2 BR-00 breaking hunt + bytes/str fix [FINITE_EVIDENCE + TOOLFIX]
Untracked `scripts/wp6_breaking.py` had `TypeError` (str tag into %b); fixed
`Rng.__call__` (encode str). Ran: seeds best-score 2754 best-minload 1;
mutate 2080 evals best-score 3000 **best-minload 2** → `breaking.json`.
First minload-2 ever observed → stronger minload≤1 claim DEAD (as anticipated).
Implication: required minload≤2 (Stage B proper) stays live; need witness → MW-00.

### C28-3 MW-00 minload-2 witness + autopsy [WITNESS BANKED / FINITE_EVIDENCE]
Script `scripts/wp6_m2witness.py` → `m2witness.json` (4000 evals, best 2, reverify 2,
0 starvation). Witness: n=128, H len 38, acc5 KEEP-36, bev88 minload-before=2.
Autopsy: e_B(acc5)=13, e_A=2 → B-heavy (13>6) ✓ danger zone. Core N=9 frozen IDs
(E1{96,97} + E2{81} + E4{117} + E3-persistent{7,57,93}) + ROTATING transient pair
((16,18)→(20,22)→…→(48,50), one pair per step). Drain bev80–88: U 18→9 monotonic;
transients enter@1, picked (small IDs beat core ties) →2, exit@2; core climbs to 2.
bev88: all-2. bev89: E3 expansion (10 members, fresh entries) saves; access continues
(e_B=13 total), best stays 2. Mechanism: frozen-core + transient-pair conveyor drain,
refreshment-rescue. Minload-2 = "drain completes just before refreshment".
Next: AS-00 (can drain complete twice → minload-3?).

### C28-4 LS-00 load-structure discrimination [FINITE_EVIDENCE + 1 REFUTATION]
Script `scripts/wp6_loadstruct.py` → `loadstruct.json` (120 hist, B=7075).
(a) E1-zone: e_B≤2e_A → ml≤1 5554/5554 (0 viol); e_B≤3e_A → ml≤2 5893/5893 (0 viol).
Confirms E1-CAP lemma empirically. (b) Per-key coupling REFUTED: worst dem/3sup
2.03× (x=103) → K-core alone cannot cover; transient sharing load-bearing (matches
killed E1+E4-only). (c) Tie-break ablation: oldest maxload 2/maxml 1/starve 0;
newest maxload 3/maxml 1/starve 0; random maxload 3/maxml 2/starve 0. Oldest-first
keeps max low; NO starvation under any tie-break. (d) Entries by class:
E1@0 (5685+5@1), K 1098@0/1499@1/11@2, W 7838@0/9787@1/191@2, E2 84@0/1971@1/3@2,
E4 726@0, E7(X) 312@0/1675@1/1@2. Max entry load 2 (≈0.6%); never 3.
(e) Picks age med 1 max 33 (recent sources serve).
Implication: E1-CAP bankable NOW; per-key-flow dead; tie-break = maxload-shaper,
not starvation-gate; entry-freshness quantified.

### C28-5 E1-CAPACITY LEMMA [PROVED_AUTHOR]
`artifacts/v04/wp6_present/0909c74a/e1cap_lemma.md`. Pure pigeonhole:
E1(t) sited, 3e_A slots, loads only from access-t B-events; j-th B-event sees
≤e_B−1 prior in-access picks. e_B≤3e_A → some E1 ≤2; e_B≤2e_A → some ≤1.
Closes ALL non-B-heavy accesses for Stage B with zero geometry. GC-independent.
Lean-pending. Dependencies: U=0 + E-eligibility structure only.

### C28-6 AS-00 Stage-B direct falsifier [FINITE_EVIDENCE]
Script `scripts/wp6_advstage.py` → `advstage.json`. M2-seeded + 120 generic seeds +
repeat-key/sustain mutations, 20,000 evals maximizing max_b min-load-before:
best=2, ZERO starvation. Cumulative anti-starvation: 2080 (BR) + 4000 (MW) + 20000
(AS) = 26,080 targeted evals, minload never exceeds 2.
Implication: Stage B (≤2) survives the heaviest direct assault mounted; minload-3
needs TWO consecutive full-drain rounds without fresh injection (never observed).

### C28-7 SV-00 savior anatomy + W-window geometry [FINITE_EVIDENCE]
Script `scripts/wp6_savior.py` → `savior.json` (150 hist, B=9869, 104 minload-1).
Savior classes: W 65 / K 25 / E2 11 / E1 3 (E4 0). **All 104 saviors entered at
load 0.** entry@3: 0. Savior age med 6 max 27 (recent). W-windows (n=46829):
med 1, p90 2, max 10. Transients are 1–2 step visitors; W is the dominant shock
absorber (62%); K backbone (24%).
Implication: five-channel case-split shape (E1 / E2-recent-pusher / K-deposit /
W-injection / E4-setup); survivors are always fresh-entered; formalize W-window
shortness + entry-freshness next.

## Live theory snapshot ( Erwin — hypotheses, NOT theorems)

- H1 PUSHER-SUPPLIES: every B-push of x (M1) creates an E2 edge (pusher's A-StepEvs
  → x's future B-events); B-deepening demand arrives with its own E2 supply. Needs:
  recent-pusher freshness bound (young-transient-exposure bound = THE open gap).
- H2 ROOT-HUB: deep-splay A-rotated tops and B-triple tops meet at root-region keys;
  explains C27 hub-density + bev33-type explosions; sparse (1–2 × 1–2 per pair).
- H3 SWEEP-REFRESH DUALITY (WEAKENED C29-2): long sterile runs exist (max 62) and
  are survivable; sterile length is NOT the gate. Drain length ↔ sweep length
  still structures the drain, but refreshment is not the sole rescue.
- H4 DISPLACE-MONO (rigorous): A-depth(x) non-decreasing between x-accesses → B-heavy
  x had a recent x-access → K holds recent deposits (loads: open - transient leak).
- H5 LAZY-OLDEST: oldest-first + rare-eligibility → dormant sources stay fresh until
  geometry needs them; tie-break shapes maxload (2 vs 3), not starvation (ablation).

## Open gap (exact)

Young/fresh-source transient-exposure bound: sources entering at load 0/1 can be
picked by unrelated B-events (E3-transient) before the B-event that needs them.
No universal bound proved; 0 saturated-entries / 44,000+ observed. Options: (i) W-window
formalization (non-x matches are ancestor-sweep, O(1) stays — SV data: max 10);
(ii) ENTRY-FRESH theorem attempt; (iii) scattering lemma (load-3 convergence);
(iv) five-channel case split with per-channel freshness lemmas.
(DONE C29: AS-01 surgical 12k best=2 maxster=62; EX-00 2.28M exhaustive max≤1.)

## C29 — exhaustive small-n + surgical sterile-run (this continuation)

### C29-1 EX-00 small-n exhaustive Stage-B [FINITE_EVIDENCE]
Script `scripts/wp6_exhaustive.py` → `exhaustive.json`. ALL BST shapes × ALL
histories (bounded L), every H present-legal: n=3 L=7 (5 trees × 279936 =
1,399,680 hist): max minload 0, ZERO minload-2, 0 starvation, 0 MSTL kills.
n=4 L=5 (14 × 32768 = 458,752): max 1, zero minload-2. n=5 L=4 (42 × 10000 =
420,000): max 1, zero minload-2. Total 2,278,432 exhaustive histories.
Implication: minload-2 is scale-emergent (needs depth + large frozen N); small
cases trivially safe (E1-CAP + tiny depths + total overlap). No small
counterexample exists. Next: AS-01.

### C29-2 AS-01 surgical sterile-run falsifier [FINITE_EVIDENCE]
Script `scripts/wp6_surgstage.py` → `surgstage.json`. M1-guided ops (DEEPEN x in
B-only via trial splays, STERILIZE x-ancestors by overlap minimization, STRIKE x,
SETUP x, GENERIC), victim = max (B-depth − A-depth) key, 12,000 evals n∈{64,128}:
best minload 2, ZERO starvation. Diagnostics: max sterile-run (consecutive
B-events with no fresh-0 entry) = 62 — long sterile runs EXIST and are survivable
(fresh-1 entries + core capacity carry them); sterile length is NOT the gate.
Cumulative anti-starvation: 38,080 targeted + 2,278,432 exhaustive.
Implication: H3 sweep-refresh as "the" gate weakened; geometry-targeted attack
fails like generic. Next: ENTRY-FRESH/W-WINDOW or obstruction packet.

### C29-3 load-3 absorption note [FINITE_EVIDENCE]
M2-witness history full replay (B=144): exactly ONE minload-2 event (bev88)
minting exactly ONE load-3 source, absorbed with no further elevation.
minload-2 events are isolated; load-3s are absorbed singletons. Starvation would
need |N| converged load-3s (never observed). Reframes Stage B as "load-3
absorption", but convergence-impossibility still unproved (scattering lemma open).

## C30 — E4 causality fix + scaffold micro-lemmas (this continuation)

### C30-1 E4-FUTURE-LEAK found and fixed [BUG + FIX, banked]
Autopsy of 11 phantom E1@1 entries (MV-00) exposed: `build_flow`, `build2`,
`build_tagged` all used FINAL `setup` dict for per-Bev E4 (future root-arrivals
eligible for past B-events; loads assigned before source creation). Example:
t=5 acc11 E4 = {60,61} with ai=14. Fix: per-access `setups[idx]` snapshot
(causal E4) in all three builders; verified 0 future-leak edges. All consumers
(LL/ML/MW/LS/SV/ST/AS/MV/EX/tiers/cut/flow) inherit fix.
Implication: sealed C23–C27 E4-inclusive numbers were optimistic (extra members
lower minload). REFIX battery (below) shows impact marginal (E4 thin/empty in
practice) — all C28–C29 conclusions STAND. Sealed artifacts preserved untouched
(documented as pre-fix); corrected numbers in `refix.json`.

### C30-2 RF-00 refix battery [FINITE_EVIDENCE]
`scripts/wp6_refix.py` → `refix.json` (fixed builders, new artifact only):
LL 2331/2/0 IDENTICAL; MA 0/100 same; M2 best=2 (at shifted 88→86), maxload 3,
starve 0 — witness survives; E1-zone 5554+5893 0-viol identical + E1@>0 entries
now 0 (phantoms gone); SAV W68/E2-12/K27/E1-3 ≈ same, entry3=0; exhaustive n=3,4
fixed max 0,1 identical; fixed hillclimb 1500 best=1, 0 starvation.
Implication: causality fix changes almost nothing quantitatively; evidence base
is now causally sound.

### C30-3 displace autopsy: raw mono FALSE, per-StepEv form TRUE [REFINED]
Raw "other keys never decrease" FALSE (24–31% bystander rises): splaying w
hoists w's descendant subtrees through series of descendant-position steps
(example: splay 3 lifts key 4 from 12→7). Per-StepEv riser-containment TRUE:
2870 steps, node always x, triple always ∋ x, 0 riser violations (SP-00;
first run's 1322 viols were a stale-root measurement artifact, fixed).
Consequence: H4 weakened (hoists shallow without x-access); hoisted keys create
NO own-key triples (only node-x does) — K-deposits remain the sole per-key
fodder (ML-K-PERSIST), freshness at-creation only.

### C30-4 scaffold banked: 6 micro-lemmas PROVED_AUTHOR [PROVED_AUTHOR]
`stageb_scaffold.md`: ML-E1-ENTRY (5046/0), ML-K-PERSIST (15316/0), ML-ADJ-E4
(65/0, conditional), ML-DISPLACE-STEP (2870/0), ML-RISE-WITNESS (2870/2870),
ML-W-BLOCKS (5562 member-splays ≤3 blocks, maxrun 3; proof-sketch + strong
check — occupancy contiguity flagged for tightening). All GC-independent,
Lean-pending as a block.
Remaining gap (exact): B-heavy all-3 convergence — entry-load ≤2 unproved,
young-transient-exposure unproved, load-3 scattering unproved. No counting
argument attempted (GC-reduction avoided).

## Queued next
- Scattering lemma attempts (load-3 convergence impossibility).
- ENTRY-FRESH theorem attempt (entry-load ≤ 2) or entry@3 hunt at 100k+ scale.
- ML-W-BLOCKS tightening (per-key occupancy contiguity audit).
- Lean: scaffold + E1-CAP arithmetization (after author chain closes).

## C31 — blocker census + run-structure + fresh-channel (this continuation)

### C31-1 BL-00 blocker probe [FINITE_EVIDENCE]
`scripts/wp6_blocker.py` → `blocker.json` (400 hist, B=25,981): max entry-load
2 (entries 54213@0 / 66630@1 / 863@2 — entry@3 ZERO/121k); singletons 16, ALL
load 0; max blockers-per-N = 0 (NO load-3 anywhere in this corpus; M2's singleton
blocker remains the only one ever seen); minload-2 events 0 (rate 0.00000).
Singleton anatomy (5 recorded): ALL acc=0/bev=0/age-0/E1 — history-start boundary
(first B-event, single genesis A-StepEv), NOT a mechanism. Mid-history singletons
essentially never occur (would need first-x-access + depth-1 + parent-never-
accessed + no-pumps + sterile sweep).
Implication: blockers need the rare frozen-drain to be minted; minted blockers
are ejected (conveyor) and never re-enter@3; convergence pressure ~nil. But
ENTRY-FRESH (≤2) still unproved as universal; singleton-freshness is boundary,
not mechanism. Next: run-structure (C31-2).

### C31-2 ML-RUN-STRUCTURE + ML-FRESH-CHANNEL [PROVED_AUTHOR]
Derived (not fitted) from banked laws; appended to `stageb_scaffold.md`:
- RUN: at most ONE KEEP per x-run has e_B>0 (the first). Proof: B moves only at
  KEEPs (B-freeze T3); after first x-KEEP x is B-root; run-interior DELETEs skip
  B; later x-KEEPs are B-no-ops (splay-at-root). DELETEs never demand.
- FRESH-CHANNEL: every demanding KEEP (e_B>0) has E1≥1 sited-fresh OR
  (E1=∅ AND E4 = pristine accA[s], e_A(s)≥1, s = run-start DELETE).
  Proof: demanding ⟹ KEEP. H[t-1]≠x ⟹ x A-nonroot ⟹ e_A≥1 sited (U=0).
  H[t-1]=x + demanding ⟹ t-1 is DELETE (KEEP→KEEP repeat is B-no-op) ⟹ DELETE-run
  ⟹ run-start s had x nonroot ⟹ setup[x]=s, e_A(s)≥1; interior all-x (no transient
  picks) + no interior KEEPs before t (first) + DELETEs emit no B-events ⟹ E4
  loads exactly 0 at t. E1/E4 COMPLEMENTARITY (E1=∅ ⟹ E4-pristine-nonempty;
  E4=∅+demand ⟹ setup==idx ⟹ E1≠∅; genesis corner demands nothing).
- FRESH-CAP (subsumes E1-CAP): demanding KEEP with e_B ≤ 3f (f = fresh slots)
  ⟹ minload ≤ 2 (pigeonhole; fresh loads ≤ in-access picks only).
Dependencies (all banked): Pair Access DELETE-skips-B, B-freeze T3,
root-dislodge, U=0, setup rule, ML-E1-ENTRY, ML-ADJ-E4. GC-independent.
Remaining: B-heavy overflow (e_B>3f) onto old (K/E2/W) — unchanged open gap.
