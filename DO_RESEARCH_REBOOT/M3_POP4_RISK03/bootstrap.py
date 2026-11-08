"""Prepare one explicitly authorized renewal; old evidence is read-only."""
import json,hashlib,shutil,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'M3_POP4_RISK02'

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,text):
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(text)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

run=read(OLD/'run_result.json');prior=read(OLD/'certificate.json')
assert prior['new_original_signatures']==236 and prior['total4_vectors_remaining']==341
assert len(run['completed_signatures'])==120 and run['failure']['phase']=='construct'
targets=read(OLD/'targets.json')['canonical_signatures'][120:]
first=[1,1,0,0,0,0,2,0,0,0]
assert targets[0]==first and len(targets)==175
assert sum(s==s[::-1] for s in targets)==9
assert len({tuple(v) for s in targets for v in (s,s[::-1])})==341
write(BASE/'targets.json',{'canonical_signatures':targets,'source_batches':[targets[i:i+50] for i in range(0,len(targets),50)],'old_target_order_preserved':True,'original_signatures':341,'self_reflecting_cases':9})
source('PRE_EXECUTION.md','''# M3_POP4_RISK03: renewed finite allowance, interrupted construction first

The human explicitly renews the finite allowance and authorizes continuing
the remaining 341 total-four signatures, starting with construction of
e0+e1+2e6. Fresh finite allowance: 7200 CPU seconds. Prior charges 7200
and 7195.21875 CPU seconds, all historical UNKNOWN reports and all old files
remain immutable. The same original per-phase and inherited 12h caps hold.

One principal theorem: shared J in [-2,0], J <= -psi, for exactly the new
passed sectors, all 126 masks and both realizable regions. W(O)=J-5chi8,
W(M)=-5chi8 imply every original closed mixed walk >=0 and finite walk >=-7.
Full M3, larger populations and Stage04 remain open.

Gate 1: strictly smaller total-four domain: 175 remaining representatives,
including 9 fixed reflections, only the previously proved risky fibers.
All 374 covered total-four vectors and prior source/word/bank checks reused.
Gate 2: the proved source-complete retained-budget induction at population
four, exact integer recurrence, independent ordered-key/source-address
regeneration and every residual. Analytic omission uses
w-DeltaJ >= w+psi(Bt)-2 >=0. No fit extrapolation or new existence premise.
Gate 3: one mechanism, one bounded source-audit workflow registered NOW as
four disjoint fixed batches of at most 50 canonical cases, each <=300 CPU s,
at most 1200 source CPU s overall. Each batch: one new negative H1 per case,
at most 4 full 147-O/same-actual-127-M cycles, at most 4 helper controls.
This is upfront scope partitioning, never splitting/retrying a failed phase.
Evaluate each new original root once and checkpoint immediately. All old
h0, G, middle-helper, DELETE-zeroKEEP and normal-form checks are reused.
Gate 4: before 374/715 total-four vectors; success deletes exactly the newly
source-complete sectors, up to 341 vectors / 42966 mask sectors. No new
observables, source constraints, dependencies or backend. Exact coverage,
fixed reflections once; UNKNOWN never PASS. Source-incomplete cases excluded.

FIRST mathematical action: reuse by hash ONLY the complete old relation.json
and build_status.json for e0+e1+2e6. Do not rerun enumeration or reuse its
partial failed construction. Run a fresh full construction <=300 CPU s,
then a full independent audit <=120 CPU s / 1m canonical queries. This
explicit user instruction authorizes that old interrupted construction
retry only. No other new failure is automatically retried or skipped.

Every later sigma: enumeration <=120 CPU s / 1m canonical queries,
construction <=300 CPU s, independent complete audit <=120 CPU s / 1m
queries. Live records <2m, DAG <4m, edges <5m, memory <=32GiB. Tighten
deadlines near the fresh 7200 allowance, reserve 5 seconds, capture whole
process CPU through finally plus parent metadata. Stop FIRST new cap,
UNKNOWN, failed premise, template failure or allowance boundary. Then only
already passed cases get source completion. No later experimental cases.

Nonfixed pairs reuse proved low-image/selector/B-bank reflection; fixed
sigma has a full direct table with NO J mirror-invariance assumption.
Original G slot0/current-child semantics, unfolded F occurrences, all
private count/bill branches and independent OM/MO scopes stay included.

R1 original target/full closure. R2 original Stage11F two sorts, SAME actual
midpoint, independent private scopes, q and weights. R3 frozen
(mu,b,alpha,sigma), alpha7 depth2, T266, Bank25=25, architecture and caps.
R4 exact evidence/provenance. Preserve h0 actual0/declared18/q9/weight-3
and independent fiber v. No installs, source/tests/config/Git writes, Stage04
or full-M3/negative-cycle promotion. All writes only HERE, Python -B.
All old files and tracked tree must pass final integrity audit. No subagents.
''')
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    source(name,(OLD/name).read_text().replace('M3_POP4_RISK02','M3_POP4_RISK03'))
for name in ('SOURCE_LIFT.md','REPRESENTATION_PROOF.md'):
    source(name,(OLD/name).read_text())
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK02','M3_POP4_RISK03').replace("M3_POP4_RISK01/certificate.json","M3_POP4_RISK02/certificate.json").replace("==128","==236")
source('entry.py',entry)
folder=BASE/('s'+''.join(map(str,first)));folder.mkdir()
reused=[]
for name in ('relation.json','build_status.json'):
    src=OLD/folder.name/name;dst=folder/name;shutil.copyfile(src,dst)
    assert sha(src)==sha(dst)
    reused.append({'source':src.as_posix(),'copy':dst.as_posix(),'sha256':sha(src)})
write(BASE/'reused_candidate.json',{'sigma':first,'complete_enumeration_only':True,'partial_construction_reused':False,'files':reused})
driver=(OLD/'run.py').read_text()
driver=driver.replace("phase in ('prefix_dp','construct')","phase=='prefix_dp'")
driver=driver.replace("assert tuple(sig)==first and phase=='audit';returncode=0 if read(exitfile)['error'] is None else 1","raise AssertionError('unexpected phase output: no new failure may be retried')")
driver=driver.replace('Only the explicitly authorized bootstrap audit exists at first entry.','No phase output exists before this driver; only enumeration is reused.')
driver=driver.replace('ALL295_REMAINING_TOTAL4_FINITE_PASS','ALL175_REMAINING_TOTAL4_FINITE_PASS')
driver=driver.replace("'previous_allowance_budget_charge_unchanged':7200","'previous_allowance_CPU_charged_unchanged':7195.21875,'older_allowance_budget_charge_unchanged':7200")
driver=driver.replace("'reused_completed_old_phases':2","'reused_completed_old_phases':1")
driver=driver.replace("'interrupted_old_audit_explicitly_retried':True","'interrupted_old_construction_explicitly_retried':True")
source('run.py',driver)
combined=(OLD/'combined_certificate.py').read_text()
needle="        renewed={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK02/certification_run.json').read_text())['source_certified_signatures']}"
combined=combined.replace(needle,"        renewal3={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK03/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in renewal3 or tuple(reversed(sig)) in renewal3:return 'renewal3_population4'\n"+needle)
needle="        elif kind=='renewed_population4':"
combined=combined.replace(needle,"        elif kind=='renewal3_population4':\n            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK03'));m=module('renewal3_population4_bank',REBOOT/'M3_POP4_RISK03/certified_decoder.py');self.decoder=m.PopulationFourCertificate()\n"+needle)
source('combined_certificate.py',combined)
verify=(OLD/'verify_combination.py').read_text()
verify=verify.replace("    assert len(old)==3044","    prior2=read(BASE.parent/'M3_POP4_RISK02/combination_check.json')['new_certified_signatures']\n    for s in prior2:assert P.scope({'sigma':s})=='renewed_population4';old.add(tuple(s))\n    assert len(old)==3280")
verify=verify.replace("P.scope({'sigma':s})=='renewed_population4'\n    remaining", "P.scope({'sigma':s})=='renewal3_population4'\n    remaining")
verify=verify.replace('577','341').replace('138','374').replace('3044','3280')
source('verify_combination.py',verify)
fin=(OLD/'finalize.py').read_text().replace('577','341').replace('138','374').replace('3044','3280')
fin=fin.replace("run['reused_completed_old_phases']==2","run['reused_completed_old_phases']==1").replace('len(sources)<=6','len(sources)<=4')
fin=fin.replace("for name in ('M3_POP4_RISK01/certificate.json'","for name in ('M3_POP4_RISK02/certificate.json','M3_POP4_RISK02/final_manifest.json','M3_POP4_RISK02/combination_check.json','M3_POP4_RISK02/SOURCE_LIFT.md','M3_POP4_RISK01/certificate.json'")
fin=fin.replace("'authorized_old_incomplete_audit_retried':True,'old_complete_build_and_construction_reused':True","'authorized_old_incomplete_construction_retried':True,'old_complete_enumeration_reused':True,'partial_old_construction_reused':False")
fin=fin.replace("'prior_finite_allowance_budget_charge_unchanged':7200","'old_finite_charges_unchanged':[7200,7195.21875]")
fin=fin.replace("'interrupted_old_audit_completed':done[0]==[0,0,1,0,2,1,0,0,0,0]","'interrupted_old_construction_completed':done[0]==[1,1,0,0,0,0,2,0,0,0]")
fin=fin.replace('The explicitly interrupted audit e2+2e4+e5 was completed FIRST. Its exact saved relation, potential and complete build/construction reports were reused by hash.','The explicitly interrupted construction e0+e1+2e6 was completed FIRST, followed by a new full independent audit. Only its complete relation and build report were reused by hash; the old partial construction was not reused.')
source('finalize.py',fin)
for p in BASE.glob('*.py'):compile(p.read_text(),str(p),'exec')
print(json.dumps({'prepared':True,'remaining_vectors':341,'canonical_cases':175,'fixed_cases':9,'first':first,'math_changes':'BASE path only in prefix/construct/audit','source_batches':4}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
