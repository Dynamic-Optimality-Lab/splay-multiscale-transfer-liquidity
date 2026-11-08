"""Prepare the explicit audit-first renewal; preserve all historical evidence."""
import json,hashlib,shutil,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
OLD=BASE.parent/'M3_POP4_RISK03'

def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,text):
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(text)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

run=read(OLD/'run_result.json');prior=read(OLD/'certificate.json')
assert prior['new_original_signatures']==157 and prior['total4_vectors_remaining']==184
assert len(run['completed_signatures'])==79 and run['failure']['phase']=='audit'
targets=read(OLD/'targets.json')['canonical_signatures'][79:]
first=[1,1,0,0,0,1,0,1,0,0]
assert targets[0]==first and len(targets)==96
assert sum(s==s[::-1] for s in targets)==8
assert len({tuple(v) for s in targets for v in (s,s[::-1])})==184
write(BASE/'targets.json',{'canonical_signatures':targets,'source_batches':[targets[i:i+50] for i in range(0,len(targets),50)],'old_target_order_preserved':True,'original_signatures':184,'self_reflecting_cases':8})
source('PRE_EXECUTION.md','''# M3_POP4_RISK04: renewed finite allowance, interrupted audit first

The human explicitly renews the finite allowance and authorizes continuing
the remaining 184 total-four signatures, STARTING WITH the interrupted audit
of e0+e1+e5+e7. Fresh finite allowance: 7200 CPU seconds. Historical charges
7200, 7195.21875 and 7195.25 CPU seconds, all historical UNKNOWN reports,
and all old files remain immutable. Original per-phase and inherited 12h
ceilings remain unchanged.

One principal theorem: shared J in [-2,0], J <= -psi, on exactly the new
proved sectors, all 126 masks/both realizable regions. W(O)=J-5chi8 and
W(M)=-5chi8 imply original closed mixed walks >=0 and finite walks >=-7.
Full M3, larger multi-support populations and Stage04 remain open.

Gate 1: total-four only: 96 remaining representatives, including 8 fixed
reflections; the previously proved risky root/target/helper fibers only.
All 531 covered total-four vectors and old source/word/bank checks reused.
Gate 2: reuse the proved complete retained-budget induction at population
four, exact signed integer recurrence, and independent ordered-key and
source-address regeneration/residual audit. Omitted fibers obey
w-DeltaJ >= w+psi(Bt)-2 >=0. No numerical extrapolation, new observable,
source constraint, backend or open existence premise is introduced.
Gate 3: one mechanism and one bounded original-source audit WORKFLOW,
registered NOW as two disjoint fixed batches of at most 50 canonical
cases, each <=300 CPU s, at most 600 source CPU s overall. Each batch:
one fresh negative H1 per new case, at most 4 full 147-O/same-actual-127-M
mixed cycles and 4 helper controls. This is upfront scope partitioning,
never splitting or retrying a failed phase. Every original root evaluated
once and checkpointed immediately. All completed h0/G/middle-helper/
DELETE-zeroKEEP/normal-form checks are reused, not replayed.
Gate 4: BEFORE 531/715 total-four vectors. Success deletes exactly newly
source-complete sectors, up to 184 vectors / 23184 mask sectors. Exact
coverage and fixed sectors counted once; UNKNOWN never PASS. No new
assumptions. Source-incomplete and unfinished sectors remain excluded.

FIRST mathematical action: copy by hash ONLY relation.json, potential.json,
build_status.json and construction.json of e0+e1+e5+e7. Reuse completed
enumeration and construction; do not repeat them. Run a NEW FULL independent
audit <=120 CPU s / 1m canonical queries, not a continuation of partial
in-memory state. The human explicitly authorizes this interrupted audit
retry ONLY; no new failed phase may be retried or skipped automatically.

Every later sigma: one enumeration <=120 CPU s / 1m canonical queries,
construction <=300 CPU s, independent full audit <=120 CPU s / 1m queries.
Live records <2m, DAG <4m, edges <5m, memory <=32GiB. Tighten deadlines near
the fresh 7200 allowance; reserve 5 seconds. Capture whole-process CPU
through finally plus parent metadata CPU, including failed processes.
STOP FIRST new cap/UNKNOWN, premise/template failure or allowance boundary.
No later experiments after that stop. Source-audit only passed new cases.

Nonfixed pairs reuse the independently proved low-image/selector/B-bank
reflection transfer. Fixed sectors have full direct tables with NO J
mirror-invariance assumption. Original G slot0/current-child reads,
unfolded F occurrences, all private count/bill branches and independent
OM/MO scopes stay included. Potential coarsening never merges graph states.

R1 original target/full closure. R2 original Stage11F two sorts, SAME actual
midpoint, independent private scopes, original q/weights. R3 frozen
(mu,b,alpha,sigma), alpha7 depth2, T266, Bank25=25, architecture and caps.
R4 exact status/evidence/provenance. Preserve h0 actual0/declared18/q9/
weight-3 and independent fiber v. No installs, original source/tests/config/
Git writes, Stage04 or full-M3/negative-cycle promotion. All new writes
only HERE, Python -B; all old files read-only. Final integrity audit pins
every old file and tracked HEAD/tree. No subagents.
''')
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    source(name,(OLD/name).read_text().replace('M3_POP4_RISK03','M3_POP4_RISK04'))
for name in ('SOURCE_LIFT.md','REPRESENTATION_PROOF.md'):
    source(name,(OLD/name).read_text())
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK03','M3_POP4_RISK04').replace('M3_POP4_RISK02/certificate.json','M3_POP4_RISK03/certificate.json').replace('==236','==157')
source('entry.py',entry)
folder=BASE/('s'+''.join(map(str,first)));folder.mkdir()
reused=[]
for name in ('relation.json','potential.json','build_status.json','construction.json'):
    src=OLD/folder.name/name;dst=folder/name;shutil.copyfile(src,dst)
    assert sha(src)==sha(dst)
    reused.append({'source':src.as_posix(),'copy':dst.as_posix(),'sha256':sha(src)})
write(BASE/'reused_candidate.json',{'sigma':first,'complete_enumeration_and_construction_reused':True,'partial_audit_reused':False,'files':reused})
driver=(OLD/'run.py').read_text().replace("phase=='prefix_dp'","phase in ('prefix_dp','construct')")
driver=driver.replace('only enumeration is reused.','only enumeration and construction are reused.')
driver=driver.replace('ALL175_REMAINING_TOTAL4_FINITE_PASS','ALL96_REMAINING_TOTAL4_FINITE_PASS')
driver=driver.replace("'previous_allowance_CPU_charged_unchanged':7195.21875,'older_allowance_budget_charge_unchanged':7200","'old_finite_charges_unchanged':[7200,7195.21875,7195.25]")
driver=driver.replace("'reused_completed_old_phases':1","'reused_completed_old_phases':2").replace('interrupted_old_construction_explicitly_retried','interrupted_old_audit_explicitly_retried')
source('run.py',driver)
combined=(OLD/'combined_certificate.py').read_text()
needle="        renewal3={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK03/certification_run.json').read_text())['source_certified_signatures']}"
assert needle in combined
combined=combined.replace(needle,"        renewal4={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK04/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in renewal4 or tuple(reversed(sig)) in renewal4:return 'renewal4_population4'\n"+needle)
needle="        elif kind=='renewal3_population4':"
combined=combined.replace(needle,"        elif kind=='renewal4_population4':\n            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK04'));m=module('renewal4_population4_bank',REBOOT/'M3_POP4_RISK04/certified_decoder.py');self.decoder=m.PopulationFourCertificate()\n"+needle)
source('combined_certificate.py',combined)
verify=(OLD/'verify_combination.py').read_text()
verify=verify.replace("    assert len(old)==3280","    prior3=read(BASE.parent/'M3_POP4_RISK03/combination_check.json')['new_certified_signatures']\n    for s in prior3:assert P.scope({'sigma':s})=='renewal3_population4';old.add(tuple(s))\n    assert len(old)==3437")
verify=verify.replace("P.scope({'sigma':s})=='renewal3_population4'\n    remaining","P.scope({'sigma':s})=='renewal4_population4'\n    remaining")
verify=verify.replace('341','184').replace('374','531').replace('3280','3437')
source('verify_combination.py',verify)
fin=(OLD/'finalize.py').read_text().replace('341','184').replace('374','531').replace('3280','3437')
fin=fin.replace("run['reused_completed_old_phases']==1","run['reused_completed_old_phases']==2").replace('len(sources)<=4','len(sources)<=2')
fin=fin.replace("for name in ('M3_POP4_RISK02/certificate.json'","for name in ('M3_POP4_RISK03/certificate.json','M3_POP4_RISK03/final_manifest.json','M3_POP4_RISK03/combination_check.json','M3_POP4_RISK03/SOURCE_LIFT.md','M3_POP4_RISK02/certificate.json'")
fin=fin.replace("'authorized_old_incomplete_construction_retried':True,'old_complete_enumeration_reused':True,'partial_old_construction_reused':False","'authorized_old_incomplete_audit_retried':True,'old_complete_enumeration_and_construction_reused':True,'partial_old_audit_reused':False")
fin=fin.replace("'old_finite_charges_unchanged':[7200,7195.21875]","'old_finite_charges_unchanged':[7200,7195.21875,7195.25]")
fin=fin.replace("'interrupted_old_construction_completed':done[0]==[1,1,0,0,0,0,2,0,0,0]","'interrupted_old_audit_completed':done[0]==[1,1,0,0,0,1,0,1,0,0]")
fin=fin.replace('The explicitly interrupted construction e0+e1+2e6 was completed FIRST, followed by a new full independent audit. Only its complete relation and build report were reused by hash; the old partial construction was not reused.','The explicitly interrupted audit e0+e1+e5+e7 was completed FIRST. Its complete relation, potential, build and construction reports were reused by hash. No old complete phase was repeated and no partial audit state was reused.')
source('finalize.py',fin)
for p in BASE.glob('*.py'):compile(p.read_text(),str(p),'exec')
print(json.dumps({'prepared':True,'remaining_vectors':184,'canonical_cases':96,'fixed_cases':8,'first':first,'math_changes':'BASE paths only in prefix/construct/audit','source_batches':2}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
