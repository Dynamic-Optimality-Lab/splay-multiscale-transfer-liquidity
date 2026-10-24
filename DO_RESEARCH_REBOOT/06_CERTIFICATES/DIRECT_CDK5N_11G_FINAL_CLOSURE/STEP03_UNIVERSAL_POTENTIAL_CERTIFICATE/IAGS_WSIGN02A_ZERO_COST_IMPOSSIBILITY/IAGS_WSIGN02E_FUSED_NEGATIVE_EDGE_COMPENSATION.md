# IAGS-WS-02E — Fused Negative-Edge Compensation: Source-Derived Rotation Transfer, Reserve Attempt, and Closed-Walk Bridge

Mission: `IAGS-WS-02E-...`, entry HEAD `0ddedea` (verified on
`coarse-double-branch`; no other changes made).
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source/graph changes. Inherits WS-02A (PROVED), WS-02B (OUTCOME A),
WS-02C (OUTCOME B), WS-02D (OUTCOME A) as certified, with exact scope.
Verdict: **OUTCOME B — QUANTITATIVE LEMMA PROVED, COMPENSATION OPEN**
(see §J; R1–R4 audit in §I).

## A. Frozen target, inheritance, and Box

Target: a source-derived quantitative transfer law for fused negative H = 1
low edges (single marked KEEP, `d_A ∈ {1,2}`, `d_B ∈ {6,7,8}`, `q ∈ {3,4}`,
`w = −δ`, `δ ∈ {1,2}`; WS-02D's depth-9 allowance concerns multi-event
histories only and is not imported into the fused class) that explains
deficit compensation (`§2 T_E`). Inheritance: H ≥ 1 universally (02A);
resynchronization, GenDiv attribution + injectivity (02B); H = 1 fusion to a
single-event KEEP with endpoint `q`-identity and shallow-A/deep-B
characterization (02C); universal `q ≤ 4`, H = 2 nonnegativity (02D); frozen
interpreters/repairs/11F simulation; R1–R4. Unresolved ambiguity `U_E`:
whether A-shallow/B-deep access releases a reusable structural resource whose
regeneration provably costs enough. Bridge `β_E`: a state function
`R` with `R(t) − R(s) ≤ w_L` per low edge (telescoping on closed low-only
walks) — pursued, not assumed.

## B. Exact fused negative-edge structure (inherited, restated for scope)

Fix fused genuine H = 1 edge `s → t`, marked target `x`: A-splay of `x`
from depth 1–2 to root (`d_A` prims, `a = 1`); B-splay of `x` from depth
6–8 to root (`d_B` prims); B unchanged before terminal (fusion); entry
Sync-labelled `S(x0)`, `x ≠ x0`, both roots become `x`; `w = 2 − q = −δ`.
No hidden history remains (fusion audit, WS-02C).

## C. Rotation-transfer derivation (PROVED — Task A deliverable)

All claims verified against `PC_B_CONTROLLER.b_splay_event/b_single_rot`
(`:164-213`, `:73-96`) and the identical-math A-side
(`PC_ROTATION_INTERPRETER.splay_event/single_rot`, `:160-211`, `:114-148`).
Labels: **PROVED**.

1. **Exact prim count.** Gates partition levels: pairs fire exactly for
`t + 2 ≤ d` (`t` even), the zig fires exactly for `d = t + 1` (never both in
one level). A depth-`d` splay performs exactly `⌊d/2⌋` pairs + `(d mod 2)`
zig = exactly `d` single rotations. Fused negative: `d_A + d_B ∈ {7..10}`
prims; `q = ⌊d_B/2⌋` = number of B-pairs, `a = ⌈d_A/2⌉` = number of A-levels.
2. **Write locality** (restated from WS-02D for the transfer): each prim
rewrites child fields only at its `{x, p, gp}` (gp writes gated off when it
is the root step); all other slots keep refs; off-path subtrees move rigidly
(`(kind,ref)` pairs preserved; ports/empty ride without slot-depth effect).
3. **Level-set preservation + target progress.** Each prim permutes its
triple within the same level-set (rotation swaps `x,p` depths, `gp` fixed;
non-last prims leave the root untouched via `p_was_root/pwr = FALSE`), so
by bottom-up induction triples stay consecutive; each pair drops the target
exactly 2 levels, each zig exactly 1; `d → 0`.
4. **Triple depth-sum invariance (new).** Every prim moves its triple as
`x:−1, p:+1, gp:0` (rotation definition, verified ref moves), so each prim
preserves its own triple's depth-sum exactly. Triples overlap across prims
(shared nodes; deeper path nodes ride with risen ancestors), so no
whole-splay path-sum invariant follows — the net change over a splay is
exactly the off-path sum in item 5. Each prim drops the target exactly one
level (as triple member, or as rider inside the risen ancestor's subtree —
the zigzig same-side chain guarantees the rider case), giving the
2-per-pair/1-per-zig progress of item 3.
5. **Per-prim transfer equation (new).** With `S` = `p`'s other-side slot
subtree, `L` = `x`'s kept-side slot subtree (kind-0 descendants only; ports/
empty contribute 0): `Δ(total slot-depth) = |S| − |L|` per prim
(`x:−1, p:+1, L:−1 each, M:0, S:+1 each`). Whole-splay law:
`Δ = Σ_prims(|S| − |L|)`. Sign indefinite from rotation structure alone.
Marked-restricted sums obey the same equation on `∩ M`.

## D. Structural quantity: attempted, none constructed (OPEN)

No state function `R` with a proved debit law was derived. The transfer
laws of §C are exact but sign-indefinite: the only net depth change comes
from off-path `S/L` terms, whose sizes (0 to tree-bounded) and marked
content are uncontrolled by any proved frozen predicate. Transplant rigidity
gives internal-depth preservation of off-path subtrees, not a signed total.

## E. Negative-edge debit: obstruction, not theorem (OPEN)

The §C identities rule out — with proof, not skepticism — the entire
depth-only reserve family: total B-depth-sum, ancestor-restricted sums, and
path-compression "release" (per-prim triple moves are zero-sum, but triples
overlap and riders shift, so no whole-splay path invariant follows;
hand-verified d = 2 traces, OBSERVED: zigzig path-sum 3 → 3, zigzag 3 → 2 —
already showing no uniform path-sum law). A depth-only
`R` cannot satisfy `R(t) − R(s) ≤ w = −δ < 0` universally, since §C.5 exhibits
the sign-indefinite `|S| − |L|` mechanism. Trivial one-bit quantities
(e.g. root-markedness) fail directionally. The missing ingredient is
identified precisely: subtree-size/rank control of the off-path terms
(the Sleator–Tarjan rank idea is the known direction; rebuilding its
rotation inequalities over frozen prims, gaps/fringe, DELETEs, and A-shadow
changes is a separate proof obligation, stated here as identified work, not
progress — per R1 it is not dressed up as a result).

## F. Replenishment: classes catalogued, uniform law OPEN (Task C verdict)

Per-class structural facts (all inherited/proved): H = 1 `q ≤ 2` fused
singles (`d_B ≤ 5`) nonnegative by arithmetic; H = 2 multis `w = 4 − q ≥ 0`
(WS-02D); zero-weight edges (`q = 2H`) sit on the boundary and move every
depth-based quantity either way by §C.5 — the mission's warned failure mode,
confirmed structurally (a zero-weight edge with large marked `S` strictly
increases total marked-depth, so no depth-based per-edge certificate can
hold); DELETEs are B-identical (A-only moves, budgeted in H); fringe/gap
splays obey the same prim laws with gap-slot targets; intermediate
nongenuine KEEPs and α-changes are replay-identities or H-budgeted moves
with the same sign-indefinite transfer. No uniform `R(t) − R(s) ≤ 2H − q`
is derivable from §C: the obstruction is identical to §E (off-path terms),
now on the upper-bound side.

## G. Reconstructed bridge (CONDITIONAL)

*If* a state function `R` on abstract states `(μ,b,α,σ)` satisfied the
per-edge law on all low edges, closed low-only walks would satisfy
`Σw ≥ Σ(R(t_e) − R(s_e)) = 0` by telescoping — transport is legitimate
because consecutive walk edges share full abstract states (no witness-history
concatenation is assumed). The bridge is valid; its hypothesis is unproved.
High-edge interface (future obligation, not claimed): any shared reserve
would additionally need `R(t) − R(s) ≤ 6 − q` on contracted-high edges, or a
separately bridged multi-component certificate.

## H. Contracted-high interface requirements

Unchanged from WS-02C: high edges live in a different relation with weight
`w_H = 6 − q`; no high-edge accounting is attempted here; a low-edge reserve,
even if completed, extends only via the §G interface (or a new certificate
with its own bridge), which remains a separate proof obligation.

## I. IAGS R1–R4 audit

R1 (easier + high-leverage): the §C package is the first exact whole-splay
transfer law in this series (prim counts, level-sets, triple invariance,
signed transfer equation) — genuinely new and quantitative. Its leverage is
eliminative and directive: it *proves* depth-only reserves cannot work and
isolates subtree-size/rank control of `|S| − |L|` as the single missing
ingredient, removing an identifiable blind alley rather than renaming the
conjecture. No potential was guessed; no sampled trajectory cited; no
qualitative restatement passed off as progress. R2: fusion used only for
H = 1 (scope kept); WS-02D's `q ≤ 4` never invoked for a potential law.
R3: frozen graph, semantics, states, theorem all untouched; only new lemmas
added. R4 labels: §C **PROVED**; §D–F reserve/debit/replenishment **OPEN**
(with exact obstruction); §G bridge **CONDITIONAL**; naive depth-sum/path-
compression reserves **REFUTED as R-candidates** (transfer equation +
both-sign mechanism; not a refutation of the weight-sign theorem).

## J. Final outcome: OUTCOME B

A genuinely new rotation-transfer lemma package (§C) is established, but no
complete replenishment or closed-walk certificate follows. Smallest remaining
obligation, in order: (1) subtree-size/rank control of off-path transfer
terms over frozen prims; (2) a reserve with proved debit + replenishment on
all low-edge classes; (3) high-edge interface. The H = 1 fused deficit
(`δ ∈ {1,2}`) and the H = 2/multi-event bounds stand as certified; the
accumulation question is untouched by this campaign beyond §C–G.

## K. Authorization status and hard stop

This campaign authorized the WS-02E proof attempt only. No solvers, no
experiments, no source/graph/cap changes, no WS-02F launch, no Step 03/04
promotion, no Dynamic Optimality claim. Bank25 = 25. The identified next Box
(rank-controlled transfer) is **not executed without authorization**.

**HARD STOP.**
