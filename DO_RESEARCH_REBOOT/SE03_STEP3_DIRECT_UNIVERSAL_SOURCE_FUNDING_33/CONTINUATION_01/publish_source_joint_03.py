"""Metadata-only publication; charges and all old files stay cumulative."""
import hashlib,json,subprocess,time
from pathlib import Path
START=time.process_time();B=Path(__file__).resolve().parent;F=B/'SOURCE_JOINT_REPAIR_03';P=B.parent.parent;ROOT=B.parents[2]
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    entry=json.loads((B/'entry_authorized1440.json').read_text());old=json.loads((B/'SOURCE_AUGMENTATION_02/resources_checkpoint.json').read_text())
    global_cpu=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries'];new=[]
    for path in sorted(B.glob('run_*_result.json')):
        z=json.loads(path.read_text());ep=B/('controller_'+z['phase']+'_exit.json');c=json.loads(ep.read_text());charge=z['child_CPU']+c['whole_process_CPU_seconds']
        global_cpu+=charge;groups[z['group']]+=charge;queries+=z.get('source_queries',0)
        if z['phase'] in ('proof166','core39','proof167','verify79'):
            new.append({'phase':z['phase'],'group':z['group'],'status':z['status'],'child_CPU':z['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'total_charge':charge,'source_queries':z.get('source_queries',0),'run_sha256':pin(path),'controller_exit_sha256':pin(ep)})
    assert len(new)==4 and all(z['status']=='PASS' for z in new)
    assert global_cpu==old['global_CPU']+sum(z['total_charge'] for z in new)
    assert groups['symbolic']==old['symbolic_CPU']+sum(z['total_charge'] for z in new if z['group']=='symbolic')
    assert groups['independent']==old['independent_CPU']+sum(z['total_charge'] for z in new if z['group']=='independent')
    assert queries==old['source_queries']+sum(z['source_queries'] for z in new)
    deps=json.loads((B/'SOURCE_AUGMENTATION_02/dependency_manifest.json').read_text())['dependencies']
    for z in deps:assert pin(Path(z['path']))==z['sha256']
    extra=[(B/'SOURCE_AUGMENTATION_02/CHECKPOINT.md','ENTRY_CHECKPOINT_INSPECTED'),
      (B/'SOURCE_AUGMENTATION_02/resources_checkpoint.json','ENTRY_LEDGER_NO_RESET'),
      (P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md','INHERITED_MAXIMAL_CORE_PATH_TO_STAR_MATHEMATICS; original verification labels retained'),
      (P/'SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md','INHERITED_UNIFORM_P_HALF_SOURCE_FORMULAS_AND_REFLECTION_INSPECTED'),
      (B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md','ACCEPTED_CLOSED_EMBEDDING_COROLLARY_REUSED'),
      (B/'uniform_A_realization_independent_audit.json','PRIOR_INTERFACE_RECEIPT_REUSED_NOT_RERUN'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md','UNCHANGED_PARENT_AND_CORE6_OWN_BASE'),
      (P/'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py','ORIGINAL_CANONICAL_COMMON_H0_PRIOR'),
      (P/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py','ORIGINAL_FULL_H_FROZEN_EXTENSION')]
    deps.extend({'path':str(p),'sha256':pin(p),'status':status,'inspected':True} for p,status in extra)
    for file in ('symbolic_source_proof.json','independent_source_audit.json'):
        receipt=json.loads((F/file).read_text())
        for name,sha in receipt['input_sha256'].items():
            path=Path(name) if Path(name).is_absolute() else F/name
            assert pin(path)==sha
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_manifest.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':True,'dependencies':deps,'all_old_source_owner_and_proof_bytes_preserved':True,'no_inherited_audit_pending_label_promoted':True})
    ledger={'status':'C33_SOURCE_JOINT_REPAIR_03_PUBLISHED_PRINCIPAL_OPEN','branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':True,
      'active_authorization':'../resource_amendment_1440.json','controller':'../run_phase_1440.py','prior_ledger':'../SOURCE_AUGMENTATION_02/resources_checkpoint.json',
      'global_CPU':global_cpu,'global_cap':7200,'symbolic_CPU':groups['symbolic'],'symbolic_cap':1440,'independent_CPU':groups['independent'],'independent_cap':600,
      'source_queries':queries,'source_query_cap':3000000,'remaining_queries':3000000-queries,'source_query_batch_cap':50000,'Bank25':25,
      'remaining_global_CPU':7200-global_cpu,'remaining_symbolic_CPU_including_reserve':1440-groups['symbolic'],'remaining_independent_CPU_including_reserve':600-groups['independent'],
      'global_reserve':5,'controller_reserve':1,'live_state_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'memory_limit_bytes':34359738368,'wall_limit_hours':12,
      'phase_caps_unchanged':entry['phase_caps'],'default_new_phase_cap':20,'new_charges':new,'all_historical_charges_including_failures_retained':True,'usage_reset':False,
      'metadata_publication_CPU':'excluded under inherited convention; separately in publication_exit.json','resource_exhaustion_claimed':False,'new_cap_request_pending':False,
      'principal_C33':'OPEN','new_result':'source-derived MR funding and working2 for arbitrary dirty A under actual MR B-cost pattern; all-extreme raw source injection on maximal core; exact interior shared-ticket obstruction'}
    out('resources_checkpoint.json',ledger)
    with (B/'CHECKPOINT_1440_SOURCE_JOINT_REPAIR_03.md').open('x',encoding='utf-8') as f:f.write('# Latest C33 direct source checkpoint\n\nRead [SOURCE_JOINT_REPAIR_03/CHECKPOINT.md](SOURCE_JOINT_REPAIR_03/CHECKPOINT.md) and its current resources_checkpoint.json. C33 is OPEN; the new source laws and the exact remaining interior-transfer obstruction are recorded there. No old checkpoint or owner was overwritten.\n')
    files={p.name:pin(p) for p in sorted(F.iterdir()) if p.is_file()}
    scripts={p.name:pin(p) for p in (B/'audit_proof166.py',B/'audit_core39.py',B/'audit_proof167.py',B/'audit_verify79.py',Path(__file__))}
    out('publication_manifest.json',{'files':files,'new_scripts':scripts,'root_checkpoint_sha256':pin(B/'CHECKPOINT_1440_SOURCE_JOINT_REPAIR_03.md'),'principal_C33':'OPEN','no_frozen_file_overwritten':True})
    out('publication_seal.json',{'manifest_sha256':pin(F/'publication_manifest.json'),'status':'SOURCE_JOINT_REPAIR_03_CHECKPOINT_PUBLISHED','universal_C33_sealed':False,'metadata_only':True})
    print(json.dumps({k:ledger[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries','principal_C33')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('publication_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True,'error':error,'source_queries':0})
