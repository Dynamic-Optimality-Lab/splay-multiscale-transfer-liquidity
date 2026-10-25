# IAGS-11G-S03-M2-CYCLE — Universal High-Only Sign or Certified Countercertificate: Deterministic Witness Structure, Endpoint Filters, and the Irreducible Sign Gap

Mission: direct M2 sign-or-countercertificate campaign (no pipeline extension).
Entry HEAD `9ff0cee` (verified on `coarse-double-branch`; no other changes).
Method: source-exact proof only. No solvers, code/graph/budget changes, no
new stages. Inherits M2 B-projection/equivalence, WS-02H normal form, P19
orbit analysis, COREK retraction, KD01 rectangularity, Steps 01/02/11F,
G03/G01/G02 ledgers with exact statuses. Verdict: **OUTCOME F — NO NEW
SIGN LEVERAGE; NO COUNTERCERTIFICATE** (valid partial theorems preserved;
see §Q–S).

## A. Checkpoint and freeze

R1-T/R2/R3/R4 preserved: `NonNegCycles(Ĝ⋆)` target; `w_H = 6 − q_H`;
`E^H_w ⟺ ∃m(E^OM_w ∧ E^MO_0)`; Z3 frozen, Int-exact, `(μ,b,α,σ)`, `h = 2`,
`T = 266`; no Step 04, Bank25 = 25. Read authoritatively: freeze/dependency
docs, parent reconstruction, all listed IAGS/Step-02/Step-01 records and
sources (M2 B-only relation, WS-02H/P19 mechanics, COREK/KD01 equivalences,
CW product + projections, G01 contraction, G02/G03 ledgers).

## B. IAGS Box definition

`T`: `Σq_H ≤ 6|C_B|` over all closed B-walks, or a fully certified negative
B-cycle lifting to the frozen graph. `C`: exact B relation; cyclic
participation/return analysis; envelope equivalence; independent signed
mechanism; countercertificate or explicit obstruction. `I`: as above.
`U`: whether anomalous declared credit admits a negative closed B-walk.
`β`: witnessed transitions ⟹ cycle sign *or* certified counterexample —
neither established (see §§L–M).

## C. Exact negative-credit classification (PROVED setup)

`q_H = ⌊d/2⌋`, `d ≤ 18` (verify_bpath, unconditional), so `w_H ≥ −3`.
`q_H = 10` (`w_H = −4`) is UNSAT by frozen text alone (`q ≤ 9`
conjoined; `2·10 ≤ 18` impossible) — independent source proof
corroborating, not replacing, the solver UNSAT. Table: `−4` IMPOSSIBLE
(proved); `−3` (`d = 18` exactly) UNKNOWN (preserved verbatim incl.
timeouts); `−2,−1,0` SAT; `+1` SAT-contracted with standalone OM timeout
(recorded as stated; no reconciliation beyond C1/C2 expansion, which is
cited not executed); `+2..+6` per frozen ledgers (OM +2..6 SAT;
contracted +2 UNKNOWN-by-timeout, +1/+3/+4/+5/+6 SAT — preserved exactly,
no inference across timeouts).

## D. Deterministic witness structure (PROVED — new)

For fixed B-state and target, the B-witness is functionally determined:
`path[0] = x`; `path[k+1] = b_parent_of(path[k])` (deterministic mux,
unique parents where counts force them); `bdir` forced by actual sides;
static order is a check, not a choice; `q = ⌊d/2⌋` forced by `d`; replay
deterministic. The ONLY witness freedom is the declared length `d`
(`0 ≤ d ≤ 18`), subject to per-step static compatibility and endpoint
validity. True-chain steps auto-satisfy static order (interval-implied
crank order — proved from `b_valid` children intervals + rank bounds);
NULLB steps are vacuous (side forced FALSE); detour steps impose the P19
rank-compatibility filters (necessary, not sufficient). No `q`
renormalization, no root-termination/no-repeat import (verified absent).

## E. Return-path and cyclic participation (proved framework, no bound)

G03F equivalence inherited (pure graph theory): negative B-edge needs a
return path of weight `< r`. Structural facts: self-loops impossible for
ANY high edge — `diff` conjoined over structural fields forces
`bs1 ≠ s.b`, so no fixed point exists (PROVED; length-1 cycles excluded
universally, weight-blind). Beyond length 1: reversal needs a valid
declared-depth splay back; zero-weight (`q = 6`) returns are admissible
in principle (`d ∈ {12,13}` still anomalous, fully legal); detour
satisfiability is per-witness, not universal. No forced positive return,
no excluded negative edge (except self-loops), no two-cycle exclusion —
each would require universal statements over all B-pairs that the
conjuncts do not support.

## F. Worst-credit edge envelope (PROVED, sign-neutral)

`Q_max(b,b') = max q` over valid witnesses (finite set, attained) and the
min-weight parallel-edge substitution preserve closed-walk negativity in
both directions (endpoints fixed; original witnesses retained). Stated and
proved as combinatorics; explicitly NOT sign progress (per R1).

## G. Signed mechanisms attempted and refuted/abandoned (all OPEN or dead)

D1 potential: no `Φ_B` constructed — endpoint-difference circularity,
sign-indefinite transfers (WS-02E/F), zero-weight mimics (below).
D2 decomposition: no telescoping-plus-nonnegative-residual found; residual
nonnegativity is the original difficulty restated. D3 exclusion: only
self-loops (no weight content). D4 forced return: no invariant; zero-weight
returns admissible. D5 counting/amortized bound: declared depth free up to
validity; validity is shape-, not sum-, constraining. Rank/depth/reserve
routes remain abandoned per WS-02E/F/G (not reopened; their identities
reused only as stated).

## H. Anomalous sentinel/excess adversarial audit (mechanism confirmed, no sign)

P19 orbit/detour/static analysis stands as the correct trace mechanics.
New check: endpoint `b_valid` forces gap slots childless (kind-only), so
detour prims that leave kind-0 gap children are UNSAT — a REAL filter on
detour witnesses. But: clean-state excess splays never touch gaps (path
nodes are core-or-NULLB; NULLB writes nothing), so the filter binds only
detour cases, where satisfiability remains instance-dependent (neither
universal failure nor universal success provable by hand). Sentinel
aliasing, selective writes, transient vs final roots all behave as
previously derived; no new sign-relevant restriction emerges. `q_H = 9`
needs `d = 18` + full detour cycling + rank compatibility + valid endpoint;
none of it is contradictory, none satisfiable-by-proof. UNKNOWN preserved.

## I. Zero-weight stress test (route-blocking, as anticipated)

`q_H = 6` (`d ∈ {12,13}`) edges perform genuine deep splays with full
endpoint validity and arbitrary B-topology effects at weight exactly zero.
Hence: no potential can be forced by B-change magnitude; no return path
must be positive; no claimant/depth invariant can carry a sign; any
unsigned structural law is compatible with a weightless restoration.
This single admissible family defeats every candidate in §G that is not
already dead.

## J. Minimal negative-cycle analysis (no leverage)

Simple cycles suffice (inherited). Two-cycles need `q_0 + q_1 > 12`;
longer cycles `Σq > 6n`. No length admits a universal exclusion (would
require ruling out all reverse splays of sufficient declared depth —
impossible from the predicates, which permit them). No valid cycle of any
length is constructed (correctly refused: single-edge SAT ≠ closed walk;
compatibility ≠ witness). Minimality adds no constraint (no valid
reduction preserves negativity while simplifying structure).

## K. Countercertificate audit: NONE (correctly withheld)

A valid negative B-cycle requires complete 19-slot states with full
validity, exact declared paths/directions/static checks per step,
primitive-by-primitive replay, genuine `diff`, exact `q`, exact closure
`b_n = b_0` incl. `lo`/`hi`, and M2 fixed-shadow lifting with shared
midpoints — none of which is established here. Compatibility arguments,
SAT single edges, timeout records, and plausible detours are explicitly
NOT countercertificates. No Step-03 premise is refuted; no unrestricted
Dynamic Optimality inference is drawn.

## L. Universal M2 sign certificate: NOT PROVED (OPEN, with exact residual)

`Σq_H ≤ 6|C_B|` remains unproved for high-only closed B-walks. Missing:
any source-derived signed law, potential, invariant, or exclusion covering
all valid excess traces, zero-weight transformations, detour satisfiability
variants, and the UNKNOWN `q_H = 9` family. This is the irreducible M2
obligation; nothing in §§C–K reduces it.

## M. Reconstructed M2 lifting (CONDITIONAL bridge, intact)

*If* a B-only sign theorem were proved, M2's NegCycle equivalence transfers
it to the original contracted high graph immediately (inherited, no new
hypotheses needed). The bridge is valid; its hypothesis is open. No Step-03
claim follows (M1/M3/low-high mixing untouched). KD01's interface is
unaffected (rectangularity stands independently). No Step 04.

## N. R1–R4 audit

R1: no new signed theorem, no excluded negative family, no return bound,
no potential, no decomposition, no verified countercertificate — Outcome A
and B both correctly withheld; F is the honest verdict (route explored
exactly as chartered, obstruction precisely located, no disguised
repackaging). R2: all 22 checks hold — exact B relation used; full
endpoint validity (incl. `lo`/`hi`, intervals, gaps) retained and
distinguished from `b_equal`; genuine B-change required; marked targets
kept; `verify_bpath`/parent/side/static order intact; no added
root-termination/no-repeat/`q`-normalization; P19 conditional form kept;
`-3` UNKNOWN preserved; zero-weight and all SAT families retained;
abstract-only/nonprimitive/parallel coverage kept; hidden witnesses stay
per-edge; no low fusion imported; no positive-return assumption.
R3: no pipeline/step/budget/graph/code changes, no new observables, no
sub-campaigns spawned. R4: every claim labeled — PROVED (setup lemmas,
determinism, self-loop exclusion, envelope equivalence, gap-filter
mechanism as conditional); CONDITIONAL (detour satisfiability,
`−3`/return-path existence); OPEN (sign, countercertificate, minimal-cycle
leverage); no UNKNOWN-as-PASS, no invented witnesses, no sampled proof.

## O. Final verdict: OUTCOME F — NO NEW SIGN LEVERAGE, NO COUNTERCERTIFICATE

The B-only cycle problem is exactly formulated (deterministic witnesses,
full endpoint validity, explicit obstruction map), the anomaly ledger is
sourced (`−4` proved impossible; `−3` UNKNOWN preserved with necessary
`d = 18` structure), and every sign-closing route is shown blocked by
frozen-semantics facts (zero-weight structural freedom, detour
satisfiability openness, no invariant). Nothing from the valid partial
results implies, or is presented as implying, nonnegativity.

## P. Residual obligations and HARD STOP

M2 OPEN (universal high-only sign including `-3`; no verified negative
B-cycle either). M1 OPEN (fused H = 1 deficit). M3 OPEN. Step 03 OPEN.
Step 04 unauthorized. Bank25 = 25. No successor, no refutation claim.

**HARD STOP.**
