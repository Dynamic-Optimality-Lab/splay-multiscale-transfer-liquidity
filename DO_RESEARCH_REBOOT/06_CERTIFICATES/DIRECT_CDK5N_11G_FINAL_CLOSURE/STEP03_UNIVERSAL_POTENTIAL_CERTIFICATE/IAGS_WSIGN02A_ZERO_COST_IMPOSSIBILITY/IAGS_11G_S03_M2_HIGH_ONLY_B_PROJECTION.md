# IAGS-11G-S03-M2 — High-Only B-Projection and Exact Cycle Lifting

Mission: M2 obligation under Step 03 parent Box (no pipeline extension).
Entry HEAD `cca64d1` (verified on `coarse-double-branch`; no other changes).
Method: source-exact proof only. No solvers, no code/graph changes, no new
stages. Inherits parent-Box reconstruction, WS-02H normal form, Steps 01/02,
DH-01/CORE-01 with exact scopes (monotonicity gap retained, not reopened).
Verdict: **OUTCOME B — NEW HIGH-LEVERAGE B-ONLY THEOREM, SIGN OPEN**
(see §O; R1–R4 audit in §N).

## A. Checkpoint and frozen graph contract

R1-T/R2/R3/R4 preserved: Step-03 target `NonNegCycles(Ĝ⋆)` unchanged;
`w_L = 2H−q_L`, `w_H = 6−q_H`; `E^H_w(s,t) ⟺ ∃m(E^OM_w ∧ E^MO_0)` with shared
midpoint; no repairs, narrowing, new coordinates, solver use, or Step-04.
High-only sector `G^H_{μ,σ}` is a proof partition, not a graph restriction;
`μ_s = μ_t`, `σ_s = σ_t` per edge follows directly from the ten `EQ`
conjuncts plus `s.mu = g.mu = t.mu` (`build_shigh`), so high-only walks
stay in-sector. Ordinary state `s = (μ,b,α,σ)` kept whole everywhere.

## B. IAGS Box B_M2

`T_M2`: high-only sign via exact B-only reduction (prove or refute).
`C_M2`: B-only relation; sound forward projection; weight-preserving reverse
lifting; endpoint preservation; excess-credit characterization; sign
certificate or valid counterexample; transfer back. `I_M2`: Steps 01/02,
parent reconstruction (`w_L ≥ −2` OO empties `−4/−3`), WS-02H normal form
(root `x`, NULLB-suffix conditional, `x`/`v` independence, low-continuation
iff `x == v`), exact contraction, DH-01/CORE-01 with gaps retained.
`U_M2`: B-only closed cycles vs declared-credit accumulation; A-shadow
removal vs cycle-language preservation. `β_M2`: `NegCycle(G^H) ⟺
NegCycle(H^B)` — proved in §H, then used (not assumed) in §§K–L.

## C. Exact high-edge source interface (PROVED from full read)

`build_shigh` (90 lines) conjoins: full `b_valid` + `b_tree_valid` on
`s.b`, `t.b`, `g.b`; `popcount5(g.mu)`; `g.v < 9`; mu/sig equalities;
`t.b == g.b` (`b_equal` on root+`kl/rl/kr/rr`); `t.aS[0]`;
`t.aI[0] == g.v`; `marked(g.v)`; `verify_bpath(s.b)` (hence `bd ≤ 18`);
`bs1 = splay(s.b)`; `bs1 == g.b`; genuine `diff`; core marked target
(`bT < 9`, marked via `s.mu`); `q ≤ 9`, `2q ≤ bd < 2q+2`; `w1 = 6−q`.
Absent (verified): A-replay, H-charge, sync, `root_terminated`,
no-repeat, `same_keep_target`, shadow-match, and — critically — any
`EQ(bt.bT[0], g.v)`. Hence: B-target `x` vs fiber label `v` independent
(both marked core); A-shadow constrained only by `state_valid7` bounds +
root label `v`; B-witness independent of `α` except through sector
`(μ,σ)`. No low-style sync or A/B coupling may be imported.

## D. A-shadow independence and fiber-label audit (PROVED)

A-shadow vars occur only in bounds + `t`-root-label conjuncts; B-witness
vars (`bT/bd/bpath/bdir`) only in path/splay/`q`/marked-target conjuncts;
the sole cross-constraint is `t.aI[0] == g.v` (α-to-fiber, never α-to-B),
and fiber-to-B has none (`v` free of `x`). Fixed sector `(μ,σ)`:
`ω`-style weights unneeded — elimination is by independence, not fitting.
`lo`/`hi` warning resolved: they are per-vertex data constrained by each
state's own `b_valid`/tree-validity; `b_equal`'s subset comparison is sound
because `g.b`'s intervals get fresh validity constraints (the splay's stale
`lo`/`hi`, carried from `s.b` by `_clone`, never leak into `g.b`).
B-states are fully valid at every high endpoint (conjoined on `s.b`,
`t.b`, `g.b`).

## E. Full B-state projection definition (PROVED well-formed)

`V(H^B_{μ,σ})` = fully valid BStates (`b_valid` + full `b_tree_valid`;
both conjoined at high endpoints, so no vertex leaves the domain).
`H^B_{μ,σ,w}(b,b')` ⟺ ∃ witness (marked core target, path/dirs,
`bd ≤ 18`, `verify_bpath`, splay `== b'`, genuine `diff`, `q ≤ 9`,
`2q ≤ bd < 2q+2`, `w = 6−q`) — i.e. the OM leg's B-content with sector
fixed, A/fiber/MO data eliminated as irrelevant (MO is B-identical,
weight-0 relabeling; fiber label constrains only `α`). No new coordinates;
no witness class dropped (detour suffixes, fringe-free targets all
admissible where satisfiable).

## F. Forward projection theorem (PROVED)

Every contracted-high edge projects: `s →_H^w t` with witness ⇒
`b_s →^w_{H^B} b_t` with the same witness, weight, sector, validity, and
midpoint provenance (existential elimination; `q`/`w` unchanged).
Endpoint B-states are fully valid by §C; root is the marked target
(WS-02H last-prim theorem, independent of suffix shape).

## G. Uniform fixed-shadow realization (PROVED — the decisive lemma)

Fix sector `(μ,σ)`, marked `v⋆ ∈ M_μ`, and one `α⋆` with `aS[0]=1`,
`aI[0]=v⋆` (other positions any `state_valid7`-legal values). Claim: EVERY
`H^B` edge lifts to a full high edge on identical `(α⋆,v⋆)`. Proof: reuse
the B-witness; set fiber `v = v⋆`, `g = (μ,σ,b',v⋆)`,
`s = t = (μ,·,α⋆,σ)` with respective B's. All §C conjuncts check:
state-validity (endpoints valid by definition; `α⋆` legal by construction);
mu/sig equalities (sector constant); `t.aS[0]`, `t.aI[0]=v⋆=g.v`, marked
`✓`; path/splay/diff/target/`q`/`w` (witness verbatim). No per-edge shadow
choice is needed — the A-side is too loose to obstruct any B-transition.
In particular this is NOT silent per-edge shadow-switching: one shadow
works for all edges simultaneously.

## H. Bidirectional closed-walk lifting (PROVED)

B-only closed walk `(b_0 → … → b_n = b_0, same weights)` lifts via §G to
`s_i = (μ,b_i,α⋆,σ)` with the same witnesses/weights; `s_n = s_0` exactly
(full B equality incl. `lo`/`hi` + shared `α⋆`/sector); each edge keeps its
own midpoint (sharing required only within edges). Hence, as sets of
attainable total weights:
`ClosedWalkWeights(G^H_{μ,σ}) = ClosedWalkWeights(H^B_{μ,σ})`, and therefore
`NegCycle(G^H) ⟺ NegCycle(H^B)` per sector. Lifting never concatenates
hidden histories (each edge reuses its own witness); closure is by shared
exact vertices, valid for nonprimitive and abstract-only walks.

## I. Exact high-only weight preservation (PROVED corollary)

Weights ride entirely on the B-witness (`w = 6−q_H`); MO contributes 0.
The equivalence preserves every edge weight, so B-only sign analysis is
faithful: high-only nonnegativity ⟺ B-only nonnegativity sector-wise.
Remaining B-only problem, exactly: `Σq_H ≤ 6n` over B-splay witnesses
(`q = ⌊d/2⌋`, `d ≤ 18`, root always marked core, endpoints fully valid).

## J. Canonical and excess-credit B-transition normal forms (restated scope)

WS-02H applies verbatim in B-only language: true chain (`h ≤ 8`,
core-only) + forced `path[h+1] = NULLB` + conditional tail (no universal
all-NULLB claim — detours via kind-0 `19`-claims admissible where
side/static-order conjuncts allow); last-prim root theorem
(`root = x` for every genuine witness, `d ≥ 1` forced by `diff`);
slot-0 aliasing for sentinel reads, selective real writes, transient
sentinel roots never surviving endpoint validity. No new restriction on
successive B-targets is derived: `x_{i+1}` ranges freely over its entry
tree (root `x_i`), and each edge witnesses independently — reported, not
disguised.

## K. Universal B-only sign theorem: OPEN (residual precisely stated)

No per-edge bound beyond `q_H ≤ 9` exists (declared depth is
witness-chosen up to 18; validity constrains shape, not credit).
Candidate levers examined and found insufficient: root-always-marked
(uniform, no weight content); successive-target structure (free);
core-membership constancy (conditional on unproved excess-prim
monotonicity — WS-02H audit stands, DH-01 dependency unchanged);
finite B-state space (bounds lengths, not weights); self-loops excluded
(`diff` forbids fixed points — PROVED, but one-vertex only). The exact
residual: `Σq_H ≤ 6n` over B-only closed walks, with no derived
telescoping, counting, or exclusion law. Not promoted, not refuted.

## L. Negative B-cycle construction: NOT PROVED (correctly refused)

A 2-cycle with `q_0+q_1 > 12` (or longer analogues) is structurally
admissible in principle (no conjunct forbids the required trees/paths/
validity), but hand-construction of a complete valid witness pair —
full 19-slot states, parent/side/static-order checks, rotation outcomes,
endpoint validity, fiber compatibility — cannot be certified without
computation (no solvers authorized). No partial path, trace, or
satisfiability verdict is promoted to a countercertificate. The
`w_H = −3` UNKNOWN (`bd = 18` necessary) is preserved exactly.

## M. Source-level monotonicity and historical dependency audit

CORE-01 R1–R3 micro-lemmas require path-node operands with marked ancestry
— satisfied by genuine-trace prims, not by excess-trace sentinel/detour
prims; high-edge `C`-monotonicity therefore covers canonical traces only,
and DH-01's constancy/`q`-average program inherits exactly that scope
(no regression, no extension). G03F return-path equivalence holds
independently (pure graph theory) and is the route by which any future
return bound would lift — none derived here. SAT/UNKNOWN/UNSAT ledger
(`−4` impossible by source proof; `−3` UNKNOWN; rest as recorded) untouched.

## N. IAGS R1–R4 audit

R1: the B-only cycle equivalence (§§E–H) removes A-shadow reconstruction,
fiber labels, midpoint sharing, and the MO leg from every high-only
closure obligation — a proved domain reduction with the residual
complexity stated honestly (§K: B-only sign over splay witnesses).
It is not mere notation: uniform fixed-shadow lifting (§G) is the
nontrivial content (per-edge shadows would not close walks). No reserve,
potential, matching, or fitted claim is made. R2: every inheritance
checked — WS-02H root/suffix/interface used within proved scope;
DH-01/CORE-01 conditionality preserved; ledger statuses preserved;
no existential freedom converted to universal freedom (detours stay
conditional; `v⋆`/`α⋆` choices are existential constructions inside the
proof, not universal claims). R3: no pipeline/stage/step-04/M1/M3 work, no
repairs, no new coordinates, no narrowing (all detours/fringe/abstract
walks retained), no searches/solvers/budgets. R4: lifting/equivalence
PROVED; sign/counterexample OPEN (explicitly not promoted); detour
universality REFUTED-as-stated (conditional form proved instead);
no UNKNOWN-as-PASS, no invented witnesses, no sampled-cycle claims.

## O. Final verdict: OUTCOME B — NEW HIGH-LEVERAGE B-ONLY THEOREM

The exact weight-preserving B-only cycle equivalence is proved and
removes the A-shadow/fiber/midpoint dimensions from high-only closure.
The high-only sign (`Σq_H ≤ 6n`) and any countercertificate remain OPEN;
the residual is precisely stated (§K) with all failed/sufficient
alternatives documented (§§J–M).

## P. Residual M1/M2/M3 status and HARD STOP

M1 (fused low deficit compensation): OPEN, untouched. M2: B-only
equivalence PROVED; high-only sign OPEN (residual above). M3 (mixed
integration): OPEN, untouched (continuation-forcing from WS-02H stands
as the only mixed structural law; no weight bridge claimed). Bank25 = 25.
No WS-02I, no Step 04, no Dynamic Optimality inference.

**HARD STOP.**
