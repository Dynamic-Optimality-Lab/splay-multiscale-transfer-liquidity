# C184 — KEEP-2STEP DECISION AUDIT

Branch `wp5x-k6c2-specialized`, HEAD `88f344d` + local C161–C184 tree
(authoritative working tree; no history rewritten, main untouched).

Target theorem (sole remaining GC decision inequality):

    KR2(h,x) := r_x(s) + Q(K_x(s)) - Phi(h) <= 0

universally on reachable present-legal histories (exact integers;
`scripts/wp6_keep2step.py`). Any reachable KR2>0 appends its maximizing
<=3-KEEP continuation and drives Phi<0 = genuine GC refutation (mission
Sec 21). No KR2>0 was found: terminal B is unavailable.

## 1. Falsification ledger (all negative, exact)

- Phi_min BFS (exact min-Phi + R3 check): n=3 (19 reached pairs), n=4
  (196 pairs): worst KR2 = 0. No negative cycle / negative dist.
- Random walks n=8..48 (vine/reverse-vine/balanced/random, mixed
  KEEP/DELETE, L=25..40): best KR2 = 0 everywhere (tight).
- Targeted 14 families (deep cycles, DELETE epochs C176-shape, far-key
  alternation, combs, stale-root, DELETE builders, KEEP-heavy): 0
  (one -2).
- Myopic beam n=12,20 (14 deep): 0 (degenerate, weak adversary — noted).
- Maximizing triples + reset windows (150 records): best 0; Q(s1)=0 in
  95%+ (single-term regime); y==x attainer 62% when Q>0.
- BK1 +11 witness replay (micro s=6, Phi=97, r=31): max KR2 = -55
  (margin 55 where BK1 fails; Q1 up to 41 absorbed by Phi).
- n=3 exhaustive histories (all 5 T0 x all 6^4+6^5 action strings,
  220320 states): 0 kills, best exactly 0.
- Micro-seed sweep (40 seeds, all high-r states): KR2 <= -10.
- matters-subcase (y≠x with Q_y>H1(s1)): occurs (11% of Q>0) but tiny
  (-17..-41) vs bank.

## 2. Lipschitz reformulation (new proof architecture)

R3(A,B) := max_x [r_x + Q(K_x)] (= R3 in audit). KEEP-2STEP is
P(h) : Phi(h) >= R3(end(h)), proved by history induction from:

- Base R3(diag) = 0 (root residual 0, no-op KEEP).
- DELETE-Lip: R3(D_z) <= R3 + 3a_z. Clean EVERYWHERE tested: all pairs
  n=4 (196) + n=5 (1764), arbitrary n<=24, all reachable sweeps.
  Excess exactly 0 (tight). Conjectured universal state theorem.
- KEEP-Lip: R3(K_z) <= R3 - r_z. Clean on ALL reachable states tested
  (walks, tight states, micro extremes incl. R3=42 witness with slack;
  tight 0s). REFUTED universally: +1 on rare large arbitrary pairs
  (2/60 at n=24; clean <=18).

Induction steps kernelized (`GCStaticKeepResidual.lean`: `lip_delete_step`,
`lip_keep_step`, `lip_diag_base`; §2 expansion `kr2_expand_1/2/3`,
`phi_after_keep`; attainer collapse `keep2step_of_attainer`; gap bound
`keep2_gap_le_h1s2`). All `lean` exit 0, no sorry/admit/axioms.

## 3. The +1 KEEP-Lip witness (exact, new phenomenon)

`keep2step/lip_witness.json`. Both hits: KEEP of the A-rooted R3-attainer
itself with (a,b)=(0,3) (A-free pure drain r=3); post-state R3 exceeds
budget by exactly 1 (new liability via Q of a bystander key created by the
B-side splay). DELETE-Lip at the same key is exactly tight (0). Max excess
1 (never >=2 observed). Scale-emergent (onset n>=19), rare (~3%), same
family as BK1+11/collapse+1. Reachability unknown (random pairs).

## 4. Falsified side-routes (§20, bounded-prepend note)

- §20 third-term saturation: FALSE (r_z=13>0 after maximizing pair at
  micro s=6: F3>F2 genuinely). Not pursued.
- y=x attainer case: PROVED reducible to KEEP-RESIDUAL (root-noop;
  kernelized). Wild confirmation (micro s=6 x=1: y=1 exactly).
- Case-(b)-with-r_y>=0 implies BK1 violation at the future state
  (derived, not yet exploitable).

## 5. Proof status per component

- PROVED+KERNELIZED: §2 expansion algebra; Phi_after identity; y=x
  collapse (mod KEEP-RESIDUAL); gap<=H1(s2) compression; Lipschitz
  induction skeleton (conditional).
- FINITE-CLEAN (open): DELETE-Lip universal (no counterexample anywhere);
  KEEP-Lip reachable (only arbitrary-pair +1s); KEEP-RESIDUAL reach;
  DELETE-H2 (mission §0.11 reduction asserted, Lean ride pending);
  BD1 AUTHOR (Lean ride-induction deferred).
- REFUTED (not revived): PREPEND-2, ROOT-COLLAPSE x2, §20 saturation.

## 6. Verdict

NO TERMINAL REACHED. Terminal A (KEEP-2STEP proved) is blocked on the
reachable-KEEP-Lipschitz gap (= bystander creation across KEEP, the same
unified wall as C176–C183, now in sharpest Lipschitz form). Terminal B
(reachable KR2>0 -> GC kill) has no witness after 8-channel exhaustive
negative falsification. Nothing is promoted to proof; no axiom/sorry
introduced; no definition mutated; no history rewritten.

## 8. Resumed findings (C184-2, same session)

- BOUNDED-PREPEND (new AUTHOR lemma, finite-universal): a prepended splay
  saves downstream 2-access cost at most its own event-cost,
  `C_T(x,y) - C_T(z,x,y) <= a_z(T)`. Clean exhaustively n<=6 + vines /
  balanced / random BSTs n<=64 (tight 0). (Unbounded PREPEND-2 stays dead;
  this bounded form is what DELETE-Lip needs.)
- DELETE-Lip proof skeleton mapped: B-terms cancel EXACTLY across the
  DELETE (B frozen, same x*/y* KEEPs both sides), reducing to attainer
  A-drop correlation. Gap isolated precisely.
- Per-chain growth is NOT Lipschitz: measured +52 chain growth across a
  DELETE banking 45 (vine32 diagonal, z=30). Any proof MUST use
  max-structure (R3 grew only 20: 0->20 vs budget 45). Chain-wise
  induction is impossible — negative guidance recorded.
- Drop-sums S<0 attainable for arbitrary keys (down to -11 sampled):
  attainer-essential confirmed (proof must exploit maximizer structure).
- C184-3 DELETE z-CHAIN EXACTNESS: post-DELETE R3-attainer is z itself in
  98.6% (414/420 post-DELETE states; 512/525 earlier sweep); every tight
  DELETE-Lip case has attainer z; all non-z attainers carry slack (only
  one at -2). z-chain growth is EXACTLY 3a_z by root-noop identity
  (r_z(D)=b_z since a=0; K_z(D_z(p))=K_z(p) same state) — kernelized
  conditionally (`delete_zchain_exact`, `delete_r3_zpart`, exit 0); model
  grounding available (`splay_at_root` kernel-proved in GCStaticLoop.lean;
  needs H1/Q tree layer + ecount-at-root for full closure).
  Remaining DELETE-Lip remainder: non-z attainer drop-correlation (2.5%).
- C186 SAME-B H1-DIFF + LAYERING IMPOSSIBILITY: `h1_diff_sameB` kernel
  green (floor-aware outer max(0,·) is load-bearing; un-floored form refuted
  in double-zero case). Single-key saving<=a_z finite-clean tight (drop ≤
  2a_z each — 6x off joint need without correlation). NEGATIVE RESULT:
  nested max-lifting multiplies budget by lookahead depth, so no layered
  per-key bound can close DELETE-Lip/KEEP-Lip without the joint
  drop-correlation (S≥0-ish, 96.6% finite). AUTHOR-derivation recorded:
  gap−zslack ≤ −3S (conditional on nested Q-diff bound).
- C188 SUBCASE SPLIT (toward proof): non-z DELETE attainer splits by
  floors — 1-term (Q(s1)=0) CLOSED mod single-prepend (kernel
  `delete_lip_1term` + `resid_le_R3`); SINGLE-PREPEND (saving_1 ≤ 0)
  finite 0/2640+ with rotation-counting AUTHOR-sketch; 2-term
  (H1(s2)=0) jointness finite-clean (min exactly 0; vine refutation was
  third-term, consistent); 3-term (H1>0) + KEEP a≥1 REMAIN OPEN.
  VERDICT: GC-STATIC neither proved (blocked on bystander-creation
  control: 3-term joint correlation + a≥1 mechanism) nor refuted
  (exhaustive negative falsification: KR2, Lipschitz-reachable, Phi-SA).
  Exact obligation list for closure: single-prepend kernel-proof (BD1
  kit) → 2-term mechanism → 3-term correlation → cleanliness proof →
  a≥1 mechanism.
- C187 KEEP SPLIT (DELETE-Lip + B-from-D): post-KEEP R3-attainer is NEVER
  z (61/61 reachable; opposite asymmetry to DELETE's 98.6% — liability
  lives in bystanders). B-only Lipschitz REFUTED from arbitrary A (+4)
  but HOLDS TIGHT (0) from A-rooted D-states. So KEEP-Lip factors exactly.
  Kernelized green: `bstep_zchain_exact_tree` (z-chain drops exactly b_z
  across B-step) + `keep_lip_split` (pure-arithmetic composition).
  Remaining: DELETE-Lip remainder (non-z 2.5%) + B-from-D attainer
  correlation (same shape, B-side).
- C185 ATTACK ROUND (a)(b)(c):
  (a) TREE LAYER CLOSED: `lean/WP6/GCStaticKeep2Step.lean` (sanctioned name)
  kernel green — STree H1/Q/R3 layer matching engine semantics, fold-max
  dominance, `delete_zchain_exact_tree` + `delete_r3_zpart_tree` grounded
  in the model down to single operational hypothesis hNode (post-DELETE
  A rooted at z; consequence of banked deliver+validity+membership).
  Bare-Lean note: no `le_trans`/`le_max_*` in scope — order reasoning via
  `omega`+hypotheses; match-compiled defs need shape-split before unfold.
  (b) NON-Z ATTAINERS: 1.4–2.5% of post-DELETE states; all carry slack
  (top excess -4..-8); the single tight non-z instance was a tie with the
  z-chain (tie-break artifact). Refined conjecture: tight DELETE-Lip ⟹
  z-chain attains (up to ties).
  (c) STEERED +1-SIGNATURE HOLDS TIGHT: DELETE-reroot after deep churn
  reproduces (a=0,b=2..3,R3=att=tgt) reachable — KEEP-Lip excess exactly 0
  every time (post-R3 annihilates to 0, n=24/32, 20+ steers). Same local
  signature fails (+1) only on arbitrary pairs. CONCLUSION: reachability
  is load-bearing for KEEP-Lip; pure-state proof impossible (witnessed);
  proof must consume historical consistency.
- C185-2 DOUBLE-ROOTED-R3 KILLED + A-FREE SUBCASE CLOSED (conditional):
  post-KEEP R3 hits 11 on micro double-rooted states (no general
  cleanliness). BUT A-free KEEP (a_z=0) splits decisively: reachable
  post-R3 = 0 always (steers+walks+micro), arbitrary post-R3 up to 2 —
  ROOT-KEEP CLEANLINESS is reachability-essential (new finite lemma).
  Kernelized (`Q_nonneg`, `resid_le_R3`, `keep_lip_afree`, exit 0): the
  a_z=0 KEEP-Lip subcase — covering BOTH known +1 witnesses — follows
  from cleanliness + state fact R3 ≥ r_z. Remaining KEEP-Lip: a_z ≥ 1.

## 9. Resume state (carried over + updated)

- Tree: HEAD 88f344d + uncommitted C161–C184 (see `git status`).
- Active subcase: prove reachable-KEEP-Lip (R3(K_z)<=R3-r_z on pairs
  reachable from a diagonal), or find a reachable +1 (then immediately
  test KR2>0 nearby per Sec 21).
- Minimized candidates: `keep2step/lip_witness.json` (arbitrary-pair +1s,
  recipe inside); tight-reachable states all clean.
- Resume commands: `py scripts/wp6_keep2step.py walk|targeted|beam|phimin|
  triples`; `lean lean/WP6/GCStaticKeepResidual.lean`.
- Suggested next theory: 4-key rotation-row coupling for DELETE-Lip
  (B-frozen: same-B'' attainer argument gives H1-diff <= attainer drop);
  last-reset nesting for reachable-KEEP-Lip (asymmetry grounded at
  DELETE-created divergence from diagonal genesis).
