# GCSTATIC TARGET DIRECT — C190 scratch/proof audit

TARGET:
  for every reachable state s and legal KEEP z,
  r_z(s) + R3(K_z s) <= R3(s).

Frozen semantics: a/b = exact A/B StepEv counts (event-list lengths =
ceil(depth/2) by kernel ecount_eq); r = b-3a; K_z splays both trees at z;
Net_s(word) = sequential KEEP sum of (b-3a); R3 = max over KEEP words
|.|<=3 incl. STOP(=0). Verified against repo engine (0 formula/replay
mismatches, C181). No new quantities introduced below.

## PROOF OF TARGET

Closed cases (each sound by replay-algebra / root-noop / floors, kernel
tags in lean/WP6/GCStaticKeep2Step.lean unless noted):

- TGT<=0 -> STOP (Net([])=0). Kernel: R3_nonneg, exch_stop_consume.
- Post len 0 (post=0): TGT=r_z. [z] gives Net=r_z exactly; STOP if r_z<=0.
- Post len<=2: tau=[z]++sigma*, |tau|<=3, Net splits exactly
  (Net_s = r_z(s) + Net_{s'}(sigma*)). Kernel: keep_exchange_short.
- Post len 3 with shorter s'-tie sub: tau=[z]++sub, same split.
  Kernel: keep_exchange_tie. (Walk len-3 post-attainers all tied.)
- Post len 1 DELETE: same-chain via single-prepend (r-diff = -3drop,
  B frozen). Kernel: delete_lip_1term (hSP = single-prepend shadow).
- Double-rooted s (z rooted both): r_z=0 and K_z=noop, equality.
  Kernel: target_doubleroot_tree (fully proved, verified 0/12 nonzero).
  Eliminates last-op-KEEP-z minimal counterexamples.
- a_z=0 DELETE side: z-chain exact (delete_zchain_exact_tree,
  delete_r3_zpart_tree; grounded to valid+mem via deliver bridge).

Unclosed hard case (same TARGET, no renaming): reachable s, KEEP z,
strict len-3 post-attainer [x,y,w] (all-distinct, z-free by root-noop
deletion, post>0, no shorter tie), TGT>0. Only universal taus left are
same-chain [x,y,w] (STOP/[z]+sub fail by strictness). Obligation:
Net_s([x,y,w]) - Net_{s'}([x,y,w]) >= r_z, i.e. 3-term drop-correlation.
Status: OPEN. (plus1/t=5 arbitrary pair is exactly here and fails;
no reachable instance found.)

## FALSIFICATION OF TARGET

- Residual r_z+R3(K_z)-R3(s) on reachable walks/micro/steered (incl.
  R3=42 extremes, A-rooted B-deep steers, n<=48): all <=0, tight 0s.
- KR2/Phi direct channels to n=64/96/128: clean; Phi-SA 550+ histories
  minPhi 0.
- Arbitrary pairs: +1 KEEP-Lip family (a_z=0,b_z=3, onset n>=19, rare
  ~3%, excess exactly 1, post-R3 in {1,2}, no s'-ties). Reachability
  unknown; n<=18 dense hunt (100 pairs) clean. NOT a GC kill (needs
  history + Phi<0 continuation, none exists).
- Double-rooted residual: 0/12 nonzero (trivial-case check).
- B-saving min: -12 reachable-extracted B, -7 arbitrary (pure-B lemma
  for a_z=0 dead).

## SUPPORTING CALCULATION USED IMMEDIATELY IN PROOF OF TARGET

C193 direct-Phi strong induction (no R3): DELETE-last/profitable-KEEP/
base free by banking+IH; a_z=0-draining KEEP fuses via macro
([DELETE z, noops, KEEP z] = direct KEEP, same state+Phi, shorter) to IH;
macro shape verified wild 3/3; state+Phi match kernel green
(macro_state_match, macro_phi_match). Greedy max-r drain + SA-max clean.
SINGLE OPEN STEP: a_z>=1 draining KEEP covered (r_z<=Phi(Pfx)).

- Selector scan (424 transitions): F2+ never wins; menu = {STOP,[z],
  [z]+sub,same}. Vine52 needs outside root (STOP); plus1 unfixable.
- Maximality ledger: strict attainer gives r_w2>0, segment strictness,
  z-free-ness, repetition collapse ([x,x,y] identical to [x,y]).
- B-prepend REFUTED (+4): DELETE has no [z]+sub rule (asymmetry recorded).
- Post-KEEP attainer never z (61/61); post-DELETE attainer z 98.6%.
- Per-chain growth +52 vs bank 45 (max-structure mandatory); drops to -11;
  S<0 in 3.4% (slack-covered, undescribed); single-prepend finite 0/2640+
  with rotation-counting sketch ([MECHANICS-ROT] open); two-term jointness
  finite-clean min 0 (mechanism open); nested lifting multiplies budget
  per level (jointness unavoidable, proved as negative guidance).
- Last-op split: KEEP-z-last trivial (above); DELETE-z-last = B-from-D
  (finite-tight, open); else general. History-minimality adds nothing
  further (last-op bridge needs transition-comparison = Lipschitz proper).
- Rotation case analysis assessed unexecutable-in-principle for drops
  (drop locations are post-downstream; rows give per-rotation bounds only).

## VERDICT

Neither END A (proof blocked on strict len-3 same-chain drop-correlation
+ DELETE non-z + B-from-D + cleanliness/a>=1 proofs) nor END B (no
reachable residual>0) is reached. GC-STATIC OPEN/NO_WITNESS. All Lean
lemmas green, no sorry/admit/axioms, nothing promoted, nothing committed.
