# LITERATURE_BRIDGE_AUDIT.md — literature-to-arrival-divergence audit (C177-C179)

Campaign: determine whether known Splay/BST theory contains a relational
magnitude object the proof architecture has not consumed, against the exact
open obstruction (arrival-divergence rate: GC-def <= slack/2; 6*ceil(dA/2)
+ pool >= dB - 1 in aggregate). Status vocabulary binding. Finite NEVER
proves universals. Primary bytes frozen for L3/L6 (in-repo); GI/Russo
retrieved to temp with hashes (see §0).

## §0. Source bytes
- L3 Levy-Tarjan: v03/history/external/papers/L3_levy_tarjan_foundation_1907.06310.pdf
  (frozen, SHA in v03/history/external/papers/SHA256SUMS). 29 pp, read crossing/
  monotonicity/crossing-cost sections.
- L6 Chmel et al: v03/history/external/papers/L6_chmel_et_al_2026_2607.18498.pdf
  (frozen, SHA in SHA256SUMS). 68 pp, lemma index built; ranks/gaps/pairings
  lexical scan + structural read of load-bearing lemmas.
- GI Chalermsook-Jiamjitrak ESA 2020: retrieved
  https://drops.dagstuhl.de/.../LIPIcs.ESA.2020.28.pdf (932,849 B,
  sha256 7e97911b...; note aaltodoc sibling is 1.17MB, version differs;
  Dagstuhl version used). 16 pp, read in full (defs, lemmas, proofs).
- Russo arXiv 1511.03148v3: retrieved https://arxiv.org/pdf/1511.03148
  (256,715 B, sha256 ca375d8a...). 19 pp, read (regular access, weights,
  organizing splays, Thm 4.6/7 proof).
- v03 translation audit: v03/history/math/L6_PAIR_ACCESS_MAPPING.md (27/27
  definitions SAME, zero theorems consumed) + theorem_MST26_literature_scope.md
  (non-consumption PROVED as scope record). L6 code: vocabulary only.

## §1. GI (extended geometric inversions) — VERDICT: REFUTED (transplant)
- SOURCE: Defs 5/6/7 (inversion / extended inversion / base potential Phi as
  total EI count, z-coins), Lemma 8 (upward-path), Lemma 9 (z on S_A(x) has
  z-coin at LCA_O; CP(z,LCA)=1, CP<=Phi pointwise, sum CP=|S_A|), Def 12
  (Phi proves A<=_eta O: drop + eta*|S_O| >= |S_A|), Prop 13
  (cost_A <= eta*cost_O + Phi_max), Lemma 15/21 (witness intervals: net-new
  coins <= O(|S_O|); per-alpha <= 4), Lemma 27 (static-optimality-via-Psi +
  move-to-root => MTR-competitive), Thm 20 (G(X) <= 4*cost_O + m + n^2).
- REPO ANALOGUE: subject=B, reference=A (pre-access per §5 experiment).
- PRIOR STATUS: definitions never transplanted (no GI code existed); no prior
  corpse (family-name dismissal forbidden; this is first contact).
- KILLERS (exact):
  K1 log-depth reference required: ranks = depth in nearly-optimal T* with
  LOGARITHMIC depth (Theorem 2); heavy paths/gaps/bends/lazy intervals/
  Lemma 11-15/22 all need low ranks or O(log G). Ours: arbitrary-depth
  vines (d up to 253). Transplanting our depths gives O(n)-gaps (not O(log)),
  killing every quantitative lemma. [assumption mismatch, §20-rule-2]
  K2 additive terms kill per-prefix tightness: Prop 13/Thm 20 carry Phi_max /
  n^2 initial + m per-access + O(n log n) globals. Our margins are 0-6 on
  n=256 histories. No additive term is affordable. [form mismatch]
  K3 moving reference uncovered: GI theorems handle static O + MTR-moved O
  (separate global accounting). Our A splays EVERY access. No GI theorem
  bounds arbitrary reference moves. [missing theorem, not a gap in ours]
  K4 reference-update creation UNBOUNDED (machine-measured, gistep.json):
  net coins per A-StepEv scales ~n^2/2 (n=32:496, 64:2016, 128:8120,
  256:32632, 512:130808; movesz ~ n-1). No universal C exists for
  Delta_Phi <= C*e_A. Single zig gives exactly 1 (massive cancellation
  elsewhere), but deep doubles shifting whole subtrees create ~n^2/2 net.
  [exact finite refutation of transplanted bound]
  K5 witness-interval vacuous/false here: with reference = post-A-splay A1
  (x at root), |S_O| = 1, so O(|S_O|) = O(1) against O(n)-scale creation
  (K4). Lemma 15's proof needs low-rank x± (fails: ranks arbitrary).
  K6 per-access B <= O(A-depth) FALSE on diverged bursts ((0,127) needs
  C >= 254; unbounded across instances). [exact counterexample class]
- SURVIVING FRAGMENTS (true but insufficient, no Lean per policy):
  CP-existence (Lemma 9 analog verified 0/530 fails on traces; pure
  laminarity+LCA structure, always true). Twin Phi_0 = n EXACTLY at all n
  (self-coins only, zero cross-EI on identical trees; elegant, insufficient).
  Neither bounds creation => neither implies RATE.
- VERDICT: REFUTED (transplant). Six independent exact killers.

## §2. Russo reference-depth weights — VERDICT: REFUTED (transplant)
- SOURCE: w_T(v) = 1/4^{d_T(v)} on OPT T; amortized splay_S(v) <= O(1+d_T(v));
  organizing splays (extra splays optimizing for future); Conjecture 3.1
  REGULAR ACCESS (c_1+..+c_m = O(c'_1+..+c'_{m+e})); Thm 4.6/7: splay total
  = O(n+R+M) given regular access.
- REPO ANALOGUE: S=B, T=A (reference weights from A), per §9-10.
- KILLERS:
  K1 open-conjecture premise: Conjecture 3.1 explicitly unproved by the
  author ("At this time we do not have a proof"). Consuming it assumes an
  open splay property likely as hard as the target. [source-admitted gap]
  K2 global-with-additive: O(n+R+M) with O(n) additive; per-prefix
  tightness (margins 0-6) incompatible. [form mismatch]
  K3 per-access form false: splay_B <= O(1+d_A) fails on diverged bursts
  ((0,127): needs C >= 254; unbounded). Organizing splays (which would
  fix this) need regular access (K1). [exact counterexample class]
- VERDICT: REFUTED (transplant). (Reference-splay change Delta_Phi_R <=
  C*e_A hoped in §10 inherits K1-K3; no separate experiment needed.)

## §3. L3 Levy-Tarjan crossing machinery — VERDICT: INAPPLICABLE-AS-PROOF
- SOURCE: crossing nodes (x, root, direction-alternating path nodes),
  crossing depth l_T(x), bookkeeping nodes (rest), crossing cost sum(l),
  bookkeeping cost sum(d-l); crossing bound = MTR crossing cost ~= Wilber II;
  approximate monotonicity (cost(Y) <= b*cost(X) for subsequences) iff
  dynamic optimality; optimal algorithms monotone (Thm 3.1); temporal spread
  discussion; single-request-removal cost-increase examples.
- REPO ANALOGUE: decompose dB_arr = crossing + bookkeeping depth (§16).
- FINDINGS:
  F1 Our danger sits in BOOKKEEPING (straight vine runs): (0,127) burst at
  dB=253 on a vine has crossing depth ~= 2, bookkeeping ~= 251. Crossing
  machinery is blind to vine-danger (measures alternations; danger is
  straight runs). [anti-correlation, exact]
  F2 Crossing bound is a LOWER bound on OPT (wrong direction for our UPPER
  bound needs). Approximate monotonicity is a global subsequence-robustness
  property, not a per-prefix ratio. Temporal spread EXPLAINS burden
  movement (matches pool/divergence dynamics qualitatively) but bounds
  nothing in our ledger.
  F3 L3 is a FOUNDATION (defines crossing, proves lower-bound monotonicity,
  outlines barriers); it proves NO splay upper bound (that IS dynamic
  optimality). Nothing to transplant as a premise.
- VERDICT: INAPPLICABLE-AS-PROOF (right language for the danger's address
  (bookkeeping depth) and temporal picture; zero theorems bounding it by
  A-work). Not a corpse (never claimed as proof route); recorded to prevent
  rediscovery.

## §4. L6 theorems (Chmel et al.) — VERDICT: REFUTED (transplant, all forms)
- SCOPE: 27/27 definitions translated, ZERO theorems consumed (MST26 scope
  record). This audit is first theorem-level contact.
- LOAD-BEARING LEMMAS vs OUR THREE STRUCTURAL KILLS (K1 log-depth
  reference; K2 additive/global (n^2, m, O(n log G)) vs per-prefix tight
  margins 0-6; K3 moving reference (T*/MTR/static only; our A splays
  every access)):
  Lemma 9/CP-analog: same as GI Lemma 9 (structural, survives as pure
    fact; insufficient (no bound)). Noted, not formalized (policy).
  Lemma 10 (good pairing decreases contracted gap): needs contracted gaps
    + log framework (K1). Dead.
  Lemma 13/15 (O(1) junctions/updates on T* rotation): need log-depth T*
    (K1); bound INTERVALS not mass (mass unbounded per gistep K4).
    Dead (reference-move form included).
  Lemma 22 (O(log G) important pairings): needs log gaps (K1). Dead.
  Lemma 25/26/32-35 (global counting, u+O((n+cost)log G)): global+additive
    (K2); OPT-relative not A-relative. Dead.
  Theorem 1/20 (global + additive + OPT-relative): K2 + wrong comparator
    (OPT cost vs our S_A StepEvs). Dead.
- §13 OUTCOMES: (A) not same obstruction (L6: global asymptotic gap
  accounting with log reference; ours: per-prefix exact with arbitrary
  reference — strictly narrower target, different reference choice
  (pre-arrival A vs post-A snapshot), no theorem consumed): verdict MIX
  B+C+D (narrower target + lost arrival information + theorems never
  consumed). (E) superconstant loss stands (no Pair-Access collapse found).
- §14 LAZY-INTERVALS-AS-POOL: REFUTED analytically. L6 gap mass scales
  with REFERENCE depth (ranks = depth in A); arrival-divergence has SHALLOW
  reference (dA small) by definition. L6 mass is SMALL exactly when our
  danger is LARGE (anti-correlation, from gap defs directly). Lazy
  intervals/point/contracted gaps do NOT measure our danger. No experiment
  needed (definitional mismatch).
- VERDICT: REFUTED (transplant, all forms with exact killers K1/K2/K3 +
  anti-correlation).

## §5. v03 Branch-A/B + transfer calculus — VERDICT: EXACTLY_SUBSUMED / OPEN
- Prior finding (from repo records): contracted baseline reproduced shape
  only; transfer calculus attacked need without contraction; raw boundary
  laws failed; MST0-08 locality gap stands; final v0.3 obstruction recorded.
- Current relevance: none of Branch-A/B machinery addresses pre-arrival
  A-relative magnitude with per-prefix exactness (same K1/K2/K3 family).
  No re-audit needed beyond this pointer. VERDICT: EXACTLY_SUBSUMED
  (by K1/K2/K3 above + v03's own obstruction record).

## §6. What survives for the rate law
- CP-existence (canonical payment supported on A-path; verified 0/530).
- Twin Phi_0 = n exactly (self-coins only).
- Subject-update net-new <= 0 on all measured traces (giscale.json;
  B-splays never create net coins here — unproven universally, and
  insufficient alone).
- Crossing/bookkeeping vocabulary (names the danger's address).
- NOTHING bounding reference-update creation (unbounded ~n^2/2 measured)
  or per-access B-vs-A magnitude. The rate law stands open.

## §7. Campaign ledger (countermodel loop)
- G0 base (prior kernels only): abstract violators exist trivially
  (unbounded spending, no creation bound) — not built as program (hand
  analysis already exhibits arrival-diverged pairs with unbounded ratio).
- G1 + GI transplant: KILLED by K1-K6 (log-depth/additive/moving-ref/
  measured-unbounded/vacuous-witness/counterexample-class).
- G2 + Russo transplant: KILLED (open-conjecture/additive/per-access-false).
- G3 + L3 transplant: INAPPLICABLE (foundation only; crossing blind to
  vine-danger; no upper-bound theorem).
- G4 + L6-theorem transplant: KILLED (K1/K2/K3 per lemma; anti-correlation
  for gap-as-pool).
- No surviving bridge. Monotone refinement terminates: all known literature
  families exhausted with exact killers. Rate law OPEN.
