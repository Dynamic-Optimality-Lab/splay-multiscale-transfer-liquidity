# PIVOT-15 U4: ONE missing lemma (minimal-X dance elimination)

Status: U4 OPEN. COARSE-DOUBLE OPEN (conditional composition ready).
`Q_B ≤ 2A` unrefuted on 700+ tests. This file states the single weakest
U4-completing lemma, why all stronger forms failed, and the exact evidence.

## A. Exact minimal Hall-deficient structure after U1–U3/L1–L3

Let `X` be inclusion-minimal with `|N(X)| < |X|` (LEFT = B-double units,
RIGHT = A-credits, edges = local/creator/setup). Then `|N(X)| = |X|−1` and
X has NO private neighbors (else a smaller deficient set). Consequences:
(i) every starved X-double's DELETE-setup pool (disjoint from ALL other
pools: DELETE hosts no doubles, builds nothing — L1) is shared, forcing
exactly one non-starved co-namer (H3+L2 leave no other sharer): the dance
`s < D_j < u < D'` (all one key); (ii) every non-starved X-access is
multi-double with tight locals and starved/empty creators; (iii) dual:
failure ⟺ extreme pool-concentration (quantified H4+namers). No
contradiction follows — the dance is dynamically coherent.

## B. Deterministic era definition

`E(s)` = [setup DELETE `s` .. starved KEEP `t` (quiet, only-own-key) ..
dethroner `u` .. non-starved sharer `t'` (setup `= s`)] until `t'`
destroys the sharing relation. Definable from the walk alone. Residuals
assigned: `q_t` (starved) + `(q'−2a')⁺` (sharer). Credits: `2a_s`
(DELETE, dedicated). Eras for distinct setups are access-disjoint at
their setup pools (L2) but share builders/dethroners (overlap — §17:
no useful disjointness/nesting; crossing epochs kill laminar routes).

## C. Bracketing/order theorem discovered (and its limit)

Builder-near ⟺ key-interval-near (to touch x's B-chain, builder key must
bracket x; same keys ⇒ same intervals in A). Hence every B-deepening
builder A-moves x: GROSS motion correlates (shared overlap size). BUT
NET depths don't (signs independent across separate splays): A can cancel
while B accumulates. Interval bracketing is necessary-but-insufficient:
crossing intervals (sharing x without nesting) kill any D-vs-d bound
from statics alone. The correlation needs dynamics (cancellation
control), which is absent. This is the cancellation wall (see D).

## D. Half-pool law (`q ≤ a_s`): OPEN (neither proved nor refuted)

Strongest empirical clue (`q/(2a_s) ≤ 0.5`, 51 rows; era `D ≤ 2d+2`
53/53; strong-form 69/69; single-builder 50/51). Attempted proof via
bracketing: BLOCKED by cancellation wall (C) — adversarial
A-cancellation with B-accumulation is dynamically coherent (separate
splays/rotations/signs), so no deterministic net bound follows; closedness
doesn't forbid finite cancellation patterns. Attempted refutation
(greedy-steered discrepancy maximization + targeted cancellation
construction): FAILED to violate — and revealingly: penalizing A-motion
prevents B-deepening entirely (myopic gradient ~0), i.e. interval-sharing
forces joint motion; you cannot grow B-depth without A-motion, but NET
depths still decouple via cancellation. So S1 is: unproved (wall),
unrefuted (all attacks bounce off), possibly false in principle.

## E. Same-creator residual fan-in theorem

Bounded: distinct edges per namer (H4, `O(dB)`); starved namers bring
private DELETE-setups (L2); non-starved namers bring locals. Residual
(left-over after locals+setups) fan-in is empirically ≤1 per starved and
tiny overall, but no universal ≤2 bound proved (needs S1 fragment:
setup-deficit control). Status: BOUNDED-SHARING (exact bounds banked),
not closed.

## F. Setup-sharing/dance capacity theorem

Per-dance demand (`q_starved + residual_nonst`) vs `2a_s`: exactness
(tight/over) never observed (dance 6/66, tight-pools 0; bubble-concentration
unconstructible — mutual dethrone forces per-key setups, L2 defends).
Needs S1 (`q ≤ a_s`) + residual cap. Status: OPEN (conditional on S1).

## G. Minimal dance-cycle analysis

Alternating setup→starved→creator→non-starved→setup cycles are coherent
(each step dynamically realizable; §16 monovariant hoped-for strict
interval movement fails — everything returns on a closed walk; the
relation to kill must be acyclicity of dance-steps, but dance-steps are
temporally cyclic, and key-direction gives no strictness (builders free)).
Peeling (leaves = starved-with-empty-creator into setups; settled pools)
gets stuck exactly at contested tight dances. No kill. Status: OPEN.

## H. Per-era capacity: OPEN (needs S1)

S1 ⇒ era demand ≤ `2a_s` + small residuals ⇒ S2 (with overlap accounting).
Without S1, eras can be over-tight in principle. Per §19/§20: S1 unproved
(not false) ⇒ S2 unproved ⇒ S3 = U4.

## I. Closed-component capacity: OPEN

## J. U4 overflow_capacity: OPEN

## K. total_overflow ≤ total_slack: OPEN (holds 700+ tests)

## L. COARSE-DOUBLE Q_B ≤ 2A: OPEN (composition `Q−2A = overflow−slack ≤ 0`
ready; unrefuted everywhere; §26 never triggered)

## M. B ≤ 3A: conditional on U4 + banked C.ZIG (`Z_B ≤ A`, mechanical
assembly V1–V3 still open — unchanged, no new campaign started)

## N. ONE exact remaining lemma (weakest U4-completing)

**NO-TIGHT-DANCE:** There is no closed-walk-realizable tuple
`(s, D_j, u, D', pools)` with: `s` DELETE-setup shared by starved-KEEP
demand `D_j` and non-starved demand `D'` in dance order, all incident
pools (setup `2a_s`, sharers' locals, involved creator pools) exactly
tight (`demand = capacity`, no slack), no private neighbors, and creators
as specified (in-epoch, starved-or-fat as needed for tightness).
**Why this completes U4:** minimal-X (A) forces exactly this shape; ruling
it out leaves no deficient set ⇒ Hall holds ⇒ injection ⇒
`total_overflow ≤ total_slack` ⇒ U4.
**Why stronger forms failed:** S1 half-pool (cancellation wall — coherent
adversarial cancellation; greedy/census never violate but can't certify);
S2 era (needs S1 + overlap control); S3 = U4 itself. Smallest witnesses:
none falsifies S1 (all attacks fail = support, not refutation);
S2/S3 subsume. So the missing lemma is NOT a stronger inequality but the
dynamic unrealizability of the tight configuration.
**Lean gap:** block/access model + L1/L2 + NO-TIGHT-DANCE statement (~200
lines); U1 descent kernel stands green.
**COARSE-DOUBLE remains unrefuted** (700+ cycles, extremal incl.).
