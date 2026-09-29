# WP6 Proof DAG — live dependency graph (Stage B → GC → MSTL-14P)

Updated: 2026-09-30 (C28 assault). Prior: `audits/WP6_COLD_RECONSTRUCTION.md` §4.
Legend: [BANKED] proved author-level (Lean-pending noted) · [OPEN] live target ·
[EV] finite evidence · [DEAD] refuted/superseded, never resurrect.

```
[ BANKED ] U=0 · M1 · B-freeze · tenure T123/need/run · A0=B0=T0 · present domain
      │
      ▼
[ BANKED ] TRICHOTOMY — N(b) never empty (E1|E2|E4 or vacuous; E3 bonus)
      │
      ▼
┌─ [BANKED C28-5] E1-CAP ────────────────────────────────────┐
│   e_B≤3e_A → minload≤2 · e_B≤2e_A → minload≤1 (pigeonhole)  │
│   CLOSES all non-B-heavy accesses. GC-independent.         │
└────────────────────────────────────────────────────────────┘
[ BANKED C30-4 ] scaffold: ML-E1-ENTRY · ML-K-PERSIST · ML-ADJ-E4 ·
  ML-DISPLACE-STEP · ML-RISE-WITNESS · ML-W-BLOCKS(sketch+check) · causal E4 fix
[ BANKED C31-2 ] RUN (≤1 demanding KEEP/x-run) · FRESH-CHANNEL (E1≠∅ or
  E4-pristine for every demand) · FRESH-CAP (subsumes E1-CAP) · entry@3 zero/121k ·
  singletons boundary-fresh · blockers zero-in-corpus (M2 singleton only one ever)
[ BANKED C32 ] ENTRY@3 witness (ENTRY-FRESH-universal DEAD) · LADDER theory:
  loads form via re-entry climbs 0→1→2→3 across ≥3 pick-episodes + dormancy;
  drains synchronize N's; dilution (e_A fresh + W-refresh) races drain;
  blockers ejected, never converge (38k + 30k + 2.28M + 121kENTRY evals)
[ BANKED C33 ] SYNCHRONY (spread ≤1 at 100% drains; ≤1 at 97% all) · DILUTION
  (fresh0 med6 vs eB med2; deficit only 7.5%) · negative margins (~1%) NEVER
  convert (40 worst-seeds + rescue-suppression, 8k evals, best 2, margin −31)
      │  (STILL OPEN: spread-3 conjunction; dilution-race formal; scattering)
      ▼
[ BANKED C34 ] DILUTION-ZERO (e_B≤f ⟹ minload 0; 9252/0) · K-RATCHET
  (old-K monotone; fill-order descriptive; fluid-closure≡GC DISCARDED) ·
  K-0 absence characterizes B-heavy elevation (med 3 vs 0)
[C35] K-0 = BUFFER not gate (elevated K0==0 21/25; safe K0==0 59/177;
  E1-0 present+eaten 25/25; case-b immune 5/5; elevation = drain > buffers)
      │  (STILL OPEN: K-0 necessity exact split; spread-3; W-tightening; scattering)
      ▼
[ BANKED C36 ] KERNEL: AR-01..19 exit 0 (AR-08 repaired; AR-17/18/19 trio new;
  no sorry) · splay-model formalization still pending · scaffold/zones/blocks intact
[ REFUTED C37 ] STAGE B online (chronological least-loaded starves: starve_min.json
  n=128 acc8 KEEP-19 eA1 eB7, N=5 all-3; fresh-key-drain mechanism; E1-CAP intact
  (B-heavy open zone)) — the ONLINE path is dead; nothing downstream of it survives
[ BANKED C38 ] GENERIC-HALL (8A deficit-one / 8B deg≥4 / 8C connected / 8E latest-
  access / AR-20+AR-21 kernel) · PEEL verdicts (killer+ENTRY@3 empty; M2 4-core
  stall ⟹ CAP3-PEEL-as-universal REFUTED, flow intact) · 20k Hall hunt clean
  (shortfall 0; best slack 2) · hygiene §25 exact
      │  (STILL OPEN: GC-STATIC old-abundance theorem; one-access Hall; E2-hole;
      │   min-cut+E3; credits; MSTL-14P composition)
      ▼
[ BANKED C39 ] MINCUT (E3-necessary 44/44 saves; optimal packs to cap; glue med18) ·
  GC-ASSAULT 15k clean (gap never >0; cumulative raw-GC 41k+ clean)
      │  (STILL OPEN: GC-STATIC theorem; credits; MSTL-14P composition)
      ▼
[ BANKED C41 ] NEAR-MISS (slack-2 singleton degenerate; large-tight max Q=3;
  diversity law) · 8I/8J/8K (residual shape; |Q_L|≥3|U_L|+1; reverse induction
  ⇒ single lemma: old-new sufficiency) · AUGMENT (optimal E3-only 107/112;
  repair len-3 to spare A5; spare-circularity flagged) · E2-hole bounded
      │  (THE one wall, Q-localized: old-new sufficiency at B-heavy Q-blocks)
      ▼
[ BANKED C40 ] 8H FRESH-BOUND (non-heavy Q never violates; violators need B-heavy
  overflow) · CREDITS resolved outcome-B (no freestanding theorems; downstream
  consumes counts+LIQ0; obligations = GC-STATIC content) · CONDITIONAL CHAIN
  (C0 GC-STATIC open premise → C1 accounting → C2 GC → C3 D6 → C4 service →
  MSTL-14P; audits vs code; support-collapse mapped)
      │  (THE one wall: GC-STATIC old-abundance theorem)
      ▼
[ CONJECTURE C37 ] GC-STATIC: offline cap-3 causal assignment always saturates
  (killer shortfall 0/112; 6k adversarial shortfall 0, GC-gap 0) [FINITE_EVIDENCE]
      │  (IF GC-STATIC proved → GC counting → ledger chain WITHOUT online Stage B;
      │   online-vs-offline audit point flagged; N-FIRST/N-AUG-credit need re-derivation)
      ▼
[ OPEN ] GC — E_B(t) ≤ 3·S_A(t) every present prefix (sole survivor; NO witness either way)
│
│  Five-channel split (SV-00 weights: W62% / K24% / E2 / E1 / E4):
│   ├── E1-overflow channel — E1 saturates in B-heavy; overflow q=e_B−3e_A to old
│   ├── [H1] E2-recent-pusher — M1: B-pushes create E2 edges; recent pushers fresh
│   │       OPEN GAP: young-transient-exposure bound
│   ├── K-deposit channel — per-x-access fresh deposits, persistent via-x
│   │       [DEAD] per-key-flow alone (2.03× refutation, LS-00)
│   ├── [H2/H3] W-injection — transient conveyor, windows med-1 (SV-00), hub-hits
│   │       OPEN GAP: W-window formalization; entry-freshness theorem
│   └── E4-setup channel — tenure-bounded; adjacent DELETE→KEEP pristine
│
│  [EV] 38,080 targeted evals (BR+MW+AS+AS01) never breach minload 2
│  [EV] 2,278,432 exhaustive small-n (n=3,4,5): max minload ≤1, zero minload-2
│  [EV] M2-witness: frozen-core + transient-pair drain → refreshment-rescue
│  [EV] saviors always entered@0; ENTRY@3 exists (C32 witness) but never converges
│  [EV] load-3s are absorbed singletons (M2 hist: 1 minload-2 → 1 load-3, absorbed)
│  [EV] sterile runs to 62 survivable (sterile length NOT the gate; H3 weakened)
│
      │  (IF Stage B proved, with banked D2-sum N≤2X)
      ▼
[ OPEN ] GC — E_B(t) ≤ 3·S_A(t) every present prefix (sole survivor, slack 0.33)
      │  derivation audit queued: no cloning, no double spend, causality, counting
      ▼
[ BANKED ] D2 — D ≤ 2E_B  →  STOCK D ≤ 6S_A (k=6) + rho=2 bandwidth
      ▼
[ OPEN ] N-FIRST-CREDIT + N-AUG-CREDIT (causal-credit corollaries; old forms DEAD)
      ▼
[ OPEN ] MSTL-14P — ACTIVE_pre_discharge ≥ need every present KEEP (author-level)
      ▼
15P → 17P → 18P → 19 (BLOCKED_BY_SOURCE/L2)

[DEAD, do not resurrect] broad-MSTL-14 · raw-rotation · per-key attribution ·
intervals · depth/IPL · Psi · splay-distance · one-step hazard · sterilization-strong ·
X-RETURN-universal · old N-FIRST (slack/interval/reset/setup/borderline) ·
rank/Bellman@scale · SOD-single · raw-dist · quotient-masses/per-run · TSRC ·
corridor-greedy · perceptron · rank-proxy · E3-laminar · E1+E4-only · matroid-free
greedy · per-key-GC [DEAD C28-4] · stronger-minload≤1 [DEAD C28-3, M2 witness].

Queued: K-0 necessity exact split · spread-3 conjunction · W-WINDOW tightening ·
scattering lemma (load-3 convergence) · Lean scaffold (post-close).
```

Stage B is the immediate bottleneck. No downstream work until proved/refuted.
