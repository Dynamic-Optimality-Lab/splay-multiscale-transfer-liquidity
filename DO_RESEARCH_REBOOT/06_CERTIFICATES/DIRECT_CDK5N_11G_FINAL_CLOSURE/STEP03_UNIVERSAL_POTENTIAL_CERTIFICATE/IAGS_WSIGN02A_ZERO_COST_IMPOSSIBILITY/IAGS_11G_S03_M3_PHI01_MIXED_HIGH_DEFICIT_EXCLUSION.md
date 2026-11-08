# IAGS-11G-S03-M3-PHI01 — M2 Potential Across Low/High Composition

## A. Pre-execution gate — 2026-10-28, Asia/Karachi

User authorization: continue M3 using the M2 potential, run experiments,
seek a signed bound or certified negative mixed cycle, preserve R1-R4.

Checkpoint: coarse-double-branch at fea2a25b05e97f726b6e1891cebb12c4cfca821a;
tracked tree clean. All 32 existing untracked files have entry SHA256
baselines. Existing research is read-only. New writes are confined to this
report and DO_RESEARCH_REBOOT/M3_PHI01/.

Principal theorem to attack: every mixed closed walk has nonnegative HIGH
contribution, with no negative high edge on such a walk. This is a strict
mixed-cycle coverage result, not a claim that the whole mixed sum is
nonnegative. A complete negative mixed cycle, if found, takes precedence.

Mechanism: prove that low macros preserve chi8, using the ordered-rotation
write sites at the maximum real node; combine this with M2's explicit
Phi=-3*indicator(chi8), clean-negative entry and high absorption. When gap 9
is present, endpoint chi8 is impossible; when absent, core 8 is the maximum
present real B node throughout low replay, including internal gap states.
The proposed stronger low identity is Phi(t)=Phi(s), but only proved
implications will be used. No per-low nonnegative cost is assumed.

1. Strictly smaller: audit one existing two-valued potential on LOW edges,
   deleting mixed cycles containing negative HIGH edges if successful.
   Arbitrary low deficit compensation remains explicitly outside the child.
2. Concrete reason: root-terminated, no-repeat low paths use real rotations;
   a primitive at a maximum node writes only its left pair. This is a local
   exact identity, with a finite symbolic production-DAG check and event
   induction, rather than a new potential-existence premise.
3. One prompt: this maximum-node conservation mechanism, one source audit,
   one mixed contribution theorem or exact obstruction. A bounded search
   for mixed cycles is diagnostic; any candidate needs full original low
   and high roots, exact full endpoints and shared midpoints before use.
4. Upward advancement: success eliminates every negative-high mixed-cycle
   case from M3 and supplies an exact high-part signed bound. It does not
   substitute an equally hard new premise or promote M3 from a reweighting.

Inherited: M2 DSK01/SEP01/ESD01; low true-path/ordered-replay semantics from
the frozen compiler and M1 source audit; KD01 alternating interface; low
w>=-2 is an established bound only, not a low-cycle theorem.

Freeze: G_star=G_AF, original O/M sorts and shared midpoint; all masks,
signatures and full endpoint coordinates; w_L=2H-q_L, w_H=6-q_H and source
credit unchanged. Exact mathematical Int; Z3 5.1.0 architecture unchanged;
s=(mu,b,alpha,sigma), A-shadow depth 2, T=266. No new coordinates,
observables, graph/source edits, solver switches, cap increases, commits or
pushes. Initial work uses no SMT solver. Python -B prevents bytecode writes.

Registered bounds: primitive certificate <=120 CPU seconds; finite cycle
diagnostic <=120 CPU seconds, <=500,000 low extensions, <=2,000,000 states
and <=5,000,000 edges; full-compiler control phase <=300 CPU seconds and
original DAG <=4,000,000 nodes. Cap/truncation is UNKNOWN, not absence.
The search corpus is nine-core zero-gap trees, fixed mask {0,2,4,6,8},
one balanced A source per marked root, 1..3 consecutive fused low KEEPs
followed by one canonical high return. This is a finite SUBSET only; it is
not a restriction of the parent graph. Complete original checks will also
include dirty chi8 controls and a fringe/internal-gap macro if constructible.

M2 remains PROVED. M1, M3 and Step 03 remain OPEN until an independently
sufficient proof or exact obstruction is complete. Step 04 UNAUTHORIZED;
Bank25=25. No automatic successor after this box.

## B. Execution

Completed: 3,570 production-DAG primitive identities; 359,720 finite low
extensions and 17,051 closed-return candidates; 22 complete original low/high
controls, including six exactly closed mixed cycles. No negative candidate
was found in the registered finite corpus. Universal conclusions below come
from source coverage and induction, not from that finite absence.

## C. Theorems and exact limits

Let chi8(b) mean b.kr[8]=0 and b.rr[8]=19. The M2 potential on either
original sort is Phi(z)=-3*indicator(chi8(z.b)).

**T1 — Low conservation, PROVED—UNIVERSAL.** Every valid original low edge
s->t satisfies Phi(t)=Phi(s). More precisely, in every sector with sigma[9]=0,
the two fields kr[8],rr[8] are preserved exactly, at every B-event boundary.
When sigma[9]>0, neither valid ordinary endpoint can satisfy chi8.

**T2 — Mixed-path high contribution, PROVED—UNIVERSAL.** For any finite path
in the original graph, containing arbitrary low/high legs,

    sum(weight of OM high legs) >= Phi(end)-Phi(start) >= -3.

MO legs have weight zero. All repeated-coordinate multiplicities and actual
shared states are retained. If a negative high leg occurs, every subsequent
state is in chi8, every subsequent contracted high edge has weight >=2,
and no later high edge is negative. After m later high edges, the high
contribution from that first negative edge is at least -3+2m. Low weights
are not included in that particular contribution bound.

**T3 — Mixed closed-walk exclusion, PROVED—UNIVERSAL.** No mixed closed walk
contains a negative high leg. Its entire high contribution is nonnegative.
Every closed walk either stays in chi8 or stays outside it. In particular,
every mixed cycle containing a negative high edge, formerly an open M3
case, is now excluded in the complete frozen graph.

**T4 — A signed mixed subclass.** For a closed walk in chi8, let N_H count
contracted high edges and let D_L=sum(max(0,-w_L)) be its total low deficit.
Let P_L=sum(max(0,w_L)). Then

    weight(C) >= 2*N_H + P_L - D_L.

Thus D_L<=2*N_H implies nonnegative total weight. Since each negative low
edge has deficit at most 2, the simpler sufficient condition
N_H>=number of negative low edges also excludes a negative mixed cycle in
chi8. Arbitrarily many zero/positive low edges and arbitrary low/high runs
are allowed in this statement. This is a proved mixed subclass, not a
restriction imposed on the parent graph.

**Exact obstruction to extending Phi unchanged.** Complete original low
assignments exhibit H=1,q=4,w=-2 with Phi(t)-Phi(s)=0, both outside and
inside chi8. Therefore Phi alone fails the full-graph edge inequality
Phi(t)-Phi(s)<=w. This refutes that particular global-potential template,
not M3, and is not a negative closed-walk certificate.

M3 remains OPEN. Low deficits can still outweigh the nonnegative high
contribution on an unexcluded cycle. No assertion about their universal
compensation is made. M1 remains OPEN, M2 remains PROVED, Step 03 remains
OPEN, Step 04 remains UNAUTHORIZED and Bank25 remains 25.

## D. Source audit and proof of low conservation

Relevant unchanged files are relative to DO_RESEARCH_REBOOT/06_CERTIFICATES/:

| Source | Load-bearing behavior |
|---|---|
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py | build_slow: exact five-event B replay; inactive/DELETE B identity; original root_terminated; full entry/destination validity and structure-only intermediate validity |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py | root_terminated: true root at declared depth, no repeated active path entries, B constraints gated to active KEEP |
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py | b_valid:39; b_single_rot:73; b_parent_of:110; verify_bpath:130; b_splay_event:164 |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py | Unique real parents, exact nonnegative depths and root claim count; gap presence from signature |
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py | Original exact partial evaluator and total grounded evaluator |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py | M2 edge relation and structural b_equal; no added low-style path constraint on high |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_PRODUCT_COMPILER.py | Original weighted OM leg and zero MO leg, with shared midpoint |

Inherited proved interfaces: M1_LOW_ONLY_MARKED_ROOT_CYCLE_CLOSURE D-G and
M1_ZRC01_ZERO_WEIGHT_RETURN_CLOSURE K for low true paths and internal-gap
scope; M2_DSK01 C/F/H for the high potential and dirty-source w>=0; SEP01
for positive high absorption; ESD01 for clean negative entry into chi8.
The old quarantine statement about absence of high-style sentinel creation
is not treated as a low sign theorem. Here the specific preserved maximum
pair is proved from the low primitive writes, with its exact domain.

### D1. Every active low KEEP uses ordinary real rotations

Entry b_tree_valid and b_valid give a connected ordered tree over all nine
cores and the present gap slots. Unused raw references and kind!=0 pairs
are opaque data, not real edges. Absent gaps start childless.

At a KEEP boundary, an actual target is present: a core is always present,
and the explicit fringe-occurrence conjunct requires a nonzero signature
for a gap target. verify_bpath fixes its parent chain in the current B state.
The root-termination and no-repeat conjuncts force declared depth to equal
the first true-root depth. A path extended past that root could not end at
the same root without repeating it. It therefore contains only distinct,
present real nodes, with no active sentinel child/parent operands.

For such a path, the frozen b_splay_event wiring is ordinary bottom-up
rotation replay: zigzig first rotates the path parent over grandparent and
then the target over its current parent; zigzag rotates the target twice;
the odd leftover rotates the target over the actual root. The current
grandparent is real except at a root rotation, where p_was_root is TRUE and
the sentinel grandparent receives no write. The explicit source assignment
order has no x/p/gp collisions because these real path nodes are distinct.
Each step moves the middle typed pair rigidly and preserves real tree order.

DELETE and inactive B events are blended to identity, even if their unused
B descriptors are arbitrary. Induction over the primitives and the <=5
events preserves real-node membership and order. Present gaps MAY become
internal; the argument retains them as ordered real nodes. Absent gaps
remain childless because no active primitive can address them. Intermediate
lo/hi may be stale, but the ordered tree property is an inductive semantic
fact from the replay, not a fresh interval assumption imposed at that point.

This reasoning is restricted to low's established true paths. It does not
import root termination, no-repeat, or ordinary rotation behavior into high
sentinel/alias witnesses.

### D2. Gap 9 absent: core 8 is the maximum real node

All potentially present real nodes then have crank<=17. Core 8 has rank
17, whereas gap slots 9..17 have even ranks 0..16. The rank-18 gap slot 18
is absent and cannot become an active address. Every intermediate ordered
tree therefore has core 8 as its maximum, even when other gaps are internal.

Audit the only possible write roles of slot 8 in one real rotation:

- If 8 is outside {x,p,gp}, no field in its slot is written.
- If x=8, the real parent is smaller, so side_x=RIGHT. The primitive writes
  x.left, leaving x.right unchanged.
- If p=8, its real rotating child is smaller, so side_x=LEFT. The primitive
  writes p.left, leaving p.right unchanged.
- If gp=8, its real child p is smaller, so side_p=LEFT. Adoption writes
  gp.left, leaving gp.right unchanged; root gating can only suppress it.

Thus kr[8] and rr[8] are exactly unchanged for ALL source values of that pair,
not merely when it is a phantom. The result tolerates all other phantom
claimants, larger raw reference values, ports, empty pairs and kind values
allowed by the frozen relation. No numeric-order permutation is used.
Inducting over primitives/events proves exact pair conservation in a whole
low macro when sigma[9]=0.

### D3. Gap 9 present: chi8 is impossible at a full valid endpoint

The rank-18 gap is a leaf at each ordinary endpoint by b_valid. In the
connected ordered endpoint tree, core 8 must be its ancestor: if their
lowest common ancestor were a different core, both rank-17 and rank-18
nodes would belong to that ancestor's right subtree, contradicting the
definition of a lowest common ancestor. No gap can be an ancestor there,
because all gaps are childless. Consequently a real path to gap 9 must
leave 8 through its right child. chi8 gives a sentinel dead end on exactly
that side, contradiction.

The signature is preserved by every low edge. Therefore with sigma[9]>0,
both endpoint Phi values are zero. Together with D2, this proves T1 over
every sector and every complete original low witness.

### D4. Original-DAG symbolic check of the primitive identity

certify_maximum.py builds the unchanged b_single_rot DAG (638 nodes).
It enumerates every ordered path triple from the 18 potentially present
real labels, allowing gp=N only at a root rotation. The required rank-side
comparisons and ancestor consistency give 3,570 cases. Role counts for 8:
OFF 2,992; rotating child X 153; parent P 153; grandparent GP 272.

For each case, only x,p,gp,side_x,side_p,p_was_root are pinned. Every B
source field is symbolic. The ORIGINAL DAG.simplify returns out.kr[8] and
out.rr[8] as the exact same variable nodes as source.kr[8],source.rr[8].
Acceptance is literal leaf identity, hence reflexive equality; no custom
simplifier or unproved solver premise is used. All cases passed in 3.453
CPU seconds, below the registered 120-second cap.

The table covers actual label indices, including literal slot 0 and every
possible internal gap below core 8. No alias/sentinel-read symmetry is
needed. D1-D3 establish the complete source coverage and event induction;
the finite table alone is not asserted to enumerate complete low macros.

## E. Direct mixed graph connection and signed accounting

For each original OM high leg e:s->m, M2 proves

    r_H(e) := w(e) - (Phi(m)-Phi(s)) >= 0.

Every original MO leg has weight zero and structural B equality, hence
Phi(t)=Phi(m). Every low OO edge has Delta Phi=0 by T1. Summing on the
actual shared states yields T2 without identifying private edge witnesses:

    sum_H w = sum_H r_H + Phi(end)-Phi(start).

This is an exact identity, not a fitted potential or a new existence
condition. In particular, on a closed walk sum_H w=sum_H r_H>=0.

For the stronger individual-negative-edge exclusion, Phi is nonincreasing
on EVERY original edge: it is constant on low and MO; high cannot leave
chi8 by SEP01. The only possible drop is 0->-3 upon entry into chi8. A
closed walk cannot have a strict drop, so Phi is constant on each of its
edges. The M2 inequality then gives w_H>=0 individually. Alternatively,
a negative high edge enters chi8 and neither low nor high can return to
its clean source. Both arguments include the h=0 clean root-preserving
-3 edge; it remains a valid open-path edge and is excluded from mixed
closed walks by absorption, not by incorrectly requiring a root change.

For any cycle, therefore,

    weight(C) = sum_L w_L + sum_H w_H >= sum_L w_L.

This bound is not nonnegative when the low sum is negative. If the cycle
lies in chi8, each contracted high edge has w>=2; splitting the low sum
into positive cost P_L and deficit D_L gives T4. The inherited per-low
bound w_L>=-2 implies D_L<=2*N_L_minus. No M1 cycle theorem is assumed.

These proofs apply to all masks and signatures, arbitrary repeated states,
parallel witnesses, abstract-only states and arbitrary closed lengths, with
full original closure. A walk starting at a midpoint can be read cyclically;
MO contributes zero and preserves Phi. The count N_H is the number of OM
legs, equivalently contracted high transitions, not the total number of
two-sort legs. No low/high hidden histories are concatenated.

## F. Experiments, complete controls and exact obstruction

### F1. Finite mixed search

search_mixed.py enumerated all 4,862 ordered nine-core B trees, retaining
the 3,584 sources whose root belongs to the fixed mask {0,2,4,6,8}. For
each source it used one balanced concrete A tree with the same root,
then tested all registered 1..3 fused marked low accesses with 1<=d_A<=4,
genuine B change and H=ceil(d_A/2)<=2. Canonical B splays were used.
Every legal prefix tested a canonical high return to the original B tree;
the high endpoint shadow can reset to the initial A shadow under the exact
high interface. Every possible negative candidate still required complete
compiler validation before being a countercertificate.

Result COMPLETE for this finite corpus, 0.953 CPU seconds:

- 359,720 attempted low extensions.
- Legal low prefixes: 14,336 of length 1; 54,024 of length 2; 201,496 of
  length 3. Including initial sources, state occurrences are <=273,440,
  within the registered state ceiling.
- 17,051 closed B-return candidates; no negative total candidate.
- Minimum candidate totals by number of low edges: 6, 9 and 4.
- An open low edge with d_A=1,d_B=8,H=1,q=4,w=-2 was found and retained
  for complete validation.

No corpus result is promoted to a universal cycle theorem. Multi-event
H=2 macros, all other shadows, additional high returns and longer mixed
walks remain in the parent graph. This search does not exhaust them.

### F2. Entire original low/high roots and full closure

verify_full_mixed.py built the unchanged build_slow DAG (1,400,081 nodes)
and build_shigh DAG (53,455 nodes), both below the frozen 4,000,000-node
ceiling. It evaluated the ENTIRE original roots under total assignments,
checking every variable's finite-domain bounds. COMPLETE: 22/22 controls
accepted as expected, 16 low and 6 high, in 26.531 CPU seconds.

The six mixed cycle controls are the three minimum-corpus examples with
and without chi8 decoration. Their totals are respectively 6,9,4 in each
region. The weight-4 examples contain three separate zero-weight low edges
followed by a high edge of weight 4. Every low edge has its own full A
structural witness and inventory; intermediate ordinary states match EXACTLY
between low edges. The high source matches the final low destination, and
its destination matches the first low source on mu, sigma, all B fields
including lo/hi, and all seven shadow positions. Its complete unprojected
assignment supplies a shared original fiber for its OM and MO legs.

Special controls include:

- The w=-2 low edge both clean and chi8-dirty, with H=1,q=4 and zero Phi
  change. These are full original edges, not merely compatible templates.
- A two-event macro K(fringe gap 0),K(core 0), with H=2,q=1,w=3 and
  sigma[0]=1. Its intermediate B-root is the INTERNAL gap slot 9, while
  the final ordinary endpoint again has childless gaps. chi8 and the exact
  right pair of 8 survive every event boundary. This case bypasses the
  inherited concrete certifier's all-core-terminal-ancestor filter by
  assigning the complete original relation directly; no compiler predicate
  is bypassed or altered.
- A low edge with the outer rank-18 gap present, sigma[9]=1, confirming
  endpoint Phi=0 on both sides.

full_mixed_controls.json contains every total environment, event path,
ordinary state, B boundary topology/parent/depth data and shared midpoint
needed to reproduce these evaluations. Its boundary helper also records
fresh canonical lo/hi for the reconstructed tree; those helper annotations
are not asserted to be the intermediate replay's stale lo/hi. The original
DAG derives those stale fields itself from the source, and only structural
validity is imposed at intermediate boundaries. Ordinary endpoints use the
recorded full valid annotations. The positive cycles demonstrate nonvacuity
and exact closure; they are not universal sign evidence.

### F3. Precise failure of the unchanged global-potential template

For either validated negative low edge,

    Phi(t)-Phi(s)=0 > -2=w_L.

Thus using the M2 potential alone as a certificate for every edge fails
EXACTLY. It remains a correct certificate for high contributions because
low Phi changes vanish; low reduced weights equal their original weights.
No global fitting/synthesis rescue is attempted. No negative full mixed
cycle was certified, and no conclusion of universal absence follows from
the finite search.

## G. R1-R4, adversarial coverage and theorem ledger

| Concern | Disposition |
|---|---|
| Internal gaps and stale intervals | Real ordered rotations used inductively; an actual internal-gap full macro passes |
| Absent gaps | Start childless, never active addresses, remain absent/childless |
| Outer gap 9 | Split by mandatory sector coordinate; present case makes chi8 impossible at both valid endpoints |
| Phantom refs / multiple claimants | Maximum pair identity holds for arbitrary symbolic source fields; low true paths do not detour through them |
| Slot-0 mux fallback | No active low child is sentinel; all real labels, including slot 0, covered directly |
| DELETE / inactive entries | B identity by original gating; no hidden restrictions on their unused descriptors |
| h=0 negative high correction | Retained; mixed absorption excludes closure without denying edge validity |
| Low-negative adjacency / zero edges | Retained; w=-2 certified, three zero low edges occur in full mixed cycle controls |
| Shared states and private witnesses | Total environments per edge; full endpoint equality and one actual high midpoint |
| Arbitrary walk length | Symbolic edge law and induction/telescoping; no bounded-to-universal inference |
| Whole M3 sign | OPEN; high nonnegativity is not compensation for low deficits |

R1: no graph/domain or target weakening. The high-negative mixed-cycle
class is excluded by proof in the unchanged full graph. T4 labels its
proved subclass and leaves its complement open.

R2: original source q, signed weights, full states, O/M sorts and midpoint
sharing unchanged. Low paths use their OWN root-termination constraints;
none are imposed on high. No shadow or interval closure is discarded.

R3: no solver run/switch, source edits, new coordinates/observables, graph
changes, cap increases, commits or pushes. chi8 and low deficit/counts are
proof notation over existing states/edge weights, not graph additions.
All registered phases completed below their CPU/node/count bounds.

R4: finite absence remains finite; the exact low-edge obstruction rejects
only the unchanged global Phi template. T1-T3 are universally proved from
the source; T4 is universally proved on its explicitly stated subclass.
M3, M1 and Step 03 remain OPEN. No Step 04 or Bank25 promotion.

| Claim | Status |
|---|---|
| Low conservation of M2 Phi | PROVED—UNIVERSAL |
| High contribution on arbitrary mixed paths | PROVED—UNIVERSAL: >=Delta Phi>=-3 |
| Negative high edge on any mixed closed walk | IMPOSSIBLE, universally |
| Total mixed sign in chi8 when D_L<=2*N_H | PROVED—RESTRICTED DOMAIN |
| M2 Phi as an unchanged global edge potential | REFUTED—EXACT by valid w=-2 low edges |
| Registered finite search | FINITE-EXACT; no negative candidate in corpus |
| Negative original mixed cycle | NONE CERTIFIED |
| M1 / M3 / Step 03 | OPEN |
| M2 | PROVED—UNIVERSAL, inherited certificate preserved |
| Step 04 | UNAUTHORIZED |
| Bank25 | 25 |
| Dynamic Optimality | OPEN |

## H. BEFORE / RESULT / AFTER

BEFORE: M2 supplied a high-only potential and positive chi8 absorption.
Low macros might have removed the extremal phantom, allowing a mixed
return around a negative high edge. KD01's alternating representation
alone supplied no signed bridge.

RESULT: exact maximum-pair conservation across low macros closes that
escape. The M2 potential is unchanged on all low edges, including internal
gap macros. Every negative high mixed-cycle case is eliminated. The high
contribution has a universal boundary bound; chi8 mixed cycles additionally
satisfy 2*N_H+P_L-D_L. Full original low assignments show why this does not
make Phi a global certificate: their unchanged low weights can be -2.

AFTER: every possible negative mixed cycle has only nonnegative high legs
and must get its negative total from low deficits. It either stays outside
chi8, or stays inside with D_L>2*N_H+P_L (necessarily D_L>2*N_H). No mixed
cycle crosses into/out of chi8. The full compensation problem for those
remaining compositions is OPEN, not assumed as a new theorem premise.

NET PROOF ADVANCEMENT: delete all negative-high mixed-cycle obligations
and the stated signed chi8 subclass from M3. Universal M3 is not deleted.
No new existence burden is introduced. The specific unchanged global-Phi
extension is stopped on its certified low-edge obstruction; no successor
potential fit or independent campaign is launched.

## I. Artifacts, reproduction and integrity

All new executable/evidence files are in DO_RESEARCH_REBOOT/M3_PHI01/:

- certify_maximum.py / primitive_certificate.json: all 3,570 symbolic
  primitive identities with source fields unfixed.
- search_mixed.py / mixed_search.json: full finite search counts and
  selected positive cycles/negative open edge.
- verify_full_mixed.py / full_mixed_controls.json: 22 full original roots,
  total assignments and six exact full-state mixed closures.
- audit_results.py / manifest.json: row provenance, full-control consistency,
  hashes and preservation of all 32 entry untracked files.

From the pinned repository root, with Python -B:

    python -B DO_RESEARCH_REBOOT/M3_PHI01/certify_maximum.py
    python -B DO_RESEARCH_REBOOT/M3_PHI01/search_mixed.py
    python -B DO_RESEARCH_REBOOT/M3_PHI01/verify_full_mixed.py
    python -B DO_RESEARCH_REBOOT/M3_PHI01/audit_results.py

Generators use exclusive JSON creation and refuse to overwrite prior
evidence. Reproduction needs a separate copy with fresh versioned result
paths; source files and inherited research remain read-only. The audit is
read-only, checks every primitive pin row and all recorded state/weight
closures, and does not claim to rerun original full-root evaluations.
The completed generator run is the authority for those evaluations.

The final manifest records this report, the new scripts/evidence, frozen
dependencies and all baseline SHA256 values. Local HEAD/branch and remote
coarse-double-branch tip are checked, tracked diff is empty, and all new
paths are confined to this report and M3_PHI01/. The manifest excludes its
own hash. Windows extended-length reads handle the long report path.

## J. Terminal verdict

IAGS-11G-S03-M3-PHI01 — TERMINAL VERDICT

Completed 2026-10-29, Asia/Karachi.

LOW CONSERVATION OF M2 POTENTIAL: PROVED—UNIVERSAL
MIXED HIGH CONTRIBUTION BOUND: PROVED—UNIVERSAL
NEGATIVE HIGH LEG ON MIXED CLOSED WALK: IMPOSSIBLE
CHI8 MIXED SIGN WHEN D_L<=2*N_H: PROVED—RESTRICTED DOMAIN
UNCHANGED M2 PHI AS A GLOBAL CERTIFICATE: REFUTED—EXACT
NEGATIVE MIXED CYCLE: NONE CERTIFIED
OUTCOME: NEW SIGNED RESTRICTED PROGRESS; M3 OPEN
M1: OPEN
M2: PROVED—UNIVERSAL
M3: OPEN
STEP 03: OPEN
STEP 04: UNAUTHORIZED
BANK25: 25
DYNAMIC OPTIMALITY: OPEN
NO SOLVER RUN
NO SOURCE OR GRAPH MODIFICATIONS
NO COMMIT OR PUSH
NO AUTOMATIC SUCCESSOR

HARD STOP
