# PIVOT-16: NO-TIGHT-DANCE universal attempt — E0, gross/net wall, verdict

## A. Fully-shared tight dance (formal)

A demand set `X` (B-double units) with pools `N(X)` (A-credits via
local/creator/setup eligibility) is a tight dance component iff:
(i) creator/setup-closed (all named pools included); (ii) every starved
setup in play is shared starved+non-starved (maximal, L2/H3-bound);
(iii) no private neighbors (every credit touched ≥2); (iv) `|N(X)|=|X|−1`
(deficient by exactly 1 — the minimal-Hall form; "tight core" `=|X|`
is the peeled-boundary variant, off-by-one tracked explicitly);
(v) all incident local/creator/setup pools saturated in counting sense;
(vi) every relation realized by an actual closed Pair-Access walk
(creator in-epoch (U1), setup = latest arrival (U2), DELETE-setups (L1),
disjoint blocks (H2), EXACTLY-one-starved/block (H3)).

## B. Minimal-Hall → tight-dance bridge (no off-by-one)

Minimal deficient `X` has `|N(X)|=|X|−1` (else a smaller deficient set)
and no privates (else removal preserves deficiency: sole-locally-paid
members are removable since locals drop `2a≥2` vs demand drop 1 —
formalized). Starved members force shared setups (private DELETE pools
(L1) must be shared (no-privates) ⟹ exactly one non-starved co-namer
(H3+L2)); non-starved members are residual-or-tight-sharing. Hence every
minimal deficient set contains a tight dance core; killing all tight
dances kills all minimal deficiencies ⟹ Hall ⟹ U4. Bridge banked.

## C. Dance-cell chronology (one key z)

`s(DELETE z, dA=d>0, 2a_s credits, B frozen)` → quiet `(s,t)` (only-z
DELETE-noops, z A-root, B frozen) → `t(KEEP z, dA=0, dB=D frozen,
q doubles, first-KEEP)` → `u(first non-z, dA(w)>0 (motion, else no
dethrone), a_u≥1)` → `(u,t')` non-z only (else a z-arrival supersedes
`s`) → `t'(KEEP z, setup=s, dA'>0, D' rebuilt post-t)`. Roots: A z→w→z;
B z→(t roots)→w?/rebuild→z. B-depth at `t` = pre-`s` built (frozen);
at `t'` = post-`t` rebuilt. Depths: `D` (pre-s builders), `d` (setup A),
`D'` (rebuilders), `d'` (post-u). All transitions forced by splay
mechanics + quiet/maximality (no choice).

## D. Tight-preserving transition

A transition preserving (E0 + full sharing) must avoid: (A) extra
eligible capacity (any new named pool or credit), (B) private credits
(any pool touched once), (C) sharing destruction (edge/relation loss via
rotations/rooting). Definitions are counting-exact (Hall-level), not
room-based (matching-level) — deliberate (§2 precision).

## E. Equality conditions EQ1..EQk

For the minimal 2-access dance (`X` = all doubles of `t,t'`, creators
empty/starved, `u∉X`): pools `S(2a_s)+L'(2a')` disjoint (distinct
accesses; creators ≠ DELETE/`t'`/post-`t`) give
**E0: `(q_t−2a_s)+(q'−2a') = 1`** (starved-deficit + nonst-residual = 1
exactly). With fat creators `C`: `−Σ_C2a_c` added (creators raise the
bar; deficits must be larger). Forced equalities: setup `a_s` exact;
`q_t,q'` exact depths; locals exact (`q'=2a'` or extremal); creators
all-starved (else LHS drops); sharing exact (one co-namer); order exact
(C). General X: `Σ_E2a_e = R_T−1` (external = residual-sum − 1).

## F–H. Escapes (status)

A (extra capacity): any unnamed→named pool conversion or fresh arrival
breaks E0 (LHS drops). No theorem forcing A in tight transitions (fresh
pools are 2-hop/ineligible). B (privates): sole-locally-paid exclusion
proved (peeling rule, Endgame-E flavor); full private-freedom unproved
(requires tightness everywhere). C (sharing destruction): rotations that
rebuild consumed edges replace creators (U1-latestness) — ruled IN (not
out): destruction makes room (helps), and E0 already assumes the
post-destruction latest creators. None yields a universal escape
theorem; all three are live possibilities that real cycles exploit
(slack everywhere: WQ −40..−70).

## I. Root-divergence analysis

DELETE-setup creates A/B asymmetry for free (A: z→root, B: frozen).
Starved KEEP resolves it (z→both-roots). Dethroner recreates it
(w→A-root). Non-starved sharer needs own divergence (B-deep + A-shallow
rebuilt post-`t`). Per closed cycle, divergence created/exploited/
reassigned in balance — but ZERO-surplus only constrains NAMED pools;
unnamed DELETE-slack (re-roots with A-work, no B-demand) is abundant
yet ineligible. Divergence accounting is exact but non-constraining
(supply exists where Hall can't see it). Not scalar fitting: actual
root/dethrone/arrival operations counted.

## J. Bracketing under equality (gross/net wall)

B-push-down builders must be key-interval-near x (to touch its B-chain);
same keys ⇒ same intervals in A ⇒ builders A-move x. Hence GROSS
motions correlate (shared overlap size). But NET depths don't (signs
independent across separate splays; A-cancellation with B-accumulation
is coherent). Crossing intervals (sharing x without nesting) kill static
D-vs-d bounds. Conditioning on tightness does NOT restore determinism:
cancellation needs motion (credits!) but those credits sit in ALREADY-NAMED
pools (setups/builders — E0 counts them) or unnamed ones (ineligible).
The wall stands under equality conditions. Tried: strict inclusion
(fails: crossing), endpoint movement (fails: returns), orientation table
(LL/RR-dominant but free), zig-zag strictness (minority patterns).

## K. Signature: NONE FOUND (cyclic return kills monovariants)

Every candidate (interval nesting, bracket endpoints, creator rank,
orientation+size, trapped-key count, rebirth order, root orientation,
zig-direction) either returns around closed walks or is direction-free
(builders free). Vector/lexicographic variants same fate. No signature
stated (honest null result after full attack per §§11/17/19).

## L. Cyclic composition: OPEN

Cells compose (attractors exist: trajectories collapse to shallow loops;
extremal pre-states transient-only 22/22). Closure does not force
tightness-breaking (BFS closes extremal cycles that still match with
slack). No composition theorem.

## M. NO-TIGHT-DANCE: OPEN

Not refuted (0 tight dances in 700+ cycles; shape-hunt 133 cycles 0 hits;
dance 6/66 never tight). Not proved (E0-dance coherent at every step;
temporal root-moving resolves all local tensions; exact tightness is a
joint marginal-lucky conjunction — individually realizable, jointly
unobserved, jointly unrefuted).

## N. U4 after minimal-Hall: OPEN (conditional on M)

M ⇒ no deficient X ⇒ Hall ⇒ injection ⇒ U4. Chain ready, premise open.

## O. total_overflow ≤ total_slack: OPEN (700+ green)

## P. COARSE-DOUBLE Q_B ≤ 2A: OPEN (composition `Q−2A=overflow−slack`
ready; unrefuted; §26/§38 never fired — no tight dance found, so no
(i)/(ii)/(iii) classification triggered)

## Q. ONE weakest missing statement (NO-TIGHT-DANCE itself, sharpened)

**E0-DANCE UNREALIZABILITY:** no closed walk realizes, for one key,
`s(DELETE, a_s) < t(KEEP, (0,q_t)) < u < t'(KEEP, (a',q'))` with shared
setup `s`, zero-fat-creators for all involved doubles, and
`(q_t−2a_s)+(q'−2a') = 1` (plus the fat-creator generalization
`−Σ_C2a_c`). This single equation + order + sharing is the weakest
U4-completing claim (kills minimal-X directly). Why it resists: each
conjunct (extremal depths, tight locals, starved creators, sharing,
exact over-by-1) is individually coherent; only their conjunction is
unobserved; no single conjunct is false (S1 unrefuted; §28 honesty:
no falsity witnesses exist — the gap is joint, not local).
Lean gap: block/access model + E0 statement (~150 lines on top of
green U1 kernel); GCStaticGenealogy/GCStaticVine preserved.
