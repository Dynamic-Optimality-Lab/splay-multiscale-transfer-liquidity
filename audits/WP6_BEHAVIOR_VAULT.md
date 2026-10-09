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

## Queued next (SUPERSEDED ordering note: C31–C37 below are positionally scrambled
by sequential edit order — follow entry IDs/dates, not file positions; live
queues: the STALE-marked one is dead; the LIVE queue sits just before C37)

## C33 — margin probe + near-miss feeder (this continuation)

### C33-1 MG-00 safety margin: synchrony + dilution + negative margins [FINITE_EVIDENCE]
`scripts/wp6_margin.py` → `margin.json` (300 hist, B=19,982): margin min −54,
p1 −11, med 49. Spread: ALL events {0:944, 1:18445, 2:593} (≤1 at 97%);
AT DRAINS (min≥1, n=192): {0:97, 1:95} — spread NEVER exceeds 1 at drains.
DRAINS ARE SYNCHRONOUS (whole-N water level, range ≤1). Dilution: per-access
fresh0 med 6 vs e_B med 2; fresh0<e_B only 7.5% (dilution usually covers demand
numerically at access start). Negative optimistic margins (~1% of events) are
arithmetically starvable moments that did NOT starve (waste/churn rescued).
15 near-misses (margin≤2) recorded as falsifier seeds.
Implication: race formulation exact (uniform level vs rescue); spread-3 needs
dormancy+return+ladder conjunction (0/19982) — candidate sub-lemma. Next: NM-00.

### C33-2 NM-00 near-miss feeder: negative margins do NOT convert [FINITE_EVIDENCE]
`scripts/wp6_nearmiss.py` → `nearmiss.json`: 40 negative-margin seeds (worst −48)
+ generic pool, freeze-N-biased mutations, 8000 evals maximizing minload (tie-break
min margin): best minload 2, best margin −31, ZERO starvation. Even from
arithmetically-starvable states with rescue-suppressing mutations, waste/churn/
dilution always intervene (picks scatter onto exited-W, refreshment arrives, N
churns in fresh members). Frozen+long contradiction: frozen-N needs sterile sweep;
long sweep hits hubs (refreshment); sterile-long (maxster 62) still gets fresh-1
+ core carry. The perfect-placement conjunction is dynamically forbidden.
Cumulative: 46k+ targeted, 2.28M exhaustive, 121k-entry census, 30k entry-hunt.

## C32 — ENTRY@3 found + ladder-episode theory (this continuation)

### C32-1 EH-00 entry@3 hunt: ENTRY-FRESH-as-universal DEAD [WITNESS + AUTOPSY]
`scripts/wp6_entryhunt.py` → `entryhunt.json` (30,000 evals, re-entry bias):
ENTRY@3 at it=43 (B-event 118, aev 40). No starvation in 30k (Stage B holds;
entry@3 needs convergence, not yet seen). M2 side-check: load-3 (aev7, minted
bev86) + transient re-entries@2 in-drain (pairs cycling 1→2, the conveyor).
### C32-2 ladder autopsy: the complete load-formation mechanism [MECHANISM]
aev40 biography (genesis ai=0, E3-only, 12 eligibility events): bev4 ENTER@0
(unpicked) → dormant → bev45 (acc2) ENTER@0 PICKED (0→1) → dormant 46–74 →
bev75 (acc3) ENTER@1 PICKED (1→2) → dormant 76–105 → bev106 (acc12) ENTER@2
PICKED (2→3) → bev118/121/129/133/136/138 ENTER@3 as dead weight (never picked;
others ≤2 serve). LADDER: re-entries climb 0→1→2→3 across ≥3 pick-episodes
separated by dormancy; completed ladders persist as blockers; blockers are
ejected by triple-motion (conveyor) and absorbed.
Synchrony: drains elevate whole N's together (M2 bev80–88 all→2); dilution:
each x-access deposits e_A fresh-0 (race: e_B drain vs e_A + W-refresh supply).
Starvation ⟺ |N|-fold synchronized ladder completion before rescue (e_B bound
+ refreshment + access-end). Never observed (38k targeted + 30k entry + 2.28M
exhaustive + 121k-entry census).
Same-key-return note: aev40's episodes are CROSS-SPLAY (acc 2,3,12,15,17,18,21,
22,23) — compatible with ML-W-BLOCKS ≤3/splay (MV 829 = within-splay multi-key
blocks). Cross-splay return is the ladder vehicle.
Remaining (exact): synchronized-ladder-completion impossibility (scattering);
deposit-dilution race formalization. No counting attempted (GC-reduction avoided).

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

## Queued next (STALE — superseded; live queue at file end before C37)

## C35 — K-0 necessity split: gate → buffer (this continuation)

### C35-1 K0-00 exact split [FINITE_EVIDENCE]
`scripts/wp6_k0split.py` → `k0split.json` (DL corpus, 202 B-heavy accesses):
elevated K0==0: 21/25 (NOT universal — 4 elevated with K0 = 1,1,1,6).
Safe K0==0: 59/177 (sufficiency fails: no-buffer but short/absorbed drains).
Elevated E10==0: 0/25 (E1-0 ALWAYS present, eaten as buffer); W0==0: 22/25;
E40==0: 25/25. All 25 elevated are case-a; case-b heavy 5/5 safe (incl. e_B=32
with f=2 — E4-pristine + old-zeros carry 26 overflow picks at 0).
eB med 12 (elevated) vs 8 (safe); elevated K0≥1 cases all thin-fresh (f=1–2).
REFINEMENT: K-0 is an absorption BUFFER (|K-0| picks), not a gate. Elevation
signature: case-a + thin fresh (f=1–2) + long drain (e_B 8+) + pre-elevated old
(K-0=0 in 84%) + W0=0 (88%). Elevation ⟺ drain-picks > buffers (margin view,
C33). No new proof (buffer arithmetic = margin arithmetic); K-0 necessity as
universal REFUTED (21/25).

## C34 — dilution-zero + K-ratchet (this continuation)

### C34-1 DL-00 dilution probe [FINITE_EVIDENCE + 1 PROOF]
`scripts/wp6_dilution.py` → `dilution.json` (250 hist, B=16,335):
DILUTION-ZERO 9252/9252 0-viol (e_B ≤ f_struct ⟹ minload 0 throughout).
B-heavy (n=202): ml0=177 vs ml1+=25; K-0 med 3 vs 0 — K-0 absence characterizes
elevation (round-2+ gate); E2-0/W0 meds 0/0 (thin at start; W arrives mid-splay).
### C34-2 ML-DILUTION-ZERO + ML-K-RATCHET banked [PROVED_AUTHOR + WARNING]
Scaffold (`stageb_scaffold.md`): DILUTION-ZERO proof (fixed-fresh no-exit +
pigeonhole; strengthens E1-CAP deep zone); K-RATCHET (i) old-K monotone across
x-accesses PROVED, (ii) fill-order descriptive. WARNING banked: water-filling as
closure ≡ GC ≡ forbidden endpoint (discard); race inequality stays empirical.
Counting/fluid paths to all-3 exhausted without exception (all reduce to L0/GC);
remaining hope is purely geometric (episodes/returns/blocks).

## Queued next (LIVE)
- Offline-matchability assault at scale (Hall hunt 30k+; kill GC-STATIC or not).
- GC-direct prefix-gap assault (kill GC or not).
- Min-cut anatomy WITH E3 (proof-relevant cut object for GC-STATIC attempt).
- N-FIRST/N-AUG-credit re-derivation via offline assignment.
- MSTL-14P composition (D2+GC stock, k=6, rho, collapse, conservation, service).

## C37 — STAGE B REFUTED + offline fallback alive (this continuation)

### C37-1 SC-00: spread3 + 2-blockers + STARVATION [KILL WITNESSES]
`scripts/wp6_spread.py` (25k budget): SPREAD3 at it=1063, 2-BLOCKERS at it=1576
(witnesses LOST — early return before persist; method lesson: persist
incrementally; subsumed by kill below), blockers 9→10, then STARVATION it=18913
(`starve.json`, H len 46, n=128 implied). First minload-3 ever: online greedy
starves. No banked lemma contradicted (all kills in open zones — verified C37-2).
### C37-2 MZ-00: minimized kill + anatomy + mechanism [WITNESS BANKED]
`scripts/wp6_starvemin.py` → `starve_min.json`: 46→9 accesses, B=112, best
minload 3, first starve bev110 (acc8 KEEP-19, e_A=1, e_B=7): N=5 ALL at load 3
(E1{98 age0} + E2{96 age3} + K{8 age8} + W{52,56 age8}; E4 empty).
E1-CAP/FRESH-CAP/DILUTION-ZERO consistent (e_B=7 > 3·1: B-heavy open zone).
MECHANISM (fresh-key drain): minimized H walks FRESH keys (10→12→18→19) through
shared triple geometry with setup chain (1,20,12,10); each access demands
overflow from the SAME old pool (genesis acc0 A-StepEvs 8,52,56 + acc5 pump 96)
while deposits go to unrevisited keys (miskeyed supply); E1-98 sprints 0→3
in-access (3 of 7 picks); synchronized convergence at bev110. Scattering broken
by geographic concentration (shared zone revisited via fresh keys).
### C37-3 OF-00: offline survives killer + 6k adversarial [FALLBACK ALIVE]
`scripts/wp6_offline.py` → `offline.json`: killer Hmin offline max-flow
shortfall 0/112 (online myopia ≠ structural deficit — same demand placeable
offline). 6000 adversarial: worst shortfall 0, worst GC-gap 0 (no Hall violator,
no GC kill). GC-STATIC conjecture (offline cap-3 causal assignment always
saturates) has first finite evidence. LEDGER PATH: past-only offline assignment
suffices for accounting (existence, not online construction); online-vs-offline
audit point flagged for author-proof (no future info in edge direction; full-
history accounting is standard amortized practice — to be audited, not assumed).
IMPLICATION: Stage B REFUTED (terminal-B for the online theorem); GC and MSTL-14P
NOT refuted (zero witnesses); MSTL-14P chain must rebuild via offline (queued
above). All scaffold/zone/geometry lemmas UNAFFECTED (nonemptiness, zones,
fresh channels, blocks, kernel AR-01..19 — none relied on minload≤2).

## C36 — kernel upgrade: AR-01..19 exit 0 (this continuation)

### C36-1 toolchain found + AR-08 repaired [PROVED_KERNEL]
`lean.exe` v4.21.0 present via elan (prior "no toolchain" stale).
`lean/WP6/MSTL14PArith.lean` FAILED at AR-08 `capped_gain` (omega treats
`Nat.min` opaquely — uninterpreted atom, unprovable). Repaired with lattice
proof (`min_le_right` + `le_add_left` transitivity; two elaboration iterations
needed:elsion order + left-vs-right). Full file re-checked: EXIT 0.
STATUS comments in-file updated (were "kernel check PENDING").
### C36-2 StageBArith.lean: AR-17/18/19 trio [PROVED_KERNEL]
New `lean/WP6/StageBArith.lean`: freshcap_two/one + dilution_zero (exact Nat
pigeonholes behind FRESH-CAP/DILUTION-ZERO; f≥1 from FRESH-CHANNEL; used≤eB−1
Layer-A). Direct `lean` EXIT 0, no sorry/admit/axioms.
UPGRADE: AR-01..05 (confirmed) + AR-06..16 (skeleton→kernel) + AR-17..19 (new)
= full arithmetic backbone AR-01..19 PROVED_KERNEL. Scaffold status updated.
Still Lean-pending: splay-model formalization (trichotomy, K-persist, risers)
+ pool-close composition (AR-09 pool_step checked; close-iff-prefix is Layer-A
prose + OPEN B-source — correctly open).

## Queued next (LIVE)
- N-FIRST/N-AUG-credit re-derivation via offline; MSTL-14P composition.
- Splay-model Lean core.
- Spread-3 conjunction (dormancy proof).

## C39 — min-cut+E3 anatomy + GC-direct assault (this continuation)

### C39-1 MC-00 min-cut anatomy [FINITE_EVIDENCE]
`scripts/wp6_mincut.py` → `mincut.json` (150 hist, B=10,088): E1+E2+E4-only
fails 44/150 (29%); E3 SAVES all 44 (E3 necessary for offline saturation).
Optimal-flow load hist: 0:10580 / 1:940 / 2:425 / 3:2766 (packs to cap; most
mass at 0). Cross-access shared-N med 18 max 117 (§12 glue burden large —
per-access decomposition would triple-count massively).
### C39-2 GA-00 GC-direct assault [FINITE_EVIDENCE]
`scripts/wp6_gcattack.py` → `gcattack.json` (B-heavy sustain + concentrated
walks + long histories + killer-seeded): 15,000 evals, best prefix gap
(E_B−3S_A) = 0, ZERO GC kills. Cumulative raw-GC: 41k+ evals (OF-6k + HH-20k +
GA-15k) gap never >0. GC holds everywhere tested; still OPEN (unproved).

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (the one wall).
- ML-W-BLOCKS tightening; spread-3 dormancy proof (auxiliary).
- Splay-model Lean core (auxiliary; does not block author chain).

## C40 — 8H fresh-bound + credits resolution + conditional chain (this continuation)

### C40-1 8H HALL-FRESH-BOUND + NONHEAVY-Q [PROVED_AUTHOR]
`hall_lemmas.md`: Delta(Q) ≤ Σ_{B-heavy Q-accesses} (e_B−3f) via pairwise-
disjoint fresh sets (E1 fresh ids; pristine-E4 distinct setups across runs;
mixed E1/E4 double-duty with both demanding IMPOSSIBLE by setup-update + RUN
contradiction — genesis corner demands nothing). Hence non-heavy Q never
violates. Halves Hall (non-heavy done); B-heavy overflow + shared-old remains.
### C40-2 N-FIRST/N-AUG outcome B both [RESOLVED]
`audits/WP6_CREDITS_RESOLVE.md`: no freestanding theorems exist (grep-verified);
downstream consumes prefix counts + LIQ0 only (§14 audit: no persistent matching
needed; MSTL-14P.md + LIQ0 + D2/D6 verified, no N-FIRST edge). Obligations mapped:
first-cash + subsequent funding = GC-STATIC vertices; N-AUG content (genuine ids,
cap 3, dormancy≠clone, re-entry≠new-cap, sharing=edges, past-only) = flow-
construction properties (true by construction). Old formulations stay REFUTED;
labels SUPERSEDED_BY_GC_STATIC (conditional; corollaries automatic with GC).
Residuals/borderline/tenure-cargo are states-not-demand (E2/E3 edges represent).
### C40-3 conditional composition map [CONDITIONAL PROOF]
`audits/WP6_CONDITIONAL_CHAIN.md`: GC-STATIC (OPEN premise, the only one) →
C1 accounting-validity (conditional author proof: matching→counts, U=0, DELETE
inclusion, no double-count, prefix conventions) → C2 GC → C3 D6 (D2 + AR-13
kernel + §21 audit vs banked defs/code lines) → C4 service → MSTL-14P (§22
ten-point audit vs legacy_embedding.py:164-246 + LIQ0 banked units) → C5
downstream preserved (§23: 14P OPEN needs C4; 15P/17P/18P/19 untouched).
Support-collapse mapping: no such repo object (grep-verified); LIQ0-06 +
cumulative reduction used instead (terminology mapping, not gap).
Kernel reverified exit 0 (AR-01..21); StageBArith arithmetic-only (§24.2
observed: refuted online Stage B not represented as proved).

## Queued next (LIVE)
- Min-cut anatomy WITH E3 (proof-relevant cut object for GC-STATIC attempt).
- Offline-matchability assault at scale (Hall hunt 30k+).
- GC-direct prefix-gap assault.
- N-FIRST/N-AUG-credit re-derivation via offline; MSTL-14P composition.

## C38 — Hall program: generic lemmas + PEEL verdicts + 20k hunt (this continuation)

### C38-1 status hygiene §25 [AUDIT]
65-key ledger verified: Stage-B-online REFUTED (killed_stageb), least-loaded
realization REFUTED (same), offline GC-STATIC OPEN (alive_offline), raw GC OPEN
(no witness). Four strengthening-kills consolidated to explicit ledger key this
round: spread≤2 REFUTED (spread 3, SC log), blocker-count≤1/2 REFUTED (9–10, SC
log), ENTRY≤2 REFUTED (entry@3, entryhunt.json), permanent ejection REFUTED
(aev40 re-entered@3).
### C38-2 hallcore tool + killer/M2/ENTRY@3 runs [FINITE_EVIDENCE]
`scripts/wp6_hallcore.py` → `hallcore.json` (maxflow + verified min-cut +
tight sets + CAP3-PEEL + 4-core anatomy + latest-access boundary): killer
112/112 saturate, PEEL EMPTIES (tightest acc8: Q=7 N=18 slack 47); ENTRY@3
140/140 saturate, PEEL EMPTIES (tightest acc10: Q=2 N=14 slack 40); M2 144/144
saturate BUT PEEL STALLS at 42-residual, mindeg EXACTLY 4, Delta −183, connected,
acc span 2–37. CAP3-PEEL-as-universal REFUTED (stalls without Hall failure);
GC-STATIC unaffected (banked distinction).
### C38-3 generic minimal-Hall lemmas + Lean cores [PROVED_AUTHOR + KERNEL]
`hall_lemmas.md`: 8A MINIMAL-DEFICIT-ONE, 8B DEG≥4 (Q'=∅ boundary closed),
8C CONNECTED-CORE (all vertices edged via N-def + trichotomy-nonemptiness),
8E LATEST-ACCESS (E1(L)-only-same-access; violator |Q_L|≥4 or repeat-L),
8F ONE-ACCESS-HALL (open, same wall fractal), 8G E2-HOLE (DELETE→KEEP pushers
leak E2 attribution; triple-exception conjunction; open).
Lean `StageBArith.lean`: AR-20 deficit-one forcing + AR-21 peel-step identity
exit 0 (AR-21 needed no-truncation hypothesis 3n≤q — genuine edge, honest fix).
### C38-4 HH-00 20k Hall hunt [FINITE_EVIDENCE]
`scripts/wp6_hallhunt.py` → `hallhunt.json` (geographic-walk bias per C37
mechanism, killer-seeded): 20,000 evals, shortfall 0 throughout, no GC kill;
best (min) slack = 2 (tight sets exist, none deficient). Cumulative offline:
26k+ evals + killer/M2/ENTRY@3, zero shortfall.
OPEN (exact): GC-STATIC (old-abundance structural theorem); one-access Hall;
E2-hole conjunction (BOUNDED C41: repeat-cycles anchor supply; residual =
sterile-thin-heavy conjunction); min-cut+E3 anatomy; credit re-derivation;
MSTL-14P comp.

## Queued next (STALE — superseded by C42 queue at file end)

## C41 — GC-STATIC assault: near-miss persistence + residual/induction frame + augmenting anatomy (this continuation)

### C41-1 TQ-00 + LT-00 near-miss persistence [FINITE_EVIDENCE + METHOD FIX]
`scripts/wp6_tightest.py` → `tightest.json` (12k evals, incremental persist):
best slack 2 is a DEGENERATE singleton (minimized lenH=1: single KEEP-126,
1v1 E1+E3) — smallness, not pressure. `scripts/wp6_largetight.py` →
`largetight.json` (12k, Q-growth): best Q=3 slack 6; NO large tight set —
B-events constantly expose new sources (DIVERSITY: every 10 B-events touch
≥6 distinct sources). Near-miss lesson: min-slack alone misleads; large-tight
is the violator shape, and it never forms.
### C41-2 8I/8J/8K: residual theorem + extreme-access + induction frame [PROVED_AUTHOR]
`hall_lemmas.md`: 8I Q-specific fresh/overflow (naive e_B−3f corrected to
|Q_j|−3|F_j∩N|); 8J |Q_L| ≥ 3|U_L|+1 with U_L ⊇ E1(L) (repeat-L = demand-
without-supply habitat; violator latest access B-heavy or repeat); 8K reverse
induction (strong induction on |Q|; step needs ONLY old-new sufficiency at
B-heavy Q-blocks; slack-transfer unified, non-circular, non-GC-equivalent).
Single missing lemma isolated: old-new sufficiency (≡ old-abundance §10).
### C41-3 AP-00 C37 augmenting anatomy [MECHANISM]
`scripts/wp6_augment.py` → `augment.json`: greedy starves bev110 (N all-3);
optimal 112/112 with E3-only 107/112 (E1-alone 0!). Repair path
B110→A96→B63→A5 (length 3): optimal puts bev110 on 96, evicts a greedy unit to
A5 (greedy-spare load 2, dormant-neglected). Resource: E3-dense connectivity +
scattered spare capacity. Circularity flagged: spare-existence ≡ GC-flavored
(augmenting route = §8K in disguise; banked as mechanism, not proof).
### C41-4 E2-hole bound + diversity law [REFINED]
`hall_lemmas.md` 8G: supply-free pushing needs repeat-cycles that always anchor
supply at run-start (E1 fresh / pristine-E4 for victim's KEEP); residual hole =
E2-misses-DELETE-half + hub-luck + sterile + thin + heavy conjunction.
Diversity law (finite): tight sets stay tiny (min-slack singleton; large-tight
max Q=3) — union growth outpaces demand concentration everywhere tested.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; induction leverage dead).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C42 — UL-sufficiency fails; induction circular; zone+short hunts clean (this continuation)

### C42-1 UL-00 old-new sufficiency probe [FINITE_EVIDENCE]
`scripts/wp6_ulsuff.py` → `ulsuff.json` (250 hist, B=15,620, 187 B-heavy
blocks): U_L-sufficiency (|U_L| ≥ |Q_L|/3) FAILS (margin min −6.00, p5 −1.33;
12 violations, e.g. Q=13 with U_L=1). U_L class split: old:E3 2174, E1 386
(W-first-overlaps dominate new supply). Strong-step dead empirically.
### C42-2 carry autopsy: 8K-sufficiency CIRCULAR [BANKED HONESTLY]
`hall_lemmas.md` 8L: carry (d_L ≤ sigma_{prev}) ⟺ Hall(Q itself) biconditional
— assuming carry proves the goal. 8K induction DEAD as proof strategy (§25-trap
caught live). STANDS: 8J-necessary, sigma-identity (algebra), UL-measurements.
Carry-holds-on-full-histories (187/187) = shortfall-0 restated (adds nothing).
### C42-3 ZH-00 zone hunt + short-concentrated hunt [FINITE_EVIDENCE]
`scripts/wp6_zonehunt.py` → `zonehunt.json`: 15k sustained shared-zone walks
(40–70 accesses, zone-confined): shortfall 0, best slack 5 (acc3 slice — long
walks self-supply via per-access E1). Inline short hunt (L 5–12, zone-confined):
8k evals, 0 kills. Pool-exhaustion via sustained walks does not occur (hub-E1
supply holds it). Cumulative offline: 26k + 15k + 8k + 2.28M exhaustive +
killer/M2/ENTRY@3, zero shortfall.

## Queued next (STALE — superseded; live queue at file end)

## C43 — ML-HUB + short-hunt + carry-ordering fix (this continuation)

### C43-1 8M ML-HUB (connectivity only) [PROVED_AUTHOR]
`hall_lemmas.md`: last B-StepEv of every nontrivial B-splay E3-adjacent to last
A-StepEv of every nontrivial past A-splay (root-zig both sides; code-pinned
push/inv construction; node-always-key verified). Hub-bank-vs-deep-KEEP has no
universal sign (deep KEEPs outrun 3/access; all-deep-Q avoids hub) — NO counts
content (hub = the model itself); first-top-injection real but offsettable. No
violator-contradiction (deep-KEEP + all-deep-Q consistent; hunts clean).
### C43-2 short-concentrated hunt [FINITE_EVIDENCE]
Inline (L 5–12, zone-confined, from zone machinery): 8k evals, 0 kills.
Cumulative offline now 26k + 15k + 8k + 2.28M + killer/M2/ENTRY@3.
### C43-3 carry-ordering + file hygiene [MAINTENANCE]
8M/8L header repairs in `hall_lemmas.md` (edit-orphan fixes, content intact);
vault ordering notes current (follow IDs/dates).

## Queued next (STALE — superseded by C45 queue at file end)

## C44 — fourth-use assault: ascent falsified, episode-tax banked, DAG/aggregate dead (this continuation)

### C44-1 FT-00 fourth-use ascent test [REFUTED + CLASSIFIED]
`scripts/wp6_fourth.py` → `fourth.json` (200 hist, 3045 Qs full-B + access
slices, 31,331 deg≥4 sources): FOURTH-USE ASCENT FALSE — fails E1|E3 2859
(same-access E1 ties), E2 769 (complete concentration), E3 93, rest scattered.
Pure-W corrected (S-disjoint + W-inc>0; earlier flag polluted by E2-complete).
§27.8 classification done: E1/E2/K/E4-complete exempt (§21.A fresh machinery).
### C44-2 8N episode-tax [PROVED (W-conditional) + DAG/AGGREGATE DEAD]
`hall_lemmas.md` 8N: K-inc (S∋x: complete/access) vs W-inc (S∌x + E3-tagged:
≤3/splay by OCCUPANCY — rigorous) vs complete-class others. W-inc≥4 ⟹ ≥2 splays
FORCED, verified 7943/7943 multi-episode; companions 7943/7943 (repeat-hole
EMPTY finite; open universal). DAG (§27.10/13) DEAD: E1-complete + B-heavy give
companionless deg≥4 maximals (structural, not rare). AGGREGATE DEAD: one later
E1 companions unboundedly many earlier pressures (sharing ∞, no finite C).
Net: W-conditional-tax + E1-exemption stand; closures dead; wall unchanged.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; supply avenues exhausted).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C45 — pool-deficit diagnostic + supply-avenue exhaustion (this continuation)

### C45-1 PE-00 pool-deficit hunt [FINITE_EVIDENCE]
`scripts/wp6_pool.py` → `pooldef.json` (overflow-biased holders, 12k evals):
best deficit (overflow − 3·R_old) = −6 (never positive). Full-B deficit ≤ 0
universally here — but full-B form is TOOTHLESS (R_old massive by construction).
Sharp per-Q form = one-access-Hall+ (open, wall); single-access deficit =
Delta exactly (so deficit-hunt there ≡ shortfall-hunt, 46k+ clean).
Deficit>0 does NOT imply Hall kill (buffers dropped); violator ⟹ deficit>0
(necessary only). Pressure map, not kill path.
### C45-2 8O pool-deficit bound + exhaustion audit [PROVED_AUTHOR (bound)]
`hall_lemmas.md` 8O: Delta(Q) ≤ overflow(D_Q) − 3·R_old(Q) =: deficit(Q)
(fresh-partition + per-access split; demanding-only disjointness).
Supply avenues with verdicts: fresh ✓ done; E1/E4-complete (no forcing);
E2 (hole-y, bounded); K (ratchet/dilute); W (transient/sterile, OCC/STEPS);
E7 (+2); hub (counts-nil); pushes (zone-mismatch); runs (miskeyed); induction
(circular); fluid (forbidden); augmenting (circular); DAG/aggregate (dead);
fourth-use (mapped); deficit (restatement). NO avenue untried: new idea or
violator required.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C46 — K-vs-W necessity + fourth final numbers (this continuation)

### C46-1 mincut E3K split: K saves half, W necessary [FINITE_EVIDENCE]
`scripts/wp6_mincut.py` (E3K filter: E3 members whose rotated contains splay
key) → `mincut.json` extended (same 150 histories, deterministic rerun):
E124-fail 44/150; E3-saves 44/44; K-saves 22, K-fail 22. K-persistent alone
covers HALF the E3-dependent cases; genuine W-transients NECESSARY in 15%
(22/150). W not redundant; K does not subsume W. Optimal loads unchanged
(0:10580/1:940/2:425/3:2766); glue med 18 max 117 unchanged.
### C46-2 fourth rerun final (incidence-split + rephole) [FINITE_EVIDENCE]
`scripts/wp6_fourth.py` + `fourth.json` (committed this round; reruns were
reported textually in C44): K-inc vs W-inc incidence-exact split (K-inc:
S∋x + ai≤acc + sited, complete/access; W-inc: S∌x + E3-tagged, ≤3/splay OCC);
W-inc≥4 ⟹ multi-episode 7943/7943, companions 7943/7943; repeat-hole 0
(W-inc≥4 + all-later-repeat + nocomp: none); E2/K-episode companions 12021/0.
E1/E2/K/E4-complete exempt (single-access concentration needs no episodes).

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; hub dead, displacement-coupling open).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C47 - ML-HUB refuted + surgical fizzle + displacement coupling (this continuation)

### C46-1 ML-HUB autopsy: REFUTED with exact witness [REFUTED]
C37 killer acc8-top B-triple [18,19,123] vs past A-last-triples acc0 [1,128],
acc1 [1,20], acc2 [12,20], acc3 [1,10,12], acc5 [10,12]: FIVE of six disjoint
(only acc6 [12,18,20] meets at 18). Root MIGRATES every access (rotations
involving root descend it; mid-splay transient roots differ per step) — no
universal hub key exists. C43 "root" conflated pre-splay label with triple
membership. Narrow SYNC-HUB survives (x-top ∋ B-root-before + w-access triples
∋ w ⟹ overlap {w}; needs w-access nontrivial-A; killer w=18 via trivial acc7
→ hub EMPTY, consistent). aev97 connects via pushed-18 (zone, not hub).
Sites all True (U=0 intact — no kill there).
### C46-2 SG-00 surgical first-x-strike: FIZZLE [FINITE_EVIDENCE]
`scripts/wp6_surgical.py` → `surgical.json` (first-x + zone-avoidance +
repeat-pushers, first-x discipline preserved by mutations): 8k evals, shortfall
0 throughout, best slack 34 (LOOSE). Strikes stay safe because B-heavy needs
asymmetric displacement (supply-touching) while undisplaced x isn't heavy
(E1 covers at T0-depths). Autopsy → 8P displacement-supply coupling (refined
conjunction: avoidance + repeat-holes + sterile, all three; open).

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; push/avoidance incompatible (finite)).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C48 - surgical v2 + push/avoidance incompatibility (this continuation)

### C48-1 SG2-00 T0-shallow first-x strike [FINITE_EVIDENCE]
scripts/wp6_surgical2.py -> surgical2.json (victim T0-depth<=6 (E1 1-3 naturally thin), first-x discipline, repeat-pushers, avoidance, sterile bias): 10k evals, shortfall 0, best slack 27. Sharper than SG-00 yet fizzles identically.
### C48-2 strike-shape diagnostic: pushing/avoidance incompatible [FINITE_EVIDENCE]
300 surgical-style histories: e_A<=2 at strikes (64, shallow ok) but e_B>=8 NEVER (0) - B-deepening fails under avoidance+shallowness. Pushers B-paths through x force A-contact (synced roots correlate shapes) or miss x in B (no push). E2-alone arithmetic suggests E2 nearly covers first-x demand; root-pusher fraction bounded single-shot+rebuild. Residual = sterile-rebuild sustain (open). hall_lemmas.md 8P sharpened.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; decoupled regime also safe by supply).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C49 - DELETE-heavy decoupled regime + big-n assault (this continuation)

### C49-1 DH-00 DELETE-heavy falsifier [FINITE_EVIDENCE]
scripts/wp6_delheavy.py -> delheavy.json (80-90 percent DELETEs (trees decoupled: A advances alone, B frozen stale), rare shared-zone KEEP pushers/strikes): 15k evals, shortfall 0, best slack 2 (cut singleton). Autopsy: decoupled regime is SAFE BY SUPPLY (each DELETE banks deep A-supply with zero B-demand; E_B tiny vs 3*S_A huge). Sterile-prone in theory, supply-rich in fact. (Artifact hygiene: script wrote evals only on improvement; final count 15000 restored programmatically + final-write added to DH/LT scripts; same fix applied to largetight.json 12000.)
### C49-2 BN-00 big-n assault [FINITE_EVIDENCE]
scripts/wp6_bign.py -> bign.json (n=256/512 vines + balanced, walks + shallow strikes + B-heavy bias): 5.5k evals (B to 611 events), zero shortfall, zero GC-gap. E2 scales with pushes at scale (supply tracks demand); no new scale regime breaks. Cumulative offline now 60k+ targeted + 2.28M exhaustive + killer/M2/ENTRY@3, zero shortfall, zero GC-gap.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; pushing is 95 percent impure).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C50 - chase-pusher conjunction dynamics (this continuation)

### C50-1 CH-00 chase falsifier [FINITE_EVIDENCE]
scripts/wp6_chase.py -> chase.json (victim T0-shallow, first-x discipline; greedy sustain of push+avoid+sterile+hole conjunction; breakdown by leg): pushes sustain to maxpush 22 then stall at B-bottom (nothing below to push with); tags over all picks: displace+overlap+nonhole 1352, overlap+nonhole 932, pure (0,0,0) 115, others 20. Pushing is 95 percent impure (supply-creating); pure pushes exist singly (5 percent) but NEVER sustain (0 pure-sustain histories). Strikes after sustained pushes saturate (supply arrived via impurity). Bugs fixed en route: positioner B-replay missing; hole-pusher skip (trivial-A is the hole!); pushes-var collision; far-below splashes LIFT x (pushers must be nearby-below: splash-30 3->2 vs splash-123 3->4).
### C50-2 displacement-supply in numbers [FINITE_EVIDENCE]
Pushing B-deep while holding A-shallow+sterile fails because pushes inherently touch (displace in A and/or overlap triples) 95 percent of the time; the 5 percent pure pushes are single-shot dead ends (next step stalls or goes impure). E2-hole pushers (trivial-A + real-B-splash) exist but cannot chain (single-shot + rebuild-supply). Consistent with SG/SG2 fizzles, AS-01 maxster, 8P coupling.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C51 - E2-solo coverage ladder (this continuation)

### C51-1 mincut E12/E12K ablation [FINITE_EVIDENCE]
scripts/wp6_mincut.py extended (E12 = E1+E2 only; E12K = +K-persistent) rerun same 150 histories (deterministic): E12-fail 44/150 (SAME 44 as E124: E4 saves ZERO marginal over E1+E2 here); E12K-fail 22/150 (K saves the same 22 E4 could not). Necessity ladder: E12 covers 106; +E4 covers +0; +K covers +22; +W covers +22 (150 total saturate). Honest caveat: case-b (E1-empty DELETE-runs, E4-pristine domain) is rare in corpus (random-walk repeats ~1/33), so E4-redundancy is marginal-contribution evidence, NOT necessity refutation - E4-pristine stands by ML-ADJ-E4/FRESH-CAP proof. E2-alone arithmetic (push-supply order covers demand order; root-fraction bounded single-shot+rebuild) consistent: E2 carries the bulk (106/150 alone with E1).

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; mindeg-zone reduced to violator-zone).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C52 - conditional mindeg-safety 8Q (this continuation)

### C52-1 8Q lemma [PROVED_AUTHOR conditional]
hall_lemmas.md 8Q: smaller-Hall + mindeg(N(Q))<=3 implies Hall(Q) (strong-induction step: remove min-degree neighborhood R, |R|>=1 so strictly smaller; Delta(Q)<=d-3<=0). Honest status: conditional on smaller-Hall (which is the open global); NOT unconditional and NOT a close. Violator-zone corollary: Hall reduces to mindeg>=4 zone (= violator zone; 8B consistent). Mindeg-4-removal bonus: minimal violator with min-degree exactly 4 has every such removal tight (Delta=0, no orphans) else smaller violator contradicts minimality - consistent, not contradictory. Degree-ladder (1-source and 2-source removals) stops exactly at 8B (deg>=4); no leverage beyond.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C53 - pinning-impossibility 8R (this continuation)

### C53-1 root-motion census + 8R lemma [PROVED_AUTHOR]
Every nontrivial splay moves its pre-splay root (final StepEv pivots old root down; verified 2661/2661 across 120 histories). Hence A-root-pinning breaks on every nontrivial access (repeats/no-ops only refuge); supply-free pushes are single-shot per state with rebuilds supplying (zone-overlap for x open; sterile-rebuilds need fresh-far keys (finite pool) else stall-or-save). hall_lemmas.md 8R banked. Wall unchanged (overlap question survives pinning analysis).

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C54 - full-split sustain falsifier (this continuation)

### C54-1 FS-00 zone-disjointness sustain [FINITE_EVIDENCE]
scripts/wp6_fullsplit.py -> fullsplit.json (demand-zone vs supply-zone A-rotated disjointness, first-x + B-heavy strikes): 12k evals, shortfall 0, best sustain 28 consecutive disjoint accesses (breaks via zone-boundary bleed, e.g. overlap keys [80,81] at zone edge). Slack stays 44-53 throughout (fresh E1s + dilution carry even fully sterile stretches). Sterility sustains (transient W/E2/K/E4 all avoidable together for dozens of accesses) but never converts (fresh channels + dilution absorb). (Artifact hygiene: evals corrected 9097->12000 post-run (improvement-only writes); final-write added.)

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C55 - run-drain sustain + transient-diversion waste (this continuation)

### C55-1 RD-00 per-run net-drain [FINITE_EVIDENCE]
scripts/wp6_rundrain.py -> rundrain.json (250 hist, 6678 runs): 21 B-heavy-drain runs, worst single-run net -29 (t=182 acc2 x=124: dem=32, new=1 - 32 B-events on old-shared + 1 new, yet saturates offline via shared pool). Sustain hunt (run-repeat bias, 8k evals): best cumulative drain -24, zero shortfall. Single-access extremes survive via shared-old (not fresh); cumulative drains never exhaust buffers.
### C55-2 transient-diversion waste 44.9 percent [MECHANISM, online-only]
waste.json (MA corpus, 76 elevation events): 44.9 percent of in-access picks land on sources that have EXITED by elevation time. Transients absorb picks then leave with them, starving the core of saturating picks (protects current minload). Explains M2/C37/NM patterns (drains stall; negative margins do not convert). Correlative blocker risk (exited-loaded may re-enter@3: aev40 pattern) but blockers rare+absorbed, so protection dominates. SCOPE: online-dynamics only (least-loaded picks/minload); offline Hall has no loads/picks/waste (static graph) - does NOT advance GC-STATIC directly; supports offline-fallback framing (C37) by separating the two processes.

## Queued next (LIVE)
- GC-STATIC old-abundance theorem (bare wall; wallmax caps pressure at 2).
- Splay-model Lean core (auxiliary).
- Spread-3 dormancy proof (auxiliary).

## C56 - wall-pressure maximizer + minimal-counterexample proof (this continuation)

### C56-1 WM-00 wall-pressure maximizer [FINITE_EVIDENCE]
scripts/wp6_wallmax.py -> wallmax.json (first-x + nearby-below pure pushers + run-repeat drain + far-key avoidance, hillclimb on shortfall/gap/pressure/eB-f-ratio): 10k evals, zero shortfall, zero GC-gap, bestpress 2 per history (seeds best 1 ratio 9.67; it90 ratio 34 slack 20; it583 press 2), final bestpress 2 bestratio 12.0 bestslack 32 (acc14 Q1 N11). Even MAXIMIZED, pressure stays <=2 isolated and slack >=32. Wall-pressure cannot be sustained/elevated by any generator in the arsenal. Finite face of sustained-sterile-B-heavy impossibility + single-pressure absorption.
## C57 - killshot trilogy + imprint lemma face (this continuation)

### C57-1 KS-00 medium-small-n hunt [FINITE_EVIDENCE]
scripts/wp6_killshot.py -> killshot.json (n=6..32 decouple+pusher+burst, 12k evals): NO KILL, bestslack 2 (degenerate singleton cut Q1 N1 — wrong objective, tight singletons not violator-zone).
### C57-2 K2 one-access-Delta + violator-zone climb [FINITE_EVIDENCE]
scripts/wp6_killshot2.py -> killshot2.json (DELETE-x-root pin + pushers + xc bursts, 12k evals): NO KILL, bestA one-access-Delta -2 (singleton Q1 N1, stuck from seeds: NO multi-event slice ever exceeds -2), bestB mindeg>=4-Delta -8 (acc0 Q4 N4, stuck: violator zone FAR, M2 -183 consistent). Climb cannot move either objective — structural signal, not budget.
### C57-3 K3 exhaustive n=6 + random-T0 family [FINITE_EVIDENCE]
scripts/wp6_killshot3.py -> killshot3X.json (n=6 L<=4 ALL 22,620 histories vine-left): clean; killshot3R.json (vine/balanced/random-BST T0, n=8..64, 9k): clean. Prior exhaustive stopped at n=5; vine-only bias removed. Cumulative now ~140k targeted + 2.28M exhaustive + 22.6k exact n=6 + 69 vault entries, zero shortfall/gap.
### C57-4 IMPRINT trivial-burst supply census + sited-always sketch [FINITE_EVIDENCE + LEMMA SKETCH]
scripts/wp6_imprint.py -> imprint.json (180 hist): final-A-StepEv sited 3871/3871 = 1.000 (interior 2856/2856); trivial bursts (E1-empty + B-demand) 75: E4-pristine 75/75 = 1.000, K-imprints min 2 (never 0), E3-union med 17 max 51, worst one-access Delta -8 (Q1 N3). Escape hatch (unsited/never-touched) never materializes. Sited-always sketch (Lean-ready): StepEv rotating distinct keys a<b has interval [lo,hi] with lo<=a, b<=hi so i=lo... precisely i=a in [lo,hi) with 1<=a<n, a+1<=b<=hi gives site; failure needs lo==hi single-point = no rotation = not a StepEv. If triple bounds verified in splay_trace, sited-universal is a 1-liner; final-triple-contains-x is splay mechanics (last StepEv rotates x). Together: every past nontrivial x-access banks a sited x-imprint serving all future x-bursts via K-persistence. Residual: cap-exhaustion (few imprints x3 slots vs big e_B — transients cover finitely, chase 95%) + variation formalization (each heavy access brings new old — fullsplit 28-then-bleed finite face). NOT a close; wall narrowed to imprint-cap-exhaustion + E3-variation.

### C56-2 whole minimal-counterexample proof with holes [CONDITIONAL PROOF]
audits/WP6_MINIMAL_COUNTEREXAMPLE.md: Steps 1-6 banked (8A deficit-one / 8B mindeg>=4 / 8C connected / 8E+8J latest-access |Q_L|>=3|U_L|+1 / 8H+8I non-heavy done / 8K frame with 8L circularity noted) -> HOLE-1 old-abundance at B-heavy Q-blocks (|Q_L|<=3|U_L| via old-new) is FIRST load-bearing hole; assuming HOLE-1 contradiction immediate. HOLE-1 assault (1a sustained-sterile / 1b single-pressure / 1c repeat-hole / 1d E2-hole+K-thin+sterile-E3 / 1e sterile-rebuild): all finite-safe, none proved (wallmax + pressure + chase + SG2 + fullsplit + rundrain + fourth + 8R). Resume: HOLE-2 one-access-Hall 8F + overlap (8R residual) OPEN; HOLE-3 repeat-hole universal + E2/K-tax universals OPEN. End: conditional GC-STATIC -> GC -> D6 -> MSTL-14P; unconditional OPEN/NO_WITNESS (70k+ targeted + 2.28M exhaustive clean).

## C123 - alternating-trap vacuity + greedy totality law (this continuation)

### C123-1 TA typed alternating closures [REFUTED-BY-BERGE]
scripts/wp6_trap.py -> trapanat.json (600 evals: biased pushers + gr1-style walks n<=512 L70; configs REV|E1E4KT, FWD|K-hoard, FWD|E1E4KT): 4 stuck (all FWD|E1E4KT n512 walks, reproduces greedyadv 6 percent rate), ALL 4 closures OPENED via augmenting paths, traps=0. Closed alternating traps are VACUOUS when maxflow saturates: Berge guarantees an augmenting path from any non-maximum matching, so the BFS closure from an unmatched bev always opens. The trap instrument cannot witness anything; sealed REFUTED. (Intermediate bug caught: BFS leaked onto unplotted a-nodes; restricted to plotted-only before banking.)

### C123-2 TB greedy totality sweep [FINITE_EVIDENCE + LAW]
totality.json (6 tier-orders x FWD/REV x 40 walks n<=512 L70): FWD rules 0-1 stuckbev/40evals (T-first-FWD 0/40 best; E1-first/K-first/E4-first 1/40); REV rules 6-100/40 (K-first-REV 74, T-first-REV 100). DIRECTION dominates tiers: chronological (FWD) greedy is near-total, anti-chronological fails. Zero Hall kills. Law: past-only competition + E1-freshness make FWD greedy the constructive-matching direction for 8AC; next is the FWD pressure law via W-charge-to-rotations (C124, grounded in banked ML/OCC lemmas).

### C124-1 WC W-charge-to-rotations census [FINITE_EVIDENCE + LAW]
scripts/wp6_wcharge.py -> wcharge.json (FWD|T,E1,E4,K, 150 gr1-walks n<=512 L70): stuck=0/150, zero kills. Placement mix: W 54 percent (25819), E1 22, E2 14, E7 9, K 0.1 (56/47k - K nearly DEAD at scale in walk family). W TIME-ARROW: all 25819 W placements loader-older-than-site (past->future, 100 percent; same/future-loader 0). Quartile handoff monotone: E1 40/3.5/0.8/0.2 pct Q0..Q3, W 40/67/72/73 pct, E7 3/14/17/17 pct. sitemaxW=sitemaxall=3. Headroom formula (3|sites|-pastW-siblings) REFUTED as pressure measure (med -3, min -109, 184 neg-accesses, yet total): bevs escape FORWARD onto future sites, need no own-E1. Mechanism: early bevs E1-own + W-forward; late bevs W-forward into denser-late sites + E7/E2 last-stand. K relegated to pusher-family mechanism (imprint) - reconcile in C125 second family. Next: 8AC-IND forward-escape/last-stand induction sketch.

### C125-1 ARROW eligibility time-arrow + induction frame [PROVED_AUTHOR-by-construction + CORRECTION]
Code audit of build_tagged: E1 same-access; E2/E4/E7/K older-or-same (index bounds in construction); E3 ai<=idx explicit. Forward edges structurally nonexistent -> 8AC-TO (hall_lemmas.md). 8AC-PRISTINE corollary: own-E1 opens each access with full 3|sites| slots, zero past-load. 8AC-IND: FWD induction (pristine-E1 + residual-sufficiency) with single HOLE-IND (per-site future-demand bound via OCC/rotation budgets or positional density). CORRECTION to C124: arrow is BACKWARD-grazing (51,292/51,292 placements loader-newer-or-same, trel relabeled older/same/newer in wcharge.json + wcharge_pusher.json); quartile gradient re-read (early E1-own 40pct, late W-on-past 73-85pct); all C124 numbers stand. Zero kills.

### C126-1 HOLEDEMAND per-site future-claim census kills counting residual-sufficiency [PROVED_AUTHOR]
scripts/wp6_holedemand.py -> holedemand.json (80 hists walks+pushers): claim(i)=future-bev eligibility via K/W/E2/E7/E4: 82.4pct sites claim>3 (17127/20793), med-claim med 15 / max 88, sitemax 406 (K-only 108). Demand exceeds cap almost everywhere, yet maxflow saturates always: ASSIGNMENT carries the theorem, counting cannot. 8AC-HD (hall_lemmas.md): HOLE-IND counting-form DEAD (consistent 8N(d)/8AC-D); residual-sufficiency needs matching/contention theory = 8AC-RM door #1, else verified counterexample (door #2). Zero kills.

### C127-1 LEANHALL Lean matching cores + positional edge interface [PROVED_KERNEL]
lean/WP6/GCStaticHall.lean (exit 0, no sorry/admit/axioms): mindeg_safe + mindeg_three (8Q-core counting), zone_step (8AC-ZONE + IH assembly), zone_target (violator-zone equation), TEdge interface (siteAcc/bevAcc/chan) + arrowOk hypothesis pin + pristine_of_arrow/e1_arrow/old_arrow/arrow_cases (8AC-TO/PRISTINE Layer-B pin; Layer A = build_tagged bounds C125). Mode-A assembly counting kernel-closed; multi-session position evolution queued (C128: key-depth dynamics from SplayRotate rows).

### C128-1 LEANPOS migration locality / sibling rigidity [PROVED_KERNEL]
lean/WP6/GCStaticPos.lean (exit 0, no sorry/admit/axioms): underL/underR operators (op strictly inside one child) + rigid_R_underL/rigid_L_underR (sibling depths bit-identical) + rigid_root_underL/underR (root stays 0) + rigid_absent_underL/underR (absence preserved). Any off-path key has displacement exactly 0; on-path shifts are the 8W rows. Full per-StepEv displacement table pinned: migration moves keys only via on-path rotations (8AC-MW kernel pin). Next: splay-loop descent + co-location interface (C129).

### C129-1 LEANSPLAY double-step delivery + side dynamics [PROVED_KERNEL]
lean/WP6/GCStaticSplay.lean (exit 0, no warnings): zzR/zzL/zagLR/zagRL transformers + delivery (accessed key 2->0 each); goesL/goesR sides + preservation under underL/underR (4 thms: root key fixed => sides fixed); rotR/rotL keep/break (4 thms: below-new-root stays, between-old-and-new-root switches side). Co-location dynamics kernel-pinned: breaks exactly between old/new root, preserved everywhere else. Next C130: fuel-bounded loop + root delivery.

### C130-1 LEANLOOP splay skeleton + key-membership preservation [PROVED_KERNEL]
lean/WP6/GCStaticLoop.lean (exit 0, no warnings, 12 theorems): faithful recursive splay skeleton (zig + 4 doubles with conditional fixup, matches only on args); 6 transformer-mem + 4 fixup-mem (Or AC-normalization); splay_at_root (shape-split + root-test); mem_splay via splay.induct functional induction (10 cases, refine-with-explicit-motive). Battles won: splitter-friendly single-match definitions; cases-before-simp for split equations; by_cases+if_pos/if_neg for Bool ifs. Next C131: BST validity + conditional delivery.

### C131-1 LEANVALID BST validity + rotation preservation [PROVED_KERNEL]
lean/WP6/GCStaticValid.lean (exit 0, no warnings, 8 theorems): allLT/allGT/valid predicates; allLT_mem/allGT_mem + monos; mem_search_L/R (splay descent correct on valid trees); valid_rotR/valid_rotL (single rotations preserve BST validity: the invariant behind every StepEv). Battles: explicit association nesting in obtain/refine; deep .2.2.2 projections. Next C132: conditional root delivery.

### C132-1 LEANDELIVER conditional root delivery [PROVED_KERNEL]
lean/WP6/GCStaticDeliver.lean (exit 0, no warnings): deliver (valid t + mem t x => rootKey (splay x t) = some x) via 10-case splay.induct; rootKey_some inversion; 6 valid-decomp helpers; restated frame (mem/bounds/search/splay). Doubles route via search correctness into IH, invert delivered key, discharge fixup; off-route vacuous by bounds. Skeleton now certified end-to-end at model level. Next: pointer-engine simulation relation.

### C133-1 LEANSIM pointer-engine simulation at rotation level [PROVED_KERNEL]
lean/WP6/GCStaticSim.lean (exit 0, no warnings, 15 theorems): PTree mirror of engine nodes; protR/protL line-by-line transliterations; toSTree projection; correspondence (engine step = model step); wf preservation; pointer-side bounds + pattern distinctness; emit/emit3 with lo<hi; sited chain; zig_sited/double_sited end-to-end (valid pattern + key range => emission carries sites, all StepEv shapes). Battles: True.intro for folded equalities; explicit middle nesting; simp-normalization over rfl. Next: loop-level simulation (event sequences).

### C134-1 LEANSIM2 double-step simulation + branch agreement [PROVED_KERNEL]
lean/WP6/GCStaticStep2.lean (exit 0, no warnings, 5 theorems): sim_LL/RR/LR/RL (engine rotation pairs = zzR/zzL/zagLR/zagRL under projection, full firing patterns); eclassify + classify_agree (engine link-geometry table = skeleton classifier). Battles: full-pattern statements (partials route to ZIG/identity by engine if-chain); child-subtree application with parent threading for zigzags. Every loop iteration now pinned. Next: full-trace induction over iterations.

### C135-1 LEANTRACE skeleton trace theory [PROVED_KERNEL]
lean/WP6/GCStaticTrace.lean (exit 0, no warnings, 3 theorems): steps emission (one SStep per level, bottom-up); steps_nil_root (root-hit silent, loop-exit agreement); splay_noop (empty trace iff skeleton idle, 4 shape combos); steps_length (trace fits tree size, 10-case steps.induct + omega). Battles: explicit with-binders; rw at h and goal; simp-at-hyp for emitting arms. Next: engine-side emission + loop-lifted agreement + Aev accounting.

### C136-1 LEANSUPPLY event-supply accounting [PROVED_KERNEL]
lean/WP6/GCStaticSupply.lean (exit 0, no warnings, 3 defs+2 theorems): sites_count (_sites model); sites_ge_one (valid interval banks >=1 site, witness lo); trace_supply (event-list total covers event count, induction). Quantitative 8S face in kernel. Battles: mem_range step form; decide direction; cases-substitution asymmetry. Next: engine event-list + loop-lifted agreement.

### C137-1 LEANNAV navigation + position-correct rewriting [PROVED_KERNEL]
lean/WP6/GCStaticNav.lean (exit 0, no warnings): getPath + direction lemmas; rewriteAtAux (rotation par always the true enclosing key); rewrite_toSTree (rewriting projects to STree plugging); wf_rewrite (links preserved); pall monos/reparent; pvalid_protR/L (pointer rotations preserve BST validity). Battles: match-arm arity; def ordering; pvalid_reparent; generalizing arg order. Next C138: fuel engine loop + emission + bounds.

### C138-1 LEANEMIT engine-side emission validity + length [PROVED_KERNEL]
lean/WP6/GCStaticEngine.lean (exit 0, no warnings): emitTrace (one interval per level, zig pairs + double triples); emitTrace_valid (every interval proper on valid trees, 10-case induct); emitTrace_length (trace fits size). Battles: simp-at-hyp idiom; beq order; omega for disequalities; substitution asymmetry; indent sensitivity. Next: loop-lifted agreement + supply lift.

### C139-1 LEANLIFT loop-lifted agreement + fused event validity [PROVED_KERNEL]
lean/WP6/GCStaticLift.lean (exit 0, no warnings): trace_length_eq (emission and step traces agree in length, uniform simp closers); event_ok (every emission on range-valid trees satisfies 1<=lo<hi<=n, keyrange threading + bounds + omega). Battles: rw arm-specificity; Or-depth by side; singleton simp. Next C140: supply lift application.

### C140-1 SUPPLYTOTAL fused per-access supply total [PROVED_KERNEL]
lean/WP6/GCStaticSupplyTotal.lean (exit 0, no warnings): sites_count floor + supplyTotal append + supply_total (10-case fused induct: IH supply cover + per-event floor via range/distinctness, omega assembles). Event count covered by counted supply per access in kernel. Lean positional track complete through supply; open wall stands.

### C141-1 AUGMENT stuck anatomy + t75 dissection [FINITE_EVIDENCE + REFUTATION]
scripts/wp6_augment2.py -> augment2.json (720 evals walks+pushers x 3 configs): 76 stuck ALL REV|E1E4KT-walks, ALL sibling-saturated E1-only (E1 982/982 full, sib-loads 2808, past 0); augmenting paths ALL length 5 terminal W (chan E1/E3E1/W). FWD configs 0/480 (totality ~1100 evals cumulative). t75 (sole FWD-stuck, gr1 n64): bev19 acc3 x39, E1=1+K=2+T=1 (REFUTES stuck=>E1-only); loaders x39 siblings (E1+K site12) + x38 adjacent past cohort (site13); aug len5 via W/K. Tier-ledger: cohort-saturation only, never exotic theft; repair global. Next: scale test of cohort-locality (C142).
### C142-1 CODIST loader key-distance kills interval-locality [FINITE_EVIDENCE + REFUTATION]
scripts/wp6_codist.py -> codist.json (300 evals, 42k placements): W |loader_x - site_acc_x| med 23 / p90 129 / max 493; K med 0 / p90 23 / max 297; E1 always 0 (structural). t75 adjacency = small-n luck. 8AC-IL (interval-localized Hall counting) REFUTED finitely; contention key-global (consistent 8N(d) sharing-infinity, 8Z long chains). hall_lemmas.md: 8AC-IL dead. Wall stands on 8AC-RM doors only.

### C143-1 STUCKSIB stuck-cohort lemma + totality tally [PROVED_AUTHOR]
hall_lemmas.md 8AC-STUCK-SIB: stuck + nonempty E1 => 3|E1| sibling-loads (greedy-maximality per-tier + E1 same-access scoping + 8AC-TO no-forward-edges); E1-empty => pure backward-spill exhaustion. Finite faces: 76/76 REV + t75 (E1=1 sib + K sib + adjacent past). Repair always W/K-augmentable (len 5). T-first-FWD totality: 940/940 zero-stuck, zero kills (TB+WC+C125+CD). Exchange localizes to cohorts.

### C144-1 LEANMATCH greedy maximality in kernel [PROVED_KERNEL]
lean/WP6/GCStaticMatch.lean (exit 0, no warnings, 16 defs+theorems): cap-3 greedy with threaded loads; update lemmas; placeIn bound/outcome/some/preserve/mono; runGreedy; greedy_maximal (cap + future-empty + unplaced-implies-full, 3-part induction). Kernel core of 8AC-STUCK-SIB (E1-sibling specialization stays Layer A). Battles: Nat-succ equation friction (induction-tactic form only); subst direction (subst var); underscore arity discipline; rw auto-close limits; motive generalization for inductions. Next: Berge improvement + assembly.

### C145-1 LEANFLIP path-flip set improvement [PROVED_KERNEL]
lean/WP6/GCStaticCount.lean (exit 0, no warnings): mupd/pathflip + flip_offpath/flip_set + flip_improve (distinct-bev path flip matches head + preserves all matched). Counting deferred as unnecessary (pointwise+Nodup suffice); cap-side stays with C144 loads + 8AC-BERGE meta. Battles: simp over-normalizes negations (controlled simp only); pair-destruction before equations; subst direction (subst var); generalizing M for IHs.

### C146-1 LEANBOUNDARY Lean track pauses at clean kernel boundary [META]
No new .lean (deliberate): flip load-validity in full generality needs list-count API absent from core (count_eq_one_of_mem/pos_iff_mem missing; count_append exists) for a consumer (Hall assembly) blocked on finite-set cardinality either way. Kernel matching pair (C144 maximality + C145 improvement) + full positional model through supply (C127-C140) stand as the complete core-Lean contribution. Assembly (maximal+unaugmentable => violator-or-saturated) and zone/matching universals need Mathlib-scale theory or open mathematics. A near-trivial single-upd-cap draft was written and REMOVED rather than banked (anti-triviality). Lean track pauses; GC-STATIC remains OPEN/NO_WITNESS.

### C147-1 RIDES burst-relative silent-push census refutes 8V-strong [FINITE_EVIDENCE + REFUTATION]
scripts/wp6_rides.py -> rides.json (535 heavy bursts eB>=8, full-history window, B-depth gains + E3-imprint check): 76.8pct of burst-built depth silent (1391/1787 push events silent; fully-silent bursts to eB=91/depth=181). 8V-strong (imprint-proportional cover) REFUTED; 8V-weak survives (pushers bank global-pool supply). K_x med-cover 1.51x but min 0.0: cover is PORTFOLIO (K + E1 + E4 + transients), no single channel dominant. Ride-sterility is the norm (G-outer bystander mechanics). 8V route over.

### C148-1 COHORTX cohort-localized exchange v2 [SKETCH + FINITE]
augment2.json futdepth (med 20/max 69 future-grazer depths; past-loaders 0 everywhere); AU-LEN5 single-displacement law 526/526; hall_lemmas.md 8AC-XC (per-channel locality table + processing-precedence + precise tier-ledger hole + conditional assembly). Exchange fully mapped; deficiency forcing remains the wall. Zero kills.

### C149-1 WCHAIN W time-arrow + chain mediation [PROVED_AUTHOR]
hall_lemmas.md 8AC-WOLD (all W-edges strictly backward: same-access E3 subset E1) + 8AC-WWIT (non-xx chain-key witness per W-edge). Explains codist K-vs-W split + C124 arrow structurally. Finite faces: t75 site-13 K-touch {38,39}; live W-edges with far witnesses (379 via 31). W-residual = chain-key recurrence. Zero kills.

### C150-1 RECUR recent-pool recurrence law [FINITE-STRONG]
scripts/wp6_recur.py -> recur.json (59k triple-keys): recurrence 81.9pct, recency med 1 / p90 16 / max 86; burst coverage med 1.0, zeros all J=0; heavy min J>0 = 0.005 (eB=67 fresh, E1-trivial 67x67). hall_lemmas.md 8AC-REC: supply side fully mapped; composition is the remainder. Zero kills.

### C151-1 LEANFIN finite-set toolkit [PROVED_KERNEL]
lean/WP6/GCStaticFin.lean (exit 0, no warnings, 19 defs+theorems): dedup + mem/nodup/size; rawNb/neighbors + mem; degree/mindeg + mindeg_le_mem; erase_mem (local); sdiff + mem/nodup/length; subset_length (+aux) + length_strict. Core lacks Finset/erase/nodup API; all built locally. Battles: false mem_erase (erase removes first only!); match-vs-if equations (cases-on-Bool); simp over-normalization; Nat-succ friction avoided via explicit lists. Next C152: assembly.

### C152-1 LEANASM zone-implies-Hall assembly [PROVED_KERNEL]
lean/WP6/GCStaticFin.lean + zone_implies_hall (exit 0, no warnings): bound induction; empty case via eligibility-free vacuity; mindeg<=3 via 8Q-removal (length_strict + subset counting + C127 arithmetic inline); mindeg>=4 via zone hypothesis directly. Eligibility subsumed (zone entails it). GC-STATIC is exactly 8AC-ZONE in kernel. Battles: pipe-projection ascription; rw auto-close limits; subst direction; induction generalization via explicit forall. Next: zone itself.

### C153-1 ZONE2 violator-zone floor -8 across families [FINITE_EVIDENCE]
scripts/wp6_zone2.py -> zone2.json (400 evals walks n<=512 + pushers; claim pools top-20 + access slices + mincut sets): 262 mindeg>=4 candidates, best Delta EXACTLY -8 (Q4 N4 mindeg4, same signature as K2B vine-only). Floor robust; concentrated zone cores do not assemble (consistent pack3 confinement-infeasibility). Zero kills.

### C154-1 LEANTGRAPH time-indexed matching core [PROVED_KERNEL]
lean/WP6/GCStaticTGraph.lean (exit 0, no warnings, 22 items): FinList toolkit restated + QL/QQ/UL defs + partition counting + Nunion + Nsplit + E1L_sub_UL (E1 inside new sources via arrow+latest) + eightJ arithmetic. 8J necessity kernel-closed; HOLE shape exact. Battles: match-vs-if equations; simp over-normalization; dup consolidation; pipe ascription. Next: old-abundance itself.

### C155-1 PREFIX prefix-Hall equivalence + censuses [PROVED_AUTHOR + FINITE]
scripts/wp6_prefix.py -> prefix.json (300 evals): mincut tight sets downward-closed 0.06pct / exact-prefix 0 (prefix-shape REFUTED); prefix-slack min 0 / med 27 (binds, never negative). hall_lemmas.md 8AC-PREFIX: PREFIX-HALL <=> HALL proved (access induction with E1-pristine + residual counting => FWD totality => Hall); two-access warmup closed (margin 2); open universal prefix-slack >= 0 (tight) with concrete path. Zero kills.

### C156-1 PUSHLEDGER cost links + coupling [FINITE + STRUCTURE]
scripts/wp6_pushledger.py -> pushledger.json (150 hists): eB<=d+1 (0/5642), eA>=d/2 (0/5059), Phi_min +2 global; first-eq is idx-0-only (8T scope correction); global alternation-count REFUTED (2695 vs 1595). hall_lemmas.md 8AC-PUSH: tight-window coupling precisely stated (heavy bursts need buffer; buffer can be 0; finite never breaks); no telescoping shortcut. Zero kills.

### C157-1 COUPLE tight-window coupling shape [FINITE-STRONG]
scripts/wp6_tightwin.py -> tightwin.json (150 hists, 10.6k points): overflow-buffer gap max -6 (global margin 6, 2077 divergent); low-buffer (<=20) overflow max 5 (n=11) vs high-buffer max 125 (n=2066): overflow SCALES with buffer. Tight prefixes rare (0.2pct), deep-synced (Amax/Bmax ~60), low-current-demand, followed by bigger bursts (med 18). hall_lemmas.md 8AC-COUPLE: decoupling-budget structured; mechanism (tight forces mild) open. Zero kills.

### C158-1 PHIDRAIN cumulative-Phi drain fails [FINITE-STRONG]
scripts/wp6_phidrain.py -> phidrain.json (150 hillclimbs L<=80 with A-root targeting for guaranteed supply-free splashes + repeat-pushers + migration): minPhi NEVER below 0 (best 0 = initial; no negative). Direct refutation of prefix-GC fails; cumulative counting robust even adversarially. Zero kills (no hallkill; phikill untriggered).

### C159-1 SYNCED synced-divergence exact characterization [PROVED_AUTHOR + FINITE-EXACT]
tightwin sync fields: 674/674 synced-divergent accesses are exactly (eA,eB)=(0,1); zero synced with overflow>=2. hall_lemmas.md 8AC-SYNCED: proof via exact StepEv counting e(d)=ceil(d/2) (loop structure, Layer A cited; loop correspondence queued): synced-divergent forces m=0 (dA=0) hence (0,1); synced with dA>=1 never diverges. Decomposition: synced-trivial (<=1) + diverged-buffer (open). Zero kills.

### C160-1 AROOT A-root persistence + (0,1)-closure [PROVED_AUTHOR conditional]
hall_lemmas.md 8AC-AROOT: eviction (B-pushes move A-root, delivery kernel) => persistence means all-x-accesses; B-depth nonincreasing under persistence; stale depth needs banked rooting-DELETE (+3) or T0/first-safe; (0,1)-splash drains exactly 1 from buffer >= 3 (strong prefix IH) => Phi preserved (>= 2). Needs loop-StepEv correspondence + single-finish-shallow + ceil-exactness (concrete Lean queue). A-nontrivial-synced helps (<= -1, same links). Diverged branch open. Zero kills.

### C161-1 STEPCOUNT ceil-exactness in kernel [PROVED_KERNEL]
lean/WP6/GCStaticStepCount.lean exit 0 no-sorry (direct `lean`; lake env broken by frozen legacy lakefile, untouched): sdepth_self, sdepth_downL/R (existential one-level descent, cases-substitution rfl witness), ecount (one per recursion level, mirrors splay control), ecount_eq steps=ceil(depth/2) via ecount.induct 10 cases + omega div-arithmetic. Closes AROOT/SYNCED ceil-exactness link; remaining loop links: loop-StepEv correspondence (C162: identify ecount with engine e_B/e_A), single-finish-shallow. Zero kills.

### C162-1 LOOPCOUNT loop correspondence + SYNCED/AROOT links kernel [PROVED_KERNEL]
lean/WP6/GCStaticLoopCount.lean exit 0 no-sorry (direct `lean`): steps_length_eq ((steps).length = ecount, transliteration of C139 trace_length_eq skeleton, 10 cases simp) + omega cores eb_le_depth / ea_ge_half / sync_overflow_le / sync_nondivergent / shallow_single / shallow_exact. Chain C139+C162+C161 kernelizes e_B = ceil(d^B/2), e_A = ceil(d^A/2). Closes: 8AC-SYNCED counting core (status -> PROVED_KERNEL counting, engine-application via simulation kernels) and 8AC-AROOT Lemma C (status -> kernel-closed; A/B + prefix-IH stay PROVED_AUTHOR). Full 21-file kernel regression green. Remaining opens: micro-coupling (synced-trivial buffer <= 1), tier-ledger coupling (diverged branch). Zero kills.

### C163-1 MICRO micro-coupling CLOSED (kernel + finite) [PROVED_KERNEL + FINITE-STRONG]
scripts/wp6_micro.py -> micro.json (150 histories): A synced-disjunction 0 viol (7955 synced, 4702 nontrivial); B synced overflow>=1 exactly (0,1) w/ buffer>=1, 689/689 (== z01 count: every overflow-1 in sample is synced-(0,1); plus 8 unsynced ov==1 small-divergent e.g. (1,4)); C (0,1)-buffer min 13 (0/689 viol, Lemma B's >=3 holds with margin); D global Phi_min +2; F ceil-exactness eB=(dB+1)//2 eA=(dA+1)//2 zero viol in 16776 (finite mirror of C161+C162). Kernel GCStaticMicro.lean exit 0 no-sorry: micro_couple disjunction + micro_step_zero + micro_step_one (all omega). hall_lemmas: 8AC-MICRO added (CLOSED), SYNCED decomposition updated. Bonus FINITE-STRONG: TRIPLE-COVER — every heavy burst (2174, ov>=2, never synced) satisfies buf >= 3*eB (triple_min exactly 0; max eB=127 at buf=381=3*127); margin buf-ov >= 4; lobuf(<=20) heavy max ov 5 (n=10). Tier-ledger mechanism still OPEN: gap analysis shows prefix-IH alone is 4/3x too weak (needs deepening pushes banked; supply-free real splashes exist; needs 8R/freshness). Zero kills.

### C164-1 WINDOW diverged-burst window attribution [FINITE-STRONG]
scripts/wp6_window.py -> window.json (150 histories, 2174 heavy bursts): telescoping dB(t)==dB0+sum(delta) EXACT (tele_viol=0); window inequality win_min=4 (== margin). Funders over all heavy windows: DELETE banking +562137 (36567 pushes) dominates; deep-supplying +42831 (5106); nondeep +13654 (25469); deep-free DRAIN -40290 (9486, avg -4.2/push vs supplying +8.4/push, net +2541 ~ neutral). (0,127) anatomy SOLVED: x=254, dB0=253 genesis vine, window = ONE DELETE (e_A=127, net +381) then burst (0,127): buf=381=3*127 is one banking event at 3/unit + one spending event at 1/unit on twin vines — kills the repeated-units hypothesis. Min-margin case same shape at small scale ((0,2), dB0=3, one DELETE +6). Zero kills.

### C165-1 ADVERSARIAL diverged kill-attempt fails everywhere [FINITE-STRONGEST]
scripts/wp6_adv.py -> adv.json: greedy builders (drain/phimin/starve/freeride, L<=100) x 5 T0 shapes (vine/vineL/balanced/comb/zigzag, n=32/64) = 40 runs: min margin >= 0 (real-burst >= 6; margin-0 records all trivial genesis root-hits), Phi floor 0. keeponly twin-confirmation: div=0 on ALL shapes (6 runs) — all-KEEP histories never diverge (twin-symmetry: same deterministic splay on twins). Long-run grind (L~600 concatenated): Phi>=0, NO ratchet — late heavy margins (1201+) >> early (26+), pool accumulates. Prior 150 phidrain hillclimbs (minPhi floor 0) + ~200M exhaustive stand. Zero kills (exit 0, kills=[]).

### C166-1 HISTORY history-ledger kernel + mechanism verdict [PROVED_KERNEL + AUTHOR]
lean/WP6/GCStaticHistory.lean exit 0 no-sorry: STree/sdepth/splay/ecount copies + presence-gated applyA/accEA + stepAB + Int runPhi; twin_step + delete_step (congruence/rfl) + twin_run (all-KEEP from twins keeps twins, e_A=e_B per access, Phi monotone nondecreasing => Phi>=0; induction with twin invariant) + diverged_step_cond (explicit window funder hypothesis => burst preserves nonnegativity; pins the exact gap). 8AC-TIER added to hall_lemmas: DIVERGED-AFFORDABILITY-WINDOW minimal theorem + circularity audit (telescoping/delta/twin/genesis-twin all GC-free; only bank-rate law open) + four-routes verdict (A fails 4/3-gap; A' circular without rate laws; B fails cap-exhaustion except DELETE-attribution; C right for maxflow not counting; D adds nothing; new route E twin+DELETE-attribution sole viable path). Full 23-file kernel regression green. GC-STATIC stays OPEN/NO_WITNESS; single load-bearing item: window bank-rate law (deepening pushes banked >=4/3x spend / supply-free deepening sufficiently rare). Zero kills.

### C167-1 PAIR supply-free pairing finite-closed + arrival-banking kernel [AUTHOR + FINITE-CLOSED + KERNEL-EDGE]
scripts/wp6_pair.py -> pair.json (150 histories): 2849/2849 supply-free pushes pair with same-key banking DELETE-arrival; frozen B-depth between 2849/2849 (structural: any B-touch unroots from A); zero genesis-root cases; arrival banking min 0 (no-op arrivals), pair nets to -118 (diverged arrivals). AUTHOR pairing theorem (same-key banking arrival + frozen-B window; KEEP-arrival would un-deep so arrival is DELETE). Kernel edge GCStaticHistory.lean: ecount_pos (sdepth-some + depth>=1 => ecount>=1 => arrival banks >=3; needed downL/R copies + unfold/dsimp/by_cases engineering). Turtles verdict: arrival-divergence regresses one level per pairing (built-by-pushes + shallowness-from-rooting/rides), bottoms at genesis twins, constants never close — aggregate rate law irreducible and OPEN. Full 23-file regression green. GC-STATIC stays OPEN/NO_WITNESS. Zero kills.

### C174-1 RUNCANON run-canonical frame kernel + ten route corpses [PROVED_KERNEL (frame) + AUTHOR (corpses)]
Present-domain locked (absent excluded: PresentLegalPairInstance requires every access key in keys(T0), key set preserved by mem_splay kernel; absent-KEEP need>0/zero-supply shape out of scope). Kernel GCStaticHistory.lean (exit 0): runstart_bank (off-root arrival forces >=1 step via ecount_pos) + genesis_run_surplus (twins=>need vanishes) + synced_run_le1 (synced deficit<=1) around exact open remainder (div-runs vs surplus-runs). hall_lemmas 8AC-ROUTES: ten corpses with exact killers — V (birth-multiplicity/cap-exhaustion/geometry), VI (birth-multiplicity/pool-collapse), VIII (subset-minimality invalid for dynamic replay; first-violation valid but known geometry), I (unbounded/log-class), II/IV/X (supply-vanishing kills classical interface), III (dual=potential/charging), VII (log not constant), IX (non-confluence). No doomed experiments per falsification law (analytic kills). Full 24-file regression green. GC-STATIC + DIRECT-D6 stay OPEN/NO_WITNESS; single item stands.

### C169-1 D6DEF DIRECT-D6 deficit assault fails (max exactly 0) [FINITE-STRONG]
scripts/wp6_d6.py -> d6.json: greedy max-(need-6e_A) builders on vine/bal/comb/zigzag n=16..64, L<=120 (32 runs): max D6-deficit EXACTLY 0 everywhere (never positive; boundary only). Sitedness verified 0/10914 unsited (8S: S_A = all-Aevs sum exact, computation valid). Reduction banked: D6-def = 2*GC-def - slack with slack>=0 per access (D2), so DIRECT-D6 <=> GC-def <= slack/2; first D6-violation would need dB > 5dA+1+buffer (vs GC's 3dA) — same diverged-burst node, rescaled constants, identical rate-law wall (confirmed 6 ways: deficit/slack/pair/potential/charging/first-violation all term-identical). D6-directed kill is strictly harder than GC-kill (any D6-witness is a GC-witness). Zero kills.

### C170-1 TERMC Terminal C: D6 confirmed NECESSARY, no weaker substitute [PROVED_KERNEL + FINITE]
scripts/wp6_d6svc.py -> d6svc.json (240 long histories): service holds everywhere (0 violations unfiltered); joint_svc_hold_d6_hold 240/240 (zero kernel_contra); unsited 0. Kernel lean/WP6/GCStaticD6.lean exit 0 no-sorry: slack_identity (list distributivity) + slack_nonneg (D2) + d6_of_gc (banked route) + service_implies_D6 (conservation + inject-6 + paid==need => D<=6*S_A, pure arithmetic) + no_weaker_substitute (prop closure: (D6=>X)+(X=>service)+(service=>D6) => (X=>D6)). VERDICT: D6 is the UNIQUE minimal cumulative obligation (necessary; sufficient with banked C4 activation). Bypass hope REFUTED as logic: no strictly-weaker X can imply service. Proving D6 remains load-bearing (same wall). Full 24-file regression green. Zero kills.

### C171-1 D6COND conditional D6 kernel + beam on isolated hypothesis [PROVED_KERNEL + FINITE-STRONGEST]
GCStaticD6.lean extended (exit 0, no warnings): d6_micro01_charge ((0,1) charges <=1; hA unneeded for charge, kept for step ID) + d6_no_first_violation (dB<=5dA+1+B => no crossing; contrapositive gives dB>5dA geometry) + slack_of_needpos / slack_ge_depth (per-access slack quantified) + d6_of_rate (single open premise GC-def<=slack/2; hslack dropped — Int floor-div makes it unconditional). scripts/wp6_d6beam.py -> d6beam.json: beam (W<=40, L<=50) maximizing D6-deficit directly on isolated hypothesis: max EXACTLY 0 all 8 runs (tight boundary instances exist, never crossed). Isolated hypothesis FINITE-STRONGEST; kernel surroundings complete. GC-STATIC + DIRECT-D6 stay OPEN/NO_WITNESS; single load-bearing item unchanged (window bank-rate law). Zero kills.

### C168-1 BEAM choreographed kill-attempt fails; triple-cover equality boundary [FINITE-STRONGEST]
scripts/wp6_beam.py -> beam.json: beam search (width<=48, L<=45, n=16/32, vine+balanced) jointly optimizing pool-zeroing + divergence gap, then forced KEEP-xc burst: best margins 4..16, ALL with eA=0 achieved (A-trivial bursts reachable!) but pool always covers (buf>=3*eB exactly at worst: (0,2)@buf6, (0,8)@buf24, cf. (0,127)@buf381). Zero kills (8 runs). Conclusion: pool-zero + diverged-burst combination is STRUCTURALLY UNREACHABLE (building divergence banks; pool-zeroing un-diverges) — the choreography the kill needs cannot be assembled. Triple-cover buf>=3eB holds under choreographed assault with equality cases explained (twin-depth banking-then-spending: SA==eB_burst with zero prior spending). Zero kills.

### C172-1 FREERIDE free-ride-to-root hits floor dA>=1, never 0 [FINITE-STRONG]
scripts/wp6_freeride.py -> freeride.json: beam (xc unaccessed, objective min dA with dB held) on vine/balanced n=16/32: xc rides 16->1 (vine32: dA=1,dB=15,pool=21) and to 2 (balanced) but NEVER 0 (8 runs, zero kills). FLOOR: unaccessed keys reach dA>=1, never exactly 0 (last step to root needs access). Consequence: every nontrivial burst banks e_A>=1 (own zig, >=3 supply) unless at exact root, and exact-root occupancy postdates a banking arrival (or genesis-never-left, which forces B-shallow by 8R unrooting) — kernel-composable via ecount_pos. Does NOT close rate (pair magnitudes still open) but bounds banking shape. Zero kills.

### C173-1 PHASED freeride-grind-burst kill-attempt fails; pool-divergence coupling [FINITE-STRONGEST]
scripts/wp6_phase.py -> phase.json: phased assault (freeride xc to (dA>=1,dB large) [16 states], grind pool to 0 via x-frozen covered drains (delta 0 both trees), burst xc): grind STALLS — x-frozen accesses net-BANK (pool rises 21->30 on vine32; min pool 9-47 across 16 runs), bursts covered margins 8-43. Zero kills. MECHANISM CANDIDATE (AUTHOR): pool-draining pushes rotate large regions and necessarily disturb the burst key; x-frozen accesses are local/shallow and bank. Draining the pool while preserving (dA>=1,dB large) appears geometrically impossible (deep paths catch ancestors; disjoint-subtree heavy-diverged setups need their own banking arrivals). GC-STATIC stays OPEN/NO_WITNESS; single item unchanged (arrival-divergence rate law). Zero kills.

### C175-1 RVTAX run/first-violation/tenure taxonomy + remaining route corpses [AUTHOR precision + PROVED_KERNEL frame]
First D6-violation is always a run-start KEEP (DELETEs: -6e_A<=0 never cross; mid-run accesses contribute 0 (needs+S_A posted at run starts)): (A) run-starts-with-KEEP (deficit need*-6e_A*, dB>5dA+1+B kernel d6_no_first_violation) or (B) tenure shape (DELETE banks e_A^del>=1 by root-dislodge, B frozen; first KEEP e_A*=0, need*=dB_del-1; uncovered dB_del-6e_A^del-1 needs global pool = arrival-divergence rate). Genesis/T0-root runs always surplus (twins); synced runs deficit<=1 (kernel synced_run_le1). hall_lemmas 8AC-RV: exact first-crossing taxonomy (geometry banked, aggregate open). Remaining route corpses (analytic, no doomed experiments): I weighted-cut (bystander-unbounded/log-class), II/IV/X rank/log/earthmover/classical (supply-vanishing: access lemma bounds demand while S_A vanishes exactly on dangerous steps), III dual (dual-of-game = potential; feasibility = charging), VII rotation-injection (log not constant), IX normal-form (non-confluence). Run-canonical frame kernel stands (runstart_bank/genesis_run_surplus/synced_run_le1). GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS; single item stands. Zero kills.

### C176-1 TWINEX twin-exclusion + manual ARS loop verdict [AUTHOR structure + FINITE]
8AC-TWINEX: single-root exclusion proves supply-free deepening forces burst key off-root (dA>=1, burst banks e_A>=1 via ecount_pos); (0,eB)-bursts pair with banking DELETE-arrival + frozen-B window (KEEP-arrival would un-deep; between-accesses forced DELETE no-ops). Re-arrival D6-net = 6*ceil(dA_arr/2)-(dB_arr-1), negative iff arrival-diverged; arrival-divergence regresses with no constant closure (same wall, sharpest pair form). Manual ARS loop executed: sharpest abstract violator (arrival-diverged pair + frozen window) realization-attempted positionally; free variant KILLED by twin-exclusion (two-root impossibility); remaining variant = arrival-divergence rate (open). Conditional on free-ride-floor (FINITE-STRONG). GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS; single item stands. Zero kills.

### C178-1 LRI local-reweighting kill test: W1 linear, W2 log, W4 bounded [FINITE + AUTHOR theory]
scripts/wp6_lri.py -> lri.json (ZIG/doubles every site, vines/balanced n=32..2048): R per StepEv W1-depth ~2n LINEAR (whole-subtree gains) DEAD; W2-subtree ~log n 8.9..21.0 DEAD slowly (merge ratios); W4-heavy-light-no-max EXACTLY 2.0 bits (1 gainer, LR-double) ALL n — bounded positive reweight EXISTS (positive lemma). But LRI-1 fails around it: mass-divergence at c1<=3 (D6 needs c1~=3, divergent boundary; satisfiable only c0~25/c1>3 i.e. weak), log-terms ~11/access on zero-banking trivial accesses, composition drowns (log-terms + 5.5*S_A reweight exceed GC allowance alone). Trilemma/dilemma confirmed: persistent + depth-tracking + local-increase incompatible; tracking-vs-vacuous dilemma absolute. audits/REWEIGHTING_BRIDGE_AUDIT.md filed (cross-audit: LRI genuinely new; W1/W2/W4 + progress-factor + ST85-design analysis). hall 8AC-LRI. LRI-for-D6 DEAD. Pair-Access-large-C side door open in principle (not pursued). GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS. Zero kills.

### C179-1 PARATIO W4 large-C route REFUTED, BRANCH E [FINITE asymptotic witness]
scripts/wp6_paratio.py -> paratio.json: full candidate (3*log(W/w)+1+R)/cost_A maximized (vines/balanced/comb/broom/random, n=32/128/512): max ratio 29.05/41.19/53.23, ALWAYS min-mass ROOTS on comb trees (costA=1, R=0, ratio=3*log2(W)+1; W superlinear via compounding pocket lightmass). Ratio grows ~3*log n UNBOUNDEDLY: no universal finite C exists (normalization-invariant; root-heavy repair breaks depth-tracking per trilemma). Asymptotic witness family (comb roots) kills W4 Pair-Access route per §32E; no return to D6 (no surviving route: all literature families carry exact killers). GC-STATIC + DIRECT-D6 + MSTL-14P OPEN/NO_WITNESS. Zero kills (route refutation, not theorem refutation).

### C177-1 LITBRIDGE literature arsenal exhausted with exact killers [AUTHOR audit + FINITE refutations]
audits/LITERATURE_BRIDGE_AUDIT.md (full matrix). Primary bytes: GI ESA2020 (Dagstuhl PDF 932849B sha 7e97911b, 16pp read fully) + Russo arXiv1511.03148v3 (256715B sha ca375d8a, 19pp read) + frozen L3/L6 PDFs re-read (crossing/monotonicity; 68pp L6 lemma index). v03 audit: 27/27 L6 defs translated, ZERO theorems ever consumed (MST26 scope record stands). GI transplant REFUTED (6 kills): log-depth reference required (ours vines) + additive n^2/m vs margins 0-6 + moving reference uncovered + reference-update creation UNBOUNDED ~n^2/2 per StepEv measured (gistep.json: 496..130808 across n=32..512; single zig exactly 1) + witness-interval vacuous at |S_O|=1 + per-access B<=O(A-depth) false on diverged. Surviving fragments (insufficient, unformalized per policy): CP-existence 0/530 fails, twin Phi_0=n exactly, subject net-new<=0 always. Russo REFUTED (open Conjecture 3.1 premise + global-additive + per-access false on (0,127)). L3 INAPPLICABLE-AS-PROOF (foundation only; crossing blind to vine-danger: 253-depth burst has crossing~=2, bookkeeping~=251; lower-bound direction wrong). L6-theorems REFUTED (K1/K2/K3 per load-bearing lemma; lazy-gap mass ANTI-CORRELATED with our danger: shallow reference => small gaps exactly when bursts explode). Branch-A/B EXACTLY_SUBSUMED. No surviving bridge; monotone refinement terminates (all families exhausted). GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS; single item stands. Zero kills.

### C180-1 ASYM asymmetric ancestor pairs dead both sides [FINITE + AUTHOR mechanisms]
scripts/wp6_asym.py -> asym.json (Euler-tour ancestor tests, vines/balanced/comb/random n=32/128/512): A-splay nets [-473,+62173] (creation O(n^2): vine-B makes every A-flip count; ratio O(n) vs cost_A); B-splay nets [-62173,+478] (x-pairs destroyed exactly -d monotone, bystanders add +O(n) creation vs cost_A=1). hall 8AC-ASYM: four independent killers (reversed twin-chains kill edge/boundary/level RELEASE with zero disagreement at depth d; splay-obliviousness kills rotation-distance contraction; granularity dilemma (fine breaks CREATE via O(|b|) bystander flips, coarse breaks RELEASE); rigid coherence kills signed cancellation (same-direction moves)). x-specific exact destruction (-d) swamped by bystander nets; quotienting it needs future burst key. No Phi of this family closes CREATE+RELEASE. GC-STATIC + DIRECT-D6 OPEN. Zero kills.

### C181-1 BELLMAN H1 barrier: BD1 holds everywhere, BK1 fails +11 scale-emergently [FINITE falsification + AUTHOR]
scripts/wp6_bellman.py (fast v2: formula-H1, replayed post-states, spot-validated 0 mismatches) -> bellman/h1_attack.json. Walk (60 histories): rd_max=0 (DELETE barrier HOLDS on all reached states), rk_max=+11 (KEEP barrier FAILS once: micro-gen s=6 access-5 KEEP, hypothetical KEEP-1 with (a,b,da,db)=(1,32,1,63), H1 31->13, residual 32+13-31-3=11; Phi=97 there so GC holds (barrier non-inductive, not violated)). min(Phi-H1)=0 (barrier tight but holds on walked). Beam (myopic max-residual): v=0, never builds divergence (setup has <=0 residual). Exhaustive n=3,4,5 (ALL BST pairs, all keys/modes): rd=rk=0 universally => BD1+BK1 hold on all small pair-states => GC-STATIC PROVED for n<=5 (H1 Bellman-closed + induction + diagonal H1=0; AUTHOR/bounded-exhaustive). BK1 failure needs deep divergence (dB~63, scale-emergent like minload-2). Next: minimize +11 witness, F_2/F_3 closure, closed-form guess. Zero kills (barrier failure, not GC refutation).

### C182-1 FK-LADDER F_2/F_3 stabilize locally + BD1-AUTHOR + pack-death + tautology [MIXED]
scripts/wp6_fk.py -> bellman/fk.json: witness (pool 97) F_1=31, F_2=42 (KEEP-1: absorbs +11 shortfall exactly), F_3=42 (no depth-2 shortfall; setups bank). Liability stabilizes LOCALLY (not universal: F_3 global needs symbolic bound = rate law). BD1 AUTHOR (DELETE half universal): rotation rows +-1 exact per region (kernel SplayRotate) + telescoping rotations=depth (finite-exact 3517/0 + banked b_event_count_lemma) + ceil-subadditivity + max-algebra + B-freeze on DELETE (code) => H1(D_x)<=H1+3a_x; halves F_2 (DELETE branch redundant); Lean ride-induction skipped (non-sufficient half: BK1 fails anyway). PACK DEAD: second-key o-shifts reach +87 measured (need unbounded slack; F_pack would need shift-bound that fails). TAUTOLOGY identified: pool>=0 <=> sum-nets>=0 (definitional, no vehicle); F_k-positivity <=> length-k witness (same hardness as direct assault); F*-finiteness <=> rate law (circular). PUMP channel assessed: 72 walks vacuous (no revisits; state space dwarfs walks), small-n precluded by H1-closure proof, large-n revisits unreachable (no inverse splays). FLOOR banking (+6 D6-stock per diverged push via dA>=1 floor or turnover) real but insufficient (spending unbounded). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C183-1 BD1-AUTHOR DELETE Bellman universal + Bellman status ledger [AUTHOR theorem]
8AC-BD1: H1(D_z)<=H1+3a_z universally (measured rd<=0 everywhere; proof from verified rotation rows +-1/0 exact + telescoping 3517/0 + ceil-subadditivity + max-algebra + B-freeze). Consequences: DELETE-side never needs Bellman closure (any future proof cites BD1); F_2 drops DELETE branch (KEEP-lookahead only: F_2(s)=max(F_1(s), max_x[b_x+F_1(K_x)-3a_x])); BK1 failure (+11) isolated as the SOLE Bellman gap (KEEP side only). Closed-form verdicts: F=H1+C dead (cancels in Bellman differences); F=max(H1,Phi) needs H1-monotonicity (false: +87 shifts); F_pack needs shift-bound (measured +87 unbounded); F* finite <=> rate law (circular, not progress). Remaining: KEEP-side closure (F_2 symbolic bound = rate law) or GC refutation via Q_x>Phi with Phi'<0 (never observed; KEEP-RESIDUAL margins unmeasured — next falsifier). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C183-2 KEEPRESIDUAL scalar falsifiers: PREPEND-2 + COLLAPSE dead, H2/DELETE-H2/KEEP-RESIDUAL survive [FINITE + AUTHOR pivot]
scripts/wp6_keepres.py -> keep_residual/{prepend_n4,n5,n6,prepend_vine32,vine64,rootcollapse_n3,n4,n5,walk}.json + beam/deepdiv/walk48 inline. PREPEND-2 REFUTED universally + unbounded-linear: vine(n) triple (n-2,n,n-1) saves n/4-1 (n=8:1, 16:3, 32:7, 64:15); minimal killer n=4 vine [1,None,[2,None,[3,None,[4,None,None]]]] arg (2,4,2) saves 1 (prepending banks shared-path depth: splay non-monotonicity, exact mechanism). Bounded-prepend (saving<=a_z or <=3a_z) untested; bypassed (unneeded: DELETE-H2 holds directly). ROOT-COLLAPSE (same-root => H2=H1) REFUTED: +1 at n=32 random same-root (H1=1,Qmax=2,gap 0); ROOT-COLLAPSE-REACH (post-KEEP, roots equal by construction) REFUTED: +1 at n=32 post-KEEP (H1=0,Qmax=1). Exhaustive n<=5 same-root max 0 (small-state collapse holds; failure scale-emergent like BK1). Walk rc=2 (n=16/32) / 4 (n=48) all different-root (24 vs 21 etc): NOT collapse counterexamples (Q-excess on diverged roots is H2's purpose); rc grows mildly with n. SURVIVORS (all finite-held, zero kills): (a) H2-IDENTITY gap=0 (DEL2 never exceeds max(H1,Q)): universal exhaustive n=3,4 (25+196 pairs) + walks n=16/32/48 + beam + deepdiv => DEL2 branch REDUNDANT, and it FOLLOWS from BD1 (DEL2(z)=H1(D_z)-3a_z<=H1 since B frozen on DELETE states); (b) DELETE-H2 H2(D_z)<=H2+3a_z: dh_max=0 universal n=3,4 + walks + sampling n=48; (c) KEEP-RESIDUAL reach Q_x<=Phi(h): kr_max=0 walks n=16(L40)/32(L25)/48(L30,1/4-key sample) + myopic beam n=16 (12 steps, always 0) + deepdiv vine-24 alternating (Phi banks to 64, H1=H2=Q=0 throughout); universal-Phi0 version false (+1 n=3, +2 n=4 on arbitrary diverged pairs) as EXPECTED/irrelevant (induction carries true banked Phi; BK1-+11 witness has Phi=97 vs Q_x=42, margin 55: kr strictly weaker than BK1, robust exactly where BK1 dies). Pivot: carry H2=max(H1,Q) as separate object (no collapse); epoch induction scaffold = BD1-corollary + DELETE-H2 + KEEP-RESIDUAL + KEEP-2STEP hypotheses => Phi>=H2>=H1 preserved (Lean GCStaticKeepResidual). GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS. Zero kills.

### C184-1 KEEP-2STEP kill hunt negative + Lipschitz architecture + universal-KEEP-Lip +1 witness [FINITE + AUTHOR reduction, NO TERMINAL]
scripts/wp6_keep2step.py (modes walk|targeted|beam|phimin|triples) -> keep2step/{kr2_walk,kr2_targeted,kr2_beam,phi_min,future_triples,lip_witness}.json + audits/GCSTATIC_KEEP2STEP_DECISION.md. KR2<=0 EVERYWHERE reachable: Phi_min BFS n=3 (19 pairs) + n=4 (196) worst 0; walks n=8..48 best 0 tight; 14 targeted fams 0; beam 0 (weak adversary, noted); triples best 0 (Q(s1)=0 in 95%+); BK1-+11 replay max -55 (margin 55); n=3 exhaustive histories 220320 states 0 kills best 0; micro 40-seed high-r sweep <=-10; matters-subcase (y!=x, Q_y>H1(s1)) occurs 11% but tiny (-17..-41). NEW ARCHITECTURE: R3(A,B)=max_x[r_x+Q(K_x)]; KEEP-2STEP = P(h):Phi(h)>=R3(end(h)) by history induction from R3(diag)=0 + DELETE-Lip (R3(D_z)<=R3+3a_z, clean EVERYWHERE: all pairs n=4,5 + arbitrary n<=24 + reachable, tight 0s, conjectured universal) + KEEP-Lip (R3(K_z)<=R3-r_z, clean ALL reachable incl R3=42 micro extreme with slack). UNIVERSAL-KEEP-LIP REFUTED: +1 excess, 2 hits/60 arbitrary n=24 pairs (seed 4242 trials 2,20; onset n>=19; clean <=18): signature = KEEP of A-rooted R3-attainer with (a,b)=(0,3), post-R3 exceeds budget by exactly 1 (max 1, never >=2; DELETE-Lip exactly 0 at same key; roots differ). Reachability of +1 pairs unknown. PROVED+KERNELIZED in GCStaticKeepResidual.lean (exit 0): §2 expansion (kr2_expand_1/2/3, phi_after_keep), y=x attainer collapse to KR (wild-confirmed micro s=6), gap<=H1(s2) compression, Lipschitz induction steps (lip_delete_step/lip_keep_step/lip_diag_base, conditional hypotheses). §20 saturation REFUTED (r_z=13>0). Case-(b)-with-r_y>=0 IMPLIES BK1 violation at future state (derived). Remaining gap = reachable-KEEP-Lip = bystander creation across KEEP (unified wall C176-C183, sharpest Lipschitz form). NO TERMINAL (neither proved nor refuted); nothing promoted; no sorry/axioms. GC-STATIC + DIRECT-D6 OPEN/NO_WITNESS. Zero kills (route-level +1 is Lipschitz-arbitrary, not GC).

### PIVOT8-1 C.ZIG stands proved; formalization gaps itemized [AUTHOR-complete]
ZIG (Z_B<=A, all closed pair-walks) PROVED: run-partition + <=1-zig-per-run + leading-funds (KEEP self-pairs, DELETE funds run) + disjoint capacity + zero-A subcase. No reachability, no finiteness in the math. Green kernel: deliver(+copy), splay_at_root, ecount_root, mem_splay, delete_step, ecount_eq, valid_rotR/L (Deliver/History/Valid verified green this run). OPEN mechanical only: (V1) validity for doubles+fixups+splay-induction composition; (V2) mem->sdepth-some for ecount-zero chain; (V3) history-fold + run/matching formalization. DOUBLE stays dead. DOUBLE-FLEX/B<=2A open (excess-slack, no mechanism). GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT7-2 V-correction + run-local-sum + verdict [AUTHOR + FINITE]
V=0 NEVER observed (corrects tightness claim; max V=-2; B=2A unattained). Run-local sums EXACTLY to DOUBLE-FLEX (sharp sufficient form); holds extremals/killer tight, fails open steered (needs diverged-closed test). B<=2A unproved; no V>0. GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT7-1 DOUBLE-FLEX assault: ZIG stands, B<=2A unproved [AUTHOR + FINITE]
ZIG run-proof complete (premise audit done). DOUBLE-FLEX/B<=2A OPEN: divergence-telescoping dead (+1798 anti-corr); counting insufficient (proved); all reformulations tautological. V-max -2, V=0 tight attained. GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT6-1 DOUBLE-FLEX: n=5 matching + V=0 tight + ZIG proof [FINITE + AUTHOR]
6/6 doubles match (4 PRIMARY-same + 2 FLEX; overflow = 2nd doubles of B-depth-4); StepEv parse 360/360; V-max -2, V=0 attained (tight); run-local tight on extremals; ZIG run-proof + premise audit (validity-doubles open mechanical). B<=2A needs excess-slack (open). GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT5-1 DOUBLE refuted (n=5 witness) + ZIG proved-modulo-banked [FINITE + AUTHOR]
DOUBLE false: [(K5),(K1),(K5),(K3)] closed, QB=6>A=4 (all-doubles, ZB=0); onset n=5 (n<=4 holds exact). ZIG proved by run-structure (injective B-zig to A-StepEv assignment; needs validity-full-splay + ecount-chain (assemblable) + deliver/noop (banked)); holds all closed walks (no reachability needed). B<=2A needs excess<=slack (no mechanism). GC-STATIC OPEN/DO OPEN. Zero GC kills.

### PIVOT4-1 Two-lane data (SUPERSEDED on DOUBLE by PIVOT5-1) [FINITE + Lean]
Lane identities green. DOUBLE+ZIG zero failures (extremals/oracle/corpus/periodic/twin/steered); sharp anatomy Z_B=A,Q_B=A-2,B=2A-2 confirmed both maximizers; B=R_A + defect=Z_A=2 new pattern. n=8 hunt max 1.0 (twin-locked). B<=2A needs DOUBLE+ZIG proofs (open). GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT3-1 Rotation/parity anatomy + rho_6=5/3 + motif lifts [Lean + FINITE exact]
StepEv 2e=rot+zig + sums green. ROT REFUTED (n=3:4>2); corrected R_B<=R_A+Z_A TIGHT all extremals; ZIG holds everywhere (tight); all-KEEP R-invariance twin-trivial only, false diverged (8v6). lip_compose green (refuses correctly on 5/3). rho_6=5/3 EXACT (int-BF cert + replay achiever [K3,K6,K3,K4,K2,K1] A6B10, all r<0). 3/2 motif lifts ALL n>=4, 5/3 lifts n>=12 verified (gap-block opacity proved; sup>=5/3). Mixed=max via noop-padding. Pattern (2k-1)/k suggests sup 2; n=8 open. GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT2-1 Recurrent ratio exact n<=5 + recovery + bias [Lean + FINITE exact]
Oracle (wp6_cycle_ratio.py + exact int Dinkelbach/BF): single SCC n<=6 (all pairs reachable all diagonals); zero-A-posB cycles 0 everywhere (theorem + finite). rho: n=2:1, 3:1, 4:3/2, 5:3/2, ALL CERTIFIED (integer BF + achievers); n=6 pending (graph built 17k/209k). Extremals all-KEEP ([K2,K1,K3,K4], [K5,K4,K5,K2], A=4B=6). Recovery: local-2 edge + min-A return (3,4) -> closed 3/2. Checkpoint graph agrees 3/2. Periodic to n=256 max 1.0; two-key exhaustive 1.0; dual bias corr depth-disc 0.73. Conjecture rho<=3/2 universal (unproved). Kernel: reward_identity/add/pump_step green. GC-STATIC OPEN/DO OPEN. Zero kills.

### PIVOT-1 Literature exact + heap-viol dead + translation green [Lean + FINITE]
LT 1907.06310 (DO<=>approx-monotone; repeater absorbs g; crossing monotone<=4; Splay per-removal fails) + Chmel 2607.18498 (Õ(loglogn); losses mapped: rank dynamics persist under coupling => polylog not constant) read exactly. Cost translation kernel green (C'=2C+1,g'=2g). LT heap-viol-diff candidate DEAD (C_min 1->15.5 with n; steered n=64 needs C>=15; constant papering not paying). Ratio bounded ~1.68, SA/greedy clean to n=128. Wall invariant across potential forms (sums bleed, maxes BK1, counts blind, weights polylog). GC-STATIC OPEN/DO OPEN. Zero kills.

### C193-1 Case-B macro closed + greedy-max-r fails + single open step [Lean + FINITE]
Strong Phi-induction: DELETE-last/profitable-KEEP/base FREE (banking); a_z=0-draining KEEP fuses via macro [DELETE z, noops, KEEP z] -> direct KEEP (same state+Phi, shorter history) => IH. Kernel green: macro_state_match + macro_phi_match. Macro shape verified (wild 3/3). Greedy max-r drain (480 drains n=32/64) + SA-max (15k acc n<=96, 5 shapes): minPhi never <0. SINGLE OPEN STEP: a_z>=1 draining KEEP covered (r_z<=Phi(Pfx)). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C192-2 Twin facts kernel-proved (R3_twin_zero, twin_restore, bigmax_nonpos) [Lean PROVED]
Twins have R3=0 exactly; twin+DELETE+KEEP restores twin exactly. Explains steered post=0 (twin-adjacent); micro-diverged not covered (recorded limit). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C192-1 Strict ledger + B-single + trace-fold assessment [FINITE + AUTHOR-negative]
Full 19-word strict ledger plus1 (min gap exactly 1, 6× tight; terms r_5=0; defect pure r_z=3). Winner-menu collapses to {[],[z],[z]+sub,same} — never clever words (all data). B-side single-prepend HOLDS tight (A:1,2-word ok; B:1-word ok, 2-word +4 dead). Single-prepend kernel-proof needs trace-fold/applySteps semantics (ABSENT from kernel) + per-step lower rows: major formalization, specified not started. No trace-fold exists (grep). NEITHER END attainable: proof blocked (drop-corr + O5 + ROT + clean/macro + a>=1), falsification clean. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C191-1 DEFECT identity + strict census + F3 verdicts [Lean + FINITE]
DEFECT=r_z+3DROP_A-DROP_B kernel green (defect_identity). §9 certificates: plus1 defect pure r_z (drops net 0, no-tie strict gaps all>=1); steered defect>0 but saved via [z] (preR3=tgt); NO single separating condition (parities identical). Strict len-3 census: ZERO on walks/micro-post-KEEP (62+ states); EXISTS micro s=10 ([51,50,7] post 11, no ties) — hard branch reachable-realized. F3=F2: fails +2 micro post-KEEP (ladder route dead as universal; word-saturation via F3 dead). B-saving min -12/-7 kills pure-B. Small-n +1 hunt clean (onset>=19 genuine). NEITHER END reachable. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C190-1 TARGET direct: doubleroot kernel + no-terminal verdict [Lean + FINITE]
TARGET (r_z+R3(K_z)<=R3(s) reachable) frozen. Closed: STOP/[z]/len<=2-exact/tie-rule/len-1-DELETE-mod-SP/doubleroot-kernel(target_doubleroot_tree green, 0/12). Hard remainder: strict len-3 same-chain correlation (plus1-shape, arbitrary-only). B-saving min -12/-7 kills pure-B a_z=0 lemma. Small-n +1 hunt clean (onset>=19 genuine). Rotation analysis unexecutable-in-principle for drops; history-minimality adds nothing. NEITHER END (blocked, not refuted). Audit GCSTATIC_TARGET_DIRECT.md. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C189-1 Attainer exchange: selector complete, B-prepend dead, kernel [FINITE + Lean]
Exchange scanner (wp6_exchange.py -> attainer_exchange/): hard set (vine52 STOP-saves via outside root; plus1 genuine violation isolated; BK1 F0-tight with repetition) + 424-transition scan 0 lipfail, F2+ never needed. SELECTOR: STOP(tgt<=0) / [z](len-0) / [z]+sigma(KEEP len<=2 EXACT) / [z]+sub(s'-tie) / same-chain-or-violation. B-side bounded-prepend REFUTED (+4): DELETE has no [z]+sub rule. Tie data: walk len-3 all tied; plus1/t=5 no ties (exact diagnosis). Len>=2/tgt>0 pattern REFUTED n=24 (12 hits: 10 same-tight, 1 F2-exact, 1 violation). Kernel: R3_nonneg/exch_stop/keep_exchange_short+tie (conditional; O5 word-model specified). REMAIN: same-chain drop-corr (1-term closed-mod-SP; 2-term finite; 3-term open) + O5 + ROT + clean/macro + a>=1. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C188-1 Subcase split: 1-term closed, single-prepend, 2-term finite [Lean + FINITE]
Non-z DELETE attainer splits by floors: 1-term (Q(s1)=0) CLOSED mod single-prepend (kernel delete_lip_1term + resid_le_R3). SINGLE-PREPEND (extra splay never saves next access, saving_1<=0) finite 0/2640+ tight; AUTHOR-sketch via rotation counting (drop<=rotations=d_z, ceil-halved). 2-term (H1(s2)=0) jointness (Dx+Dy>=-a_z) finite-clean min exactly 0 (vine refutation was 3-term H1=2, consistent). 3-term (H1>0) + KEEP a>=1 REMAIN OPEN (bystander creation, no mechanism). GC-STATIC NOT PROVED (blocked) / NOT REFUTED (exhaustive negative). Zero kills.

### C187-1 KEEP split: post-att never z + B-from-D tight + kernel [FINITE + Lean PROVED]
Post-KEEP R3-attainer NEVER z (61/61 reachable; bystander liability; opposite to DELETE 98.6%). B-only Lip REFUTED arbitrary-A (+4) but TIGHT from A-rooted D-states (0). KEEP-Lip = DELETE-Lip + B-from-D exactly. Kernel green: bstep_zchain_exact_tree (z drops exactly b_z) + keep_lip_split. Remainder: non-z correlation both halves. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C186-1 Same-B H1-diff kernelized + layering impossibility [Lean PROVED + AUTHOR negative]
h1_diff_sameB kernel green (floor-aware, mechanics-free via foldmax_diff; outer max(0,·) load-bearing — un-floored form false in double-zero case). Single-key saving<=a_z finite-clean (tight). NEGATIVE: nested max-lifting multiplies budget by lookahead depth (3a_z+3a_z+... per level: 3x per level), so jointness (S>=0-ish correlation) is unavoidable — no layered bound closes without it. AUTHOR-derivation: gap-zslack<=-3S (needs nested Q-diff). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C185-3 Max-algebra lifting kernelized [Lean PROVED, mechanics-free]
GCStaticKeep2Step.lean += foldl_max_init_mono, max_sub_max_le, foldmax_diff (exit 0): per-key drop bounds lift to fold-max bounds with NO splay mechanics (pure order theory). DELETE-Lip now factors into kernel-proved lifting + open per-key drop bounds (mechanics) + non-z correlation. Bare-Lean notes: order reasoning via omega+hyps; shape-split before unfold; simp proves ∈-cons goals. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C185-2 Double-rooted-R3 killed + a_z=0 KEEP-Lip closed conditional [FINITE + Lean]
Post-KEEP (double-rooted) R3 hits 11 on micro (no general cleanliness). A-free KEEP (a_z=0) splits: reachable post-R3=0 always, arbitrary to 2 — ROOT-KEEP CLEANLINESS reachability-essential (finite). Kernelized Q_nonneg/resid_le_R3/keep_lip_afree (exit 0): a_z=0 subcase (both +1 witnesses) follows from cleanliness + R3>=r_z. Remaining: a_z>=1. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C185-1 Tree H1/Q/R3 layer + steered-signature verdict [Lean PROVED (conditional) + FINITE]
lean/WP6/GCStaticKeep2Step.lean kernel green: tree resid/H1/Qchain/Q/Rchain/R3, fold-max dominance, delete_zchain_exact_tree + delete_r3_zpart_tree grounded to single hNode (banked deliver path). Non-z attainers 1.4-2.5%, all slack (one tie-artifact); tight=>z-attains (ties). STEERED +1-signature (DELETE-reroot after churn, n=24/32, 20+ steers) holds tight every time (post-R3 annihilates to 0); same signature +1 only arbitrary. Reachability load-bearing for KEEP-Lip; pure-state proof impossible. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C184-3 DELETE z-chain exactness + attainer statistics [FINITE + AUTHOR + Lean-conditional]
Post-DELETE R3-attainer is z itself 98.6% (414/420; 512/525 prior sweep); every tight DELETE-Lip case has attainer z; all non-z attainers carry slack. z-chain growth EXACTLY 3a_z by root-noop (r_z(D)=b_z; K_z(D_z(p))=K_z(p) same state) — kernelized conditionally (delete_zchain_exact/delete_r3_zpart, exit 0); grounding available via kernel splay_at_root (GCStaticLoop.lean), needs H1/Q tree layer. Remainder: non-z attainer drop-correlation (2.5%). GC-STATIC OPEN/NO_WITNESS. Zero kills.

### C184-2 Resumed: bounded-prepend universal + DELETE-Lip skeleton + per-chain impossibility [FINITE + AUTHOR]
BOUNDED-PREPEND (new AUTHOR lemma, finite-universal, tight 0): C_T(x,y)-C_T(z,x,y)<=a_z(T) — exhaustive n<=6 + vines/balanced/random n<=64 (unbounded PREPEND-2 stays dead; this bounded form feeds DELETE-Lip). DELETE-Lip proof skeleton: B-terms cancel EXACTLY across DELETE (B frozen, same x*/y* KEEPs) reducing to attainer A-drop correlation (gap isolated). PER-CHAIN GROWTH NOT LIPSCHITZ: +52 chain growth across DELETE banking 45 (vine32 diag z=30; R3 grew only 20 via max-structure) => chain-wise induction IMPOSSIBLE, any proof must use max-structure (negative guidance). Drop-sums S<0 attainable for arbitrary keys (to -11) => attainer-essential. GC-STATIC OPEN/NO_WITNESS. Zero kills.

### PIVOT9-2 Vine excursion decomposition: open law + census + bounds + coverage [AUTHOR + Lean + FINITE]
OPEN VINE LAW PROVED+KERNELIZED: B(V)-A(V)<=tau(s)-tau(t) on vine paths (tau=differ-bit; per-edge verified 2688/2688 n=6; Lean vine_path_bound green; sharp via (0,1)). Bit-convention bug fixed (Lean bits are twin-bits; PIVOT_VINE_UNIVERSAL.md flips restated differ-consistently; math unaffected). CENSUS: n=6 (9600 shortest first-returns, W in [-12,+2], 58 positives all-KEEP len3-4 exits (K,1/6,a=0,b=2-5) differ->twin); n=7 streaming (46592, W in [-18,+2], 104 positives (103x+1,1x+2 at (4,10))). Max surplus +2 both n, no length growth (longer excursions more negative). BOUNDS: E0/E1/E2/E3-as-universal REFUTED with exact witnesses (E3 holds 9592/9600 + 46591/46592; failures = +2 excursions, residual exactly +1); E4a fails same 8 (re-entry always costs A>=1: 8768x1+832x2, zero A=0); E4b (B<=3A on excursions) HOLDS fully n=6,7. RESIDUAL EQUATION (exact): total W_2 = SUM r_E - A_vine (charges telescope); E5 needs vine-A cover of 8+1 residual-+1 types: OPEN. +2 SELF-REPAYING (finite): shortest closures -12..-18; exact bounded max-returns (len<=12) -13..-15 (closures -11..-13); no vine path +2-end->+2-start (chaining impossible in chamber). ENTRY THEOREM (n>=5, V1-contrapositive): leaving requires depth>=2; finite types (doubles x A-only52/both44/B-only4). EXIT: destroys last 1-2 branches; token moves (same-key 1.6%; +2s flip ends). 5/3 EXTREMAL avoids vine-pairs entirely (u0=137 mixed, per-edge W 0,0,-1,0,0,-2 defect on two (1,1)s): non-vine-only max rho = 5/3 = global (SPFA ceiling tight). HUB: single SCC n=7 verified both directions (184041/184041); sweep KEEP1..n->left-vine universal word (finite-exhaustive to n=10+random; pair version -> twin vine); LV reaches all shapes to n=8; universal return-word open. ANCHOR: conditional chain proved (E5-vine-return + both-direction hub => no positive cycles); E5 + universal hub remain open. DO OPEN. GC-STATIC retired, unvisited. Zero kills (decomposition, exact witnesses banked).

### PIVOT10A-1 VINE-VISITING-C2 conditional proof via debt-machine [AUTHOR + Lean + FINITE]
9 residual-+1 classes share ONE signature (no literal words used): A-rooted deep-B KEEP exit (0,3) + 1-3 neutral (1,2) middles + (1,1) twin re-entry; (A,B)=(2,6) n=6 (8, mirror pair) + (4,10) n=7 (1); exit +3 / mids 0 / reentry -1, boundary +1, residual +1. CONDITIONAL THEOREM: closed vine-visiting walks satisfy W_2<=0 (n>=5; n<=4/5/6 by global rho certs) given D1 (r<=1), F1 (+1 ends twin), F2 (+1 starts differ), R0 (twin-start r=0 ends twin). DEBT-MACHINE (finite-state counting, no potentials/choices): debt-bit (<=1 outstanding: second +1 needs differ-start while debt forces twin, via F2+invariant); creations pair with first-clearing-forward (A>=1-vine by T1 from twin, or r<=-1) disjointly (strict betweenness); walk-start-twin tail pairs with payer-before P_0 (first-differ-reaching needs payer by T1+R0+F2+D1; P_0 distinct (before C_1)); leftovers <=0; total <=0. NO sharing pathology, NO word-specificity. T1 kernelized (Lean twin_exit_A green: twin-start A=0 => B=0; +V1+noop assembly). HYPOTHESIS SUPPORT (all load-bearing, unproved universally): D1 finite-exact shortest n=6,7 (max +1) + DFS non-shortest sampled (no r>=2 in ~8M expansions) + steered n=8..20 (~12k trials, max r=-8); F1 9/9 end twin + no end-differ +1; F2 9/9 start differ + twin-start max -8; R0 exact 56/56 (n=6) + 72/72 (n=7) twin-start r=0 ends twin + steered none. Falsification hunt for r>=2 / twin-start-+1 / twin->differ-r=0: all negative. R0 kills the twin-start chaining that would break debt (twin-start r=0 always ends twin; +1 needs differ-start). VINE-VISITING-C2: CONDITIONAL SUCCESS. Global B<=2A still needs non-vine-only chamber (§18). DO OPEN. Zero kills (conditional proof + exact witnesses).

### PIVOT10B-1 Excursion-bit law: finite-exact + partial universal + obstruction [AUTHOR + Lean + FINITE]
EXCURSION-BIT r(E)<=d(s)-d(t) (DT:+2 / DD:0 / TT:0 / TD:-2 on W_2) EQUIVALENT to D1/F1/F2/R0 jointly (mechanical both directions via integrality; recorded). FINITE-EXACT: n=6 all 9600 shortest (per-class maxW TT:0/DD:-2/DT:+2/TD:-3, tight TT+DT, zero violations; counts 3530/1648/3216/1206); n=7 all 46592 (same, zero violations; sole +2 is DT). UNIVERSAL PROOFS (new): §10 vine bit-change d(v)-d(u)<=A(V) ALL n (per-edge: a=0 keeps twin (root-tracking) else diff<=1<=a; telescope; Lean vine_bit_le_A + vine_step_le green); re-entry A-forcing (lands-differ ==> DELETE a_r>=1: KEEP twin-roots; a_r=0 ==> pre vine-pair); no-A-zero excursions (B-root/frozen lock); length-2 DD/TD W<=-3 (n>=5: DELETE re-entry needs B-pre vine so exit is A-only (V1: a_e>=1, b_e<=1-or-0) + re-entry -2a_r; data: DD max -4, TD max -3 exact). OBSTRUCTION (precise): interior B-restoration capacity per StepEv type unbounded in principle (deep splays) but empirically capped (single zig fixes <=2 branches; +1 family needs its neutral middles + (1,1) closer); proving any restoration bound needs per-StepEv branch-creation/elimination lemmas = C.ZIG-ownership machinery (next campaign). FALSIFICATION negative: steered n=8..32 (~15k trials: deep-B/shallow-A exits, long/all-KEEP/DELETE-poor, lifts/mutations) max r=-8; four thresholds (DT r>=2, DD/TT r>=1, TD r>=0) never breached. VINE_VISITING_C2 stays CONDITIONAL (debt-machine needs the bit law). NO universal claim. DO OPEN. Zero kills (exact witnesses + partial universal theorems).

### PIVOT9-1 Universal vine-pair B<=A PROVED (n>=5 proof + n<=4 finite) [AUTHOR + Lean kernel]
THEOREM: closed walks confined to vine-pair states satisfy B<=A, all n (C=1, first universal region). LEMMA V1 (n>=5): vine-preserving splay has depth<=1 — contrapositive by first-double-step analysis (code order grandparent-first): non-leaf x branches (zigzag always; zigzig keeps outer + gains p-side, inner-only branches middle instead; kernel vine_LL/RR/LR/RL_branch green); x-leaf straight mirrors locally, continuation forced (depth-2-leaf forces n=3, depth-3-leaf-mirror+zig forces n=4 by node count; n>=5 always reaches a branching double with x carrying a child); persistence: x-branched stays branched through rises (keeps real far + gains real parent-side), descendant-branches ride rigidly (rotations rebuild only matched triples). BOUNDARY REAL: n=3 extreme depth-2 mirror + n=4 extreme depth-3 zigzig+zig preserve (measured True; break at n>=5) => n>=5 threshold exact. CLASSIFICATION (depths<=1 => costs in {0,1}^2; twin bit by root-tracking): (0,1) entry-only +1 (from-twin impossible); (0,0) self-loops; (1,0) never 1->1 (from-twin only DELETE-exit -1); (1,1) lands twin always, never 1->0. COUNTING (kernel vine_cycle_nonpos green): N01<=entries=exits<=N10 => B-A<=0. FINITE BASE: integer BF no-positive-(B-A)-cycle on vine-pair subgraphs n=1..5 (1/4/16/64/256 pairs) + re-confirmed n=6 (1024), n=7 (4096); vine-preserving=>depths<=1 verified 0-counterexample n=6,7; vine subgraph nontrivial (1152 internal edges n=6, so B<=A is genuine not vacuous). LEVERAGE: vines are the tame region (extremal 5/3 uses non-vines); next excursion decomposition. Residue-growth + potential-route-death + attainer-bug-correction recorded in PIVOT_VINE_UNIVERSAL.md. DO OPEN. GC-STATIC OPEN/NO_WITNESS. Zero kills (proof).

### PIVOT10B-1 Excursion-bit REFUTED by sweep-return family (exact witnesses) [FINITE falsification]
EXCURSION-BIT r(E)<=d(s)-d(t) is FALSE universally. Witness (replay-verified, sha c7d01179, vine_excursion/refutation_n32.json): n=32 start (inc-vine,dec-vine) differ-pair; word K1+K1..K32 (33 all-KEEP); interior 32 states ALL non-vine; end twin-vine (32,32); A=31,B=71,W=+9. DT class needs W<=+2: have +9. Residual r=+8 (needs <=+1): D1 DEAD. Smaller sibling n=20 (L=21,A=19,B=42,W=+4,r=+3). Onset <=20 in sweep family; best-W n=8..32: 0,0,1,2,4,5,9 (~n/4 growth). Mechanics: exit (0,16) [B-depth-31] + sweep phase sustaining B/A~2.29 (per-step ~(1,1.7)); sweep repays (-7) but cannot cover deep exit (+16). KILLED: EXCURSION-BIT, D1, E3-universal, PIVOT-10A debt-machine (hypotheses false, not open). NOT killed: Lean kernels (true proved statements re classified walks); PIVOT-9 vine B<=A; n<=6 rho certs; C.ZIG; E4b (witness B=71<=93); global B<=2A (witness OPEN; rho->2 stands). CONSEQUENCE: VINE_VISITING_C2 loses debt route, returns to OPEN; uniform-residual charging dead; next routes must bound exit-minus-return jointly per excursion (residue grows ~n/4). F1/F2/R0 (about r=+1/r=0) technically unrefuted but moot (residuals reach +8). DO OPEN. Zero kills on global (refutation is of the bit law, an open-walk statement).

### PIVOT11-1 Vine-disagreement credit: NEGATIVE endpoint, R0-rule banked [AUTHOR + Lean + FINITE]
Vine endpoint-choice encoding (L/R words) bijective 2^(n-1), roundtrip exact; vine roots always global endpoints (1/n) so pos0-diff = twin-bit exactly; deep-frozen on vine-internal moves (letters change only at positions {0,1}, max verified + provable via zig/noop-only (V1) + rotation tables); vine-edge combos collapse to 8 (W,d1,dtau). ~40 candidate D falsified (Hamming 128+41; H+tau 128+28; weighted x4, directed x5, subsets x9, rank x2, deep-mass grid x9, twin-augmented with PROVEN coefficient contradictions; bias h flat 0..3 uncorrelated with spine). R0-RULE (D=2tau): 0 violations on ALL n=6 macro (2688 vine + 9600 excursions) + n=7 derived; UNIVERSAL on vine-edges/paths (n>=5: V1-costs + root-tracking flips per combo; n<=4 finite 2/16/64/210, 0 viol); Lean vine_W2_twin_bound green (pre-existing); tight on +2s and (1,0)-exits; range-capped +2 so witness (+9) exceeds it. n=32 family anatomy: A=n-1 exact, per-step ~(1,1.7), twin-roots throughout but branched shapes, H 31->0, W +16-10-then-repay to +9. Tensions (structural, not luck): swap/growth opposite twin-signs; creation/destruction overlap every deep position; scale-vs-tightness; bias flat. No additive positional D can close vine-visiting cycles; joint exit-return bounding or C.ZIG branch mechanics required next. DO NOT revive EXCURSION-BIT. DO OPEN. Zero global kills.

### PIVOT12-1 COARSE-DOUBLE Q_B<=2A: n<=6 analytic closure + program [AUTHOR + FINITE]
n<=6 PROVED with zero new computation: Q<=B termwise + banked rho (1,1,3/2,3/2,5/3<2) gives Q<2A for A>0 (hence Q<=2A-1); A=0 gives B=0 (banked zero-A theorem; also direct universal: A-free access = at root, so root/shape frozen and B changes at most once, hence closed A-free walks have B=Q=0) so Q=0. Max W_Q=0 exact (self-loops attain; all A>=1 cycles<=-1); fixed-Howard confirms (0/1); an early Howard +1/+2 reading was traced to an off-by-one depth-table bug in scratch scripts (replay-verification caught it; no audit pollution). REGRESSIONS (q/z exact): n=5 killer (4,6,0): W_Q=-2 safe; true 5/3 (1,5)-start closed (6,4,6): W_Q=-8, rho_Q=2/3, eps all<=0 (B-excess pure zig Z=6); 3620 old blocks epsilon=0 definitionally; N=32 EXCURSION-BIT killer: (31,49,22): W_Q=-13 (old +9 was Z=22 zig-noise; trajectory peaks +23 then repays); residue +2s: (2,3)/(4,8-tight-W_Q=0). rho_Q table: upper rho_n, lower best-verified (2/3 n=6 via 5/3 word; 1.0 n<=5/n=7 random closed). EPSILON census: n=6 4 bad types all a=0 (A-rooted B-deep); n=7 6 types (5x a=0 + NEW (1,3,0)); universal ladder (a,q>=2a+1); same-key KEEP-chain safe universally; n<=6 bad isolated. VINE SLACK universal n>=5 (V1 depths<=1 => q=0 => eps=-2a; n<=4 via rho-global). MATCHING on 5/3: 4/4 local, 8 credits unused, no Hall issue. PER-EXCURSION-Q program: n=6 all 9600 W_Q<=0 (max 0 tight), n=7 all 46592 <=0, n=32 -13; vine Q=0 (n>=5) so vine-visiting would close with NO charging given per-excursion-Q universal (OPEN: restoration wall). Minimal-counterexample framing + nonconsecution recorded. DO chain (C=3: B<=3A => E<=3S+g => LT<=7LT+2g => LT/DO) conditional on universal; translation parametric already. Lean: none new (no walk model). n>=7 (incl non-vine-only) OPEN. Zero kills (Q_B<=2A unrefuted everywhere).

### PIVOT13-1 Overflow genealogy: StepEv charging via creator+setup matching [FINITE strong]
MACHINERY (scripts/wp6_overflow.py): StepEv-level bipartite charging (LEFT=B-double StepEvs with ordered triples+patterns, RIGHT=2 credits/A-StepEv; count identities assert-verified; 5/3 replay reproduces banked A6Q4Z6B10). ORIGIN/creator = latest strictly-prior builder of consumed ancestor edges (transitive through same-splay steps; GENESIS if never built). SETUP (E4 reborn) = last A-root-arrival access; pays starved a=0 overflows (often DELETE pure-slack). Kuhn matching local-first + Koenig Hall-violator extraction. CANONICAL OVERFLOW frozen deepest-first but MOOT empirically (150 cycles: overflow ~all single-double (0,1,+1); only multi is (0,2,+2) x4; no (1,3), no partial k<q). RESULTS: lap2-steady FULL MATCH hunt-n6 200/200, walk-n6 63/63 (incl 5/3 fully local + n5-killer), walk-n7 35/35; full-history 189/200 + 29/35 (rest = lap1 genesis-transient only). Genesis rate 0 in steady state; creator distances 1-9; chains <=10 hops all terminating, no loops. HALL AUTOPSY: 7 pre-setup failures all starved-(a=0,q=1) with a=0 creators (N(X)=empty) on short D,K-alternating cycles; setup edges fixed all 7 -> the deficiency found the missing rule (DELETE-slack path). VIGNETTES: (0,1) acc6 of [D3,K3,K2,D1,K1] (creator lap1-K1 + setup D3); (0,2,+2) acc2 of [K6,D4,K4] (both doubles -> creator K6 credits: builder pays). NONCONSECUTION: 40 cycles, all overflow runs length 1, 0 consecutive pairs. rho_Q: upper rho_n (n<=6), lower best-found (2/3 n=6; 1.0 n<=5,7 random; 0.833/0.857 n=7 achiever words @diag 5/400); n=7 upper OPEN; exact-Howard dropped (scratch off-by-one caught by replay-verification; analytic max W_Q=0 stronger). VINE SLACK universal (V1 => q=0 n>=5; n<=4 global). Z-THREAD: excursion W_2 caps +2 confirmed (n6 58pos 50x+1/8x+2; n7 104pos 103x+1/1x+2; E4b 0 viol; positives short K-only B-deep/A-shallow). n32 W_Q=-13 (peaks +23, repays; old +9 was Z-noise: Q stays charged). SOUP: A 198dbl+140zig / B 136dbl+106zig; zigzig dominates (A120v78 B86v50); bottom-up structural. MINIMAL-COUNTEREXAMPLE criterion concrete: charge() lap2-full=False on a steady cycle; 296 cycles, 0 survive. UNIVERSALIZATION OPEN: creator-existence/churn, chain-termination, setup-availability with wraparound accounting, nonconsecution universal, non-vine-only chamber. VINE_VISITING_C2 stays OPEN. DO OPEN. Zero kills (Q_B<=2A unrefuted everywhere).

### PIVOT14-1 U1/U2/U3 PROVED + U4 located + Lean genealogy kernel [AUTHOR + Lean + FINITE]
U1 CYCLIC CREATOR EXISTS (PROVED): every B-double has a creator strictly inside its key epoch (prev-KEEP-x completion .. consumption). Epoch lemma (empty epoch => still B-root => q=0; m=1 vacuous). Consumed-descent (v2: follow consumed pre-step ancestor edges, not post-step identities): (x->p)-line always terminates in-epoch (absent-at-epoch-start (x rooted) forces a post-epoch builder; same-splay hops decrease seq finitely); (p->g)-line may escape pre-epoch or hit ETERNAL (never-rotated) edges -- harmless (max stays in-epoch via x-line). Mod-m well-defined, != consuming index. Genesis eliminated structurally (periodic extension has no T0). v2 ORIGIN patched into scripts/wp6_overflow.py, parity confirmed (hunt 100/100 identical). U2 SETUP AVAILABLE (PROVED): structural setup = latest same-key A-root-arrival (dA>0); dethrone+quiet lemma (setup interval holds only own-key accesses, all dA=0, zero middle credits); existence via backward scan (all-dA=0 => single-key cycle => B frozen => contradicts genuine B-work (overflow q>=1 or builder rotation)); setup carries >=2 credits; scope = starved links (a=0 with B-content); wraparound = mod-m indexing (one budget 2A, no duplication, definitional). U3 TERMINATES (PROVED, <=2 hops): creator (KEEP always) either has a>=1 (terminal) or is starved => its setup exists (U2 generalized) with a>=1 (terminal); no third hop, no reachability loop (free-credit question correctly separated to U4). H-STRUCTURE (PROVED): starved blocks pairwise disjoint (different keys by quiet; same key ordered by B-rooting); exactly one starved overflow per block; no two starved share a setup; creator fan-in <= 3xrotations = O(dB) (observed max 2); setup-KEEP self-competition common (26/53). U4 CAPACITY (OPEN, first unproved): same-creator fan-in + setup-KEEP self-competition unbounded in the general argument; crossing epochs kill laminar counting; missing = closed-component capacity lemma (every creator/setup-closed demand component carries enough credits). COMPOSITION CONDITIONAL: U4 => total_overflow<=total_slack => Q_B<=2A; +C.ZIG => B<=3A; banked chain to DO unchanged. FALSIFICATION (mandatory S25/S26): v2 parity + siege 255/255 (long-walk/keep/cross batteries VACUOUS (0 steady overflow -- reported honestly); cannon 60/60 meaningful) + breeder n=6 60/60 (maxlen 52, mean ovf 2.2) + n=7 80/80 + 19-cycle fan-in census; NO mechanism failure => S26 classification never triggered; Q_B>2A nowhere. LEAN lean/WP6/GCStaticGenealogy.lean GREEN (direct lean exit 0, no sorry/admit/axioms): latestBelow search (fixed a real truncation bug: hi=0 guard) + U1 descent soundness/completeness/packaged cyclic_creator_exists, all-explicit binders, splay facts as hypotheses; U2/U3/H paper-complete (Lean gap noted); U4/coarse_double NOT kernelized. Zero kills (mechanism stands; theorem open at U4).

### PIVOT14-2 U4-Core attempt: three new lemmas + minimal-X theory + 600 tests, U4 OPEN [AUTHOR + FINITE]
L1 DELETE-SETUP (PROVED): starved-overflow setup always DELETE (KEEP-setup would root B; quiet+first-KEEP forces q=0, contra) => dedicated pure-slack 2a_s pools, never a creator; 42/42 census. L2 SETUP-INJECTIVITY (PROVED): no two starved B-active share a setup (sharers share key; same-key dies by B-rooting; k=1 degenerate by dethrone/frozen); namer bounds <=1 starved-KEEP + <=1 non-starved per setup; 0 violations (69 cycles). L3 NON-STARVED EXTREMALITY (arithmetic): eps>=1,a>=1 needs dB>=4a+1 with dA<=2a (n=6: impossible (q<=2); n<=8: only (1,3) with (dA,dB) in {1,2}x{6,7}, residual <=1). MINIMAL-X THEORY: Hall-failure => no private neighbors => starved setups shared with exactly one non-starved each (dance s<D_j<u<D', coherent) + dual concentration characterization (H4 fan-in + L2 bounds); no contradiction derivable -- dance coherent, needs new dynamical invariant or full Hall. NEGATIVE RESULT: no canonical/local routing can close U4 (bubbles conserve; era-correlation at best leaves <=1-bubbles needing global room; rotation counting collapses to Z=Sz tautology). EVIDENCE: (1,3) engineered n=7,8 (12+18 legs) + BFS-closed 8/8 steady-state all lap2-full (WQ -37..-73); deep-starved 0/73 closed; non-starved 0/73 closed (22/22 extremal pre-states transient-only, never recur); dance 6/66 never tight; era-correlation D<=2dA(s)+2 53/53; strong-form 69/69; q/(2a_s)<=0.5; single-builder 50/51 key-near (interval-correlation next-lemma candidate via path-bracketing). Bubble-concentration unconstructible (mutual dethrone => per-key setups; L2 defends). 600+ match-full, 0 failures, Q_B>2A nowhere; S26 never triggered. U4 OPEN at per-terminal demand<=capacity under bounded sharing. Lean: U1 kernel stands; L1/L2/U2/U3/H paper-complete (block-model Lean gap deferred). DO conditional unchanged. Zero kills.

### PIVOT15-1 U4-Core: minimal-X forced, S1/half-pool vs cancellation wall, ONE missing lemma [AUTHOR + FINITE]
MINIMAL-X FORCED FORM (A): deficient X => |N|=|X|-1 + no privates => every starved setup shared with exactly one non-starved (dance s<D_j<u<D, one key) + tight locals + starved/empty creators; dual = extreme concentration (H4+L2 quantified). No contradiction (dance coherent). ERA E(s) defined (setup..starved..dethroner..sharer); eras overlap via builders (no laminar/disjoint rescue). BRACKETING (C): builder-near <=> key-interval-near (shared keys) => GROSS motion correlates; NET depths decouple (independent signs across separate splays); crossing intervals kill static bounds. HALF-POOL S1 (D: OPEN): q/(2a_s)<=0.5 (51 rows), era 53/53, strong 69/69, single-builder 50/51; proof BLOCKED by cancellation wall (adversarial A-cancel + B-accumulate coherent; closedness forbids nothing finite); refutation ATTEMPTED (greedy discrepancy-steer + cancellation construction): 0 violations -- and gradient-flat evidence (penalizing A-motion prevents B-deepening: joint motion forced). So S1 unproved+unrefuted, possibly false in principle. FAN-IN (E): bounded-sharing banked (H4+L2/H3/namer<=1+<=1), residual<=2 unclosed (needs S1). DANCE-CYCLE (G): monovariant dead (closed returns), peeling stuck at contested tights, no kill. S2 needs S1; S3=U4. SHAPE-HUNT: 133 cycles 133-full, 0 obstruction shapes. EXTREMAL: (1,3) 8/8 closed match; deep-starved 0/73; nonst 0/73; 22/22 pre-states transient. 700+ green, Q_B>2A nowhere, S26 never fired. ONE MISSING LEMMA (N): NO-TIGHT-DANCE (tight fully-shared dance-component unrealizable) => kills minimal-X => Hall => U4 => Q_B<=2A. Lean: U1 kernel stands; block-model + L1/L2 + NO-TIGHT-DANCE gap (~200 lines). DO conditional unchanged. Zero kills (S1 not refuted; U4/DO open).

### PIVOT16-1 NO-TIGHT-DANCE universal attempt: E0-equation, gross/net wall, OPEN [AUTHOR + FINITE]
FORMAL DANCE (A): tight = creator/setup-closed + fully-shared + no-privates + |N|=|X|-1 + saturated + realizable (tight-core =|X| variant tracked; off-by-one bridged, no gap). BRIDGE (B): minimal deficient => |N|=|X|-1 + no privates (sole-locally-paid exclusion proved as peeling rule) => contains tight dance core; killing dances => Hall => U4. CELL CHRONOLOGY (C): s(DELETE,d>0) -> quiet noops -> t(first-KEEP,(0,q),D frozen pre-s) -> u(first non-z,dA(w)>0-motion,a_u>=1) -> (u,t) non-z only (else arrival supersedes s) -> t(nonst,setup=s,D rebuilt); roots/divergence tracked exactly. TIGHT-PRESERVING (D): avoid A(extra eligible cap)/B(privates)/C(sharing loss), counting-exact. E0 (E): minimal 2-access dance => (q_t-2a_s)+(q-2a)=1 exactly (starved-deficit + nonst-residual = 1); fat creators add -SC2a_c (raise bar); general X: SE2a_e = R_T-1. ESCAPES (F-H): no universal forcing (fresh pools 2-hop/ineligible; private-freedom needs tightness; destruction helps room; real cycles exploit all three (WQ -40..-70)). DIVERGENCE (I): DELETE creates asymmetry free; unnamed DELETE-slack abundant-but-ineligible; exact accounting, non-constraining. BRACKETING (J): gross correlates (shared intervals), nets decouple (independent signs); crossing kills statics; conditioning on tightness fails (cancellation credits already counted or ineligible). SIGNATURE (K): NULL (all monovariants return or direction-free). COMPOSITION (L): OPEN (attractors shallow; BFS closes extremals with slack). M: OPEN (0 tight/700+; coherent everywhere; joint-lucky conjunction). N-U4/Q/SLACK/DOUBLE: OPEN conditional chain ready; unrefuted; S26/S38 never fired. Q (ONE lemma): E0-DANCE UNREALIZABILITY ((q_t-2a_s)+(q-2a)=1 + order + sharing + zero-fat-creators (+fat generalization)) -- weakest U4-completing; resists via joint coherence (no false conjunct; S1 unrefuted). Lean: block-model + E0 gap (~150 lines over green U1 kernel). Zero kills.

### PIVOT17-1 E0->U4->DOUBLE finishing attempt: gap decomposition + per-access room, E0/U4 OPEN [AUTHOR + FINITE]
E0 PREDICATE frozen code-accurate (complete naming: members name ALL pools; pools per-access 2a_e disjoint). BRIDGE + sole-naming-empty refinement (minimal members sole-name only empty pools; fat pools all shared; gap exactly 1). ZERO-FAT E0 (q_t-2a_s)+(q-2a)=1; FAT form -SC2a_c (minimal obstruction = zero-fat). RESIDUAL splits (1,0)/(0,1)/compensated; L3-extremality for positive nonst. PARITY: no contradiction (independent parities; E0-A dead). NORMAL FORMS (DELETE/quiet/starved/sharer/divergence-engine) all coherent, no contradiction. CREATOR inventory: starved builders = free labor (rotations w/o credits) + private ineligible setups; E0-C dead. SKELETON minimal a_s=1,q_t=2,a=1,q=3; contraction unproved; E0-D/E/F tautological-dead. GAP DECOMPOSITION (new lens): GAP=SHARING-EXCESS-SLACKS (EXCESS=S cap(fanin-1)>=0; SLACKS=S(room-|X_t|)>=S(room-q)>=0 via per-access room); deficiency <=> EXCESS>SLACKS. PER-ACCESS ROOM banked finite 150/150 (every access fits named pools) + shape-hunt 133/133 + prior 600+ all charge-full, 0 E0/dance witnesses, Q_B>2A nowhere, S26/S38/S44 never fired. E0/U4/OVERFLOW<=SLACK/DOUBLE: OPEN (composition ready). R: C.ZIG AUTHOR (V1-V3 mechanical OPEN, no Z_B file); B<=3A conditional; PIVOT-2 excision = mechanical obligation (not re-verified); translation parametric banked; LT/DO conditional. Lean: U1 kernel stands; block-model+E0 gap (~150-200 lines). Zero kills.

### PIVOT18-1 SHARING->SLACK injection attempted: correction + two blockers, OPEN [AUTHOR + FINITE]
DEFINITIONS frozen code-exact (complete naming; double-fanin; baseline/earliest; headroom room-|X_t|; GAP identity verified; sole-naming-empty; zero-fat). UNITS + enable (ORIGIN/arrival/co-located; ENABLE-K/D/REBIRTH structural). CORRECTION: complete naming over-counts per-pool injection (tight pools match w/o headroom); correct excess = RESIDUALS (post-locals starved-full + nonst (q-2a)+); canonical locals-first sufficient-needs-era+concentration. PER-CLASS: setup excess needs era-margin (unproved); creator excess needs fanin-vs-room (unproved H4+L3 joint). VERDICT OPEN. TWO BLOCKERS (both necessary): (i) era q_starved<=2a_setup (cancellation wall; 0 violations incl greedy); (ii) residual-concentration bound (extremal leftovers vs fat pools; coherent marginal corner; 0/900+). Per-access room finite 150/150; long-splice n6/7 (93/86) full, 0 room-viol. E0/U4/Double OPEN (ready, unrefuted; S26/38/44 never fired). ONE missing: E0-dance unrealizability = (i)+(ii) jointly. Lean U1 green; block+E0 gap. DO conditional. Zero kills.

### PIVOT18R-1 Residual repair: joint tradeoff analyzed, JOINT MARGINAL EXCLUSION missing [AUTHOR + FINITE]
CORRECTED accounting (residuals post-locals-first (WLOG-sufficient, Kuhn-reassignable); headroom physical-once; GAP_res=R-H=Q-2A identity; minimal obstruction R=H+1). DISENTANGLE IMPOSSIBLE: d_s+r=1 forces luck wherever equation demands (fat-nonst=>massive starved-deficit-luck; extremal-nonst=>mild starved (era-boundary)); conditional era/concentration add nothing (absence/order, no fresh headroom). JOINT MARGINALITY: every projection marginal (depths-boundary, A-net cancellation, order-exact, sharing-exact); squeezing one inflates others (luck conserved). FALSIFICATION (all fail=support): greedy-flat (joint motion forced), cancellation-collapse (deep transient 22/22), bubble mutual-dethrone (L2 defends), extremal loops (no recur), long-splice 93/86 full, room 150 full, shape 133 zero, 900+ green, Q_B>2A nowhere. TAIL QUANTIFIED: violation ~5sigma A/B decoupling (~1e-6/long-cycle; needs 1e6 cycles, infeasible) => explains 0/900 + coherence. R<=H OPEN; E0/U4/Double OPEN (ready, unrefuted). ONE missing: JOINT MARGINAL EXCLUSION (E0-marginals jointly unrealizable). Lean U1 green; residual/block gap. DO conditional. Zero kills.

### PIVOT18R-2 Forced-pool lemma + wall-map exhaustive, E0/U4 OPEN [AUTHOR + FINITE]
FORCED-POOL (proved): zero-fat E0-overfull => genuine Hall failure (starved forced (no locals; creators empty); nonst residuals forced (locals full; creators empty); setup overfull => pigeonhole, no reorder escape). Hence U4 => no zero-fat E0-overfull (necessary). WALL MAP (10 formulations, same core): access/cell/pool/demand/residual/canonical/augmenting/builder-tree/dual/fat-lift/peeling all need sharing-multiplicity vs headroom with independent A/B quantities; E0 integers always work ((0,2)+(1,3)+a_s=1); every conjunct OBSERVED ((0,2)x4, (1,3)x8-closed, a_s=1, single-builder 50/51, sharing 6/66); only JOINT exact co-occurrence unobserved (0/900+) yet coherent (temporal root-moving). No proof (joint coherence), no refutation (marginals satisfiable). E0/U4/Double OPEN (ready, unrefuted). ONE missing: E0-dance unrealizability (joint). DO conditional. Lean U1 green. Zero kills PIVOT-13..18R.

### PIVOT19-1 E0->E0_CORE mutation: n<=6 CLOSED (era-route) + sign-locking, E0/U4 OPEN [AUTHOR + FINITE]
MUTATIONS: locals/setup-macro/genealogy/zero-fat/symmetries/neutral/graph-kernel/macro-scalar/restricted/canonical/cell/builder-tree/per-access-room/complete-naming/sole-empty/gap/forced/E0-equation/joint-beam -- all preserve-or-expose the same joint-marginal core (each load-bearing part verified: sharing->trivial-Hall; tightness->satisfied; marginal-depths->room; order->causality; zero-fat minimal). E0_CORE = zero-fat dance + n>=7 + sign-locked/transient + T0/builder + exact tight/order + GAP=1. n<=6 CLOSED (new proof, era-route: q<=2 (cap) <= 2a_s>=2 (floor arrival) => starved fit private setups (L2); nonst q<=2<=2a locals cover; full matching => Q<=2A; independent of PIVOT-12 analytic). FRONTIER SHARP n>=7. SIGN-LOCKING (0/15000+, p<1e-9): sustained runs move same-sign-or-still, never counter/split (n=6,7,8 + priors; fresh roots unlock mixing transiently (6%)); discrepancy <=> fresh-transient + T0-marginal (never sustained-builder-built); dethrones fat-or-transient. Mechanism unknown (mean-reversion suspected). E0/U4/Double OPEN (ready, unrefuted; S26/38/44 never fired; joint beam F=0 (pools cover)). ONE irreducible: joint-marginal tight dance +1 (tight-satisfied dances force retention; +1-over unobserved (margins 2-6x systematic)). Lean U1 green; block+E0 gap. DO conditional. Zero kills PIVOT-13..19.

### PIVOT20-1 FRESH-TRANSIENT compensation: sign-locking frozen, path-hit-locking, OPEN [AUTHOR + FINITE]
SIGN frozen (sigma=(sgn dB,sgn dA) per builder (wp6_signed.py); FRESH = arrival + sign-change OR T0-first-touch (mod-m, cut-independent); T0-marginal = builder-less/eternal ancestry + closure-restoration (restorers unnamed (ineligible) => global-only). E0 needs freshness (sustained-sign-locked builders cannot discrepancy (would need counter-motion, 0/15000+)); T0-path coherent-marginal. CLASSES: F-D (pool saturated, no headroom); F-K (room iff fat (unproved)); F-T0 (unnamed (ineligible)). COMPENSATION OPEN (per-fresh saturated/terminal/ineligible; aggregate telescopes NET zero closed; alternating = Kuhn = Hall circular; loops = sharing-cycles consistent; one-fresh needs T0-marginal (coherent unobserved)). PATH-HIT-LOCKING (new attempt): paths hit-or-miss together (never split, 0/15000+) via co-evolved hot/cold shapes; mechanism heuristic (frequency), unproved wall (needs splay-geometric path-correlation). E0/U4/Double OPEN (ready, unrefuted 900+; S26/38/44 never fired). ONE atomic: SUSTAINED SIGN-LOCK THEOREM (same-sign-or-still, deterministic). Lean gap: sign model + lock (~120 lines over U1 kernel). DO conditional (C.ZIG-V1V3 + PIVOT-2-excision). Zero kills PIVOT-13..20.

### PIVOT21-1 GLOBAL PATH-HIT bypass attempt: rotation-exact, inventory-exact, wall stands [AUTHOR + FINITE]
ROTATION-LOCAL (A): single-rot risers/fallers exact; r=d EXACT (rot-counting = depth-counting, no leverage). SIGN-LOCK (C): 0/15000+ sustained same-sign-or-still (fresh unlocks transiently); perturbation-seek 0 opposite (stable-absence); mechanism unproved (hot/cold heuristic). QUANT (D): magnitudes independent (hub corners); no universal c. INVENTORY (E): pairs created=consumed=Q exact (closed); creation-vs-A needs depth bounds (wall). GENESIS (F/G): periodic elimination works; eternal-consumed impossible/none; wall relocates to fan-in. BLOCK/BOUNDARY (H/I): telescoping correct; regime inequality needs depth control (same wall); no finite K either. DIRECT (J/K): Q=(D_B-Z_B)/2, 2A=D_A+O_A exact; need D_B<=2D_A+slack; starved-vs-DELETE same wall (31 formulations). Unrefuted 900+. L: DO conditional (C.ZIG-V1V3 + PIVOT-2-excision mechanical). Lean U1/descent green; path-hit/block gap. Zero kills PIVOT-13..21.

### PIVOT22-1 EXACT BINARY DECISION: n<=9 YES-certified, n>=10 wall (honest OPEN) [FINITE exact + AUTHOR]
DOSSIER: cleanroom replay (5/3 exact A6Q4Z6; self-loop 0); defs frozen (a=ceil(dA/2), q=floor(dB/2), W=Q-2A; counts assert-verified). n<=6 analytic+BF (banked). HOWARD n=7 max-mean mu*=0/1 (2 iters, exact cross-mult). BF FEASIBLE: n=7 (3 passes, 184K states), n=8 (4 passes, 2M), n=9 (7 passes, 23.6M). VERIFIERS GREEN independently (fresh trans): n=7 2576574/2576574, n=8 32718400/32718400, n=9 425502792/425502792 edge inequalities, 0 violations. Max-mean EXACTLY 0 (self-loops attain). YES n<=9 CERTIFIED (dual potentials bf7/8/9.pkl, machine-checkable telescoping). n>=10: BF infeasible (n=10: 282M states, 5G edges/pass ~2hr (time, not just memory)); obstruction circular (support<=>N_*<=>m<=>states, no base; R1 symbolic chains; excision n-dependent only; W>=1 lands E0-wall); NO-hunt negative (W_Q hillclimb best -2; constructions preserve nonpositivity (splice sums, attractors, marginal closers); typical 2x margins uphill-futile). 31 formulations converge on discrepancy-independence wall (per-access depths independent; gross/typical ratio O(1)~1/2; tails coherent ~5sigma needs 1e6 cycles; 0/900+; unproved nonzero prob). VERDICT: n<=9 YES PROVED; n>=10 OPEN (not YES (universal unproved) not NO (no witness)); S32 binary unsatisfied, S33 honored (no guessing). ONE missing: E0/joint-marginal unrealizability n>=10. DO conditional. Zero kills.

### PIVOT23-1 DUAL UNIVERSAL: twin-max falsified (80560), obstruction banked [FINITE falsification + AUTHOR]
CERTS: bf7/8/9 (3/4/7 passes; potentials {0..-3}/{0..-4}; 79% zeros; max-prefix-W meaning (canonical maximal feasible)). TIGHT: 12.68% edges; 94% nodes 1-2 tight successors; battery (DELETE recharge +2, overflow drain -1, self-loop hold; capacity 3-4). DERIVATIVES kill locality: D(e) 2-7 values per (mode,dA,dB); root-pair NOT determining (all 49 multi (prior 0/49 was scoping bug, caught by histogram)); differ {0,-1} only; left-subpair 99.2% (151 failures need right-B vine/branch = history). CANDIDATE Phi=-twin-max(0,(maxD_B-2)//2): REFUTED 80560/2576574 (K-under 96%: (0,1)x18370,(0,2)x25750,(0,3)x2108,(1,2)x21320,(1,3)x9716; K-over 4%; DELETE zero (twin+B-frozen holds)). MINIMAL VIOLATOR: K1, Aroot1, Broot5, maxB4, dA0 dB3 (0,1,w+1); post twin maxB3; twin +1 canceled by max-recharge -1 (4->3 destroyed); net 0<+1. MECHANISM: max-preserved gives twin-only +1 (covers q=1); max-touched recharges (cancels) or small-drops (vine-consecutive covers q<=2 tight; q>=3 needs setup-era (wall)); no max-form covers all (preserved-vs-destroyed contradiction). KEEP/DELETE: DELETE holds; KEEP fails as above. n8/9 validation skipped (refuted n7). COARSE-DOUBLE OPEN (n<=9 BF-certified; universal dual open). ONE obstruction: max-term recharge-vs-drop dilemma. Lean U1/descent green; dual gap. DO conditional. Zero kills (candidate refuted, theorems untouched).

### PIVOT24-1 FSM COMPRESSION: left-99.2% + interface bits insufficient (281 multi), OPEN [AUTHOR + FINITE]
ADDTIVITY REFUTED (residual -3..+2 given (r,pL,pR); subproblem values insufficient (need shapes)). OFFSETS: ancestor counts unbounded (parity finite useless alone). MAX-DEPTH INVERSE (deep-max<->shallow-Phi (recent-splash vs accumulated)): state-local maxD insufficient (same maxD, different Phi via history). PROJECTIONS insufficient (B 401/429, A 429/429 multi). INTERFACE BITS (right-B vine/branch/orient + left-pair): 19759 groups, 281 multi (WORSE than left-only 151 (finer partition, still multi)) => finite bits insufficient; sufficient needs depths (unbounded, wall) or full shapes (vacuous). CANDIDATES: twin-max REFUTED 80560 (max-recharge cancels twin-payment; max-preserved caps +1); twin-exceedcount REFUTED worse (147128). n8/9 validation skipped (dead n7). COARSE-DOUBLE OPEN (n<=9 BF-certified; universal dual open). ONE obstruction: max-term dilemma + interface unboundedness (finite bits insufficient; depths unbounded; shapes vacuous). Lean U1/descent green; dual gap. DO conditional. Zero kills (candidates refuted; theorems untouched).

### PIVOT25-1 CEGAR abstract-dual: twin/root-pair infeasible, lift dies in detours [AUTHOR + FINITE]
SIGN FIX (methodology win): prover BF used costs=w (found slack cycles); corrected to c=-w (positive-W detection). L0 twin-bit abstract (2 nodes): INFEASIBLE, positive cycle [T,D] (T->D maxw -2 (DELETE diag), D->T maxw +3 (starved-deep (0,3?) (28,0)->K7? (0,428)->K1)). L1 root-pair (49 nodes, 637 edges): INFEASIBLE, cycle [(7,7),(1,1)] witnesses e1=(28,0)K7 (eps+1,(1,3)) e2=(297,428)K1 (eps+1,(1,3)). LIFT CHECK: e1end=(339,345)!=e2start(297,428); e2end=(90,83)!=e1start(28,0) (different root-pairs (2,1)/(1,7) vs needed -- incompatible, refine forced). BFS detours: d1 len8 W=-16, d2 len8 W=-18; total +1+1-16-18=-32 (repayment 17x abstract gain; closures dominate (mean-reverting bounded excursions)). So abstract-positive dies in lifting (detour repayment). No direct NO witness. REFINEMENT would need depths/shapes (unbounded/vacuous wall). E0/U4/Double OPEN (n<=9 BF-certified; universal open). ONE missing (unchanged kind). Lean U1/descent green. DO conditional. Zero kills.

### PIVOT25R-2 CONSTRAINT-GUIDED DUAL LOOP EXECUTED: L2 GREEN n=7, wall n=8/9 [AUTHOR + FINITE]
L1 DECODE (canonical replay): e1 (28,0)K7 + e2 (297,428)K1, both (1,3) w+1 twin-kept, pres both-vine md6/6, B-posts non-vine; stitches incompatible, smallest separator isVine(B) (l2_decode.json). L2 alpha=(rootA,rootB,vineB), Phi=-2twin+P (FREE), ALL 2.58M edges as max-c: n=7 FEASIBLE (63/98 classes, 875 abs edges, 3 passes), INDEPENDENT VERIFIER GREEN 2576574/2576574 (l2_refine7.json). Verifier caught+fixed pot sign bug (P=dist not -dist; feasibility booleans unaffected). P_7 COMPACT: P=-[B non-vine] only (all 63 classes) => Phi=-2twin-[nonvineB], total/n-independent. DELETE universally PROVED (AUTHOR: B frozen; a=0 fixes twin; a>=1 pays). KEEP reduces to 2DT+DNV>=q-2a. TRANSFER n=8 (all 32.7M): RED 72252, all KEEP q=3 twin-kept-or-+1 B-nonvine-kept (l2_transfer8.json). L2-8 FREE-P INFEASIBLE (cycle (2,2,0)-(7,7,0)-(8,8,0) +3, decoded witnesses a=1q=3; stitch0 separated by vineA) (l2_refine8.json). L3 (+vineA) INFEASIBLE (same roots +3 in all-False classes; split untouched) (l3_refine8.json). L4 (B-maxdepth bit) identified, withheld (bit-chase demonstrated; bounded-payment wall decisive). PROBE n=9 q>=4 (1.24M pair-edges, ordering replays 200/200): RED 126836 in 2 classes, short exactly 1 despite twin-max+vine-destruction (l2_probe9.json). WALL (quantitative): (a=0,q=4) needs drop 4 > twin+vine ceiling 3; each max-q +1 needs another bit (~1/2 sizes); unbounded q needs depth-proportional payment = E0/setup-era wall. COARSE-DOUBLE OPEN (n<=9 BF-certified; universal open). No Q_B>2A witness. Lean: none new (finite tables aren't theorems; DELETE needs model alignment). DO conditional. Zero kills.

### PIVOT25R-26 ROOT-SELECTED: GATE I PROVED (kappa=4), GATE II FINITE-GREEN [AUTHOR + EXACT + UNIVERSAL-PROOF]
D formulas verified; D0 reduction exact; da=0 = x=y=A-root (pointed-B, G1-only). Cone one-dimensional, stable n=5/n=6. Absorbed-mass gauge (g*=outside-subtree indicator, monotone via set-growth absorption). UNIVERSAL LEMMA proved by fold induction (aL/aR<=0, f<=2, c<=q): R<=2*abs+(1-b) => kappa_*=4; DA0-ROW regression 0/19K violations. Identity D_KEEP=D0+D_DEL 0/8820; D_DEL<=0 always (proved). Absorbed-H row-switch REFUTED (3338 fails, all kappa>=0; reachable). JOINT fiber cone FEASIBLE+strict (58K/893K): SCALE, architecture intact. Universal row-switch + residual + Coarse-Double OPEN (conditional chain recorded). Mechanization open. Zero kills.

### PIVOT25R-25 GAUGE RIGIDITY: finite R1 proved, da=0 fiber R2-direction [AUTHOR + EXACT]
Gauge reduction symbolic (verified 0/300); NONE=ancestor slot (lambda always 0); hub-1 universal (0/256); padding lifts all finite edges; twin never destroyed under KEEP (proved), DELETE destruction (356) kills twin harvest. Isolation REFUTED (17/102; swap adds 0). Finite LP-max=0 n=5/6 coarse+refined (19K/235K rows) + positive circulation: B-only gauges all drop-free. Fiber: da=0 harvests robustly (twin-blind, atomwise-valid, +6.3 over CB; 130904 n=6); da=1,2 twin artifacts; da=3 rigid; da=0 = x=y=A-root family. da=0 fiber = R2 program (universal verification open). VERDICT R4 (missing: universal da=0-fiber admissibility + compaction). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-24 ATOMIC INTEGRATOR: weight = tautology, COHOMOLOGY [AUTHOR + EXACT]
r_static frozen (C_B row target, 0 mism). Atoms (y,z), tau=(slot,lambda), ell exact, full-claim transport 0 amb; merges/splits resolved per-z. Root token bounded (twin 99.5%). Bellman h solved (16 nodes, 0 residual, cover 100%) BUT h=2-lambda exactly = §9 FORBIDDEN TAUTOLOGY (slot-independent; H_y=const-R_B). No non-tautological margin forced. §17: no coverage witness (vacuity, not coverage); no bundle forced. COHOMOLOGY (admissible sense). Recharge decoded (weight gain 2->3 funded by slack, tautological). Universal h_k + aggregation OPEN. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-23 A-STATIC CARRIER: STATIC-A, latent B transport proved [AUTHOR + EXACT]
A-static 5214/31234 (16.7%), C 1..8, C_A=0 verified, identity 0 mismatches. Witness (18,12,5,1) decoded (NOT A-static: y moves; smallest true A-static (0,19,1,4) twin-driven). T1 1974/T2 644/T3 3876/T4 3014; merges 1402/splits 1804. Fresh 3876/3876 latently sourced (100%). G1-G4 exhaustive (G5 0). Full-claim Delta prediction 0 amb (1008 classes); coarse (slot,G) 17/21 amb (fringe detail required). Twin 0->1 99.5% (bounded +2 charge, spikes need B). M_static naive sum covers 43.7% (multiplicity open). Negative-edge static recharge EXISTS (6972 cases, e.g. D=-5 V:0->3). No §17 killer. STATIC-A. Next: weighted M_static + moving-A coupling. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-22 SINGLE-CROSSING REFUTED: B-creation on A-static keys [AUTHOR + EXACT]
Cut system nested verified; Gamma/sign-split per cut. |CAND|: d0 4798 (vacuous) + delta-empty 6246 (A/twin channels) + norel 1398 (colocated) + nocon 110 + mixed 1332; in-scope failures 1442 (contact fix rescued 1510). SMALLEST (18,12,5,1): d=1, single support key 3 STATIC in A (depth/parent unchanged), B-coeff -2->-1, twin +2, A-cost -2, net +1; cut e_1 rel/act/nonvac pass, contact fails. Supporting (9,0,5,1). R1-R4/I_common/L_i moot (verdict forced). Richer carrier forced (cut + static B-coeff claims), unlaunched per §17. Twin bounded +-2 in 96%, insufficient alone. D=-2 V:1->3 (14,17,3)->904: M must allow +2 rises. No M; no telescope; DO preserved. COARSE-DOUBLE OPEN. Zero kills.

### PIVOT25R-21 A-CARRIER ISOLATION
: H8 dead, H7-necessary, H* = path-neighborhood [AUTHOR + EXACT]
31K gateway events (5.6K genuine Dpost>0). H1 necessary; H2/H3 moot (path-determined, 0 variation); H4/H5/H6 unresolved; H7 necessary-sometimes (268 groups; mirror pair C=5v3 via per-key depths, tracked dA 1->2v2->3, twin same, CB same); H8 ELIMINATED (empty); H9 residual. Support-pre-placement 341 amb (needs post info). Minimal family = full path-neighborhood + y + support + twin/roots + full B. No compressed transport law; component rules exact. No M. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-20 GATEWAY KERNEL: V=V2 at n=5 only, exposure needs post-coeffs [AUTHOR + EXACT]
V=V2 holds 82/82 gateways n=5; fails 1430/4392 n=6 (smallest u=18, needs horizon 2; V rises 1->3 along tight D=-2 edge). Identity C=CB+CA+Ctwin exact 671,364/671,364 (twin creation dominates). Collision pair decoded (Lambda rows differ, R values agree; post rows both discharge; demand in migrating fringe mass). Exposure+masses: 238 classes/43 amb (was 21/21); residual = fresh post-coefficients. 328-chain: 296 (+twin), 250 (+Broot), 237 (+argmax), 114 (+full rows), 0 vacuous (+A-depths). No compact Z; no M; C* refuted n=6. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-19 BELLMAN CLOSURE: profile fails n=6, Lambda-rows are the datum [AUTHOR + EXACT]
Tight DAGs + D=0 self-loops only (458K/1764D n5; 4120K/17424D n6); no nontrivial SCCs. P->V: 0 amb n=5 (960), 328 amb n=6 (8895); +twin 296, +Broot 250. Smallest same-twin pair: same A/D/twin, V 1v2, Lambda rows differ while R VALUES agree everywhere (key1 c=0/n4 v c=1/n2) => FIRST DATUM: (c,lambda-support), not values. Horizons h5=2/h6=5 (V_k==V exact); gateway 82/4392; C-vectors 3 patterns (all value from C_2). (P,x)->P' amb 1254; value-det amb 210; smallest decoded. Outcome: B at n=5, C at n=6. No M. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-18 CANONICAL INTEGRATOR: V exact, propagation up, no M [AUTHOR + EXACT]
Full graphs (KEEP+DELETE) n=5 (1764/17K) + n=6 (17K/209K): max-mean 0/1 both; V exact (0 sigma/fixed-point violations; ranges {0..3}/{0..5}). Tight graphs ACYCLIC (all-singleton SCCs); every state has tight successor. Trajectories: n5 all length-1; n6 up to 4; (9,83,1) decoded (V=3=1+2 via tight K6 to V=0). S0-S3 zero ambiguity n=5. Propagation 99.5% deterministic, STRICTLY UP to Bpost-ancestors (896/896), Lambda overlap 91%. Units: max-deficit 95% but 86 Bellman fails; gateway states 93% non-twin + 100% non-vine-B. Zero-D edges: V ignores B-root motion + twin flips. NO M (paired-fringe next, untested). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-17 COMPILATION: R_T/D exact, all aggregations dead, no cycle bar [AUTHOR + EXACT]
R_T static fold 0/300; D_s profile + KEEP-equivalence. Census: K_+/sum/max, majorization, K_1, K_abs ALL REFUTED (n5/n6; smallest (9,83,1): mass moved+amplified 1->2; k1 worst reshuffles on d=0). Transfer law: move+amplify, no conservation. A-budget rewritten (d + parity); pairing open (paired-fringe proposed untested). Max-mean-D=0 (no cycle obstruction; edge-creation is the harder wall). No M; DELETE/KEEP/telescope open; DO chain preserved unchecked. COARSE-DOUBLE OPEN. Zero kills.

### PIVOT25R-16 MACHINE SOLVED: R-fold exact, twin+Db wall algebraized [AUTHOR + EXACT]
R_entry backward fold VERIFIED (L4c -4, PR904/V19 -8, R10-29 +8, zig +7/+14: all match). Absorption S'=S+2+U+V universal. T_LL/RR/LR/RL derived (f shifts +2/step; (aL,aR) decrement; reachable infinite-structured). Zig-outer = genuine demand (top fringe descends, unlifted). EXACT identity: surplus = 2a+2(1-t_pre)-R_entry; DELETE proved universally; KEEP iff R<=2a+2(1-t_pre). NO K emerges (fringe demand real). M: recharge-free fringe-mass payment terms for shortfall max(0,R-2a-2(1-t_pre)). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-15 RECOVERY-MACHINE PROVED, ZIG-UNBOUNDED, OPEN [AUTHOR + EXACT-SYMBOLIC]
X* machine proved: rigid blocks, G LL/RR/LR/RL (RL mirror-bug fixed), fringe shift by side-persistence (keys unneeded), twin timing (never destroyed B-phase; created at root-arrival/zig), supply F + zig formula. Regression 346/346 + 41/41 held-out. Residual: absorption monotone (x-subtree grows; fringe depletes; late fringe (m<=2) never amortizes). ZIG-OUTER FAMILY verified (r=5 @n9, 12 @n16, =n-4 unbounded; w=0 edges, NOT CD killers): NO uniform bound; r<=2a FALSE; §16 blocked (needs non-twinDb terms). Classification: zig-outer (unbounded) vs double-shortfall (late-fringe bounded). Mixed-run induction + compact rule + universal proofs OPEN. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-14 HIGH-NEED RECURRENCE: deterministic mass-flow found+held-out [AUTHOR + EXACT]
55 high-need (needs 3..15): traces clear/overshoot (-26), 6 rise-then-recover. X-ladder on 50K doubles: X3/V1/V2 ambiguous (1061/1515/1853), X4 fringe ZERO ambiguity (3247 multi states). Recurrence VERIFIED: (L,R) maps per orientation 61/61 + 41/41 held-out (RL mirror-bug caught+fixed by held-out); fringe via side-persistence; twin via remdepth; supply formula+twin. A: NO (3->6 minimal); B: NO; C/D: no single scalar/invariant; E: recharge-then-recovery. WORLD B (bounded residual, access-local, no echo). Adversarial (alternating/delayed/unbalanced/mirrors/fresh) all predicted. COMPRESSED: X*+G+F stated, relation observed-unproved. NEXT: arbitrary-subtree update proofs. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-13 RECOVERY CHARACTERIZED: second-double + zig rules, held-out [AUTHOR + EXHAUSTIVE]
Hard-first necessary 100% (unpaid), 95-97.5% (borrower); first-easy never borrows (0 cases, both sizes). Recovery: second double remaining => paid 100% (56+428); single remainder <=> zigpay>=need with zigpay=f(first config,twin,top-outer) exact (108+256 groups, 0 ambiguity, 1932 events). need=w-first_pay pre-state computable; need<=0 auto-pays modulo later-loss 5%; need>=3 zig-only ~89% unpaid. Boundary: n<=6/needs<=2; need>=3-with-remainder unobserved (gap). Mechanism: absorption + twin timing from depths. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-12 DISCOVERY EXPERIMENT: first-hardness necessary, recovery open [AUTHOR + EXHAUSTIVE]
Exhaustive n=5 (8,820) + n=6 sample (6,000): unpaid 5.9%/6.9% under twin+Db. FIRST-HARD NECESSARY: borrower=>first-hard 95-97.5%, first-easy=>never borrower (0 cases), UNPAID=>first-hard 100% both sizes. Recovery 77% (later overpayment); unpaid lives in q=1 zigzig-hard-first (+rare n=6 outliers). Residual: zig-state 5%. Cross-access: 0 persistence (access-local). L4c overpays -6 (local-only hardship); L4d genuinely unpaid +1. Hypotheses H1-H5 (first-hardness, recovery, prefix-debt, twin-timing, outer-evolution); held-out confirms necessary direction. Missing: pre-state recovery predictor. Next: remainder-class characterization. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-11 REALITY-DISCOVERY: pay factored, naked arrival, lineage [AUTHOR + FINITE + EXACT]
650 doubles (178 hard) with full transport records. pay=twinDrop+DbDrop EXACTLY; DbDrop=size-formula 650/650 (shape-independent by rigid motion, rigorous); twinDrop in {0,+2} by roots. D0-D4 collisions resolve to twin alone (5 classes); D3 zero ambiguity. NAKED ARRIVAL: hard inner-mean 0.40 (118/178 zero) vs easy 2.60; outer 2.17 vs 0.74. Absorption inverts debt within accesses (L4c xL 0->3->5; pays -1,+3,+7). Lineage: debt persists+migrates+splits; cover flickers (placement volatile); pivots net zero in doubles. Refinement collapses to singletons (negative). Missing: size-evolution meter (access level); double level CLOSED. Next: sequence-aware absorption profile (unbuilt). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-10 B-DOUBLE PAYMENT: 4 scalars dead, tables exact, no live D [AUTHOR + FINITE + EXACT]
rho REFUTED 824 @n6 (x-local vs geodesic; unique good move at root far from x; exchange false). D2 REFUTED 1318 (Lipschitz proved; trade -3/+3); root-bonus impossible all-K + inherits twin-kept fails. E1 REFUTED n=2 single A-zig (rise 4>2; twin-destroy). E_del REFUTED 11/20 (restructuring raises cost). Symbolic tables EXACT 346/346 (LL/RR/LR/RL/Z formulas; recharge=outer-descent; LL fails 51/85). Per-double: twin never destroyed in B-phase; 54 twin-kept doubles need joint. Fuel: none alive (properties precise); disjunctive C4|C5 lead untested. Conditional (A)(B)(Z)=>Q<=2A proved, premises open. Charging gated (no meta-proof + E0/Hall ban). Missing: twin-kept Db-stagnant double (L4c ledger). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-9 EXACTIFICATION: frozen exact, verdict RESOURCE-UNRESOLVED [AUTHOR + EXACT-SCOPED]
41,036/41,036 replay-verified exact (7,693 cosmetic zero-cell diffs resolved, 0 real; 41,024 distinct, all primitive). Gauge PROVED (M*1=0; uniform-shift invariance; one-fix justified). Pairwise exact: 0 prop-dupes, 0 negations (no free equalities). Diverse-vertex/persistent/RREF/basis/exact-LP BLOCKED (degenerate LP >=20 min/solve; exact methods missing at 41Kx2.1K). t*~=0 re-confirmed; margin-infeasibility carries by superset. Self-caught probe bug discarded (no artifact impact). Verdict: RESOURCE-UNRESOLVED (§11-D third option) -- NOT infeasible, NOT compute-timeout-on-solver, but missing exact-rational-LP capability. No new cuts (correct per §8). n=8 untouched. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-8 CUTTING-PLANE VERDICT: float-feasible n=7, exact unresolved (method) [AUTHOR + FINITE + EXACT-SCOPED]
21 iters / 41,036 genuine rows; LP feasible throughout (no Farkas trigger). Float loop CONVERGED iter11 (0 viol tol1e-4). Exact: 101K->oscillating 1K-32K (vertex whack-a-mole); deficit split 1.5K grazes vs 27K real; big-batch no collapse. Root cause: t*~=0 marginal (margin-delta infeasible); 3880/13588 active rows break under /1024 rounding; exact rational LP unavailable. Verdict: template VIABLE at float precision on complete n=7; exact GREEN/RED UNRESOLVED (method limit, neither template failure nor compute). n=8 deferred (blocked + 32.7M exact-scan scale). Rotation identities banked scoped. DELETE finite OK/universal open. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-7 GROWTH ROUND: 133 edges feasible, R1 refuted, updates derived [AUTHOR + FINITE + EXACT]
n=11 replayed (a=0q=5w=5, cap 40/9<5); range law U-L>=1/2, M>=1/4 verified necessary (ternary provably non-universal). Growth 66 rows (B-deep to n=64 b=29, twin-to-twin, 15 DELETEs, 40 omega-controls; E skipped visibly as included). Re-solve: FEASIBLE exact 0/133, minmax 29/128, values ±5/22+0 (range hugs n=64 bound 29/64; optimality uncertified). R1 majority-list (44 cases, total): REFUTED 27/133 (candidate failure). Rotation identities engine-checked (outside 115 clean; non-pivot sets identical 387; inside deltas ±2, +down measured). DELETE: old theorem non-transferring; 28 finite rows OK; universal OPEN. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-6 UNIFORM JOINT-CONTEXT ROUND: depth-template dead, eta-template alive [AUTHOR + FINITE + EXACT]
Attachment verified TWICE (standalone PASS + canonical 42/42 replay, no mismatch): -2twin+sum f(dA,dB) REFUTED, surplus 10971177 (scoped: this template only). eta=(dA,dB,nA,nB,omega) (417 contexts; interval property asserted): old multipliers give 415 nonzero => NOT refuted (not feasibility). Free-g LP on 67 hard edges x 580 vars: FEASIBLE exact 0/67 with all g in {-1/9,0,1/9} (minmax optimum 1/9; first wild-magnitude assignment was solver artifact, superseded). Template ALIVE (sparse only, NOT universal). No refinement (no obstruction yet); no evaluator (rule extraction next); updates unexecuted. DELETE AUTHOR; KEEP/TELESCOPE open. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-5 POSITIONAL ROUND EXECUTED: additive excluded, POS/POSA infeasible [AUTHOR + FINITE]
§3 PROVED (mechanics + analytic): no -2t+F(A)+G(B) on all-pairs n>=64 (0-step A no-op illustrated a=0q=3w=3; C4 in excluded family). alpha_pos=(L4,dA(n),dB(n),LCA_A(2,n)) (order ranks; lca root-first bug caught+fixed); splitting table: L4 S1/S3 separated all-3-coords (LCA 8v7,8v2 confirmed), S0/S2 stay. POS-7 FEASIBLE (1064 classes); POS-8 INFEASIBLE 5-cycle +1 (2448 classes,82851 abs edges; B-vine class + slack edge). POSA (+mdA>=4, first A-bit): INFEASIBLE 6-cycle +1 (3168 classes,127190 edges; same 2 archetypes re-routed; 0/6 merges agree). Five infeasible refinements, stable pattern. No live candidate (C4 term-only). Micro-reward accounting proved per-access (replay asserts); J blocked on live Phi. Battery 21 stands; n=32 uncovered. DELETE AUTHOR; KEEP/TELESCOPE open. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-4 REPAIR ROUND: exclusion proved, L4 diagnosed, C4 refuted-as-complete [AUTHOR + FINITE]
CORRECTIONS: C4 REFUTED as complete potential (w=0/drop=-1 L4d replayed; term-only henceforth); L2-4 refute tested summaries only (recursion unexhausted); no annotation-without-live-Phi; BF-mismatch never a rejection cert. §2 PROVED (all steps + non-vine-A illustration a=1q=3w=1): no F(rootA,vineA,T_B) on all-pairs n>=64 (fresh-A scope); L2/L3/L4 families + unbounded tables over them universally void; B-only additions cannot repair (L5-spine void; withheld). L4 FULL-TREE decode: binding +1s differ ONLY in B-depth(8) 6v2 (A-cost equal); no stitch has coinciding A-paths; S3 A-trees agree on all 9 coarse stats (positional/keyed gap only). PANEL: no coarse A-bit separates binding stitches (prof differs only S0/S1). LOOP DIAGNOSED-STOPPED (L2->L3->L4 executed; keyed fuel-placement needed; lookup != compression). BATTERY 21: C1 14/C3 16/C4 3/C5 7 FAIL; C4 passes S2nv/ACTL/PR904(+14); C4 fails EXACTLY D_B-rise (+4/+1/+1). Repair spec open: zig-monotone B-payment. DELETE AUTHOR; KEEP/TELESCOPE open. n=32 uncovered. COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-3 PAIR-SENSITIVE CONTINUATION: §4 impossibility proved, L4 infeasible, C4 active [AUTHOR + FINITE]
§4 VERIFIED (7/7 steps + n=7 illustration a=1q=3w=1 twin->twin): no Phi=F(root_A,T_B) on all-pairs n>=64 (fresh-A-per-step scope; not a CD witness). Consequence: L2-family impossible analytically (any tables); A-shape necessary; L3+ escapes scope. STITCHES: L3-S always B-depth-6 fuel vs discharged E; L4-S1/S3 agree on ALL coarse features (roots/vines/maxdepths) — E vs S differ only in deep-chain placement (right-spine 6 vs 2); L5 (spine bit) identified, withheld (witness-chase). L4 (+mdB>=6, stitch-justified): n=8 140/512 classes 2796 abs edges INFEASIBLE, 4-cycle +2 (l4_refine8.json; l4_stitch.json). BATTERY (18 hard edges, canonical replays): C1 D_B-2D_A 14 FAIL, C3 -D_A 14 FAIL, C4 +D_B 3 FAIL (active; all D_B-rise: zig/max-recharge), C5 -Agree 5 FAIL; size-weighting killed analytically (Sum|sub|=D+n). §4 A-variants (same rootA+B, w=1 vs -3) illustrate A-necessity. MICRO-ANNOTATION blocked on live candidate (zig raises D_B +1 measured; no depth-sum J). DELETE proved AUTHOR; KEEP open. n=32 excursion uncovered (no replayable word). COARSE-DOUBLE OPEN. DO conditional. Zero kills.

### PIVOT25R-1 CONSTRAINT-GUIDED DUAL: twin-only best (4.5K, marginal-corner), max-depth obstruction, OPEN [AUTHOR + FINITE]
RE-VERIFIED this session: CEGAR L0 twin-bit INFEASIBLE (2 nodes, 4 edges, cycle [T,F]); L1 root-pair INFEASIBLE (49 nodes, 637 edges, cycle [(7,7),(1,1)] +2, witnesses (28,0)K7 + (297,428)K1 both (1,3)). Stitch incompatible; detours repay -32 vs +2 (17x). CANDIDATES: twin-max 80560, exceedcount 147128, threshold-graft 328K (all worse — recharge-cancel/over-recharge net-negative). TWIN-ONLY Phi=-2*[rA==rB] BEST: n=7 4484/2576574 (this session) classes (0,3,3,2)x2108+(1,3,1,0)x2376; n=8 118760 (same 2 classes); n=9 2197986 (adds (0,4),(1,4) corners) — failures EXACTLY max-depth q=floor((n-1)/2) short 1-2. No finite-range extension covers them without breaking more. COARSE-DOUBLE OPEN (n<=9 BF-certified; universal open). ONE obstruction: max-depth twin-payment gap with zero-side-effect impossibility. Lean: none new (candidates aren't theorems). DO conditional. Zero kills.
