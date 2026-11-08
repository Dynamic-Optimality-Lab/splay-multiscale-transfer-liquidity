"""Publication and byte/Git/CPU-ledger metadata only; no new source test."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent;OLD=P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8',newline='\n') as f:f.write(s.strip()+'\n')
def out(n,v):write(n,json.dumps(v,indent=2))
def table(head,rows):return '| '+' | '.join(head)+' |\n|'+ '|'.join('---' for _ in head)+'|\n'+''.join('| '+' | '.join(str(x).replace('|','/') for x in r)+' |\n' for r in rows)
def git(*x):return subprocess.check_output(['git',*x],cwd=ROOT,text=True).strip()
e=read(B/'entry.json');c=read(OLD/'aligned_source_and_owners.json');inv=read(B/'w199_inventory.json');fam=read(B/'uniform_insertion_templates.json');cc=read(B/'catchment_forcing_countercertificate.json')
audits=[read(B/n) for n in ('independent_audit.json','family_independent_audit.json','reduction_independent_audit.json','window_noncollision_audit.json')]
assert all(x['status'].startswith('PASS') for x in audits)
pins=read(B/'dependency_pins.json')
for z in pins['pins']:assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in pins['external_pins']:assert sha(Path(z['path']))==z['sha256']
assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head'] and not git('status','--porcelain','--untracked-files=no')
total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);newqueries=0;phases=[]
for p in sorted(B.glob('run_*_result.json')):
    r=read(p);controller=read(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+controller['whole_process_CPU_seconds'];total+=charge;groups[r['group']]+=charge;newqueries+=r['source_queries'];phases.append({**r,'controller_CPU':controller['whole_process_CPU_seconds'],'total_charge':charge})
qsum=e['inherited_source_queries']+newqueries;qsafe=qsum+e['inherited_C15_C27_engine_calls']
assert qsafe<2000000 and total<7200 and all(groups[g]<e['group_caps'][g] for g in groups)
status='''Scope/status: original source semantics, exact physical IDs and all old
successes are frozen. W28 is FUNDED with P*=empty. The full U28 universal
claim remains OPEN. New restricted theorems and their audit boundaries
are stated separately; there is no Universal CD or Gate U promotion.
'''
write('C28_FROZEN_TARGETS.md',f'''# C28 frozen targets and final scope

{status}
Original complete directive: USER_DIRECTIVE.txt, hash{sha(B/'USER_DIRECTIVE.txt')}.
W28: fixed Campaign27 199-operation history and ALL its successful actual
owners. No57-entry rollback. U28: EVERY original guarded-e4 history under
the inherited full policy/Bank25 domain, not the new insertion family.
Preserve R1–R4, Bank25, source costs, fE and every actual old a value.
No target changes after a failed proof route.

The closed-source candidate of a pure frame catchment partition was
REFUTED and retained, then replaced by a sufficient hybrid comparison
route. That alteration changes a PROOF CONDITION, not W28, U28 or CD.
No full SOURCE_UNIFORM_FUNDING_THEOREM.md or negative architecture
countercertificate is created because neither full conclusion is proved.
''')
write('SOURCE_INTEGRITY.md',f'''# Source provenance

Repository `{ROOT.as_posix()}`. Branch `{e['branch']}`;
HEAD `{e['head']}`; tracked tree clean. All new work is in this C28 folder.
No commit, push, destructive Git/file action or old research mutation.
All {len(pins['pins'])} inherited local content pins and external directive
pins match. Exact paths/hashes in dependency_pins.json. These byte checks
establish provenance, not mathematical verification.

The first C28 research artifact was W199_FROZEN_SOURCE_AND_POLICY.md.
Authoritative fixed source SHA256 {sha(OLD/'aligned_source_and_owners.json')}.
Accepted separate-implementation C27 verification is reused, not repeated.
New48- and459-operation histories are distinct source objects; their source
words and successful maps never replace W199 or its current58 owners.
The saved C27 product graph was read to recover an ACTUAL closed source
word. No abstract edge or cached search absence was promoted to realizability
or universal exclusion: the new original source was then independently
replayed and its complete policy verified.

Original accepted CD6, five-key selector, raw states and event definitions
are unchanged. Prior audit-pending universal results retain that status.
R1 source/target/closure, R2 actual weighted events/identities, R3 owners/
controllers/caps, R4 proof-status discipline remain. C27's240/600 cap
authorization persists cumulatively; there is no new increase or reset.
''')
write('C27_INHERITANCE_LEDGER.md',f'''# Dependencies inspected/reused

Paths below are relative to DO_RESEARCH_REBOOT. All hashes and historical
read/status annotations are retained in dependency_pins.json and the old
C27 dependency ledger. This campaign uses the ACTUAL local worktree.

| Source | Use and exact status |
|---|---|
| C27 CONTINUATION_01 FULL_PROOF/FINAL_VERDICT/CHECKPOINT | Source existence; accepted at its exact199-operation scope. |
| C27 aligned_source_and_owners.json; independent_audit2.json | Complete58-owner source/cut/Bank receipt; distinct same-agent implementation PASS reused. |
| C27 ACTUAL_E4_EFFECTIVE_OWNER_LEDGER.md | The later(661,3) payment is a frozen success. |
| C26 SOURCE_FORCED_FROZEN_EXPANSION.md | Counting-level total-H exchange and eligibility closure; storage was separate, now quantitatively bounded in restricted theorem. |
| C26 DIRECT_CONSUMER_SOURCE_BRIDGE.md | Raw direct e4 owner cycle isolated for its stated comparison; no free endpoint inferred. |
| C25 T19_ARRIVAL_LOCALIZATION.md; CANONICAL_G_V_EXCLUSION.md | Original selected/pre-j and safe-G scopes retained; pending universal audits not promoted. |
| C24 SOURCE_SPEC.md; SOURCE_FORCED_OCCUPANCY_BOUND.md | Actual static period/block license, literal ownership, exterior-source limitations. |
| C23 FINAL_VERDICT.md | Nonidentity correction G=-1/R=0 retained; new maps use original units. |
| C22 CREATOR_POLICY_COMPATIBILITY.md; PAIRED_LEDGER_FUNDING.md | Every-producer LAST-tail creator rule and exact own-tail policy. |
| C21/C20 order-class checkpoint interfaces | Exact prior restricted/pending scopes retained, no five-macro analogy. |
| C19 BIRTH_GROUP_REDUCTION.md | Distinct selected births and own-tail source rule. |
| C15 UNIFORM_LEAF_CHANNEL_THEOREM.md | Inspected path-to-star frame proof, per-key lifetime pairing and branch frontier; historical density/all-SS prerequisites retained. |
| C14 CLOSED_PERIOD_CORE_CONSTANCY.md | Marked core cannot grow under fixed-mark accesses; old five-core absence remains valid in insertion family. |
| C14 UNIFORM_R_TRANSFER.md | Exact I(r), license A/B, all three E_r clauses; conditional only. |
| Step1 source_allocation.py / CD6 cd6_allocator.py | Original accepted selector/dispatch unchanged; no five-key/core9 instance supplied outside its domain. |

New count and source-family proofs state their source assumptions explicitly.
An exact trace audit does not retroactively seal all old universal claims.
''')
bitrows=[]
for z in inv['bits']:
    bitrows.append([z['unit'],z['A_depth'],z['macro'],z['source_block'],','.join(z['comparison_preimages']),z['auxiliary_owner'] or '—',z['effective_owner'] or 'UNOWNED','empty P',z['C23_repair_association']])
write('W199_PHYSICAL_BIT_INVENTORY.md',f'''# Complete physical bit inventory

{status}
All522 actual bits are below. w199_inventory.json supplies every exact
target/mode, StepEv frame, preimage demand for each named comparison,
source macro/block and original A depth. Auxiliary/comparison ownership
is distinct from effective full ownership. The listed464 unowned bits
are not declared eligible for arbitrary hypothetical future demands.
For the ACTUAL current residual set, the eligibility family is empty.
C23 associations are comparison debits, not an additional physical spender.

{table(['unit(t,j,b)','A depth','macro','source block','comparison membership','aux owner','effective owner','current eligibility','C23 repair'],bitrows)}
''')
drows=[]
for z in inv['demands']:
    drows.append([z['demand'],z['effective_unit'],z['first_effective_stage'],z['full_natural_comparison_unit'] or '—',z['common'],bool(z['selected_zero_origin']),bool(z['selected_birth']),z['first_own_tail_comparison_unit'] or '—','FROZEN / paid'])
write('W199_FULL_DEMAND_OWNER_LEDGER.md',f'''# Complete original full-demand ledger

{status}
One row per actual full B double. Multiple source/comparison descriptions
never duplicate a physical demand. Raw h6=f6 is justified here by the
original special-five-key-domain audit; that equality is not generalized.
The full common restriction is fixed first, then successful effective
exchange values, creator/T19/own-tail/j stages and the later gap payment.
Creator and own-tail comparison values do not replace effective owners.

{table(['demand','effective unit','first successful stage','natural h0 comparison','common','T19 zero','selected birth','own-tail comparison','status'],drows)}

u_v=(769,1,1) has effective owner e4=(771,4). The later original success
(661,3)->(621,2,0) remains fixed. No current demand is unpaid.
''')
write('W199_RESIDUAL_DEMAND_SET.md','''# Exact current residual set

W28-FUNDED. The inherited CURRENT effective map has58 distinct demands
and58 distinct actual units, total on the full domain. Therefore P*=empty.
The historical57-entry stage had root(661,3), not merely a comparison
birth e2; C27's later success(661,3)->(621,2,0) already paid it. That
success is frozen too. Removing it would alter the problem.

Hence g*:empty->U* is the empty extension and U* has464 unowned units.
There is no current residual-specific eligibility or neighborhood to
optimize. This is NOT evidence that every guarded source is funded, or
that all464 units could fund a different claim under every contract.

The source is R-type; no new physical unpaid G-deficit demand is invented
from the separate corrected G=-1 ledger. Generic G compensation is a
different obligation. Exact JSON inventories and original audit are reused.
''')
write('W199_EXACT_ELIGIBILITY_AND_BANK25.md','''# Actual eligibility and physical storage

The authoritative C24 SOURCE_SPEC.md uses original static one-period/block
eligibility, with stronger storage/comparison requirements retained when
stated. It does not impose a newly invented causal deadline or terminal
key condition. A nonuniform future E(p) cannot be supplied by assuming a
matching. Here P*=empty, so its exact indexed eligibility family is empty.
The ACTUAL58 existing assignments are inherited unchanged and fully listed.

The endpoint schedule processes original A-bit endpoints(t,0,j,b), then
full B demand endpoints(t,1,k,0). It stores an earlier unit as that actual
bit, or an earlier demand as a debt record, and closes the record at the
other endpoint. Ignored units do not enter the bank. Counting both kinds
of records is a conservative sufficient physical bound under the inherited
one-period/block accounting. It is not a necessary characterization of
every possible stronger scheduling license or a universal causal theorem.

w199_inventory.json includes every116 endpoint transition of the actual
58-owner map. Peak6, empty actual573/771 seams. Original raw six-key
working peak10 and f6 endpoint peak4 remain. Every original donor is in
the same actual period. No Hall implication substitutes for this schedule.

For new source-uniform extensions, cut-path comparison proves only the
SUFFICIENT pointwise bound B_extended<=B_H+2B_a. Actual source eligibility
and any additional reservations are separate premises. These are not
silently supplied on all guarded histories by W199's passing receipt.
''')
write('W199_COMPLETE_PHYSICAL_FUNDING.md','''# W28-FUNDED — complete inherited construction

Every original full demand is already paid by the exact frozen map in
W199_FULL_DEMAND_OWNER_LEDGER.md and w199_inventory.json. The complete
source/owner receipt and distinct C27 replay are pinned, and the new
independent inventory audit checks domain/image/Bank/source membership.

The C28 extension is g*=empty because P*=empty. It changes NO old value,
does not claim another spare for e4 and has no additional storage load.
This is a valid, vacuous extension of a genuinely complete58-demand map,
not a new matching inferred from522>=58. Scalar checking is separately
58<=522 with margin464; the explicit injection establishes funding.

No W199_FROZEN_EXTENSION_OBSTRUCTION.md is created: the actual complete
map disproves an obstruction for THIS witness. The source-uniform U28
question requires different mathematics and remains explicitly separate.
''')
write('W199_FINAL_FUNDING_VERDICT.md','''# W28-FUNDED

ALL current58 original demands are paid. P*=empty; U* has464 unowned
actual bits; g*=empty. e4 retains u_v, and the later gap success is frozen.
Original source/cut/corrections are unchanged and peak6 fits Bank25.
The original separate source verifier is reused; new inventory independently
checked without repeating completed original-source replay.

Witness decision is complete. It is vacuous as a test of new donor escape
after all successes, so no universal theorem follows merely from W28.
''')
write('SOURCE_UNIFORM_ESCAPE_INVARIANT.md','''# New source-level mechanisms and their exact boundaries

1. C28-C: an actual hard frame with H/Q word(>=3/1,1/2,1/1,1/3,1/1,
   1/2,1/1,1/6) supplies j ordinals2..6 for its five native deficits and
   g/t/p second units for up to3 outside native deficits per catchment.
   This builds a FULL independent H before consulting frozen owners.
2. The pure universal catchment-forcing conjecture is REFUTED by the
   exact459-operation guarded source: one Q6 frame, five outside native
   deficits. It is FUNDED, not a Coarse-Double or architecture counterexample.
3. C28-H replaces that insufficient condition with disjoint branch-free
   closed-leaf blocks and hard-frame catchments. Leaf normalization keeps
   every original natural h0 value. Current examples have raw peak8.
4. C28-I proves complete prescribed frozen funding for V^m W, every integer
   m>=1, arbitrary ordered BST substitutions at14 external gaps, reflection,
   and one actual carried first-V bit. Peak6 independent of m. This is a
   PROPER subclass, not a redefinition of U28. It tolerates unbounded
   outside natural deficits(m+1), showing why that naive count was wrong.
5. C28-B uses intrinsic actual leaf potential D_leaf=L-1. The signed
   residual2min(H,3)-beta-z has only four possible negative count classes.
   The beta3 class is a three-branch marked comb. A uniform correction J
   and all owner/storage bridges are still unproved for the whole class.

None of these is a desired-matching assumption. Each completed smaller
construction specifies actual source event ordinals or actual alternating
paths. The full source-forced hybrid coverage or signed-J law remains
the load-bearing missing theorem. New restricted proofs/audit boundaries
are in their theorem files; historical universal pending labels remain.
''')
write('SOURCE_FORCED_GLOBAL_EXPANSION.md','''# Global expansion: derived smaller results, full claim OPEN

The all-W/all-unpaid-subsets eligible expansion target is not assumed.
W199 has no nonempty unpaid subset, so its Hall condition is vacuous.
In the C28-C/H restricted classes, explicit full source H and unchanged
inverse-a paths produce distinct endpoints; counting/Hall follows from
that injection. Cut bounds and actual eligibility remain separate.

The proposed source-forced PURE frame-catchment partition is false.
The separate459-operation history is original reachable, triple-closed,
fully guarded e4, completely funded, and has one Q6 frame but five
outside native deficits. See catchment_forcing_countercertificate.json
and family_independent_audit.json. The family V^m W proves unbounded
outside native counts with only one guarded deep frame, uniformly in m.

The failed sufficient route was altered and attacked again: leaf blocks
absorb its nondeep returning insertions and yield a hybrid comparison.
Natural-compatible normalization and a quantified storage bridge are
explicit. No universal source forcing of this hybrid partition, all
exception-receipt coverage or all-E eligibility closure is established.

New precise alternative: prove signed preservation on the four negative
branch classes of C28-B with intrinsic seven-mark state data, including
the H2 zero helpers; or source-derive a complete hybrid decomposition
and its frozen profile bounds. This is additional source mathematics,
not an identity or a renamed global cardinality inequality.
''')
write('G_BLOCK_SOURCE_COMPENSATION.md','''# Corrected G compensation scope

Original C23 G=6-7=-1 and R=8-8=0 remain unchanged. W199 and V^m W use
the actual R-type frame; no G deficit or extra credit is invented there.
Their source comparison does not count shadow events as new physical units.

NEW RESTRICTED BRIDGE: C28-C works directly with the full original j..e
H/Q table, independently of an identity-case G/R surplus. Whenever an
actual G-type recovery has that full table, its entire catchment has at
most3 outside native deficits, the actual eligibility bridge holds and
the stated frozen cut bound fits25, its original full demands are funded
by the five j and three loop source slots. That is an explicit larger-
window physical comparison, not a declaration that the corrected G
block itself has surplus or that an occupied R-v bit becomes free.

Universal G compensation is STILL OPEN: it is not proved that every G
history meets these catchment/owner/storage premises, or that intersecting
G and other source windows admit one globally compatible assignment.
Smallest remaining G Box: source-derive the supplier/branch-frontier
license for a corrected G=-1 block with arbitrary outside successful
F-only interceptors, and prove their joint storage/noncollision. Preserve
every actual shadow repair association and old owner throughout.
''')
write('EXTERIOR_OWNER_COVERAGE_MATRIX.md','''# Exterior receipt coverage

| Class | Existing exact evidence | U28 / Gate U gap |
|---|---|---|
|Safe G-v|C25 qualified original raw/five-key scope; old pending labels retained|Does not imply R-v freedom or all receipts.|
|R-v epsilon0|C26 raw rank4 discard on high-core hypotheses|Discard does not release pre-existing full ownership.|
|R-v epsilon1/direct e4|C27 genuine W199; C28 exact full map and V^m W family|All guarded receipts outside family still need source escape/profile proof.|
|Older-common-normalized f6|Actual dispatcher preserves applicable old f5; none applicable on present examples/family|Arbitrary original core9-five-key receipt interference not classified universally.|
|Retained-key full/erased discrepancies|Exact original QF/QE and ordinal overlap inventories|Other source-global interceptions need complete paths and eligibility.|
|Erased C receipts|Original A-only-in-aux semantics preserved|Old full successful owners cannot be retired as though they were auxiliary-only.|
|Direct H1/Q3 or Q4 auxiliary consumers|C26 conditional first-consumer paths and raw-cycle isolation|Only one e4 subclass has full present source analysis.|
|Paired q5/q1 consumers|Inherited core11 high-core law at declared raw scope|No universal normalized/common/exterior compatibility proof here.|
|Core8 FIFO|Separate inherited six-key backend|Outside present high-core guarded-e4 target; broader Gate U still needs its interface.|
|Corrected flip owners|C23 original p-bit repair retained and instantiated|Cannot double-count repair bits or infer global G funding.|
|New frame comparer|Full actual source H for <=3-outside-deficit catchments|Pure universal catchment forcing refuted; hybrid coverage not proved.|
|Branch-free closed leaf blocks|Uniform local comparison and natural normalization; V templates audited|Not every nondeep block is branch-free; general signed frontiers remain.|
|Other frozen exterior successes|Every actual success preserved; provenance exceptions explicitly retained|No unproved support-only bound on their number or image interceptions.|

No comparison-preimage is silently identified with its effective root.
Additional frozen receipts or reservations must appear in the actual a/E
contract; nothing makes them movable. Full U28 is not assembled from this
matrix until every required source class and interface is proved.
''')
write('MIXED_ORDER_EFFECTIVE_COMPATIBILITY.md','''# Mixed-order interface

The four C20/C21 ancestor-order derivations retain their original scopes
and pending audit labels. They have not been re-proved or promoted here.
C28-C's source slot construction uses the EXPLICIT eight-macro H/Q table,
so key reflection or ordering does not affect it once that table holds.
C28-N proves any two distinct actual frames with that cost word have
disjoint macro inventories. This is a genuine collective comparison seed
noncollision result, not freedom of those seeds under every old owner.

No source theorem is supplied that every mixed-order recovery lies in
that table-defined class, or that all intervening source deficits admit
the F/L partition and legal eligibility/profile bounds. Other order
windows can interact with transported effective owners and correction
capacity. Complete mixed-order effective compatibility remains OPEN.
The independent new comparator is a separate proof map, never mutation
of one of the older successful comparison or effective assignments.
''')
write('ARBITRARY_SUPPORT_ESCAPE_LIFT.md','''# Support and population quantifiers

The arbitrary insertion theorem is uniform in m, actual source length,
reflection, and arbitrary finite BST populations in the14 external gaps
of its13-anchor source. Its marked support remains exactly SEVEN.
The opaque-gap commutation proof is symbolic; no finite fringe cutoff
is used. Arbitrary anonymous ancestors above the known A anchors are
NOT all equivalent to external gaps and are not covered by that lift.

C28-C/H are uniform source statements whenever their explicit seven-key
geometry/count/cut hypotheses hold, not only on the two stored examples.
The exact off-path budget r>=Q+1+beta+(1-z) holds at arbitrary r; the
special beta<=3, capped6-unit budget, four negative classes and Bank
constants are SEVEN-key consequences. They do not prove every r>=7.

The original r-4 carry/width obstruction persists. No increase of Bank25
and no extrapolation of literal Q6 to arbitrary r is licensed. A future
lift needs a support-parameterized source comparer or signed debt and
actual ownership/storage proof, not a constant six-key lookback assumption.
''')
write('FROZEN_EXTENSION_ARCHITECTURE_REASSESSMENT.md','''# Architecture preserved; one sufficient partition rejected

W199 is fully funded. The separate459-operation witness is fully funded.
No complete eligible-neighborhood or Bank25 obstruction to the frozen
extension architecture is established. Hence OUTCOME E-F is NOT claimed.

What fails is precisely the proposed pure F-catchment source-forcing rule.
Its exact counterexample is retained. Replacing that sufficient condition
by a hybrid source comparer repairs the counterexample without moving old
owners or changing Coarse-Double. The V^m W proof closes a real uniform
subclass. It does not prove that the broader hybrid route is exhaustive.

For any ACTUAL complete H, counting-level frozen extension is constructive;
the new cut inequality identifies an additional physical storage condition.
For nonuniform E, the old eligibility closure/transport remains a separate
source theorem. Frozen ownership is not automatically a global obstruction,
nor does a full static matching automatically settle Bank25.
''')
write('ADVERSARIAL_SOURCE_CONTROLS.md','''# Adversarial evidence and exact scope

W199's later successful gap assignment is retained, making P*=empty.
The R-v/e4 bit remains owned and its isolated cycle is never called free.
All522 unit identities and58 demands are inventoried; old source replay
is reused rather than repeated. The separate48-source control reduces
padding while preserving every original KEEP A state, two origins and
actual qE4; its complete policy is independently checked. It is not W199.

A bounded A-state search for a short j preparation found no witness in
its explored set. It is not a universal exclusion or lower-bound theorem.
Its full query/CPU charge and negative search record are retained.

The first candidate uniform catchment claim was actively falsified by
the independent459-operation source. All operations, A/BF/BE states,
selected lifetimes, normalized branch, successful maps and Bank6 are
explicit. Five outside native deficits and one Q6 refute only that
partition, not funding. A new hybrid comparer repairs it and is normalized
to keep all natural h0 values. Reflection/private-gap lifting and arbitrary
repetition use proofs with exact induction interfaces, not finite passing
tests as universal evidence. No donor from another cyclic copy appears.

C23 signed R correction and actual p bits remain; G=-1 is never upgraded
by count positivity. Frozen extra/intermediate owners are not recolored.
Other exterior receipts, normalized policies, shared recoveries, core8,
other order classes and arbitrary support are explicitly not assumed
covered. No static Hall shortcut supplies a storage schedule.

Source-uniform count classification uses the proven marked off-path
budget, not realizability of abstract tuples. B2 is the original price
PLUS an intrinsic leaf-potential difference, not a replacement of the
actual physical costs. The new branch-minus-two comb has actual Q3/H1;
it is not the historical cold-chart qE4 weight-minus-two class.

Distinct implementation receipts are same-agent audits, not external
review or formal proof-assistant certificates. All failed/limited routes
remain recorded; every semantic process and controller is charged.
''')
write('IAGS_PROOF_TREE.md','''# IAGS recursive reconstruction

BOX W28. Target: exact current witness funding. Conditions: ALL successful
old owners. Inherit C27 complete58-map and audit. Ambiguity: none after
inventory; Pempty. Bridge: explicit domain/image plus old storage receipt.
CLOSED W28-FUNDED, empty extension. No artificial57-owner rollback.

BOX F. Target: source-derived complete H. Conditions: hard eight-macro
cost table and<=3 outside native deficits per catchment. New source
lemma: j2..6 and g/t/p second units. Bridge: explicit full comparator,
unchanged-inverse-a paths and B_H+2B_a. CLOSED restricted theorem.

BOX F-FORCING. Target: every guarded source admits only such catchments.
Conditions: original full U28 domain, not rewritten. Recurse into source
loops using saved transitions. Exact459-source REFUTES this sufficient
partition. Keep countercertificate; do not alter original U28.

ALTER sufficient route to BOX HYBRID. Target: compose F with branch-free
closed-leaf blocks. New leaf comparer and h0 normalization. Bridge:
disjoint actual inventories plus cut-profile bound. CLOSED conditional
source theorem; source-forced global partition is OPEN.

BOX INSERT. Target: repeated nondeep obstruction family. Source V is an
exact65-operation triple return; W original199. Inherit explicit policies;
reconstruct canonical raw reset, leaf/creator/own-tail locality and one
real carry. Base/self-loop/final templates prove V^m W for all m>=1
and opaque gap BST substitution. CLOSED specified source/receipt subclass.
No completed full-U28 proof file is created from this smaller result.

BOX BRANCH. Target: locate exact remaining source mechanics. Off-path
marked budget gives beta<=3 and four negative B2 count classes; all
H>=2 nonnegative. CLOSED classification under inherited SS source scope.
New correction J, its zero-helper signed preservation and global frozen
eligibility/storage are OPEN. No fixed-nine-Score potential is imported.

PARENT U28/GATE U. Target unchanged. Hybrid coverage or complete signed
branch repayment, all exterior/normalization profiles, mixed/shared
source assembly and arbitrary support remain OPEN. Reconstructing upward
is permitted only after those exact bridges exist. C29 is not ready.
''')
gate_rows=[
['U28.1 I(6)','ACCEPTED','C14 certified constructive dispatch/license at its original scope; same-agent distinct verifier, not external formal proof.'],
['U28.2 guarded e4','RESTRICTED','W199 complete; V^m W complete specified family; C28-C/H conditional source classes. Full original class OPEN.'],
['U28.3 exterior owners','OPEN','Actual old owners fixed; arbitrary normalized and unselected exterior receipt coverage not proved.'],
['U28.4 corrected G','RESTRICTED / OPEN','Direct full-frame comparison funds qualifying G catchments; universal G=-1 source compensation not proved.'],
['U28.5 mixed orders','RESTRICTED / OPEN','Table-defined frames have disjoint source slots; every mixed-order/source interface and effective storage not established.'],
['U28.6 arbitrary r','OPEN','New bank constants and literal Q6 are seven-key. No all-r source license.'],
['U28.7 other classes','OPEN','Branch-deficient nondeep, smaller cores, other arrivals and anonymous A-ancestor configurations remain.'],
['U28.8 owner/physical contract','VERIFIED ON INSTANCES / SPECIFIED FAMILY','Full original contract retained. Generic eligibility and frozen profile bridges still hypotheses.'],
['U28.9 all E_r','NOT PROVED','Neither all-r license E_r2 nor all-source eligibility/storage E_r3 follows.'],
['U28.10 C29','C29-ASSEMBLY-BLOCKED','Do not begin unconditional promotion. Continue at the source branch/frontier theorem below.']]
write('GATE_U_PREREQUISITE_MATRIX.md',f'''# C29-ASSEMBLY-BLOCKED

Exact original source is C14 UNIFORM_R_TRANSFER.md, inspected directly.
I(r) is a witness-rich LOCAL license A(disjoint source seeds) or B(signed
source credit), including natural/common owners, original actual period,
eligibility and Bank25. Its theorem remains I(r-1)+E_r=>I(r).

E_r1: same original A execution, legitimate erased recurrence/domain,
actual fixed fE and absolute cut/event bijection. Basic correspondence
inherited; all new instances/family have explicit compatible data.
E_r2: a specified r-key full-source license derived independently from
original rotations/marked geometry, fE and CD(r). OPEN for all original
sources/arbitrary r; new restricted comparers do not supply it universally.
E_r3: common pairing, E-only retirement, block eligibility, legal cuts and
Bank25 with every old success unchanged. Instance/family verified; generic
all-owner/eligibility/storage theorem remains OPEN.

{table(['gate','status','exact evidence or gap'],gate_rows)}

No stronger all-core I(5) selector is inferred from scalar CD5. Accepted
CD6 is not reopened. Unconditional Gate U, Step3, Universal Coarse-Double
and Dynamic Optimality remain OPEN.
''')
write('C29_UNCONDITIONAL_TRANSFER_HANDOFF.md','''# Not ready for unconditional assembly

Current decision C29-ASSEMBLY-BLOCKED. Reuse completed W199, new source
audits and actual proof receipts; do not restart existence or repeat old
certificate checks. Preserve the exact new counterexample and the hybrid
repair; pure native-deficit count per deep frame is false.

NEXT BOX E28-COMB:
Target: source-exact signed repayment for H1,Q3,beta3,z1 macros, the
three-branch marked comb. Its ORIGINAL physical price is2H-Q=-1;
after the intrinsic leaf potential its residual is-2. Construct two
distinct actual source-origin repayment obligations and prove signed
preservation through original helpers/leaf births, or produce a genuine
source refutation of the proposed mechanism. Account for all old owners
and actual cut; do not assume every abstract comb is realizable.

Conditions: original seven-mark/core13 source and the actual H1 geometry,
all permitted private A ancestors, reflected orders, root repeats and
every original operation. Inherit the exact C15 path-to-star ledger,
accepted CD6/normalization and new count bound. Bridge upward: a source
repayment theorem for this class plus the three branch-minus-one classes
and ALL zero/positive preservation rules could supply signed source
credit; ownership/Bank25 and other Gate U source classes remain separate.

Alternative source route: prove an exhaustive admissible F/L or richer
source-block partition with explicit outside branch-frontier supply,
eligibility closure and compatible frozen cut profiles. The new hybrid
does not cover every source by assumption. No universal J or hard width
is declared established; [0,14] is only a Bank25-compatible target range.

Only after ALL original E_r clauses at EVERY required r are proved may
C29 assemble unconditional transfer/induction. This handoff is focused
proof work, not permission to label missing premises complete.
''')
write('INDEPENDENT_AUDIT_STATUS.md',f'''# New verification and trust boundary

PASS independent_audit.json: new522/58 inventory, no old source replay;
separate48-source pointer replay and full policy; source comparers and
universal-variable arithmetic/propositional certificates.
PASS family_independent_audit.json: NEW459-source pointer replay, full
114-demand policy, exact partition counterexample, hybrid comparison,
and empty/one-carry induction interfaces for arbitrary-m theorem.
PASS reduction_independent_audit.json: four necessary branch count
classes and explicit natural-compatible normalized full comparator.
PASS window_noncollision_audit.json: all possible proper overlaps of the
exact eight-macro cost word, a complete combinatorial proof check.

Verifier reuses the previously accepted DISTINCT mutable-parent-pointer
implementation as a library; it does not import producer engines or
allocators, and it does not repeat W199's completed source replay.
New program checks and old dependency proofs are distinguished. Induction,
opaque-subtree commutation and off-path witness arguments are inspectable
mathematical proofs with checked local interfaces; the software is not a
formal proof-assistant verification of every universal source lemma.
All audits are operated by the SAME research agent; no external peer
review. Historical pending universal proof labels are preserved.

Remaining audit checklist for FULL U28 is mathematical as well as
verification work: exhaustive source signed repayment/hybrid coverage;
all normalized/exterior receipts; target eligibility/physical storage;
multiple recovery and mixed-order assembly; arbitrary-support scope.
None is declared complete merely because current examples pass.

Cumulative CPU{total}/7200; symbolic{groups['symbolic']}/240;
independent{groups['independent']}/600. New C28 queries{newqueries};
retained continuation query sum{qsum}; adding preserved older engine
calls gives conservative{qsafe}<2000000. All phase/controller charges,
including bounded unsuccessful source search, are retained. No reset,
budget reclassification, cap extension or verifier-controller bypass.
''')
write('FINAL_VERDICT.md',f'''# OUTCOME A-W — witness physical funding established

W28 is complete: the actual fixed W199 has ALL58 demands already funded.
Its later gap payment is a frozen success, so P*=empty, g*=empty and
there is no additional donor request. u_v stays owned by e4. All522
physical units/58 demands, source eligibility at the empty residual set,
original signed correction and Bank6 receipt are explicitly preserved.
This is a successful witness-level theorem, not full Campaign28 closure.

New mathematical advances beyond the vacuous witness extension:

* A source-defined full comparer from the actual hard j..e frame funds
  its five native deficits from j ordinals2..6 and three outside slots
  from g/t/p second units. Quantified frozen storage bound is explicit.
* The first global catchment-forcing conjecture was REFUTED by a genuine
  independently verified459-operation guarded source, NOT a funding
  obstruction. It is completely funded with peak6.
* The route was repaired by branch-free closed-leaf blocks, natural-owner
  normalization and frame catchments. Actual normalized raw peak8.
* A complete source-uniform insertion theorem funds V^m W for EVERY
  integer m>=1 under its specified frozen receipt recipe, with Bank6,
  arbitrary ordered external-gap BSTs and reflection. Its exact induction
  interfaces are checked; this proper subclass is not the full U28 class.
* All actual hard-frame source seed windows have collective noncollision
  at the explicit cost-table scope. Intrinsic leaf credit gives an
  exhaustive four-class negative branch-deficit reduction; no new J is
  falsely inferred from it or from the old fixed-nine-Score certificates.

U28 remains OPEN: a source-forced complete partition or signed repayment
for the remaining branch classes, generic normalized/exterior receipt
eligibility/Bank25, mixed/shared recovery compatibility and arbitrary
support are not established. No frozen-extension architecture refutation,
Coarse-Double counterexample, or unconditional Gate U is claimed.

Decision: C29-ASSEMBLY-BLOCKED. The exact next source Box is E28-COMB in
C29_UNCONDITIONAL_TRANSFER_HANDOFF.md, with its zero/helper/owner bridges
explicitly retained. Step3, Universal CD and Dynamic Optimality stay OPEN.

Branch `{e['branch']}`, HEAD `{e['head']}`. Tracked tree clean;
{len(pins['pins'])} old local pins match. Original source/owners/CD6/caps
preserved. Distinct implementations are same-agent audits, not external
peer review or formal proof-assistant certification.
Cumulative CPU{total}/7200, groups{groups['symbolic']}/240 and
{groups['independent']}/600; conservative queries{qsafe}/2000000.
''')
write('CHECKPOINT.md',f'''# C28 checkpoint — A-W, restricted uniform theorems; U28 OPEN

Authoritative final verdict FINAL_VERDICT.md. W199 unchanged,58/58 paid,
Pempty. Do not repeat its completed source verification or undo its late
successful payment. Source/cost/owner/full-bit ledgers and all new audit
receipts are saved. Branch `{e['branch']}`, HEAD `{e['head']}`.

Reuse CATCHMENT_COMPARISON_THEOREM, HYBRID_COMPARISON_THEOREM and
NEUTRAL_INSERTION_FAMILY_THEOREM. The source-fixed65-operation V returns
the entire triple, active leaf channels are local, debt2 resets raw bank,
and the old owner stages are componentwise. One physical first-V unit
funds the sole shifted W root for every m>=1; peak6. Natural-compatible
independent hybrid raw comparator also saved. No new bit is borrowed
from another symbolic copy. Preserve current four-copy success9213→57710.

Do not resurrect the FALSE pure F-catchment forcing rule. The exact
459-source countercertificate has one Q6 frame and five outside native
deficits yet complete funding. The hybrid repair absorbs its returning
nondeep blocks; full original source coverage of that repair is unproved.

Precise remaining target E28-COMB: original H1/Q3/beta3/z1 source macros,
three-branch marked comb, signed leaf-adjusted residual−2. Prove its actual
joint source repayment (or exact mechanism refutation) with old owners,
then the three−1 classes and ALL zero/positive preservation rules. A
new signed J is not yet proved; old chart normalization is not valid here.
The new off-path bound and D_leaf identity are in BRANCH_DEFICIT_CLASSIFICATION.

Gate U E_r2(all-source/arbitrary-r license) and E_r3(all-owner eligibility,
physical storage and cut compatibility) remain OPEN. C29 not ready.
Current authoritative usage is resources_checkpoint.json; no cap reset.
Global{total}/7200, symbolic{groups['symbolic']}/240, audit{groups['independent']}/600.
Conservative retained query count{qsafe}/2000000; other hard caps unchanged.
''')
resources={'status':'CUMULATIVE_NO_RESET','prior_uniform_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'global_cap':7200,
    'global_remaining':7200-total,'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
    'group_remaining':{g:e['group_caps'][g]-v for g,v in groups.items()},'phases':phases,
    'all_producer_independent_and_controller_charges_retained':True,'new_C28_source_queries':newqueries,
    'inherited_continuation_source_queries':e['inherited_source_queries'],'continuation_source_query_sum':qsum,
    'preserved_older_engine_calls':e['inherited_C15_C27_engine_calls'],'conservative_all_queries':qsafe,'query_limit':2000000,
    'conservative_remaining_queries':2000000-qsafe,'query_note':'No inherited per-run/live-state caps changed; also retain this conservative sum across continuations and older calls.',
    'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,'memory_limit_bytes':32*1024**3,
    'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,'resource_authorization':e['resource_authorization'],
    'metadata_CPU_excluded_under_inherited_convention':{'entry_checkpoint':e['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()},
    'full_U28_closed':False,'C29':'ASSEMBLY_BLOCKED'}
out('resources_checkpoint.json',resources)
out('C28_RESULT_CERTIFICATE.json',{'outcome':'A-W — W199 complete, residual extension vacuous','W28':'FUNDED','P_star':[],
    'source_uniform_restricted_results':['C28-C frame catchments','C28-H hybrid leaf/frame comparisons','C28-I arbitrary V^m W prescribed-source funding','C28-N hard-frame slot noncollision','C28-B negative branch count classification'],
    'full_U28':'OPEN','source_forcing_candidate_refuted':'pure one-frame/<=3-outside-native-deficit catchments',
    'frozen_extension_architecture_refuted':False,'C29':'ASSEMBLY_BLOCKED','CD6_reopened':False,
    'Universal_CD':'OPEN','Dynamic_Optimality':'OPEN','branch':e['branch'],'HEAD':e['head'],
    'audits':['independent_audit.json','family_independent_audit.json','reduction_independent_audit.json','window_noncollision_audit.json'],
    'external_peer_review':False,'proof_assistant_certification':False,'inherited_pins_matching':len(pins['pins'])})
manifest={'status':'CONTENT_CHECKPOINT_NOT_EXTERNAL_OR_FORMAL_CERTIFICATION','branch':e['branch'],'HEAD':e['head'],
    'outcome':'A-W; full U28 OPEN','inherited_pins_rechecked':len(pins['pins']),
    'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.iterdir()) if p.is_file()]}
out('campaign_manifest.json',manifest)
out('publication_exit.json',{'metadata_CPU_at_final_checkpoint':time.process_time(),'source_semantics_executed':False,
    'manifest_sha256':sha(B/'campaign_manifest.json'),'old_pins_checked':len(pins['pins']),'tracked_tree_clean':not bool(git('status','--porcelain','--untracked-files=no'))})
out('publication_seal.json',{'manifest_sha256':sha(B/'campaign_manifest.json'),'publication_exit_sha256':sha(B/'publication_exit.json'),
    'result':'A-W; restricted uniform theorems; U28 open; C29 blocked'})
print(json.dumps({'status':'C28_PUBLISHED','outcome':'A-W','U28':'OPEN','C29':'ASSEMBLY_BLOCKED','old_pins':len(pins['pins']),
    'CPU':total,'groups':groups,'conservative_queries':qsafe,'documents':len(list(B.glob('*.md'))),'manifest_files':len(manifest['files'])}),flush=True)
