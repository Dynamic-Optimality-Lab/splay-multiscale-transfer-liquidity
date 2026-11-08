"""PROVENANCE/RESOURCE METADATA ONLY. No source, solver or proof checker.
Publishes immutable snapshot while requested resource amendment is pending.
Metadata CPU is recorded under the inherited publication convention.
"""
import json,time,hashlib,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time()
def rd(p):return json.loads(p.read_text())
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    e=rd(B/'entry_research.json');g=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);queries=e['inherited_conservative_queries'];runs=[]
    for path in sorted(B.glob('run_*_result.json')):
        r=rd(path);controller=rd(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+controller['whole_process_CPU_seconds'];g+=charge;groups[r['group']]+=charge;queries+=r.get('source_queries',0);runs.append(dict(r,controller_CPU=controller['whole_process_CPU_seconds'],total_charge=charge))
    assert groups['symbolic']<480 and groups['independent']<600 and g<7200 and queries<=3000000
    root=B.parent.parent.parent
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=root,text=True).strip();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip();tracked=subprocess.run(['git','diff','--quiet'],cwd=root).returncode
    assert branch==e['branch'] and head==e['head'] and tracked==0
    out('resources_checkpoint.json',{'status':'CUMULATIVE_SAFE_CHECKPOINT_SYMBOLIC_AMENDMENT_PENDING','branch':branch,'head':head,'tracked_clean':True,'global_CPU':g,'global_cap':7200,'symbolic_CPU':groups['symbolic'],'symbolic_cap':480,'independent_CPU':groups['independent'],'independent_cap':600,'source_queries':queries,'source_query_cap':3000000,'remaining_queries':3000000-queries,'source_query_batch_cap':50000,'remaining_global_CPU':7200-g,'remaining_symbolic_CPU_including_reserve':480-groups['symbolic'],'remaining_independent_CPU_including_reserve':600-groups['independent'],'global_reserve':5,'controller_reserve':1,'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'memory_limit_bytes':32*1024**3,'wall_limit_hours':12,'usage_reset':False,'query_or_audit_cap_increased':False,'pending_symbolic_request':600,'pending_request_authorized':False,'all_run_charges':runs,'schema_instantiation_accounting':'Reused audited free-gap source identities are charged as symbolic CPU and separately counted. Only original new splay-engine calls are new source queries; no new native10 replay is claimed for lifted cases.','principal_U33':'OPEN'})
    states=[{'id':'ALL_B_CORE_LE8','status':'PROVED_SOURCE_CLASS','proof':'CORE_AT_MOST_EIGHT_SOURCE_THEOREM.md','audit':'eight_core_independent_audit.json'},
      {'id':'NATIVE9','status':'PROVED_SOURCE_CLASS','proof':'NATIVE_NINE_SOURCE_THEOREM.md','audit':'native9_sparse_independent_audit.json'},
      {'id':'BF9_ONE_A_HELPER_ALL_GAPS','status':'PROVED_SOURCE_CLASS','proof':'ONE_HELPER_SOURCE_THEOREM.md','audit':'one_helper_complete_independent_registry.json'},
      {'id':'ACTUAL_R7_FROZEN_OWNER_EXTENSION','status':'PROVED_INSTANCE','audit':'one_helper_original_source_independent_audit.json'},
      {'id':'C1_NATURAL_PRICE','status':'REFUTED_RULE_NOT_CD','proof':'NINE_CORE_C1_FAILURE.md'},
      {'id':'COST_FREE_UNARY_PROJECTION','status':'REFUTED_BRIDGE','proof':'UNARY_PROJECTION_BRIDGE_REFUTATION.md'},
      {'id':'UNARY_RETURN_FAMILY_REPAIR','status':'PROVED_FAMILY_INTERFACE','proof':'UNARY_SOURCE_REPAIR_THEOREM.md','audit':'unary_source_repair_independent_audit.json'},
      {'id':'NATIVE10_PRIMITIVES','status':'PROVED_SOURCE_KERNEL','audit':'native10_source_independent_audit.json'},
      {'id':'NATIVE10_RANGE_LE2','status':'REFUTED_RULE_NOT_CD','proof':'NATIVE10_WIDTH_THREE_LOWER_BOUND.md','audit':'native10_width3_lower_independent_audit.json'},
      {'id':'NATIVE10_RANGE3','status':'OPEN_SAVED_CANDIDATE_FAILS_CHECK','audit':'native10_checkpoint_complete_audit.json','checkpoint':'native10_debt_02.pkl'},
      {'id':'UNIVERSAL_E_R_AND_GATE_U','status':'OPEN','proof':'SOURCE_COVERAGE_AND_GATE_U.md'}]
    out('certificate_registry.json',{'results':states,'independent_verification':'distinct implementations, same agent; no external/formal certification','principal_U33':'OPEN','inherited_frozen_pins':'dependency_pins.json'})
    excluded={'publication_manifest.json','publication_seal.json','publication_exit.json'};manifest={};archive=[]
    for p in sorted(B.iterdir()):
        if not p.is_file():continue
        if p.suffix=='.pkl':archive.append({'file':p.name,'bytes':p.stat().st_size,'role':'preserved producer/search checkpoint; accepted coefficients separately published or explicitly hashed by audit'});continue
        if p.name in excluded:continue
        manifest[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    candidate=rd(B/'native10_checkpoint_complete_audit.json');manifest['native10_debt_02.pkl']={'sha256':candidate['input_sha256'],'provenance':'immutable input hash from complete independent candidate check; reused, not rehashed','bytes':(B/'native10_debt_02.pkl').stat().st_size}
    out('publication_manifest.json',{'branch':branch,'head':head,'tracked_clean':True,'files':manifest,'preserved_binary_inventory':archive,'principal_U33':'OPEN','snapshot':'at symbolic cap480, resource amendment pending'})
    out('publication_seal.json',{'status':'PROVENANCE_SNAPSHOT_NOT_UNIVERSAL_PROOF_SEAL','manifest_sha256':hashlib.sha256((B/'publication_manifest.json').read_bytes()).hexdigest(),'principal_U33':'OPEN','metadata_CPU_excluded_under_inherited_publication_convention':time.process_time()})
    print(json.dumps({'status':'CHECKPOINT_PUBLISHED','global_CPU':g,'symbolic_CPU':groups['symbolic'],'independent_CPU':groups['independent'],'queries':queries,'manifest_files':len(manifest),'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('publication_exit.json',{'metadata_only_CPU':time.process_time(),'error':error,'source_engine_calls':0,'solver_or_checker_run':False})
