"""Metadata-only append-only C30 publication, no semantic calls/replays."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;ROOT=P.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
def git(*s):return subprocess.check_output(['git',*s],cwd=ROOT,text=True).strip()
e=read(B/'entry.json');dep=read(B/'dependency_pins.json');audit=read(B/'independent_audit.json');mix=read(B/'independent_mixed_reset_audit.json');exc=read(B/'independent_source_exclusion_audit.json')
assert git('branch','--show-current')==e['branch'] and git('rev-parse','HEAD')==e['head'] and not git('status','--porcelain','--untracked-files=no')
for z in dep['pins']:assert sha(ROOT/z['path'])==z['sha256'],z['path']
for z in dep['external_pins']:assert sha(Path(z['path']))==z['sha256'],z['path']
assert audit['status'].startswith('PASS_') and mix['status'].startswith('PASS_') and exc['status'].startswith('PASS_')
total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[];queries=0
for p in sorted(B.glob('run_*_result.json')):
    z=read(p);c=read(B/('controller_'+z['phase']+'_exit.json'));z['controller_CPU']=c['whole_process_CPU_seconds'];z['total_charge']=z['child_CPU']+z['controller_CPU']
    total+=z['total_charge'];groups[z['group']]+=z['total_charge'];queries+=z['source_queries'];phases.append(z)
qtotal=e['inherited_conservative_queries']+queries
assert total<7195 and all(groups[k]<e['group_caps'][k] for k in groups) and qtotal<=2000000
r=read(B/'nonextremal_source_countercertificate.json');p=read(B/'forward_recovery_and_period_receipt.json');bridge=read(B/'mixed_reset_bridge_receipt.json')
footer='''
Scope/status: original seven-genuine-KEEP/maximal-core13/all-SS source,
unless a narrower source family is explicitly stated. Exact new receipts
passed a distinct implementation operated by the SAME research agent;
not external peer review or formal proof-assistant certification. Written
uniform inductions are not finite sampling proofs. Accepted inherited
theorems/audit-pending labels remain at their original scope. Principal
NH30, unrestricted Gate U, Universal CD and Dynamic Optimality remain OPEN.
'''
def doc(n,s):write(n,s+'\n'+footer)

doc('SOURCE_INTEGRITY.md',f'''# Original local source, immutable inputs and cumulative resources

Branch `{e['branch']}`, HEAD `{e['head']}`; tracked tree clean. All work is
new untracked C30 files. No reset/checkout/commit/network replacement or
historical proof/owner edit occurred. All {len(dep['pins'])} inherited local
artifact hashes and external directive pins match. Exact hashes/paths are
in dependency_pins.json. Provenance hashes do NOT certify mathematical truth.

The first research artifact is NH30_FROZEN_SOURCE_BOX. Source reconstruction
uses the actual C29 checkpoint, verdict, MC29-P/X/F, helper/debt identities,
source and independent receipts; C28 witness/hybrid/family; original Step1,
CD6 and Gate U14 interfaces. Core membership constancy and all three E_r
clauses were inspected directly in C14. No remote snapshot was substituted.

A splays EVERY original operation. Full B splays KEEP including identities;
DELETE is A-only, never physical deletion. Erased B takes its exact KEEP
subsequence. Actual a=ceil(depth_A/2), q=floor(depth_B/2), physical unit
(t,j,b). Genuine full macros retain ALL intermediate operations. Original
source, full midpoint/shadows, signed quantities and actual IDs are unchanged.

R1 exact original target/domain/closure; R2 original weighted costs and
events; R3 frozen sources/owners/caps, separate explicit new comparison;
R4 no UNKNOWN/FAILED as PASS or premature theorem promotion. Bank25 stays25.
The executed controller is preserved; run_phase2 adds version-name aliases
for the SAME phase/query budgets and subtracts every earlier run. This is
not a new allowance. All children/controllers, including failures, are charged.

The counterexample N has actual I86..170, reachable diagonal prefix85,
all three trees closed, full core13/erased core11 and exact event ledgers.
No supplied original f5/f6 is fabricated for this NEW source. The normalized
owner theorem quantifies over an ACTUAL supplied effective map and retains
its original eligibility/retirement/cut and profile hypotheses.
''')
doc('C29_INHERITANCE_LEDGER.md','''# Exact dependency status and use

All paths are under DO_RESEARCH_REBOOT; dependency_pins.json contains exact
filenames/hashes. Earlier inspected proofs/receipts are reused rather than
rerunning completed audits. Interface-only inheritance is not new sealing.

|Dependency|Current status/use|
|---|---|
|C29 FINAL_VERDICT/CHECKPOINT|A-L, principal MC29 OPEN; authoritative H29-1 Box|
|C29 PREDECESSOR_CLASSIFICATION|Exhaustive incoming marked-comb U/B/P and two-step separation; exact source hypotheses retained|
|C29 EXTREMAL_COMB_REPAYMENT|Opposite-extreme comb endpoint guard; comparison-level theorem, generic owner interface conditional|
|C29 MIXED_COMB_FAMILY_THEOREM|W0/W1 arbitrary finite mixture, prescribed raw inputs, actual frozen map peak5; not all-normalized theorem|
|C29 degree-excess/helper/source receipts|E formula and genuine closed helper-1; global per-edge E REFUTED|
|C28 W199 and V^mW|W19958/58,Pempty; specified neutral family Bank6, restricted source/receipt theorem|
|C28 W459/hybrid|Pure catchment forcing REFUTED, physical funding/hybrid restricted repair retained|
|C27 exact source|Accepted guarded-e4 witness/owner receipt; source not rerun|
|C26/C25/C24|Qualified direct consumer/cycles, safe exterior G-v and ownership-adjusted eligibility; no new universal owner audit|
|C23/C22|Actual nonidentity G=-1/R=0, creator/T19/own-tail policies and successful owners unchanged|
|C14 CLOSED_PERIOD_CORE_CONSTANCY|Inspected proof: fixed-mark core labels cannot grow; strict loss excludes a closed core13 transition|
|C14 UNIFORM_R_TRANSFER|Inspected I(r-1)+E_r=>I(r), all three premises; no unconditional induction|
|C14 cd6_allocator, original Step1|Inspected distinction between raw and supplied fE-normalized branch, source period/retirement rules; accepted CD6 not reopened|
|C15 path-to-star|Actual nearest-marked-ancestor degree and leaf identities at original all-SS domain|

Same-agent separate implementation is not external review. All inherited
audit-pending status is retained. New exact source failures are classified
by their actual missing premise and not used as failed CD certificates.
''')
doc('SIGNED_REPAYMENT_DEPENDENCY_GRAPH.md','''# Source dependency and closed/open bridges

Original Pair Access -> fixed marked-core membership -> all-SS actual path
to star -> C29 rho/E identity -> exact negative helper class/arity budget.
MC29-P -> critical Qj2 zero predecessor -> NEW paired-closed source N
-> three-macro rule REFUTED (owner-independent source statement).

N exact source -> actual forward q1 return seed -> complete signed48-macro
partition/full natural-compatible H_N -> rotated U returning word
-> arbitrary U^m induction, local profile3, all-cut profile6.

C29 W0/W1 plus U -> identical B/BE, unequal A -> SAME actual A-only
ordered reset -> exact two-endpoint source bridge -> arbitrary cyclic
mixtures -> matching signed chart boundaries -> independent raw working17.

TOTAL comparer + ACTUAL supplied normalized a + original path eligibility/
retirement/transport + B_a<=9 -> literal frozen extension, profile<=24.
This is conditional; it does not assert all normalized a satisfy those
hypotheses. H is a separate reference, never extra physical spending.

Failed immediate-first-return falsifier -> actual core label6 lost ->
excluded by closed-source constancy. Uniform low-side parity barrier and
low-phase signed bound-1 -> at most2 debt units at first upper KEEP.
OPEN: upper/return phase uniform repayment and joint owner/noncollision.
''')
doc('NONEXTREMAL_SHALLOW_SOURCE_NORMAL_FORM.md','''# Exact inherited class; no intuitive redefinition

Shallow means H1, one ACTUAL A StepEv in a genuine full macro. It need not
mean Q1; a unique earlier DELETE of the terminal key can carry that event.
Every intermediate zero/root-repeat/delete is retained. High arity is
marked outdegree alpha>=3, not physical BST child count or A-tree degree.
The checkpoint priority class is target old degree d0,Q>=2, exactly one
high-arity ancestor k3=1, hence sigma_E=-1. The alpha/Q/beta ranges are
proved in HIGH_ARITY_SOURCE_UNIFORMITY, not guessed from a finite search.

Nonextremal means the old extremal guard cannot be used. In the weak-P
before-comb subcase the relevant comb endpoints x,R are not opposite extreme
KEEP keys. The helper's own endpoints are a DIFFERENT pair. General negative
helpers need not precede any comb. The old negative control remains admitted,
even though its following comb is extremal. No domain exception hides it.

The new source realizes the critical case: predecessor j target7,H1,Q2,
beta2,z0,k3=1,sigma0; helper target11,H1,Q2,beta1,z1,k3=1,sigma-1;
comb target5,H1,Q3,beta3,z1,sigma0. At the source the key order is
x5<Y7<R11<Z13, outside C29's x<Y,Z<R premise. Physical A paths L,RL,LL
are independently reconstructed, as are all actual full/erased B states.

This is genuine closed reachability for one critical arrangement. The
complete combinatorial arity table is only a necessary source restriction;
unconstructed alpha4/5 cases are neither excluded nor declared realizable.
''')
doc('NEGATIVE_HELPER_BALANCE_SOURCE_CONTROL.md','''# The old -1 control and the new nonextremal obstruction

The old C29 W0 word remains exactly as saved: actual I129..256 from its
common diagonal prefix, helper160 has H1,Q2,beta1,z1 and E1->0, hence
sigma_E=-1. Comb161 has sigma0. Current full34-owner map/Bank5 is unchanged.
Its effective unpaid set is EMPTY after the saved late payment; no new
donor is requested. The global per-edge branch certificate remains FALSE.

The cause is an actual helper DEBIT: zero physical helper price2H-Q=0
while E falls by1. The comb correction alone did not pay that debit. This
is not a sign-chart typo, a new physical donor shortage or double ownership.

New N is a stronger nonextremal control: prefix N from common T reaches S,
period N at I86..170 returns A/BF/BE exactly. At117,118,119 the triple has
sigma0,-1,0, total-1; all three H1. Its full source has A109,QF66,QE42.
Actual helper118's high ancestor7 has degree3; the following comb has
nonextreme endpoints5,11. All old source/owner data are preserved.

The refuted statements are 'weak P always forces Hj>=2 without its guard'
and 'the same predecessor/triple packet repays every nonextremal helper'.
The result is independent of normalized ownership, which never occurs in
those source implications. It is NOT a counterexample to NH30 existence,
Coarse-Double, Universal CD or Dynamic Optimality.
''')
doc('NONEXTREMAL_SIGNED_DEFICIT_IDENTITY.md','''# Exact original signed price and helper correction

At the inherited source domain Q=u+beta and Delta L=u-z. With c=min(H,3),
D_leaf=L-1 and b=#marked branching vertices,

    rho=2c-Q+Delta D_leaf=2c-beta-z,
    E=L-b-1, sigma_E=rho+Delta(3-b)=2c-Q+Delta E.

For target old marked degree d and k3 ancestors of degree>=3,
sigma_E=2c-k3 for d>=2;2c-1-k3 for d1;2c-min(Q,2)-k3 for d0.
Thus the frozen priority H1,d0,Q>=2,k3=1 has EXACT debit-1. The scalar
is not changed to protect a candidate. Actual E differences telescope only
on the true boundaries; raw branch holes, native holes, effective roots
and signed debit are separate mathematical objects.

On N the critical triple rho0,0,-2 differs from sigma0,-1,0. Actual forward
recovery adds macro balances0,+1, giving a four-macro helper packet0. In the
mixed theorem W uses D_leaf while U uses E+2; their common boundary values
are both3. The exact original-rho correction inside U is Delta(2-b), with
ZERO switch jump. No old fixed-nine-Score debt or freely selected chart
representative is used. Full nonidentity G/R corrections elsewhere remain.
''')
doc('EXTREMAL_TO_NONEXTREMAL_BRIDGE.md','''# Which old proof premises survive?

|C29 premise|Nonextremal status|
|---|---|
|Path-to-star degree identities|Inherited unchanged at actual all-SS scope|
|U/B/P predecessor classification|Inherited, no new source enumeration needed|
|Comb two-step separation|Inherited for comb packets; not automatically for all negative helpers|
|Opposite-extreme key-order barrier|Fails as a premise on x5<Y7<R11<Z13|
|Weak-P source force Hj>=2|REFUTED without that premise by N|
|Immediate predecessor/triple E repayment|REFUTED by the same actual triple|
|Existing normalized owner's bit availability|UNKNOWN until actual receipt/eligibility checked|
|Same-boundary physical family composition|Needs a source bridge; the A-only reset supplies it for W0/W1/U|

The new forward repair counts two actual successor accesses, BOTH shallow,
and a real q1 spare. It does not reintroduce the invalid future-depth claim.
The broader first-root-return mechanism remains OPEN. A tempting immediate
return7 was excluded by actual RLR/core loss, not accepted as a negative
closed-source edge. LOW_SIDE_SOURCE_BARRIER supplies a genuine necessary
first-upper event and bounded low-phase debt on that physical B frame.
''')
doc('NONEXTREMAL_HELPER_DEBT_PROVENANCE.md','''# Actual helper costs, debts and physical provenance

N's earlier preparation ends116, actual H32. The critical zero predecessor
117 has H1,Q2 and changes E1->1. Helper118 has H1,Q2,E1->0. Comb119
has H1,Q3,E0->1. The proposed earlier packet still owes1; cost32 is NOT
silently counted inside it. It exists elsewhere but a rule must license it.

The proved forward packet is118..121: actual targets11,5,11,7, H1 each,
Q2,3,1,2 and E1,0,1,0,1. Its total signed/physical balance is0. Natural
h0 pays the sole demand at120 with(120,1,0); physical spare(120,1,1)
finances comb(119,3) in the separate independent comparer. No new operation
is inserted into a frozen history and no future event is assumed deep.

Other negative helpers128/140/148 and ALL recovery costs are included in
their exact source packets. A donor under H can be occupied by actual a;
only NH30-O's licensed endpoint extension makes an actual new payment.
Auxiliary-only retirement and extra reservations remain explicit licenses.
The source reset in the mixed theorem is already in every word, and its
cross-boundary cost correction is R(previous)-R(destination), telescoping
around the actual cycle rather than generating new total credit.
''')
doc('SOURCE_FORCED_SHALLOW_REPAYMENT_MECHANISM.md','''# Surviving mechanisms, with their exact scope

REFUTED: guard-free old predecessor force/triple repayment. The exact N
counterexample is complete; changing its helper balance is not a repair.

PROVED RESTRICTED ROUTE: actual forward return packets of the specified N
word, a full signed partition and one real q1 ordinal seed. RETURNING_
NONEXTREMAL_FAMILY proves every U^m, not just one passing source. Reset-
synchronized mixed W0/W1/U source induction then includes both prior
extremal and new nonextremal blocks at compatible signed boundaries.

NORMALIZED INTERFACE: any ACTUAL supplied normalized effective map with
profile<=9 and the original retirement/eligibility/transport license is
preserved literally by a full independent comparer, with bound24. This is
a theorem with explicit hypotheses, not proof they hold in every NH30 case.

NEW SOURCE-FORCED RESTRICTION: on the post-comb B frame, the first upper
KEEP must be11 or13; arbitrary low continuation has signed sum>=-1.
Thus at most2 units of this comparison debt can reach that upper phase.
Uniform repayment through first root7 return is NOT yet established.
Source validity rules out the immediate7 falsifier but does not prove all
remaining signs. All unnamed global source-supply claims stay OPEN.
''')
doc('SINGLE_NONEXTREMAL_REPAYMENT.md','''# One genuine nonextremal helper disposition

NH30-C at actual118 is a closed-source negative helper requiring one signed
unit. Its old predecessor/triple fails at-1, despite all three A accesses
being single-event. The actual four-macro successor packet118..121 pays it:
sigma=-1+0+0+1=0, Q8,H4, E1->1. No helper cost/debt is omitted.

Natural h0 has just ONE full source deficit, comb(119,3), while the signed
helper debit is at118. Preserve h0 and assign that deficit to actual bit
(120,1,1). This is the full independent comparison H_N,66 distinct full
demands/units. It does not assert that the same bit is free under normalized
a. The licensed owner interface uses alternating endpoints and retains
every old value, with its explicit profile/eligibility conditions.

The complete source also repays its other three negative helpers; exact
48-macro packet table is saved. Raw max-E debt2 and working9 are verified.
This one-source rule is uniform under the stated returning-word, reset,
gap and reflection constructions. It is NOT a theorem that arbitrary
nonextremal sources contain these return accesses in this order.
''')
doc('NEGATIVE_BALANCE_STRESS_TEST.md','''# Arbitrarily negative helper-only balance is source-realizable

Every U block contains four actual one-high-arity shallow helpers, each
Q2,beta1,z1,alpha3 with sigma_E=-1. U returns all three actual trees.
For EVERY m>=1, U^m is therefore a genuine closed source with helper-only
aggregate-4m. Prefix/period construction and opaque-gap induction are in
RETURNING_NONEXTREMAL_FAMILY; this is not extrapolation from finite m.

Consequently no finite uniform initial helper bank WITHOUT nonhelper inflow
can fund this bookkeeping stream: choose4m larger than its initial credit.
Nor can a closed-source potential repair that zero-inflow global balance,
whose state correction telescopes. This refutes that NAMED helper-only
architecture, not one allowing real source contributions outside helpers.

Complete accounting has sum sigma_E=60m, original2A-QF=152m, and an explicit
full independent injection. A negative local helper aggregate is therefore
neither a negative original cost cycle nor a Coarse-Double counterexample.
Old W0's-1 and V^mW controls remain admitted with their actual comparisons;
no new theorem predicts they have nonnegative helper-only balances.
''')
doc('BANK25_SHALLOW_HELPER_COMPATIBILITY.md',f'''# Exact storage bounds and their prerequisites

New source U independent H has endpoint peak3 on its actual block interval
157..241. Raw signed max-E construction has actual maximum2 and working9.
Arbitrary cyclic W0/W1/U mixtures have an independent hybrid raw working
bound17, local complete comparer profile3 and all-cut/all-m profile<=6.
The cutwise proof uses live(t) symmetric-difference live(cut), not a bank
allowance reset. All physical bits retain actual(t,j,b) within the supplied
period; a long wrapped endpoint is the same real occurrence, not extra credit.

For ACTUAL normalized effective a, NH30-O gives B_extended<=6+2B_a.
Thus B_a<=9 and the inherited source path/retirement/transport license give
24<Bank25. Bank25 alone does NOT imply B_a<=9. No theorem for larger
profiles/extra locked reservations is asserted. Raw comparer construction
and final effective assignment are separate proof maps; H is not additional
physical spending alongside a. Old physical assignments stay literal.

All cumulative caps unchanged: CPU{total}/7200, symbolic{groups['symbolic']}/240,
audit{groups['independent']}/600; conservative queries{qtotal}/2000000 leave
{2000000-qtotal}. Every failed/successful producer and controller is charged.
No new independent-audit allowance, query allowance or storage cap was made.
''')
doc('COLLECTIVE_NONEXTREMAL_REPAYMENT.md','''# Collection-wide result actually established

For the specified U^m family every helper/recovery packet is inside its own
actual block, with one explicit local physical seed and disjoint event IDs.
The48-macro signed partition repeats exactly. Ordered reset/gap proofs,
not finite repetition tests, establish this for arbitrary m. No helper
payment or physical unit is reused. Four negative helpers per block have
their full costs/corrections included; arbitrary helper-only debt is allowed.

The reset-synchronized mixed theorem proves the same independent comparison
and signed composition for every finite cyclic mode word in W0/W1/U. It
handles unequal A endpoints through their actual common reset and matched
B-state chart values. Arbitrary supplied normalized owners compose only
under NH30-O's actual profile<=9 and original eligibility/transport license.

General overlapping first-return intervals, shared ancestor creators,
alpha4/5 helpers, two-ternary debts, nonidentity flips outside these words,
unselected exterior owners and arbitrary support remain OPEN. The old comb
separation lemma does not prove all such helper packets disjoint.
''')
doc('SHALLOW_REPAYMENT_PERIOD_AND_CHARTS.md','''# Actual intervals, legal cuts and chart accounting

N: common diagonal T, actual prefix N of85 operations, then I86..170.
Full A/BF/BE close exactly. Every saved path/event/cost is independently
replayed, including all original DELETE/root-repeat gaps. Erase11: exact
six-key/core11 period, not full/erased equality. No fixed f5/f6 input is invented.

U: rotate after actual156, the last genuine full KEEP. Prefix N+N[:71]
reaches its actual start; interval157..241 contains all H_U endpoints.
This rotation is a new source construction, NOT permission to recut an
existing normalized receipt. Original cd6_allocator.realize_aligned_period
explicitly requires caller-certified cut legality. Our all-cut profile
theorem applies to ANY ACTUALLY supplied legal cut; it does not authorize it.

The critical bad triple recurs in every returning N/U copy. On a legally
cut period containing at least two actual copies, at most one such packet
can cross the seam, so another is wholly interior. A legal cut cannot
remove this local source obstruction by discarding events. Copies are real
original operations, not donors borrowed from a symbolic adjacent period.

W uses D_leaf, U uses E+2; at common B endpoints both values are3. Thus
signed switch correction is exactly zero, and within U the explicit
Delta(2-b) bridge to original rho remains. Original nonidentity G=-1/R=0
corrections and p bits on older histories are untouched. These new words
contain no imported H1/Q6 G/R block to suppress. Reflection and external-
gap substitution preserve actual operation types/event ordinals and the
specified receipts; no old fixed-chart representative is substituted.
''')
doc('HELPER_REPAYMENT_ARCHITECTURE_VERDICT.md','''# OUTCOME E applies to the named predecessor architecture

The same earlier-source repayment rule used with an extremal guard is
FALSE without that guard: a reachable closed triple has Hj=Hp=He=1 and
sum sigma_E=-1. This refutes both the guard-free cost-forcing lemma and
its universal predecessor/triple repayment consequence. A choice of raw
or normalized owners cannot change a source cost/degree counterexample.

The response was NOT a local exception in E. Actual forward return packets
yield a complete restricted signed source comparison; reset synchronization
and matched boundary charts prove an arbitrary mixed returning family.
Helper-only balances can still be-4m. Independent H is extended to actual
normalized owners only through explicit retirement/eligibility/profile laws.

A tempting first-root-return falsifier was INVALID in this domain: actual
KEEP7 at that point follows RLR and loses core label6. Its failed control
is not promoted to a source refutation. The low-side source barrier leaves
first-return repayment as a precise, viable OPEN theorem. No claim that
all possible NH30 architectures or Universal Coarse-Double are false follows.
''')
doc('ADVERSARIAL_SOURCE_CONTROLS.md','''# Controls, failures and honest verification levels

Old -1 helper, W19958/58/Pempty, W459 false partition/hybrid and V^mW are
kept literally. No old source is rerun. New signed claims reuse accepted
rows and do not contradict negative helper aggregates. C29 extremal proof
retains its guard; new triple lies outside it. Old owners/fE/CD6 are unchanged.

source1 recorded two exact A preparations, neither fully shallow; PASS
means that bounded diagnostic completed, NOT NH30 was proved. source2 found
a harmless Qj1 form and failed an incorrect expected total; it is FAILED.
The critical Qj2 construction in source3 is the distinct-audited source.
source4's apparent first-root-return counterexample failed its SS premise.
source5/independent2 verify RLR/core13->12, so it is EXCLUDED, not a counter.
No source4 symbolic embedding word/certificate was produced or used.

The main independent checker rejects duplicate donor, adjacent-copy donor
and moved natural owner corruptions. It verifies exact N source/closure,
complete forward comparison, max-E bank, rotated source identities and
cut templates. Cross resets use ONLY26 new A-only operations per producer/
checker; other identical suffixes are reused by deterministic source proof.

Unequal boundary states were recorded before the reset bridge was derived;
equal core size was never treated as state equality. No new proof assumes
raw f6 consumption equals normalized ownership. The profile<=9/eligibility
hypotheses remain explicit. Arity3 examples and the nine necessary count
classes are not generalized to all support or arbitrary A ancestry.
''')
doc('IAGS_PROOF_TREE.md','''# IAGS recursive closure and reopened parent

Freeze NH30: unchanged inherited signed/physical/normalized all-helper target.
Inherit C29 exact identities/source scopes, C14 source constancy and CD6.
Recurse critical predecessor Box: actual Qj1 is harmless; Qj2,k3=1 is the
remaining zero-transfer. New source lemma realizes it in a closed period.
Close negative result: guard-free predecessor/triple rule REFUTED.

Alter sufficient route: include actual successor recovery rather than
postulate a deeper predecessor. New forward packet includes helper-1 and
actual q1 spare. Reconstruct complete U source partition and repeated-word
induction. Close proper family; parent NH30 still OPEN.

Recurse owner Box: target literal normalized successes; conditions actual
map plus source eligibility and profile; inheritance total-H exchange;
bridge B_extended<=B_H+2B_a. Close conditional theorem at B_a<=9 only.

Recurse mixed-boundary Box: initially A states unequal. New ordered reset
lemma/cross checks synchronize suffixes; source costs telescope and B-state
chart values match3. Close arbitrary cyclic W0/W1/U source/comparison family.

Test alternative first-root-return rule: apparent negative edge has strict
core loss and is source-invalid. Reopen rule as NOT refuted. New low-side
barrier forces first upper11/13 and bounds low signed debt by1. Missing
upper-phase repayment through7 is the exact next Box. It is mathematical,
not 'the current attempt ended' or a CPU explanation. Global NH30/Gate U
cannot be reconstructed until that and the remaining source/owner classes
are actually closed.
''')
doc('C31_NORMALIZED_SIGNED_COMPOSITION_HANDOFF.md','''# GLOBAL COMPOSITION BLOCKED — FIRST-RETURN SOURCE BOX OPEN

Export the exact predecessor refutation, complete forward returning U
family, reset-synchronized mixed W0/W1/U source/comparison theorem and
conditional actual-normalized-owner theorem. These are proper results,
not complete NH30 or all E_r.

Next Box NH30-FR3:
Target: for the actual critical Qj2 zero predecessor, helper h of profile
H1,Q2,beta1,z1,degree3 high rootY, followed by an H1 binary comb, prove
sum sigma_E from h through the FIRST subsequent genuine full KEEP of Y
is nonnegative, or give a genuine closed-core13 countercertificate.
Begin with the physical frame NH30-C (Y7,R11,x5,Z13), allowing arbitrary
ordered gap populations, actual A-only operations and finite source length.
Conditions: original reachable closed source, actual shallow prefix and
original signed costs/period. Do not force any future A depth.
Inheritance: exact negative triple, core constancy, parity barrier, low-
phase sigma>=-1 and mandatory first upper11/13. Initial debt at that upper
event is at most2. The immediate7 falsifier is source-invalid.
Ambiguities: uniform upper/return compensation, other physical frames and
shared return intervals; actual normalized eligibility/storage if funded.
Bridge: one valid first-return signed theorem would repay this critical
arity3 component. It would not alone prove collective disjointness,
alpha4/5, two-ternary helpers, large-profile owners or arbitrary support.

Closed CD6/M3 may NOT simply be applied to an open six-target suffix with
dirty initial state and an inactive marked7. Such a reduction needs an
explicit source boundary/debt correspondence; inventing it would be circular.
After this Box, prove a source partition/noncollision theorem and the exact
normalized old-owner profile/eligibility interface before global assembly.
''')
doc('GATE_U_SOURCE_DEPENDENCY_STATUS.md','''# Conditional Gate U after Campaign30

Original I(r) supplies a specified local source-seed or signed packet
license with own/common maps, source periods, eligibility and Bank25.
Accepted theorem remains I(r-1)+E_r=>I(r); accepted I(6)/CD6 not reopened.

|E_r clause|Status after C30|
|---|---|
|1 Actual erased reachability/normalization, same A events, recurrence/cut, fixed fE|Basic correspondence accepted. New N/U and mixed family have exact A/BF/BE return; no arbitrary original f5/cut selector fabricated.|
|2 Independently source-derived full license A/B|New proper nonextremal and mixed returning families complete; all-source/nonextremal arity4/5, two-ternary and arbitrary-r source license OPEN.|
|3 Common pairing,E-only retirement, eligibility, actual cuts, Bank25, old values|Conditional owner theorem for actual supplied normalized profile<=9; general effective/exterior maps, extra reservations and legal transport remain OPEN.|

No all-r E_r is established. G-block-1 compensation, exterior F-only classes,
other core/arrival types, nonidentity flip interactions outside the stated
words, anonymous A ancestors and support-dependent r-4 debt/storage remain
at their previous OPEN/restricted status. A seven-key block theorem does
not overcome the all-r width/carry obstruction. A stronger all-domain I(5)
selector is not inferred from scalar CD5. Campaign31 is not authorized
to treat this conditional export as unconditional signed/physical assembly.
''')
doc('INDEPENDENT_AUDIT_STATUS.md',f'''# Exact scope of distinct checks

independent_audit.json: PASS, original85-operation prefix/period, all A/BF/BE
rotations, full core13/erased core11, all costs and exact triple closure;
critical sigma-1 packet; forward signed partition/full H; raw working9,
aligned profile3 and cyclic cut templates. It uses344 source queries.

independent_source_exclusion_audit.json: PASS, only the NEW immediate7
transition and six paths,9 queries; strict loss of core label6. Completed
N source is reused, not rerun. First-return theorem itself is NOT audited
as proved. independent_mixed_reset_audit.json: PASS, two26-operation-total
A-only resets and static source/comparison interfaces; all other accepted
suffix states are identical and reused. The arbitrary mixed-word theorem
uses the written reset/chart/endpoint inductions, not finite word samples.

All checks are distinct implementations operated by the SAME research
agent, not external peer review or a formal proof assistant. New universal
manuscripts, including the low-side induction, have no external independent
certification; no SEALED label is used. No actual unsupplied normalized
f5/f6 receipt is claimed. That interface is a conditional proof.

Every failed diagnostic, child/controller cost and query is retained.
No audit has been disguised as a producer replay or taken outside its
controller. Cumulative symbolic/audit CPU is{groups['symbolic']}/240 and
{groups['independent']}/600. Exact publication resources follow below.
''')

gate_rows=[('1 Source class','RECONSTRUCTED','one-high-arity priority and explicit nonextremal meaning; no source exception'),
('2 Signed identity','PROVED','original rho, intrinsic E, explicit hybrid chart bridge'),('3 Old -1 control','PRESERVED','never predicts helper-only nonnegativity'),
('4 Source repayment','RESTRICTED / NAMED RULE REFUTED','forward template family; general first-return law open'),
('5 Helper cost/debt','EXACT ON PROVED FAMILIES','all actual helper/recovery/reset costs retained'),('6 Resource license','CONDITIONAL GLOBALLY','physical comparer explicit; actual old eligibility/retirement still needed'),
('7 Frozen owners','UNCHANGED; EXTENSION CONDITIONAL','no historical map edited; supplied normalized a preserved under NH30-O'),
('8 Normalized f6','PARTIAL','no raw substitution; actual profile<=9 plus original license'),('9 Bank25','PROVED AT STATED SCOPE','raw17 and effective24 under actual owner hypotheses'),
('10 Arbitrary collections','PROPER FAMILY','all cyclic W0/W1/U words; arbitrary overlapping helper intervals open'),
('11 Extremal composition','RESTRICTED PROVED','reset bridge, exact cost correction and matching chart boundary3'),
('12 Charts/arity/support','EXPLICIT RESTRICTED','reflected/gap/cut lifting; examples alpha3/r7, necessary alpha<=5'),
('13 Source uniformity','PROPER CLASSES ONLY','symbolic returning-word/reset/low-side inductions'),
('14 Gate U discharge','PARTIAL E_r2/E_r3 COMPONENTS','not all-source or all-r'),('15 Remaining','OPEN','first-return law, alpha4/5/two-ternary, profiles>9/eligibility, all-r')]
table='\n'.join(['|NH30 gate|Status|Exact scope/gap|','|---|---|---|']+[f'|{a}|{b}|{c}|' for a,b,c in gate_rows])
doc('FINAL_VERDICT.md',f'''# OUTCOME E — proposed predecessor architecture refuted

The exact reachable85-operation source N refutes the guard-free source
claim Hj>=2 and the universal three-macro E repayment rule. At actual
117,118,119 all H1, with sigma0,-1,0. A/BF/BE close exactly; all source
states/events were checked by a distinct implementation. This is NOT a
Coarse-Double counterexample and does NOT refute all NH30 mechanisms.

Further positive results (A-L scope): a genuine four-macro forward recovery
packet pays the helper with its real q1 spare; all U^m have complete signed
comparison and physical independent H. An actual reset bridge then proves
arbitrary cyclic mixtures of C29 extremal W0/W1 and new U, with correctly
matched boundary charts. Local comparison profile3, all-cut profile6, raw
working bound17. Any ACTUAL supplied normalized effective map with profile
<=9 and its original eligibility/retirement/transport license extends without
changing an old value, with Bank24. No arbitrary normalized profile bound
or cached raw receipt is invented. Historical owners and CD6 stay unchanged.

The apparent immediate-return7 falsifier loses core label6 and cannot occur
in a closed core13 source. A new uniform low-side barrier forces first upper
11/13 and bounds low-phase sigma below by-1. It does NOT yet repay the
upper phase through first root7 return. That is the precise next source Box.

{table}

Principal NH30 and MC29 remain OPEN. GLOBAL COMPOSITION BLOCKED — EXACT
FIRST-RETURN SOURCE BOX OPEN. Step3, Universal CD and Dynamic Optimality
are OPEN. This is a mathematical source/owner gap, not an assertion that
the current proof attempt or CPU allowance has ended.

Branch `{e['branch']}`, HEAD `{e['head']}`, tracked tree clean; all
{len(dep['pins'])} inherited local pins match. CPU{total}/7200; symbolic
{groups['symbolic']}/240; audit{groups['independent']}/600. Queries
{qtotal}/2000000, remaining{2000000-qtotal}. No cap reset/extension.
''')
doc('CHECKPOINT.md',f'''# C30 continuation — exact rule refuted, proper mixed theorem retained

Read FINAL_VERDICT, CRITICAL_PREDECESSOR_AND_FORWARD_RETURN,
EXTREMAL_NONEXTREMAL_GLOBAL_COMPATIBILITY, NORMALIZED_SHALLOW_OWNER_INTERFACE,
LOW_SIDE_SOURCE_BARRIER and the three distinct receipts. Do not rerun old
W199/W459/C29 or accepted N/reset audits. No remaining donor request exists
on a historical fully funded fixture; new H is a separate comparison.

New concrete source N85: prefix N from common T; I86..170 closes A/BF/BE,
full core13/erased core11, A109,QF66,QE42. Triple117..119 sigma-1 with all
H1. Forward packet118..121 sigma0 uses real(120,1,1) for comb(119,3).
U is its actual rotation after lastKEEP156, interval157..241. Repetition
has helper-only-4m, complete signed60m, independent profile3/all-cut6.

All cyclic W0/W1/U mixtures have a reset-synchronized source theorem:
unequal A endpoints, EXACT common B/BE, same original reset13..1. Costs
158n0+159n1+109nU telescope correctly. W chart D_leaf and U chart E+2
agree3 at every boundary; no old chart normalization restored. Raw bound17.
Actual normalized owner theorem needs original eligibility/retirement/cut
license AND effective profile<=9, then Bank24. Do not infer either premise.

Smallest next Box NH30-FR3: take the actual critical zero Qj2 predecessor,
H1/Q2/beta1/z1 degree3-root helper followed by an H1 comb. At the specific
NH30-C physical B frame and its actual A shallow prefix, prove the signed
sum from that helper to FIRST genuine return of its old marked root7 is
nonnegative, or give a valid closed-core13 counterexample. Arbitrary low
phase and original DELETEs/private gaps must be retained. First return
exists by the original marked support/closed source, not by a future-depth
assumption. Immediate7 is RLR and loses6; it is excluded. First upper
event must11/13 and at most2 comparison-debt units arrive there. The
upper-phase/return sign and later collective owner bridge are still OPEN.

Do not apply closed CD6 to an open dirty six-target segment without the
missing boundary/source bridge. Other physical frames, alpha4/5, k3=2,
larger owner profiles, exterior receipts and all-r support remain parent
obligations even if NH30-FR3 closes. Global C31 assembly is NOT ready.

Use run_phase2 with cumulative entry/receipts; version aliases share the
same caps and every earlier run is subtracted. CPU{total}/7200, symbolic
{groups['symbolic']}/240, audit{groups['independent']}/600. Conservative
queries{qtotal}/2000000 leave{2000000-qtotal}, unchanged reserves and other
caps. Branch `{e['branch']}`, HEAD `{e['head']}`. Preserve failed scripts:
source2's incorrect expected total and source4's invalid SS premise.
''')

resources={'status':'CUMULATIVE_NO_RESET','prior_uniform_CPU':e['prior_uniform_CPU'],'cumulative_CPU':total,'global_cap':7200,'global_remaining':7200-total,
    'cumulative_group_CPU':groups,'group_caps':e['group_caps'],'group_remaining':{k:e['group_caps'][k]-groups[k] for k in groups},'phases':phases,
    'new_C30_source_queries':queries,'conservative_all_queries':qtotal,'query_limit':2000000,'conservative_remaining_queries':2000000-qtotal,
    'all_failed_successful_child_controller_charges_retained':True,'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,
    'memory_limit_bytes':32*1024**3,'wall_limit_hours':12,'global_reserve':5,'controller_reserve':1,
    'resource_authorization':'Inherit explicit240/600 and7200 caps; query cap2M cumulative; no extension or reset.',
    'metadata_CPU_excluded_under_inherited_convention':{'entry_checkpoint':e['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()},
    'outcome':'E — named predecessor mechanism refuted; A-L positive source/conditional owner theorems','principal_NH30_closed':False,'Gate_U':'OPEN'}
out('resources_checkpoint.json',resources)
out('C30_RESULT_CERTIFICATE.json',{'outcome':'E','named_rule_refuted':'guard-free Hj>=2 / universal earlier triple E repayment','counter_source_length':85,'counter_interval':[86,170],
    'critical_sigma_E':-1,'source_and_forward_distinct_audit':'PASS','restricted_positive_results':['forward recovery U^m','reset-synchronized arbitrary cyclic W0/W1/U source/comparison','actual normalized profile<=9 licensed extension','low-side source barrier/debt bound'],
    'raw_working_bound':17,'independent_profile_all_cuts':6,'normalized_effective_profile_hypothesis':9,'conditional_extended_bound':24,
    'first_return_falsifier':'SOURCE-INVALID core loss, not a counterexample','first_return_repayment':'OPEN',
    'principal_NH30':'OPEN','Gate_U':'OPEN','Coarse_Double_counterexample':False,'external_audit':False,'branch':e['branch'],'HEAD':e['head']})
out('campaign_manifest.json',{'status':'APPEND_ONLY_C30_PUBLICATION','branch':e['branch'],'HEAD':e['head'],'tracked_tree_clean':True,'inherited_local_matches':len(dep['pins']),
    'files':[{'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f)} for f in sorted(B.iterdir()) if f.is_file() and f.name not in ('campaign_manifest.json','publication_exit.json','publication_seal.json')],
    'principal_theorem_not_promoted':True,'no_historical_artifact_modified':True})
out('publication_exit.json',{'status':'PASS_METADATA_PUBLICATION','whole_process_CPU_seconds':time.process_time(),'semantic_calls':0})
out('publication_seal.json',{'status':'HASHED_PUBLICATION_NOT_A_THEOREM_SEAL','manifest_sha256':sha(B/'campaign_manifest.json'),'publication_exit_sha256':sha(B/'publication_exit.json')})
print(json.dumps({'status':'C30_PUBLISHED','outcome':'E','NH30':'OPEN','CPU':total,'groups':groups,'queries':qtotal,'queries_remaining':2000000-qtotal,'pins':len(dep['pins'])}),flush=True)
