"""Explicit CPU renewal, audit first, established two-million query cap."""
import json,hashlib,shutil,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_POP4_RISK05'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,s):
    if name.endswith('.py'):compile(s,str(BASE/name),'exec')
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(s)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

prior=read(OLD/'certificate.json');run=read(OLD/'run_result.json')
assert prior['total4_vectors_covered']==654 and prior['total4_vectors_remaining']==61
assert len(run['completed_signatures'])==16 and run['failure']['phase']=='audit'
assert run['renewed_CPU_charged']==7195.28125
targets=read(OLD/'targets.json')['canonical_signatures'][16:]
first=[1,0,0,0,0,1,1,0,1,0]
assert targets[0]==first and len(targets)==33 and sum(s==s[::-1] for s in targets)==5
assert len({tuple(v) for s in targets for v in (s,s[::-1])})==61
write(BASE/'targets.json',{'canonical_signatures':targets,'source_batches':[targets],'remaining_original_signatures':61,'fixed_cases':5,'query_cap':2000000,'old_order_preserved':True})
source('PRE_EXECUTION.md','''# M3_POP4_RISK06: renewed allowance, interrupted audit first

The human explicitly renews the finite CPU allowance and authorizes the
remaining61 total-four signatures, STARTING WITH the interrupted audit
e0+e5+e6+e8. Fresh finite allowance7200 CPU seconds, starting0. All old
charges7200,7195.21875,7195.25,7195.28125, historical UNKNOWN reports and
old files remain immutable. The last charge includes RISK04 plus RISK05;
do not double count its carried4718.984375 portion. Inherited12h unchanged.

Preserve established caps:2m canonical queries for enumeration AND
independent audit;120/300/120 CPU seconds; live records<2m,DAG<4m,
edges<5m,memory<=32GiB. Reserve5 CPU seconds near the renewed7200 boundary;
charge whole child-process CPU through finally and parent metadata CPU.
Stop FIRST new cap/UNKNOWN, premise/template failure or allowance boundary.
No skipped cases, failed-phase split, automatic retry or allowance reset.

One principal theorem/mechanism: one J in[-2,0],J<=-psi per new sector,
W(O)=J-5chi8,W(M)=-5chi8; original closed mixed walks>=0,finite walks>=-7.
Full M3, larger populations and Stage04 remain open.
Gate1: total-four only,33 representatives/61 original vectors, including5
fixed reflections, using already proved risky fibers. Existing654/715
total-four sectors and all completed source/bank/selector/word checks reused.
Gate2: existing complete population-four retained-budget induction, exact
integer recurrence, independent ordered-key/source-address regeneration
and residual checks. Omitted fibers obey w-DeltaJ>=w+psi(Bt)-2>=0.
The two-million query guard is preserved, not raised or a row restriction;
the prior GUARD_PRESERVATION.md argument is reused. No numerical extrapolation,
new state/observable/source constraint/backend or open existence premise.
Gate3: one bounded original-source audit phase<=300 CPU s, registered NOW
for up to33 NEW cases: one negative H1 per passed case, at most4 full
147-O/same-actual127-M mixed cycles and4 helper controls. No old roots
replayed. Checkpoint each accepted new root immediately. All completed
h0/G/middle-helper/DELETE-zeroKEEP/normal-form checks are reused.
Gate4: BEFORE654/715; success deletes exactly new source-complete sectors,
at most61 vectors/7686 mask sectors. Exact coverage, fixed sectors once,
UNKNOWN never PASS. No source-incomplete/failed/unstarted sector promoted.

FIRST mathematical action: copy by hash ONLY relation.json,potential.json,
build_status.json,construction.json for e0+e5+e6+e8. Reuse completed
enumeration and construction; do not repeat them. Run a NEW FULL independent
audit with120 CPU s/2m query caps; do not resume lost partial in-memory state.
The explicit human renewal authorizes that interrupted audit retry only;
no new failed phase is automatically retried.

R1 exact original theorem/full-state closure. R2 original Stage11F two
sorts,SAME actual midpoint,independent OM/MO private scopes,q and weights.
R3 frozen(mu,b,alpha,sigma),alpha7 depth2,T266,Bank25=25,architecture and
currently established2m-query/other caps. R4 exact evidence/provenance/status.
Preserve h0 actual0/declared18/q9/weight-3 and independent free fiber v.
Fixed sectors use full direct tables, NO J mirror-invariance assumption.
Nonfixed reflection reuses proved low-image/selector/B-bank transfer.
G literal slot0/current-child reads, unfolded F occurrences and every
private count/bill branch remain included. No graph-state quotient.

All new writes only HERE, Python -B. No installs/original source/tests/
configuration/Git changes, Stage04 or full-M3/negative-cycle promotion.
Pin entry-baseline files and verify all their bytes/HEAD/tracked tree at end.
Concurrent U4 additions may be recorded separately, never modified or used
as M3 mathematical premises. All prior files read-only. No subagents.
''')
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    source(name,(OLD/name).read_text().replace('M3_POP4_RISK05','M3_POP4_RISK06'))
for name in ('SOURCE_LIFT.md','REPRESENTATION_PROOF.md','GUARD_PRESERVATION.md'):source(name,(OLD/name).read_text())
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK05','M3_POP4_RISK06').replace('M3_POP4_RISK04/certificate.json','M3_POP4_RISK05/certificate.json').replace('==91','==32')
source('entry.py',entry)
folder=BASE/('s'+''.join(map(str,first)));folder.mkdir()
files=[]
for name in ('relation.json','potential.json','build_status.json','construction.json'):
    src=OLD/folder.name/name;dst=folder/name;shutil.copyfile(src,dst);assert sha(src)==sha(dst)
    files.append({'source':src.as_posix(),'copy':dst.as_posix(),'sha256':sha(src)})
write(BASE/'reused_candidate.json',{'sigma':first,'files':files,'completed_phases_reused':2,'partial_audit_reused':False})
combined=(OLD/'combined_certificate.py').read_text()
needle="        override5={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK05/certification_run.json').read_text())['source_certified_signatures']}"
assert needle in combined
combined=combined.replace(needle,"        renewal6={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK06/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in renewal6 or tuple(reversed(sig)) in renewal6:return 'renewal6_population4'\n"+needle)
needle="        elif kind=='override5_population4':"
combined=combined.replace(needle,"        elif kind=='renewal6_population4':\n            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK06'));m=module('renewal6_population4_bank',REBOOT/'M3_POP4_RISK06/certified_decoder.py');self.decoder=m.PopulationFourCertificate()\n"+needle)
source('combined_certificate.py',combined)
verify=(OLD/'verify_combination.py').read_text()
verify=verify.replace('    assert len(old)==3528',"    prior5=read(BASE.parent/'M3_POP4_RISK05/combination_check.json')['new_certified_signatures']\n    for s in prior5:assert P.scope({'sigma':s})=='override5_population4';old.add(tuple(s))\n    assert len(old)==3560")
verify=verify.replace("P.scope({'sigma':s})=='override5_population4'\n    remaining","P.scope({'sigma':s})=='renewal6_population4'\n    remaining")
verify=verify.replace('93','61').replace('622','654').replace('3528','3560')
source('verify_combination.py',verify)
fin=(OLD/'finalize.py').read_text().replace('93','61').replace('622','654').replace('3528','3560')
fin=fin.replace("run['reused_completed_old_phases']==0","run['reused_completed_old_phases']==2")
fin=fin.replace("for name in ('M3_POP4_RISK04/certificate.json'","for name in ('M3_POP4_RISK05/certificate.json','M3_POP4_RISK05/final_manifest.json','M3_POP4_RISK05/combination_check.json','M3_POP4_RISK05/SOURCE_LIFT.md','M3_POP4_RISK05/GUARD_PRESERVATION.md','M3_POP4_RISK04/certificate.json'")
fin=fin.replace("'authorized_old_capped_enumeration_retried':True,'complete_old_phases_replayed':0,'query_guard_user_exception':[1000000,2000000]","'authorized_old_interrupted_audit_retried':True,'complete_old_phases_replayed':0,'complete_enumeration_and_construction_reused':True,'query_guard_preserved':2000000")
fin=fin.replace("'old_finite_charges_unchanged':[7200,7195.21875,7195.25]","'old_finite_charges_unchanged':[7200,7195.21875,7195.25,7195.28125]")
fin=fin.replace("'old_capped_case_completed':done[0]==[1,1,0,0,1,0,0,0,1,0]","'interrupted_old_audit_completed':done[0]==[1,0,0,0,0,1,1,0,1,0]")
fin=fin.replace("'prior_current_finite_CPU':4718.984375,'additional_finite_CPU':run['additional_finite_CPU_charged']","'fresh_finite_CPU_allowance':7200,'prior_current_finite_CPU':0,'additional_finite_CPU':run['additional_finite_CPU_charged'],'per_phase_caps_preserved_from_RISK05':True")
fin=fin.replace('The user explicitly authorized exceeding the former one-million-query guard. The capped e0+e1+e4+e8 enumeration was retried FIRST under a two-million-query guard. No complete old phase was repeated; no complete relation had been saved for the failed case.','The interrupted audit e0+e5+e6+e8 was completed FIRST under the existing120 CPU s/two-million-query caps. Its complete relation,potential,build and construction reports were reused by hash; no complete old phase was repeated and no partial audit state was reused.')
fin=fin.replace('Existing finite allowance:7200 CPU seconds; prior charge4718.984375 retained, cumulative charge','Fresh explicitly renewed finite allowance:7200 CPU seconds; charged')
fin=fin.replace('User resource exception:2m canonical queries in enumeration and independent audit. Other caps stay120/300/120 CPU seconds,2m live states,4m DAG nodes,5m edges,32GiB; original12h ceiling unchanged. The CPU allowance was not reset.','Established caps preserved:2m canonical queries,120/300/120 CPU seconds,2m live states,4m DAG nodes,5m edges,32GiB; original12h ceiling unchanged. Old CPU ledgers remain immutable; the human explicitly renewed this finite allowance.')
source('finalize.py',fin)
print(json.dumps({'prepared':True,'canonical_cases':33,'original_vectors':61,'fixed_sectors':5,'query_cap':2000000,'fresh_CPU':7200,'first':first}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
