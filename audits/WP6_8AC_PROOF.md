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
