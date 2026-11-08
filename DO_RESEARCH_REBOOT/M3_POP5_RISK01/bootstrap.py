"""Population-five specialization; unchanged experimental guards and algorithms."""
import json,hashlib,subprocess,sys
from pathlib import Path
from itertools import combinations_with_replacement
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_POP4_RISK07'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,s):
    if name.endswith('.py'):compile(s,str(BASE/name),'exec')
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(s)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()
prior=read(OLD/'certificate.json')
assert prior['total4_vectors_covered']==715 and prior['total4_vectors_remaining']==0
assert prior['cumulative_whole_process_finite_CPU_charged']==4055.96875
all5=[tuple(xs.count(i) for i in range(10)) for xs in combinations_with_replacement(range(10),5)]
multi=[s for s in all5 if sum(n>0 for n in s)>1]
def order(s):
    occupied=[i for i,n in enumerate(s) if n]
    return (occupied[-1]-occupied[0],len(occupied),occupied[0],tuple(-n for n in s))
targets=sorted({max(s,s[::-1]) for s in multi},key=order)
assert len(all5)==2002 and len(multi)==1992 and len(targets)==996
assert not any(s==s[::-1] for s in targets)
batches=[targets[i:i+50] for i in range(0,len(targets),50)]
write(BASE/'targets.json',{'total_population':5,'all_total5_signature_count':2002,'already_certified_single_support_vectors':10,'new_original_signatures':multi,'canonical_signatures':targets,'signature_count':1992,'canonical_count':996,'self_reflecting_cases':0,'order':'increasing occupied-gap span, support size, minimum occupied gap, then descending vector','source_batches':batches,'source_batch_size':50,'source_per_phase_CPU_cap':300,'maximum_registered_source_phases':20,'prior_current_finite_CPU':4055.96875,'finite_CPU_ceiling':7200,'query_cap':2000000,'CPU_caps':{'prefix_dp':120,'construct':300,'audit':300}})
source('PRE_EXECUTION.md','''# Population-five campaign: written gates before execution

Authorized scope is total-five multi-support only. The prior total-four
theorem is complete715/715; all old signatures, proofs, source controls,
selector/78-word audits and B-bank checks are reused unchanged. The ten
single-support total-five vectors are already certified and NOT rerun.

Gate1 - strictly smaller:1992 new original vectors/996 reflection pairs,
against the full unresolved multi-population M3 problem. This is a fixed
finite-population extension, not an all-horizon existence reformulation.
Odd total5 implies no fixed reflection sectors. The fixed prelisted order
is increasing support span, support size, minimum gap, descending vector.
Gate2 - concrete mechanism: the existing budget-consuming structural
induction applies at5 (SOURCE_LIFT.md); the selector identity
w-DeltaJ>=w+psi(Bt)-2>=0 is population-independent. Construct the integer
J in[-2,0],J<=-psi using the SAME recurrence; independently regenerate
ordered-key/source-address families and verify EVERY required residual.
No feasibility or source constraint is inferred merely from n4 fits.
Gate3 - one principal theorem/mechanism: new passed sectors have
W(O)=J-5chi8,W(M)=-5chi8, original closed mixed walks>=0, finite walks>=-7.
One bounded source-audit workflow, with fixed disjoint phases registered
NOW in targets.json, at most50 canonical cases/300 CPU seconds each,
at most4 mixed cycles and4 helper controls per phase. At most20 phases,
6000 source CPU seconds worst-case; only the completed finite prefix is
audited. These are not subdivisions of a failed phase. Stop first source
cap/failure; do not retry or split. No second independent open theorem.
Gate4 - real deletion: BEFORE0/1992 total-five multi-support certified.
Each NEW finite-audited AND source-complete pair deletes two original
sigma obligations, all126 legal masks, both regions wherever realizable.
Unstarted, capped, failed or source-incomplete sectors stay excluded.
Success is restricted to those pairs, never full M3 or Dynamic Optimality.

The finite CPU ceiling remains7200. Prior4055.96875 is retained; only
3144.03125 remains. No renewal/reset is implied by this continuation.
Reserve5 seconds; charge whole child-process CPU through finally plus
parent metadata CPU. Enumeration120/construction300/independent-audit300
CPU seconds, canonical queries2m in enumeration/audit, live records<2m,
DAG nodes<4m, edges<5m, memory<=32GiB, inherited12h ceiling unchanged.
Stop FIRST new cap/UNKNOWN, premise/template failure or allowance boundary.
No later finite case, failed-phase split, retry, backend/cap change.
After that stop, only finish the pre-registered source checks for completed
finite sectors, combine those actually source-complete, and package.

R1 exact original target/full-state closure. R2 original Stage11F two sorts,
SAME actual127-M, independent OM/MO private witnesses, original q/weights.
R3 frozen(mu,b,alpha,sigma),alpha7 depth2,T266,Bank25=25,architecture and
all current caps. R4 exact evidence/provenance/status. Corrected h0 stays
actual0/declared18/q9/weight-3, independent free v. Preserve literal-slot0
G/current-child observations, unfolded actual F occurrences, every private
count/bill branch, and all147 O/127 M closure coordinates. No graph quotient.

All new writes only HERE, Python -B. No installs, source/tests/config/Git
changes, old research overwrites, subagents, Stage04 or full-M3 promotion.
Pin old files before mathematics and verify bytes/HEAD/tracked tree at end.
Concurrent U4 additions are recorded separately and never M3 evidence.
''')
source('SOURCE_LIFT.md','''# Population-five source lift

Status: established structural coverage lemma, conditional only on the
explicitly reused PROVED dependencies; no new potential feasibility claim
until a new sector finishes construction, independent audit and source checks.

The retained-budget induction in M3_POP4_RISK01/SOURCE_LIFT.md is valid for
each fixed finite budget. Here specialize to sigma of total5. For any
original private witness, protect exactly the same source-address union
and real operands as before. Assign every retained anonymous occurrence its
actual gap color; conservation/nonnegativity gives componentwise counts<=sigma.
Hidden unretained nodes need no selected count. The outer product over all
counts<=sigma includes this assignment. Distinct unfolded F occurrences
retain distinct actual source addresses; no shared private completion or
literal rank-room is imposed.

Induct on the protected prefix. At a Score pivot k, choose that actual
pivot, split retained counts between children and restrict gaps<=k/>k.
At an anonymous pivot in gap g, consume ONE g count, then split the
remaining counts; Score intervals are belowg/atleastg and anonymous gap
sets<=g/>=g. Equal-gap nodes may occur on either side. These child calls
have strictly smaller protected prefixes and smaller remaining counts
when an anonymous pivot is consumed. At an unobserved cut, choose P with
zero selected count. At the G boundary, use the same required empty-Score
interval and original-slot0/current-child observations. These are exactly
the unchanged PrefixDP productions. No induction step depends on total4;
the sole numerical extension is the input vector of total5. The independent
ordered-key checker supplies9 Score keys plus at most5 actual gap keys,
so checks the same branch classification without importing this DP.

The population-independent omitted-fiber inequality is
w-J(t)+J(s)>=w+psi(coreB(t))-2>=0 for J in[-2,-psi]. Reuse the exact risky
root/terminal classification and all78 word/address proofs. H1, outer-gap
H2 Gamma1, Gamma0 preterminal debt and all other LOW charge/credit laws are
unchanged. A helper can be ANY actual node in an occupied outer gap;
zero KEEP follows the same charged actual root, including DELETE. Do not
fuse H2 into H1 or substitute macro-entry debt. B kernels depend on gap
occupancy, not its positive multiplicity. The two occupied outer directions
and every private color/count/bill branch are included. Weak LE bills are
forgotten only in the established source superrelation, never tightened.

For each passed representative, one integer J constrains the SAME raw
alpha/coreB across all retained branches; unlisted alpha defaults to-psi.
Raw term deduplication uses the established endpoint/H/target/weight identity.
No private choice enters J. Reflection acts on the actual LOW image and
uses pinned selector/kernel/debt equivariance; it does not assert reflection
of original weak LE assignments or HIGH sentinels. Total5 has no fixed
reflection vector, since every symmetric ten-coordinate vector has even sum.

Only complete independent grammar/option/residual audits plus the new
original-source controls permit promotion. Actual nonvacuity fixtures are
controls, not the universal coverage proof. With the inherited universal
HIGH law and corrected h0 entry-3, set W(O)=J-5chi8,W(M)=-5chi8. Preserve
independent v, independent OM/MO scopes, original q/weights and same actual
127-M. Original walks close on all147 O/all127 M coordinates. The potential
is defined on full original states; no vertex quotient is performed.
Each original leg has w>=DeltaW. W in[-7,0] gives finite walks>=-7 and
fully closed mixed walks>=0. Original edges conserve sigma/mu, so sectors
combine. Isolated invalid projections retain the established totalization;
uncertified sigma errors occur BEFORE that totalization.

Dependencies: M3_POP4_RISK01/SOURCE_LIFT.md; M3_POP3_RISK01/REPRESENTATION_PROOF.md,
representation_audit.json and risk_selector.json; M3_UNITPAIR01/B_bank.json;
the pinned inherited original LOW normal forms/HIGH law and h0 correction.
No old lemma/check is rerun. All new signs are proved anew, not extrapolated.
Full M3 and all unpromoted total-five/larger sectors remain OPEN.
''')
for name in ('REPRESENTATION_PROOF.md','GUARD_PRESERVATION.md','AUDIT_CAP_PRESERVATION.md'):source(name,(OLD/name).read_text())
changes=[]
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    s=(OLD/name).read_text();replacements=[('M3_POP4_RISK07','M3_POP5_RISK01')]
    if name in ('candidate_decoder.py','certified_decoder.py'):
        replacements += [('sum(sig)!=4','sum(sig)!=5'),('PopulationFour','PopulationFive'),('population4','population5'),('total4','total5')]
    if name=='construct.py':replacements += [('one four-unit signature','one five-unit signature')]
    if name=='source_audit_batch.py':replacements += [('population4','population5'),('PopulationFour','PopulationFive'),('pop4_','pop5_'),('RENEWED_TOTAL4_SOURCE_BATCH_PASS','TOTAL5_SOURCE_BATCH_PASS')]
    if name=='audit_source_batches.py':replacements += [('RENEWED_TOTAL4_SOURCE_BATCH_PASS','TOTAL5_SOURCE_BATCH_PASS')]
    for a,b in replacements:s=s.replace(a,b)
    source(name,s)
    restored=s
    for a,b in reversed(replacements):restored=restored.replace(b,a)
    assert restored==(OLD/name).read_text(),name
    changes.append({'file':name,'source_sha256':sha(OLD/name),'new_sha256':sha(BASE/name),'exact_replacements':replacements})
write(BASE/'implementation_change_audit.json',{'files':changes,'only_location_population_scope_and_labels_changed':True,'recurrence_grammar_residuals_source_predicates_and_guards_unchanged':True,'CPU_caps':[120,300,300],'query_cap':2000000})
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK07','M3_POP5_RISK01').replace('M3_POP4_RISK06/certificate.json','M3_POP4_RISK07/certificate.json').replace("['new_original_signatures']==54","['new_original_signatures']==7")
source('entry.py',entry)
combined=(OLD/'combined_certificate.py').read_text()
needle="        renewal7={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK07/certification_run.json').read_text())['source_certified_signatures']}"
assert combined.count(needle)==1
combined=combined.replace(needle,"        risk5={tuple(v) for v in json.loads((REBOOT/'M3_POP5_RISK01/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in risk5 or tuple(reversed(sig)) in risk5:return 'risk_population5'\n"+needle)
needle="        elif kind=='renewal7_population4':"
assert combined.count(needle)==1
combined=combined.replace(needle,"        elif kind=='risk_population5':\n            sys.path.insert(0,str(REBOOT/'M3_POP5_RISK01'));m=module('risk_population5_bank',REBOOT/'M3_POP5_RISK01/certified_decoder.py');self.decoder=m.PopulationFiveCertificate()\n"+needle)
source('combined_certificate.py',combined)
print(json.dumps({'prepared':True,'canonical_cases':996,'original_multi_vectors':1992,'prior_finite_CPU_retained':4055.96875,'CPU_left':3144.03125,'first':targets[0],'source_phases_pre_registered':len(batches)}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
