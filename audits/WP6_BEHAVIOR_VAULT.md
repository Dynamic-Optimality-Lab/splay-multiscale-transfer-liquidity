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
