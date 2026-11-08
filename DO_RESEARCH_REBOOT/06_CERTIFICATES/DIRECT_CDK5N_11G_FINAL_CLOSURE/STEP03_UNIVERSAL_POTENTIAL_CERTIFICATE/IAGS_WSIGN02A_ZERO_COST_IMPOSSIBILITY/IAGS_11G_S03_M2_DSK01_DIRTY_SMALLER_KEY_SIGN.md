# IAGS-11G-S03-M2-DSK01 — Dirty Smaller-Key Sign and Residual High Cycles

## A. Pre-execution record — 2026-10-28, Asia/Karachi

User authorization: continue M2 on negative smaller-key edges in dirty states
outside chi8, run experiments, seek a signed bound or a certified negative
cycle, preserve R1-R4.

Checkpoint: coarse-double-branch, local HEAD and remote branch tip
fea2a25b05e97f726b6e1891cebb12c4cfca821a. Tracked tree clean. All seventeen
pre-existing untracked files, including R8R01 and SEP01 evidence, are preserved;
baseline SHA256 values were captured before execution.

### Four-rule gate / IAGS Box

Parent T: all closed high B-walks have sum(6-q)>=0. Inherited SEP01 excludes
negative cycles intersecting chi8 and all negative target-8 edges on cycles.
Residual cycle negatives therefore have dirty sources outside chi8 and target
x<8. The full graph remains unchanged.

Child mechanism: first characterize dirty negative witnesses by their SELECTED
sentinel claimant; then audit the periodic source trace and aliased rotations
for a target that claims sentinel on its right, allowing EVERY true-chain
direction pattern. Candidate sufficient bound: no dirty-source high edge has
negative weight. A failure is only a local counterexample unless a full closed
composition is separately validated. The principal goal is residual-cycle sign
or an exact original-relation negative-cycle countercertificate.

1. Strictly smaller: one negative-edge source/target family; no A-shadow
   synthesis or arbitrary closed-walk search before this source classification.
2. Concrete foothold: two-core-path union has at most nine nodes, forcing early
   static conflicts for incompatible claimants; same-target claimant traces
   have bounded periodic path/direction words and exact finite alias tables.
3. One mechanism: selected-claimant filtering -> alias normal forms -> signed
   edge bound -> cycle reconstruction, or exact witnessed cyclic obstruction.
4. Advancement: success deletes the remaining dirty negative-edge obligation
   (or refutes the frozen sign premise with a fully certified negative cycle).

I: frozen compilers, B-only lifting, clean negative -> chi8 (ESD01), positive
absorbing chi8 (SEP01), exact private witnesses and complete interval closure.
U: can a nonextremal claimant's mixed-direction orbit support valid excess
credit and a negative return? beta: a proved dirty-edge nonnegative bound plus
SEP01's exclusion of clean negative edges from cycles proves M2; otherwise
only a fully witnessed negative closed composition refutes it.

### Freeze and experiment bounds

G_star=G_AF; original O/M relation and shared midpoint; exact source q and
w=6-q; s=(mu,b,alpha,sigma); A-shadow depth 2; T=266; all original masks,
signatures, phantom refs, zero edges, arbitrary closed lengths and full-state
closure. Z3 5.1.0 architecture unchanged; initial experiments use no solver.
No source or graph modifications, extra state coordinates, cap increases,
commits or pushes. Step 04 remains unauthorized; Bank25=25.

New artifacts: this report and DO_RESEARCH_REBOOT/M2_DSK01/ only.
Python -B, no bytecode caches. Diagnostic CPU cap 120 seconds; production-DAG
certificate phase cap 300 seconds, within frozen resource ceilings. Any cap
or incomplete case audit is UNKNOWN, never a proof. Negative candidates need
full original build_shigh verification and exact shared ordinary states,
including lo/hi, before any cycle claim.

No M1/M3 work or automatic successor. Existing reports are not rewritten.

## B. Execution

The first diagnostic completed 2,555 same-target right-claimant cases, all
with a forced final-root claim. The initial target=selected-claimant-only
filter is NOT assumed: equality in the static test also permits a distinct
family where the selected claimant is a LEFT phantom at the target's inorder
successor. This family uses active sentinel-child reads of literal slot 0 and
requires separate source-exact cases fixing slot 0 under any replay renaming.
Both are branches of the precommitted selected-claimant mechanism. No theorem
has yet been promoted from these diagnostics.

## C. Final result and theorem scope

**OUTCOME A — M2 PROVED—UNIVERSAL on the complete frozen high subgraph.**

Let N=19. Write P19(b) for the core slots with a kind-0 child reference to N;
dirty means P19(b) is nonempty. Define the existing-coordinate predicate

    chi8(b) := kr[8]=0 and rr[8]=19.

These are proof abbreviations, not added state coordinates or observations.
All claims below quantify over the original valid high witnesses, all 126
masks, all admissible signatures, every original phantom/reference value,
and all ordinary and midpoint states of G_AF. No low-only path restriction
is imported. True depth h is distinguished from declared depth d throughout.

**D1 — Dirty-source signed edge bound.** Every valid high edge from a dirty
source satisfies w=6-q>=0. In particular, a dirty source outside chi8 admits
no negative smaller-key high edge. This does not assert the stronger +2
bound for arbitrary dirty smaller-key edges; zero and +1 are retained.

**D2 — Explicit high potential.** On both original sorts, using their own B
field, set

    Phi(z) = -3 * indicator(chi8(z.b)).

Every weighted OM high leg satisfies Phi(m)-Phi(s)<=w. Every zero-weight MO
high leg satisfies Phi(t)-Phi(m)=0. Hence every finite high path P satisfies

    weight(P) >= Phi(end)-Phi(start) >= -3,

and every finite closed high walk has nonnegative total weight. This proves
M2 with exact signed weights and shared midpoints, at arbitrary walk length.
No negative high cycle exists in this frozen graph.

The source of the -3 offset is real: the clean h=0,d=18 edge has weight -3
while preserving root 8 and creating chi8. The correction is retained, and
two complete original-compiler controls with different fringe profiles
confirm it. A clean negative edge can have a negative one-successor prefix;
there is no claim that a single successor always repays it.

M1, M3 and Step 03 remain OPEN. This is a high-only certificate; its edge
inequality has not been proved for low edges. Step 04 remains UNAUTHORIZED,
Bank25=25, and Dynamic Optimality remains OPEN.

## D. Load-bearing sources and inherited proved premises

The unchanged executable sources are under DO_RESEARCH_REBOOT/06_CERTIFICATES/:

| Source | Relevant definition |
|---|---|
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py | b_valid:39; muxb:66; b_single_rot:73; BTrace:99; b_parent_of:110; b_side_of:121; verify_bpath:130; b_splay_event:164 |
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_TYPED_DAG.py | simplify:182: exact partial evaluation, with unfixed variables retained |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py | b_tree_valid:22: root has zero real-slot claims; every other core has exactly one parent, with exact depth consistency |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py | b_equal:23; build_shigh:31: complete high relation, genuine change, marked target, original replay, d<=18 and w=6-q |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py | StateVars7/state_valid7: existing ordinary-state interface and legal shadow values |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_PRODUCT_COMPILER.py | Original OM/MO projections, OM weight and zero-weight MO leg |
| DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/S03_EDGE_PROJECTIONS.py | Complete private witnesses and shared graph interfaces |

Inherited premises, with reports in this report's directory:

- M2_ESD01_ORIENTED_SENTINEL_DEBT, F-H: a clean-source negative high edge
  targets 8 and creates chi8; smaller-target high edges from chi8 have w>=2
  and preserve chi8.
- M2_R8R01_IMMEDIATE_KEY8_REPEAT: the h=0 correction and exact root-8 replay.
- M2_SEP01_SEPARATED_KEY8_REPAYMENT, E-G: all high edges from chi8 have w>=2
  and preserve chi8, including target 8; all dirty target-8 edges have w>=2.
- M2_HIGH_ONLY_B_PROJECTION: complete high closed-walk lifting. Section H
  below also proves the potential directly on the original two sorts.

These are established premises, not new open hypotheses. Their old files
and evidence are preserved byte for byte. No claim about an unproved low
edge or odd-depth old-root lemma is needed.

High does not require root termination or a repetition-free path. Its actual
target x and fiber label v remain independent marked core labels. Structural
b_equal identifies root and the four child arrays, while fresh endpoint
lo/hi fields are separately validated. Full closed-state equality still
includes intervals, alpha, mask and signature.

## E. Complete dirty-negative source classification

### E1. The forced source orbit and early-conflict bound

For a valid source, every core has a unique chain to the core root. Gap slots
are childless, so every ancestor on a core chain is core. Exact nonnegative
depths exclude parent cycles. Thus a target's true depth h is in 0..8.

Let c=max P19(b). The actual b_parent_of(N) is c by the source's last-match
scan; b_side_of(N,c) is RIGHT exactly when c's right pair is (0,N), including
the case that both pairs are (0,N). Otherwise the selected claim is LEFT.
Gap slots cannot claim. The source root has no claimant, so parent(root)=N
and side(root under N)=LEFT.

For a negative high edge, q>=7 and d is one of 14,15,16,17,18. Its active
source path therefore reaches

    target -> its true ancestors -> root -> N -> c -> ancestors of c.

The path is read against the SOURCE throughout, even after rotations.

Let r=depth(c), and let L be the lowest common core ancestor of x and c,
with depth ell. The union of their two root paths has

    h+r-ell+1 <= 9

distinct core nodes. The detour enters L at path entry

    h+2+(r-ell) <= 10.

Thus a static contradiction encountered by L is active in every negative
witness. Entry h+2, at the selected claimant itself, is also at most 10.
The static conjunct requires LEFT iff target rank is strictly less than
ancestor rank. At equality it requires RIGHT; that boundary is essential.

### E2. Selected RIGHT claim: only c=x survives

If x<c, the detour N->c is RIGHT while static order requires LEFT, a direct
contradiction. Suppose x>c. Target x cannot be a descendant of c: c's right
pair is the sentinel dead end, and its real left descendants are smaller
than c by the interval constraints. If L is a proper ancestor of both,
c enters L from LEFT while the search direction for x is RIGHT. If L=x,
c enters x from LEFT while the equality test requires RIGHT. Both fail by
entry 10. The only surviving possibility is

    RIGHT_SELF: c=x, with x.right=(0,N).

### E3. Selected LEFT claim: the inorder-successor exception

If x>=c, N->c is LEFT while static order requires RIGHT. Suppose x<c. Target
x cannot descend from c, since c's left pair is the sentinel dead end and
its right descendants are larger. A proper common ancestor again gives
opposite actual/search directions and fails by entry 10.

The surviving case is L=x: claimant c lies in x's right subtree. Entering x
from RIGHT passes the equality test. At every intermediate ancestor between
c and x, target x is smaller, so each ascent must be from a LEFT child or
the static test fails before reaching x. Therefore c is the leftmost core
in x's right subtree. Since c.left is the sentinel dead end and all nine
core labels are present, c is the core inorder successor x+1. Thus

    LEFT_SUCCESSOR: c=x+1, c.left=(0,N),
    c ascends only through LEFT links until the final RIGHT link into x.

The initial same-target-only idea would have omitted this family. It was
rejected during diagnosis, before any theorem promotion. The final proof
and certificate include both families.

### E4. Universality of the classification

The argument uses the ACTUAL selected claimant, not a single-phantom
assumption. Lower-index claimants, arbitrary kind/ref data outside the two
paths, gap populations and shadow fields do not change either real parent
chain. Interval constraints give strict order on real core links even when
other reference values are unrestricted. This proves that every possible
dirty negative witness lies in one of the two families, or already fails
an original source static conjunct. No source state is removed from G_AF.

## F. Exact replay identities for both surviving families

Only the negative declared lengths 14..18 are required here. Each surviving
source has a bounded periodic path and direction word. The following finite
identities retain all off-path B fields symbolically.

### F1. RIGHT_SELF: 511 path words, 2,555 cases

Write the distinct true target-to-root chain as A=(a0=x,a1,...,ah=root).
Let bits_h be the h LEFT/RIGHT directions on that chain. The periodic path
and direction words are

    path period: A, N
    direction period: bits_h, LEFT, RIGHT.

For every h=0..8 and every Boolean direction word, certify all five negative
lengths. There are sum(2^h,h=0..8)=511 words and 511*5=2,555 cases.

Representatives use a_j=8-j. Source pins specify only the root, each chain
link and a0.right=(0,N). The original replay primitive does not compare key
ranks: its reads are child-index muxes, and writes test equality of the
trace's child/parent/grandparent indices to real slots.

The only non-equivariant read is muxb's fallback to literal slot 0 when a
rotating child is N. It is NEVER active in RIGHT_SELF. RotB and zig read
a0. RotA reads a0 when adjacent directions differ; otherwise it reads the
next path node. If that next node is N, the adjacent directions are LEFT
(root->N) and RIGHT (N->a0), so they differ and rotA reads a0 instead.

Consequently the active replay commutes with any permutation of core slots
and core-reference VALUES, fixing N and gap slots, after the actual source
orbit has been derived. This transfers the representative identity to every
actual target/chain labeling, even when literal 0 is moved. It is a replay
identity, NOT a BST order symmetry or a symmetry of b_parent_of's max scan.
Unfixed source variables are renamed along with their slots. Arbitrary
side-field references remain arbitrary and cannot drive a write address.

All 2,555 cases force the FINAL replay root to be a0 and force at least one
real slot's kind-0 child reference to a0. The final endpoint therefore has
an incoming claim on its root, contrary to b_tree_valid.

### F2. LEFT_SUCCESSOR and literal slot 0: 749 words, 3,745 cases

Write A=(a0=x,...,ah=root). Write B=(b0=c,b1,...,b_(s-1)), where every ascent
inside B is LEFT and b_(s-1) is x's right child. Here s>=1, h+s<=8, and all
h+s+1 listed core slots are distinct. The periodic words are

    path period: A, N, B
    direction period: bits_h, LEFT repeated (s+1) times, RIGHT.

Now rotA CAN read N: root->N and N->c are both LEFT. That read must alias
the current literal slot 0. A permutation moving 0 would be unsound.

There are exactly two possible placements to cover:

1. ON A: literal 0 is a_j. If j=0, x=0 and all bits are LEFT. If j>0,
   the ascent entering 0 is RIGHT, and every ascent above 0 is LEFT,
   because 0 is the minimum core. Thus j is one plus the last RIGHT bit
   index, or 0 when there is no RIGHT bit. This gives one ON position for
   each direction word.
2. OFF A and B: all B nodes exceed x, so 0 cannot belong to B. An OFF case
   is possible only when h+s<=7, leaving a ninth core slot for 0.

For each n=h+s=1..8, take h=0..n-1, s=n-h, and all 2^h direction words.
The ON count is sum(2^n-1,n=1..8)=502. OFF has n<=7, giving 247 more.
Total: 749 words, times five lengths = 3,745 cases.

Representatives assign positive slots from 1..8 to A/B, except for the
specified ON position of literal 0. OFF leaves slot 0 completely symbolic.
Pins specify only root, chain links, c.left=(0,N), all LEFT B links, and
x.right=b_(s-1). A replay permutation FIXING 0 and N maps these positions
to any actual source labeling and preserves every mux fallback. Unlisted
slots and all unfixed kind/ref pairs remain symbolic. This is again only
a replay identity after source classification, not an order symmetry.

All 3,745 cases force final root x and an incoming real-slot claim on x.
This includes h=0, both parities, every possible location of slot 0, and
arbitrary symbolic contents of slot 0 when it is off the two paths.

### F3. Authoritative production-DAG certificate

certify_dirty.py constructs the unchanged production b_splay_event DAG once.
For each of the 6,300 cases it pins only the source links described above,
target, declared depth, active path entries and active directions. It asks
the ORIGINAL PC_TYPED_DAG.simplify to partially evaluate the property

    out.root == target
    AND OR over all 19 real slots i and both sides:
            (out.kind[i]==0 AND out.ref[i]==target).

Acceptance requires the resulting node to be CONST BOOL TRUE. Unfixed source
fields, lo/hi, inactive trace entries and every other symbolic value remain
unfixed. A residual symbolic node is a failure, not a solver assumption.
Each certificate row records its parameters, property verdict and SHA256
of the deterministic pin assignment. No diagnostic evaluator is trusted
for this authoritative check.

Result: COMPLETE, 6,300 TRUE cases, 2,555 RIGHT_SELF and 3,745 LEFT_SUCCESSOR,
zero failures; original DAG size 14,600 nodes; 147.578 CPU seconds within the
predeclared 300-second certificate cap. No SMT solver was invoked.

Structural b_equal transfers the final root and its incoming claim to g.b.
The mandatory g.b_tree_valid root-claim count must be zero; a forced incoming
claim makes it at least one. Exact Int counting cannot cancel that claim.
Fresh interval annotations cannot repair this structural contradiction.
This rejects FINAL endpoints, allowing all intermediate alias writes and
possible repairs to occur first.

Classification E covers every dirty negative witness; F rejects every
surviving family. Therefore no valid dirty-source negative high edge exists.
This proves D1. The finite replay table is used universally only with the
complete source reduction and replay-transfer arguments above.

## G. Experiments and controls: exact evidence scopes

All new scripts and JSON are in DO_RESEARCH_REBOOT/M2_DSK01/.

| Artifact | Result and scope |
|---|---|
| diagnostic.py / diagnostic.json | 2,555 RIGHT_SELF symbolic diagnostics; all final root claims; 22.844 CPU seconds |
| probe_left_successor.py / left_successor_probe.json | 40 concrete root-target successor probes; no valid negative edge; 0.375 CPU seconds; diagnostic only |
| left_diagnostic.py / left_diagnostic.json | 3,745 LEFT_SUCCESSOR symbolic diagnostics; all final root claims; 34.516 CPU seconds |
| certify_dirty.py / proof_certificate.json | Authoritative original-DAG 6,300-case proof described in F |
| verify_static_partition.py / static_partition.json | Every 4,862 ordered nine-core BST, every one of its ten empty child slots, every nine-core target: 437,580 queries |
| verify_full_high.py / full_high_controls.json | 39 complete original build_shigh controls: 21 accepted edges and 18 rejected negative candidates; zero potential violations; 44.062 CPU seconds |
| audit_certificate.py / manifest.json | Deterministic row/pin provenance, dimensions, evidence consistency, source hashes and baseline preservation |

The finite static diagnostic has 48,620 single-phantom zero-gap source
models. Exactly 43,758 target queries are compatible: 24,310 RIGHT_SELF and
19,448 LEFT_SUCCESSOR. All other 393,822 fail static order by entry 10.
It additionally checks 6,916 geometries with the unchanged verify_bpath
function. CPU time 35.500 seconds. Its universality is limited to that
finite corpus; arbitrary signatures and multiple claimants are handled by
the mathematical argument in E, not by extrapolating this enumeration.

The complete high controls include targets 0,3,6 as well as other core
targets, positive true depths, both depth parities, and all slot-0 placement
types. A dedicated source has multiple lower sentinel claimants, a nonleaf
literal slot 0, and a present gap with population 266. Its actual selected
claimant is the left successor. Every accepted control supplies legal
source/destination/fiber annotations, masks, shadows and auxiliary values;
all variable range bounds are checked. Every rejected candidate also has
an independently valid source and source path; its replayed final root has
an incoming claim, and the entire original high root evaluates FALSE.

The last three controls reuse the two clean h=0,-3 source geometries and a
chi8 depth-8,d=9 boundary case from SEP01, and reevaluate them with the new
complete build_shigh DAG. All accepted edges satisfy D2's potential law.
The accepted full controls demonstrate nonvacuity. Pointwise rejection of
18 candidates is supplementary; the universal rejection is F's symbolic
certificate. No bounded absence search is used as a no-cycle proof.

Diagnostic phases each stayed within their 120-second CPU caps. All writes
and in-memory replay work stayed within the registered mechanism. No
compiler edits, dependency installation, solver switch or cap increase.

## H. Signed potential, original sorts and arbitrary closure

For a complete contracted high transition b->b', consider four possibilities:

| Source/destination region | Delta Phi | Justification |
|---|---:|---|
| chi8 -> chi8 | 0 | SEP01: w>=2 |
| outside -> chi8 | -3 | Every high weight is >=-3 since q<=9 |
| outside -> outside | 0 | Dirty source: D1. Clean source: a negative edge would enter chi8 by ESD01, contradiction |
| chi8 -> outside | impossible | SEP01 forward invariance |

Every row gives Phi(b')-Phi(b)<=w. This is an explicit integer construction
from proved source laws. It does not fit a potential to finite samples or
assume the desired absence of negative cycles.

For an original OM edge s->m of weight w, its existential complete high
witness supplies a valid source s.b and endpoint m.b, so the same inequality
applies directly. For an original MO edge m->t of weight zero, its complete
witness imposes b_equal(m.b,t.b); in particular the two kr[8]/rr[8] pairs
agree, so Phi(t)=Phi(m). The private witnesses on the two legs need not be
identified. The shared midpoint is the actual original state m, and the
potential is defined on it. Independent witnesses therefore introduce no
compatibility gap in telescoping.

Summing over any finite high path cancels each shared vertex potential with
its actual multiplicity. A closed walk has the same full initial/final
state and sort, so its boundary term is zero. The argument covers repeated
vertices, nonprimitive walks, parallel weights/witnesses, abstract-only
states, all masks/signatures and every closed length. It does not require
minimal length, a simple cycle, or root-only equality. It also covers a
closed high walk starting at a midpoint.

Equivalently, no high closed walk can contain a negative edge: D1 makes
every such edge clean-source, ESD01 places its endpoint in chi8, and SEP01
prevents any high continuation from returning to the clean source. Closed
walks outside chi8 consequently have only nonnegative weights; those
intersecting chi8 have weight at least twice their contracted edge count.

After any entering clean negative edge, m subsequent high transitions
contribute at least 2m, giving the inherited sharp-safe bound -3+2m. The
general potential bound -3 permits that initial deficit, including h=0.
Neither proof assumes a high continuation exists where none does.

## I. Adversarial audit, R1-R4 and net proof advancement

| Issue | Resolution |
|---|---|
| Static equality at target | LEFT_SUCCESSOR included; not collapsed into RIGHT_SELF |
| Sentinel fallback to literal slot 0 | No active read in RIGHT_SELF; fixed-0 transfer and complete ON/OFF cases in LEFT_SUCCESSOR |
| All direction patterns | Every bits_h included, with all permitted h/s and both declared-depth parities |
| h=0 correction | Genuine clean root-preserving -3 edge retained and rechecked; dirty h=0 aliases included |
| Multiple claimants | Actual max claimant and RIGHT precedence used before replay reduction |
| Larger raw references and other child kinds | Unfixed source data remain symbolic; no canonical-reference assumption |
| Intermediate invalidity or later repairs | Only the final root claim is used to reject endpoints |
| Boundary depths | Negative alphabet d=14..18 exhaustive under q/depth constraints; no declared=true substitution |
| Off-spine fringe and interval data | Symbolic replay fields; annotations cannot repair a final root claim |
| Global sharing | Same explicit potential on both original sorts; zero MO preserves its value |
| Zero-weight edges | Retained; no claim that all dirty smaller-key edges are strictly positive |
| Evidence vs proof | Static corpus and controls scoped finitely; universal result uses E/F and established premises |
| Circularity | Explicit two-valued potential constructed after source bounds; no cycle-absence premise |

R1: the exact original target, full graph domain and complete closure are
preserved. The new universal theorem deletes M2's residual dirty negative
edge case. No reactive induced-subgraph substitution is used.

R2: original O/M sorts, source q, signed weights, witnesses and midpoint
sharing remain intact. All edge claims are consequences of unchanged
source predicates and final validity. The high-only telescoping law is
proved on the actual two-sort product.

R3: no source edits, solver run/change, state additions, observable additions,
graph modifications or resource-cap increases. Core depths, LCA and named
regions are mathematical proof notation over existing fields. Branch and
local/remote branch tip remain pinned; no commits or pushes.

R4: 6,300 accepted symbolic identities are accompanied by full source
coverage and transfer proofs. No UNKNOWN or search absence is promoted.
Only M2 advances to PROVED—UNIVERSAL. M1/M3 and Step 03 stay OPEN; Step 04
stays UNAUTHORIZED; Bank25 remains 25.

BEFORE: SEP01 excluded cycles meeting chi8 and every negative target-8 edge
on a high cycle. Negative smaller-key edges from dirty states outside chi8
were the exact remaining high-only sign obligation.

RESULT: selected-claimant static filtering gives two complete source orbit
families. Every negative replay in either family has a mandatory final root
claim, certified in the original DAG with all unpinned fields symbolic.
Thus dirty-source high weights are nonnegative. The explicit Phi combines
this with the inherited clean/chi8 laws and telescopes on the original sorts.

AFTER: all high-only closed-walk sign obligations of M2 are discharged.
No new existence premise, reserve synthesis or auxiliary open theorem is
introduced. M1 and M3 remain independent obligations. Step 03, restricted
Coarse-Double and unrestricted Dynamic Optimality are not completed.

NET PROOF ADVANCEMENT: the original M2 obligation is deleted, rather than
restated or replaced by a conditional potential-existence problem. No
automatic successor campaign is authorized by this report.

## J. Reproduction and integrity

Run from the pinned repository root with Python -B. The following commands
generate their versioned evidence once and refuse to overwrite it:

    python -B DO_RESEARCH_REBOOT/M2_DSK01/diagnostic.py
    python -B DO_RESEARCH_REBOOT/M2_DSK01/probe_left_successor.py
    python -B DO_RESEARCH_REBOOT/M2_DSK01/left_diagnostic.py
    python -B DO_RESEARCH_REBOOT/M2_DSK01/certify_dirty.py
    python -B DO_RESEARCH_REBOOT/M2_DSK01/verify_static_partition.py
    python -B DO_RESEARCH_REBOOT/M2_DSK01/verify_full_high.py

Use a separate reproduction copy with fresh result paths; preserve inherited
research. The static partition precedes the full controls, which also read
the preserved SEP01 controls. A nonwriting 128-row timing probe is available
as certify_dirty.py --benchmark 128. The cheap provenance audit is read-only:

    python -B DO_RESEARCH_REBOOT/M2_DSK01/audit_certificate.py

The audit verifies the complete ordered parameter list, deterministic pin
hashes, all per-row TRUE verdicts, dimensions and evidence consistency. It
does not rerun the already completed 6,300 symbolic reductions. The original
certificate command reproduces those reductions.

manifest.json records SHA256 values for this final report, all new analysis
programs and evidence, the load-bearing source dependencies and all seventeen
pre-existing untracked files. It checks their unchanged baseline hashes,
unchanged local HEAD/branch, unchanged remote coarse-double-branch tip and
empty tracked diff. The remote's default HEAD is a different ref and is not
used as the campaign checkpoint. New untracked paths are confined to this
report and M2_DSK01/. Python files are parsed without bytecode generation;
long report paths use Windows extended-length reads. The manifest does not
hash itself. No old report, test, config or source is overwritten.

## K. Terminal verdict

IAGS-11G-S03-M2-DSK01 — TERMINAL VERDICT

DIRTY-SOURCE HIGH SIGN: w>=0, PROVED—UNIVERSAL
NEGATIVE DIRTY SMALLER-KEY HIGH EDGES: IMPOSSIBLE
HIGH POTENTIAL: Phi=-3*indicator(chi8), PROVED ON O AND M
ALL FINITE HIGH PATHS: weight>=Phi(end)-Phi(start)>=-3
NEGATIVE HIGH CYCLE IN FULL FROZEN GRAPH: IMPOSSIBLE
AUTHORITATIVE ORIGINAL-DAG CASES: 6,300 / 6,300 TRUE
COMPLETE HIGH CONTROLS: 39 / 39 AS EXPECTED
OUTCOME: A
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
