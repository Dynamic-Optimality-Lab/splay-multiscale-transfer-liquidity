# 8AC Closure Proof (C121→; autonomous campaign)

Target: 8AC (cap-3 causal routing with combined accounting, no double-count)
=> Hall(Q) ∀Q => GC-STATIC => E_B ≤ 3S_A => D ≤ 6S_A => service => MSTL-14P.
Method: Mode B (first failure) + Mode A (sufficient lemmas). Status per section.
Conventions match WP6_MINIMAL_COUNTEREXAMPLE.md (present-legal instances only;
B demand 1/event; A cap 3/sited source; past-only E1+E2+E3+E4+E7; Delta(Q)).

## C121. FIRST-FAILURE-FRESH-SUFFIX [PROVED_AUTHOR]
(Campaign §5 item; vault C121-FFFS. ID differs from campaign "C120" label only
because C120-EXACT-SHAPES already occupies C120.)

Assume some present-legal history has unsaturable cap-3 causal demand (¬8AC
matching-form). Order all B-events chronologically (access idx, then Bev index;
finite total order). Let b* = first B-event with prefix {b_1..b*} unsaturable
(exists: full demand unsaturable + well-ordering on Nat prefix index; prefix
before b* saturates by minimality, empty prefix vacuously). Let L = access(b*),
f = |E1(L)| (sited same-access Aev count = e_A(L) sited StepEv count, by 8S),
r = #{B-events of access L strictly before b*}.

Claim: r >= 3f. Hence Case A (f > 0): r >= 3f >= 3 and e_B(L) > 3f (B-heavy at
L, since r+1 <= e_B(L)). Case B (f = 0): vacuous (r >= 0).

Proof. Let M saturate prefix-minus-b* (exists by first-failure minimality;
finite b-matching existence predicate; M respects cap 3 and demand 1).
E1(L) sources are adjacent ONLY to L-Bevs: E1(L) subset elig[j] iff acc(j) = L
(builder: e1 = set(a for a in accA[idx] if sited) with idx = Bev's own access
(abl lines 64-66), identical for all Bevs at idx (E1-completeness); E2/E3/E4/E7
of earlier Bevs never contain ai=L ids (E2 window u<idx<L, E3 ai<=idx<L, E4
setup<=idx<L, E7 v<u<L (abl lines 68-94); causality ai<=acc throughout).
In M, E1(L)-load <= r: only the r earlier L-events are placed and can use E1(L)
(b* unplaced; later L-events outside the prefix; earlier accesses nonadjacent
as shown). Each placed demand uses 1 unit, so free E1 slots >= 3f - r
(f sources x cap 3 (abl lines 105-107)). If r < 3f (r <= 3f-1): free >= 1, so
some s in E1(L) has load_M(s) <= 2. b* is E1-adjacent to s (completeness +
both sited/demand in graph (hallcore adjacency)). M U {b*->s} is a valid
cap-3 matching (s has free cap, b* unmatched, edge exists) saturating
prefix-through-b*, contradicting first-failure definition. Therefore r >= 3f.
Case A corollary: e_B(L) >= r+1 >= 3f+1 > 3f. QED.

Dependencies (all banked/audited, no finite evidence used): E1 construction +
completeness (abl 64-66); per-Bev access scoping (E1(L) only in L-Bevs' elig);
cap 3 iff sited (abl 105-107; hallcore 53-54); B-demand 1 (abl 108); 8S (all
StepEvs sited: E1(L) exactly the sited set, f = StepEv count, no filtering
loss); chronological B-order; finite matching existence; first-failure
well-ordering. Audits: G (W/K untouched); E (¬8AC assumed = Mode B, legitimate);
J (past-only used correctly; no future leak); F (no induction/carry); A (n
unbounded); B (present-legal only); C (real builder graph); L (cap arithmetic
exact). Lean kernels: ffs_free, eb_suffix (GCStaticArith.lean, exit 0).

Dichotomy banked: first failure is either post-fresh-suffix (Case A: e_A(L)>0,
b* at B-position >= 3f within access L, L B-heavy) or repeat/no-fresh (Case B:
e_A(L)=0, E1 empty; descent required (§6 campaign: repeat-case backward
descent via 8R/tenure/rebuild machinery)).

## C122-DESCENT. REPEAT-CASE BACKWARD DESCENT [PROVED_AUTHOR]
(Campaign §6 item. ID note: campaign §7+ numbers shift by one hereafter
(C121-FFFS occupies C121); typed trap = C123-TRAP, immune-descent = C124-IMM,
W-cycle = C125, NO-FREE-W-LOOP = C126+.)

Setup: Case-B first failure — access L on key x with e_A(L) = 0 (A-trivial:
x A-rooted before L (present domain: e_A = 0 iff x at root, since absent keys
are illegal and splay_trace emits [] exactly for absent/root (legacy_embedding
107-143))), b* a B-event at L, e_B(L) > 0 (demanding: B-events exist iff B-trace
nonempty iff x NOT B-rooted (same mechanics)), prefix-minus-b* saturable.
So x is A-rooted yet B-deep (stale) at L — the pressure shape.

Claim: there is a finite strictly-decreasing chain of access indices
L = t_0 > t_1 > ... > t_k (rank = access index, well-founded on Nat) where each
step names its causal creator/rebuilder and created channel, terminating in
either (a) a nontrivial-A access (CASE-A-like origin banking E1/K-imprints),
or (b) a thin origin (T0-root-x never touched, trivial setup, or silent-ride
rebuilding with no banked imprint). Each origin's supply content is specified;
thin origins hand EXACTLY the 8Y-conjunction remainder to variation analysis
(no supply claim made there).

Proof by backward construction (each step proved from banked laws):
D1. L is not history-first: first access has A=B=T0, so x A-rooted ⟹ x B-rooted
  ⟹ B-trivial (e_B = 0), contradicting demanding. Hence past accesses exist. [8T]
D2. Some DELETE occurred before L: if all past accesses were KEEPs, A and B
  (both from T0) evolved identically (KEEP splays same key in both trees),
  so x A-rooted ⟺ x B-rooted, contradicting B-deep. Hence ≥1 past DELETE.
  (DELETE moves A only (Pair Access def); KEEP moves both; B-freeze T3.)
D3. E1-empty + demanding ⟹ H[L-1] = x: otherwise H[L-1] ≠ x ⟹ x A-nonroot
  before L (only the accessed key roots... precisely: non-access leaves the
  previous A-state; x A-rooted now with H[L-1]≠x means x was ALREADY rooted
  and untouched — consistent so far, but FRESH-CHANNEL case (a) gives E1≠∅
  whenever H[t-1]≠x with x nonroot; the E1-empty case forces the complementary
  branch) — apply FRESH-CHANNEL (banked C31-2) directly: demanding + E1-empty
  ⟹ H[L-1] = x AND L-1 is DELETE (KEEP→KEEP repeat is B-no-op, contradicting
  demanding) AND run-start s (first consecutive-x access ≤ L-1) satisfies
  setup[x] = s with E4-pristine accA[s] (causal snapshot setups[·], abl 67-68).
  Provided s itself was nontrivial-A (e_A(s) ≥ 1, i.e., x nonroot before s);
  if s was trivial (x already rooted), setup[x] was NOT updated at s (nrb false,
  abl 45-46) and E4(s) is empty — descent continues past s (see D5).
D4. B-deep-x at L with A-rooted-x ⟹ B was deepened while A stayed rooted:
  B moves only at KEEPs (B-freeze); any KEEP z≠x unroots A-x unless z was
  A-rooted (then A-trivial no-op). Hence B-deepening KEEPs were either (i) x
  -involving (imprint ∋ x-path keys: K/E3-visible (8U mechanics; E2-visible iff
  pumped (pump_push ∋ x))), or (ii) A-trivial pushers (z A-rooted, B-splashing:
  e_A = 0, bank nothing; 8R: single-shot per state, splash roots B-pusher), or
  (iii) silent rides (G-outer trains, +2, off-chain roots; 8W). Cases (i)-(ii)
  bank imprints or alternate with supplying accesses (8R corollary); case (iii)
  banks train/block/path-root imprints on-chain (motion involves ancestor roots
  which lie on x's chain at motion time) but they migrate (positional decay →
  variation analysis, NOT claimed here).
D5. Rank and termination: each step moves to a strictly earlier access (setup s
  < L (causal snapshot: setups are past-only); pusher/ride/train accesses < L
  (past motion); previous root-arrival < current). Rank = current access index,
  strictly decreasing naturals ⇒ terminates in ≤ L steps. Endpoints: (a) a
  nontrivial-A access (banks E1 sited (8S) + K-imprints (8U) + possibly E2/E7:
  CASE-A-like supplied origin —exact supply content: e_A ≥ 1 sited fresh,
  K ⊇ its x-imprints if x-access else path-imprints hitting per E3); or (b) a
  thin origin: T0 (x = T0-root region never touched — then B-deep impossible by
  8T-adjacent unless silent rides, which need trains (their roots imprinted at
  motion (positional!))) / trivial setup (E4 empty; continue past it per D3) /
  silent-ride-only rebuilding (no imprints; W/transient-only cover).
Residual (OPEN, handed to HOLE-1/variation, not closed here): supply sufficiency
at thin origins (cap-exhaustion: E4+K thin or empty; E2-hole via DELETE-halves
(8G+C41 bounded: repeat-cycles anchor at run-starts); sterile W (zone/thin);
unchained E7) and contention at supplied origins (caps + cross-x sharing =
routing wall). What C122-DESCENT achieves (Mode A/B): Case B is converted from
"repeat magic" into enumerated origin types (supplied vs thin) with exact
per-origin supply content; the remaining universal is NARROWER than HOLE-1
(thin-origin heavy bursts + supplied-origin contention, not all heavy blocks).
No finite evidence used; no Hall premise; no carry; arbitrary n; present domain
only; real builder graph (abl + hallcore citations); cap arithmetic exact.
Status: PROVED_AUTHOR (structural descent + classification; supply sufficiency
at thin origins explicitly OPEN).
