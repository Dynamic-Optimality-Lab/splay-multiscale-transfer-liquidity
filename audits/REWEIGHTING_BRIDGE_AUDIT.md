# REWEIGHTING_BRIDGE_AUDIT.md — C177 local reweighting bridge (LRI)

## 1. Repo cross-audit (§6)
Searched entire repo (code/proofs/audits/history/v01-v03) for: reweight,
reweigh, remass, Georgakopoulos, Lucier, Multi-Splay, dynamic/changing/
reference weight, preferred child/path, progress factor, template splay,
mass assignment, refLeftParent/refRightParent, lip/rip, unpreferred subtree,
weight increase, positive/local reweight, working-set reassignment,
working set, sum-of-log, access lemma, rank potential, heavy/light (as
mechanism, not vocabulary).
RESULT: no such machinery exists. Hits are only "statistical reweighting"
prose, L6 heavy/light vocabulary (definitions, never weight dynamics), and
this campaign's own files. Related-but-distinct banked items: rotation
tables (SplayRotate kernel: single-rotation depth deltas, no weights),
8W.2 yield bounds (bystander depth gains, no masses), LIQ0 ledger
(counts, no weights), tenure/run structure (positions, no masses).
VERDICT: LRI genuinely new (not subsumed). No algebraic mapping to any
corpse exists (corpses concern counts/potentials/matching, never analysis
weights with reweight costs).

## 2. External interfaces supplied (no external search performed)
- Geo04 reweighting lemma (SPLAY amortized <= 3 log(s(root)/w(v)) + 1;
  REWEIGHT cost max(0, 4 log(w'/w)); decreases free). Candidate interface,
  bytes not pinned (no premise use).
- Multi-Splay remassing skeleton (hat_w = mass + US mass; Diamond =
  lip/rip/{x}; w = max over Diamond; dominance invariant; local triple
  reweight per preferred-path switch). Reconstructed from campaign brief;
  preferred-child rule must be defined explicitly (no future smuggling).
- ST85 root-increase design clue (only accessed root increases).
- Lucier (1,n,1,n,...) killer pattern (Theta(n) positive increases kill
  naive global weights; localization mandatory).
- Progress-factor calculus (edge-local W(u)/W(v) with superadditive W).
- Constant audit: D6 needs ~3*dA (6*ceil(dA/2)); Splay access lemma
  coefficient is 3, so log(W/w) ~ dA (not 2*dA); Kraft/normalization
  losses recorded per scheme, never silently absorbed.

## 3. Candidate weight definitions (all to be falsified in §9 kill test)
- W1 depth weights: w(v) = 2^{-dA(v)}. LRI-1 shape OK (log(W/w) ~ dA +
  log W). PREDICTED KILL (LRI-2): shallowing subtrees gain en masse
  (Lucier pattern; R ~ subtree size, unbounded).
- W2 subtree weights: w(v) = 1/s_A(v) (rigid-invariant: moved subtrees
  keep internal sizes). PREDICTED KILL (LRI-2): pivot mass-ratio
  unbounded (tiny pivot absorbs huge subtree, log-ratio O(log n));
  LRI-1 normalization loss (log) + shape mismatch (log s vs dA).
- W4 heavy-light without max-cascade: w from light-subtree masses, no
  Diamond max (tests locality alone). PREDICTED KILL (LRI-2): O(1) nodes
  increase but merge ratios unbounded (tiny/large light-subtree swaps).
- W3 full Diamond/max deferred (needs preferred-child rule + max-cascade
  analysis; max propagates up diamonds (O(depth) cascade predicted)).

## 4. Per-StepEv positive reweight theorem (kill test §9, then prove-or-corpse)
R(A,A') = sum_{w'>w} 4*log(w'/w) over ONE legal A StepEv (ZIG/LL/RR/LR/RL),
tracked separately, across vines/balanced/random/adversarial/C176 histories.
PASS threshold: R <= universal C (independent of n/subtrees).
FAIL xor REPAIR per §10 (local edge data / subtree-set pivots /
progress products / increase-only-at-pivots / decreases-free).

## 5. Exact killers banked so far (analytic; §9 measurement to confirm)
- K-LRI-A (mass budget): LRI-1 with c1<=3 forces shallow nodes to hold
  Omega(W) mass each; satisfiable only with large c0 (~25 for n<=256) or
  c1>3 (weaker than D6). D6-via-LRI needs c1~=3 (divergent boundary).
- K-LRI-B (trilemma): persistent + depth-tracking + local-increase
  triple-incompatible under subtree-moving rotations (pigeonhole stale
  nodes + rigid-move blindness).
- K-LRI-C (dilemma): reweight-to-track-depth gives unbounded R on subtree
  moves; not-tracking gives vacuous LRI-1. No middle (any depth signal
  moves rigidly with subtrees).
- K-LRI-D (merge ratio): any set-mass merge of disparate masses has
  unbounded log-ratio (tiny absorbs huge); progress-factor/edge-local
  schemes inherit it. Bounded ratios need balanced merges only, which
  rotations do not guarantee.
- K-LRI-E (Lucier pattern): (1,n,1,n,...) present-analogue forces
  Theta(n) positive increases for global/recency schemes.

## 6. Relation to C176
LRI does not consume twin-exclusion/pairing/floors as premises (would risk
circularity); it must INDEPENDENTLY bound arrival-divergence magnitude via
weights. Success criterion: LRI-1 + LRI-2 + LRI-3 compose to RATE or direct
Pair Access (side door §17). Current status: all legs OPEN, kill test next.

## 7. Status ledger
- LRI-1 (access encoding): OPEN (candidate W1 shape promissory only).
- LRI-2 (local positive reweight): OPEN, predicted dead (K-LRI-B/C/D).
- LRI-3 (prefix-safe endpoint): OPEN (needs LRI-1/2 first; O(n log n)
  endpoints insufficient for DIRECT-D6; Pair-Access side door tracked).
- LRI-COMPOSE: OPEN.
- PAIR-ACCESS-DIRECT: OPEN.
