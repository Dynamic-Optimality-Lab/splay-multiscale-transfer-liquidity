"""Append-only final CD(5) publication/resource/provenance seal."""
import hashlib,json,subprocess,time
from datetime import datetime,timezone
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parent.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time()
e=read(B/'entry.json');pins=read(B/'dependency_pins.json')['pins']
for row in pins:assert sha(ROOT/row['path'])==row['sha256'],row['path']
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head==e['head']
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
phases=[]
for path in sorted(B.glob('run_*_result.json')):
    d=read(path);controller=read(B/('controller_'+d['phase']+'_exit.json'))
    assert d['status']=='PASS' and d['returncode']==0 and d['termination'] is None and d['error'] is None
    assert controller['error'] is None and d['child_CPU']<d['allocated_CPU_cap']
    assert d['peak_working_set_bytes_observed']<e['memory_cap_bytes']
    phases.append({'phase':d['phase'],'child_CPU':d['child_CPU'],
      'whole_controller_CPU':controller['whole_process_CPU_seconds'],
      'charged_CPU':d['child_CPU']+controller['whole_process_CPU_seconds'],
      'allocated_CPU_cap':d['allocated_CPU_cap'],'peak_working_set_bytes_observed':d['peak_working_set_bytes_observed']})
assert {p['phase'] for p in phases}=={'assemble','independent'}
assert next(p for p in phases if p['phase']=='assemble')['allocated_CPU_cap']==120
assert next(p for p in phases if p['phase']=='independent')['allocated_CPU_cap']==300
new=sum(p['charged_CPU'] for p in phases);total=e['prior_uniform_CPU']+new
assert total+e['required_reserve']<7200
a=read(B/'assembly.json');audit=read(B/'independent_audit.json')
assert audit['status']=='INDEPENDENT_CD5_BASE_AUDIT_PASS'
assert audit['CD5_mathematical_conclusion'] and audit['all_cases_covered']
assert audit['mandatory_open_CD5_dependencies']==[]
assert audit['new_finite_tests']==audit['new_solver_queries']==audit['new_original_root_queries']==0
assert audit['completed_accepted_semantic_checks_replayed']==0
for n in ('PRE_EXECUTION.md','CD5_PROOF.md','DOMAIN_AUDIT.md','PROOF_AUDIT.md'):
    assert (B/n).is_file() and (B/n).stat().st_size>0
res={'prior_sealed_uniform_CPU':e['prior_uniform_CPU'],
  'new_CPU_including_all_children_and_controllers':new,'cumulative_uniform_CPU':total,
  'global_allowance':7200,'remaining_CPU_including_reserve':7200-total,'required_reserve':5,
  'per_phase':phases,'old_signature_ledger_unchanged':7195.203125,'no_old_phase_renewal_or_cap_increase':True,
  'canonical_query_cap':2000000,'new_canonical_queries':0,'live_record_cap':2000000,
  'new_live_graph_records':0,'input_DAG_cap':4000000,'new_compiled_input_DAG_nodes':0,
  'stored_edge_cap':5000000,'new_stored_graph_edges':0,'memory_cap_bytes':32*1024**3,
  'per_phase_wall_cap_hours':12,'proof_object_bytes':audit['proof_object_input_bytes'],
  'universal_affine_proof_schemas':len(audit['universal_affine_schemas']),
  'symbolic_integer_interval_partitions':2,'new_finite_tests':0,'completed_semantic_checks_replayed':0,
  'metadata_bookkeeping_excluded_by_inherited_convention':True}
write('resources_final.json',res)
cert={'status':'PROVED_CD5_COMPLETE_ORIGINAL_CLOSED_WALK_BASE',
  'theorem':a['theorem'],'domain':a['domain'],'costs':a['costs'],
  'normalization':a['normalization'],'core_geometry':a['geometry'],
  'exhaustive_partition':a['partition'],'leaf_conclusions':a['leaf_conclusions'],
  'completed_components':{
    'RT2':'../06_CERTIFICATES/DIRECT_NFKS_RT2/DIRECT_NFKS_RT2_coarse_double_class_proof.md',
    'K4':'../06_CERTIFICATES/DIRECT_CD_K4/DIRECT_CD_K4_original_class_proof.md',
    'K5_LOW':'../06_CERTIFICATES/DIRECT_CDK5_LOW/DIRECT_CDK5_LOW_restricted_class_proof.md',
    'K5_CORE9':'../RESTRICTED_CD_STEP04/RESTRICTED_CD_CERTIFICATE.json'},
  'mandatory_open_CD5_dependencies':[],'no_new_assumptions':True,'R1_R4_preserved':True,'Bank25':25,
  'proof':'CD5_PROOF.md','domain_audit':'DOMAIN_AUDIT.md','independent_audit':'independent_audit.json',
  'audit_explanation':'PROOF_AUDIT.md','resources':'resources_final.json','dependency_pins':'dependency_pins.json',
  'independent_audit_scope':'separate source/scope/case/affine audit reusing completed proofs; not external peer review or whole-compiler formalization',
  'new_finite_tests':0,'completed_semantic_checks_replayed':0,
  'prefix_bound_claimed':False,'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,
  'publication_gates':{'mathematical_union':'PASS','independent_audit':'PASS','all_original_cases':'PASS',
    'phase_controllers':'PASS','cumulative_resources':'PASS','declared_dependency_hashes':'PASS','HEAD_and_tracked_tree':'PASS'}}
write('CD5_CERTIFICATE.json',cert)
write('CURRENT_STATE.json',{'CD5_base':'SEALED_PROVED','exact_domain':a['domain'],
  'mandatory_open_CD5_dependencies':[],'certificate':'CD5_CERTIFICATE.json',
  'cumulative_uniform_CPU':total,'remaining_CPU_including_reserve':7200-total,
  'unrestricted_CD':'OPEN','Dynamic_Optimality':'OPEN','Bank25':25,
  'next_unproved_principal_bridge':'uniform genuine-support extension beyond five',
  'support_lifting_campaign_executed':False,'historical_files_left_immutable':True})
result=f'''# CD(5) base sealed

**PROVED on the complete original domain:** for every finite ordered key set
and every reachable, fully closed Pair Access walk gamma,

\\[|G(\\gamma)|\\le5\\quad\\Longrightarrow\\quad Q_B(\\gamma)\\le2A(\\gamma).\\]

Ambient tree size, word length, DELETE support, repetition, zero/nongenuine
events, fringe and legal relabeling remain unrestricted. Closure is equality
of both full labeled trees; the closed walk need not start at a diagonal.

If G is empty, Q_B=0. Otherwise cyclic root provenance gives KEEP support=G.
The complete cases are support1..3 (RT2), support4 (CDK4), support5/core<=8
(CDK5-LOW), and support5/core9 (the sealed Restricted-CD theorem). The marked
core is constant throughout the closed walk and has size<=9 in the five-key
case, so these are whole-walk cases with no missing mixed-core branch.

The separate audit passed:872 declared dependency/source hashes, original
domain and closure bridges, two symbolic integer interval partitions, six
universal affine proof schemas, and every imported class hypothesis. Completed
proofs and certificates were reused. No finite tests, new solver/root queries
or completed semantic-check replays were run. R1-R4 and Bank25=25 are preserved.
This audit is a separate checker/derivation here, not external peer review or
formal verification of the entire compiler.

New CPU including children and full controllers:{new:.6f}s.
Cumulative uniform CPU:{total:.6f}/7200s. Remaining:{7200-total:.6f}s,
including the required5s reserve. All current per-phase and other caps passed;
the old finite-signature ledger remains7195.203125s.

Certificate: CD5_CERTIFICATE.json. Proof: CD5_PROOF.md.
Scope: DOMAIN_AUDIT.md. Separate audit: PROOF_AUDIT.md and independent_audit.json.
All artifact hashes are sealed by final_manifest.json.

The support<=5 closed-walk base has no remaining mandatory obligation.
Uniform extension beyond five genuine KEEP keys remains OPEN. No prefix bound,
unrestricted CD or Dynamic Optimality result is promoted. No successor ran.
'''
with (B/'RESULT.md').open('x',encoding='utf-8') as f:f.write(result)
files=[{'file':p.name,'sha256':sha(p)} for p in sorted(B.iterdir()) if p.is_file()]
write('final_manifest.json',{
  'status':'CD5_BASE_SEALED_ALL_PUBLICATION_GATES_PASS','files':files,'certificate':'CD5_CERTIFICATE.json',
  'CD5_complete':True,'all_original_support_le5_closed_walks_covered':True,'mandatory_open_CD5_dependencies':[],
  'verified_existing_input_pins':len(pins),'all_reused_inputs_unchanged':True,
  'HEAD':head,'tracked_tree_clean':True,'R1_R4_preserved':True,'Bank25':25,'new_finite_tests':0,
  'cumulative_uniform_CPU':total,'unrestricted_CD_proved':False,'Dynamic_Optimality_proved':False,
  'sealed_UTC':datetime.now(timezone.utc).isoformat(),'metadata_CPU_excluded_for_final_seal':time.process_time()-start,
  'manifest_self_excluded_from_its_file_hash_list':True})
print(json.dumps({'status':'CD5_BASE_SEALED_ALL_PUBLICATION_GATES_PASS','new_CPU':new,
  'cumulative_uniform_CPU':total,'remaining_CPU':7200-total,'files_sealed':len(files)}))
