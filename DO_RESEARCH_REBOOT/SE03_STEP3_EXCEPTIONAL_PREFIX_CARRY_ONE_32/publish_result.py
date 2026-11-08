"""Append-only C32 metadata publication. No source operation or proof test.
All actual symbolic/static arithmetic runs used the cumulative controller.
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
audit=read(B/'static_independent_audit.json');ran=read(B/'restricted_proof_arithmetic_audit.json');one=read(B/'transient13_independent_audit.json')
assert all(z['status'].startswith('PASS_') for z in (audit,ran,one))
for field,obj in [('input_manuscript_sha256',audit),('input_sha256',ran)]:
    for n,h in obj[field].items():assert sha(B/n)==h,n
assert one['input_sha256']==sha(B/'transient13_source_control.json')
total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[];queries=0
for p in sorted(B.glob('run_*_result.json')):
    z=read(p);control=read(B/('controller_'+z['phase']+'_exit.json'))
    z['controller_CPU']=control['whole_process_CPU_seconds'];z['total_charge']=z['child_CPU']+z['controller_CPU']
    total+=z['total_charge'];groups[z['group']]+=z['total_charge'];queries+=z['source_queries'];phases.append(z)
qtotal=e['inherited_conservative_queries']+queries
assert queries==3 and qtotal==2000000 and total<7195
assert all(groups[k]<e['group_caps'][k] for k in groups)
boundary=read(B/'six_key_boundary_analysis.json');rootbound=read(B/'old_chart_terminal_root_bound.json')
w=read(B/'transient_W105_certificate.json')
foot='''
Status convention: original reachable seven-key/core13/all-SS source unless
a proper subclass is stated. New source inductions are written mathematical
proofs; static complete-certificate arithmetic passed a separate same-agent
implementation. Only the targeted new13 A/BF access and one independent BF
check were executed. No full W105/factorial period or normalized owner map
was replayed. External/formal/source-kernel audit of the new inductions is
pending. Principal FR32-CARRY1, universal FR31-FIX, eventual repayment, Gate U,
Universal CD and Dynamic Optimality remain OPEN. All inherited owner, source,
audit-pending and resource restrictions are preserved; no new theorem is SEALED.
'''
def doc(n,s):write(n,s+'\n'+foot)

doc('SOURCE_INTEGRITY.md',f'''# C32 source provenance and cumulative execution gate

Branch `{e['branch']}`, HEAD `{e['head']}` verified at entry and publication.
Tracked files remain clean; preexisting untracked research is preserved.
Only this new C32 directory was written. No destructive Git, remote source
substitution, commit or historic certificate/owner edit occurred. All
{len(dep['pins'])} inherited local hashes and external directive pins match;
dependency_pins.json lists exact paths/hashes. campaign_manifest covers the
new files. Hash equality is provenance, not mathematical certification.

First artifacts freeze FIX/PREFIX/EXC and the original falsifiable Box.
A receives every original KEEP/DELETE; full B every KEEP including identity
repeats; erased B its exact subsequence. DELETE is A-only, never physical
deletion. H is the actual complete natural-macro A event count, Q actual
full B doubles, units(t,j,b), demands(t,k). Ordinary bottom-up semantics,
all original occurrences and legal period/cut conditions remain unchanged.

R1 preserves theorem/source scope; R2 actual operations, events and costs;
R3 frozen certificates/owners/caps; R4 explicit UNKNOWN/refuted/conditional/
proved/audit-pending distinctions. Bank25 is25. Entry CPU/caps and original
2M query ledger are inherited, never reset. New queries are exactly the
post-activation KEEP13 A and BF access plus one independent BF access.
Every subsequent check uses saved certificate data and structural/arithmetic
proofs, not a hidden original splay or new source-frame compilation.
''')

doc('C31_INHERITANCE_LEDGER.md','''# Exact inherited dependencies and status

All paths are relative to DO_RESEARCH_REBOOT; dependency_pins.json supplies
exact hashes for these and all transitive inherited artifacts. Earlier
accepted audits were reused, not rerun. Source proofs read in C31 remain
inherited at their exact scope; C32 re-read the new decisive interfaces.

|Dependency|Inspection and use|
|---|---|
|C31 CHECKPOINT/FINAL_VERDICT|Read; PREFIX zero-return law refuted, FIX separate OPEN, exact continuation/caps|
|C31 CLOSED_COUNTEREXAMPLE_PROOF and CERTIFICATE_INTERPRETATION|Read; literal W101 authoritative, W99/97 metadata superseded, symbolic BE orbit not replay|
|C31 prefix_candidate_rows and authoritative v2 word/states|Read/reused cached source, no old trajectory rerun|
|C31 ENTRY_COMPENSATION_REDUCTION|Read; exceptional low-empty/upper11/H1, entry1; other entries separate|
|C31 COMPLETION_CREDIT_AND_OWNER_LICENSE|Read; longer-family raw20/H3/6, actual licensed profile9 implies24 only|
|C31 FIX/PREFIX source steering|Read; deeper subtree variation not silently fixed|
|C30 N85, low/source barrier, four-macro recovery, U/mixed reset|Read in inherited reconstruction; accepted source/return scope preserved, no generic reset|
|C30 conditional normalized interface|Read; actual a, eligibility/retirement/transport and profile9 not assumed globally|
|C29 extremal/degree/helper proofs and negative fixture|Inspected inherited proofs; extremal guard retained, helper-only negativity admitted|
|C28 W459/hybrid, C27 W199, C23-C26 owner/flip interfaces|Unchanged accepted restricted receipts; no retrospective promotion|
|C14 UNIFORM_R_TRANSFER / CD6 FULL_PROOF|Read; three E_r clauses, source partition and conditional support transfer preserved|
|Unary14 FULL_PROOF and branch_funding|Read; complete974 A quotient, all LOW/HIGH signed tables, q5 pairing and actual D source definition|
|Unary14 branch_grammar2, branch_core11_mask0, independent receipts|Old accepted COMPLETE symbolic syntax reused; only new pointwise arithmetic analyzed, no old kernel audit repeated|
|Step1 SOURCE_BRIDGE/source_allocation|Read; sealed M3 debt is an input, closed chi8 cancellation cannot be silently extended to an open segment|
|C18 RR7/creator checkpoint|Read exact status: old RR7 protection refuted; HIGH threshold5 does not cover a new H2 pivot creator|

Accepted CD6 is not reopened. No invalid historical dependency was found.
New local uses of its table require the explicit fixed-core/source bridges,
not the scalar closed CD6 theorem. New adverse necessary tuples are not
declared reachable by splicing unrelated quotient states.
''')

doc('FR32_ENTRY_DEBT_CLASSIFICATION.md','''# Gate A — exact exceptional entry, broader cases separate

For general PREFIX low phase, P_low>=0 and theta in{0,1,2} give
helper/comb/low total P_low+theta-2 and positive debt at most2. FR31-EN
shows first-upper13 pays that original prefix debt; theta0/upper11 also
forces H>=2. Only no genuine low, upper11,H1 can leave1 unpaid at the
FIRST upper. This reduction is uniform in the allowed deeper A terms.

EXC is exactly that remaining branch, so D_entry=1, not an unproved choice
among0/1/2. It is source-realized by W101. A pre-upper debt2 realization
is not needed for C32 and was not newly constructed. An entry0 or2 history
is not silently added to EXC; its later evolution is a separate broader
PREFIX theorem. The first upper is11 by definition here, while later13
accesses are allowed and indeed create the new transient-two control.
''')

doc('EXCEPTIONAL_PREFIX_DEEP_GEOMETRY.md','''# Gate C — exact A frame, activation and pivot information

Before critical j the ordered shallow anchors are13(7(5(...),11(T9,...)),...).
The actual j/helper/comb paths L,RL,LL give costs1,1,1. After u11 the
A frame is11(7(5(...),T9),13(...)). A subsequent activation9 with H1
requires root(T9)=9; after it the actual A upper skeleton is9-11-13 with
the lower7/5 term attached to9. FIX has its entire saved deeper term and
the immediate9 costs2; PREFIX permits the reachable H1 variation.

The new post9 KEEP13 has H1 while full B Q2,E1->0, so it creates a
SECOND intermediate debt. In that state B-return7 is not permitted: the
fixed lower path from9 is LRL with odd depth. UPPER_ONLY_BARRIER proves
this for every finite H1 upper word, not just the new witness.

DISTINGUISHED_7_SOURCE_PERSISTENCE proves a separate uniform creator fact:
once considering the six active marks excluding7, a genuine H1 A macro
cannot change whether physical7 belongs to their ancestor core. Any loss
or restoration needs H>=2. This locates a source event, but does not prove
positive certificate slack or an available frozen-owner donor. Those are
distinct obligations; old refuted RR7 protection is not revived.
''')

doc('FR32_RETURN_PATH_SOURCE_CLASSIFICATION.md','''# Gate D — complete split at first9; proved and open branches

Every valid first-return history either has no9 before tau7, or has a
unique first activation9 before tau. Closed genuine support ensures tau;
an open fragment without it is not a terminal example. No bounded return
length or generic W0/W1/U decomposition is assumed.

|Source class|Current result|
|---|---|
|No9 before first7|FR32-N9: universal D_out<=1 at this proper subclass|
|Immediate H1 first9, actual return H>=3|FR32-H: universal D_out0, all intervening source operations retained|
|Immediate H1 first9, arbitrary H1 upper-only word before first lower|FR32-U: return impossible before lower exit; debt<=1 at that exit, arbitrary finite upper repetitions|
|Immediate H1 first9, H2 return|Static terminal import has only two adverse necessary sectors; actual source slack/exclusion still OPEN|
|Immediate H1 first9, H1 return|Further adverse necessary sectors, including a two-ternary marked return candidate; reachability/slack OPEN|
|Delayed first9 or H>=2 activation|Fixed old/new chart source bridge proved; cold D-transfer and entry slack OPEN|

Once activated,7 is a B marked leaf in a rigid term. Both pre-activation
and post-activation six-key phases have fixed core11/density source
representations. The q5 maximum-depth star lemma prevents truncation at
the cold9 or return7 seam; only tau itself q5 in the no9 case needs the
proved weakened singleton bound. Cold chart switching and actual terminal
slack are STILL not supplied by the fixed-chart certificate.
''')

doc('W101_CARRY_ONE_SHARPNESS.md','''# Gate E — exact attained debt one, without claiming the missing supremum

The C31 source is unchanged. After original N85 and modified reachable
prefix, helper124..return129 has targets11,5,11,9,5,7; H1 each,
Q2,3,1,3,1,2 and sigma-1,0,0,0,0,0. Entry1, return repayment0, D_out1.
Next11 at130 contributes+1 only in that known word. Every old A/BF/short
BE state and occurrence is retained in the authoritative C31 v2 file.

W101 and its symbolic finite erased alignment satisfy the full original
paired-closed source conditions. It lies in EXC with immediate H1 activation,
so the principal source class really attains1. This proves sup D_out>=1,
not sup=1 while the universal upper bound remains OPEN. It is outside
FR32-N9 and has H1 return, hence is not excluded by FR32-H. The later
positive11 is not made a universal recovery horizon.
''')

doc('FR32_SYMBOLIC_SOURCE_COMPLETION_STANDARD.md','''# Gate J — symbolic original-source closure and execution distinctions

C31's accepted literal W101 returns A/BF by an SS inverse/support/A-only
reset proof; its seven genuine marks require the KEEP1,KEEP3 support loop.
The erased map F acts deterministically on the same13-key BST universe,
C=Catalan13=742900 states. Prefix N W^C, period W^(C!) closes erased B
because every eventual orbit period p<=C divides C!. This is a finite
original word represented compactly, not an abstract transition edge.

C32 inserts the exact source identity L4=(KEEP13,9,11,9) after W position42.
The first operation has new A/BF execution and one independent BF check.
The remaining B inverse and A opposite rotations are written proofs.
W105 returns A/BF, retains all seven genuine marks, and has the same
finite-orbit erased completion. transient_W105_certificate records the
literal105 operations and exact symbolic initial erased state F105^C(E0).

Neither whole W105 nor C! copies were numerically executed. The short
erased state after new13 is an exact unevaluated ordinary splay expression.
It is not a guessed tree/cost. Closed-copy erased states are their actual
F105 orbit points. No evaluated full-period QE, normalized owner receipt,
or legal Step1 cut is invented. Any supplied cut/map retains its actual
original certificate; source IDs are transported on both endpoints.
''')

doc('FR32_TERMINAL_STATE_INTERFACE.md','''# Gate H — exact nonresetting terminal state

Retain S_return=(actual A tree, actual full B tree, actual erased tree or
its exact original-execution expression, M/core labels, chart definition,
cumulative signed B, D=max(0,-B), helper provenance, orientation, actual
source occurrence/period phase, frozen successful map a and bank state
where the physical interface requires them). No smaller quotient has been
proved sufficient for ALL future signed/owner evolution. The six-key A
quotient suffices only for the imported D table, not all future7 accesses.

W101 has E_return0 versus pre-helper1, D_out1; it is a genuine nonreset.
W105 has an interior D2, but FIRST return D0 after a real +2 loop. These
are distinct terminal/trajectory records despite both returning root7.
FR32-N9 proves only the restricted terminal range{0,1}; FR32-H proves0
at its HIGH-return scope. General EXC's terminal range is still unproved.
In particular no debt coordinate is set to zero at a chart or root boundary.
''')

doc('CARRY_AWARE_REPAYMENT_HANDOFF.md','''# Gate I — bounded terminal carry and eventual payment are separate

The known W101 terminal1 is real; its next11 pays only that construction.
FR32's restricted bounds neither force a next11 nor a deep future access.
Even a future universal carry-one theorem would not settle eventual payment,
repeated overlapping debt, persistent owners, chart renewal or source cuts.

For now preserve the exact activated terminal state and the open source
slack/cold-transfer conditions in OPEN_CHART_AND_TERMINAL_INTERFACES.
Do not begin unconditional normalized-owner/global Gate U composition from
a false zero-reset or an unproved principal carry bound. A source credit
must still have actual original provenance and one eligible physical owner.
''')

doc('CARRY_VERSUS_PHYSICAL_COST.md','''# Gate K — signed carry is not an original cost violation

W101 has Q82,A>=58 and original2A-Q>=34; its12-demand negative signed
first-return interval already has a complete separate12-unit injection.
The new13 H1/Q2 macro itself has2A-Q0 and both demands naturally fit its
two bits. It raises signed debt because E drops1, not because it lacks
physical units. W105 adds4 A events and6 B doubles, so Q88,A>=62 and
2A-Q>=36. Its full return has D0 despite intermediate2.

No source-valid terminal D>=2 was constructed. Even if one were found,
it would refute this signed carry architecture, not automatically a full
matching, Coarse-Double, Universal CD or Dynamic Optimality. Original costs,
selected capped budgets, signed potential differences and frozen-owner
eligibility are kept as different mathematical quantities.
''')

doc('FR32_NORMALIZED_OWNER_COMPATIBILITY.md','''# Gate L — original owners fixed; no global payment inferred

This campaign's restricted signed theorems do not spend a physical bit or
move any existing successful owner. The complete raw independent H for
W101 has its accepted scope; normalized effective extension still needs
ACTUAL a, original eligibility/retirement/transport and a real profile<=9
receipt. Under those hypotheses its all-cut H6 gives bound24. Bank25
alone never implies profile9 or that an apparent q1 spare is unowned.

W105 is a new mathematical source control. No canonical/normalized f6 or
full supplied fE/a was numerically evaluated on its factorial period.
No old W101 raw20/H3/6/conditional24 receipt is copied to W105 without
a separately proved composition/profile bridge. No new frozen-owner
extension or Bank24 theorem is claimed here. This keeps the primary
signed carry investigation separate from universal owner funding.
''')

doc('FR31_FIX_STATUS_PRESERVATION.md','''# Gate M — FIX remains a separate branch

FIX is the exact saved C30 entire A tree. PREFIX includes it at that
parameter and allows only source-valid prescribed shallow-frame variations.
The C31 variation changes the deeper ordered A term below11; it does not
refute the universal FIX zero-return theorem. The old FIX9 activation H2
versus PREFIX H1 control remains unchanged and was not rerun.

FR32-N9/H/U apply to FIX only when their explicit source hypotheses hold.
They do not prove the entire FIX problem or the broader PREFIX theorem.
The new transient-two fixture uses the existing PREFIX activation and
does not alter the FIX input. Universal FIX stays OPEN.
''')

doc('REPEATED_RETURN_CARRY_INTERFACE.md','''# Gate N — repeated intervals are not silently independent

W101 and W105 can be repeated on their exact aligned original periods;
each copy has distinct original occurrence/event/bit IDs. Their complete
closed resets are mathematical source constructions; a root7 inside a
copy is not that reset. They do not prove arbitrary EXC intervals have
disjoint helpers, common chart state, or independent carry coordinates.

A future repeated-return theorem must state whether outgoing local debt
enters the next obligation, retain positive balances, identify overlap of
helpers and actual physical repayments, preserve frozen a and chart/cut
state, and never borrow a unit from another formal cyclic copy. No repeated
global carry bound or inevitable later repayment is established by the
restricted one-return results. The all-r r-4 width/storage obstruction is
not removed by a seven-key statement.
''')

controls=[
('A1 W101','Included EXC, attained terminal1; no new old-source replay'),
('A2 FIX/PREFIX9','Preserved cost2 versus1; FIX not refuted'),
('A3/A4 N85/four-macro','Accepted full source/control unchanged; its first return repays'),
('A5 W0/W1/U','Restricted returning/reset theorem retained, not all-return decomposition'),
('A6 helper-1','Genuine helper debit remains; helper-only nonnegativity never asserted'),
('A7/A8 W459/W199','Prior refutation/repair and successful owners unchanged'),
('A9 entry2','Outside EXC; broader barrier retained, no new reachability claim'),
('A10 second negative','New actual post913 H1/Q2, intermediate2; not terminal counterexample'),
('A11/A12 first11/13','EXC first11 fixed; first13 outside, later13 allowed'),
('A13 long phases','Seven-form proof arbitrary finite H1 upper length; general activated continuation OPEN'),
('A14/A15 flips/charts','Actual A state/H and intrinsic E boundaries retained; cold table transfer not assumed'),
('A16/A17 debt/deeperreturn','Terminal state explicit; W101 root7 carries1'),
('A18 core6 loss','Invalid direct-return controls preserved; full core13 required'),
('A19/A20 closure/replay','W105 original inverse identity plus symbolic erased orbit; not executed whole word'),
('A21 signed/physical','Intermediate2 at physical price0; no CD inference'),
('A22/A23 raw/profile','No normalized substitution, no unproved profile9'),
('A24/A25 scope','No eventual-payment or all-r promotion'),
('A26/A27 copies/undefinedreturn','Absolute actual IDs; no return value assigned to an unfinished fragment'),
('A28 caps','Exactly3 authorized new queries, total2M; all symbolic/static CPU under controller')]
ct='\n'.join(['|Control|Result|','|---|---|']+[f'|{a}|{b}|' for a,b in controls])
doc('ADVERSARIAL_SOURCE_CONTROLS.md',f'''# Exact controls and failed sufficient bridges

{ct}

Two candidate imports failed as pointwise claims on OLD necessary syntax:
D6<=E6+1 has94 adverse BF blocks (max gap3), and the unrestricted proposed
terminal import has1493 adverse quotient tuples. They are NOT new reachable
source counterexamples. q5 singleton margin>=0 also fails on saved LOW
tuples; the weaker margin>=-1 holds everywhere and is used only where the
real source proof handles the terminal fragment. Failed mechanisms are
retained, not patched by assuming their adverse states unrealizable.
''')

doc('IAGS_PROOF_TREE.md','''# IAGS closure/reopening ledger

Freeze: exact FR32 source Box, FIX/PREFIX separation, original sigma debt.
Inherit: C31 exact counter/entry/full-family interfaces and accepted CD6
complete local source syntax, not a scalar open-path theorem.
Recurse: exact N1/N2 negative classes -> carry-two necessity R<=-1.
New source lemma: marked SS preserves core/density; old/new six-key phases
separated by first9; q5 stars cannot straddle the interior-key seams.
New arithmetic: old-root7 D bound, weakened q5 singleton bound; separate
implementation verifies them on the old COMPLETE grammar.
Reconstruct/close child FR32-N9: no activation before return -> carry<=1.

Alter sufficient route: allow intermediate2 rather than false all-times1.
New control: real13 operation plus symbolic identity loop -> W105 closed,
intermediate2 but terminal0. Not a parent refutation.
New source seven-form grammar -> upper-word potential/forced lower exit.
Close child FR32-U: debt<=1 at first lower exit, not all later returns.
Close child FR32-H: immediate H1 activation, HIGH return -> debt0.

Reopen pointwise table shortcuts: D6<=E6+1 and unrestricted terminal import
fail on necessary syntax. No adverse tuple is assumed source-realizable.
New A pivot-persistence lemma locates an H>=2 creator, but owner freedom
and positive signed slack are NOT inherited from that location alone.

Parent remains OPEN: delayed cold9 source transfer, activated LOW terminal
reachability/slack. Next child has one A quotient/two BF sectors at H2;
prove source-forced Lambda>=1 or construct actual closed Lambda0. A proof
would close that child only; H1 and delayed entries remain parent Boxes.
No original theorem or resource cap is altered to accommodate a failure.
''')

doc('C33_CARRY_AWARE_REPAYMENT_HANDOFF.md','''# Next bounded source Box — H2 terminal slack in two sectors

Principal FR32 is unresolved. Do not start an unconditional eventual-
repayment or normalized-owner campaign. Start the exact smaller Box in
OPEN_CHART_AND_TERMINAL_INTERFACES:

Target: immediate H1 activation with D6(v)=1; actual first-return H2;
A quotient381, BF1060 or1063. Prove actual Lambda_new>=1 from source
rotations/creator geometry, or construct a paired-closed Lambda_new0
occurrence. Exact identity R=Lambda_new-1 makes the latter a genuine
D_out2 counterexample. The protected seventh key's physical A placement
and actual history must be retained, not inferred from the six quotient.

Conditions: unchanged EXC, original source/SS/core13, genuine seven marks,
actual A macro costs, cold/terminal chart meanings, all original owners
and period rules. Inheritance: proved fixed-six source bridge, all old
table inequalities, exact two adverse sectors and pivot persistence.
Ambiguity: whether its required H>=2 creator contributes positive source
slack; physical owner availability does not follow from H>=2 alone.
Bridge: Lambda>=1 pays this boundary loss1; a real Lambda0 example refutes
principal carry-one. Neither conclusion automatically handles H1 terminal
sectors or delayed cold entries.

Query budget is0 at2M/2M. Continue manuscript/saved-proof analysis under
the remaining cumulative CPU caps; no new original source primitive or
compiler is authorized without a legitimate extension. Every old failed
and current exact receipt remains preserved. External source-induction
audit and all global owner/Bank25 interfaces keep their actual status.
''')

doc('GATE_U_SOURCE_DEPENDENCY_STATUS.md','''# Gate U — no unconditional promotion

Accepted C14 transfer remains I(r-1)+E_r=>I(r), where I is a witness-rich
source license with actual unit selection/period/owners, not an assumed
desired full matching or scalar CD. Accepted I(6)/CD6 is unchanged.

|E_r clause|C32 contribution and remaining status|
|---|---|
|1 erased reachability/normalization/actual period/fixed fE|W105 has a new symbolic original paired embedding; no evaluated normalized allocator/cut selector fabricated|
|2 complete source-derived full license|Restricted carry/source barriers advanced; principal EXC carry-one and other full-domain/all-r supply still OPEN|
|3 common pairing/retirement/eligibility/transport/Bank25/old owners|No owner moved; old conditional profile9/interface retained, no universal new proof|

The old stronger I(5) source selector is not inferred from scalar CD5.
All-r r-4 carry/width and Bank25 restrictions remain. Local bounded carry
is not eventual repayment, and neither implies the missing global
source/owner hypotheses. U-OPEN. Step3, Universal CD and Dynamic
Optimality remain OPEN.
''')

pt='\n'.join(['|Phase|Class|Status|Source queries|CPU child+controller|','|---|---|---|---|---|']+[f"|{z['phase']}|{z['group']}|{z['status']}|{z['source_queries']}|{z['total_charge']}|" for z in phases])
doc('INDEPENDENT_AUDIT_STATUS.md',f'''# Executed verification and proof limits

{pt}

Exactly3 NEW original source queries: producer A/BF KEEP13 from the saved
after9 state, and distinct mutable BF execution. Source A was not replayed
by the independent implementation; erased13 was not numerically executed.
No old source trajectory or accepted old semantic audit was repeated.

New static producer/independent checks read the OLD complete A/BF grammar,
cached transition costs and debt arrays. They check new integer statements,
root-bound, weakened q5 law, boundary-sector arithmetic, the twelve manually
derived upper-form edge weights, and the literal W105 descriptor. They
perform no new splay, source path call or newly compiled source relation.
The A gap-depth predicate is a necessary syntax condition, not a realized
private7 depth query; the B terminal formula uses cached q9 and the written
source identity. Their CPU is fully charged, not hidden in metadata work.

The complete source grammar's OLD uniform lifting is inherited. New SS,
q5-boundary, upper-normal-form and pivot-membership inductions are written
mathematical proofs; the static scripts do not formally certify them or
claim a new kernel audit of every form. Pending external/source proof audit:
check exact private-term stencils, mass preservation, extreme-star seam
argument, A one-event persistence, no9 old-chart initial/terminal lifting,
HIGH return identity and actual new chart/cut/ownership interfaces.

Whole W105 and factorial erased period are symbolic source constructions,
not executed runs. Same-agent separate implementations are not external
peer review. Every input manuscript hash is pinned to its receipt where
checked; no audit-pending proof is promoted to SEALED.
''')

gate=[('A entry','CLOSED AT EXC SCOPE','entry1; broader0/2 classes separate'),
('B carry-two necessity','DERIVED','R<=-1; exact N1/N2/Rplus ledger'),
('C geometry','PARTIAL SOURCE THEOREMS','pivot persistence, actual transient2; not terminal2'),
('D return exhaustion','STRUCTURAL SPLIT','no9 closed; activated phases and LOW terminal/cold gaps explicit'),
('E W101','PRESERVED','attained terminal1, universal supremum still OPEN'),
('F carry-two construction','NOT ESTABLISHED','W105 intermediate2 ends first return0'),
('G invariant','RESTRICTED PROOFS','N9 carry<=1; immediate9 HIGH return0; H1-upper lower-exit bound'),
('H terminal state','EXPLICIT','full state/carry/phase retained, root7 not reset'),
('I eventual repayment','OPEN SEPARATE','no next11 theorem'),
('J closed embedding','SYMBOLIC CONTROL','literal W105/finite orbit, not whole execution'),
('K physical cost','PRESERVED','W105 Q88,A>=62,margin36; no CD counterexample'),
('L owners/bank','CONDITIONAL UNCHANGED','no new normalized receipt/profile/extension'),
('M FIX','SEPARATE OPEN','new PREFIX control does not refute saved tree'),
('N repetitions','OPEN GENERALLY','only literal repeated closed fixture'),
('O principal verdict','UNRESOLVED','neither universal terminal bound nor genuine terminal2')]
gt='\n'.join(['|Gate|Status|Scope|','|---|---|---|']+[f'|{a}|{b}|{c}|' for a,b,c in gate])
principal=f'''# UNRESOLVED — terminal carry-two exclusion/construction remains open

FR32-CARRY1 is NOT proved and no source-valid FIRST-RETURN debt>=2
counterexample is claimed. The new genuine debt2 control is INTERMEDIATE;
its closed W105 completion has terminal0. The known W101 still ends at1.

New restricted uniform derivations:

1. FR32-N9: for every EXC history with no activation9 before first return7,
   D_out<=1, arbitrary length/private populations/original operations.
2. FR32-H: immediate H1 activation9 and actual return H>=3 imply D_out0,
   with arbitrary intervening original source operations.
3. FR32-U: every finite H1 upper-only word after immediate activation must
   exit through1/3/5 before a legal7 return, and debt<=1 at that first exit.
   This allows the actual intermediate2 and proves its compensation there.

The source bridge reuses the accepted six-key certificate correctly: fixed
old chart before first9, fixed new chart after it, original A operations
unchanged, explicit cold-transfer and terminal conditions. q5 stars cannot
straddle an interior-key seam. Static array/graph arithmetic passed a
separate same-agent implementation; new source inductions are manuscripts
with external/source-kernel audit pending, not newly SEALED proofs.

The naive pointwise terminal import fails on1493 NECESSARY tuples, not
1493 realizable counterexamples. For immediate H1 activation, only TWO
sectors obstruct the H2-return import: A381 with BF1060/1063, D6=3 and
actual terminal margin-1. The exact remaining source identity there is
R=Lambda_new-1. Prove source-forced Lambda_new>=1, or construct a genuine
closed Lambda_new0 history. This is the next bounded Box. H1 terminal
sectors (including a two-ternary candidate) and delayed/other cold entries
remain additional parent obligations; they are not excluded by convenience.

{gt}

Branch `{e['branch']}`, HEAD `{e['head']}`. Tracked files clean;
{len(dep['pins'])} inherited local hashes match. Cumulative CPU{total}/7200;
symbolic{groups['symbolic']}/240; independent{groups['independent']}/600.
Original source queries{qtotal}/2000000, remainder0. All new queries were
the precise13 control, not a broad search. No cap reset or extension.

The query cap is now a verification boundary; it is not proof that a
terminal2 source is impossible. The MATHEMATICAL gap is actual source
reachability/slack at the LOW terminal sectors and cold chart transfer.
No scalar global inequality, assumed injection or owner-free spare fills
it. All frozen owners, R1-R4, Bank25 and accepted CD6 remain unchanged.
Universal eventual repayment, Gate U and Dynamic Optimality remain OPEN.
'''
doc('FR32_CARRY_ONE_FINAL_THEOREM_OR_COUNTERCERTIFICATE.md',principal)
doc('FINAL_VERDICT.md',principal)

doc('CHECKPOINT.md',f'''# C32 continuation — restricted barriers proved, principal terminal law OPEN

Read FINAL_VERDICT, PRE_ACTIVATION_CARRY_THEOREM, HIGH_RETURN_CARRY_THEOREM,
UPPER_ONLY_BARRIER and OPEN_CHART_AND_TERMINAL_INTERFACES. Source scopes
are frozen in FR32_FIX_PREFIX_SCOPE_FREEZE; FIX remains separate OPEN.

Principal identity: after u, balance-1,E0. For T=(u,tau], R=P+E_tau,
D_out=max(0,1-R). Terminal2 iffR<=-1. Negative macros are only actual
H1 marked-leaf N1(-1) or two-ternary N2(-2); necessary, not all realizable.

Closed children: no9 before first7 ->D_out<=1. Immediate H1 activation9
and returnH>=3 ->D_out0. H1 upper-only arbitrary finite words cannot
return7 before a lower1/3/5 exit; at that first exit debt<=1. Fixed old/new
six-core11 source and complete q5-packet bridges are written explicitly.
Do not apply scalar closed CD6 to an open path or freely switch D charts.

New source control: insert13,9,11,9 after W101 position42. First13 H1/Q2
sigma-1 was executed in A/BF, independently checked in BF. Loop+2 returns
A/BF symbolically. W105 Q88,62 genuine KEEPs, margin>=36; erased closure
uses exact F105 orbit/C! construction, NOT replay. Intermediate2 is NOT
Outcome E; FIRST return7 ends at0. Preserve all W101 data and superseded
C31 metadata distinctions; no old source check needs rerunning.

Next exact Box: immediate H1 activation,D6(v)=1; actual terminalH2,
A381/BF1060 or1063. R=Lambda_new-1. Prove actual source Lambda_new>=1
or construct fully closed Lambda_new0. Retain physical A7 placement and
the whole original history; quotient compatibility is not realizability.
Pivot-core membership changes need H>=2, but positive slack/eligible donor
does not follow merely from this creator location. H1 terminal and delayed
cold9 transfer remain separate parent Boxes.

All static checks passed; source-induction/external audit pending. No full
principal theorem or terminal2 source certificate exists. All normalized
owner/retirement/transport/profile and Bank25 conditions remain original.

Branch `{e['branch']}`, HEAD `{e['head']}`. CPU{total}/7200;
symbolic{groups['symbolic']}/240; independent{groups['independent']}/600.
Queries{qtotal}/2000000 leave0; controller and all other caps unchanged.
Manuscript/saved-proof reasoning remains allowed; NO new original source
query, source-frame compiler or hidden splay is authorized. This is not
a CPU-exhaustion claim or mathematical impossibility conclusion.
''')

resources={'status':'CUMULATIVE_NO_RESET','prior_uniform_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'global_cap':7200,'global_remaining':7200-total,
 'cumulative_group_CPU':groups,'group_caps':e['group_caps'],'group_remaining':{k:e['group_caps'][k]-groups[k] for k in groups},
 'phases':phases,'new_C32_source_queries':queries,'conservative_all_queries':qtotal,'query_limit':2000000,'conservative_remaining_queries':0,
 'source_query_budget_exhausted':True,'manuscript_and_saved_certificate_analysis_not_prohibited':True,
 'all_failed_successful_child_controller_charges_retained':True,'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,
 'memory_limit_bytes':32*1024**3,'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,
 'resource_authorization':'unchanged explicit240/600/7200 caps, 2M source queries; no extension or reset',
 'metadata_CPU_excluded_under_inherited_convention':{'entry_checkpoint':e['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()},
 'outcome':'UNRESOLVED principal; restricted source barriers retained','principal_FR32_CARRY1':'OPEN','Gate_U':'OPEN'}
out('resources_checkpoint.json',resources)
out('FR32_RESULT_CERTIFICATE.json',{'outcome':'UNRESOLVED','principal_FR32_CARRY1':'OPEN','terminal_carry_two_counterexample':False,
 'restricted_mathematical_derivations':{'FR32_N9':'all EXC without activation9 before tau have D_out<=1',
 'FR32_H':'immediate H1 activation9 and H_tau>=3 have D_out=0',
 'FR32_U':'arbitrary finite H1 upper-only words force lower exit, debt<=1 at that exit'},
 'new_transient_two_control':{'literal_closed_word':'transient_W105_certificate.json','terminal_debt':0,'intermediate_debt':2,
 'Q':88,'A_lower_bound':62,'CD_margin_lower_bound':36,'full_word_and_period_replayed':False},
 'static_terminal_necessary_tuple_failures':1493,'actual_H2_candidate_sectors':audit['actual_H2_terminal_static_exceptions'],
 'next_source_target':'actual Lambda_new>=1 in A381/BF1060 or1063, immediate H1 activation with D6(v)=1 and actual return H2; real Lambda0 would refute principal',
 'remaining_parent_obligations':['H1 activated return sectors','delayed/other cold9 D-transfer','actual source slack/reachability','global normalized owners','repeated carry/eventual repayment'],
 'new_source_execution':'2 producer queries A/BF post9 KEEP13; 1 distinct BF query; erased state expression only',
 'new_static_independent_arithmetic':'PASS','source_induction_kernel_or_external_audit':'PENDING','external_audit':False,
 'full_normalized_owner_receipt_evaluated':False,'historical_owners_modified':False,'Bank25':25,
 'Coarse_Double_counterexample':False,'Gate_U':'OPEN','branch':e['branch'],'HEAD':e['head']})
assert not (B/'FULL_PROOF.md').exists() and not (B/'CARRY_TWO_ORIGINAL_SOURCE_COUNTEREXAMPLE.md').exists()
out('campaign_manifest.json',{'status':'APPEND_ONLY_C32_PUBLICATION','branch':e['branch'],'HEAD':e['head'],'tracked_tree_clean':True,
 'inherited_local_matches':len(dep['pins']),'no_historical_artifact_modified':True,'principal_theorem_not_promoted':True,
 'files':[{'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f)} for f in sorted(B.iterdir()) if f.is_file() and f.name not in ('campaign_manifest.json','publication_exit.json','publication_seal.json')]})
out('publication_exit.json',{'status':'PASS_METADATA_PUBLICATION','whole_process_CPU_seconds':time.process_time(),'semantic_calls':0})
out('publication_seal.json',{'status':'HASHED_PUBLICATION_NOT_A_THEOREM_SEAL','manifest_sha256':sha(B/'campaign_manifest.json'),'publication_exit_sha256':sha(B/'publication_exit.json')})
print(json.dumps({'status':'C32_PUBLISHED','principal':'UNRESOLVED','restricted_derivations':['N9','HIGH_RETURN','UPPER_EXIT'],
 'CPU':total,'groups':groups,'queries':qtotal,'query_balance':0,'pins':len(dep['pins'])}),flush=True)
