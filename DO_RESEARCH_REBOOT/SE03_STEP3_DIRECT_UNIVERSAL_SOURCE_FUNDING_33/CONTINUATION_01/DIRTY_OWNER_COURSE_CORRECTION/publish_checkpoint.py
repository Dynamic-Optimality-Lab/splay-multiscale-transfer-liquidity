"""Metadata/IO-only publication; no source, symbolic or audit phase is run.
Retains the inherited convention separating bookkeeping CPU from research
controller phases, and records this publication's CPU explicitly.
"""
import hashlib,json,subprocess,time
from pathlib import Path
C=Path(__file__).resolve().parent;B=C.parent;P=B.parent.parent;R=P.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(name,value):
    with (C/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    entry=read(B/'entry_authorized1440.json');total=entry['prior_uniform_CPU'];sym=entry['inherited_group_CPU']['symbolic'];audit=entry['inherited_group_CPU']['independent'];queries=entry['inherited_conservative_queries'];charges=[]
    for p in sorted(B.glob('run_*_result.json')):
        v=read(p);controller=read(B/('controller_'+v['phase']+'_exit.json'));charge=v['child_CPU']+controller['whole_process_CPU_seconds'];total+=charge;queries+=v.get('source_queries',0)
        if v['group']=='symbolic':sym+=charge
        else:audit+=charge
        charges.append({'phase':v['phase'],'group':v['group'],'status':v['status'],'child_CPU':v['child_CPU'],'controller_CPU':controller['whole_process_CPU_seconds'],'total_CPU':charge,'queries':v.get('source_queries',0)})
    git=lambda *args:subprocess.check_output(['git','-C',str(R),*args],text=True).strip()
    branch=git('branch','--show-current');head=git('rev-parse','HEAD');tracked=git('status','--short','--untracked-files=no');untracked=git('ls-files','--others','--exclude-standard').splitlines()
    resource={'status':'PUBLISHED_CURRENT_OWNER_COURSE_CORRECTION','active_authorization':'../resource_amendment_1440.json','controller':'../run_phase_1440.py','entry_snapshot':'resources_checkpoint.json','branch':branch,'head':head,'tracked_clean':not tracked,'untracked_paths_count':len(untracked),'untracked_path_inventory_sha256':hashlib.sha256('\n'.join(sorted(untracked)).encode()).hexdigest(),'global_CPU':total,'global_cap':7200,'symbolic_CPU':sym,'symbolic_cap':1440,'independent_CPU':audit,'independent_cap':600,'source_queries':queries,'source_query_cap':3000000,'remaining_queries':3000000-queries,'remaining_symbolic_CPU_including_reserve':1440-sym,'remaining_independent_CPU_including_reserve':600-audit,'remaining_global_CPU':7200-total,'source_query_batch_cap':50000,'Bank25':25,'global_reserve':5,'controller_reserve':1,'live_state_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'memory_limit_bytes':34359738368,'wall_limit_hours':12,'phase_caps_unchanged':entry['phase_caps'],'cumulative_usage_reset':False,'all_run_charges_including_failures':charges,'metadata_only_publication_CPU':'excluded under inherited metadata convention; separately recorded in publication_exit.json','new_cap_request_pending':False,'principal_U33':'OPEN','outcome':'A-L_STRUCTURAL_REDUCTION_NOT_PRINCIPAL_COMPLETION'}
    out('resources_checkpoint_01.json',resource)
    dependencies=[
        (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md','PROVED_CONDITIONAL_TRANSFER; all-source E_r OPEN'),
        (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CARRY_STORAGE_SEAM.md','INHERITED_ACCEPTED_ORIGINAL_WORKING_BANK_CONTRACT'),
        (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md','INHERITED_ACCEPTED_ACTUAL_PERIOD_AND_CUT_TRANSPORT'),
        (P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py','INSPECTED_ORIGINAL_NATURAL_AND_FULL_OWNER_IMPLEMENTATION'),
        (P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py','INSPECTED_ORIGINAL_COMMON_PARTIAL_EXCHANGE'),
        (P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md','INHERITED_SUPPORT_FREE_SOURCE_OWNER_INTERFACE_AT_DECLARED_SCOPE'),
        (P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/leaf_channels.py','INSPECTED_PARTIAL_COMPARISON_FRONTIER_IMPLEMENTATION; maximal-core source restriction retained'),
        (P/'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/SOURCE_FORCED_FROZEN_EXPANSION.md','INSPECTED_MANUSCRIPT_DIAGNOSIS; inherited audit-pending label NOT promoted'),
        (B.parent/'GLOBAL_SOURCE_SUPPLY_DEMAND_IDENTITY.md','INHERITED_IDENTITY; not a global source sign theorem'),
        (P/'SE03_STEP3_GUARDED_E4_PHYSICAL_ESCAPE_28/W199_FROZEN_SOURCE_AND_POLICY.md','INSPECTED_CURRENT58_OWNER_POLICY; no earlier57-entry rollback'),
        (Path('C:/Users/Saif malik/.codex/attachments/47454adb-9c71-4b95-b128-abd82a9743af/Pasted text.txt'),'AUTHORITATIVE_USER_COURSE_CORRECTION_READ')]
    out('dependency_manifest.json',{'dependencies':[{'path':str(p),'sha256':sha(p),'status':status,'inspected':True} for p,status in dependencies],'branch':branch,'head':head,'no_frozen_source_or_owner_file_modified':True})
    receipts=[('H2_actual_owner_independent_audit.json','SOURCE_EXACT_NEW_NORMALIZED_LINEAGE; no H2 donor gap'),('owner_model_independent_audit.json','NEW_REVERSE_COMPONENT_AND_RESERVE_MODEL_CHECK; historical30/current32 separated'),('own_solvent_uniform_independent_audit.json','UNIFORM_SYMBOLIC_OWN_SOLVENT_REDUCTION; arbitrary deficit expansion OPEN')]
    out('certificate_registry.json',{'new_results':[{'receipt':name,'status':read(C/name)['status'],'scope':scope,'sha256':sha(C/name)} for name,scope in receipts],'owner_profile_reduction':'explicit algebraic composition of the inspected original C14/C15 contracts; no new source-existence claim','universal_dirty_frame_source_expansion':'OPEN','all_route_source_architecture_counterexample':'NONE','principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False})
    required=['DIRTY_FRAME_EXACT_FEASIBILITY_MODEL.md','ARBITRARY_DIRTY_FRAME_OWNER_THEOREM.md','FROZEN_OWNER_BLOCKING_STRUCTURE.md','SOURCE_FORCED_DONOR_EXPANSION.md','DIRTY_FRAME_MINIMAL_OBSTRUCTION.md','H2_DIRTY_OWNERSHIP_BRIDGE.md','GLOBAL_H_L_EXCHANGE_APPLICABILITY.md','DIRTY_FRAME_BANK25_SCHEDULE.md','DIRTY_FRAME_GATE_U14_BRIDGE.md','ARBITRARY_DIRTY_FRAME_FINAL_VERDICT.md','C33_NEXT_PARENT_BOX.md','resources_checkpoint.json','resources_checkpoint_01.json']
    missing=[n for n in required if not(C/n).is_file()]
    if missing:raise FileNotFoundError(missing)
    manifest={p.name:{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(C.iterdir()) if p.is_file() and p.name not in ('publication_manifest.json','publication_seal.json','publication_exit.json')}
    for name in ('resource_amendment_1440.json','entry_authorized1440.json','run_phase_1440.py','CHECKPOINT_1440_OWNER_COURSE.md','audit_proof162.py','audit_proof163.py','audit_verify74.py','audit_verify75.py','audit_verify76.py'):
        p=B/name;manifest['../'+name]={'sha256':sha(p),'bytes':p.stat().st_size}
    for phase in ('proof162','proof163','verify74','verify75','verify76'):
        for name in ('run_'+phase+'_result.json','controller_'+phase+'_exit.json','audit_'+phase+'_exit.json','log_'+phase+'.txt'):
            p=B/name;manifest['../'+name]={'sha256':sha(p),'bytes':p.stat().st_size}
    modelpin=read(B/'sparse_source_advance_11_independent_audit.json');manifest['../full_geometry_sparse_work_11.pkl']={'sha256':modelpin['input_sha256']['full_geometry_sparse_work_11.pkl'],'bytes':(B/'full_geometry_sparse_work_11.pkl').stat().st_size,'role':'accepted unchanged causal-discovery checkpoint hash reused; INCOMPLETE, not universal feasibility'}
    out('publication_manifest.json',{'branch':branch,'head':head,'tracked_clean':not tracked,'required_deliverables_present':required,'files':manifest,'principal_U33':'OPEN'})
    out('publication_seal.json',{'status':'COURSE_CORRECTION_CHECKPOINT_PUBLISHED','manifest_sha256':sha(C/'publication_manifest.json'),'metadata_only':True,'outcome':'A-L_STRUCTURAL_REDUCTION_NOT_C33_CLOSURE','principal_U33':'OPEN'})
    print(json.dumps({'status':'PUBLISHED_OWNER_COURSE_CORRECTION','files':len(manifest),'global_CPU':total,'symbolic_CPU':sym,'independent_CPU':audit,'queries':queries,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('publication_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True,'error':error})
