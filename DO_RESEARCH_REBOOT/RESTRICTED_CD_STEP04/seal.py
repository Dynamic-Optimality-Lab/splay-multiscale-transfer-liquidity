"""Final metadata/resource/integrity gate; no mathematical queries or tests."""
import hashlib,json,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time()
entry=read(BASE/'entry.json');pins=read(BASE/'dependency_pins.json')['pins']
for row in pins:assert sha(ROOT/row['path'])==row['sha256'],row['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
dirty=subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
assert head==entry['head'] and not dirty
phases=[]
for p in sorted(BASE.glob('run_*_result.json')):
    d=read(p);ctrl=read(BASE/('controller_'+d['phase']+'_exit.json'))
    assert d['status']=='PASS' and d['termination'] is None and d['error'] is None
    assert ctrl['error'] is None
    assert d['child_CPU']<d['allocated_CPU_cap']
    assert d['peak_working_set_bytes_observed']<=entry['memory_cap_bytes']
    phases.append({'phase':d['phase'],'child_CPU':d['child_CPU'],
        'whole_controller_CPU':ctrl['whole_process_CPU_seconds'],
        'charged_CPU':d['child_CPU']+ctrl['whole_process_CPU_seconds'],
        'cap':d['allocated_CPU_cap'],'peak_working_set_bytes_observed':d['peak_working_set_bytes_observed']})
assert {p['phase'] for p in phases}=={'compose','independent'}
assert next(p for p in phases if p['phase']=='compose')['cap']==120
assert next(p for p in phases if p['phase']=='independent')['cap']==300
new=sum(p['charged_CPU'] for p in phases);total=entry['prior_uniform_CPU']+new
assert total+entry['required_reserve']<entry['global_allowance']
audit=read(BASE/'independent_audit.json');c=read(BASE/'composition.json')
assert audit['status']=='INDEPENDENT_RESTRICTED_CD_COMPOSITION_AUDIT_PASS'
assert audit['mandatory_open_dependencies']==[] and audit['restricted_CD_mathematical_conclusion']
assert audit['new_finite_tests']==audit['new_SMT_queries']==audit['new_original_root_queries']==0
assert audit['completed_accepted_semantic_checks_replayed']==0
for name in ('PRE_EXECUTION.md','DOMAIN_AND_DEPENDENCY_AUDIT.md','RESTRICTED_CD_PROOF.md','PROOF_AUDIT.md'):
    assert (BASE/name).is_file() and (BASE/name).stat().st_size>0
resources={
 'prior_sealed_uniform_CPU':entry['prior_uniform_CPU'],'new_CPU_including_all_children_and_controllers':new,
 'cumulative_uniform_CPU':total,'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,
 'required_reserve':5,'per_phase':phases,'old_signature_ledger_unchanged':7195.203125,
 'no_cap_increase_or_old_phase_renewal':True,'canonical_query_cap':2000000,'new_canonical_queries':0,
 'live_record_cap':2000000,'new_live_graph_records':0,'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,
 'stored_edge_cap':5000000,'new_stored_graph_edges':0,'memory_cap_bytes':32*1024**3,
 'per_phase_wall_cap_hours':12,'new_proof_object_bytes':audit['proof_object_input_bytes'],
 'new_universal_affine_proof_schemas':len(audit['universal_affine_proof_schemas']),
 'new_finite_tests':0,'completed_accepted_semantic_checks_replayed':0,
 'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_final.json',resources)
certificate={
 'status':'PROVED_UNIVERSAL_RESTRICTED_COARSE_DOUBLE_W5_CORE9',
 'theorem':c['theorem'],'domain':c['domain'],'graph':c['graph'],
 'principal_derivation':'forall W choose its 11F closed P: 0 <= w(P) <= 2A(W)-Q_B(W)',
 'dependencies':{'simulation':'../06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP04_UNIVERSAL_CERTIFICATION/S04_STAGE11F_COMPLETION_CERTIFICATE.md',
   'pointwise_sign':'../M3_XFER21/M3_CERTIFICATE.json','full_graph_coverage':'../06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/G01_SOURCE_COVERAGE_THEOREM.md',
   'exact_pins':'dependency_pins.json'},
 'potential':c['potential'],'Step03_M1_M2_M3_closed':True,'Step04_closed':True,
 'mandatory_open_dependencies':[],'R1_R4_preserved':True,'Bank25':25,
 'proof':'RESTRICTED_CD_PROOF.md','domain_audit':'DOMAIN_AND_DEPENDENCY_AUDIT.md',
 'independent_audit':'independent_audit.json','audit_explanation':'PROOF_AUDIT.md',
 'resources':'resources_final.json','new_finite_tests':0,'completed_semantic_checks_replayed':0,
 'independent_audit_scope':'separate exact composition/source-interface checker; reuses completed universal theorems; not external peer review or whole-compiler formalization',
 'unrestricted_Coarse_Double_proved':False,'Dynamic_Optimality_proved':False,
 'publication_gates':{'mathematical_composition':'PASS','independent_audit':'PASS','phase_controllers':'PASS',
    'cumulative_resources':'PASS','declared_dependency_hashes':'PASS','HEAD_and_tracked_tree':'PASS'}}
write('RESTRICTED_CD_CERTIFICATE.json',certificate)
write('CURRENT_STATE.json',{
 'Restricted_CD_W5_core9':'PROVED_UNIVERSAL','11G_Step03':'CLOSED','11G_Step04':'CLOSED',
 'M1':'CLOSED_BY_COMMON_PER_EDGE_POTENTIAL','M2':'CLOSED_BY_COMMON_PER_EDGE_POTENTIAL',
 'M3':'PROVED_UNIVERSAL_ORIGINAL_FULL_GRAPH','mandatory_open_Restricted_CD_dependencies':[],
 'certificate':'RESTRICTED_CD_CERTIFICATE.json','current_uniform_CPU':total,
 'unrestricted_CD':'NOT_PROVED_BY_THIS_CERTIFICATE','Dynamic_Optimality':'OPEN','Bank25':25,
 'historical_files_left_immutable':True})
result=f'''# Step04 result: Restricted CD closed

**PROVED, universal at the exact frozen target:**

\\[\\forall W\\in\\mathcal W_5^9,\\qquad Q_B(W)\\le2A(W).\\]

This is the original five-genuine-KEEP-key, nine-core domain: all126 masks,
arbitrary admissible fringe and saturated signatures, KEEP/DELETE, zero-cost
and nongenuine intermediate KEEPs, E3/E4, arbitrary lengths, primitive and
nonprimitive walks, exact labeled paired closure. No domain was narrowed.

For each W, certified11F supplies a closed P with w(P)<=2A(W)-Q_B(W). The
sealed XFER21 common potential applies to every original edge of the same
full graph, so w(P)>=0. Thus 0<=w(P)<=2A(W)-Q_B(W), proving the inequality.
The common pointwise theorem also closes the LOW-only M1 and HIGH-only M2
cases; no separate Step03 sign premise remains.

The separate audit passed:791 declared dependency hashes, original source
interfaces and full-state/midpoint closure, all-sector scope, quantifier order,
and six universal affine proof schemas. It imports no construction code.
This is an audit reusing completed proofs, not external peer review or a formal
verification of the entire compiler. No finite tests, new solver/root queries,
or completed accepted semantic checks were run. R1-R4 and Bank25=25 remain.

New charged CPU: {new:.6f}s, including both children and full controllers.
Cumulative uniform CPU: {total:.6f}/7200s; remaining {7200-total:.6f}s,
including the required5s reserve. All per-phase and other current caps passed.
The old finite-signature ledger remains7195.203125s.

Certificate: [RESTRICTED_CD_CERTIFICATE.json](RESTRICTED_CD_CERTIFICATE.json).
Proof: [RESTRICTED_CD_PROOF.md](RESTRICTED_CD_PROOF.md).
Domain/dependencies: [DOMAIN_AND_DEPENDENCY_AUDIT.md](DOMAIN_AND_DEPENDENCY_AUDIT.md).
Separate audit: [PROOF_AUDIT.md](PROOF_AUDIT.md), [independent_audit.json](independent_audit.json).
Resource ledger: [resources_final.json](resources_final.json).

**Restricted CD at W_5^9 is closed.** This seal does not prove unrestricted
Coarse-Double, arbitrary KEEP support, or Dynamic Optimality.
'''
with (BASE/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(BASE.iterdir()) if p.is_file()]
write('final_manifest.json',{
 'status':'RESTRICTED_CD_CLOSED_ALL_PUBLICATION_GATES_PASS','files':files,
 'certificate':'RESTRICTED_CD_CERTIFICATE.json','Restricted_CD_complete':True,
 'exact_scope':'W_5^9','Step03_complete':True,'Step04_complete':True,
 'verified_existing_dependency_pins':len(pins),'all_reused_inputs_unchanged':True,
 'HEAD':head,'tracked_tree_clean':True,'new_finite_tests':0,'R1_R4_preserved':True,
 'cumulative_uniform_CPU':total,'Dynamic_Optimality_proved':False,'Bank25':25,
 'sealed_UTC':datetime.now(timezone.utc).isoformat(),
 'metadata_CPU_excluded_for_final_seal':time.process_time()-start,
 'manifest_self_excluded_from_its_file_hash_list':True})
print(json.dumps({'status':'RESTRICTED_CD_CLOSED_ALL_PUBLICATION_GATES_PASS',
      'new_CPU':new,'cumulative_uniform_CPU':total,'remaining_CPU':7200-total,'files_sealed':len(files)}))
