# IAGS-WS-02H — High-Edge Excess-Credit Normal Form: Post-Root Trace Semantics, Endpoint Interface, and Negative High-Edge Cycle Obligations

Mission: `IAGS-WS-02H-...`, entry HEAD `18be385` (verified on
`coarse-double-branch`; no other changes made).
Method: mathematical proof from frozen source text only. No coding, no solvers,
no source/graph changes. Inherits WS-02A..WS-02G with exact scope (failed
reserve/recurrence routes not reopened; their valid identities reused).
Verdict: **OUTCOME B — NORMAL FORM PROVED, SIGN OPEN** (see §M).

## A. Frozen theorem, checkpoint, inherited scope

Step 03 target `∀C closed in Ĝ⋆, w(C) ≥ 0` unchanged; Step 04 unauthorized;
Bank25 = 25. High compiler `STRICT_HIGH_COMPILER.build_shigh` (90 lines,
read in full), product `CW_PRODUCT_COMPILER` (OM hides `t`, MO hides `s`,
MO weight 0 only, `w_H = 6 − q`), projections `S03_EDGE_PROJECTIONS`
(OM keeps `QO+QM`, MO keeps `QM+QO2`), graph interfaces G01/G02 (ledger:
`w_H = −4` UNSAT, `−3` UNKNOWN, `−2..1` SAT, `2..6` SAT; G01 decided-fragment
claim; G03F return-path equivalence; DH-01 high-only work OPEN/conditional),
CORE-01 high monotonicity (audited, not reopened). Inherited: low-edge
theorems (H ≥ 1, `q_L ≤ 4`, fusion, causality, rotation/transfer/mass
identities); no low result is imported into the high compiler.

## B. IAGS Box BH

`T_H`: exact excess-credit endpoint normal form + a nontrivial Step 03
cycle constraint. `C_H`: (1) true-vs-declared depth separation; (2) suffix
characterization; (3) exact post-root rotation analysis; (4) midpoint/
endpoint preservation; (5) structural restriction on the anomalous class;
(6) bridge to return-path/cycle obligations. `I_H`: compilers, graph
theorems, anomaly ledger, scoped monotonicity. `U_H`: whether excess prims
induce constrained endpoints or genuinely new transitions, and whether those
can be excluded from negative cycles. `β_H`: trace semantics ⇒ endpoint
normal form ⇒ cycle constraint (each arrow proved or explicitly left open).

## C. True depth versus declared depth (PROVED setup)

Entry `s.b` carries full `b_valid` + `b_tree_valid`, so gaps are childless
and the marked core target's true chain uses core slots only:
`0 ≤ h = depth(x) ≤ 8`, all ancestors core, root core (cycle argument:
9 core nodes, exact-one-parent counts, strict depth decrease forbid a
non-core root). Declared `d = bt.bd[0] ≤ 18` (verify_bpath bound, conjoined).
Credit `q_H = ⌊d/2⌋` from conjoined `2q ≤ d < 2q+2` (integer DAG). Hence
`q_H ≥ 5 ⟺ d ≥ 10 > h`: every `w_H ≤ 1` edge necessarily runs an excess
trace; negatives (`w_H < 0 ⟺ q_H ≥ 7`) always do. `q_H ≤ 9` universally
(explicit `LE(q,9)`; independently `bd ≤ 18`), so `w_H ≥ −3` and
`q_H = 10` (`w_H = −4`) is impossible by source text alone — solver-free
proof of the recorded UNSAT. `w_H = −3` forces `bd = 18` exactly.

## D. Exact root/sentinel path behavior (PROVED)

`bpath[0] = x`; parent links are forced through the true chain
(`path[1..h]` = unique ancestors: exact-one-parent counts make
`b_parent_of` deterministic; depths strictly decrease to the unique
depth-0 root, all distinct). Root has no kind-0 claimant
(`tot == 0` conjoined), so `path[h+1] = NULLB` is FORCED. Beyond:
`parent(NULLB)` = NULLB iff no slot carries a kind-0 child ref `19`;
such refs are NOT forbidden by any validity conjunct (interval/count/bpar
machinery ranges over `0..18` only) — verified absence of constraint —
so the suffix is CONDITIONAL: all-NULLB iff the state has no `(0,19)`
claimants, else a detour through the last-match claimant and onward
(then subject to actual-side/static-order conjuncts, which can still
disagree and rule out specific detours). Item-by-item (§7):
(1) non-root core parent unique ✓; (2) true root parentless ✓;
(3) sentinel returned ✓; (4) sentinel-of-sentinel conditional (above) —
not universally NULLB; (5) unexpected kind-0 `19`-claimants admissible
(proved by absence of any forbidding conjunct); (6) beyond-root dirs forced
FALSE (`b_side_of` with `par = NULLB` never matches), static order vacuous
(`19 ≮ 9`) — degenerate but consistent; (7) NO hidden root-termination or
no-repeat in the high compiler (PROVED by exhaustive 90-line read: no such
import or conjunct, unlike the low repairs).

## E. Pair and zig gate classification (PROVED)

`splay_event` gates fire purely on declared `d`: pairs `t+2 ≤ d` (t even),
zig iff `d = t+1`, all within loop bounds for `d ≤ 18`. Levels `t+2 ≤ h`
are ordinary genuine prims (same operands/order as a canonical splay;
top-boundary `gp = NULLB` is correct absent-grandparent handling).
Levels beyond `h` are excess prims mixing the real target `path[0]`
with suffix/detour operands. No prim fires for `d = 0` (then `bs1 = s.b`,
contradicting conjoined genuine `diff` — so every valid genuine high edge
has `d ≥ 1`).

## F. Post-root rotation equations and endpoint normal form (PROVED)

Per prim (`b_single_rot`, verified assignments): child-field writes occur
only at real `{x,p,gp}` indices (`19` never matches the `0..18` write
muxes); NULLB operands read by aliasing slot 0 (`muxb` default); transient
`root := NULLB` is possible mid-trace (zigzig rotA with NULLB `xA` and
`pwrA`) but never survives: the LAST firing prim is always rotB/zig with
`x = path[0]` and true root-update, so for every valid genuine high edge
**`root(g.b) = x` (marked core)** — target-to-root with no need of
root-termination or no-repeat lemmas. Genuine-prefix effects are ordinary
splay work; excess prims rewrite real path/fiber slots with alias-derived
values under the same gates. Endpoint constraints (all conjoined):
full `b_valid` + `b_tree_valid` on `g.b` (real root, childless gaps,
one-parent, depths, gap-parents-core, intervals). Normal form:
`B_t = FullDeclaredPrimSequence(B_s, x, suffix, dirs)` ending at marked-core
root `x` in a fully valid tree — the anomaly is localized to subtrees plus
the witness-held `q_H`; the root/label skeleton is canonical.

## G. Low-continuation forcing (PROVED graph-level restriction)

Destination `t` carries `t.b.root = x` but shadow label `t.aI[0] = g.v`.
Low-edge entry sync demands `s.aI[0] == muxb(...broot...)`; with core root
this forces exact slot equality, so a low edge can follow `t` iff `x == v`,
and an `x ≠ v` high edge forbids every low successor: any walk continuing
past it must use high edges. (The converse is permission, not guarantee:
`x == v` merely satisfies sync.) This is a proved mixed-walk restriction
deriving directly from the normal form.

## H. High target, fiber label, A-shadow interface (PROVED audit)

`x = bt.bT[0]` (core `<9`, marked via `s.mu`) vs `v = g.v` (`<9`, marked):
NO equality conjunct exists in the 90-line compiler (verified) — `x` and
`v` are independent, both marked core. Consequences: `root(g.b) = x` (§F);
`root(g.b) = v ⟺ x = v`; destination shadow root is `v` regardless of `x`;
A-side is loose — no `AState`, A-replay, `H`, sync, shadow-match, or
A-target coupling exists in `build_shigh` (verified by full read; only
`state_valid7` labels, mu/sig equalities, `t.aS[0]`, `t.aI[0] = v`,
`marked(v)`). High B-target selection is A-independent. Assuming
`x = v`, low-style sync, or A-replay for high edges is therefore unsound;
WS-02C fusion does not transfer. Fiber `v` is the sole marked-label channel
OM→MO→`t` (midpoint preservation: OM hides `t`, MO hides `s`, weight split
`6−q | 0`).

## I. Per-weight anomalous classification (PROVED bounds; statuses kept)

`q_H = 10` (`w = −4`): impossible (C). `q_H = 9` (`w = −3`): requires
`bd = 18` exactly (9 pairs; necessary condition proved; satisfiability NOT
claimed — UNKNOWN preserved with timeout provenance). `q_H ∈ {5,6,7,8}`
(`w ∈ {1,0,−1,−2}`, all SAT-certified): necessarily excess (`d ≥ 10 > h`);
retained as genuine obligations — no exclusion, no naturalness argument.
`q_H ≤ 4` (`w ≥ 2`): `d ≤ 9`, excess undetermined. No family is promoted or
deleted; SAT/UNKNOWN/UNSAT statuses preserved exactly as ledgered.

## J. Contracted-high midpoint preservation (setup, verified from code)

`E^H_w(s,t) ⟺ ∃m (E^OM_w(s,m) ∧ E^MO_0(m,t))` over shared fiber vars
(CW product + projections as read); C1/C2 extension (`t := m-image` always
satisfiable) inherited, not re-proved. The normal form applies at OM
endpoints; MO is B-identical shadow relabeling to `v`.

## K. Return-path and negative-cycle implications (one proved; rest open)

Inherit G03F equivalence (negative edge + cheaper return ⟺ negative closed
walk; restated, not altered). New: (i) §G continuation forcing — return
paths from `x ≠ v` high destinations must begin with high edges, eliminating
mixed returns that start low (a real, if modest, return-path restriction).
No normalization to a cheaper parallel edge was found (correctly not
manufactured: erasing a negative edge with a nonnegative parallel one proves
nothing). No cycle-excluding invariant was found (endpoint outcomes stay
fully flexible within validity). No negative closed walk is exhibited
(correctly refused: that requires a complete valid certificate, not a
suggestive trace). DH-01 high-only constancy and q-average work is untouched;
note its dependency: core-membership constancy along high-only walks used
universal high monotonicity whose rotation lemmas assume genuine-trace
operands — see §L.

## L. IAGS R1–R4 audit + monotonicity applicability audit (R2)

R1: the package (suffix theorem, always-`x` root, excess-prim equations,
`x/v` separation, looser-A proof, continuation forcing, sharp `q`
necessities) is a genuine normal form that eliminates false degrees of
freedom (sentinel roots, A-replay, forced `x = v`, free credit reading)
and localizes the anomaly to subtrees + declared `q` — material reduction
of high-edge endpoint complexity for all downstream cycle/return work;
`w = −3` and cycle exclusion stay explicitly open, so OUTCOME A is not
claimed. R2: WS-02D `q_L ≤ 4` never applied to `q_H`; WS-02C fusion never
imported (interface differs — §H); CORE-01 high monotonicity audited:
its R1–R3 micro-lemmas require the rotated child to lie on marked
ancestor chains, which holds prim-by-prim only up to the true root —
excess prims with sentinel/detour operands fall outside the proved
hypotheses, so high-edge `C`-monotonicity (and DH-01 constancy built on it)
is PROVED for genuine-trace prefixes but CONDITIONAL for anomalous
suffixes; no anomalous-trace extension is asserted. R3: no compiler, graph,
weight, or scope alterations; no narrowing (detours admitted as
conditional). R4: suffix forcing/conditionals, root theorem, interface
equalities/inequalities, `q` bounds, continuation forcing: PROVED; detour
realizability, `w = −3` satisfiability, cycle exclusion: OPEN (preserved);
no counterexample claimed.

## M. Final verdict: OUTCOME B

A universal excess-credit endpoint normal form is established
(true chain + characterized suffix; always-marked-core root; exact
post-root prim semantics; `x/v`/A-shadow interface; continuation forcing;
sharp per-weight necessities). It materially reduces high-edge endpoint
complexity and scopes every downstream obligation, but universal cycle
exclusion and the `w = −3` family remain OPEN.

## N. Remaining Stage 11G Step 03 obligations

`w = −3` satisfiability; low-only compensation (fused H = 1 deficit, still
open per WS-02E/F/G); high-only and mixed closed-walk nonnegativity;
any Step 03 certificate must cover all retained families (low negatives,
zero/positive lows, high `w = 6 − q` incl. anomalous, abstract-only cycles)
or the scope must be re-frozen with justification (not authorized here).

## O. Authorization status and hard stop

WS-02H only. No solvers, searches, compiler/graph/budget changes, no WS-02I,
no Step 04, no Dynamic Optimality claims. Bank25 = 25.

**HARD STOP.**
