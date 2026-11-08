# IAGS-11G-S03-M2-SEP01 — Separated Key-8 Accesses in Dirty States

## A. Pre-execution record (2026-10-28, Asia/Karachi)

User authorization: continue M2, run experiments on key-8 accesses separated by
smaller-key transitions in dirty states, seek a signed repayment theorem or a
certified negative cycle, and preserve R1-R4.

Checkpoint: local and remote coarse-double-branch at
fea2a25b05e97f726b6e1891cebb12c4cfca821a. Tracked tree unchanged. Eight
pre-existing untracked files (R8R01, six MSINK/DLSS side files, x.json) are
preserved; baseline hashes recorded before execution.

### Four-rule gate and IAGS Box

Parent T: universal M2 nonnegative closed high B-walks, all frozen sectors.
Child T: resolve the sign of closed high B-walks lying in chi8, where
chi8(b) := kr[8]=0 and rr[8]=19, by a source-derived repayment theorem or
a complete original-relation negative-cycle certificate. This is a proof
partition only; the parent graph and other dirty states remain unchanged.

C / mechanism: R8R01 excludes consecutive accesses to 8 when its destination
is in chi8; smaller targets preserve chi8 with w>=2. Cut a chi8 cycle at
target-8 edges into nonempty smaller-target runs followed by one 8-edge.
Test a nonnegative block bound, or find an exactly closed negative composition.
All-smaller cycles are already strictly positive by the inherited barrier.

I: frozen high compiler and complete B-state semantics; M2 B-only lifting;
ESD01 barrier/persistence; R8R01 exact alias proof and corrected h=0 case.
U: do separated 8-edges admit excess credit that defeats intervening payment?
beta: independently nonnegative return blocks imply nonnegative chi8 cycles;
a fully validated negative closed composition refutes the full graph premise.
A negative open block alone proves neither direction.

1. Strictly smaller: focus on one existing extremal dirty region and its
   separated-8 blocks, rather than arbitrary claimant configurations.
2. Concrete foothold: deterministic sentinel orbit, source-level alias maps,
   and actual frozen-primitive replay; no fitted reserve or circular premise.
3. Bounded scope: one block-composition mechanism, targeted diagnostics first,
   followed by bounded exact enumeration only if needed; no successor pivot.
4. Upward advancement: prove a signed law for this dirty cycle class or produce
   a complete negative original-graph cycle. Diagnostics alone do not qualify.

### Freeze and execution discipline

R1-R4 preserved: G_star=G_AF; exact Int; original O/M sorts and shared midpoint;
source q and w=6-q; full B topology AND interval closure; all masks/signatures;
s=(mu,b,alpha,sigma), A-shadow depth 2, T=266; frozen Z3 5.1.0 architecture;
Bank25=25. Initial experiments use exact integer evaluation, not another solver.

No source/compiler edits, graph restrictions, solver switch, state coordinates,
cap increase, commits, pushes, or modifications of prior artifacts.
New artifacts are limited to this report and DO_RESEARCH_REBOOT/M2_SEP01/.
Use Python -B; no bytecode caches. Initial enumeration CPU cap: 120 seconds;
truncation is UNKNOWN, never absence. A search-only no-result is not a proof.
All reported witnesses require a second check against the complete unmodified
build_shigh root, legal auxiliary assignments, a common sector and exact full
state closure. B-only lifting must use compatible shared OM/MO midpoints.

M1/M2/M3 and Step 03 are OPEN at entry. Step 04 is UNAUTHORIZED.

## B. Execution

The initial symbolic audit completed 171 (h,d) cases in 13.953 CPU seconds.
Before the remaining static diagnostic, record its scope: use the same source
sentinel-orbit mechanism to test the complementary dirty key-8 case whose
selected claimant is not the right claimant at 8. The candidate argument uses
the union of two existing core ancestor paths (at most nine nodes) to bound
the first contradictory static check by path index 10. This is a subsidiary
source-coverage lemma for the user-requested dirty key-8 problem; the principal
regional cycle target and frozen graph do not change. The finite diagnostic
uses zero-gap 9-core trees with one phantom; arbitrary signatures and multiple
claimants require the mathematical argument, not empirical promotion.

## C. Verdict and exact theorem statements

**OUTCOME A FOR THE AUTHORIZED REGIONAL BOX; M2 REMAINS OPEN.**

Define P19(b) to be the set of core slots with a kind-0 child reference to 19.
A dirty state has P19(b) nonempty. Define chi8(b) := kr[8]=0 and rr[8]=19,
and R8(b) := chi8(b) and root(b)=8. These are proof predicates over existing
coordinates, not new graph coordinates or compiler observables.

The following results are established for the complete frozen high relation,
all 126 masks, all admissible signatures, all finite lengths, all original
phantoms and auxiliaries, with exact shared states:

**T1 — Dirty extremal target bound.** If chi8(b) and a valid high edge from b
targets 8, then d<=h+1<=9, q<=4, w>=2, and chi8(b'). At h=0 no such genuine
edge exists (R8R01). No canonical-depth equality is imposed: d=h+1 is retained.

**T2 — Positive absorbing region.** Every valid high edge from chi8 has weight
at least +2 and ends in chi8, regardless of target. For smaller targets this
uses ESD01; T1 supplies the formerly missing target-8 case.

**T3 — Separated-return block bound.** If b0 is in R8, a nonempty run of k>=1
smaller-target high transitions is followed by a high access to 8, then

    w(block) >= 2(k+1) >= 4,

and every state remains in chi8. The endpoint is again in R8. This is not
restricted to primitive paths or a bounded k. More generally, every n-edge
high path starting in chi8 has weight at least 2n.

**T4 — Clean-excess repayment and cycle exclusion.** A clean-source negative
edge has w>=-3 and enters chi8. Any continuation by m high edges satisfies

    w(negative edge + continuation) >= -3+2m.

Thus m>=2 repays its worst deficit. This is conditional only on those
continuation edges existing; no existence of an infinite continuation is
assumed. Moreover that negative edge lies on NO high-only closed walk:
an absorbing dirty region cannot return to its clean source.

**T5 — All dirty-source key-8 edges are positive.** For every dirty source,
including states outside chi8, a valid high edge targeting 8 has d<=9,
q<=4 and w>=2. The proof is a first-static-conflict bound using two ancestor
paths, not an assumption that all dirty states are extremal.

**T6 — Residual negative-cycle reduction.** A negative high-only closed walk
exists in the full frozen graph iff one exists with all ordinary vertices
outside chi8. In any such cycle every negative edge has a dirty source
outside chi8 and target strictly below 8. No sign theorem for that residual
class is asserted.

No negative cycle is certified by this campaign. Negative chi8 cycles are
excluded by proof, not by a bounded search returning no result.

## D. Sources, authority and exact semantics

All executable source is unchanged from the pinned HEAD. Relevant paths below
are relative to DO_RESEARCH_REBOOT/06_CERTIFICATES/:

| Source | Load-bearing behavior |
|---|---|
| DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py | b_valid:39; muxb:66; b_single_rot:73; BTrace:99; b_parent_of:110; b_side_of:121; verify_bpath:130; b_splay_event:164 |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py | b_tree_valid:22: root claim count zero, core nonroot count one, exact parent/depth constraints, childless gaps via b_valid |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/STRICT_HIGH_COMPILER.py | b_equal:23; build_shigh:31: original replay, diff, marked target, d<=18, exact q/w and full validity |
| DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py | StateVars7 and state_valid7: existing high ordinary-state interface only |
| DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_PRODUCT_COMPILER.py | Original OM/MO projections, shared fiber and high weight |
| DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/S03_EDGE_PROJECTIONS.py | Private existential witnesses and complete interfaces |

Inherited reports in this report's directory:
- M2_HIGH_ONLY_B_PROJECTION, Sections C-H: exact B-only closed-walk equivalence
  with uniform fixed-shadow lifting.
- M2_ESD01_ORIENTED_SENTINEL_DEBT, Sections F-H: clean-negative target 8 and
  phantom creation; smaller-target barrier and persistence.
- M2_R8R01_IMMEDIATE_KEY8_REPEAT: exact root-8 alias proof, including h=0.
- M2_CYCLE_SIGN_OR_COUNTERCERTIFICATE: deterministic active witness structure.

Ordinary closure includes every B field, including lo/hi, plus alpha, mu and
sigma. Structural b_equal omits lo/hi; fresh endpoint annotations are validated
independently. No equality between high B-target and fiber label is added.
No low root-termination/no-repeat predicate is imported into high.

## E. Universal source reduction to a finite alias table

### E1. Source validity and the right spine to 8

Every marked core target's true ancestor chain is core-only: gap slots have
no kind-0 children. Exact parent counts and nonnegative exact depths give a
unique chain to the core root. Thus h is in 0..8.
Here h denotes true B-depth; the frozen A-shadow depth remains 2.

Let a0=8,a1,...,ah=root be that chain, and N=19. Because 8 is the maximum core
key, every real ancestor step is RIGHT, and 8>a1>...>ah. This follows from
the interval containment and child-interval conjuncts of b_valid.

Under chi8, last-match precedence selects parent(N)=8, even with additional
lower-index claimants; gaps above index 8 cannot claim. Side(N under 8)=RIGHT.
The real root has no claimant, so parent(root)=N and its side is LEFT.

Therefore verify_bpath forces every active prefix of the periodic sequence

    (a0,a1,...,ah,N), repeated,

with directions RIGHT except at positions congruent to h modulo h+2, where
the direction is LEFT. Static checks pass on this orbit: the detour N->8 is
RIGHT with target rank equal to 8's rank; the other core ancestors are smaller.

This is an orbit on the fixed SOURCE state. Parents are never recomputed after
a rotation. Only active path/direction entries are forced.

### E2. Why the representative labels cover every actual chain

The certificate executes representatives a_j=8-j for h=0..8, leaving ALL
unfixed source fields symbolic. This is not an order-automorphism of the BST
domain and is not asserted to be a graph symmetry.

The precise transfer lemma concerns only the already-selected replay:

1. Active rotB and zig always read the real target a0.
2. Active rotA reads a0 if same=FALSE, otherwise p_(t+1).
3. If p_(t+1)=N, then the adjacent directions are LEFT (root->N) and RIGHT
   (N->8); consequently same=FALSE. Thus an active rotA NEVER reads N.
4. Every active child operand is therefore a real member of the distinct
   spine. b_single_rot reads arrays only at that child operand. Its sentinel
   default read of slot 0 is never used by an active primitive in this case.
5. Writes use equality to the real child/parent/grandparent indices, with N
   matching no slot. They do not inspect numeric key order, interval values
   or source fields as dynamic write addresses.

Consequently renaming the distinct spine slots to any actual distinct core
indices, fixing a0=8 and N=19, commutes with each active primitive. Rename
the corresponding symbolic source-field names as well. Arbitrary side fields,
including raw references and gap attachments, remain arbitrary. Exact root
claims and phantom writes transfer unchanged.

Source validity and the real chain were used BEFORE this replay renaming.
No claim that an arbitrary core permutation preserves valid BSTs is made.
Inactive operations are blended off; the production-DAG checks leave their
entries unpinned, verifying that they cannot influence the result.

This transfers the nine representative trace patterns to all possible
actual core-label chains without assuming a nonexistent order symmetry.

### E3. Exact certificate and its rejection table

The finite certificate is proof_certificate.json in DO_RESEARCH_REBOOT/M2_SEP01/.
It covers all 9*19=171 combinations of h and declared d with arbitrary
off-spine fields. The entire production b_splay_event DAG was evaluated
symbolically under the orbit pins, using the unchanged PC_TYPED_DAG.simplify.

For each case all 115 B fields were compared against independently calculated
normal forms from the same frozen functions under an exact value evaluator.
Every residual equality is reflexive or a true constant. A mandatory endpoint
contradiction or phantom preservation property is checked in the production
DAG as part of the same conjunction.

For d>h+1, every final state has root a0 and the following forced incoming
claim on a0. Notation "ajL" means aj.left=(0,a0); "ajR" means aj.right=(0,a0).

| h | Declared-depth ranges and a certified claimant on the final root |
|---:|---|
| 0 | d=2..18: a0L |
| 1 | 3..6: a0L; 7..9: a1R; 10..12: a0L; 13..15: a1R; 16..18: a0L |
| 2 | 4: a0L; 5..18: a1R |
| 3 | 5..6: a0L; 7..11: a2R; 12..15: a1R; 16: a0L; 17..18: a2R |
| 4 | 6: a0L; 7..18: a1R |
| 5 | 7..8: a0L; 9..15: a2R; 16..18: a1R |
| 6 | 8: a0L; 9..18: a1R |
| 7 | 9..10: a0L; 11..18: a2R |
| 8 | 10: a0L; 11..18: a1R |

There are 117 such cases. Structural b_equal transfers the root and its
incoming claim to g.b. Its mandatory b_tree_valid requires the root to have
zero claims. A forced claim contributes at least one to a sum of nonnegative
indicators, contradiction in exact Int semantics. Fresh lo/hi cannot fix it.
This rejects the FINAL endpoint, not merely a transient invalid structure.

For the remaining 54 cases, 0<=d<=h+1, the certificate proves exactly

    out.kr[8]=0 and out.rr[8]=19.

It does not assert all these candidates are valid edges. Some are identities,
some may be incomplete invalid splays. Their only use is the universal
preservation implication for any valid edge among them. R8R01 excludes all
genuine target-8 edges when h=0.

Thus every valid target-8 edge from chi8 has d<=h+1<=9 and preserves chi8.
Since q=floor(d/2), w=6-q>=2. This proves T1.

## F. Signed repayment, invariance and cycle consequences

If the target is smaller than 8, ESD01 C1/C2 already prove w>=2 and chi8
preservation. Combining that with T1 covers every high target, proving T2.

Induct over any high path starting in chi8. Every next source remains in
chi8, every edge has w>=2, and therefore w(path)>=2*length. This proves the
arbitrary-length bound and T3, retaining repeated states, parallel witnesses,
zero-weight candidates (proved absent here), all masks and signatures.

In particular, a smaller-key run cannot re-enable negative declared credit
for the return access to 8. The bound for a k-smaller-step plus one-8-step
block is 2(k+1). Unlike the earlier immediate-repeat exclusion, this covers
arbitrarily many smaller-key steps between accesses.

For a clean negative edge, ESD01 gives weight at least -3 and a destination
in R8. Any m-edge high continuation has weight at least 2m. Thus the total
is at least -3+2m. The two-edge prefix of weight -1 in R8R01 remains valid;
there is no claim that one successor pays the whole deficit.

No high path from chi8 reaches a clean state, since chi8 is forward-invariant
and implies dirtiness. The extremal phantom-to-clean escape problem is now
resolved as UNREACHABLE for high paths; no finite positive escape cost is
postulated. General dirty-state escape outside chi8 is not resolved.

A high-only closed walk that visits chi8 stays entirely in chi8 when read
cyclically and has weight >=2 times its number of contracted high transitions.
It is strictly positive if nonempty. This proves the principal child theorem.

A clean negative edge cannot lie on any high-only closed walk: after entering
chi8 its clean source cannot be recovered. This is independent of true-depth
parity, including h=0 and the Gate-A h=1 example. ESD01's odd-h old-root depth
question remains open as a separate structural statement, but it is no longer
a necessary bridge for excluding cycles through clean negative high edges.

These arguments concern high-only paths. No invariance under LOW edges or
mixed-cycle sign theorem is claimed.

## G. Complementary dirty key-8 source coverage

The regional theorem does not assume that every dirty source lies in chi8.
Here is a separate small source lemma, within the same sentinel-orbit
mechanism, that covers the remaining key-8 sources.

Let c=max P19(b), h=depth_b(8), r=depth_b(c).

If the selected claimant is left-only, the first detour step 19->c has side
LEFT. Target 8 has rank >= rank(c), so the static check requires RIGHT.
That step occurs at path entry h+2<=10. Any d>=10 includes the contradiction.

Suppose the selected claimant is RIGHT and c<8. Key 8 cannot be a descendant
of c: its right child is the sentinel dead end and its left descendants have
rank strictly below c. Let L be the lowest common REAL ancestor of c and 8,
at depth ell. The child below L on c's path is LEFT of L, whereas the search
direction to 8 is RIGHT. Thus the post-sentinel detour fails static order
when it enters L, at path entry

    h+2+(r-ell).

Both root paths contain only core nodes. Their union has

    (h+1)+(r+1)-(ell+1) = h+r-ell+1 <= 9

nodes. Therefore the contradictory entry has index at most 10.
This also covers L=8 (when 8 is an ancestor of c).

Hence for every dirty source outside chi8, a target-8 witness with d>=10
fails an original static conjunct BEFORE rotation. Other claimants do not
change this reasoning: real core parents are unique, and c is the actual
last-match selected sentinel parent. Present gap slots cannot be ancestors
of these core keys, so arbitrary signatures do not change the nine-node bound.

Inside chi8, T1 gives d<=9 as well. Therefore every valid dirty-source
target-8 edge has q<=4 and w>=2, proving T5.

The LCA/depth quantities are mathematical proof auxiliaries over the existing
B-tree, not added graph coordinates, predicates or solver constraints.

Consequences:
- Any negative edge targeting 8 must have a clean source.
- Such an edge enters the positive absorbing chi8 region.
- Along any high path there is at most one negative target-8 edge.
- No high-only closed walk contains a negative target-8 edge.
- In a negative high cycle outside chi8, every negative edge targets x<8.
  Its source is dirty, because ESD01 excludes clean-source negatives targeting
  smaller keys.

This does NOT make smaller-target transitions in arbitrary dirty states
positive: ESD01's smaller-target +2 theorem requires chi8. Residual cycles
can mix other dirty negative targets with positive accesses to 8.

## H. Experiments, controls and evidence scope

All scripts are new analysis artifacts in DO_RESEARCH_REBOOT/M2_SEP01/.
No production source was edited; Python -B prevented bytecode writes.

### H1. Exact diagnostic evaluator

experiment.py calls the unchanged b_parent_of, b_side_of, verify_bpath and
b_splay_event functions with exact value operations. Its boxed values are
truthy as handles even when their VALUE is zero; this preserves BState._clone
semantics for root 0. It is an evaluator, not a new solver or graph.

Its initial probe used the R8R01 +2 successor state, then tested all 19
declared target-8 lengths. Only d=2,3 survived, both with weight +5 and chi8.
A nine-geometry probe then found only d=h,h+1 at positive h. These were
diagnostics; they were not promoted to universality.

### H2. Independent production-DAG symbolic check

certify_patterns.py verifies the diagnostic normal forms against the
unchanged production DAG for all 171 representative cases, with all 115
B fields included and inactive witness entries unpinned.

Result: COMPLETE; 117 forced-root-claim cases, 54 preservation cases;
13.953 CPU seconds. The source-reduction and label-transfer proof in Section E
is essential: the finite table alone is not asserted to enumerate every BST.

### H3. Complete original high-relation controls

verify_full_high.py evaluates the ENTIRE unchanged build_shigh root under
complete legal assignments, checks finite-domain bounds, and records models
in full_high_controls.json.

Result: 37 complete high controls passed; 44.688 CPU seconds.

The controls include:
- h=1..8, d=h and d=h+1;
- zero signatures and a profile with all gaps 0..8 present at alternating
  populations 1 and 266, with gap 9 absent as required by the chosen phantom;
- two clean h=0,d=18,q=9,w=-3 controls, including nonempty fringe;
- the lead into a positive cycle and its two exactly closing edges.

The positive cycle has targets 8,0, both d=2,q=1,w=5, total weight +10.
Full B closure, including fresh lo/hi, is verified. Both ordinary endpoints
use the SAME legal alpha rooted at label 8; mu=391, sigma=0, and fiber label
v=8 on each edge. Thus closure is full-state, not merely equal roots.
The first edge's B-root becomes 8 and the second's becomes 0; target/fiber
independence is respected.

A complete unprojected high assignment supplies its own shared fiber for
both OM/MO projections. The positive cycle therefore has an exact original
graph lift without concatenating hidden A histories. It demonstrates
nonvacuity of separated accesses; it is not evidence of universal sign.

### H4. Finite complementary-orientation diagnostic

verify_orientation.py enumerated all 4,862 ordered 9-core BSTs and each of
their ten empty child slots with one sentinel phantom: 48,620 zero-gap models.

- 4,862 have the extremal right phantom already covered by Section E.
- All other 43,758 models fail the target-8 static test at d=10.
- The first contradictory path entry ranges from 2 through 10.
- 1,124 distinct (h,r,ell,c,side) geometries were additionally checked with
  the ORIGINAL verify_bpath function.
- CPU time: 4.188 seconds; result COMPLETE for that finite diagnostic.

The universal theorem for arbitrary signatures and multiple claimants is
the source path-union argument in Section G. The finite single-phantom corpus
is not silently generalized.

### H5. Search and countercertificate discipline

No large weighted-cycle search was needed after the regional positive-edge
certificate closed the authorized cycle class. No bounded no-result is used
as universal evidence. No negative cycle was found or certified globally.
A global negative-cycle certificate would still require exact full states,
every original high witness, legal auxiliary values, compatible midpoints,
exact closure and strictly negative sum. None is asserted here.

No SMT solver was invoked; the frozen Z3 architecture was neither replaced
nor reconfigured. Registered symbolic/finite diagnostics stayed below their
120-second CPU cap. Controls are separately timed above; all work remains
well inside the frozen resource ceilings. Bank25 stays 25.

## I. Adversarial and R1-R4 audit

| Concern | Disposition |
|---|---|
| h=0 root-preserving negative edge from clean source | Retained; full compiler confirms both fringe profiles |
| Repeated accesses after smaller-key steps | Covered at arbitrary path length by T2/T3 |
| Odd and even true/declaration depths | All h=0..8,d=0..18 represented and symbolically checked |
| Additional sentinel claimants | Actual max claimant used; extremal 8 dominates within chi8 |
| Dirty states outside chi8 | Covered for target 8 by the separate static-conflict lemma; other targets remain open |
| Arbitrary off-spine data and fringe | Symbolic fields; gap leaves cannot be core ancestors |
| Slot-0 sentinel read alias | Active child=N proved impossible for the periodic extremal replay |
| Aliased writes and later repairs | Exact source assignment order and FINAL root claim checked for every case |
| Fresh endpoint intervals | Root-claim rejection is annotation-independent; positive controls assign valid fresh annotations |
| Zero-weight high edges | Not removed from graph; proved impossible with chi8 source or dirty target 8 |
| Full closure | Positive cycle checks lo/hi, alpha, mask and signature, not root-only equality |
| Shared midpoint | Each control uses a common unprojected fiber; M2 lifting remains exact |
| Reactionary domain narrowing | None: full G_star unchanged; chi8 has a proved positive-absorbing coverage theorem |
| New observations/state coordinates | None: named proof predicates/depths do not alter graph interfaces |
| Classical splay assumptions | No ordinary-rotation theorem applied to sentinel/alias traces |
| M1/M3 | No sign or invariance conclusion transferred to them |
| Premature M2 promotion | Refused; smaller-target dirty residual is explicit |

## J. Dependency reconstruction and theorem ledger

New implication chain:

    source validity + selected sentinel parent
          -> periodic extremal trace
          -> alias table + final root-claim contradiction
          -> target-8 credit bound and phantom persistence
          + inherited smaller-target barrier/persistence
          -> every high edge from chi8 has w>=2 and stays in chi8
          -> arbitrary separated-return block bound
          -> no negative high cycle intersects chi8
          -> clean negative high edges are absent from all high closed walks.

Complementary chain:

    dirty source outside chi8 + target 8
          -> left-claim contradiction OR two-path union <=9
          -> static failure by entry 10
          -> d<=9 and w>=2 for every dirty-source target-8 edge
          -> no negative target-8 edge belongs to a high cycle.

Negative-cycle equivalence after proved coverage:

    NegCycle(full high graph)
        iff NegCycle(induced high graph on NOT chi8).

The original graph remains full and unchanged. This is an analytical
equivalence justified by the positive absorbing region, not deletion of
uncovered vertices or a new frozen proof region.

| Claim | Status |
|---|---|
| Regional chi8 high-cycle sign | PROVED, strictly positive for nonempty cycles |
| Separated smaller-run plus 8-return bound | PROVED: >=2(k+1), k>=1 |
| Clean negative plus m-step continuation | PROVED: >=-3+2m |
| Extremal high-only phantom escape | IMPOSSIBLE; no finite escape path |
| All dirty-source key-8 edges | PROVED w>=2 |
| Clean negative edge on any high cycle | IMPOSSIBLE, all true-depth parities |
| ESD01 odd-h old-root depth as a standalone statement | Still OPEN; no longer needed for the new clean-negative cycle exclusion |
| Other dirty states / smaller-target negative-cycle sign | OPEN |
| Universal M2 | OPEN |
| M1 / M3 / Step 03 | OPEN |
| Stage 11F / 11G Steps 01 and 02 | Inherited COMPLETE; not rerun as whole campaigns |
| Step 04 | UNAUTHORIZED |
| Negative full-graph cycle | NONE CERTIFIED |
| Restricted/unrestricted Coarse-Double / Dynamic Optimality | OPEN |
| Bank25 | 25 |

## K. BEFORE / RESULT / AFTER and remaining frontier

BEFORE:
Immediate repeated access to 8 from R8 was excluded. A smaller-key step could
change the true depth of 8, leaving separated repeats, extremal escape and
dirty-only cycle coverage unresolved.

RESULT:
The complete extremal orbit table excludes every excess d>h+1 and proves
phantom preservation for every remaining valid 8-edge. The whole chi8 region
is positive and absorbing. Arbitrarily separated accesses there cannot
accumulate deficits; an entering clean negative is repaid after two further
high steps if they occur, and cannot belong to a high closed walk at all.
A second short source argument excludes zero/negative target-8 edges from
all other dirty sources.

AFTER:
The chi8 cycle class is closed. All target-8 negative-edge cycle obligations
and clean-negative high-cycle obligations are deleted. No new sufficient
condition of comparable difficulty is introduced.

The remaining high negative-cycle problem lies outside chi8; every negative
edge on a residual cycle has a dirty source and target x<8. These states may
have nonextremal selected claimants, changing claimant sets and orientations.
Positive key-8 edges can still connect such smaller-target deficits. No
repayment theorem for those residual compositions is claimed, and no M2
closure is inferred.

Outcome A applies to the principal regional Box. These results constitute
new signed progress toward the parent; they do not prove universal M2.

## L. Reproduction and integrity

Run from the pinned repository root, using Python -B:

    python -B DO_RESEARCH_REBOOT/M2_SEP01/experiment.py probe
    python -B DO_RESEARCH_REBOOT/M2_SEP01/experiment.py patterns
    python -B DO_RESEARCH_REBOOT/M2_SEP01/experiment.py symbolic
    python -B DO_RESEARCH_REBOOT/M2_SEP01/certify_patterns.py
    python -B DO_RESEARCH_REBOOT/M2_SEP01/verify_full_high.py
    python -B DO_RESEARCH_REBOOT/M2_SEP01/verify_orientation.py

Certificate-generating programs use exclusive creation and refuse to overwrite
existing result JSON. Reproduction should use a separate copy of the new
analysis-artifact directory, or deliberately choose a fresh result path;
never overwrite inherited research. The production source remains pinned.

Machine-readable artifacts:
- proof_certificate.json: all 171 symbolic normal forms and forced properties.
- full_high_controls.json: complete positive control states and witnesses.
- orientation_controls.json: finite orientation enumeration and original
  static-predicate check counts.
- manifest.json: source/artifact hashes, baseline preservation and checkpoint.

Final integrity verification checks the unchanged branch/HEAD and tracked
tree, all eight baseline untracked SHA256 hashes, all four new Python programs,
and the three COMPLETE evidence JSON files before exclusively creating the
manifest. The manifest hashes this final report, the new scripts/certificates
and the load-bearing frozen source files; it does not hash itself. Python
integrity reads use Windows extended-length paths for the long report names.

## M. Terminal verdict

IAGS-11G-S03-M2-SEP01 — TERMINAL VERDICT

PRINCIPAL REGIONAL THEOREM: PROVED
SEPARATED-ACCESS SIGNED BOUND: PROVED
DIRTY-SOURCE KEY-8 EDGE WEIGHT: >=+2, PROVED
EXTREMAL HIGH PHANTOM ESCAPE: IMPOSSIBLE
NEGATIVE HIGH CYCLE IN CHI8: IMPOSSIBLE
GLOBAL NEGATIVE CYCLE: NONE CERTIFIED
OUTCOME: A FOR THIS BOX
M1: OPEN
M2: OPEN
M3: OPEN
STEP 03: OPEN
STEP 04: UNAUTHORIZED
BANK25: 25
EXACT EXPERIMENTS AND PRODUCTION-DAG CHECKS EXECUTED
NO SOLVER RUN
NO SOURCE OR GRAPH MODIFICATIONS
NO COMMIT OR PUSH
NO AUTOMATIC SUCCESSOR

HARD STOP

