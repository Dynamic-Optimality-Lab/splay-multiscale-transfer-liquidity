# IAGS-WS-02F — Rank/Subtree-Weighted Transfer and Replenishment: Exact Mass Identities, Debit Failure, and Route Abandonment

Mission: `IAGS-WS-02F-...`, entry HEAD `7cfbaf6` (verified on
`coarse-double-branch`; no other changes made).
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source/graph changes. Inherits WS-02A (PROVED), WS-02B (OUTCOME A),
WS-02C (OUTCOME B), WS-02D (OUTCOME A), WS-02E (OUTCOME B) with exact scope.
Verdict: **OUTCOME F — RANK ROUTE FAILED** (see §N for the precise
obstruction; valid partial theorems retained in §§D–G).

## A. Frozen target and inherited certificates

Target: a source-derived rank/subtree-mass law controlling WS-02E's signed
off-path transfer `ΔD = |S| − |L|`, yielding deficit accounting for fused
negative H = 1 low edges (`d_A ∈ {1,2}`, `d_B ∈ {6,7,8}`, `q ∈ {3,4}`,
`w = −δ`, `δ ∈ {1,2}`) plus universal low-edge replenishment and a closed-walk
bridge. Inherited: H ≥ 1 universally (02A); causality/attribution (02B);
H = 1 fusion + endpoint `q`-identity + shallow-A/deep-B characterization
(02C); universal `q ≤ 4`, H = 2 nonnegativity (02D); exact prim/level/write/
triple/transfer rotation laws and the ruling-out of depth-only reserves
(02E). R1–R4 and Bank25 = 25 preserved; Step 03 OPEN, Step 04 unauthorized.

## B. WS-02E precision correction and scoped inherited identities (PROVED)

Mandatory audit. WS-02E's unmarked transfer equation stands as written
(`Δ = |S| − |L|`: per-prim `x:−1, p:+1` cancel). Its marked-restricted form
requires the rotating-node indicators and is corrected here (recorded, not
silently altered):

> `ΔD_M = |S∩M| − |L∩M| + 𝟙[p∈M] − 𝟙[x∈M]` per prim (PROVED from the same
> verified ref moves; `M` = marked set).

The `±1` terms cannot be canceled in a marked-restricted sum. Raw-depth sign-
indefiniteness defeats naive monotonic-depth reserves; it does not by itself
refute every nonlinear/weighted/state-dependent reserve — that broader
question is settled negatively for this route in §§H–J below, not by the
equation alone. All other WS-02E identities are inherited unmodified
(prim counts `= d`, target progress, write locality `{x,p,gp}`,
transplant rigidity, per-prim triple-sum invariance, level-sets).

## C. IAGS Box B_F and high-leverage criterion

`T_F`: rank/subtree law controlling off-path terms → deficit mechanism →
universal replenishment → closed-walk bridge. `C_F`: (1) graph-visible mass
system; (2) exact mass/rank prim laws; (3) signed inequality for fused
negatives; (4) reserve from that inequality; (5) replenishment bound;
(6) verified bridge. `I_F`: §§A–B plus frozen semantics/topology/masks/
endpoint interface. `U_F` and bridge `β_F` (`R(t) − R(s) ≤ 2H − q`) as stated
in the mission. R1 bar for this Box: the rank work must impose new
quantitative constraints relevant to deficits, reserve changes, or
replenishment — bookkeeping alone does not pass.

## D. Source-valid subtree-mass definitions (PROVED sound)

`V(B)` = nine core slots ∪ present gap slots (sig ≠ 0; constant per edge
since `s.sig = t.sig` is conjoined). Let `ω(v) > 0` be per-slot and
edge-constant: unit weights, or `ω(v) = 1 + mubit(μ, sidx(v))` (μ is
edge-constant via conjoined `s.mu = t.mu`; deterministic from the endpoint
state; target-independent). Marked-only weights are rejected (subtree with
no marked key would have mass 0 → `log 0`); the `+1` form keeps every mass
`≥ min ω > 0`, so no logarithm is ever of zero (the mission's worry is
discharged by construction). Absent gaps are excluded from `V(B)` (they are
kind-childless and, per WS-02D write analysis, untouched by any splay since
entry — never path nodes, never targets — so their exclusion is stable);
ports are not B-nodes. Mass `m_B(v) = Σ_{u∈Subtree(v)} ω(u)` (kind-0
descendants; subtree sets well-defined: one-parent counts + strict depth
decrease hold at every replay boundary, and each frozen prim maps valid
trees to valid trees by exact standard-rotation ref moves). Rank
`r_B(v) = log_2 m_B(v)`. Sig-derived fringe-multiplicity weights were
considered and NOT used (their source meaning is unproved; left as an
unvalidated option, not a result).

## E. Exact primitive rank-transfer identities (PROVED)

For one frozen `b_single_rot` (any orientation; A-side identical math),
with `S` = p's other-side slot-subtree, `L` = x's kept-side, `M` = x's
rotation-side (adopted by p), `gp`'s other side untouched:

> `newm(x) = oldm(x) + ω(p) + m(S)`; `newm(p) = oldm(p) − ω(x) − m(L)`
> (equivalently `oldm(p) − oldm(x) + m(M)`); `newm(gp) = oldm(gp)`;
> every other node's mass unchanged (refs untouched ⇒ subtree sets
> unchanged; transplanted subtrees keep internal masses).

Hence, with all masses strictly positive (§D):

> `Δr(x) = log_2(1 + (ω(p)+m(S))/oldm(x)) > 0`;
> `Δr(p) = log_2(1 − (ω(x)+m(L))/oldm(p)) < 0`;
> all other `Δr = 0`.

Zig worked end-to-end (single prim = complete level): exact. Pair
composition is mechanical substitution of §E (zigzig vs zigzag differ only
in which path nodes play the prim roles; the identities are
orientation-free). No log-inequality machinery is invoked; no telescoping
is claimed. Status: exact identities PROVED; their use for bounds is
separate (§§F–H).

## F. Zig, zigzig, zigzag: no signed pair law follows (PROVED obstruction)

Composing §E over a pair gives exact mass/rank bookkeeping, but the pair
net change in any rank aggregate still contains the off-path terms
(`m(S)`, `m(L)` per prim, disjoint across levels but unsigned and
unbounded by any proved predicate). No step of the composition removes the
sign-indefiniteness WS-02E located: the `+ω(p)+m(S)` growth at `x` and the
`−ω(x)−m(L)` shrinkage at `p` do not telescope into a signed pair total
without log-concavity machinery whose hypotheses (uniform subtree-size
control across fringe/gap/DELETE/α-changing classes) are not discharged
and are not discharged here. Pair-level rank cancellation is therefore
unproved, and — decisively — unnecessary to pursue further (see §H).

## G. Whole-splay rank accounting: the bridge fails here (PROVED gap)

Even granting, arguendo, the sharp classical access-bound form
(`d + ΔΦ ≤ 3·log_2(M_tot/m_s(x)) + 1`, CONDITIONAL — imported shape, not
proved for the frozen controller), deficit coverage would require
`3·log_2(M_tot/m_s(x)) + 1 + δ ≤ d_B`. Worst admissible case (leaf target,
`m_s = 1`, `M_tot = 19`, `δ = 2`): `3·4.25 + 3 = 15.75 > 8 ≥ d_B` — fails
by a factor of two; it holds only for large-subtree targets, never
universally. (Arithmetic PROVED given the form; the form itself stays
CONDITIONAL.) Conclusion: work-bounding access lemmas are quantitatively
insufficient for per-edge deficit coverage even in the ideal case — the
deficit needs a drop-forcing law, and rotation/rank structure only bounds
work from above. This is independent of transfer details and closes the
"import ST" shortcut.

## H. New mechanism: none constructed (OPEN, route-blocking)

No function `R(μ,b,α,σ)` with a proved `R(s) − R(t) ≥ δ` on fused negatives
was derived. The structural reason is now completely characterized:
(i) every depth/rank aggregate's per-prim change decomposes into a zero-sum
triple term plus sign-indefinite off-path terms (§§B,E–F); (ii) the missing
control (off-path subtree sizes/marks) is exactly what no frozen predicate
constrains; (iii) even ideal work-bounds point the wrong way with constants
too big (§G). Mechanism II (relative A/B) fails concretely: A-rotations
obey identical transfer math (same code structure), so A-depth sums are
equally uncontrolled, and `α` sees only depth ≤ 2 while the deficit lives
at B-depth 6–8. Mechanism III (marked aggregation) fails on the corrected
§B equation (rotating-node indicators + uncontrolled `S/L∩M`). Difference-
constraint fitting of any finite-domain quantity is rejected as circular:
`R(t) − R(s) ≤ w ∀e` is feasible iff no negative closed walk exists, i.e.
iff the theorem — fitting it as "the reserve" would violate R1 (PROVED
meta-observation, standard theory, cited as such, not as frozen theorem).

## I. Fused negative-edge debit theorem: unproved (OPEN)

With no reserve constructed, `R(s) − R(t) ≥ δ` (`≥1` for `q = 3`, `≥2` for
`q = 4`) is unproved on the full fused domain (all masks, roots,
zig/zigzag patterns, fringe signatures). No restricted-domain debit is
promoted either: any shape restriction strong enough to sign the off-path
terms would have to be proved admissible-invariant, which reintroduces the
same missing control. Endpoint-computability of `q` from `(B_s,B_t)`
(target-to-root ⇒ target = exit root; unique parent chains ⇒ true depth)
is noted as valid but insufficient — it restates WS-02C, constrains nothing.

## J. Replenishment: uniform law unprovable from rotation structure (OPEN)

Class-by-class: H = 1 `q ≤ 2` fused singles, H = 2 multis (`q ≤ 4`),
zero-weight edges (`H = 1, q = 2`; `H = 2, q = 4`), fringe/nongenuine/
DELETE/α-changing events, parallel witnesses (single `R` must meet the
minimum weight). In every class the per-prim transfer is §E's
sign-indefinite form, so no uniform `R(t) − R(s) ≤ 2H − q` follows without
the same missing size control; the zero-weight stress test is decisive in
the negative direction (a uniform certificate would need `R(t) ≤ R(s)` on
zero-weight edges, which rotation structure cannot force). The H = 1-only
sufficiency observation (`R(t) − R(s) ≤ 2 − q` implies the `2H − q` law since
`H ≥ 1`) is recorded but does not help: the `2 − q` law itself is unproved.

## K. Reconstructed bridge: conditional only (CONDITIONAL)

*If* an `R` with the per-edge law on all low edges existed, closed low-only
walks would satisfy `Σw ≥ Σ(R diffs) = 0` by telescoping over shared abstract
states (no history concatenation needed) — bridge valid, hypothesis
unproved. High-edge interface (`R(t) − R(s) ≤ 6 − q` or equivalent) remains
a separate future obligation, untouched.

## L. Contracted-high interface and remaining obligations

Unchanged: `w_H = 6 − q` on a different relation; no high-edge accounting
attempted; a low-edge certificate would extend only via §K's interface (or a
new bridged certificate). Full Step 03 additionally needs the proved
per-edge law itself.

## M. IAGS R1–R4 audit

R1: the route's rank work (exact mass/rank prim identities §§D–E, marked
correction §B, ST-insufficiency arithmetic §G, circularity observation §H)
is real mathematics, but it does not impose any new quantitative constraint
relevant to deficits, reserve changes, or replenishment — the signed law at
the heart of `C_F` is unproved and shown to be unreachable from rotation
structure alone, and even ideal imported bounds fail quantitatively. The
child did not remove identifiable difficulty from the parent; promoting it
to OUTCOME B would mislabel bookkeeping as leverage. R2: H = 1 fusion never
extended; α-observability never inferred from hidden A-trees; classical
bounds never imported as frozen facts (kept CONDITIONAL). R3: target, graph,
semantics, states, theorem untouched. R4: §§D–E identities PROVED;
ST bound-form CONDITIONAL with PROVED arithmetic consequence; §§H–J reserve/
debit/replenishment OPEN (obstruction PROVED in §§F–H); §K bridge
CONDITIONAL; depth-only/finite-fitting candidates REFUTED-as-reserves
(structural proof / circularity proof — not refutations of the sign theorem).

## N. Final verdict: OUTCOME F — RANK ROUTE FAILED

First exact obstruction (structural, proved): off-path transfer terms are
sign-indefinite from frozen rotation structure, so no drop-forcing
per-edge law follows from any depth/rank aggregate without subtree-size
control that no frozen predicate supplies. Second (quantitative,
conditional arithmetic): even ideal access-lemma work-bounds exceed the
available drop budget on leaf targets. Third (methodological, proved):
finite-domain reserve fitting is equivalent to the theorem itself. No
reserve, no debit law, no replenishment law, no bridge. The rank/subtree
reserve route is abandoned. Retained valid partials: §§D–E mass/rank prim
identities and formulas, §B marked-transfer correction, §G insufficiency
arithmetic, §K conditional bridge form. A failed route is not a disproof of
the universal sign theorem; no negative-walk claim is made.

## O. Authorization status and hard stop

This campaign authorized WS-02F only. No solvers, experiments, code/graph/
budget changes, no WS-02G, no Step 03/04 promotion, no Dynamic Optimality
claim. Bank25 = 25. Logically independent next Boxes (drop-forcing laws
beyond rotation algebra; walk-level charging) are identified, NOT executed.
Step 03 remains OPEN.

**HARD STOP.**
