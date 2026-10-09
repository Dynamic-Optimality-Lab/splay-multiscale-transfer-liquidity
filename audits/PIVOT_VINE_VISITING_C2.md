# PIVOT-10A: VINE-VISITING-C2 (conditional universal theorem)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Target: for every closed
walk visiting vine-pairs, B <= 2A, via `sum_E r_E <= A_vine`.

## 1. The 9 residual-+1 structural classes (§2)
All share ONE structural signature (order-symmetric twins counted once):
- Start: differ-vine-pair with an A-rooted key x of large B-depth.
- Exit: KEEP x with (a,b) = (0,3) (A frozen/stays vine; B splays deep,
  branches, leaves vine). n=6: B-depth 5; n=7 sole case: B-depth 6.
- Middle: 1-3 all-KEEP accesses, every one (a,b) = (1,2) (W-neutral:
  B-2A = 0 each), staying non-vine.
- Re-entry: KEEP z with (a,b) = (1,1) (double-shallow), landing twin-vine.
- Totals: (A,B) = (2,6) [n=6, 8 cases: words K1,K5,K6 and mirror K6,K2,K1]
  and (4,10) [n=7, 1 case: K1,K2,K7,K3,K1]. Always W=+2, tau 1->0, r=+1.
- Anatomy of surplus: exit (+3) + middles (0) + re-entry (-1) = +2;
  boundary charge (+1) absorbs one; residual +1 remains.
No literal-word lemma is used downstream; only this signature
(A-rooted deep exit + neutral middles + (1,1) twin re-entry).

## 2. Universal hypotheses (all load-bearing; status after hunt)
- D1 (r_E <= +1, all excursions, all n): finite-exact on shortest
  (n=6: max +1 over 9,600; n=7: max +1 over 46,592); DFS non-shortest
  n=6 sampled (no r>=2 in ~8M expansions); steered large-n (n=8..20,
  ~12k trials: max r = -8). UNPROVED universally.
- F1 (r=+1 ==> end twin): finite 9/9; steered: no end-differ +1 found.
  UNPROVED.
- F2 (r=+1 ==> start differ): finite 9/9; steered twin-start max r = -8
  (far from +1). UNPROVED.
- R0/H4 (twin-start AND r=0 ==> end twin): finite-exact n=6 (56/56) and
  n=7 (72/72); steered: no twin-start r>=0 found at large n. UNPROVED.
- Banked: V1 (n>=5), StepEv/depth cost agreement, open-vine law
  (B-A <= tau(s)-tau(t), per-edge + telescope), residual equation
  (W_2 = SUM r_E - A_vine), T1 (non-trivial vine from twin has A>=1:
  Lean `twin_exit_A` + (0,0)-loops + V1 costs), rho<=5/3 global (n<=6).
- Falsification hunt (r>=2, twin-start +1, twin->differ r=0 at n=8..20):
  all negative. No refutation; no proof.

## 3. Debt-machine theorem (CONDITIONAL PROOF)
CLAIM: every closed vine-visiting walk (n>=5) satisfying D1,F1,F2,R0 has
W_2 <= 0. (n<=4: global rho certs, stronger; n=5,6: rho certs. The
conditional is needed only at n>=7.)
Debt d in {0,1}; invariant: d=1 ==> current position twin (base d=0).
Process V/E segments cyclically. r values are integers; non-+1 means r<=0
(D1). Twin-bit tau=[differ].
- +1 excursion E (starts differ [F2], ends twin [F1]): arrival needs d=0
  (d=1 ==> twin-position, but E starts differ). Set d:=1. Contributes +1.
- r=0 excursion: contributes 0. With d=1 (at twin): starts twin ==>
  ends twin (R0): invariant preserved. With d=0: anything.
- r<=-1 excursion: contributes <=-1. With d=1: d:=0 (joint with
  outstanding +1 is <= 0). With d=0: negative leftover.
- Vine V (contributes W_2(V)-c_V <= -A(V), open law): with d=1 (at twin):
  non-trivial ==> A>=1 (T1) ==> contribution <=-1, pays outstanding +1,
  d:=0. Trivial ((0,0)-loops, stays) ==> contributes 0, d stays.
  With d=0: contributes <=-A <= 0.
- First-differ-reaching lemma: from twin-land, reaching a differ state
  requires a payer (A>=1-vine [T1: non-trivial from twin] or r<=-1
  excursion [twin-start: +1 impossible by F2, r=0-twin->differ impossible
  by R0, D1 caps at +1, so r<=-1]). Used for closure forcing below.
Pairing (canonical, disjoint; each +1 in exactly one pair, joint <= 0):
- Walk-start DIFFER: every +1 is cleared forward (walk must return to the
  differ start; reaching it needs a payer). Pair each +1 C_i with its FIRST
  clearing forward P_i. P_i lies strictly between C_i and C_{i+1} (C_{i+1}
  needs d=0, first established at P_i; types differ so segments are
  distinct); the k open intervals are disjoint ==> P_i pairwise distinct.
- Walk-start TWIN (with >=1 +1): let P_0 be the first-differ-reaching payer
  (exists: +1-starts are differ). Pair C_1..C_{k-1} forward as above, and
  pair the last +1 C_k with P_0 (P_0 <= -1 with C_k +1 sums <= 0; P_0 is
  strictly before C_1 hence distinct from all forward clearings; if C_k
  also clears forward, that clearing is an unpaired negative leftover).
  If no +1s, no pairing needed.
Unpaired leftovers (r<=0 excursions, r=0, trivial/A=0 vines, extra
A>=1-vines/r<=-1 at d=0, (0,1)-hops inside vine terms) are all <= 0.
Total <= 0. QED (conditional).
No injection choices, no sharing pathology (debt-bit holds at most one
outstanding +1: a second +1 needs differ-start while debt forces twin
position, by F2+invariant). No word-specificity. No Bellman/future values
(pure finite-state counting on the walk).

## 4. Lean status (§16/H)
`twin_exit_A` (T1 edge core: twin-start A-cost-0 ==> B-cost-0) added to
GCStaticVine.lean, green exit 0. `vine_path_bound` preserved unchanged.
Full debt-machine formalization needs walk infrastructure (segment lists
+ telescope + debt invariant) and is queued, not blocking; human proof
above is the authority.

## 5. Endpoints
VINE-VISITING-C2: CONDITIONAL SUCCESS (debt-machine, hypotheses
D1/F1/F2/R0 open universally, finite+steered supported, T1/V1 banked).
Per §17 the proof passes through sum r_E <= A_vine (equivalent form of
total <= 0). Per §18 NO global claim (5/3 non-vine-only chamber remains;
next campaign: C.ZIG ownership + persistent-branch accounting).
Failure endpoint (§19) not triggered (no counterexample, no unpayable
local config found; nearest miss is the 9 residual-+1 types, all paid
conditionally). GC/Hall/R3 unvisited. Zero kills (conditional proof).

## 6. AMENDMENT (PIVOT-10B refutation): debt-machine route CLOSED
D1 (r<=+1) is REFUTED: n=32 sweep-return excursion (K1+K1..K32 from
(inc-vine, dec-vine)) has W=+9, r=+8, DT class (see
`vine_excursion/refutation_n32.json`, replay sha c7d01179...; smaller
n=20 sibling W=+4/r=+3). Since the machine's "non-+1 ==> r<=0" step needs
D1, and residuals reach +8 (growing ~n/4 with deep-B exits whose sweep
returns sustain B/A>2), the conditional collapses: hypotheses not merely
open but FALSE in general. VINE-VISITING-C2 returns to OPEN (no proof
route currently). Unaffected: Lean kernels (all true proved statements),
PIVOT-9 vine B<=A, n<=6 rho certs, C.ZIG, E4b (witness satisfies B<=3A),
global B<=2A itself (witness is open; rho->2 pattern stands). The precise
loss: uniform residual cap (+1) and any fixed-residual charging; next
routes must bound exit-minus-return jointly per excursion.
