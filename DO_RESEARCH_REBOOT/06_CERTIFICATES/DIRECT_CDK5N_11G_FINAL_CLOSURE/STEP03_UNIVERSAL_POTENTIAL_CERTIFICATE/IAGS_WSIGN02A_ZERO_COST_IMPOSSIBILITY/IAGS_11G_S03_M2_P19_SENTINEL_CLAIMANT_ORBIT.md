# IAGS-11G-S03-M2-P19 — Sentinel-Claimant Orbit and Excess-Credit Cycle Rigidity: Exact Mechanisms, No Sign Leverage, Route Abandoned

Mission: M2 subordinate Box P19 (Stage 11G Step 03, no pipeline extension).
Entry HEAD `c814d4b` (verified on `coarse-double-branch`; no other changes).
Method: source-exact proof only. No solvers, code/graph/budget changes, no
new stages. Inherits parent-Box reconstruction, WS-02H normal form (with its
conditional suffix), M2 B-only equivalence, Steps 01/02, DH-01/CORE-01 with
exact scopes. Verdict: **OUTCOME F — SENTINEL-CLAIMANT ROUTE FAILED**
(see §P for the precise obstruction; valid lemmas preserved in §§C–L).

## A. Checkpoint and frozen contract

`G⋆ = G_AF`, `w_H = 6−q_H`, `E^H_w(s,t) ⟺ ∃m(E^OM_w ∧ E^MO_0)` (shared
midpoint), no root-termination/no-repeat/`q`-normalization/new coordinates/
narrowing/mask-exclusion/repairs/solvers/budget changes/Step 04. Bank25 = 25.

## B. IAGS Box B_P19

`T_P19`: high-only sign via sentinel-claimant orbit structure.
`C_P19`: (1) deterministic post-root orbit; (2) claimant validity analysis;
(3) order restrictions; (4) `q_H = 9` structural case; (5) exact excess-rotation
effects; (6) transition dynamics; (7) closed-walk sign or countercertificate.
`I_P19`: M2 equivalence, WS-02H normal form, frozen B-controller, anomaly
ledger. `U_P19`: whether the orbit mechanism constrains negative cycles.
`β_P19`: orbit ⇒ transition structure ⇒ sign constraint (first two arrows
proved; the last fails — see §P).

## C. Sentinel-claimant definition (PROVED)

`P_19(b) = {i ∈ 0..8 : (kl_i=0 ∧ rl_i=19) ∨ (kr_i=0 ∧ rr_i=19)}`
(node-child = kind-0). Gap slots can never claim: full `b_valid` forces
`kl=kr=2` on slots `≥9` (orbit analysis assumes fully valid entry states,
where this holds). Phantom refs `20..31`: unconstrained by any validity
conjunct (all count/parent/side loops range over `0..18`), but fully inert
for path/orbit logic — `f_b` ranges over `0..19` only, claimant counts and
side/static checks never match them (PROVED by code reading; affects
neither orbit selection nor credit predicates, though phantoms may ride
inside moved subtrees).

## D. Parent-multiplexer selection theorem (PROVED)

`f_b = b_parent_of` scans `i = 0..18` with last-match-wins ITE updates, so
for the sentinel: `f_b(19) = 19` iff `P_19(b) = ∅`, else `max P_19(b)`
(single parent with both refs 19 yields that same index — no anomaly).
Direction: `b_side_of(19, c)` is TRUE iff `kr[c] = 0 ∧ rr[c] = 19`
(right-claims, whether or not left also claims); FALSE for left-only
claimants (par `= 19` never equals any loop index). No uniqueness of
claimants assumed; max-selection is many-to-one (defeats any claimant-based
injection a priori).

## E. Deterministic post-root orbit theorem (PROVED)

Fix fully valid `b`, marked core target `x`, true depth `h ≤ 8`
(core-only ancestor chain, distinct nodes, root last — parent uniqueness
from claimant counts, strict depth decrease, dep-0 ⟺ root). `verify_bpath`
forces `p_{k+1} = f_b(p_k)` on the static entry tree (never recomputed).
Root is unclaimed (`tot == 0`), so `p_{h+1} = 19` always. Case A
(`P_19 = ∅`): `f_b(19) = 19`; suffix constantly 19 (PROVED). Case B
(`P_19 ≠ ∅`, selected `c`, `r = depth_b(c)`): `19 → c → par(c) → … →
root → 19`, an exact cycle of period `r + 2` (chain nodes distinct by
strict depth decrease; `19` distinct from slots; first return to 19 takes
exactly `r + 2` steps). Genuine root-terminated reasoning is not imported
(high compiler lacks it) and not needed — the orbit is pure `f_b`
iteration. Distinguished: infinite mathematical orbit vs finite witness
prefix `p_0..p_d` (`d ≤ 18`) vs prim-used subset (`path[0..t+3]`-style
muxes); only the prefix must satisfy per-step conjuncts.

## F. Claimant-side and BST-order restrictions (PROVED)

Per-step static checks apply only for core ancestors and compare the
*witness* side against `trank(x)` vs `2·slot+1` (static crank order, which
valid-tree intervals enforce on core links — so genuine ancestors pass
automatically). NULLB steps: `is_anc_core` false (static vacuous);
`bdir` forced FALSE (no `i == 19` match). Detour step `19 → c` (core):
side = TRUE iff right-claims-19; static check then demands exactly
`trank(x) ≥ 2c+1` (right) or `< 2c+1` (left-only) — a rank-interval filter
on `x`, PROVED from the conjuncts. Consequences: (i) self-claim `c = x`
is *sufficient* (rank equality satisfies the inequality) but only with a
right-side claim (`2x+1 ≥ 2x+1`; left-only self-claim is inconsistent) —
never necessary; (ii) short detours admit many targets (single weak
inequality), so `c = x` is REFUTED as a universal requirement (constraint
form admits `c ≠ x`; no SAT witness claimed); (iii) `x` is constrained to
rank-interval compatibility, NOT subtree containment — rank equality of the
path sides does not imply `x ∈ subtree(c)` (intervals, not membership).
Truncated detours impose only the corresponding prefix subset — no
promotion to full-subtree claims.

## G. Complete versus truncated detour classification (PROVED scope)

Full detour `c → … → root` adds one rank inequality per core ancestor;
satisfiability = `x` lying in the resulting interval (possibly empty —
then that detour is unsatisfiable for that `x`, a genuine filter).
Truncations (witness ends mid-detour) impose only prefix constraints.
Repeats add nothing new (same `(ancestor, side)` pairs rechecked).
No universal forced `c = x`, no forced subtree membership, no forced
spine structure beyond what each step's inequality states.

## H. Maximum-credit `q_H = 9` source-level analysis (necessary conditions
PROVED; satisfiability OPEN)

`w_H = −3 ⟺ q_H = 9 ⟺ d = 18` exactly (`2·9 ≤ d ≤ 18`). Room exists:
`h + 2 + r ≤ 18` always (chain + sentinel + detour-to-root), with repeats
allowed (no no-repeat conjunct) to fill all 19 entries. Necessary
conditions for any valid `q_H = 9` witness: (i) declared depth exactly 18
(9 pairs, last `rotB` sets `root := x`); (ii) a suffix orbit (clean-NULLB
or cycled detour) satisfying parent/side/static checks at every step,
hence rank-compatible `x` per §F; (iii) full endpoint validity on the
9-pair rotation outcome; (iv) genuine `diff` (automatic for `d ≥ 1`:
every firing prim strictly rewrites refs — acyclicity forbids no-op
rotations). None of (i)–(iv) is contradictory; none is shown satisfiable:
**`w_H = −3` stays UNKNOWN**, with strictly more structure than the
timeout ledger (the admissible witness shape is now characterized,
not merely unsolved).

## I. Excess-rotation primitive equations (PROVED)

Per prim: child-field writes only at real `{x,p,gp}` (19 never matches);
NULLB reads alias slot 0 (`muxb` default); transient sentinel roots
possible *only* via last-pair zigzag `rotA` with NULLB `xA` (`pwr` TRUE),
always overwritten by the following `rotB`/zig to `root := x` — final
roots never sentinel (endpoint `b_valid` would reject them anyway).
Zig/rotB with NULLB `p` writes `(0,19)` into the target's rotation-side
child. Parity end-behavior for `d ∈ {14..18}` verified casewise: final
`root = x` unconditionally (for `d ≥ 1`, which genuineness forces).

## J. Clean-source versus claimant-source endpoint transformations
(PROVED lemmas, no sign consequence)

Forced-creation law: from a clean state (`P_19 = ∅`, hence all-NULLB
suffix), any excess depth `d > h+1` forces a kind-0 sentinel child at the
marked target `x` in the endpoint (last prim's `p`-operand is provably
NULLB; the `(0,19)` write is unconditional and survives as the final prim).
Parity/side refinements: odd-`d` zig with NULLB `p` always creates at `x`;
`d = h+1` zigzag creates; `d = h+1` zigzig-even is the unique clean case
(all operands real, `gp`-NULLB adoptions no-op). Destruction/overwrite of
claimants is compatible (later prims rewrite fields) but never forced.
Transition classes `∅→∅`, `∅→nonempty`, `nonempty→∅`, `nonempty→nonempty`
are ALL compatible with the conjuncts — no direction is forced, no count
is monotone, and max-selection defeats injection. Claimant fluidity is
total: no claimant-count reserve can work (independent confirmation of the
WS-02F warning, now with mechanism).

## K. Sentinel-claimant transition dynamics (COMPATIBILITY, not law)

No per-edge law links `P_19` across a transition beyond §J's write
mechanics. Zero-weight edges (`q ≤ 6`) run the same prims and can
create/preserve/destroy claimants exactly like negative ones — weight never
enters the write equations. Distinct marked targets alternate freely
(target independence per edge). The intended "regeneration forces
compensating transitions" has no source basis: every P19-dynamics class
is admissible. Self-loops are impossible for *every* high edge weight
(conjoined `diff` over structural fields ⇒ `bs1 ≠ s.b` ⇒ no fixed point)
— PROVED, weight-blind, length-1 only.

## L. Closed B-orbit restrictions and short-cycle falsification
(honestly negative)

Two-cycles need `q_0 + q_1 > 12`; reverse high splays with sufficient
declared depth are not structurally excluded (target independence,
detour compatibility, validity flexibility all permit them in principle).
Longer cycles: no invariant found (core-membership conditional on
unproved excess monotonicity; depths sign-indefinite per WS-02E/F;
`P_19` fluid per §J; finite-state size bounds lengths, never signs —
explicitly not used as proof). No forced restoring transition, no
return-weight bound, no decomposition with weight consequences exists in
the frozen predicates. Short-cycle exclusion fails (only length-1 ruled
out, §K); universal exclusion unproved; countercertificate refused
(no complete valid witnesses constructible here — correctly, per R4).

## M. Universal sign certificate or exact unresolved obstruction:
NEITHER — obstruction precisely identified

No `Σq_i ≤ 6|C_B|` law follows: declared credit is witness-free up to
full-validity filtering, which constrains shapes, never sums; detour
rank-compatibility filters *which* `(b,x)` admit long traces but imposes
no cross-edge force. No `R(t) − R(s) ≤ w` reserve is constructible from
orbit mechanics (all per-prim effects sign-indefinite or weight-free).
The obstruction is exact: **sentinel/orbit analysis completely determines
path shape admissibility and rotation mechanics, but the frozen relation
imposes no weight-relevant restriction on closed B-walks beyond per-edge
`q ≤ 9`** — the bridge `orbit ⇒ transition structure ⇒ sign constraint`
fails at its final arrow, with the first two arrows proved.

## N. Negative B-cycle and full-graph lift: NOT PROVED (correctly withheld)

No valid negative B-only cycle exhibited (would require complete
19-slot states, declared paths/directions, replay, validity, and
`Σq > 6n` — beyond hand derivation). The M2 lifting theorem stands ready
*if* such a cycle were ever certified (fixed-shadow lift is unconditional),
but nothing is lifted and no Step 03 premise is refuted.

## O. IAGS R1–R4 audit

R1: proved orbit/order/prim/transition/self-loop theorems are genuine
source mathematics, but none removes a sign-relevant obligation —
rank-compatibility filters admissibility without touching weights;
forced-creation changes B-state fields without constraining closed-walk
sums; self-loop exclusion is length-1 only. Per R1's explicit bar
(examples 1–5: no `-3` impossibility, no negative-subclass exclusion from
closed walks, no cycle-constraining transition law, no sign-problem
reduction, no return-weight bound), OUTCOME B is not earned; OUTCOME A
was never in reach of this route. R2: M2 equivalence used unchanged;
WS-02H suffix kept conditional (clean vs detour distinguished, never
collapsed); CORE-01/DH-01 monotonicity never imported beyond genuine
traces; `-3` UNKNOWN preserved; no ordinary-BST proof substituted where
sentinels occur. R3: no repairs, no `19`-forbidding, no normalization,
no `q` replacement, no narrowing, no coordinate/mask/signature changes,
no M1/M3 work, no solvers/searches/budgets. R4: every claim labeled;
no SAT-from-unconstrained-pointer (detour satisfiability explicitly
OPEN); no UNSAT without contradiction (`-3` stays UNKNOWN); no cycle
claims from traces; no universal sign from partial exclusions; no
claimant monotonicity asserted.

## P. Final verdict: OUTCOME F — SENTINEL-CLAIMANT ROUTE FAILED

The orbit is deterministic, the order filters exact, the prim equations
complete, the `q_H = 9` shape characterized — and none of it constrains
closed-walk signs. First exact obstruction: *path-shape admissibility
(rank-interval compatibility) is orthogonal to declared credit magnitude
and to closed-walk weight accumulation; the frozen predicates impose no
weight-relevant closed-orbit restriction beyond per-edge `q ≤ 9`.*
Valid lemmas (§§C–K) preserved; route abandoned; no successor spawned.

## Q. Residual M1/M2/M3 obligations and HARD STOP

M1 (low compensation): OPEN, untouched. M2: B-only equivalence PROVED;
orbit/order/prim analysis PROVED; high-only sign OPEN (residual exactly
`Σq_H ≤ 6n` over valid B-splays, `-3` UNKNOWN). M3: untouched.
Step 03 OPEN; Step 04 unauthorized; Bank25 = 25.

**HARD STOP.**
