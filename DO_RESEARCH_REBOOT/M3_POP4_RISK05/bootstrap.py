"""Explicit user override of the query guard; all mathematics is unchanged."""
import json,hashlib,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_POP4_RISK04'
PRIOR_CPU=4718.984375
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,s):
    compile(s,str(BASE/name),'exec') if name.endswith('.py') else None
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(s)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

prior=read(OLD/'certificate.json');run=read(OLD/'run_result.json')
assert prior['total4_vectors_covered']==622 and prior['total4_vectors_remaining']==93
assert len(run['completed_signatures'])==47 and run['renewed_CPU_charged']==PRIOR_CPU
targets=read(OLD/'targets.json')['canonical_signatures'][47:]
first=[1,1,0,0,1,0,0,0,1,0]
assert len(targets)==49 and targets[0]==first and sum(s==s[::-1] for s in targets)==5
assert len({tuple(v) for s in targets for v in (s,s[::-1])})==93
write(BASE/'targets.json',{'canonical_signatures':targets,'source_batches':[targets],'remaining_original_signatures':93,'fixed_cases':5,'query_cap':2000000})
source('PRE_EXECUTION.md','''# M3_POP4_RISK05: explicitly authorized query-limit exception

The human says to let enumeration exceed one million if mathematically
harmless. This explicitly overrides ONLY the diagnostic query ceiling and
authorizes retrying the capped enumeration e0+e1+e4+e8. Use a finite
2,000,000-canonical-query ceiling in enumeration AND independent auditing.
The old one-million cap/UNKNOWN and every old file remain immutable.
No old complete matrix, audit or source control is repeated. The failed
partial enumeration saved no complete relation; rerun it fully once.

No CPU renewal was requested. Carry forward 4718.984375 of the existing
7200 finite CPU seconds, leaving 2481.015625; reserve 5 seconds and charge
whole child-process CPU plus parent metadata. All other caps stay:
enumeration 120 CPU s, construction 300, audit 120; live records <2m,
DAG <4m, edges <5m, memory <=32GiB; inherited 12h ceiling unchanged.
Stop FIRST new cap/UNKNOWN, premise/template failure or allowance boundary.
No skipping/retrying later failed cases or automatic new allowance.

One principal theorem/mechanism: J in [-2,0], J<=-psi on new named sectors;
W(O)=J-5chi8, W(M)=-5chi8, original closed mixed walks >=0 and finite
walks >=-7. Full M3 and larger multiple-support totals remain open.
Gate 1: 49 remaining canonical total-four cases / 93 original vectors,
including 5 fixed sectors, only already proved risky fibers. Existing
622 total-four vectors and all source/bank/selector/word checks reused.
Gate 2: unchanged source-complete population-four retained-budget DP,
exact integer construction and independent ordered-key/address audit.
Omitted fibers still obey w-DeltaJ >= w+psi(Bt)-2 >=0. A query cap is a
stopping guard, not a mathematical constraint; see GUARD_PRESERVATION.md.
Gate 3: one mechanism and ONE new source-audit phase, <=300 CPU s, one
new negative H1 per passed case, <=4 full147-O/same127-M mixed cycles,
<=4 helper controls, no old root replay. The preceding source audit used
152.25 CPU s; old plus new <=452.25 is within the already registered600.
Only new source-complete sectors are promoted. Save accepted roots once.
Gate 4: BEFORE622/715 total-four vectors; success deletes precisely new
passed sectors, at most93 vectors/11718 mask sectors. No new assumptions,
observables, source constraints, weights, backend or existence premise.

R1 original theorem/full closure. R2 original Stage11F two sorts, SAME
actual midpoint, independent private OM/MO scopes, q and weights. R3
frozen(mu,b,alpha,sigma), alpha7 depth2,T266,Bank25=25 and architecture;
ONLY its resource query ceiling has the explicit human-authorized exception.
R4 exact evidence/status, UNKNOWN never PASS. Preserve h0 actual0/
declared18/q9/weight-3 and free independent fiber v. Fixed sigma is audited
directly without J symmetry. Nonfixed reflection reuses proved low-image,
selector/B-bank transfer. Original G slot0/current-child reads, unfolded F
occurrences and all private bill branches remain. No state quotient.

All writes only HERE, Python -B; no installs/original source/tests/config/
Git changes, Stage04 or full-M3 promotion. Pin all entry-baseline files;
verify their bytes and tracked HEAD/tree at the end. Concurrent U4 additions
may be recorded separately, never modified or used as M3 proof premises.
No subagents. This exception is recorded, never labelled unchanged caps.
''')
source('GUARD_PRESERVATION.md','''# Query-guard preservation argument

Enumeration's former condition `queries+n>1000000` stops before evaluating
a whole next word family and returns UNKNOWN. It does not filter any row
inside a completed relation. Independent auditing's `queries<=1000000`
conjunct is likewise a resource stop, separate from its residual assertions.
Replace these two resource bounds by2000000. No DP recurrence, grammar,
word transition, private count, source predicate, q, weight, state identity,
potential range or residual inequality changes. Completing more families
adds required constraints rather than removing them.

Certification STILL requires complete enumeration, exact construction,
independent regeneration of every family/option and equality of counts,
all exact residuals nonnegative, inherited source-completeness/omission
proofs and new original-source controls. Every truncation remains UNKNOWN.
Thus a larger guard can permit an additional complete certificate; it
cannot turn an incomplete or invalid mathematical certificate into a pass.
The user authorizes the resource exception; no truth-status upgrade follows
from that authorization alone. All CPU/live-record/DAG/edge/memory guards
remain in force, and the old failed report stays immutable.
''')
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    s=(OLD/name).read_text().replace('M3_POP4_RISK04','M3_POP4_RISK05')
    if name=='prefix_dp.py':
        assert s.count('if queries+n>1000000:')==1;s=s.replace('if queries+n>1000000:','if queries+n>2000000:')
    if name=='audit.py':
        assert s.count('assert queries<=1000000 and')==1;s=s.replace('assert queries<=1000000 and','assert queries<=2000000 and')
    source(name,s)
for name in ('SOURCE_LIFT.md','REPRESENTATION_PROOF.md'):source(name,(OLD/name).read_text())
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK04','M3_POP4_RISK05').replace('M3_POP4_RISK03/certificate.json','M3_POP4_RISK04/certificate.json').replace('==157','==91')
source('entry.py',entry)
write(BASE/'reused_candidate.json',{'sigma':first,'files':[],'complete_old_phases_repeated':0,'partial_enumeration_rerun_authorized':True,
  'old_failure_report':(OLD/'s1100100010/build_status.json').as_posix(),'old_failure_sha256':sha(OLD/'s1100100010/build_status.json')})
combined=(OLD/'combined_certificate.py').read_text()
needle="        renewal4={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK04/certification_run.json').read_text())['source_certified_signatures']}"
assert needle in combined
combined=combined.replace(needle,"        override5={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK05/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in override5 or tuple(reversed(sig)) in override5:return 'override5_population4'\n"+needle)
needle="        elif kind=='renewal4_population4':"
combined=combined.replace(needle,"        elif kind=='override5_population4':\n            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK05'));m=module('override5_population4_bank',REBOOT/'M3_POP4_RISK05/certified_decoder.py');self.decoder=m.PopulationFourCertificate()\n"+needle)
source('combined_certificate.py',combined)
verify=(OLD/'verify_combination.py').read_text()
verify=verify.replace('    assert len(old)==3437',"    prior4=read(BASE.parent/'M3_POP4_RISK04/combination_check.json')['new_certified_signatures']\n    for s in prior4:assert P.scope({'sigma':s})=='renewal4_population4';old.add(tuple(s))\n    assert len(old)==3528")
verify=verify.replace("P.scope({'sigma':s})=='renewal4_population4'\n    remaining","P.scope({'sigma':s})=='override5_population4'\n    remaining")
verify=verify.replace('184','93').replace('531','622').replace('3437','3528')
source('verify_combination.py',verify)
fin=(OLD/'finalize.py').read_text().replace('184','93').replace('531','622').replace('3437','3528')
fin=fin.replace("run['reused_completed_old_phases']==2","run['reused_completed_old_phases']==0").replace('len(sources)<=2','len(sources)<=1')
fin=fin.replace("a['canonical_transition_queries']==d['queries']<=1000000","a['canonical_transition_queries']==d['queries']<=2000000")
fin=fin.replace("for name in ('M3_POP4_RISK03/certificate.json'","for name in ('M3_POP4_RISK04/certificate.json','M3_POP4_RISK04/final_manifest.json','M3_POP4_RISK04/combination_check.json','M3_POP4_RISK04/SOURCE_LIFT.md','M3_POP4_RISK03/certificate.json'")
fin=fin.replace("'authorized_old_incomplete_audit_retried':True,'old_complete_enumeration_and_construction_reused':True,'partial_old_audit_reused':False","'authorized_old_capped_enumeration_retried':True,'complete_old_phases_replayed':0,'query_guard_user_exception':[1000000,2000000]")
fin=fin.replace("'interrupted_old_audit_completed':done[0]==[1,1,0,0,0,1,0,1,0,0]","'old_capped_case_completed':done[0]==[1,1,0,0,1,0,0,0,1,0]")
fin=fin.replace("'R1_R4_preserved':True","'R1_R4_mathematics_preserved_with_user_resource_exception':True")
fin=fin.replace("'per_phase_caps_unchanged':True","'other_per_phase_caps_unchanged':True,'query_cap_old':1000000,'query_cap_user_authorized':2000000,'prior_current_finite_CPU':4718.984375,'additional_finite_CPU':run['additional_finite_CPU_charged']")
fin=fin.replace('The explicitly interrupted audit e0+e1+e5+e7 was completed FIRST. Its complete relation, potential, build and construction reports were reused by hash. No old complete phase was repeated and no partial audit state was reused.','The user explicitly authorized exceeding the former one-million-query guard. The capped e0+e1+e4+e8 enumeration was retried FIRST under a two-million-query guard. No complete old phase was repeated; no complete relation had been saved for the failed case.')
fin=fin.replace('Renewed finite allowance:7200 CPU seconds; charged','Existing finite allowance:7200 CPU seconds; prior charge4718.984375 retained, cumulative charge')
fin=fin.replace('Per-phase mathematical caps remain120/300/120 CPU seconds,1m canonical word queries,2m live states,4m DAG nodes,5m edges,32GiB; original12h ceiling unchanged.','User resource exception:2m canonical queries in enumeration and independent audit. Other caps stay120/300/120 CPU seconds,2m live states,4m DAG nodes,5m edges,32GiB; original12h ceiling unchanged. The CPU allowance was not reset.')
fin=fin.replace('R1-R4,h0,original q/weights','R1-R4 mathematics with explicit query-resource exception,h0,original q/weights')
needle="    assert not[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]"
assert needle in fin
fin=fin.replace(needle,"    additions=[p for p in Path('DO_RESEARCH_REBOOT').rglob('*') if p.is_file() and BASE not in p.parents and p.as_posix() not in old]\n    assert all(p.as_posix().startswith('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/') for p in additions)\n    write(BASE/'concurrent_additions.json',{'not_mathematical_dependencies':True,'files':[{'path':p.as_posix(),'sha256':sha(p)} for p in additions]})")
fin=fin.replace("'writes_confined_here':True}","'writes_confined_here':True,'write_claim_scope':'this campaign only','concurrent_U4_additions':len(additions)}")
fin=fin.replace("'All'+str(len(old))+' old files unchanged; tracked tree clean, HEAD unchanged, all new writes confined here.'","'All '+str(len(old))+' pinned prior files unchanged; tracked tree and HEAD unchanged. This campaign wrote only here; concurrent U4 additions recorded separately.'")
source('finalize.py',fin)
print(json.dumps({'prepared':True,'canonical_cases':49,'original_vectors':93,'query_cap':2000000,'prior_CPU_retained':PRIOR_CPU,'CPU_remaining':7200-PRIOR_CPU,'source_phases':1}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
