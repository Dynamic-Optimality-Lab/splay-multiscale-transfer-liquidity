"""User-authorized audit CPU exception; old evidence stays immutable."""
import json,hashlib,shutil,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent;OLD=BASE.parent/'M3_POP4_RISK06'
def read(p):return json.loads(p.read_text())
def write(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def source(name,s):
    if name.endswith('.py'):compile(s,str(BASE/name),'exec')
    with (BASE/name).open('x',encoding='utf-8') as f:f.write(s)
def sha(p):return hashlib.sha256(Path('\\\\?\\'+str(p.resolve())).read_bytes()).hexdigest()

prior=read(OLD/'certificate.json');run=read(OLD/'run_result.json')
assert prior['total4_vectors_covered']==708 and prior['total4_vectors_remaining']==7
assert run['failure']['phase']=='audit' and run['renewed_CPU_charged']==3411.6875
remaining=read(OLD/'remaining_sectors.json')['sectors'];targets=[]
for r in remaining:
    s=r['canonical_sigma']
    if s not in targets:targets.append(s)
first=[1,0,1,0,0,0,0,1,0,1]
assert targets[0]==first and len(targets)==5 and sum(s==s[::-1] for s in targets)==3
assert len({tuple(v) for s in targets for v in (s,s[::-1])})==7
write(BASE/'targets.json',{'canonical_signatures':targets,'source_batches':[targets],'remaining_original_signatures':7,'fixed_cases':3,'query_cap':2000000,'old_order_preserved':True,'audit_CPU_cap':300,'finite_CPU_ceiling':7200,'prior_current_finite_CPU':3411.6875})
source('PRE_EXECUTION.md','''# M3_POP4_RISK07: finish total four, audit CPU exception

The human explicitly authorizes raising only the independent-audit CPU
cap from120 to300 seconds and retrying the interrupted audit FIRST.
Existing finite allowance7200 CPU seconds is NOT reset:3411.6875 already
charged,3788.3125 left. Retain5 seconds reserve and whole child-process
CPU through finally plus parent metadata CPU. Original12h ceiling unchanged.
Enumeration120, construction300, source300 CPU seconds remain unchanged;
2m canonical queries in both enumeration/audit, live records<2m,DAG<4m,
edges<5m,memory<=32GiB remain unchanged. Stop first NEW cap/UNKNOWN,
premise/template failure or allowance boundary. No skip, failed-phase
split, automatic retry, backend change or further cap increase.

Principal theorem: for each new certified sigma, J in[-2,0],J<=-psi,
W(O)=J-5chi8,W(M)=-5chi8 discharges original legs. Closed mixed walks>=0;
finite walks>=-7. Full M3, totals>=5 and Stage04 remain open.

Gate1 (strict reduction): only five representatives/seven original vectors
remain of715 total-four signatures. Reuse all708 certified cases and
previously complete proofs and checks. Three fixed sectors use full direct
tables; two reflection pairs use proved transfer. No J symmetry imposed.
Gate2 (mechanism): existing complete population-four retained-budget DP,
integer potential construction, independent ordered-key/source-address
grammar and every residual. Omitted fibers satisfy
w-DeltaJ>=w+psi(Bt)-2>=0 by the pinned selector proof. No new premise.
Gate3 (bounded scope): one principal theorem/mechanism and one source phase
<=300 CPU seconds registered now for these five representatives, at most
four closed mixed cycles/four helper controls. No old source roots replayed.
Gate4 (upward advancement): BEFORE708/715; each independently audited and
source-complete sector deletes its original obligation. Success715/715
at total four only. UNKNOWN never PASS; no unstarted/source-incomplete scope.

FIRST mathematical action is the FULL independent audit of e0+e2+e7+e9,
with300 CPU seconds/2m queries. Its four complete input/build/construction
files are copied and hash-verified; no complete phase or partial audit is
replayed/reused. Source bank, selector,78 shapes and inherited normal forms
are reused, not rederived. Old failed audit/provenance remains immutable.

R1 exact original target/full-state closure. R2 original Stage11F two sorts,
same actual midpoint, independent OM/MO private witnesses, original q/weights.
R3 frozen(mu,b,alpha,sigma),alpha7 depth2,T266,Bank25=25,architecture and
all caps except the explicitly authorized audit CPU change. R4 exact
evidence/provenance/status. Preserve h0 actual0/declared18/q9/weight-3,
independent free v, literal-slot0/current-child G and unfolded F identities,
every private count/bill branch and full147-O/same127-M closure.
Potential coarsening is not an original-vertex quotient.

All writes only HERE, Python -B, no installs/Git/source/tests/configuration
changes. Pin old files and check hashes/HEAD/tracked tree at end. Concurrent
U4 additions are recorded separately, not modified or mathematical evidence.
No subagents or execution beyond this total-four scope.
''')
changes=[]
for name in ('prefix_dp.py','construct.py','audit.py','candidate_decoder.py','certified_decoder.py','source_audit_batch.py','audit_source_batches.py'):
    original=(OLD/name).read_text();s=original.replace('M3_POP4_RISK06','M3_POP4_RISK07')
    if name=='audit.py':
        needle='CPU_CAP=min(120,float(sys.argv[11])) if len(sys.argv)>11 else 120'
        assert s.count(needle)==1;s=s.replace(needle,'CPU_CAP=min(300,float(sys.argv[11])) if len(sys.argv)>11 else 300')
    source(name,s)
    restored=s.replace('M3_POP4_RISK07','M3_POP4_RISK06')
    if name=='audit.py':restored=restored.replace('CPU_CAP=min(300,float(sys.argv[11])) if len(sys.argv)>11 else 300',needle)
    assert restored==original
    changes.append({'file':name,'source_sha256':sha(OLD/name),'new_sha256':sha(BASE/name),'only_path_and_authorized_audit_cap_changed':True})
write(BASE/'implementation_change_audit.json',{'files':changes,'recurrence_grammar_residual_source_semantics_unchanged':True,'audit_CPU_change':[120,300],'query_cap':2000000})
for name in ('SOURCE_LIFT.md','REPRESENTATION_PROOF.md','GUARD_PRESERVATION.md'):source(name,(OLD/name).read_text())
source('AUDIT_CAP_PRESERVATION.md','''# Independent-audit CPU guard

Only CPU_CAP=min(120,requested) and default120 become min(300,requested)
and default300. All ordered-key enumeration, private count branches,
family/option equalities, source-address replay, potential range checks and
integer residual assertions are byte-identical after path normalization.
The cap gates time, not membership in the matrix or an inequality. A
complete audit must still finish every required loop; truncation remains
UNKNOWN. This resource authorization alone proves nothing. Query2m and
all other guards stay unchanged. See implementation_change_audit.json.
''')
entry=(OLD/'entry.py').read_text().replace('M3_POP4_RISK06','M3_POP4_RISK07').replace('M3_POP4_RISK05/certificate.json','M3_POP4_RISK06/certificate.json').replace('==32','==54')
source('entry.py',entry)
folder=BASE/('s'+''.join(map(str,first)));folder.mkdir()
files=[]
for name in ('relation.json','potential.json','build_status.json','construction.json'):
    src=OLD/folder.name/name;dst=folder/name;shutil.copyfile(src,dst);assert sha(src)==sha(dst)
    files.append({'source':src.as_posix(),'copy':dst.as_posix(),'sha256':sha(src)})
write(BASE/'reused_candidate.json',{'sigma':first,'files':files,'completed_phases_reused':2,'partial_audit_reused':False})
combined=(OLD/'combined_certificate.py').read_text()
needle="        renewal6={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK06/certification_run.json').read_text())['source_certified_signatures']}"
assert combined.count(needle)==1
combined=combined.replace(needle,"        renewal7={tuple(v) for v in json.loads((REBOOT/'M3_POP4_RISK07/certification_run.json').read_text())['source_certified_signatures']}\n        if tuple(sig) in renewal7 or tuple(reversed(sig)) in renewal7:return 'renewal7_population4'\n"+needle)
needle="        elif kind=='renewal6_population4':"
assert combined.count(needle)==1
combined=combined.replace(needle,"        elif kind=='renewal7_population4':\n            sys.path.insert(0,str(REBOOT/'M3_POP4_RISK07'));m=module('renewal7_population4_bank',REBOOT/'M3_POP4_RISK07/certified_decoder.py');self.decoder=m.PopulationFourCertificate()\n"+needle)
source('combined_certificate.py',combined)
verify=(OLD/'verify_combination.py').read_text()
verify=verify.replace("    assert len(old)==3560","    prior6=read(BASE.parent/'M3_POP4_RISK06/combination_check.json')['new_certified_signatures']\n    for s in prior6:assert P.scope({'sigma':s})=='renewal6_population4';old.add(tuple(s))\n    assert len(old)==3614")
verify=verify.replace("for s in new:assert P.scope({'sigma':s})=='renewal6_population4'","for s in new:assert P.scope({'sigma':s})=='renewal7_population4'")
verify=verify.replace('61-len(new)','7-len(new)').replace('654+len(new)','708+len(new)').replace('3560','3614')
source('verify_combination.py',verify)
print(json.dumps({'prepared':True,'canonical_cases':5,'original_vectors':7,'audit_CPU_cap':300,'prior_CPU_retained':3411.6875,'finite_CPU_left':3788.3125,'first':first}),flush=True)
subprocess.run([sys.executable,'-B',str(BASE/'entry.py')],check=True)
