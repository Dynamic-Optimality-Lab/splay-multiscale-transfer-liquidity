# IAGS-11G-S03-KD01 — Sign-Relevant Mixed B-Block Closure: High-Shadow Rectangularity Proved, Alternating Equivalence Established, Sign Bridge Absent

Mission: post-COREK subordinate M3-interface Box (no pipeline extension).
Entry HEAD `9000c62` (verified on `coarse-double-branch`; no other changes).
Method: source-exact proof only. No solvers, code/graph/budget changes, no
new stages. Inherits parent-Box, COREK (retraction/equivalence), M1 (fused
negatives, `w_L ≥ −2`, zero-weight admissibility), M2 (B-projection/lifting,
normal form, `-3` UNKNOWN), WS-02A–H (reserves/charging failed and abandoned).
Verdict: **OUTCOME F — NO SIGN LEVERAGE** (structural theorems proved;
quantitative bridge absent; see §Q).

## A. Checkpoint and freeze

R1-T/R2/R3/R4 preserved: `NonNegCycles(Ĝ⋆)` target; `G⋆ = G_AF`;
`w_L = 2H − q_L`, `w_H = 6 − q_H`; no `q`-normalization, no source-history
concatenation, no new coordinates/observables; Bank25 = 25; Step 04
unauthorized. Read authoritatively: freeze/dependency plan, parent
reconstruction, COREK/M1/M2/P19 reports, WS-02A–H (scope-kept), both
compilers, product/projections, G01 contraction.

## B. IAGS Box

`T_KD01`: sign-relevant mixed-cycle theorem via rectangularity +
alternating-block composition (or certified countercertificate).
`C_KD01`: exact rectangularity; low-run projection; bidirectional block
lifting; signed accounting; quantitative bridge; stress/minimal-cycle audit.
`I_KD01`: §A sources. `U_KD01`: whether B-block structure bounds signed
credit. `β_KD01`: rectangularity ⇒ block representation (PROVED, §§D–G)
⇒ signed restriction (NOT FOUND, §§J–L).

## C. Inherited results (scope-kept)

COREK retraction/equivalence; M2 B-only NegCycle equivalence + uniform
fixed-shadow lift; WS-02H normal form (`root = x` always, conditional
NULLB suffix, `x`/`v` independence, low-continuation iff `x == v`);
`q_H ≤ 9`, `-3` UNKNOWN, `w_H = −4` impossible; fused H = 1 negatives
(`d_A ≤ 2`, `d_B ∈ {6,7,8}`, `w ∈ {−1,−2}`); `w_L ≥ −2` with empty OO
`−4/−3`; zero-weight structural freedom (both sorts); failed
reserve/charging routes (not reopened).

## D. High-edge rectangularity (PROVED)

Fix sector `(μ,σ)`. For marked-root fully-valid `b`, `A_b = {α :
(μ,b,α,σ) ∈ D}` is nonempty (construct: root `(S, slot(b))`, all other
fields any valid values — `state_valid7` bounds only). Claim: for any B-only
high edge `b →^w b'` and any `α ∈ A_b`, `α' ∈ A_{b'}`, the full high edge
`(μ,b,α,σ) →^w (μ,b',α',σ)` exists. Proof: reuse the B-witness verbatim
(`verify_bpath`, splay, `diff`, marked core target, `q`, `w` — none read
`α`); rebuild only the OM hidden destination shadow root to `(S, v)`
with fiber `v := b'.root` (marked core target, satisfies `t.aS[0]`,
`t.aI[0] == v`, `marked(v)`, full validity); s-side needs nothing beyond
`state_valid7` (α-independent); MO reuses its hidden ordinary witness
verbatim while `t` is the interface destination (its constrained fields
all match by construction). No A-replay/sync/shadow-match is assumed —
their absence from `build_shigh` (verified by full read) is exactly what
makes arbitrary-shadow lifting sound. `lo`/`hi` travel with the B-vertex
and satisfy per-vertex validity; `b_equal`'s subset comparison needs no
stale-interval propagation (endpoint validity is re-conjoined).

## E. Arbitrary-endpoint high-path lifting (PROVED)

For B-paths `b_0 → … → b_m` with per-edge valid high witnesses and
marked-root endpoints admitting synchronized shadows (automatic for closed
B-walks, whose vertices are all high destinations with marked core roots):
choose arbitrary `α_0 ∈ A_{b_0}`, `α_m ∈ A_{b_m}`, arbitrary synchronized
intermediates, and lift each edge by §D. Total weight preserved exactly;
no histories concatenated; parallel witnesses independent. Rectangularity
is sign-neutral: it enables negative and nonnegative completions alike.

## F. Exact low-run B projection (DEFINITIONAL, scoped)

`L_u^+(b,b')`: ∃ nonempty low-only path of total weight `u` between
synchronized states with B-endpoints `b,b'`, witnessed by complete
per-edge low witnesses sharing exact full endpoints (A-shadows included).
Fused H = 1 representatives kept where WS-02C applies; H = 2 kept whole
(no single-event reduction claimed); zero-weight edges retained;
`q_L` stays true-depth credit; no independent chaining assumed.

## G. Alternating mixed-cycle equivalence (PROVED, structural only)

Forward: closed mixed walk → maximal low/high runs (low runs keep full
witnesses; high runs project per edge; B-endpoints shared via full states).
Reverse: choose low-run witnesses first (fixing all low endpoint shadows,
which are synchronized-marked: destinations by M1, starts by entry-sync
against marked B-roots); connect each high block between the now-fixed
endpoint shadows via §E. Cyclic closure holds exactly (B returns by block
definition; shadows by Gate-E construction; `μ/σ` sector-fixed). Hence
`NegMixedCycle(Ĝ⋆) ⟺ NegAlternatingCycle(L^+, H^+)` weight-preservingly.
This is a representation theorem: it organizes but does not bound.

## H. Signed block accounting (ARITHMETIC ONLY, explicitly not a proof)

`w(C) = 2A_L + 6N_H − Q_L − Q_H` holds by definition. The required
`Q_L + Q_H ≤ 2A_L + 6N_H` is the M3 target restated, not derived. No
per-block signed inequality follows from §§D–G.

## I. Source-derived quantitative bridge candidates (all REFUTED as routes)

Return-path lower bounds: unproved (zero-weight/adjacent completions
admissible; WS-02G verdict stands). Marked-root sequence laws: no
weight-relevant restriction (roots must change per genuine terminal, but
no sign follows; alternation free). B-topology restoration: closure is
exact but weight-free (rotations rebuild topology at arbitrary declared
`q`). Two-block exclusion (`L:b→b'`, `H:b'→b`, `w(L)+w(H) ≥ 0`): unproved —
`q_H = 9` returns remain satisfiable in principle (P19 compatibility,
UNKNOWN preserved). Signed functionals: no per-block law derivable without
reinstating failed reserves (explicitly not done). Finite-state/lexicographic
arguments: rejected as sign proofs (finiteness never bounds sums).

## J. Chosen mechanism and proof: NONE (first obstruction stated)

No mechanism in §I.1–6 yields a signed law from frozen predicates. The
precise obstruction: rectangularity removes shadow-compatibility as an
obstacle but imposes no credit discipline — declared `q_H` stays
witness-free up to endpoint validity, low deficits stay fused-local, and
zero-weight transitions bridge every structural gap for free. The bridge
`B-block structure ⇒ signed restriction` has no source-derived instance.

## K. Zero-weight and negative-adjacency stress test (CONFIRMS F)

Low `(1,2)/(2,4)` and high `q_H = 6` zero-weight edges can move B-roots,
rewrite A-shadows, shift marked depths, re-prime negatives, and repeat —
all admissibly, all weightlessly. Negative low blocks adjacent to negative
high blocks (and to further negatives via distinct targets) are
unobstructed; `q_H = 9` detours and sentinel mechanics persist unchanged;
full B-closure (root/fields/intervals) is satisfiable in principle with no
forced sign; cyclic repetition adds no constraint. Every candidate law
fails here first.

## L. Minimal negative-cycle analysis (no leverage)

Simple-cycle reduction holds (G03F); self-loops excluded (genuine `diff`
forces B-change, so no edge fixes its endpoints — the only universal
exclusion found, weight-blind and insufficient per R1). No structural
consequence of minimality (length, negativity count, witness complexity)
restricts signs: dropping or merging blocks changes weights/endpoints and
is not validity-preserving in general.

## M. Universal or partial signed conclusion: NONE (OPEN, unchanged)

No `Σ(2H−q_L) + Σ(6−q_H) ≥ 0` theorem, no excluded negative mixed family,
no return bound, no decomposition with established signs follows from
§§D–L. M3 remains exactly where COREK/M2 left it.

## N. Countercertificate audit: NONE (correctly withheld)

No complete valid negative mixed closed walk exhibited (would require full
states, all witnesses, midpoint sharing, exact closure, strictly negative
total — not constructible here; no solvers authorized). Admissibility
arguments are not witnesses. The frozen sign premise stands unrefuted.

## O. M1/M2/M3 dependency implications

M1 untouched (low-only sign open; fused-deficit compensation missing).
M2 untouched (B-only equivalence and normal form stand; high-only sign
open). M3: alternating representation proved (§G) but sign-neutral; no
M3 obligation discharged. Step 03 OPEN.

## P. R1–R4 audit

R1: Gates D–G prove genuine structural theorems (rectangularity with
arbitrary endpoints, alternating equivalence with exact closure), but per
R1's explicit list these do not qualify as sign-relevant outcomes — and
correctly so, since Gate F finds no quantitative bridge and Gate K
confirms every candidate fails on zero-weight/adjacency grounds. Outcome
F, not B: no new signed restriction, no excluded negative family, no
reduced residual sign problem — only a cleaner representation of the same
open question. No reserves revived, no potentials fitted, no circular
matching, no sampled-cycle claims. R2: all 15 safeguards hold —
rectangularity proved (not inferred) for arbitrary synchronized shadows;
low runs share full endpoints (never projected-then-assumed-chained);
high paths use only source-valid B-edges; `q` untouched both sorts;
`-3` UNKNOWN preserved; no root-termination/no-repeat imported into high;
zero-weight retained; masks/signatures/B-intervals/parallel/abstract
cases covered; hidden witnesses strictly per-edge; no H1/H2/H3 import.
R3: no pipeline/graph/coordinate/weight/q/mask/signature changes, no
M1/M2/M3 work, no KD02, no Step 04, Bank25 = 25. R4: structural gates
PROVED; sign bridge OPEN (proved absent as a consequence of the predicates,
not merely unattempted); no UNKNOWN-as-PASS; no SAT-by-compatibilism;
no promotion.

## Q. Final verdict: OUTCOME F — NO SIGN LEVERAGE

Rectangularity + alternating-block equivalence are real, proved, and
preserved — and they do not constrain signed weights: every sign-relevant
question (return bounds, deficit repayment, negative-family exclusion,
countercertificate) is exactly as open as before, with zero-weight and
adjacency freedom identified as the precise, already-known obstructions.
No successor spawned.

## R. Residual Step 03 obligations (unchanged)

M1 (low-only sign), M2 (high-only sign incl. `-3`), M3 (mixed sign):
all OPEN. Fused H = 1 deficits, anomalous excess credit, and zero-weight
bridging remain the irreducible content.

## S. HARD STOP

No Step 04. No Bank25 change. No Dynamic Optimality inference.
No further Box authorized.
