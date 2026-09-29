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
      │  (only B-heavy e_B>3e_A remains)
      ▼
[ OPEN ] STAGE B — min load_before ≤ 2, cap-3 chronological least-loaded
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
│  [EV] 26,080 targeted evals (BR+MW+AS) never breach minload 2
│  [EV] M2-witness: frozen-core + transient-pair drain → refreshment-rescue
│  [EV] saviors always entered@0; entry@3 = 0/44,000+
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

Queued: AS-01 surgical sterile-run falsifier · EX-00 small-n exhaustive Stage-B ·
ENTRY-FRESH formalization · W-WINDOW lemma · Lean E1-CAP/DISPLACE-MONO (post-close).
```

Stage B is the immediate bottleneck. No downstream work until proved/refuted.
