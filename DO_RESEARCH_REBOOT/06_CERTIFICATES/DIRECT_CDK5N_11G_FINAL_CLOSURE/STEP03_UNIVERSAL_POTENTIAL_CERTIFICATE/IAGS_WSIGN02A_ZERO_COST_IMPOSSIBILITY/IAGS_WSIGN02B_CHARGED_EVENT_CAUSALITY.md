# IAGS-WS-02B — Charged-Event Causality: Root Synchronization, Divergence Generation, and Zero-Cost B-Change Attribution

Mission: `IAGS-WS-02B-...-CHARGED-EVENT-CAUSALITY`, entry HEAD `61c6abd`.
Method: mathematical proof from frozen source text only. No coding, no solvers, no source changes.
Verdict: **OUTCOME A — FULL CAUSALITY THEOREM PROVED** (see §J).

## A. Exact statement and inherited WS-02A result

**Theorem (charged ancestor of zero-cost B-change).** In any valid low macro,
for any active event `i` with `a_i = 0`, `K_i = 1` (KEEP), `ΔB_i = 1`
(complete B-state change), there exists `j < i` with `a_j > 0`,
`K_j = 0` (charged DELETE), `GenDiv(j)` (synchronized-to-desynchronized
transition at `j`), and no KEEP strictly between: `∀k, j < k < i ⇒ K_k = 0`.

Inherited from WS-02A (`IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY.md`, certified at
`61c6abd`, not reproved here): entry root pinning — initial A-root is an S-key,
initial B-root is a core slot, their S-indices agree (`Sync(0)`, see §B);
`H = Σ_active a_i = Hv ≤ 2` with `a = event_a` table
`dd ↦ 0,1,2,3,4 → 0,1,1,2,2`; active A-depth bound `dd ≤ 4`
(`build_slow` presence loop + `verify_path_dyn`); for any active KEEP whose
target is the current B-root slot, the witness B-depth is forced to `0`
(vacuity sub-lemma: `bd ≥ 1` contradicts B root-termination + no-repeat +
`bd ≤ 18`); terminal genuine block `tisS ∧ marked ∧ chg` with
`chg = OR_e(islast(e) ∧ diff(bs[e],bs[e+1]))` over `kl/rl/kr/rr/root`.

Assumptions reused exactly as certified: frozen conjuncts (C1)–(C12) of the
WS-02A inventory, same files, same gating. Nothing is narrowed.

Authoritative paths (repo-relative under `DO_RESEARCH_REBOOT/06_CERTIFICATES/`):
`DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py` (`build_slow`,
`shadow7`, `shadow_match7`, `state_valid7`),
`DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py`
(`same_keep_target`, `root_terminated:42`, `no_intermediate_genuine`,
`a_key_of`, `b_key_of`),
`DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py`
(`splay_event`, `single_rot`, `blend`, `verify_path_dyn`, `event_a`, `macro_H`),
`DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py`
(`b_splay_event`, `b_single_rot`, `b_blend`, `verify_bpath`, `b_valid`),
`DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py`
(`BStruct`, `b_tree_valid`),
`DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ATOM_INVENTORY.py`
(`_gapof:88-93`).

## B. Canonical root-label construction

Define the canonical label space
`K = {S(0),…,S(8)} ∪ {G(0),…,G(9)}`.
For an A-root slot `u`: if `wit.isS[u]` use `S(wit.sidx[u])`, else
`G(inv._gapof(wit.rank[u]))` — exactly the tables `same_keep_target` reads
(`a_key_of`). For a B-root slot `v`: if `v < 9` (core) use `S(v)`, else
`G(v − 9)` — exactly the `b_key_of`/fringe-branch convention
(`bC = (bT < 9)`, `bg = bT − 9`).
`r_A(i)`, `r_B(i)` are these labels at `A_i.root`, `B_i.root`;
`Sync(i) ⟺ r_A(i) = r_B(i)`, `Div(i) ⟺ ¬Sync(i)`.

Well-definedness (roots are always real slots, so labels are total):
A-roots start at slot `0` (`AState.root = const 0`) and each active event
sets root to its target (`§C`), a present slot (`pres` conjunct,
`STRICT_LOW_COMPILER.py:128-134`); inactive events are identity. B-roots
start at a core slot (entry sync + `b_valid` via `state_valid7`) and each
active KEEP sets root to its B-target — S-case core `< 9` via `bC`, fringe
case gap `9..18` via `_gapof ∈ 0..9` plus the nonempty-gap conjunct
(`STRICT_LOW_COMPILER.py:149-156`, which rejects `bT = 19 = NULLB` since gap
index `10` matches no `sig` position); DELETE/inactive are full B-identity
(`ITE(is_delete, …)` end-construction). Hence every `A_i.root`, `B_i.root`
is a real slot; `Sync` is never evaluated on `NULLB`/ports.

Fringe safeguard (the four equalities stay distinguished):
(1) concrete source keys, (2) S-index keys, (3) canonical fringe-gap labels,
(4) B-controller slots. Injectivity used: core slot `v ↦ S(v)` and gap slot
`v ↦ G(v−9)` are each injective, and the `S`/`G` kinds are disjoint. Thus
equal labels of equal kind force the same B-controller slot: `S(x) = S(v)`
forces B-root/target `= x`; `G(g)` forces gap slot `9+g`. Cross-kind label
equality never occurs. No promotion of same-gap equivalence to concrete-key
equality is made anywhere: causality is proved at label level, and the
KEEP-identity fungibility theorem is cited only for consistency, never as a
proof step.

`Sync(0)` is inherited: `A_0.root` is slot `0` with
`wit.isS[0] = s.aS[0] = TRUE`, `wit.sidx[0] = s.aI[0] =: x0`
(`shadow_match7` root clause, `shadow7` returns `st.root` exactly), i.e.
`r_A(0) = S(x0)`; `B_0.root = x0 < 9` (entry sync, `muxb` identity on core,
`aI < 9` via `state_valid7`), i.e. `r_B(0) = S(x0)`.

## C. Target-to-root KEEP proof (KEEP Resynchronization Lemma PROVED)

For every active event (KEEP or DELETE — `splay_event`/`b_splay_event`
condition only on the active flag, never on KEEP for the A-side; B-side
DELETE is full identity by construction), the post-state root equals the
event target. Proof from the frozen rotation code: pairs fire for
`t + 2 ≤ d` (`t` even), the leftover zig fires for `d = t + 1`, and
pair+zig are mutually exclusive in one level; the LAST firing primitive
always carries the target `x = path[0]` with root-update forced —
`pwrB = (t + 2 = d)` on the last pair's second rotation, literal
`p_was_root = TRUE` on the zig (`single_rot`/`b_single_rot` end with
`newroot = ITE(p_was_root, x, st.root)` applied through the ITE-`blend`).
Case table (both sides, zigzig and zigzag): `d = 0` → no prim, root kept,
and root-termination + path anchor already force target = root;
`d = 2m > 0` → last pair at `t = d − 2` sets root `= path[0]`, nothing fires
after (`t + 2 > d`, `t + 1 > d` for all later levels); `d = 2m + 1` → zig at
`t = d − 1` with `x = path[0]`, `p = path[d]`, correct side
(`sxmux = dirs[d−1]`), `p_was_root = TRUE`. Loop bounds cover all depths:
A `dd ≤ 4` (pairs `j = 0, 1`); B `bd ≤ 18` (pairs `j = 0..8`, zig `j ≤ 8`).
The root update depends only on `d` and `path[0] = target` — not on path
validity — so it holds even for degenerate witnesses; the path conjuncts
constrain only tree shape, and the side muxes are exactly the splay-correct
ones. Hence for active KEEP:
`A_{i+1}.root = A-target(e_i)` and `B_{i+1}.root = B-target(e_i)`.
`same_keep_target` forces the two targets' canonical labels equal
(S: `aI = bT < 9`; fringe: `gapof = bT − 9`). Therefore

> `K_i = 1 ⟹ Sync(i+1)` — KEEP Resynchronization, proved universally,
> including fringe/gap targets (gap-slot B-roots are validity-allowed:
> `b_tree_valid` lets the root be "whoever it is", gap parents core).

The same target-to-root fact holds for active DELETE on the A-side
(`splay_event` has no KEEP gate), used in §E.

## D. Zero-cost synchronization preservation

Lemma A (`a_i = 0 ⟹ d_i = 0`, active events): `a_i = 0` plus the active
`dd ≤ 4` bound leaves only `dd = 0` in the `event_a` table. For `dd = 0`
all A gates are off (`t + 2 ≤ 0` false; `0 = t + 1` false), and the
full-state ITE-`blend` (`kl/rl/kr/rr/root` all gated) returns its input:
`A_{i+1} = A_i` as complete states, for KEEP and DELETE alike.

Lemma C (`Sync(i) ∧ a_i = 0 ⟹ Sync(i+1)`), by exact case split.
DELETE: Lemma A gives `A_{i+1} = A_i`; frozen B-identity gives
`B_{i+1} = B_i`; synchronization status is unchanged. KEEP: Lemma A plus
root-termination (`plast = path[0]`, `path[0] = evT`) gives
A-target `= A_i.root`; `same_keep_target` gives the B-target the label
`r_A(i) = r_B(i)` (by `Sync(i)`); label injectivity (§B) forces the
B-target slot `=` the current B-root slot; WS-02A vacuity forces the
witness `bd = 0`; all B gates off, full-state `b_blend` identity
(`lo/hi` carried from old state), `B_{i+1} = B_i`. Identical states keep
`Sync` true.

Stronger corollary (first causal implication, no `q` involved):
`Sync(i) ∧ a_i = 0 ∧ K_i ⟹ ΔB_i = 0` with `ΔB` over the complete
B-representation (identity covers `lo/hi` too, strictly more than the
`chg`-`diff` fields). Contrapositive: `a_i = 0 ∧ K_i ∧ ΔB_i = 1 ⟹ Div(i)`.

## E. Divergence-generation classification

`GenDiv(i) ⟺ Sync(i) ∧ Div(i+1)`. Theorem: 
> `GenDiv(i) ⟹ (a_i > 0) ∧ (K_i = 0)` — every divergence-generating event
> is a positively charged DELETE.
Proof: `a_i = 0` would preserve `Sync` (Lemma C) — contrapositive gives
`a_i > 0`; `K_i = 1` would restore `Sync` (Lemma B) — contrapositive gives
`K_i = 0`. Both arrows are contrapositives of proved universals; no
sampling, no converse assumed.

Exact charged-DELETE criterion (biconditional, proved): DELETE is full
B-identity, so `r_B(i+1) = r_B(i)`; A target-to-root (§C) gives
`A_{i+1}.root = A-target`; hence
`Div(i+1) ⟺ keylabel(A-target(e_i)) ≠ r_B(i)`.
A charged DELETE need not generate divergence (it may retarget A inside the
current B-root label) — correctly not claimed; the criterion above is the
exact condition.

## F. Charged-ancestor theorem (main result, strong form PROVED)

Assume active `i` with `a_i = 0`, `K_i = 1`, `ΔB_i = 1`. By §D,
`Div(i)`; `i ≥ 1` follows since `Sync(0)`. Finiteness plus `Sync(0)`/`Div(i)`
yields a latest index `j < i` with `Sync(j) ∧ ¬Sync(j+1)`, i.e. the latest
`GenDiv(j)` before `i`. By §E, `a_j > 0` and `K_j = 0`: the ancestor is a
divergence-producing charged DELETE. No KEEP strictly between: a KEEP at
`k`, `j < k < i`, would give `Sync(k+1)` (§C); if `k + 1 = i` that
contradicts `Div(i)`, else a further transition in `[k+1, i)` contradicts
maximality of `j`. This is exactly the required
`∃j < i : a_j > 0 ∧ K_j = 0 ∧ GenDiv(j)` with
`∀k (j < k < i ⟹ K_k = 0)` — proved, with the no-intervening-KEEP clause in
the strong (any-charge) form.

## G. Bounded-event corollaries

Unique attribution: map each zero-cost B-changing KEEP to its latest prior
`GenDiv`. The map is injective: if `i1 < i2` shared ancestor `j`, then
either `j ≥ i1` (distinct from `i1`'s ancestor, which precedes `i1`) or
`j < i1`, putting KEEP `i1` inside `(j, i2)` against the strong clause.
Hence `#zerocost-B-changing-KEEPs ≤ #charged-DELETEs`. Each charged event
contributes `≥ 1` to `H ≤ 2`, so `#charged-DELETEs ≤ H ≤ 2`, and therefore
at most two zero-cost B-changing KEEPs per macro, injectively attributed —
no double-counting, since the first subsequent KEEP restores `Sync` and any
further zero-cost B-change needs fresh divergence.

Terminal/intermediate roles: a zero-cost terminal genuine KEEP
(`ΔB = 1` via `chg`) requires a preceding charged DELETE (§F). Under
`H ≤ 1` (hence `H = 1` with WS-02A genuineness), that DELETE has `a = 1`
and consumes the entire budget; all other events have `a = 0`. Under
`H ≤ 2` at most one earlier (intermediate) zero-cost B-changing KEEP can
occur. By A8 (`no_intermediate_genuine`: non-terminal active KEEP cannot
combine marked S-target with B-change), every intermediate B-changing KEEP
has an unmarked core or fringe-gap target.

## H. Fringe-gap and A8 audit

Zero-cost intermediate B-changing KEEPs are admitted, with exact
preconditions: target is S-unmarked-core or fringe-gap (A8 excludes exactly
the S-marked-target changing case; the fringe branch needs a nonempty gap
per `sig`); a `GenDiv`-producing charged DELETE necessarily precedes, with
no KEEP between (it need not target the same canonical key — the invariant
is label-level divergence at boundary `i`, and any later charged DELETE may
re-target A provided it never re-synchronizes, else `j` would not be
latest); subsequent zero-cost DELETEs preserve divergence (both-side
identity); any intervening KEEP necessarily extinguishes it (Lemma B).
`b_tree_valid` at every active boundary plus real-slot roots keep all labels
defined; `NULLB` targets are unsatisfiable for KEEP (S-branch width forces
`< 16` with core `< 9`; fringe branch plus nonemptiness forces `9..18`).

## I. Simplification and quantitative-bridge boundary

Genuinely removed from later proof search: (1) synchronized zero-cost events
are B-inert (§D corollary) — B-evolution under the `H ≤ 2` budget
concentrates on ≤ 2 charged DELETEs plus their injectively attributed
KEEPs; (2) divergence lifetime is bounded by KEEP-free segments (any KEEP
resets `Sync`); (3) WS-02C case analysis collapses to enumerating charged
skeletons (positions/charges of ≤ 2 paid events + attributed KEEP slots)
rather than arbitrary 5-event words. What remains: everything quantitative
— `q` (B-depth charge), `w ≥ 0`, any potential. Causality gives no depth or
charge control (a `GenDiv` DELETE may carry `d_A ≤ 4` arbitrary; B-depths to
18 unconstrained by these lemmas). The contribution is structural and
combinatorial, not transfer-quantitative; no `q ≤ 2H`, no weight-sign claim
is made or implied.

## J. Final verdict

**OUTCOME A — FULL CAUSALITY THEOREM PROVED.** KEEP resynchronization (§C),
divergence-generation classification (§E, charged-DELETE-only plus exact
biconditional criterion), and charged-DELETE ancestry in the strong
no-intervening-KEEP form (§F) are universally established from the frozen
semantics, with bounds: `#ZCB-KEEP ≤ #charged-DELETE ≤ H ≤ 2`, injective
attribution, terminal-budget consumption, A8 target-kind restriction. Stage
11G Step 03 remains OPEN; Step 04 unauthorized; Bank25 = 25.
