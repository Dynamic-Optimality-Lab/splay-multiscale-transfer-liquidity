# IAGS-WS-02G — Negative-Edge Recurrence and Walk-Level Charging: Readiness, Recurrence Bounds, and the Zero-Weight Obstruction

Mission: `IAGS-WS-02G-...`, entry HEAD `55a4efd` (verified on
`coarse-double-branch`; no other changes made).
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source/graph changes. Inherits WS-02A (PROVED), WS-02B (OUTCOME A),
WS-02C (OUTCOME B), WS-02D (OUTCOME A), WS-02E (OUTCOME B), WS-02F
(OUTCOME F) with exact scope; WS-02F's abandoned reserve assumptions are not
revived, its valid identities are reused as lemmas.
Verdict: **OUTCOME F — RECURRENCE ROUTE FAILED** (see §N for the exact
obstruction; valid partial theorems retained in §§C–F).

## A. Frozen theorem and inherited results

Target: `∀C closed in Ĝ⋆, w(C) ≥ 0` (unchanged; this campaign settles a
sub-Box only). Inherited: every low edge has `1 ≤ H ≤ 2` with `q ≤ 4`
(02A/02D; terminal always genuine); zero-cost B-changers need charged
DELETEs, injectively attributed (02B); H = 1 edges fuse to a single marked
KEEP preserving endpoints/charge/credit/weight, with `q = ⌊depth_{B_s}(x)/2⌋`
and entry-A-depth 1–2 (02C); rotation write-locality, per-prim gates,
triple-sum invariance, sign-indefinite transfer `Δ = |S| − |L|`
(02E, with 02F's marked correction
`ΔD_M = |S∩M| − |L∩M| + 𝟙[p∈M] − 𝟙[x∈M]`); no depth/rank reserve exists
from rotation structure (02F). Negative low edges (fused):
`H = 1`, `d_A ∈ {1,2}`, `d_B ∈ {6,7,8}`, `q ∈ {3,4}`, `w = −δ`, `δ ∈ {1,2}`,
both roots become the marked target `x` (02C fused class; WS-02D's depth-9
allowance concerns multi-event histories only and is not imported).

## B. IAGS Box definition

`T_G`: recurrence/interval-charging theorem constraining fused-negative
deficit accumulation over finite low-edge walks, from actual structural
transformations (first child: exact regeneration restrictions).
`C_G`: (1) graph-visible readiness condition; (2) post-negative readiness
change; (3) recurrence condition; (4) quantitative restoration lower bound;
(5) non-reusable charging; (6) closed-walk bridge. `I_G`: §A plus frozen
interpreters/graph interface. `U_G`: does regeneration force expensive
repayment, or recur through zero-weight/further-negative transitions?
`β_G`: available-positive-weight ≥ total-negative-deficit on closed low-only
walks — required as consequence, never assumed.

## C. Exact graph-visible negative-readiness predicate (PROVED sound)

`Ready_x(s) ⟺ x ∈ M_μ ∧ SyncRoot(s) ∧ Shallow_α(s,x) ∧ 6 ≤ depth_{b_s}(x) ≤ 8`,
where `M_μ` = five marked S-indices under `μ`; `SyncRoot` = canonical root
labels agree (B-root slot, resp. A-root slot via witness tables, WS-02B);
`Shallow_α` = WS-02C predicate (`∃p ∈ {L,R,LL,LR,RL,RR}` kind-0, S,
sidx `= x`); B-depth via kind-0 parent chains (well-defined on edge-endpoint
states by the conjoined one-parent/validity predicates; no ports, absent
slots, or fringe labels count — kind and S-index required). `R(s)` = set of
ready marked keys (function of existing coordinates only).
Soundness (PROVED): a negative edge with target `x` satisfies `Ready_x(s)`
— markedness from the unconditional terminal genuine block; `SyncRoot`
from entry pinning (02B); shallowness from the fused shadow predicate (02C);
depth 6–8 from fused B-immobility + entry gap-childlessness (core-only path,
`d ≤ 8`) + `q ∈ {3,4}`. Fusion preserves endpoints, so soundness transfers
from fused representatives to all H = 1 negatives. Converse not claimed.

## D. Post-negative readiness transformation (PROVED + refuted candidates)

After negative `e: s → t` (target `x`): `B_t.root = A_t.root = x`, so
`depth_{B_t}(x) = 0` and **`x ∉ R(t)`** (PROVED); `Sync(t)` holds with label
`S(x)` (KEEP resynchronization). For `y ≠ x`, no universal nontrivial
restriction is derivable: B-depths shift by sign-indefinite rotation
disturbance (02E/02F), A-depths beyond `α_t` are hidden, and `α_t` itself is
instance-determined. In particular the candidate `|R(t)| ≤ k` for any `k < 4`
is unsupported (refuted as a provable claim — the conjuncts admit
deep-B/shallow-A configurations for other marked keys; the trivial `k = 4`
bound has no leverage). Post-negative state is characterized, not controlled.

## E. Same-key negative recurrence (PROVED necessary conditions, no cost)

`y = x` immediately after `e` is IMPOSSIBLE (depth 0 < 6) — PROVED, but
trivially insufficient per R1. Eventual return needs: (i) B-depth of `x`
back to ≥ 6 — net `+6` via others' splays, each depth-`D` B-splay moving
any key by at most `D` (PROVED displacement lemma: every prim moves any
node by ∈ {−1,0,+1} from the verified ref pattern, `D` prims per WS-02E);
(ii) A-shadow depth of `x` back to 1–2 — requires an actual A-state change
(depth is state-derived), and **A-change forces charge**: an active event
with `A_{i+1} ≠ A_i` fired a prim, so `dd ≥ 1` (gates) and `a ≥ 1`
(PROVED; inactive events are identities). B-side has no such law
(zero-cost Div KEEPs change B freely — the operative asymmetry). But charge
is not weight: the A-returning charge can sit on an edge with `q = 2H`
(zero weight), so (i)+(ii) force H-budget, never positive `w`. No
positive-weight necessity follows.

## F. Different-key negative recurrence (adjacency NOT excluded)

For `y ≠ x`, immediate recurrence at the next edge is admissible in
principle: `Sync` holds automatically at `t`, and no frozen conjunct forbids
a marked `y` from simultaneously sitting at B-depth 6–8 in `B_t` and at
A-depth ≤ 2 in `α_t` (splay disturbance is sign-indefinite, hence can
preserve such configurations; KEEP resynchronization imposes no cross-key
exclusion). So adjacent distinct-target negatives are NOT ruled out —
nonadjacency theorems, and any charging scheme needing gaps between
negatives, fail at this point. Eventual alternation among the four other
marked keys is even less constrained. Cyclic distinct-target sequences are
not excluded by any proved predicate.

## G. Quantitative regeneration-cost theorem: OBSTRUCTION (route-blocking)

No universal positive-weight regeneration law exists within the frozen
predicates. Two independent defeaters: (1) **Zero-weight pushers are
admissible in principle.** Fused H = 1, `q = 2` singles (`d_B ∈ {4,5}`,
`d_A ∈ {1,2}`, `w = 0`) perform real B-splays (displacement ≤ 5 per edge;
H = 2, `q = 4` zero-weight pushers displace ≤ 9) and real A-moves (a charged
DELETE balanced by `q = 2`), so both the B-pushdown and the A-return of §E
can be accomplished at zero signed weight; H = 2 multi-event histories add
more zero-weight avenues. The frozen conjuncts (validity, resync,
attribution) are all compatible with such pushers — nothing forces the
balancing `q` to be small. (2) **Adjacency needs no intervening edge at
all** (§F). Hence regeneration cost in units of `δ` is unprovable: the only
forced currency is A-charge, and charge is weight-free at `q = 2H`.
The §10 stress test resolves against the route. No `δ`-denominated
regeneration inequality is promoted.

## H. Walk-level charging: no mechanism (OPEN, unbuildable here)

With §§F–G, no charging rule satisfies the mission's requirements (1)–(8):
deficit units have no forced positive sources (zero-weight/adjacent
regeneration admissible); capacity/overlap/cyclic-closure analysis is moot
without sources. Visibility would have cooperated — readiness is
endpoint-computable (`b`, `α`, `μ`, labels), so a valid mechanism would have
transported correctly across abstract-only walks without hidden-history
concatenation — but transport of a nonexistent charge is vacuous.
Overlapping-interval capacity, cyclic-rotation invariance, and nonprimitive
walks are not analyzed further: there is nothing to account. No matching
whose existence is equivalent to `P(C) ≥ D(C)` is asserted (would be
circular per WS-02F).

## I. Zero-weight transitions, overlap, cyclic closure

Zero-weight edges (`H = 1, q = 2`; `H = 2, q = 4`) can perform B-splays of
depths 4–5 (resp. 8–9), A-moves, root changes, and marked-depth increases —
all at `w = 0` — so none of those transformations implies positive cost,
and zero-weight steps can restore every component of readiness. Overlap and
cyclic-closure questions presuppose chargeable intervals and do not arise.

## J. Abstract-only walk soundness

Unaffected by the failure: readiness uses only endpoint coordinates, so it
is well-defined on abstract walks including nonprimitive cycles and repeated
states; no hidden A-tree transport is ever used (only `α`). The route fails
on cost control, not on visibility or soundness.

## K. Reconstructed bridge: not built (OPEN)

`Σw = P(C) − D(C) ≥ 0` remains unproved for low-only closed walks. The
strongest proved statements are §§C–E (readiness soundness, post-negative
characterization, same-key non-immediacy, displacement bound, A-charge
necessity) — none yields `P(C) ≥ D(C)`.

## L. Contracted-high interface and remaining obligations

Untouched: `w_H = 6 − q` on a separate relation; mixed walks may interleave
high edges between negatives (additional deficits/capacities, unanalyzed);
no high-edge sign fact is imported. Full Step 03 still needs: a drop-
forcing or charging law that survives §§F–G (positive-weight necessity, not
mere charge necessity), plus high-edge compatibility.

## M. IAGS R1–R4 audit

R1: the child lemmas (readiness soundness, displacement bound, A-charge
necessity, same-key nonadjacency) are valid but do not simplify the parent —
no cost control follows, so the recurrence/charging route cannot demonstrate
the required leverage; promoting partial recurrence observations would
violate R1 (explicitly: same-key nonadjacency alone, per-mission guidance,
is insufficient). R2: H = 1 fusion scope kept; H = 2 multis explicitly
retained as additional regeneration avenues (§G). R3: theorem, graph,
semantics, states untouched. R4: §§C–E lemmas PROVED; §D bound-candidate
and §F exclusion REFUTED-as-provable (admissibility direction);
§§G–H,K OPEN with proved obstruction (zero-weight/adjacent regeneration
admissible in principle); no unfounded existence claims (no witness
constructed — correctly, as none is authorized).

## N. Final outcome: OUTCOME F — RECURRENCE ROUTE FAILED

Earliest exact obstruction: the frozen conjuncts admit (do not exclude)
zero-weight B-pushdown/A-return transitions and adjacent distinct-target
negatives, so no recurrence law can force positive-weight repayment of
`δ ∈ {1,2}`; A-charge necessity collapses to weight-free `q = 2H`
balancing. Retained valid partials: §§C–E. The route is abandoned; no
successor Box is opened. This failure does not disprove universal weight
nonnegativity; no negative-walk claim is made.

## O. Authorization status and hard stop

WS-02G only was authorized. No solvers, searches, compiler/graph/budget
changes, no WS-02H, no Step 03/04 promotion, no Dynamic Optimality claim.
Bank25 = 25. Step 03 remains OPEN.

**HARD STOP.**
