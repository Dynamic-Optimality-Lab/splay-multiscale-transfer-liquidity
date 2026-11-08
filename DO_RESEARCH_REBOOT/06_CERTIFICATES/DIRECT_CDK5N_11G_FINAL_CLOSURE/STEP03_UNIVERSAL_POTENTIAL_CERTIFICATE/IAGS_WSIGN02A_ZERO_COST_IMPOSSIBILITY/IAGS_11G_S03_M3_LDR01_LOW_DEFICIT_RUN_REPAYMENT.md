# IAGS-11G-S03-M3-LDR01 — Low-Deficit Run Repayment in chi8

## A. Pre-execution gate — 2026-10-29, Asia/Karachi

Authorization: continue M3 on low-deficit compensation, especially chi8
cycles with D_L>2*N_H; execute experiments and seek a signed repayment bound
or a certified negative mixed cycle, preserving R1-R4.

Checkpoint: coarse-double-branch at fea2a25b05e97f726b6e1891cebb12c4cfca821a,
tracked tree clean. Entry SHA256 baselines capture all 41 pre-existing
untracked files. New writes only in this report and
DO_RESEARCH_REBOOT/M3_LDR01/. Existing research and sources are read-only.

Principal theorem to attack: a consecutive run of strictly negative low
edges has total deficit at most 2, and therefore chi8 mixed cycles whose
low edges are all strictly negative have nonnegative total weight. A valid
counterexample run refutes only the run bound, not the mixed-cycle target;
an original negative mixed cycle needs separate complete closure checks.

Mechanism: inherited H=1 fusion replaces each negative low edge by a single
marked core KEEP with d_A<=2, true d_B=6,7,8, and deficit floor(d_B/2)-2.
At full valid endpoints, gaps are leaves. Erasing gap leaves and opaque
child pairs gives an ordered nine-core BST. Core KEEPs project to canonical
core splays; unused side pairs travel rigidly. Enumerate ALL 4,862 core
topologies and every negative access, then check the longest-deficit
recurrence on this complete finite OVERAPPROXIMATION. The A-side and marking
constraints are dropped only in the sound proof overapproximation; they are
mandatory in any original-edge/cycle certificate. This is not a sampled fit.

1. Strictly smaller: strictly-negative consecutive low runs, independent of
   arbitrary zero/positive helper edges and arbitrary low/high alternation.
2. Concrete reason: a deep access uses >=7 of 9 core path nodes; its exact
   canonical splay has bounded remaining depth. A complete small transition
   classification and acyclic longest-deficit recurrence can prove a sharp
   run bound, or immediately supply a concrete structural obstruction.
3. One prompt: deep-access run classification, its signed bound or exact
   obstruction, full original controls, and one direct chi8 cycle connection.
   Test zero/positive helpers only as the same mechanism's boundary audit;
   do not launch a new potential-fit or unrelated low theorem.
4. Advancement fixed in advance: success deletes all chi8 mixed-cycle cases
   with exclusively negative low edges, even when individual counts alone
   did not close the sign. It also constrains every remaining D_L>2*N_H
   candidate to use deficit-resetting nonnegative low steps. If the bound
   fails, only an independently certified original counterexample is used.

Bounded experiments: complete nine-core access census and recurrence <=120
CPU seconds; at most 1,000,000 short helper/cycle extensions and 120 CPU
seconds, <=2,000,000 states and <=5,000,000 diagnostic edges. Full original
low/high controls <=300 CPU seconds, DAG<=4,000,000 nodes. Any cap gives
UNKNOWN, never exhaustive absence. A bounded search may use zero-gap actual
A/B trees and a fixed five-key mask as an explicit finite corpus; the parent
graph retains every original sector, macro, weight and witness.

Freeze: G_star=G_AF; exact original O/M sorts, shared midpoint, source q,
w_L=2H-q_L and w_H=6-q_H; full endpoint closure including intervals and
alpha. Z3 5.1.0 architecture, exact Int, s=(mu,b,alpha,sigma), A-shadow depth
2 and T=266 unchanged. Initial work uses no solver. Python -B; no caches,
source edits, new graph coordinates/observables, cap increases, commits or
pushes. All new functions are proof notation over existing state fields.

Inherited proved premises: M1 negative-edge fusion and w_L>=-2; M2 high
potential and chi8 high cost>=2; M3_PHI01 low chi8 conservation and negative
high exclusion from mixed closed walks. M1/M3/Step03 OPEN; M2 PROVED;
Step04 UNAUTHORIZED; Bank25=25. No automatic successor after this Box.

## B. Execution

The complete census finished: 4,862 topologies, 43,758 accesses, 4,224
negative-access edges. The negative-only graph is acyclic; its maximum
path deficit is 2 and its maximum path length is 2. No theorem promotion
yet: the full source projection and recurrence certificate are audited next.

Before the registered subsidiary checks, fix their exact scope. Verify all
408 ordered core rotation address triples against the original production
DAG, with all 115 B fields and arbitrary symbolic side data (<=120 CPU
seconds). This supports the same complete core-projection mechanism.

The helper stress test uses eight deterministic chi8 seeds (including the
previously certified -2 low-edge source), at most six fused low edges and
one canonical high return. It allows fresh actual nine-core A witnesses
between low edges ONLY when the complete seven-position abstract shadows
agree, exactly as the graph permits. All 4,862 physical A trees are indexed
by their shadows. A bounded minimum-weight search explores these witness
choices; <=1,000,000 extensions, <=120 CPU seconds and the frozen state/edge
ceilings apply. A cap produces a recorded partial UNKNOWN corpus; any found
candidate remains eligible for complete original-root validation. No finite
absence is promoted. This is the run-bound boundary audit already registered,
not an independent potential or a graph restriction.

Before promotion, independently replay all 4,224 census edges through the
unchanged production verify_bpath and b_splay_event (true declared depth,
chi8 decoration, zero gaps), comparing complete child arrays/root and stale
interval transport with the census result. This <=120-CPU-second source
composition audit complements the arbitrary-side-field primitive proof;
it does not add a new mechanism or enlarge any frozen resource ceiling.

The completed recurrence has range psi=0..2. Its immediate same-mechanism
corollary is Xi=-psi: it handles every negative low edge, and its range
automatically handles every chi8 high edge and every low edge of weight
>=2. Only low weights 0 and +1 can violate it. As the registered helper
boundary audit, select one zero-weight low access from psi=2 to psi=0
(if present) and validate it with a full original low root, in a fresh
versioned evidence file. This checks sharpness of the cheap-helper budget;
it is not a new potential fit or a new global compensation premise.

## C. Result and precise theorem scopes

**OUTCOME A FOR THE REGISTERED RUN THEOREM; M3 REMAINS OPEN.**

**T1 — Sharp negative-run bound, PROVED—UNIVERSAL.** Any consecutive run
of strictly negative original low edges has at most two edges and total
deficit at most 2. Equivalently its total weight is >=-2. The statement
covers all masks, signatures, original phantoms, auxiliary witnesses and
full shared states. A single -2 edge and a two-edge (-1,-1) run attain it.

**T2 — chi8 repayment without cheap low helpers.** Every chi8 mixed closed
walk having no low edge of weight 0 or +1 has nonnegative total weight.
Negative lows and positive lows of weight >=2 are both allowed, in arbitrary
runs and at arbitrary walk length. This includes the precommitted subclass
whose low edges are exclusively negative. It also covers cycles with
D_L>2*N_H when their >=2 low helpers provide the necessary repayment.
This is PROVED—RESTRICTED DOMAIN inside the unchanged full graph.

**T3 — Signed cheap-helper budget.** Let Z count zero-weight low edges and
O count weight-+1 low edges in a chi8 closed walk. Then

    weight(C) >= sum_high(w_H-2)
                 + sum_low_with_w>=2(w_L-2) - 2*Z - O.

Every term in the first two sums is nonnegative. Thus those surpluses repay
the remaining cheap-helper budget whenever their sum is >=2*Z+O. A negative
chi8 mixed cycle must contain a 0/+1 low edge and must fail this surplus
test, as well as PHI01's necessary condition D_L>2*N_H+P_L.

T1-T3 use an explicit integer table psi on all 4,862 ordered core topologies,
with range 0..2. On chi8 the corrected M2 potential is

    Theta(z) = Phi(z) - psi(core(z.b)) = -3 - psi(core(z.b)).

It satisfies the original edge inequality on every high leg, every negative
low edge and every low edge with w>=2. On a zero low edge its reduced weight
is >=-2; on a +1 low edge it is >=-1. MO zero legs preserve its value.
No graph coordinate or compiler observable is added.

**Sharp boundary obstruction, REFUTED—EXACT.** A full original zero-cost low
edge has psi(source)=2, psi(destination)=0. It raises Theta by 2 at cost 0.
A separate +1 low edge raises Theta by 2 at cost 1. The coefficients 2 and
1 in the per-edge cheap-helper allowance are attained. Consequently Theta
does not extend unchanged to all low edges, and this campaign does not
complete M3.

No negative mixed cycle was certified. The helper search found an exactly
validated OPEN run with weights (-2,+1,0,-1), D_L=3, P_L=1, total -2. It
does not close and does not refute the total-weight bound for any cycle.
It shows why a deficit-only cap of 2 cannot include arbitrary low helpers.
It does NOT refute a hypothetical net-weight bound for arbitrary low runs.

M1/M3/Step03 stay OPEN; M2 stays PROVED; Step04 UNAUTHORIZED; Bank25=25.
Dynamic Optimality remains OPEN.

## D. Complete source reduction for a negative low run

### D1. Mandatory negative-edge normal form

The inherited M1/WS02D universal low-credit bound gives H>=1, q_L<=4, and
w_L=2H-q_L. A negative low edge therefore has H=1, q=3 or 4, deficit
delta=q-2 in {1,2}. WS02C's unit-charge fusion, Sections C-D, replaces it
by a single genuine marked core KEEP from the SAME full entry state to
the SAME full exit state, preserving H,q,w, endpoint shadows and B fields.
Fusion is applied independently to each edge; private A histories are not
concatenated or identified.

Low root termination, no-repeat and unique parent/depth constraints force
the fused B path to be the true core-target ancestor chain. At a full valid
ordinary endpoint, every gap slot is childless, so all ancestors of this
core target are core. Thus its true depth h is in {6,7,8} and

    delta = floor(h/2)-2.

This is a low-source theorem. No high-style sentinel detour is allowed or
assumed; its exclusion follows from low's own predicates.

### D2. Erasing fringe retains the exact ordered core transition

Erase gap leaves and every child pair that does not name a real core node.
Every source core has its original unique core parent, and the nine cores
form one ordered rooted BST. All 9 labels occur, in fixed order 0..8.
Its core depth of the target is exactly h.

During the fused access, each rotating child/parent and each real
grandparent is core. A primitive copies its middle (kind,ref) pair intact,
then inserts known kind-0 references to the rotating real core nodes.
If the middle pair names a core, projection retains that core edge; if it
names a gap or opaque datum, projection erases it. No other source value
is used as a rotation address. Therefore erasure COMMUTES with each
primitive and hence with the canonical bottom-up core splay.

Gap leaves remain leaves because no gap is an active address. Arbitrary
gap populations, hidden A structure, raw refs 19..31, empty/port data and
multiple phantom claims only affect the transported side pairs. They do
not affect this core transition. There is no permutation of ordered core
labels and no claim that a numerical relabeling preserves the graph.

Every original negative low edge therefore projects to one of the complete
core transitions enumerated below, with EXACTLY the same deficit. Dropping
A-shallow and marked-target constraints enlarges the transition set, which
is sound for proving a bound. An overapproximation counterexample would
not by itself be an original graph counterexample.

Fresh endpoint intervals do not enter psi. They remain validated by the
original edge, and full state equality still transports the core topology
at shared boundaries. Fusion preserves those full states, so successive
projected transitions compose even if their private A witnesses differ.

### D3. Original production primitive identity

certify_core_rotation.py enumerates all 408 ordered address triples
(x,p,gp), including root rotations, from the actual core labels. For each
case it compares the ORIGINAL b_single_rot DAG with the explicit unaliased
rigid-pair rotation formula. Every one of the 115 B fields is included.
Every source field remains symbolic; only address/side/root flags are pinned.

The ORIGINAL DAG.simplify reduces the comparison to true constants or
reflexive equalities. The checker accepts only these conjunction leaves.
Result: 408/408 passed, DAG 638 nodes, 0.422 CPU seconds. This proves the
local formula for arbitrary side data. A structural induction over the
source b_splay_event pair/zig wiring gives D2's complete splay connection.

As an independent composition check, verify_census_replay.py runs all 4,224
negative census transitions through the unchanged verify_bpath and
b_splay_event, with true depth and chi8 decoration. Every complete child
array and root matches the census destination; replay lo/hi exactly retain
the source annotations. Result 4,224/4,224 passed, 51.281 CPU seconds.
This exact-value adapter uses truthy symbolic handles even for numeric 0,
preserving the original _clone semantics. It is not a solver.

## E. Complete finite certificate and the bounded recurrence

negative_run_census.py uses the ordered-root recurrence

    Trees([l,h)) = union over roots r of
                   (r, Trees([l,r)), Trees([r+1,h))).

This lists every ordered BST on labels 0..8 exactly once: 4,862 vertices.
All nine target accesses are checked at every vertex: 43,758 queries.
Retain exactly the depths 6,7,8. The negative graph has 4,224 edges:
2,816 at depth 6, 1,152 at depth 7 and 256 at depth 8. Each stores source,
destination, target, depth and the exact positive deficit delta.

The graph is acyclic. Define psi(v) by the completely determined longest
incoming-deficit recurrence, with a virtual zero-cost source to every node:

    psi(v) = max(0, max_(u->v)(psi(u)+delta(u,v))).

This is a construction on the COMPLETE negative-edge overapproximation,
not a potential fitted to a sampled graph or the original open mixed
problem. The resulting integer table has:

| psi | Number of core topologies |
|---:|---:|
| 0 | 4,223 |
| 1 | 556 |
| 2 | 83 |

For every one of the 4,224 rows the exact certificate checks

    psi(destination)-psi(source) >= delta,
    0 <= psi(source),psi(destination) <= 2.

The topological order, all vertices/trees, the table and all edge rows are
recorded. No unknown feasibility premise or new reserve construction is
left open. A verifier needs only complete row generation, exact integer
inequalities and the proven source projection; it need not trust an
unobserved solver or infer absence from bounded path sampling.

For any consecutive negative low run, telescope the inequality with actual
shared endpoints, retaining multiplicity:

    total_deficit <= psi(last)-psi(first) <= 2.

Each edge's deficit is at least 1, so there are at most two edges. This
also handles repetitions: a return to a repeated core coordinate would
contradict the strict increase. The maximum deficit and maximum length are
both 2; the census completed in 0.062 CPU seconds. D1-D3 transfer this
finite complete certificate to the whole original negative-low domain,
proving T1 without restricting any parent graph state or witness.

## F. Repayment on original mixed closed walks

Define Xi=-psi(core B) on the original O and M sorts and Theta=Phi+Xi.
Inside chi8, Phi is constant by PHI01 and SEP01, so only Xi changes.

| Original edge in chi8 | Certified reduced-weight lower bound w-Delta Theta |
|---|---:|
| Negative low | >=0, by the complete negative-edge certificate |
| Low w>=2 | >=w-2, since the potential can rise by at most 2 |
| Low w=0 | >=-2 |
| Low w=1 | >=-1 |
| OM high | >=w_H-2>=0, using the M2/SEP01 high bound |
| MO high leg, weight zero | =0, since structural B equality preserves the core tree and chi8 |

The shared midpoint is the actual original M state. An OM witness and an
MO witness can remain private and different; each inequality applies to
its own interface and uses the same state function Theta. Summing on a
closed walk cancels the potential exactly and proves T3. The high sum
counts OM legs, equivalently contracted high transitions. All full states,
intervals, signatures, masks, repeated vertices and parallel witnesses
remain in scope. This theorem is confined to chi8 because the high >=2
bound is mandatory there; no outside-chi8 high floor is invented.

An equivalent run-count bound is useful. Let R count maximal consecutive
negative low blocks on the cyclically read mixed walk, and K count its
nonnegative low edges. Then T1 gives D_L<=2R and

    weight(C) >= 2*N_H+P_L-2R,     R<=N_H+K.

Every separator costing >=2 can pay one block's worst deficit. If there
are no cheap 0/+1 low separators, P_L>=2K and the bound is nonnegative.
If low edges are all negative, K=0 and R<=N_H, proving the exact
precommitted mixed subclass. The rule applies to whole low macros: H=2,
DELETEs and nongenuine intermediate KEEPs in nonnegative macros are NOT
fused or removed; only their actual weights and the range bound are used.

Every possible negative chi8 mixed cycle must consequently use a cheap
0/+1 low helper. In the user's D_L>2*N_H region, R>N_H is necessary; for
an actually negative total the stronger inherited condition
D_L>2*N_H+P_L is also necessary. The full compensation question for cheap
resets, and the outside-chi8 mixed problem, remain OPEN.

## G. Helper experiments and complete original controls

### G1. Bounded helper search, exact finite scope

search_helpers.py indexes all 4,862 actual nine-core A trees by their
complete seven-position shadows: 634 shadow classes and 5,946 transition
options for mask {0,2,4,6,8}. Within an edge it uses an actual A tree and
a fused core KEEP of A-depth 1..4. Between edges it may select another A
witness ONLY from the same complete endpoint shadow class. Private hidden
A structure is not a state coordinate and is not falsely equated across
edges. B states and all ordinary shadow fields remain shared exactly.

Eight deterministic chi8 sources start with a forced negative low access.
The dynamic program explores up to six low edges, retaining minimum weight
per exact (B,alpha7) state at each length, with a deficit tie-break. It tests
a canonical high return to the original B tree. It is a minimum-weight
finite corpus, not an exhaustive enumeration of every possible D_L history.

Result COMPLETE for that registered corpus: 94,995 extensions, 32,987
retained state occurrences/return tests, all eight seeds completed, 0.625
CPU seconds. None of these retained endpoints had the required single
canonical high return. Thus there were zero closed candidates, not a
nonempty family of validated nonnegative cycles. No negative mixed cycle
and no universal absence conclusion follows from this search.

It found a four-low-edge open run with weights (-2,+1,0,-1), D_L=3,
P_L=1 and net weight -2. Complete original verification follows below.

### G2. Complete low relation, sharpness and reset controls

verify_full_runs.py reuses the preserved PHI01 environment factory, builds
the ENTIRE unchanged build_slow root (1,400,081 nodes), and checks total
assignments and all finite-domain bounds. Eight new original controls pass:

- One chi8 single edge with H=1,q=4,w=-2 and psi increasing 0->2.
- The same sharp edge with a present gap-0 leaf, sigma[0]=1.
- Two shared low edges (-1,-1), with core depths (6,6), A depths (1,2),
  and psi increasing from 0 to 2 across the run.
- Four shared low edges (-2,+1,0,-1) from the helper search, including its
  private A-witness changes with equal full endpoint shadows.

The complete ordinary state of each edge's destination equals the next
source: mu, sigma, all B child/root/lo/hi fields and all seven alpha positions.
Every control retains chi8. Their full environments and source/destination
models are recorded. CPU time 22.562 seconds. All these runs are OPEN;
none is a closed negative mixed-walk certificate.

verify_zero_reset.py selects a canonical depth-4/5 target from a psi=2
topology to a psi=0 topology, makes it A-shallow, and evaluates the complete
original low root. This ninth new low control passes with H=1,q=2,w=0,
Delta Theta=2, reduced weight -2. CPU time 6.031 seconds. The helper run's
+1 edge likewise has psi 2->0, Delta Theta=2 and reduced weight -1.
Thus the cheap-helper allowance is source-real and sharp at the edge level.

The two verified reset edges refute extending Theta unchanged to those
cheap weights. They do not refute T1, T2, T3 or global M3. The open
D_L=3 example still has net weight -2; appending a hypothetical high of
cost >=2 would repay that number, but no such closed composition was
constructed and none is assumed.

No SMT solver was invoked. All phases finished below the registered
CPU/node/state/edge/query caps. Original sources and previous evidence
were not modified or overwritten.

## H. R1-R4 and adversarial audit

| Concern | Disposition |
|---|---|
| All 126 masks | Marking relaxed only in the complete proof overapproximation; never in original controls |
| All fringe/signatures | Negative fusion and core-only real path; rigid opaque side pairs; sigma[0]=1 sharp control |
| Internal-gap nonnegative macros | Retained whole; positive >=2 edge law uses only potential range and actual weight |
| Arbitrary phantom claims | No sentinel child on true low path; copied side data remain symbolic |
| Literal slot 0 | Actual core labels enumerated; no sentinel fallback read or unsound permutation |
| Fresh intervals/full closure | Projection function ignores annotations; original endpoints still require complete validity and equality |
| Private witness sharing | Fusion preserves full endpoints; helper controls compare all ordinary coordinates |
| Repeated/parallel/nonprimitive walks | Edge inequalities telescope with multiplicity; no simple-cycle assumption |
| Finite fit vs universal proof | Entire 4,862-topology domain, all 4,224 negative rows, complete source reduction and exact integer table |
| Extra global existence burden | None; longest-deficit recurrence is completed and checked |
| Helper search scope | Finite minimum-weight corpus only, zero closing candidates explicitly recorded |
| Overclaim from open negative run | Refused; original runs are open, not negative-cycle certificates |
| Theta on cheap low edges | Exact reset counterexamples; template stopped, no new fit launched |

R1: original M3/Step03 target remains the full G_AF. All negative low runs
are bounded universally. T2 explicitly names the mixed subclass deleted;
the complementary cheap-helper and outside-chi8 cases stay in the graph.

R2: exact two sorts, shared midpoint, source q, signed weights, complete
low/high witnesses and full closure preserved. High-only costs are used
only with their chi8 hypotheses. No low/high history concatenation.

R3: no source/compiler edits, graph changes, new state coordinates or
observables, solver switch/run, cap increase, commits or pushes. psi is a
proof function of an existing B topology; its table imposes no new constraint.

R4: universal T1 uses a complete finite source projection, not sampled
absence. T2 is restricted and T3 has explicit hypotheses. Cheap-reset
counterexamples reject only Theta's unchanged extension. M1/M3/Step03
stay OPEN; M2's proof is preserved; Step04 UNAUTHORIZED; Bank25=25.

## I. BEFORE / RESULT / AFTER

BEFORE: chi8 mixed cycles satisfied the coarse bound
weight>=2*N_H+P_L-D_L. The region D_L>2*N_H could contain multiple low
deficits with no established consecutive-run repayment restriction.

RESULT: the complete deep-access classification proves every negative low
run has deficit <=2 and length <=2. Its explicitly constructed psi corrects
the M2 potential inside chi8 for all edges except low weights 0,+1. High
edges and low helpers costing >=2 repay negative runs. A precise budget
isolates cheap resets; full original controls certify both their existence
and their maximal two-unit potential drop.

AFTER: delete every chi8 mixed-cycle case without a 0/+1 low edge, including
the precommitted negative-only-low class. Every unexcluded negative chi8
cycle requires cheap helper resets and must exceed both the low-deficit
and surplus tests stated above. General compensation across those resets
remains OPEN; outside-chi8 mixed cycles remain OPEN. No equally hard new
existence premise is introduced and no M3 completion is inferred.

NET PROOF ADVANCEMENT: a sharp universal low-run law and a new signed mixed
subclass are proved, replacing the previous absence of any low-run deficit
bound. The source-real cheap-reset obstruction is recorded without
claiming it is a negative cycle. Stop this mechanism at that frontier;
no automatic successor potential or independent theorem campaign.

## J. Reproduction, integrity and terminal verdict

All new programs/evidence are in DO_RESEARCH_REBOOT/M3_LDR01/:

- negative_run_census.py / negative_run_census.json: all topologies, edges,
  topological order, recurrence table and maximal-deficit witness.
- certify_core_rotation.py / core_rotation_certificate.json: 408 symbolic
  production-DAG comparisons across all 115 B fields.
- verify_census_replay.py / census_replay.json: 4,224 original replay checks.
- search_helpers.py / helper_search.json: bounded shared-shadow helper search.
- verify_full_runs.py / full_run_controls.json: eight complete original lows.
- verify_zero_reset.py / zero_reset_control.json: sharp zero-cost reset.
- audit_results.py / manifest.json: complete integer-row checks, control
  sharing/ranges, source hashes and all 41 baseline hashes.

Run with Python -B from the pinned repository root. Census precedes the
checks/search; helper search precedes full-run controls. Generators create
JSON exclusively and refuse to overwrite inherited evidence. Reproduction
requires a separate copy and fresh versioned outputs. The read-only command

    python -B DO_RESEARCH_REBOOT/M3_LDR01/audit_results.py

checks certificate dimensions, every row/sign/range and all recorded state
sharing. It does not claim to repeat the full original-root evaluations;
those are established by the completed generator runs above. The manifest
hashes this final report, new artifacts, frozen dependencies and all entry
untracked files, excluding its own hash. Local branch/HEAD and remote
coarse-double-branch tip remain pinned, tracked diff empty, and all new
paths are confined to the authorized report/directory. Long report paths
use Windows extended-length reads. All prior research is preserved.

IAGS-11G-S03-M3-LDR01 — TERMINAL VERDICT

STRICTLY NEGATIVE LOW RUN: DEFICIT<=2, LENGTH<=2, PROVED—UNIVERSAL
SHARPNESS: ORIGINAL -2 AND (-1,-1) RUNS CERTIFIED
CHI8 MIXED CYCLES WITHOUT LOW 0/+1: NONNEGATIVE, PROVED—RESTRICTED DOMAIN
CHEAP-HELPER SIGNED BUDGET: PROVED ON ALL CHI8 MIXED CLOSED WALKS
UNCHANGED THETA EXTENSION TO ALL LOWS: REFUTED—EXACT
NEGATIVE MIXED CYCLE: NONE CERTIFIED
M1: OPEN
M2: PROVED—UNIVERSAL
M3: OPEN
STEP03: OPEN
STEP04: UNAUTHORIZED
BANK25: 25
DYNAMIC OPTIMALITY: OPEN
NO SOLVER RUN
NO SOURCE OR GRAPH MODIFICATIONS
NO COMMIT OR PUSH
NO AUTOMATIC SUCCESSOR

HARD STOP
