# IAGS-11G-S03-COREK — Universal Cycle-Core and Synchronized Boundary-Kernel Theorem

Mission: parent-Box subordinate reduction (no new pipeline; no M1/M2/M3 work).
Entry HEAD `c814d4b` (verified on `coarse-double-branch`; no other changes).
Method: source-exact proof only. No solvers, code/graph/budget changes, no
new stages. Inherits parent-Box reconstruction, M-series/IAGS reports,
Steps 01/02, DH-01/CORE-01 with exact scope (monotonicity gap retained,
never used). Verdict: **OUTCOME A — FULL CYCLE-CORE REDUCTION PROVED**
(see §T; Step 03 itself stays OPEN).

## A. Checkpoint and frozen contract

R1-T/R2/R3/R4 preserved: `NonNegCycles(Ĝ⋆)` target; `G⋆ = G_AF`;
`w_L = 2H−q_L`; `E^H_w(s,t) ⟺ ∃m(E^OM_w ∧ E^MO_0)` with shared midpoint;
`h = 2`, `T = 266`, Int-exact, frozen coordinates/interfaces; no Step 04;
Bank25 = 25. Read authoritatively: freeze/dependency plan, parent
reconstruction, M2 B-projection (B-only equivalence, uniform fixed-shadow
lift), WS-02H normal form (root-`x`, conditional NULLB suffix, `x`/`v`
independence, low-continuation iff `x == v`), `STRICT_LOW_COMPILER`,
`STRICT_HIGH_COMPILER` (90 lines, full read), `CW_PRODUCT_COMPILER`
(OM hides QO2, MO hides QO, MO weight 0, `q == 6−w` on OM),
`S03_EDGE_PROJECTIONS` (project = top-level EXISTS over non-interface vars;
membership-preserving both directions), G01/G02/G03/G03F/DH-01/CORE records.

## B. IAGS Box

`T`: weight-preserving reduction of closed-walk analysis to synchronized
marked-root states and an anchored boundary kernel. `C`: (1) destination
marked-root theorem; (2) cycle localization to `R`; (3) valid retraction
`ρ:R → D`; (4) high reattachment through projected OM/MO; (5) low identity
on the core; (6) universal weighted retraction; (7) boundary-kernel
equivalence; (8) high-only exception elimination via `F`. `I`: §A sources.
`U`: whether reattachment/retraction hold universally. `β`: destination
roots ⇒ localization ⇒ retraction ⇒ kernel equivalence (each proved below).

## C. State, sector, marked-root sets (PROVED definitions)

Fix sector `(μ,σ)`. `r_B(s) = b.root`; `r_A(s) = aI[0]` if `aS[0]=1` else `⊥`.
`R = {s : r_A ∈ M_μ ∧ r_B ∈ M_μ}` (hence B-root always core `<9`;
A-root always S-marked). `D = {s ∈ R : r_A = r_B}` (numerical slot/index
equality for core slots; implies label agreement). `D ⊆ R ⊆ V`; full
validity, intervals, non-root shadow, signatures retained in every vertex
— labels never substitute for states. Sectors preserved per edge
(mu/sig equalities in both compilers), so closed walks never leave them.

## D. Universal destination marked-root theorem (PROVED)

Low: terminal KEEP is unconditionally genuine; target-to-root both sides;
`same_keep_target` S-branch; shadow-match at exit ⇒ `t.b.root = x`
(core), `t.aS[0] = 1`, `t.aI[0] = x` with `x` marked ⇒ `t ∈ D`
(M1 result, hypotheses re-verified against the frozen conjuncts).
High: terminal B-target core marked (`tt < 9` + `mu`-marked), splay root
theorem gives `g.b.root = x`; destination copies B (`t.b == g.b`) and takes
fiber label `v` (`t.aS[0] = 1`, `t.aI[0] = v`, `marked(v)`) ⇒ `t ∈ R`
(no `x = v` required or claimed). Gate A holds for every contracted edge.

## E. Closed-walk localization to R (PROVED)

Every vertex of a nonempty closed walk is some edge's destination;
by §D all lie in `R`. Hence `ClosedWalkWeights(Ĝ⋆) = ClosedWalkWeights(Ĝ⋆[R])`
as sets (forward: restriction; reverse: induced-subgraph walks are walks).
Root-label pairs per cyclic vertex ≤ 25 — recorded as non-reduction (full
states, B-topology, intervals, shadow, signatures all retained).

## F. Synchronizing retraction (PROVED valid)

`ρ(s)`: same `μ,b,σ,α`-except-`aS[0]=1, aI[0]=b.root`. For `s ∈ R`,
`b.root < 9` is marked-core, so `ρ(s) ∈ D`; idempotent; full-state
`b`-equality (incl. `lo`/`hi`) preserved; non-root shadow untouched.
Validity: `state_valid7` constrains only `ak<3`, `aI<9`, mu/sig/b-validity
— all preserved (α-kind/signature/B untouched; new `aI[0]` < 9);
`b_tree_valid` sees unchanged B/sig (existential `bpar`/`bdep` reused);
no inventory/compat conjuncts exist in either compiler. No vertex is
modified except its A-root label, and edges are replaced (never
pretended identical) in §H.

## G. Low-edge identity on the core (PROVED)

For `E_L(s,t,w)` with `s,t ∈ R`: unconditional entry sync
(`s.aS[0]`, core B-root, `s.aI[0] == b.root`) plus `R`-markedness forces
`s ∈ D`; destination always `∈ D` (§D). Hence `ρ = id` on both endpoints;
same witness, same weight, no reconstruction. Non-`R` low edges untouched
(they never occur as closed-walk vertices, but remain in the graph).

## H. High-edge shadow reattachment (PROVED — decisive gate)

Claim: `E^H_w(s,t)`, `s,t ∈ R` ⟹ `E^H_w(ρ(s),ρ(t))`, same `w`, via rebound
midpoint `m' = (μ,σ,g.b,x)` with `x` = B-root (marked core target by
WS-02H root theorem). OM leg: `ρ(s)` keeps `s.b/mu/sig`; the B-witness,
replay, `diff`, target, `q` transfer verbatim (s.α appears only in
`state_valid7` bounds, preserved); the existentially hidden destination is
rebuilt by copying the original t-hidden state and setting only
`t.aI[0] := x` (satisfies bounds, `t.aS[0]`, `t.aI[0] == g.v'`,
`marked(x)`, full validity with reused BStruct assignments).
MO leg: reuse the original hidden ordinary source *verbatim* (its conjuncts
never mention `g.v` or `t`); `ρ(t)` satisfies the destination side because
`ρ(t).aI[0] = x = g.v'`, `ρ(t).aS[0] = 1`, `marked(x)`, B/mu/sig preserved.
Same midpoint `m'` on both legs (`μ/σ/B` shared; `v' = x` shared). No
α-replay, root-termination, or low-sync imported; no detour/`w_H = −3`
exclusion assumed; multigraph-safe (per-occurrence witnesses, no collapsing).

## I. Universal weighted retraction (PROVED)

For every original edge with endpoints in `R`, §G (low, identity) or §H
(high, rebound witness) yields an original edge `ρ(s) → ρ(t)` of identical
weight. Hence every closed walk maps to a closed `D`-walk of identical
total weight (`ρ` single-valued ⇒ `s_n = s_0` gives `ρ(s_n) = ρ(s_0)`),
and every `D`-walk is already a graph walk: `ClosedWalkWeights(Ĝ⋆) =
ClosedWalkWeights(Ĝ⋆[D])`, so `NegCycle(Ĝ⋆) ⟺ NegCycle(Ĝ⋆[D])`.

## J. Anchored boundary kernel (PROVED, F-independent baseline included)

`K_D`: G1 = all original low OO edges with endpoints in `D` (weights kept);
G2 = high-only `D → … → D` first-return excursions (strict intermediates
outside `D`; length-1 included), weighted by path sums, occurrence-indexed
(parallel edges kept distinct). Forward: negative closed walk ⇒ either
all-high (`G^H` term) or contains a low edge, whose entry lies in `D`
(sync + Gate E localization) — cut at all `D`-visits into single low
edges and maximal high-only `D`-excursions; weights preserved. Reverse:
expand kernel edges to witnessing originals/paths; endpoints match by
construction. So `NegCycle(Ĝ⋆) ⟺ NegCycle(G^H) ∨ NegCycle(K_D)` **without**
assuming §I. With §I, every high-only closed walk retracts into `D` and
decomposes into length-1 G2 edges, subsuming the `G^H` term:
`NegCycle(Ĝ⋆) ⟺ NegCycle(K_D)` and full weight-spectrum equality
`ClosedWalkWeights(Ĝ⋆) = ClosedWalkWeights(Ĝ⋆[D]) = ClosedWalkWeights(K_D)`.

## K. High-only exception elimination (PROVED via retraction)

§I subsumes the M2 `G^H` disjunct: no separate high-only cycle theory is
needed for the global equivalence (the B-only relation remains available
as an interface, its sign problem untouched and unclaimed here).

## L. M1/M2/M3 dependency reconstruction (status)

M1 (fused negatives, `w_L ≥ −2`, zero-weight/adjacency obstructions) and
M2 (B-only equivalence, normal form, `-3` UNKNOWN, no sign law) stand
unchanged and are not used beyond their scopes (low-only results never
applied to high witnesses; B-only lift never used as low-edge projection).
This campaign decides no sign question: M1, M2, M3 remain OPEN;
DH-01/CORE-01B/CORE-01/CL/G03 conditionality untouched.

## M. IAGS R1–R4 audit

R1: the retraction removes every unsynchronized marked-root vertex from
closed-walk analysis weight-preservingly, localizes all closed walks to
five-label synchronized roots, and replaces mixed high/low closure by the
anchored kernel — a genuine domain reduction with proved (not asserted)
bridge equalities; no potential fitted, no circularity
(fitting `R` would be equivalent to the theorem — explicitly refused),
no reserve/charging revival, no sampling. R2: all 14 checks pass — low
sync/`q_L ≤ 4`/fusion used within scope; WS-02H suffix kept conditional;
no monotonicity imported beyond genuine traces; SAT/UNKNOWN/UNSAT
preserved (`-3` open); no EK-normalization of detours; no self-loop
inference (repeats allowed everywhere); parallel/abstract walks retained;
no narrowing. R3: no pipeline/step/bank changes, no source/graph edits,
no new coordinates, no M1/M2/M3 work. R4: every gate PROVED as stated;
kernel sign and `-3` satisfiability explicitly OPEN; no UNKNOWN-as-PASS,
no invented witnesses, no universal sign claimed.

## N. Final verdict: OUTCOME A — FULL CYCLE-CORE REDUCTION PROVED

`ClosedWalkWeights(Ĝ⋆) = ClosedWalkWeights(Ĝ⋆[D]) = ClosedWalkWeights(K_D)`
and `NegCycle(Ĝ⋆) ⟺ NegCycle(K_D)`. This closes the reduction Box only;
Step 03, M1, M2, M3 stay OPEN.

## O. Residual sign obligation and HARD STOP

What remains is exactly the signed analysis of `K_D`/low-only/high-only
walks (unchanged problems, reduced domain). No Step 04, no Bank25 change,
no successor, no Dynamic Optimality inference.

**HARD STOP.**
