# IAGS-WS-02C — Quantitative A/B Cost Transfer: Unit-Charge Fusion, Terminal B-Depth Accounting, and Endpoint-Visible Compensation

Mission: `IAGS-WS-02C-...-QUANTITATIVE-TRANSFER`, entry HEAD `a87b2ed`.
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source changes. Inherits WS-02A (genuine ⇒ H≥1) and WS-02B (OUTCOME A:
causality, resynchronization, attribution) as certified.
Verdict: **OUTCOME B — EXACT CREDIT REDUCTION PROVED** (see §H for the exact
scope, including one explicitly isolated obstruction in the multi-event
universal bound).

## A. Exact inherited assumptions and compiler definitions

Low edge = satisfying witness of `build_slow`
(`DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py:94-210`).
Inherited conjuncts: `nev ≥ 1`, terminal KEEP, `H = Hv = Σ_active event_a ≤ 2`
with `event_a: dd ↦ 0,1,1,2,2` for `dd = 0..4`, active A-depth `dd ≤ 4`,
B-depth `bd ≤ 18`, path anchors (`evpath[0] = evT`, `bpath[0] = bT`),
A/B root termination + no-repeat (`STRICT_SOURCE_REPAIRS.py:42`),
`same_keep_target`, entry sync (`s.aS[0]`, core B-root, `s.aI[0]` = B-root
slot), `shadow_match7` at both endpoints, per-event threading
(`splay_event`, `b_splay_event` with DELETE/inactive full B-identity),
terminal block `tisS ∧ marked ∧ chg` with `chg` over `kl/rl/kr/rr/root`
(`:197`), destination `t.b = bs[5]`, weight `w = 2H − q` with
`2q ≤ bd_last < 2q + 2` (`:176-178`), B-validity at endpoints
(`state_valid7`, full `b_tree_valid`) and structure-only validity
(`intervals=False`, `:159`) at intermediate boundaries.
Every `build_slow` edge is terminal-genuine (terminal block unconditional),
so WS-02A gives `H ≥ 1` for ALL of `E_L`. IAGS Box: T_C = source-derived law
binding charged A-accesses to terminal B-credit `q` and graph-visible change;
C_C = exact accounting, unit-charge fusion, faithful depth-two A-shadow,
exact B-paths, endpoint (B-telescoping) validity; I_C = WS-02A/02B,
interpreters, repairs, 11F simulation; U_C = whether an A-cheap/B-deep access
yields provable structural credit bounding deficit accumulation; β_C = fused
single-access law + endpoint `q`-identity + exact deficit arithmetic (§E–G).

## B. Certified and bounded `q ≤ 4` reduction; multi-event defect isolated

`q = ⌊d_B^term / 2⌋` holds UNIVERSALLY (pure integer arithmetic from the
conjoined `2q ≤ bd_last < 2q + 2`; DAG INT exact; no scope restriction —
`d_B^term` is the witness `bd_last` whatever it is).

`d_B^term ≤ 8`, `q ≤ 4` are PROVED for single-event witnesses and hence for
all fused representatives: entry B carries full `b_valid` (gaps childless),
so no gap slot can lie on any parent chain (a gap claims nothing), the marked
core target's B-path has only core ancestors, at most 9 distinct core slots
gives depth ≤ 8. Consequently for single-event edges `H = 2 ⇒ w = 4 − q ≥ 0`.

For MULTI-event macros the core-ancestor step is UNPROVED — exact defect:
intermediate boundaries get structure-only validity (`intervals=False` skips
`b_valid`; `STRICT_B_CONTROLLER.py:26`), whose claimant-count/parent clauses
(`:42-48`, gap-parents-core `:78-80`) do not forbid gap slots with children;
`splay_event`/`b_splay_event` contain no gap guards, so splaying a fringe gap
target (explicitly supported: `same_keep_target` fringe branch, nonempty-gap
conjunct `:151-156`, gap roots allowed by `b_tree_valid`) leaves gap internal
nodes; such structures are cheap (fringe and Div-zero-cost KEEPs are
A8-vacuous and H-free); `verify_bpath`'s static order is core-gated and
root-termination/no-repeat/`q`-conjuncts are all consistent with gap
ancestors. No conjunct read rules out a terminal B-path through gaps
(`bd ≤ 18`, `q ≤ 9` admissible in principle). Hence universal
`H = 2 ⇒ w ≥ 0` and universal `w < 0 ⇒ H = 1, q ∈ {3,4}` are NOT promoted.
No explicit counterexample is claimed (none constructed; search forbidden) —
the earliest failed implication is precisely the core-ancestor step for
multi-event pre-states. The H = 1 story below does not need it (fusion
bypasses to singles where `q ≤ 4` holds).

## C. Unit-charge single-access fusion theorem (PROVED for H = 1 genuine)

Claim: every genuine `H = 1` low macro has an equivalent single-event genuine
KEEP of the same target slot from the same entry states (same A-charge,
terminal B-credit, weight, endpoint shadows, exit states).

Case A (charged event is terminal): all preceding events have `a = 0`; A
identity by Lemma A (WS-02B); B identity for DELETEs by construction and for
KEEPs by the Sync-corollary (Sync inducted from `Sync(0)` through zero-cost
preservation, WS-02B Lemma C). The terminal pre-states equal the entries;
the fused event reuses the terminal event's full data.

Case B (charged event `j` precedes terminal `i`): terminal is a zero-cost
B-changing KEEP, so WS-02B gives a unique charged DELETE ancestor with
GenDiv and no KEEP between (`H = 1` forces `j` to be that DELETE).
Events before `j`: identities (Sync induction). Event `j`: `d_A ∈ {1,2}`
(`a = 1` + bound + table), one complete A-splay of `x` to the A-root, B
identity. Events between: no KEEPs; active ones are zero-cost DELETEs
(identities). Terminal: zero-cost ⇒ targets the A-root `= x`
(root-termination + anchor); genuine ⇒ `x` marked S; B in entry state;
one B-splay of `x`. Fused single KEEP of `x` from the entries reproduces
both exits (same interpreter, same inputs ⇒ identical output states),
charge `a = 1`, `H = 1`, same `bd`/`q`/`w`, same genuine predicates
(same tables/slot), same exit shadows, same boundary validity
(pre = entry valid; post = original validated exit).

Conjunct-transfer audit: witness-global predicates (`wellformed`,
`link_both`, `child_bound_prop`, `inv.attach/valid`, `compat_pred`) reference
only static slot/port/sig tables — verified by reading each body — hence are
invariant under recombination with identical tables; per-event active-gated
predicates transfer verbatim (A-part against entry A as in `j`, B-part
against entry B as in terminal `i`); `macro_H`, terminal block, threading,
`nev = 1`, A8 (last-event vacuous) all check. This fusion is strictly
stronger than A3 no-op deletion (it merges a state-changing charged DELETE
with a later KEEP); A3's normal form is consistent with Case A but not used
as the proof.

## D. Endpoint-visible `q` identity and negative characterization (PROVED, H = 1)

For genuine `H = 1` (hence fused single KEEP of marked `x`): B unchanged
before the terminal access (§C both cases) and the terminal splay makes `x`
the exit root (target-to-root, WS-02B §C); core-target parent uniqueness
(exact-one-claimant counts, always conjoined) gives `bd_last` = true entry
depth, so `q = ⌊depth_{B_s}(x)/2⌋`. Entry A-depth of `x` is 1–2 (Case A:
terminal `dd`; Case B: DELETE `dd`; both from entry A). Shadow testability:
the verified A-path uses slot-kind links throughout (`a_parent_of`
requires kind 0), and `shadow7` follows kind-0 refs directly, so `x` at true
depth 1–2 appears exactly at a coarse position; the candidate predicate
`∃p ∈ {L,R,LL,LR,RL,RR}: ak[p] = 0 ∧ aS[p] = 1 ∧ aI[p] = x` holds iff the
entry shadow exposes S-key `x` within depth 2 (sidx equality is exact —
no fringe/port false positive; `ak = 0` excludes ports). Negative-edge
characterization for the fused class: `w < 0 ⟺ q ∈ {3,4}` (with `q ≤ 4`),
`depth_{B_s}(x) ∈ {6,7,8}`, `w ∈ {−1,−2}`, `x` shallow in A. Deficit
`δ = q − 2 ∈ {1,2}` exact.

## E. Compensation: investigated, mechanism OPEN (precise obstruction)

Rotation/path-compression facts established: the fused negative edge performs
exactly `d_A ∈ {1,2}` A-prims and `d_B ∈ {6,7,8}` B-prims; both roots become
`x`; entry is Sync-labelled `S(x0)`, `x ≠ x0`. What does NOT follow: no
proved identity converts these into a telescoping per-walk inequality.
Total B-depth-sum has the wrong monotonicity (single rotation changes it by
`+|mid| ≥ 0`); entry-relative `q` does not telescope by itself; any reserve
over B-states would be endpoint-visible (B is in abstract states, so
B-potentials telescope across shared endpoints — legitimate transport) but
no candidate with a proved per-edge deficit law and replenishment analysis
was derived, and inventing an arbitrary Φ would recreate the unresolved
theorem (rejected as tautological per mission §6). Replenishment structure
noted but unlinked: positive slack exists (single-event `H = 2`: `w = 4−q`;
`H = 1, q ≤ 2`: `w ≥ 0`) with no law binding it to deficit edges.
Missing piece, stated exactly: a graph-visible quantity with a proved
per-edge inequality covering `δ ∈ {1,2}` on fused H = 1 negatives plus a
replenishment/boundedness argument — and, separately, closure of the
multi-event H = 2 gap-hole (§B), since hypothetical gap-path H = 2 negatives
(`w = 4 − q` down to −5) lie outside fusion and outside any H = 1 law.
High edges (`w_H = 6 − q`, different relation) are a separate obligation,
untouched.

## F. Upward bridge and IAGS R1 audit

(1) New `q` information: `q = ⌊d/2⌋` universal; `q ≤ 4`/depth ≤ 8 for
singles/fused; endpoint identity `q = ⌊depth_{B_s}(x)/2⌋`; exact deficit
`δ ∈ {1,2}`. (2) Fusion eliminates hidden witness history for the entire
H = 1 negative class (multi-event words → single accesses, proved).
(3) The identity is endpoint-visible (entry B-state; entry A-shadow
predicate) and transports across shared abstract endpoints. (4–5) No
repaying quantity constructed; replenishment unlinked (see §E). (6) The H = 1
class is now a finite single-access problem with exact deficits — materially
easier — but universal cycle nonnegativity still needs compensation plus the
H = 2 gap-hole closure. (7) Remaining, in order: compensating law with
replenishment; multi-event H = 2 `q`-bound (gap ancestors); high-edge
transfer. R1 simplification is substantially (not completely) satisfied for
the decisive H = 1 class.

## G. Scope and non-claims

Applies to the frozen low-edge relation only (single-event bounds use entry
`b_valid`; fused representatives inherit it). Nothing is claimed about high
edges, abstract-only cycles, `q ≤ 2H`, `w_L ≥ 0`, or `NonNegCycles(Ĝ⋆)`.
No solver, no code, no source change. Step 03 remains OPEN; Step 04
unauthorized; Bank25 = 25.

## H. Final verdict

**OUTCOME B — EXACT CREDIT REDUCTION PROVED.** Unit-charge fusion (§C) and
endpoint-credit reductions with the H = 1 negative characterization (§D) are
universally established; the compensating inequality is OPEN (§E).
Recorded limitation: the multi-event universal `q ≤ 4` / `H = 2 ⇒ w ≥ 0`
form (§B) is obstructed at the core-ancestor step by admissible gap internal
nodes under structure-only intermediate validity — isolated, not promoted,
and not needed for the H = 1 results. Step 03 stays OPEN pending a
compensating law with replenishment, multi-event H = 2 closure, and high-edge
transfer.
