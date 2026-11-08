"""Append-only C31 metadata publication. No splay, source query or replay.

Mathematical arguments are in the existing manuscripts. This program checks
provenance and publishes their exact, limited conclusions; it is not a proof
checker. Failed phases and superseded completion descriptors remain present.
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
e=read(B/'entry.json');dep=read(B/'dependency_pins.json')
assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head']
assert not git('status','--porcelain','--untracked-files=no')
for z in dep['pins']:assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in dep['external_pins']:assert sha(Path(z['path']))==z['sha256'],z['path']
c=read(B/'prefix_first_return_countercertificate_v2.json')
audit=read(B/'final_independent_proof_audit.json');algebra=read(B/'entry_compensation_algebra_audit.json')
assert audit['status'].startswith('PASS_') and algebra['status'].startswith('PASS_')
assert read(B/'tuple_suffix_check.json')['status'].startswith('PASS_')
revision=read(B/'revision_bridge_audit.json')
assert revision['status']=='PASS_STATIC_MANUSCRIPT_REVISION_BRIDGE'
for n,h in audit['input_sha256'].items():
    if n!='CLOSED_COUNTEREXAMPLE_PROOF.md':assert sha(B/n)==h,n
assert revision['previous_manuscript_sha256']==audit['input_sha256']['CLOSED_COUNTEREXAMPLE_PROOF.md']
for n,h in revision['input_sha256'].items():assert sha(B/n)==h,n
assert c['W_length']==101 and c['Sigma_helper_through_first_return']==-1
total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[];queries=0
for p in sorted(B.glob('run_*_result.json')):
    z=read(p);control=read(B/('controller_'+z['phase']+'_exit.json'))
    z['controller_CPU']=control['whole_process_CPU_seconds'];z['total_charge']=z['child_CPU']+z['controller_CPU']
    total+=z['total_charge'];groups[z['group']]+=z['total_charge'];queries+=z['source_queries'];phases.append(z)
qtotal=e['inherited_conservative_queries']+queries
assert queries==67 and qtotal==1999997 and total<7195
assert all(groups[k]<e['group_caps'][k] for k in groups)
status='''
Verification scope: the NEW local trajectory has a distinct mutable source
execution and a tuple-engine check of the revised suffix. Whole W101 and
the enormous erased-aligned period are proved by the written source-word
construction, NOT reported as replayed. Same-agent distinct implementations
are not external peer review or proof-assistant verification. Uniform source
inductions retain their manuscript/audit-pending status. Principal
FR31-PREFIX's stated local signed law is refuted; universal FR31-FIX,
all-source owner supply, Gate U, Universal CD and Dynamic Optimality remain
OPEN. Historical receipts, audit labels, owners, R1-R4, Bank25 and caps
are unchanged.
'''
def doc(n,s):write(n,s+'\n'+status)

doc('SOURCE_INTEGRITY.md',f'''# Source provenance and frozen problem

Branch `{e['branch']}`, HEAD `{e['head']}`. Tracked files are clean; the
checkout already contains untracked research artifacts. C31 writes only
its new campaign directory. No old certificate/owner was edited, no Git
reset/checkout/commit was made, and no remote snapshot replaced local work.
All {len(dep['pins'])} inherited local pins and external directive pins
match. Exact paths and SHA256 values are in dependency_pins.json; C31 files
are separately covered by campaign_manifest.json. Hashes prove provenance,
not mathematical truth.

FR31_FROZEN_SOURCE_BOX was written before the new source construction.
FR31_SCOPE_STEERING records the user's subsequent explicit resolution:
PREFIX quantifies over reachable variations of the deeper A term under11;
FIX retains the ENTIRE saved A tree. This distinction is load-bearing.

Original source: A receives every KEEP/DELETE; full B every KEEP including
root repeats, and erased B its prescribed KEEP subsequence. DELETE is
A-only, never physical deletion. Bottom-up a=ceil(depth_A/2),
q=floor(depth_B/2), physical units(t,j,b), demands(t,k). Natural genuine
macros retain every intervening operation and actual H. The witness uses
exactly13 physical keys, seven odd genuine KEEP marks, full core13 and
all-SS marked-G/unmarked-P full transitions. The closed auxiliary process
is the literal erased execution, not a selected chart representative.

R1 original target/domain/closure; R2 actual operations, costs and physical
units; R3 immutable inherited proofs/owners/caps; R4 explicit PASS, FAILED,
conditional, refuted and OPEN distinctions are preserved. In particular no
closed CD6 theorem is applied to a dirty nonclosed six-target suffix.
''')

doc('C30_INHERITANCE_LEDGER.md','''# Dependency status, exact interfaces and proof inspection

Paths below are relative to DO_RESEARCH_REBOOT. dependency_pins.json gives
every exact hash. Directly read proofs are distinguished from unchanged
older interface inheritance. No accepted source replay was repeated.

|Dependency|Inspection/use and retained status|
|---|---|
|C30 CHECKPOINT, FINAL_VERDICT, NH30_FROZEN_SOURCE_BOX|Inspected; authoritative NH30-FR3 target, principal NH30 OPEN|
|C30 CRITICAL_PREDECESSOR_AND_FORWARD_RETURN|Inspected; N85 closed source, triple0,-1,0 and four-macro return0; restricted theorem|
|C30 nonextremal_source_countercertificate.json|Saved literal word/trees/events reused; old source receipt accepted, not rerun|
|C30 LOW_SIDE_SOURCE_BARRIER and FIRST_RETURN_SOURCE_BARRIER|Inspected; low bound-1, first upper11/13; immediate7 loses core6|
|C30 returning U and W0/W1/U reset/chart proofs and receipts|Inherited at exact stated returning-word scope, not all first returns|
|C30 NORMALIZED_SHALLOW_OWNER_INTERFACE|Inspected; actual supplied a, licensed eligibility/retirement/transport, B_a<=9 imply bound24|
|C30 NEGATIVE_HELPER_BALANCE_SOURCE_CONTROL / NEGATIVE_BALANCE_STRESS_TEST|Inspected; genuine negative helper debit and helper-only-4m remain valid|
|C29 BRANCH_COUNT_POTENTIAL_AND_DEBT_TRANSFER|Inspected; exact intrinsic E identity, global per-edge E law REFUTED|
|C29 EXTREMAL_COMB_REPAYMENT and HELPER_DEBT_AND_SIGNED_BALANCE|Inspected; opposite-extreme guard only; W0 triple4 includes helper-1|
|C29 mixed W0/W1 and C28 W459/V-family, C27 W199|Inherited exact funding scopes/receipts; no owner reopening or new audit|
|C23-C26 owner/flip/exterior interfaces|Inherited original source, successful owner and eligibility conditions; no universal promotion|
|C24 SS_SOURCE_INVERSE_LEMMA|Inspected complete induction; original AUDIT-PENDING status retained; C31 writes the source proof again with exact q<=3 arithmetic|
|C14 CLOSED_PERIOD_CORE_CONSTANCY and UNIFORM_R_TRANSFER|Inspected actual core/source reduction and every E_r premise; conditional transfer only|
|Original Step1 source_allocation/source bridge and restricted M3 decoder|Inspected source/normalization limits; no dirty-segment lifting assumed and no new M3 semantic call|
|C30 resources_checkpoint and executed controller|Inspected, inherited cumulative240/600/7200/2M caps unchanged|

Accepted CD6 is not reopened: no concrete invalid dependency was found.
Manuscript proofs are not relabeled externally certified by this ledger.
''')

doc('FR31_DEPENDENCY_GRAPH.md','''# IAGS dependency graph and exact decision

Freeze: original NH30-FR3 Box, then explicit PREFIX/FIX user resolution.
Inherit: original Pair Access -> fixed marked-core membership -> all-SS
path-to-star -> rho/E identity -> critical zero predecessor/weak helper.
Inherit: C30 low parity barrier -> upper11/13 and entry debt<=2.

Recurse: source low price P and theta -> FR31-EN entry theorem -> only
potentially unpaid FIRST-UPPER branch is no genuine low, upper11,H1.
The integer-cell arithmetic is independently scripted; the source induction
is a mathematical manuscript, not a finite sampling argument.

Alter sufficient route, not original theorem: vary only the allowed deeper
A term. New six A-only operations precede KEEP13 synchronization -> same
critical L/RL/LL frame -> legal KEEP11,9,5,7 continuation -> first-return
sigma-1. The intermediate5 is essential; direct7 after9 was not licensed.

Reconstruct source: literal prefix P45 -> original SS inverse40 -> genuine
KEEP1/3 support loop -> A-only reset14 -> W101 with A/BF return. Deterministic
erased F on13-key BSTs -> N W^C prefix / W^(C!) period -> exact paired
closure. A/BF local counter does not depend on the erased orbit point.

Close: FR31-PREFIX proposed local inequality is FALSE (Outcome E).
Preserve separately: FR31-FIX universal law OPEN; entry theorem and full
counterfamily independent funding are positive restricted derivations.
Do NOT reconstruct a universal normalized owner or Gate U theorem from
these children. The absent all-source carry/eligibility bridge is explicit.
''')

doc('LOW_SIDE_BARRIER_AND_ENTRY_STATE.md','''# Gate A — inherited low barrier, refined entry classification

The interval L consists of every genuine lower macro after comb and before
the first upper KEEP. Its B targets lie in{1,3,5}, Q<=2, actual H>=1.
All intermediate A-only/root KEEP operations remain in those macro costs
or the following upper macro. In the exact post-comb B frame, the right
subtree stays attached to5, whose lower SS motion changes its physical
depth by an even number. Hence paths to7/9 remain odd, and the first upper
must11/13. An actual closed seven-key source supplies such an upper event.

Let P_low=sum(2min(H,3)-Q)>=0 and theta=degree_marked(5)-2 in{0,1,2}.
Only5 can have marked degree>2 during the low phase. E starts1, ends theta.
Thus Sigma_low=P_low+theta-1>=-1, and the helper/comb/low sum is exactly
P_low+theta-2. Positive entry debt is max(0,2-theta-P_low), at most2.
Keeping the untruncated sum is essential when it is positive.

Equality in the low bound requires theta0,P_low0: the lower grammar then
requires one H1 KEEP1 and no other genuine lower transition. This is an
equality CLASSIFICATION; a new jointly reachable arbitrary-A equality
witness has not been constructed. Sharpness on every PREFIX/FIX parameter
is not claimed.

ENTRY_COMPENSATION_REDUCTION proves the actual one-event A bound and
separate upper laws, including arbitrary permitted DELETEs. Its consequence
is stronger than entry<=2: every branch except low-empty/upper11/H1 pays
the whole original pre-upper balance at the FIRST upper. Later return
transitions still need their own sign theorem. The counter has empty L,
theta1,P_low0 and D_entry1, exactly the remaining branch.
''')

doc('FIRST_UPPER_11_13_SOURCE_NORMAL_FORMS.md','''# Gate B — exhaustive entry laws; later upper paths not all classified

At the inherited post-comb frame and every valid low continuation, let
r=depth_B(5)/2 in{0,1,2}, theta=E_before_upper in{0,1,2}, c=min(H_upper,3).
The first-upper branches have DIFFERENT actual target degrees and costs:

|First upper|B doubles|Old target marked degree|k3|Exact sigma_E|
|---|---|---|---|---|
|11|r+1|1|1[theta>0]|2c-1-1[theta>0]|
|13|r+2|0|1[theta>0]|2c-2-1[theta>0]|

In both branches E_after=theta+r-1[theta>0]; topology is not thereby equal.
No representative erasure chart or hypothetical owner state is selected.

When P_low<=1, all genuine low macros have H1, so only their lower terminal
keys can have positive A accesses. The fixed right A chain survives at5.
Consequently upper13 has H>=2, and upper11 also has H>=2 when theta0.
With theta1,P_low0 there were no genuine low transitions. Only its H1
upper11 can leave debt1 unpaid at entry. See the full source argument in
ENTRY_COMPENSATION_REDUCTION and arithmetic receipt for the unbounded
P_low tail, not a bounded-population source experiment.

For the counter B11, saved new rows give every actual A/BF/BE endpoint.
BE at the closed-period copy is the exact F-orbit execution, not the short
prefix's numerical BE columns. No normalized owner bank is invented. B13's
entry compensation is symbolic and uniform under the stated frame; a
complete classification of ALL B13 upper-to-first7 paths remains OPEN.
''')

doc('FIRST_RETURN_7_SOURCE_CLASSIFICATION.md','''# Gate C — decisive legal counterclass and remaining coverage

Return means FIRST genuine full KEEP7 after the helper, NOT full-state
restoration. Marked support and closure ensure it exists. In the new source
the actual sequence from helper through return is11,5,11,9,5,7; there is
no earlier KEEP7. First upper is the third macro11; low phase is empty.
The final B path is RRLL, all13 core labels remain, and every full double
is original LL/RR marked-G/unmarked-P. Root7 is restored but E is0 instead
of its pre-helper1. The subsequent11 pays the carried unit.

|Source return class|Status|
|---|---|
|C30 direct7 immediately after comb|Invalid; RLR loses unmarked core label6|
|Failed C31 direct7 after upper11/9|Not accepted; initial source phase FAILED before revised bridge|
|C30 saved11 then7|Valid four-macro packet, total0, accepted FIX control|
|PREFIX11 then9 then5 then7|NEW valid source class, total-1, principal counterexample|
|FIX11 then9 then5 then7 without extra A-only changes|9 costs2, restricted route nonnegative; not a universal FIX proof|
|B13 arbitrary upper/return, arbitrarily long switches/root-repeat helpers|Not exhaustively classified; unnecessary for disproving a universal law|

The last row is OPEN, not excluded and not proved nonnegative by failure of
another candidate. Original DELETEs, private A populations and nonidentity
returns cannot be removed from future classifications. The counter has a
proved exact paired-closed embedding in CLOSED_COUNTEREXAMPLE_PROOF.
''')

ledgerhead='|short-prefix t|key|H|QF|QE(short prefix)|beta|z|rho|E before->after|sigma_E|A path|B path|\n|---|---|---|---|---|---|---|---|---|---|---|---|'
ledgertable='\n'.join([ledgerhead]+[f"|{z['occurrence']}|{z['target']}|{z['H']}|{z['QF']}|{z['QE']}|{z['beta']}|{z['z']}|{z['rho']}|{z['E_before']}->{z['E_after']}|{z['sigma_E']}|{z['A_path']}|{z['BF_path']}|" for z in c['ledger']])
doc('FIRST_RETURN_SIGNED_LEDGER.md',f'''# Gate D — complete actual first-return ledger

The original formulas are rho=2min(H,3)-beta-z and
sigma_E=2min(H,3)-QF+Delta E=rho+Delta(3-b), where b is actual marked
branch count. E counts nearest-marked-ancestor excess, not physical BST
binary children. No old chart-switching normalization is revived.

{ledgertable}

The six macros124..129 have sum H6, QF12 and price0; E1->0 gives sigma-1.
Helper124 owes1, comb125 preserves it, and every upper/bridge/return term
is0. Thus R_return0<D_entry1. No hidden return boundary resets E.
Next11 at130 has+1 and restores this particular accumulated signed balance.
The rho and branch-correction columns are retained through every boundary;
rho alone is not silently substituted for sigma.

QE above belongs ONLY to the replayed short reaching prefix. In the actual
erased-aligned closed period its exact states/costs are defined by the
original F_E orbit, not those numerical columns. FR31's intrinsic full-B
inequality uses A,QF,E and is unchanged by that orbit alignment. No unknown
auxiliary normalized owner, physical spare freedom or chart correction is
inferred from the short QE data.
''')

doc('SOURCE_FORCED_FIRST_RETURN_REPAYMENT.md','''# Gate E — source-forced local repayment is refuted

At the principal PREFIX scope the target is FALSE. D_entry1 is not repaid
by the first root7 return: R_return0, total helper-through-return-1.
The exact source is reachable and has a constructive closed embedding.
The obstruction is permitted deeper A geometry exposing marked9 at depth2
after first-upper11. It makes a Q3 full-B access H1 and sigma0. A legal
bridge5 then permits KEEP7 without repaying the signed debt.

On the saved FIX tree the same9 is depth4, H2, contributing+2 instead of0.
Both engines checked that isolated cost. This supplies the exact extra
geometric fact for that route; it is not an unproved generic invisibility
guard or a universal FIX theorem.

The interval already has12 physical units for12 B demands. A raw independent
injection uses actual q1 spares11/5. This does not free those bits under a
frozen normalized a. The failed conclusion concerns the LOCAL SIGNED law,
not existence of a full matching. Earlier actual preparation might prepay,
or a new state correction might carry the unit; neither is excluded by
this counterexample. On the same horizon any replacement correction J
must have J(return)-J(before helper)>=1 here. That necessary condition is
not a globally verified potential formula.

FR31-EN gives a new universal ENTRY reduction and FR31-CL funds this full
counterfamily with a longer actual packet. They are explicitly smaller
results and do not turn the false parent law into a theorem.
''')

doc('RETURNING_BLOCK_UNIVERSALITY_TEST.md','''# Gate F — restricted returning words are not exhaustive local packets

C30 U's real helper118,comb119,upper120,return121 has Q2,3,1,2 and H1 at
each; sigma-1,0,0,+1 sums0. The actual q1 bit(120,1,1) pays comb(119,3)
in the independent comparer. U is a rotated COMPLETE85-operation source,
not a four-operation synthetic closed block. Its repeated and mixed
W0/W1/U theorem keeps exact B/BE boundaries and the original A reset.

The new PREFIX path replaces the local successor word11,7 with11,9,5,7.
Its first-return balance is-1. It is consequently outside the inherited
list of already repaying local packets. No source-complete decomposition
into those packets can simply discard9,5 or reset at7. A grouping that
reaches beyond the first7 or uses earlier preparation is a genuinely
different sufficient route, requiring its own source/owner proof.

Historical U^m and W0/W1/U theorems/owners remain accepted at their stated
scope. No assertion that their literal whole words form a free-monoid
normal form for ALL closed sources is made or needed.
''')

doc('W85_FULL_RETURN_CONTROL.md','''# Gate G — preserved N85 full-return control and FIX distinction

The old C30 JSON retains literal reaching word N from common T, original
period I86..170, A109,QF66,QE42, full core13/erased core11. All old states,
source occurrences and receipts are unchanged and were not rerun. At
117,118,119 the triple0,-1,0 disproves the guard-free predecessor rule.
Its first upper120 is11 and first return121 is7. Their added0,+1 makes
the helper-through-return four-macro signed total0.

The new source reuses only old operations86..115, then adds REAL A-only
preparation before synchronizing KEEP13. The critical j/helper/comb remain
H1 with L/RL/LL paths. It is a reachable PREFIX variation, not a changed
interpretation of the old saved-tree FIX theorem. Full FIX stays OPEN.

FIX_9_activation_control and final_independent_proof_audit identify the
one accessed subtree difference: after the original upper11,9 has LRRL
path/H2; the new variation has LR/H1. The original saved first-return
control passes. No conclusion about every FIX continuation is inferred.
''')

doc('NEGATIVE_HELPER_BALANCE_RETURN_CONTROL.md','''# Gate H — actual negative helpers remain admitted

C29's weak W0 has helper160 H1/Q2/beta1/z1, E1->0, sigma-1, followed by
comb161 sigma0. The actual earlier j159 has H47, Q1, sigma5; the full
triple sums4. Its comb endpoints are opposite extreme marks, unlike the
NH30-C endpoints5/11. Thus this is a different source return class; no
NH30-C first-return7 classification is silently applied to W0.

W0's accepted34/34 full owner map and Bank5 remain literal. Its nominal
helper spare is locked by the comb; the saved late payment uses its actual
licensed preparation bit. This is evidence against treating comparison
spares as automatically owner-free, not evidence of unpaid historic debt.

C30 U^m also has genuine helper-only aggregate-4m while its COMPLETE signed
sum is60m and original2A-QF is152m. The negative contributions are paid by
nonhelper source contributions in the complete packet theorem. Neither
this campaign nor the entry reduction asserts helper-only nonnegativity.
The new first-return counter is another terminal comparison carry, not
a contradiction of these fully funded closed controls.
''')

doc('FIRST_RETURN_RESET_INTERFACE.md','''# Gate I — root return is not renewal

The counter gives a direct nonreset certificate. Just before helper, B
root7 has E1; at first return it has E0. A differs too, and the replayed
erased state/owner phase is not licensed to reset. All13 core labels
remain but constancy of labels does not imply constancy of topology.
Resetting the debt at7 would delete a real unit from the signed ledger.

For a future true renewal interface one must preserve full A/BF/BE or a
proved sufficient quotient, actual E/chart boundary, carried helper state,
frozen owners/bank, source phase and absolute occurrence identities.
C30's full returning-word seam has those specific source/chart properties;
a generic firstKEEP7 does not inherit them.

W101 has an A/BF reset by the original inverse/support/A-only reset, and
W^(C!) has the exact BE reset by the finite-orbit proof. That COMPLETE
closed-word reset is separate from its interior nonresetting root7. No
extra future access or future-depth event is forced by calling it a return.
''')

doc('COLLECTIVE_FIRST_RETURN_REPAYMENT.md','''# Gate J — local universal composition unavailable; exact repeated family

The universal nonnegative local law is already false for one interval,
so it cannot be composed as a theorem about every collection. Do not
assume disjoint return windows or erase shared negative helpers.

On the explicit W^(C!) history every W copy contains the same -1 local
interval and later+1 at its next11. Thus arbitrary permitted repetition
of this closed family retains a local negative interval per copy; it
does not generate a negative closed signed cycle. The full source has
separate disjoint seven-macro recovery packets and inverse/support packets.
COMPLETION_CREDIT_AND_OWNER_LICENSE gives their independent full funding.
Each donor uses its OWN original copy/event ID, never another symbolic
copy's unit. Distinct forward pairs and inverse words have disjoint
inventories. A generic mixture with old returning words is not proved.

For actual frozen normalized owners the licensed path extension requires
the old eligibility/retirement/transport and actual profile bound. It is
not obtained by individually choosing potentially colliding raw spares.
Global all-source collections remain OPEN, as do overlap classes beyond
this explicitly partitioned family.
''')

doc('FIRST_RETURN_NORMALIZED_OWNER_INTERFACE.md','''# Gate K — exact conditional normalized-owner interface

No historic owner is moved. A separate comparer H is not extra physical
spending beside an actual normalized map a. For THIS full counterfamily,
FR31-CL gives total H extending all natural h0, aligned endpoint profile3
and all-legal-cut profile6. New q1 spare choices are explicit original bits.

For an ACTUAL supplied effective injection a:D0->U on the SAME period,
retain every prescribed full common/successful value and original extra
reservation. Assume the original block eligibility, E-only retirement,
transport/cut licenses apply. From an unpaid root follow H, then the
literal inverse-a owner at occupied bits. Injectivity prevents cycles or
collisions from unpaid roots; finite paths terminate at distinct eligible
free endpoints. Append root-to-endpoint values only. Every a value remains.

Cutwise B_extended<=B_H+2B_a. With B_H<=6 and an ACTUAL B_a<=9 receipt,
the effective bound is24. Bank25 does not imply B_a<=9, and neither the
raw H nor a short erased replay supplies that normalized receipt. The
huge closed completion has no newly evaluated full f5/f6 map. The theorem
is conditional, not an assertion that all arbitrary normalized maps satisfy
these hypotheses. A-only preparation bit(118,2,1) is likewise only a raw
candidate until its real normalized eligibility/ownership is justified.
''')

doc('FIRST_RETURN_BANK25_COMPATIBILITY.md','''# Gate L — actual working bounds and limits

C30's old W0/W1/U raw17 and conditional normalized24 are unchanged and
are not copied onto a new word without proof. On the NEW W101 family,
FR31-CL groups helper through next11 (not first7), each original inverse
word, and all other source macros. The selected inverse budget c*<=H
includes all natural owner units, max packet16 units, E width<=4. The
resulting raw working bound is20<25. Original c=min(H,3)>=c*, so every
old sigma is explicitly at least the selected signed inequality.

The explicit independent H profile is3 aligned and6 at any legally supplied
cut. A licensed actual normalized map with profile<=9 extends within24.
This bound is separate from the raw working20; they are not added or
confused. No all-normalized profile<=9 proof exists here. New first-return
signed law failure cannot be repaired by silently resetting a bank at7.

No cap is changed. The proof does not propose a larger physical bank,
an unbounded hidden helper bank, or reserve bits from another cyclic copy.
All-r r-4 carry/storage obstructions from Gate U remain in force.
''')

doc('FIRST_RETURN_ARITY_SCOPE.md','''# Gate M — support, arity and private-tree scope

The decisive counterexample has exactly seven genuine KEEP marks on13
physical keys, maximal full marked core13 and original all-SS transitions.
Its helper has one degree3 marked ancestor. It refutes the universal
PREFIX law already in this smallest declared instance; an arbitrary-fringe
counterfamily is unnecessary. It does not refute the complete saved FIX
case, alpha4/5, two-ternary helpers or arbitrary-r funding theorems.

The entry theorem uses the exact NH30-C post-comb anchor frame and the
prescribed A shallow frame with permitted ordered private terms; source
one-event geometry retains arbitrary DELETEs and anonymous ancestors.
It is NOT an all-core13-topology classification. Reflection transports
that structural argument by order reversal/left-right exchange.

The explicit closed W101 completion is on the EMPTY-gap13-key witness.
Do not infer an exact A reset on arbitrary added private populations from
its finite13-key construction. The SS inverse itself restores arbitrary
ordered private terms; independent H's cost/owner formulas apply whenever
their actual source realization is supplied. Such conditional lifting is
distinct from a new arbitrary-population closed-source realization theorem.
No seven-key theorem is promoted to all support or constant all-r width.
''')

doc('RETURN_CHARTS_AND_ABSOLUTE_PERIOD.md','''# Gate N — signed charts and one actual period

Intrinsic E=sum(degree-2)_+ on actual full-B marked trees is used throughout
the counter. The relation sigma_E=rho+Delta(3-b) includes every branch
boundary. It is not the refuted changing nine-Score chart normalization.
First7 does not close E; pre-helper1 and return0 give the missing-1.
C30's W/U hybrid chart equality3 is inherited only on its original seams.

Let C=742900, F the exact KEEP11-erased transformation of literal W101.
Reach from the actual common diagonal by N W^C; take ONE source period
W^(C!). Its initial erased tree is exactly F^C(E0), and every within-copy
state is the original filtered-prefix transformation of the corresponding
F-orbit point. A/BF repeat every W; erased B closes by period divisibility.
This is a compact exact mathematical description, not a claimed execution
of C! blocks or a numerical auxiliary-state receipt.

At first period-copy base o=85+101C, helper=o+39, first upper=o+41,
return=o+44, next11=o+45. Donors carry absolute(t,j,b) IDs. Different W
copies are actual distinct source operations. No unit is borrowed from
another formal cyclic copy. A legal cut preserves the actual occurrence
bijection; it can split at most one short counterinterval and cannot remove
all interior ones. No particular maximum-debt cut or normalized fE receipt
is manufactured by that observation. Their original license stays necessary.
''')

controls=[
('A1 N85 triple','Preserved accepted source; its first return DOES repay; no replay'),
('A2 immediate7/core loss','Preserved INVALID control, never a source counterexample'),
('A3 four-macro recovery','Retained at exact N/U scope'),
('A4 W0/W1/U mixtures','Inherited restricted source/owner theorem, not all-return exhaustion'),
('A5 helper-1 source','Retained actual debit; j supplies real earlier compensation'),
('A6/A7 W459 false partition/hybrid','Old refutation and successful restricted repair unchanged'),
('A8 W199','Historic58/58 owners/Pempty unchanged'),
('A9 B11','New reachable PREFIX negative first return'),
('A10 B13','Uniform PRE-UPPER entry compensation only; full return OPEN'),
('A11 long upper phase','No finite length exclusion or universal proof claimed'),
('A12 repeated upper accesses','Actual11,9,5,7 countercontinuation retains all macros'),
('A13 signed chart','All rho/Delta(3-b) boundaries included; E not reset at7'),
('A14 nonidentity A','Actual saved A endpoints differ at7; not declared a reset'),
('A15 carried helper','Exactly1 remains at7; next actual11 repays this example'),
('A16/A17 locked/raw owners','Local H spares not declared free under normalized a'),
('A18 profile9','Conditional explicit hypothesis, not inferred from Bank25'),
('A19 false reset','Refuted by E1->0 and full tree endpoints'),
('A20 overlap','Only full counterfamily disjoint packets proved; generic collections OPEN'),
('A21 paired closure','Explicit SS inverse/support/reset plus finite erased orbit; symbolic, not replayed'),
('A22 cyclic cut','Actual absolute period; no borrowing; supplied cut still needs receipt'),
('A23/A24 bounded samples','No finite passing test promoted; thirteen-node counter sufficient to refute PREFIX'),
('A25 CD distinction','W has Q82, A>=58, margin>=34; not a CD counterexample')]
controltable='\n'.join(['|Control|Result/status|','|---|---|']+[f'|{x}|{y}|' for x,y in controls])
doc('FR31_ADVERSARIAL_SOURCE_CERTIFICATES.md',f'''# Adversarial source controls and retained failures

{controltable}

Failed source27-query phase is preserved as FAILED: it did not establish
the revised legal return. Failed independent30-query phase DID save the
complete valid local15-operation trajectory before a wrong completion-size
assertion failed. It remains FAILED, not relabeled PASS. Later tuple suffix
8-query and static proof phases explicitly establish the corrected claims.

The preliminary W99 completion lacked genuine KEEP1. Source-domain audit
found and repaired that gap using the original literal KEEP1,KEEP3 support
loop. Authoritative W is101, not99/97; see the v2 descriptor and
CERTIFICATE_INTERPRETATION. No failed or superseded artifact was overwritten.
''')

doc('CERTIFICATE_INTERPRETATION.md','''# Authoritative data and superseded metadata

Use FR31_RESULT_CERTIFICATE together with
prefix_first_return_countercertificate_v2.json and CLOSED_COUNTEREXAMPLE_PROOF.
The literal W101 has all seven genuine KEEP keys. Its symbolic closed period
is W^(742900!), preceded by the exact reaching N W^742900.

The earlier unversioned countercertificate contains the VALID local replay
but an INCOMPLETE W99 source-support completion; its completion is superseded.
The v2 descriptor copied that local data and explicitly replaced the closed
word, support, counts, resource-independent closure and period identities.
Its inherited free-text verification_scope still mentions an obsolete97-word
label. That string is historical, NOT an executed word-length fact. The
correct full block is101 and it was NOT newly executed. The new result
certificate and this interpretation supersede that stale prose without
overwriting a hashed source artifact or receipt.

Two different BE data scopes must not be mixed: saved numeric new_rows
replay the SHORT prefix; periodized BE is the EXACT symbolic F^C(E0) orbit.
Local A/BF/marked E values repeat independently of that BE choice. No full
numerical BE tree, QE sum, normalized a or giant-period replay is claimed.
All closure beyond the short trace uses written mathematical source proofs.
''')

doc('FR31_ARCHITECTURE_VERDICT.md','''# Outcome E — precise architecture decision

REFUTED: at principal FR31-PREFIX scope every helper-through-firstKEEP7
interval has nonnegative original sigma_E. A legal reachable counter has
entry debt1, return contribution0, terminal carried debt1. Deeper A geometry
does affect the law, exactly as the user required us to investigate.

NOT REFUTED: FR31-FIX universally (still OPEN), any physical repayment
using earlier preparation, any longer source-derived carry mechanism,
full-source normalized exchange, CD6, Coarse-Double or Dynamic Optimality.
The counterfamily has an explicit complete independent comparison and
positive original closed-period margin.

Established smaller results: FR31-EN narrows initial unpaid entry to
low-empty/upper11/H1; FR31-CL gives a complete longer-packet source-credit
license for W101 family. A new correction preserving the same short horizon
must rise by at least1 across this example. No universal replacement is
proved by that necessary constraint. Do not patch the potential with a
single local exception and claim all changing source charts are solved.

Outcome E is a decisive mathematical result for the frozen local target,
not a claim that the current attempt or CPU limit forced abandonment.
''')

doc('GATE_U_SOURCE_DEPENDENCY_STATUS.md','''# Gate U remains conditional — exact clauses

Original C14 I(r) is witness-rich local source credit, not the scalar CD(r)
inequality or an assumed desired global matching. License A uses specified
distinct physical seeds; license B uses a source-proved packet inequality
with actual selected bits including every natural h0 owner, legal seam and
Bank25-compatible working bound. I(6)/CD6 stays accepted.

|Required E_r clause|Status after C31|
|---|---|
|1 Same-A erased reachability/normalization, exact recurrence/cut, fixed fE domain|Basic transfer and counterfamily symbolic paired recurrence established; no actual all-domain fixed fE selector/cut or new normalized receipt fabricated|
|2 Independently source-derived COMPLETE full license A/B|New W101-family license proved in manuscript; universal first-return PREFIX shortcut REFUTED; other arities/cores/all-r supply OPEN|
|3 Common ordinal pairing, E-only retirement, eligibility, max-cut transport, Bank25, old owners|Original transfer interface unchanged; licensed actual-profile<=9 theorem conditional; universal eligibility/profiles/transport OPEN|

Thus I(r-1)+E_r=>I(r) remains the accepted sufficient transfer. C31 discharges
no whole arbitrary-r clause. Strong I(5) on every auxiliary scope is not
deduced from scalar CD5. Existing r-4 width/carry and Bank25 obstruction to
unchanged packet extrapolation remain. U-OPEN: REQUIRED SOURCE SUPPLY STILL
OPEN, with explicit newly refuted first-root-return route. No Universal CD
or Dynamic Optimality conclusion follows.
''')

doc('C32_NORMALIZED_OWNER_HANDOFF.md','''# Next bounded Box — terminal carry rather than false reset

Do not start normalized-owner promotion from the false PREFIX law. Keep
FIX separate and preserve the accepted old source/owners. The smallest
entry class still requiring a new mechanism is low-empty/first-upper11/H1.
Marked9 visibility is an actual obstruction, not a chart artifact.

Box FR32-CARRY1

Target: prove or refute, in the SAME exceptional PREFIX source class, the
weaker EXACT bound sum_{helper..firstKEEP7} sigma_E>=-1. Retain the terminal
debt rather than declaring it repaid. The known source attains-1.
Conditions: all original reachable closed seven-key/core13/all-SS histories,
prescribed shallow A/B frames, arbitrary permitted deeper A/DELETEs,
full signed/chart identities and legal actual-period correspondence.
Inheritance: low/upper entry reduction; actual -1 closed counter and +1
later11 in that example; E width4; original source degree and core laws.
Ambiguities: further zero/negative helper interactions, repeated upper
switches, terminal visible state, dirty open six-target boundary. No
assumption that another11 or a deep future access is forced.
Bridge: a proof would bound the carried unit at a real return; it would
NOT yet fund repeated carry or establish a global potential. A source
counter below-1 would decisively show even this carry width insufficient.

Only after a true carry/supply invariant is found should owner promotion
quantify over actual normalized maps. For the specific W101 family only,
the complete H plus actual profile<=9 and original source license already
gives bound24. Do not universalize those profile/eligibility assumptions.
''')

phaserows='\n'.join(['|Phase|Group|Status|Queries|Child+controller CPU|','|---|---|---|---|---|']+[f"|{z['phase']}|{z['group']}|{z['status']}|{z['source_queries']}|{z['total_charge']}|" for z in phases])
doc('INDEPENDENT_AUDIT_STATUS.md',f'''# Verification performed, omitted and pending

{phaserows}

The mutable local replay covered the six prep DELETEs and nine KEEPs,
actual A/BF/BE operations, marked core and SS events. The original tuple
engine checked the corrected KEEP5,KEEP7,KEEP11 suffix independently.
FIX9's isolated A access was checked by both implementations. All NEW
source calls cost67 queries including failures; static saved-row/arithmetic
checks cost0 but their CPU is charged. Versioned phases share the inherited
caps, not fresh allowances.

PASS does NOT mean the giant closed source was replayed. The full W101
and erased recurrence use the written all-SS inverse/reset/finite-orbit
proof; scripts check saved facts and arithmetic. The full source-induction
arguments, raw20/profile proof, and conditional normalized interface remain
mathematical manuscripts without external/formal certification. C24 inverse
audit-pending status is not retrospectively sealed by this publication.

Pending external/proof audit checklist: root-first inverse induction with
all source terms; ordered A reset and genuine seven-key support loop;
finite F orbit and exact original reaching/period descriptors; BE-scope
distinction and legal cut correspondence; entry A one-event induction and
lower grammar; complete H/profile/storage arguments and actual normalized
eligibility/retirement/transport for any supplied map. No actual normalized
full-period receipt is claimed. No accepted old audit is needlessly repeated.

The earlier arithmetic receipt pins an earlier closure manuscript. A
subsequent clarification explicitly separated short-replay BE from the
periodized BE orbit. The first publication correctly rejected that changed
hash before emitting reports. publication_attempt1_exit and the original
publisher are preserved. revision_bridge_audit pins the EXACT revised
manuscript, checks the unchanged source descriptor, and establishes that
ONLY the A subtree below11 differs from the saved FIX frame. It has zero
tree operations and is not described as an external mathematical audit.
''')

gates=[
('A low barrier','INHERITED + REFINED','bound-1, entry<=2, exact entry reduction; sharpness realization not newly proved'),
('B first upper','ENTRY CLASSIFICATION DERIVED','separate11/13 formulas; no complete later upper-path classification'),
('C first return','COUNTERCLASS ESTABLISHED','legal PREFIX11,9,5,7; all-return inventory unnecessary for refutation'),
('D signed ledger','EXACT LOCAL COUNTER','R0,D1,total-1; all E/rho boundaries retained'),
('E source repayment','REFUTED AT PREFIX SCOPE','FIX remains OPEN; longer/prepaid funding not refuted'),
('F U interface','RESTRICTED THEOREM PRESERVED','old word scope does not exhaust first-return packets'),
('G N85','PRESERVED','old first return total0; no replay'),
('H negative helpers','PRESERVED','W0 helper-1, U helper-only-4m not discarded'),
('I reset','ROOT-RESET CLAIM FALSE','E1->0; complete-word reset separately proved'),
('J collections','RESTRICTED FULL FAMILY','disjoint W101 completion packets; generic collections OPEN'),
('K owners','CONDITIONAL','actual a + original license + profile9, no fabricated receipt'),
('L Bank25','RESTRICTED/CONDITIONAL','new raw20; H3/6; licensed profile9 gives24'),
('M arity/support','EXACT SCOPE','seven/core13/degree3; alpha4/5,two-ternary,all-r OPEN'),
('N charts/period','SYMBOLIC CLOSED EMBEDDING','W101 inverse/reset, BE finite orbit, no giant-period execution'),
('O complete FR law','OUTCOME E','principal PREFIX statement false; no positive FULL_PROOF file')]
gatetable='\n'.join(['|Gate|Outcome|Scope|','|---|---|---|']+[f'|{x}|{y}|{z}|' for x,y,z in gates])
doc('FINAL_VERDICT.md',f'''# OUTCOME E — FR31-PREFIX first-return signed rule refuted

The principal source-uniform first-root7 repayment law is FALSE under the
user's explicit PREFIX scope. The original shallow L/RL/LL frame and
critical H1/Q2 zero predecessor are preserved. A reachable deeper A
variation permits actual helper/comb/upper/activation/bridge/return targets
11,5,11,9,5,7, all H1 and Q2,3,1,3,1,2. Their sigma_E values are
-1,0,0,0,0,0. D_entry1,R_return0. First7 retains one debt unit.
The next actual11 contributes+1 on this example. The saved-tree FIX case
remains OPEN; the isolated deeper cost is9 at H2 in FIX versus H1 in PREFIX.

This is a genuine original-source construction: local replay plus literal
W101 A/BF return, genuine seven-key support, and finite-orbit erased closure
give reaching N W^742900 and period W^(742900!). The full completion and
huge period are proved SYMBOLICALLY, not replayed. Saved numeric BE columns
belong to the short prefix; closed-period BE uses its exact F-orbit state.
No full-period normalized owner or auxiliary cost receipt is fabricated.

It is NOT a Coarse-Double counterexample. W has Q82 and A>=58, hence
2A-Q>=34. Even the negative signed interval has12 actual units and12
demands with a total independent comparison. Failure is terminal signed
carry/false root-reset, not physical original-cost shortage.

New smaller derivations: FR31-EN reduces unpaid FIRST-UPPER entry to exactly
low-empty/upper11/H1; FR31-CL gives this counterfamily a complete longer
source packet license, raw20, H profile3/all-cut6, and licensed actual
normalized profile<=9 extension within24. None proves all-source owners.

{gatetable}

Source provenance: branch `{e['branch']}`, HEAD `{e['head']}`; tracked
tree clean, preexisting untracked research preserved; {len(dep['pins'])}
inherited local hashes match. Cumulative CPU{total}/7200, symbolic
{groups['symbolic']}/240, independent{groups['independent']}/600.
Queries{qtotal}/2000000, remaining{2000000-qtotal}; no reset or cap increase.

Unresolved: universal FIX, complete later B13 returns, modified carry law
and repeated/shared repayment, actual normalized eligibility/profile/cuts,
other arities and arbitrary support. Next bounded Box is FR32-CARRY1 in
C32_NORMALIZED_OWNER_HANDOFF. Gate U, Universal CD and Dynamic Optimality
remain OPEN. No positive FR31 theorem or FULL_PROOF is emitted.
''')

doc('CHECKPOINT.md',f'''# C31 continuation — decisive PREFIX refutation, FIX separate

Read FINAL_VERDICT, CLOSED_COUNTEREXAMPLE_PROOF, CERTIFICATE_INTERPRETATION,
ENTRY_COMPENSATION_REDUCTION and COMPLETION_CREDIT_AND_OWNER_LICENSE first.
FR31_SCOPE_STEERING records the authoritative user distinction. Do not
rerun old controls or the accepted local trace. Keep all failed/superseded
artifacts. Use v2's literal W101 and new result certificate; v1 W99 lacks
genuine KEEP1 and its inherited97 prose is obsolete, not a replay claim.

New local actual helper124..return129 has H1 each,Q2,3,1,3,1,2, sigma-1
total, empty low, first upper126=11, genuine return129=7. BridgeKEEP5 at128
is necessary; failed direct return is not accepted. Next11 at130 pays+1.
The full closed completion has P45,inverse40,support2,reset14. Q82,A>=58,
genuine KEEP support all seven. Paired closed source is N W^C then W^(C!),
C742900, symbolic proof only; BE actual orbit differs from short replay.

FR31-PREFIX local law is REFUTED (Outcome E). FR31-FIX universal status
OPEN; saved FIX9 costs2, new PREFIX9 costs1. Entry theorem narrows first
unpaid branch to low-empty/upper11/H1; all-firstupper13 prefix debt paid,
but later return suffix remains separate. No old nine-Score normalization
or generic first7 reset is revived. Next precise Box FR32-CARRY1 asks
whether exceptional PREFIX helper..first7 sigma is at least-1, preserving
terminal carry and all source constraints. It is OPEN, not assumed.

Restricted completion license: raw working20; independent H profile3/6;
actual licensed normalized a profile<=9 gives24. No universal normalized
profile or actual full f5/f6 receipt is provided. Old fE/f6/a and historical
successful assignments stay literal. Gate U E_r2/E_r3 and all-r OPEN.

Branch `{e['branch']}`, HEAD `{e['head']}`. Cumulative CPU{total}/7200,
symbolic{groups['symbolic']}/240, audit{groups['independent']}/600;
queries{qtotal}/2000000 leave{2000000-qtotal}. Controller/source per-phase
caps and reserves, Bank25, live2M,DAG4M,edges5M,32GiB,12h unchanged.
Failed and successful child+controller CPU all charged. No new allowance
was inferred. External/formal proof audit remains pending; no new theorem
is called SEALED. Completion of the false principal law is logically
impossible at PREFIX scope, not an exhausted-attempt stopping reason.
''')

resources={'status':'CUMULATIVE_NO_RESET','prior_uniform_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'global_cap':7200,
 'global_remaining':7200-total,'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
 'group_remaining':{k:e['group_caps'][k]-groups[k] for k in groups},'phases':phases,
 'new_C31_source_queries':queries,'conservative_all_queries':qtotal,'query_limit':2000000,'conservative_remaining_queries':2000000-qtotal,
 'all_failed_successful_child_controller_charges_retained':True,'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,
 'memory_limit_bytes':32*1024**3,'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,
 'resource_authorization':'Inherit explicit240/600 and7200 caps; query cap2M cumulative; no extension or reset.',
 'metadata_CPU_excluded_under_inherited_convention':{'entry_checkpoint':e['metadata_CPU_excluded'],
 'publication_attempt1':'failed provenance assertion before report emission; metadata-only CPU not captured',
 'publication_before_manifest':time.process_time()},
 'outcome':'E: principal PREFIX local first-return signed law refuted','FR31_FIX':'OPEN','Gate_U':'OPEN'}
out('resources_checkpoint.json',resources)
out('FR31_RESULT_CERTIFICATE.json',{'outcome':'E','principal_scope':'FR31-PREFIX per explicit user clarification',
 'statement_refuted':'every admitted helper-through-firstKEEP7 interval has sum sigma_E>=0',
 'entry_debt':1,'upper_return_contribution':0,'sigma_through_first_return':-1,'sigma_through_next11':0,
 'local_data':'prefix_candidate_rows.json','authoritative_literal_completion':'prefix_first_return_countercertificate_v2.json',
 'authoritative_literal_completion_sha256':sha(B/'prefix_first_return_countercertificate_v2.json'),
 'closed_block_length':101,'closed_block_genuine_KEEP_support':[1,3,5,7,9,11,13],
 'closed_block_Q':82,'closed_block_A_lower_bound':58,'CD_margin_lower_bound':34,
 'closed_history_descriptor':c['symbolic_closed_history'],
 'closed_W_or_full_period_replayed':False,'closed_history_proof':'CLOSED_COUNTEREXAMPLE_PROOF.md',
 'saved_BE_numeric_scope':'short reaching prefix only; periodized erased process is the exact F_E orbit',
 'FR31_FIX':'OPEN; saved-tree scope not refuted','source_trace_implementations':'mutable local and tuple revised suffix; separate FIX access in both',
 'complete_normalized_map_evaluated':False,'normalized_owner_extension':'conditional actual a + original license + B_a<=9 => bound24',
 'smaller_mathematical_derivations':['uniform entry reduction FR31-EN','complete W101-family source license FR31-CL'],
 'external_or_formal_audit':False,'Gate_U':'OPEN','Coarse_Double_counterexample':False,
 'branch':e['branch'],'HEAD':e['head']})
assert not (B/'FULL_PROOF.md').exists() and not (B/'FIRST_RETURN_7_REPAYMENT_THEOREM.md').exists()
out('campaign_manifest.json',{'status':'APPEND_ONLY_C31_PUBLICATION','branch':e['branch'],'HEAD':e['head'],'tracked_tree_clean':True,
 'preexisting_untracked_research_preserved':True,'inherited_local_matches':len(dep['pins']),
 'files':[{'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f)} for f in sorted(B.iterdir()) if f.is_file() and f.name not in ('campaign_manifest.json','publication_exit.json','publication_seal.json')],
 'principal_positive_theorem_not_promoted':True,'no_historical_artifact_modified':True})
out('publication_exit.json',{'status':'PASS_METADATA_PUBLICATION','whole_process_CPU_seconds':time.process_time(),'semantic_calls':0})
out('publication_seal.json',{'status':'HASHED_PUBLICATION_NOT_A_THEOREM_SEAL','manifest_sha256':sha(B/'campaign_manifest.json'),
 'publication_exit_sha256':sha(B/'publication_exit.json')})
print(json.dumps({'status':'C31_PUBLISHED','outcome':'E','FR31_PREFIX':'LOCAL_FIRST_RETURN_LAW_REFUTED','FR31_FIX':'OPEN',
 'CPU':total,'groups':groups,'queries':qtotal,'queries_remaining':2000000-qtotal,'pins':len(dep['pins'])}),flush=True)
