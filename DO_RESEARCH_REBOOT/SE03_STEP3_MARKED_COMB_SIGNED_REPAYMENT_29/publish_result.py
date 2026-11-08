"""Metadata-only publication: no source calls, solver, semantic enumeration,
or re-audit of completed old certificates. Historical pins must match.
"""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent

def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*s):return subprocess.check_output(['git',*s],cwd=ROOT,text=True).strip()
e=read(B/'entry.json');dep=read(B/'dependency_pins.json');audit=read(B/'independent_audit.json')
assert git('rev-parse','HEAD')==e['head'] and git('branch','--show-current')==e['branch']
assert not git('status','--porcelain','--untracked-files=no')
for z in dep['pins']:assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in dep['external_pins']:assert sha(Path(z['path']))==z['sha256'],z['path']
assert audit['status']=='PASS_DISTINCT_IMPLEMENTATION_AT_STATED_RESTRICTED_SCOPE'
total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[];queries=0
for path in sorted(B.glob('run_*_result.json')):
    r=read(path);cc=read(B/('controller_'+r['phase']+'_exit.json'));r['controller_CPU']=cc['whole_process_CPU_seconds'];r['total_charge']=r['child_CPU']+r['controller_CPU']
    total+=r['total_charge'];groups[r['group']]+=r['total_charge'];queries+=r['source_queries'];phases.append(r)
qtotal=e['inherited_conservative_queries']+queries
assert total<7195 and all(groups[k]<e['group_caps'][k] for k in groups) and qtotal<2000000
source=read(B/'comb_source_fixtures.json');signed=read(B/'signed_comb_and_control_ledgers.json');family=read(B/'mixed_family_templates.json')
scope='Original seven-genuine-KEEP/maximal-core13/all-SS paired-closed Pair Access source; hypotheses of the inherited source theorem are retained.'
footer='''
Verification: exact new receipts passed a distinct mutable implementation
operated by the SAME research agent; this is not external peer review or
proof-assistant verification. Universal statements use the written source
proofs, not extrapolation from finite source tests. Accepted inherited scopes
and audit-pending labels remain unchanged. Principal MC29, all-r Gate U and
Dynamic Optimality are OPEN. See EXTREMAL_COMB_REPAYMENT.md and
MIXED_COMB_FAMILY_THEOREM.md for the exact restricted positive conclusions.
'''

def doc(n,s):write(n,s+'\n'+footer)

doc('SOURCE_INTEGRITY.md',f'''# C29 actual local source and provenance

Branch `{e['branch']}`, HEAD `{e['head']}`. Tracked worktree clean at entry
and publication. All changes are new untracked campaign files. No Git reset,
checkout, commit, network substitution or old certificate edit occurred.
All {len(dep['pins'])} inherited local hashes and external directive pins match.
dependency_pins.json records the exact paths/hashes; hashes prove provenance,
not mathematical validity. campaign_manifest.json records this publication.

The original source is recovered from CD5_BASE01/PRE_EXECUTION.md,
SE03_STEP1_FUND01/SOURCE_BRIDGE.md and source_allocation.py,
SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md and
CLOSED_PERIOD_CORE_CONSTANCY.md, C15 UNIFORM_LEAF_CHANNEL_THEOREM.md,
C24 SS_SOURCE_INVERSE_LEMMA.md and C28 checkpoint/comparison proofs.
The ACTUAL local worktree is authoritative; no older remote snapshot was used.

A splays EVERY operation. B splays KEEP, including identity root repeats.
DELETE is A-only, never key deletion. a=ceil(depth_A/2), q=floor(depth_B/2).
Every actual event bit is(t,j,b),1<=j<=a,b in{{0,1}}. A natural full macro
ends at a nonroot full KEEP and retains all intervening original operations.
Its H is summed A events and Q full B doubles. No H0 root gap is discarded.

R1: exact target/domain/paired closure and all original operations.
R2: original costs, ordered keys, shadows/charts and event identities.
R3: old source, certified architecture, owners, graphs and caps unchanged;
new comparison candidates are explicitly separate, including failed ones.
R4: FAILED/OPEN never PASS; scope, resource charges and provenance explicit.
Bank25 stays25. All accepted old f5/f6/effective values are literal.

Source scope: {scope} New full owner receipts use a SPECIFIED raw-canonical
six-key input with no older fixed f5 supplied. Four extra-erasure core9
domains exist in these NEW histories; their existence is recorded rather
than excluded. No arbitrary older-normalized f5/f6 theorem is asserted.
''')
doc('C28_INHERITANCE_LEDGER.md','''# Inspected dependencies and exact inherited status

Paths are relative to DO_RESEARCH_REBOOT; exact hashes in dependency_pins.

| Dependency | Status/use in C29 | Inspection |
|---|---|---|
| C28 CHECKPOINT, FINAL_VERDICT | Accepted at their witness/restricted family scopes; universal U28 OPEN | Direct |
| C27 CONTINUATION_01 aligned_source_and_owners / independent_audit2 | W199 58/58 funded, effective residual empty; same-agent distinct checker | Accepted receipt reused, source not rerun |
| C28 NEUTRAL_INSERTION_FAMILY_THEOREM | V^mW, m>=1, specified owners/gap terms/Bank6 only | Direct proof |
| C28 catchment countercertificate / HYBRID_COMPARISON_THEOREM | Pure partition REFUTED; restricted leaf/frame hybrid valid | Direct proof and new-expression row reuse |
| C28 BRANCH_DEFICIT_CLASSIFICATION | Four necessary negative profiles, not universal realizability | Direct proof |
| C26 source-frozen exchange, C25 safe exterior G-v, C24 occupancy | Exact source/eligibility qualifications retained | Inspected via authoritative ledgers/interfaces; not re-certified |
| C23 flip, C22 paired/helper creator policy | Actual nonidentity G=-1/R=0 corrections and successful owners frozen | Inherited exact interfaces, no new universal audit |
| C21/C20 order proofs | Their restricted and audit-pending states retained | Dependency ledgers, no promotion |
| C15 UNIFORM_LEAF_CHANNEL_THEOREM and leaf_channels | Source path-to-star, actual lifetime pairing, all-SS/density hypotheses | Direct proof/code |
| C14 UNIFORM_R_TRANSFER / CLOSED_PERIOD_CORE_CONSTANCY | I(r-1)+E_r=>I(r), conditional; I(6) accepted | Direct proof |
| C24 SS_SOURCE_INVERSE_LEMMA | ROOT-FIRST inverse, not nearest-first | Direct; initial producer mistake retained |
| Step1 SOURCE_BRIDGE / source_allocation / certificate | Actual original five-key scope and fixed input map | Direct, not reconstructed outside its domain |
| CD6 cd6_allocator / high-core source code and inherited debt data | Accepted constructive dispatcher; new raw receipts reconstructed | Direct; distinct source/debt lookup verification |
| R1–R4 in CD5_BASE01/PRE_EXECUTION and C14 SOURCE_SPEC | Original source/cost/scope/cap/status obligations | Direct |

No claimed theorem is externally independently verified here. Content hashes
do not clear historic audit-pending labels. The two new closed source examples
are verified separately; new general lemmas carry their stated hypotheses.
''')
doc('SIGNED_REPAYMENT_DEPENDENCY_GRAPH.md','''# Exact source dependency graph

Original semantics + fixed closed marked-core/all-SS source theorem
  -> actual marked path-to-star (C15)
  -> Q=u+beta, Delta L=u-z and the C28 off-path bound
  -> original rho=2min(H,3)-beta-z
  -> MC29-P exhaustive incoming predecessor geometry + triple separation
  -> MC29-E intrinsic branch-count correction and exact helper debit
  -> MC29-X extremal key-order barrier -> source-forced Hj>=2
  -> disjoint signed pairs/triples for every extremal comb (COMPARISON LEVEL).

Exact W0/W1 words + common diagonal reaching prefix
  -> returning actual A/BF/BE triple S
  -> canonical raw f6 with debt2 maximum at S, fixed common/natural33 owners
  -> full independent H_native and one legal late endpoint per block
  -> direct-sum arbitrary binary-word induction, frozen full34 owners/Bank5
  -> MC29-F complete signed/physical result for this PROPER family.

Missing upward bridges: nonextremal weak P source repayment; high-arity
negative helpers outside selected comb packets; arbitrary supplied old
normalized owners/eligibility/Bank profiles; other source/core/support sizes.
Without these, neither principal MC29 nor all-r E_r2/E_r3 follows.
''')
doc('MARKED_COMB_SOURCE_NORMAL_FORMS.md','''# Exact necessary marked-comb normal form and realizability

Target: classify the actual (H,Q,beta,z)=(1,3,3,1) source, at the frozen
seven-mark/core13/all-SS domain. C28's off-path proof exhausts all7 marked
vertices: root chain g3,g2,g1,x plus one leaf li off EACH gi, each gi degree2.
The physical path has6 edges with marked gi/unmarked pi SS pairs. Ordered
private subtrees are retained; no unknown fringe population is bounded.

H1 means the unique actual positive A access to terminal x is a zig or
one of four double stencils from synchronized root g3. The middle parent
may be anonymous. If the event is an earlier DELETE x, trailing zero-cost
operations are still present and terminal KEEP x is still processed by B.
All-SS source hypotheses, not arbitrary graph edges, license these facts.

PREDECESSOR_CLASSIFICATION proves ALL possible incoming marked degrees:
U=(Q1,beta0,z0), B=(Q1,beta1,z0), P=(Q2,beta1,z1), with actual Hp>=1.
This is necessary source classification, NOT an assertion that every key
assignment has a closed embedding. The exact W0/W1 sources realize P Hp1
and P Hp2, old comb root13,target1, actual I129..256/129..257.
Their JSON contains all original A/BF/BE states, paths and rotations.

The extremal order x=min KEEP,R=max KEEP (or reflection) has a uniform
three-one-event impossibility proof, even with anonymous A parents. Other
orders are not ruled out by this proof. The bounded nonextreme search
saved two genuine B routes and one A preparation for a non-P case, but
NOT a closed source counterexample to MC29-X or its possible extension.
Failed stronger-preparation searches prove no impossibility theorem.
''')
doc('MARKED_COMB_SIGNED_DEFICIT_IDENTITY.md','''# MC29 exact signed identity

At the original source scope, target old leaf indicator z and old marked
unary/branch ancestor counts u,beta satisfy Q=u+beta, Delta L=u-z.
Thus D_leaf=L-1 in[0,5], c=min(H,3), and

    rho=2c-Q+Delta D_leaf=2c-beta-z.

On a genuine marked comb: physical2H-Q=-1, Delta D_leaf=-1, rho=-2.
No chart correction, donor availability or already-paid demand is silently
added to rho. hLambda's branch/death prefix leaves TWO branch frontiers,
but natural h0 has only ONE missing double. Current effective residual
count is a THIRD object, computed from actual locked owners.

Let b=#marked branch vertices and J_B=3-b. E=L-b-1 is D_leaf+J_B-3.
The exact corrected identity is

    sigma_E=rho+Delta J_B=2c-Q+Delta E.

For target old degree d, b2=#degree2 ancestors, k3=#degree>=3 ancestors,
Delta b=1[d+Q>=2]-1[d>=2]-b2. This is a state difference on ACTUAL
source trees, not the historically refuted fixed-nine-Score chart debt.
On the comb Delta J_B=+2 and sigma_E=0. A helper can have Delta J_B=-1;
the closed W0 source realizes exactly that negative helper. All differences
are retained at their true boundaries and telescope only on a closed seam.
''')

lines=['# Exact new source debit and physical owner ledger','',
       'Complete words, reaching prefix, A/BF/BE trees and all event IDs are in comb_source_fixtures.json. No abstract transition substitutes for them.','',
       '|source|macro end|H|Q|beta|z|rho|E before->after|sigma_E|','|---|---:|---:|---:|---:|---:|---:|---|---:|']
for r,s in zip(source['reports'],signed['reports']):
    tags=r['tags'][0]
    for m in s['macro_ledger']:
        if m['end'] in tags.values():lines.append(f"|{r['source_id']}|{m['end']}|{m['H']}|{m['Q']}|{m['beta']}|{m['z']}|{m['rho']}|{m['before']['E']}->{m['after']['E']}|{m['sigma_E']}|")
lines+=['','W0: I129..256, 128 operations, A158,QF34,QE30. W1: I129..257,129 operations,A159,QF34,QE30. Both reach S after the SAME original128-operation W0 prefix from the explicit common diagonal T.',
'','W0 actual prior33 map leaves helper demand(160,2), not two comb demands. Its nominal helper bit(160,1,1) is LOCKED by comb(161,3). The full native comparison sends that comb demand to preparation bit(129,1,1), which is physically real and outside the prior image. Append only (160,2)->(129,1,1).',
'','W1 actual prior33 map leaves helper(161,2); bit(160,1,1) of the extra DELETE1 is locked by comb(162,3). The actual late extension is (161,2)->(129,1,1). All33 old values remain. The separate strong comparison can instead use terminal KEEP13 tail(161,1,0)/(161,1,1); it does NOT replace the current full map.',
'','Both current maps have34/34 demands and Bank peak5. Their physical success alone does not prove a pointwise signed law. The helper debit is included in the pair/triple theorem.']
doc('MC29_EXACT_DEBIT_LEDGER.md','\n'.join(lines))
doc('HELPER_SOURCE_PROVENANCE.md','''# Actual helper provenance

MC29-P helpers p/j are the actual preceding genuine full macros. All their
DELETE/root-repeat operations are included, not invented to improve signs.
The predecessor profiles follow from its destination degree2; helper A cost
is never inferred from beta alone. MC29-X proves a P Hp1 predecessor in
the extremal class has an actual earlier Hj>=2 by the order barrier.

In W0/W1 j ends159, has actual H47,Q1 and capped rho5. In W0 p is KEEP13
at160 with H1. W1 inserts an ORIGINAL DELETE1 at160, then KEEP13 at161;
the two-event helper has H2. The extra operation is charged, never treated
as free. It is part of THIS chosen source family, not a licensed insertion
into an arbitrary frozen history. Source word and exact before/after states
are saved; the independent verifier rebuilds them from a common diagonal.

W1's additional cost shifts the helper branch/reserve prefix to the two
DELETE units and exposes two real terminal KEEP13 tail bits. W0 has no
tail. No raw comparison-free bit is presumed effectively unowned. Exact
locks, paths and old successful values are in the saved physical ledgers.
''')
doc('HELPER_DEBT_AND_SIGNED_BALANCE.md','''# Coupled helper debt, including unfavorable terms

For U,B,P predecessors respectively,

    rho(p)=2cp,2cp-1,2cp-2;
    sigma_E(p)=2cp-1,2cp-2,2cp-3.

The comb rho=-2, sigma_E=0. Hence original rho pairs repay U always,
B/P at Hp>=2, but NOT weak B/P. Corrected E pairs repay U/B always,
P at Hp>=2, but weak P costs sigma_E=-1. Dropping this debit is false.

MC29-X pays weak P using the actual j with Hj>=2 forced ONLY under its
extremal hypothesis. Its destination degree1 gives sigma_E(j)>=2;
degree3 gives sigma_E(j)>=1. Triple sum is nonnegative. The original rho
sufficient condition Hj>=3 is separate and stronger, not silently forced.

W0's helper/comb pair has rho=-2, sigma_E=-1. Actual j has rho=sigma5,
so the full triple rho3, sigma4. W1's pair rho0, sigma1 and full triple
rho5,sigma6. Both terminal source states and helper debts close on each
complete block. In the arbitrary mixed family there is no unpaid carry
at the S seam; helpers are used by one disjoint block only.

The full all-comb route cannot assume every earlier j has H47 or Hj>=3.
General high-arity shallow helpers outside these selected packets still
need a source repayment theorem, not a new exception in E's formula.
''')
doc('MARKED_COMB_FROZEN_OWNER_INTERFACE.md','''# Literal frozen owners and the physical interface

Signed cancellation is comparison-level; it never licenses overwriting a.
The separate full H_native extends every natural h0 value and funds the
single native comb deficit with an actual unused natural predecessor unit:
p ordinal2 for Qp1; p ordinal3 for P Hp>=2; j ordinalQj+1<=4 for weak P
when Hj>=2. Distinct packets have distinct source inventories. Units can
still be effectively owned by a, so this is an independent comparer only.

With a total independent injection H, start at an unpaid actual demand,
follow H then inverse-a until a physical free endpoint. Injectivity forbids
a root from entering a closed owned cycle; different roots have distinct
endpoints. Append only those unpaid roots, leaving ALL old a values literal.
If H is partial, the path can terminate at another undefined demand; that
is frontier relocation and is not funding. Eligibility/same-period/storage
conditions remain necessary even for total H. Sufficient endpoint profile
bound B_extended<=B_H+2B_a is inherited only under its actual source license.

In the two templates the actual owner walks are explicit, total, same-period,
and finish at(129,1,1), with final34 demands and peak5. For arbitrary mixed
blocks, six-key bank maximum2/empty boundaries and block-local33-prefix
maps prove one such legal extension per block, never donor reuse. Theorem
MC29-F covers exactly these specified raw-canonical receipts, not arbitrary
supplied nested-normalized maps. Four possible original core9 f5 domains
exist; no fixed input f5 was supplied on these NEW examples. Old supplied
f5/f6 maps on historical examples are untouched and not assumed free.
''')
doc('W459_PARTITION_REFUTATION_AND_HYBRID.md','''# W459 inherited failure and retained hybrid

The exact459-operation source is V^4W: five outside native deficits with
only one deep frame. This refutes the pure partition requiring each
one-frame catchment to contain at most3 outside deficits. It is not a
funding obstruction; all114 demands are funded, peak6, and all old values
including the successful late root payment remain fixed.

C28's corrected hybrid uses branch-free closed-leaf L blocks and source
frame F catchments. A leaf block returns the marked-leaf set and has
beta+z<=2H at every macro; leaf births/deaths pair WITHIN that actual block.
Natural-owner normalization is explicit. The full independent comparison
and its source/cut/owner/storage hypotheses are retained at their proved
scope. We do not resurrect the false pure F partition under a new name.

New test of E uses the already independently accepted saved source rows,
not a repeated original replay: W199 has4 negative sigma_E macros, W459
has8, neither contains a beta3 comb. Thus E's local correction cannot
replace the old hybrid with a per-edge certificate. The old full funding
and nonidentity G=-1/R=0 corrections remain valid; no old p bit is respent.
''')
doc('NEUTRAL_INSERTION_SIGNED_COMPATIBILITY.md','''# Neutral insertion family: exact compatible and incompatible claims

Inherited V^mW, every integer m>=1, has its specified full source/owner
theorem, Bank6 and external-gap lifting. Its complete original comparison
and actual G/R correction are retained. W199 is already paid58/58,Pempty.

V's marked branch count beta<=1; W's beta<=2. Exact B returns mean each
copy starts from the same B state. Therefore NO marked comb occurs in
ANY V^mW, including arbitrary ordered external-gap terms and reflection.
This is a uniform exclusion proof, not extrapolation from m=4.

Nevertheless each V contains a REAL H1/Q3,beta1,z1 high-arity leaf helper
with sigma_E=-1. Thus the global E-per-macro law fails on every member.
The closed-block signed sum is not lost: V contributes30, W84, giving
30m+84. This is returning-word additivity, not automatic local repayment.
Passing physical funding is not per-edge E preservation. The inherited
hybrid remains the correct restricted composition interface for that family.
''')
doc('FOUR_PROFILE_SIGNED_CLASSIFICATION.md','''# Complete inherited negative counts and exact new transfer

Off-path source budget7>=Q+1+beta+(1-z) implies the complete NECESSARY
original negative profiles below. Dynamic realizability is separate.
For the new E comparison sharpen to7>=Q+1+beta+k3+d: choose TWO disjoint
off-path marked witnesses at every degree>=3 ancestor, and d distinct
children of the target. Degree witnesses are pairwise disjoint.

|H,Q,beta,z|rho|allowed k3|sigma_E|Disposition|
|---|---:|---|---|---|
|1,2,2,1|-1|0,1,2|-k3|binary case canceled; high arity still open|
|1,3,2,1|-1|0,1|-k3|binary case canceled; high arity still open|
|1,4,2,1|-1|0|0|pointwise comparison cancellation proved|
|1,3,3,1|-2|0|0|pointwise cancellation; actual helper repayment still required|

E's NEW negative class, including originally nonnegative helpers, is exactly
within H1,d0,Q>=2,k3>=1. For d>=2 sigma=2c-k3; d1 gives2c-1-k3;
d0 gives2c-min(Q,2)-k3. The strengthened budget proves no other negative
counts and nonnegativity at H>=2. k3=2 forces Q2,beta2, BOTH ancestors
degree3 and all7 marks used: a two-ternary comb, sigma=-2. k3=1 gives-1.
These are necessary classes, not an invented source-realization bridge.

The named E-per-macro candidate is genuinely source-refuted by W0's weak
helper (k3=1). The correction relocates the source obligation from binary
branching combs into high-arity helpers. Universal source repayment and
owner-compatible composition of those helpers remain unproved.
''')
doc('COLLECTIVE_SIGNED_REPAYMENT.md','''# What arbitrary finite collective repayment is proved

MC29-P proves no two marked combs occur within two genuine predecessor
positions: a comb's postroot has degree3 with all children unary, whereas
the state before a predecessor has root degree1 or degree3 with a binary
child. Thus triples(j,p,e) for distinct combs are disjoint even cyclically.
MC29-X chooses pairs/triples inside those disjoint windows and pays EVERY
helper debit under its extremal source hypothesis. Shared keys or anonymous
ancestors do not duplicate original event occurrences. This is a uniform
COMPARISON-LEVEL theorem for all such extremal combs, not full old-owner
coverage in an arbitrary containing source.

MC29-F gives a COMPLETE signed and prescribed physical-owner theorem for
every finite nonempty mixture of W0/W1. Both return the whole triple S.
The raw six-key debt is maximal2 at S; its bank is empty at each seam.
Common/natural maps and their only unpaid helper root are block-local.
Full H_native walks end at distinct preparation units inside their own
blocks and preserve every existing success. Repeating the exact local
empty-boundary transition proves final peak5 for arbitrary multiplicity.
The separate leaf signed triples have balances3 or5; all uncovered original
macros have H>=4 and rho>=2. Source aggregate, debt and bit ownership close.

No such theorem for nonextremal weak-P histories, unrelated normalized
old receipts, mixed high-arity negative helpers or arbitrary support is
inferred. Local packet disjointness does not alone solve those interfaces.
''')
doc('SIGNED_REPAYMENT_ABSOLUTE_PERIOD.md','''# One actual period and both debts

Original diagonal T is explicit in comb_source_fixtures.json. The SAME128
original operations W0 reach S. W0 period I129..256 and W1 I129..257
both return S exactly in A/BF/BE. All source operations and all six-key
auxiliary KEEP erasures are preserved, including DELETEs and root identities.
Every new donor is a literal(t,j,b) inside that interval.

For an arbitrary binary mixture, add actual block offsets to every demand
and unit. Distinct copies have distinct absolute occurrences. No borrowed
previous/next symbolic-period unit exists. Full/erased trees and the
intrinsic marked-leaf/branch potentials agree at the final and initial
boundary, so their signed differences really telescope.

DO NOT confuse auxiliary fixed-certificate debt2 with leaf debt3. Both
are maximal at S in these templates. The family forced-triple leaf
construction uses actual source cut0, working10/12, with full original
H_native profile3. The auxiliary f6 uses the SAME interval/cut, working10.
Current frozen effective map has profile5. Alternative E packet processing
starts at packet5/6 solely to construct a SEPARATE comparer; all endpoints
and its measured profile stay on the original interval, no old map recut.

Arbitrary ordered external-gap BST substitution commutes with every anchor
rotation and preserves actual IDs/costs/returns. Reflection transports
words, trees and the specified receipt; arbitrary new selector values are
not presumed identical. Anonymous A ancestors are allowed in the extremal
comparison proof, but not in the whole physical family lifting theorem.
''')
doc('SIGNED_COMPARISON_ARCHITECTURE_VERDICT.md','''# Architecture verdict — debt is relocated, not erased

Original MC29 is unchanged. Immediate-predecessor rho repayment is FALSE
on the exact weak source: pair rho=-2. The branch-count candidate
E=L-b-1 in[0,4] fixes each binary marked comb but its proposed global
per-macro inequality is FALSE: helper sigma_E=-1, pair sigma_E=-1.
Both failures occur in a genuinely reachable, exactly A/BF/BE-closed source.
They refute those NAMED sufficient mechanisms, not Coarse-Double.

There is a structural replacement at a proper scope: source-forced earlier
repayment for extremal combs, plus a complete returning mixed-helper family
with actual frozen owners. No unverified witness-specific exception is
added to E. Its exact all-edge degree law and high-arity residual class
are preserved, so the next source bridge has a precise target.

Uniform pointwise E preservation is abandoned. A global packet certificate
would need all negative high-arity helpers and all zero/positive transfers
to be repaid, not just binary comb destinations. Universal natural/common
normalization, eligibility, legal cuts and Bank25 are also separate proofs.
The present result does not refute the complete Gate U sufficient mechanism,
the principal all-comb theorem, Universal CD, or Dynamic Optimality.
''')
doc('ADVERSARIAL_SOURCE_CONTROLS.md','''# Adversarial controls and retained failures

|Control|Result|
|---|---|
|Weak helper with zero original rho|REAL paired-closed W0; helper E-debt-1 retained|
|Positive helper obtained by source insertion|W1 extra DELETE1 charged one event, no fictitious cost-free helper|
|Occupied helper second bit|Locked by comb3 in both prior maps; cannot be spent again|
|Two branch frontiers vs effective roots|Two raw branch holes, one native hole, one actual prior unpaid helper root; distinct ledgers|
|Shared/repeated comb suppliers|Disjoint predecessor triples; mixed-word induction uses fresh absolute block IDs|
|Original nested-five domains|Four core9 candidates really exist; arbitrary old normalized receipt not claimed|
|False F partition|W459 countercertificate and old hybrid retained; no reopened unpaid W199|
|G/R correction and direct e4 owner cycle|Old exact source/physical corrections unchanged; new family has no imported H1/Q6 frame|
|Neighbor-period/duplicate/moved frozen donor|Independent checker rejects all three corruptions|
|Gap populations|Opaque rotation substitution proof, not bounded population tests|
|Anonymous A ancestors|Covered in extremal comparison lemma; not silently promoted to the full family|
|Other three negative profiles|Full count reduction preserved; high-arity debt not discarded|

audit_source.py failed because its inverse used nearest-first order.
It failed BF closure, was charged and retained; source2 uses the inspected
ROOT-FIRST source inverse and passes. The first two independent runs
failed a mistaken expected six-key debt3, corrected to ACTUAL debt2 in
the immutable third version; neither failure is counted PASS. Written
family statement is corrected; bank emptiness at S still holds.

nonextreme_source_search.json contains only a partial source exploration:
B route[7,11], comb5 (and1), roots3,7,11, and one actual A preparation.
This is not a full paired-closed comb/owner certificate. Two bounded
attempts at a stronger P preparation returned no witness; their failed
logs/CPU/query charges remain. Absence proves no reachability exclusion.
No new closed nonextremal refutation is asserted from these searches.
''')
doc('IAGS_PROOF_TREE.md','''# IAGS recursive proof closure record

Freeze: MC29_FROZEN_SOURCE_BOX is the unchanged original all-comb target.
Inherit: original semantics, C15 path-to-star, C28 exact identities/owners.
Alter sufficient route: predecessor repayment instead of assumed free tail.
Recurse Box P: target exhaustive incoming comb source; conditions degree2
destination; inheritance path-to-star; ambiguity realizability of each
label subclass; bridge Qp+d=2. CLOSED as a necessary classification.

New lemma Box E: target cancel binary comb deficit; conditions intrinsic
marked tree; inheritance degree identity; bridge rho+Delta(3-b)=sigma_E.
Pointwise comb identity CLOSED; GLOBAL candidate REOPENED/REFUTED on W0.

Recurse Box X: target repay weak P's -1; conditions opposite extreme KEEP
keys, H1 actual macros; inheritance exact predecessor states; ambiguity
nonextremal order; bridge one-event source-order barrier forces Hj>=2.
CLOSED comparison-level at that proper scope, not generic physical owners.

Reconstruct Box F: target complete signed/frozen owner family; conditions
specified W0/W1 returning blocks/raw six-key inputs; inheritance actual
templates, empty debt2 bank at S, total-H exchange; bridge block-local
33-old-owner/one-new-root transition with profile5. CLOSED for arbitrary
finite mixtures and ordered external gaps, reflected transported receipts.

Reopen parent MC29: nonextremal weak P or unselected high-arity helpers
have no proved universal source repayment/owner interface. A-L conclusion
does not change parent quantifiers. The exact next Box is in CHECKPOINT.
No source validity is deduced from an abstract negative chart edge.
''')
doc('C30_GLOBAL_SIGNED_COMPOSITION_HANDOFF.md','''# GLOBAL COMPOSITION BLOCKED — EXACT SOURCE BOX OPEN

Export MC29-P, MC29-E identities, MC29-X restricted source comparison and
MC29-F complete mixed returning source/owner family. Their scopes are
explicit and compatible only where their hypotheses really apply.

The next bounded Box H29-1: in the actual seven-mark/core13 source,
take a shallow leaf access H1,Q>=2 with EXACTLY ONE degree>=3 marked
ancestor. Its corrected sigma_E=-1. Construct a source-defined preceding
repayment packet with nonnegative total sigma_E, actual helper costs,
all physical/frozen owners and a legal Bank25 schedule; or give an exact
original paired-closed counterexample to the PROPOSED packet rule.
Begin with the weak P helper before a nonextremal comb, where the proven
opposite-extremes order barrier cannot be applied. Do not assume Hj>=2.

Conditions: all original operations, full/erased provenance, supplied old
f5/f6 and frozen a, original interval/cut. Inheritance: P classification,
exact sigma_E law, current W0/W1 positive and negative controls. Ambiguity:
source force of earlier supply and generic effective eligibility. Bridge:
one source-licensed -1 repayment theorem, with explicit noncollision, would
cover this helper component; it would NOT alone cover k3=2 or all-r E_r.

If simple two/three-macro repayment fails, the next mechanism must trace
actual earlier A preparation/marked-branch creation or use a separately
licensed comparison exchange. Do not reuse E as a per-edge theorem.
Unbounded nondeep insertions and literal old chart corrections remain.
''')
doc('GATE_U_SOURCE_DEPENDENCY_STATUS.md','''# Gate U14 exact source clauses after C29

I(r) is the witness-rich LOCAL source-credit invariant with either
rotation-derived disjoint own-spare seed license A, or actual packet
signed-credit license B including natural owners, common map, legal
period and Bank25. This is stronger than an existential scalar CD(r).
Accepted transfer remains I(r-1)+E_r=>I(r).

|E_r clause|Current status|C29 consequence|
|---|---|---|
|1 Same A source, erased reachability/domain, recurrence/cut/absolute IDs and fixed fE|Basic correspondence accepted; each instance still needs its source/domain receipt|Exact new family triple returns and IDs verified; no arbitrary f5 selector inferred|
|2 Specified source license A/B independent of fE and CD(r)|OPEN for all original sources/arbitrary r|Complete license only on MC29-F; extremal comparison component MC29-X; global high-arity helpers open|
|3 Common pairing,E-only retirement, eligibility, legal cuts, Bank25 and unchanged successful owners|OPEN universally|Two new actual raw templates and all finite mixtures have exact owners/Bank5; arbitrary normalized/exterior maps open|

I(6) and sealed CD(6) at their original scope remain ACCEPTED. No concrete
invalid dependency was found and they are not reopened. Exterior F-only
ownership, unselected/normalized receipt interactions, universal G=-1
compensation, mixed/shared recovery/source classes, smaller cores and
arbitrary-support lifting remain open at their old scopes. C29 has seven
marks only; the r-4 carry obstruction is not bypassed by a constant-width
seven-key E function. The stronger all-core I(5) selector is not silently
deduced from CD(5). No unconditional transfer or Universal CD follows.
''')
doc('INDEPENDENT_AUDIT_STATUS.md',f'''# Separate implementation and certification status

independent_audit.json PASS from immutable audit_independent3.py. It imports
NO new producer source/allocator/exchange module. The accepted distinct
parent-pointer source/debt decoder supplies primitives; the new checker
rebuilds original prefix, both source periods, all rotations/costs,
canonical raw f6, leaf/natural/common maps, owner paths, packet maps and
Bank profiles. Six opaque-subtree rotation stencils are checked. It uses
{audit['source_queries']} actual source queries. Exact input hashes are recorded.
No old W199/W459 source is rerun: saved accepted rows are reused ONLY for
new E identities. Existing proof receipts/historical statuses are retained.

Same research agent, distinct implementations; NOT external peer review,
NOT a formal proof assistant and NOT automatic universal proof from a
finite test. The uniform extremal and mixed-family statements are written
symbolic derivations; their source arguments were inspected against the
stencils/templates. External independent audit remains pending. No SEALED
label is applied to the new universal restricted manuscripts.

Failures are preserved and charged: first inverse BF closure; two mistaken
six-key debt3 expectations; two bounded nonextremal preparation searches.
Nothing UNKNOWN is treated PASS. No cap/owner reset or disguised verifier
run occurred. Exact current totals in resources_checkpoint.json, including
child and controller costs of every failed and successful phase.
''')
doc('FINAL_VERDICT.md',f'''# OUTCOME A-L — restricted signed repayment established

Principal MC29 is NOT complete. The original source problem is unchanged.

New symbolic theorems: MC29-P exhausts every incoming marked-comb profile
and proves two-step separation. MC29-E gives the exact intrinsic excess
law and proves its proposed per-macro certificate FALSE in a real closed
source. MC29-X proves signed pair/triple repayment for ALL opposite-extreme
KEEP combs, including weak-helper debt, arbitrary anonymous A middle parents
and disjoint simultaneous packets. Its generic physical owner interface is
conditional, explicitly separate from comparison-level repayment.

MC29-F is COMPLETE at its specified proper source/receipt scope: EVERY
finite nonempty mixture of actual W0/W1 returning words, arbitrary ordered
external-gap BST populations and reflected transported receipts has full
original signed repayment AND a physical34-demands-per-block injection
preserving all prescribed successful raw/common/natural/effective owners.
Helpers are actual source operations, their debts/costs retained, no bit
is reused, legal seam is exact, final owner Bank peak5. The two templates
and separate signed packet maps passed a distinct same-agent implementation.

Named failed mechanisms: immediate predecessor always pays original rho;
E=L-b-1 globally satisfies the per-macro law. W0 is a source-exact
countercertificate to BOTH. This is NOT a Coarse-Double counterexample.

Remaining: general nonextremal weak P repayment; high-arity shallow helper
debt outside selected packets; two-ternary residuals; arbitrary supplied
normalized five/six-key and exterior owner eligibility/storage; global
source coverage and arbitrary support. No failed bounded search settles
these source questions. All old W199/W459 funding remains unchanged.

GLOBAL COMPOSITION BLOCKED — EXACT SOURCE BOX OPEN. E_r2/E_r3 are still
OPEN universally. Step3, Universal CD and Dynamic Optimality remain OPEN.
Next bounded theorem H29-1 is stated in CHECKPOINT, with a falsifiable
source target, not a request for unspecified compensation.

Branch `{e['branch']}`, HEAD `{e['head']}`; tracked tree clean, all
{len(dep['pins'])} inherited local pins match. CPU{total}/7200, symbolic
{groups['symbolic']}/240, audit{groups['independent']}/600; conservative
queries{qtotal}/2000000. No caps extended. New manuscripts are not labeled
externally certified or SEALED.
''')
doc('CHECKPOINT.md',f'''# C29 continuation — A-L, principal MC29 OPEN

Read FINAL_VERDICT, EXTREMAL_COMB_REPAYMENT, MIXED_COMB_FAMILY_THEOREM,
BRANCH_COUNT_POTENTIAL_AND_DEBT_TRANSFER and the passed independent receipt.
Do not rerun completed W199/W459 or the new closed-source audits. Preserve
all failed scripts/logs; the successful verifier is independent3, not1/2.
Auxiliary debt at common S is2; separate leaf debt at S is3. Both banks
empty there. Actual full effective maps have34/34 successes, Bank5.
No remaining payment is requested on either NEW fixed fixture.

Smallest next Box H29-1:
Target: actual H1 leaf access, Q>=2, exactly one high-arity marked ancestor,
has sigma_E=-1. Prove source-exact earlier packet repayment with distinct
helpers and frozen owners, or refute one explicit packet rule in an actual
paired-closed history. Start weak P before a NONEXTREMAL marked comb.
Conditions: frozen7/core13/all-SS source, original actual operations,
supplied old normalized owners, Bank25 and legal period.
Inheritance: exhaustive P predecessors; sigma_E exact degree law; extremal
order barrier ONLY when both endpoints are extreme; two closed controls.
Ambiguities: no universal source force of Hj>=2 at other key orders;
effective availability and global helper repayment remain open.
Bridge: a uniform source supply/packet theorem here pays ONE -1 class;
k3=2/two-ternary cases and other source/owner/support interfaces remain.

The nonextreme search is PARTIAL only: it found a B route and one A
preparation, not a full closed stronger P witness. Neither failed bounded
preparation search proves impossibility. No new source-independent edge
list or potential patch may replace the missing reachability/repayment proof.

Use controller and current resource checkpoint without reset. Actual
CPU{total}/7200, symbolic{groups['symbolic']}/240, audit{groups['independent']}/600.
Conservative queries{qtotal}/2000000 leave{2000000-qtotal}. Reserve and all
per-phase/state/DAG/edge/memory caps unchanged. This is NOT a CPU-limit
claim: the unresolved issue is the stated source theorem and owner bridge.
Branch `{e['branch']}`, HEAD `{e['head']}`. GLOBAL COMPOSITION BLOCKED.
''')

resources={'status':'CUMULATIVE_NO_RESET','prior_uniform_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'global_cap':7200,
    'global_remaining':7200-total,'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
    'group_remaining':{g:e['group_caps'][g]-v for g,v in groups.items()},'phases':phases,'new_C29_source_queries':queries,
    'conservative_all_queries':qtotal,'query_limit':2000000,'conservative_remaining_queries':2000000-qtotal,
    'all_producer_independent_and_controller_charges_retained':True,'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,
    'memory_limit_bytes':32*1024**3,'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,'resource_authorization':'Inherited explicit user increases240/600; no additional increase, no reset.',
    'metadata_CPU_excluded_under_inherited_convention':{'entry_checkpoint':e['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()},
    'principal_MC29_closed':False,'outcome':'A-L','Gate_U':'OPEN'}
out('resources_checkpoint.json',resources)
out('C29_RESULT_CERTIFICATE.json',{'outcome':'A-L','restricted_theorems':['MC29-P incoming source classification','MC29-X extremal source signed comparison','MC29-F arbitrary finite mixed returning source/owner family'],
    'named_candidates_refuted':['Immediate predecessor always repays rho-comb','E=L-b-1 per-macro global signed certificate'],
    'principal_MC29':'OPEN','source_uniform_all_combs':False,'Coarse_Double_counterexample':False,'full_funding_peak_on_family':5,
    'audit':'distinct implementation SAME research agent, no external review or proof-assistant claim','Gate_U':'OPEN','C30':'GLOBAL COMPOSITION BLOCKED — EXACT SOURCE BOX OPEN',
    'branch':e['branch'],'HEAD':e['head'],'inherited_pin_matches':len(dep['pins'])})
out('campaign_manifest.json',{'status':'APPEND_ONLY_C29_PUBLICATION','branch':e['branch'],'HEAD':e['head'],'tracked_tree_clean':True,'inherited_local_matches':len(dep['pins']),
    'files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file() and p.name not in ('campaign_manifest.json','publication_exit.json','publication_seal.json')],
    'source_files_not_overwritten':True,'universal_principal_not_promoted':True})
out('publication_exit.json',{'status':'PASS_METADATA_PUBLICATION','whole_process_CPU_seconds':time.process_time(),'semantic_calls':0})
out('publication_seal.json',{'status':'HASHED_PUBLICATION_ONLY_NOT_THEOREM_SEAL','manifest_sha256':sha(B/'campaign_manifest.json'),'publication_exit_sha256':sha(B/'publication_exit.json')})
print(json.dumps({'status':'C29_PUBLISHED','outcome':'A-L','CPU':total,'groups':groups,'queries':qtotal,'remaining_queries':2000000-qtotal,'inherited_pins':len(dep['pins'])}),flush=True)
