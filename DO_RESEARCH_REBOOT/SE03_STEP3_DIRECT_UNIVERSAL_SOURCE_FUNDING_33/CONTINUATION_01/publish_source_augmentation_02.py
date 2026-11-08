"""Metadata-only resource/provenance publication; no semantic execution."""
import hashlib,json,subprocess,time
from pathlib import Path
START=time.process_time();B=Path(__file__).resolve().parent;F=B/'SOURCE_AUGMENTATION_02';P=B.parent.parent;ROOT=B.parents[2]
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT).decode('utf-8',errors='replace').strip()
def main():
    entry=json.loads((B/'entry_authorized1440.json').read_text());old=json.loads((B/'FINAL_C33/resources_checkpoint.json').read_text())
    global_cpu=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries'];new=[]
    for pp in sorted(B.glob('run_*_result.json')):
        z=json.loads(pp.read_text());ep=B/('controller_'+z['phase']+'_exit.json');c=json.loads(ep.read_text());charge=z['child_CPU']+c['whole_process_CPU_seconds']
        global_cpu+=charge;groups[z['group']]+=charge;queries+=z.get('source_queries',0)
        if z['phase'] in ('proof165','verify78'):
            new.append({'phase':z['phase'],'group':z['group'],'status':z['status'],'child_CPU':z['child_CPU'],'controller_CPU':c['whole_process_CPU_seconds'],'total_charge':charge,'source_queries':z.get('source_queries',0),'run_sha256':pin(pp),'controller_exit_sha256':pin(ep)})
    assert len(new)==2 and all(x['status']=='PASS' for x in new)
    assert global_cpu==old['global_CPU']+sum(x['total_charge'] for x in new)
    assert groups['symbolic']==old['symbolic_CPU']+sum(x['total_charge'] for x in new if x['group']=='symbolic')
    assert groups['independent']==old['independent_CPU']+sum(x['total_charge'] for x in new if x['group']=='independent')
    assert queries==old['source_queries']
    deps=json.loads((B/'FINAL_C33/dependency_manifest.json').read_text())['dependencies']
    for z in deps:assert pin(Path(z['path']))==z['sha256']
    extra=[(B/'FINAL_C33/CHECKPOINT.md','ENTRY_PARENT_BOX_INSPECTED'),(B/'FINAL_C33/BANK25_SCHEDULE_PROOF.md','ENTRY_BANK_HYPOTHESES_INSPECTED'),
      (B/'FINAL_C33/resources_checkpoint.json','PRIOR_PUBLISHED_LEDGER'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md','ORIGINAL_CONDITIONAL_GATE_AND_TYPE_A_B_CONTRACT_INSPECTED'),
      (P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CARRY_STORAGE_SEAM.md','ORIGINAL_WORKING_BANK_CONTRACT_INSPECTED'),
      (B/'PREPARED_FRAME_STATIC_BANK25.md','INHERITED_ACCEPTED_STATIC_SOURCE_BLOCK_SCHEDULE'),
      (B/'prepared_frame_static_bank_independent_audit.json','ACCEPTED_VERIFY66_REUSED_NOT_RERUN'),
      (B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md','INHERITED_PUBLISHED_TRANSFORMATION_COROLLARY_INSPECTED'),
      (B/'uniform_A_realization_independent_audit.json','ACCEPTED_REALIZATION_INTERFACE_RECEIPT_REUSED'),
      (P/'SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md','INHERITED_UNIFORM_W_H_CLOSED_SOURCE_AND_RR_INDUCTION_INSPECTED'),
      (P/'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/FINAL_VERDICT.md','RESTRICTED_DERIVATION_AUDIT_PENDING_SCOPE_RETAINED'),
      (P/'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20/REMAINING_EXTREME_FRAME.md','EXACT_RETURN_AND_SCOPE_OBLIGATION_INSPECTED_NO_STATUS_PROMOTION')]
    deps.extend({'path':str(p),'sha256':pin(p),'status':s,'inspected':True} for p,s in extra)
    audit=json.loads((F/'independent_symbolic_audit.json').read_text())
    for p,sha in audit['input_sha256'].items():
        target=Path(p) if Path(p).is_absolute() else F/p
        assert pin(target)==sha
    assert not git('status','--porcelain','--untracked-files=no')
    out('dependency_manifest.json',{'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':True,'dependencies':deps,'old_source_and_owner_bytes_unchanged':True})
    ledger={'status':'C33_SOURCE_AUGMENTATION_02_PUBLISHED_OPEN','active_authorization':'../resource_amendment_1440.json','controller':'../run_phase_1440.py','prior_ledger':'../FINAL_C33/resources_checkpoint.json',
      'branch':git('branch','--show-current'),'HEAD':git('rev-parse','HEAD'),'tracked_clean':True,
      'global_CPU':global_cpu,'global_cap':7200,'symbolic_CPU':groups['symbolic'],'symbolic_cap':1440,'independent_CPU':groups['independent'],'independent_cap':600,
      'source_queries':queries,'source_query_cap':3000000,'remaining_queries':3000000-queries,'query_batch_cap':50000,'Bank25':25,
      'remaining_global_CPU':7200-global_cpu,'remaining_symbolic_CPU_including_reserve':1440-groups['symbolic'],'remaining_independent_CPU_including_reserve':600-groups['independent'],
      'global_reserve':5,'controller_reserve':1,'live_state_limit':2000000,'DAG_limit':4000000,'stored_edge_limit':5000000,'memory_limit_bytes':34359738368,'wall_limit_hours':12,
      'phase_caps_unchanged':entry['phase_caps'],'default_new_phase_cap':20,'new_charges':new,'all_historical_charges_including_failures_retained':True,'usage_reset':False,
      'metadata_publication_CPU':'excluded under inherited convention and separately recorded in publication_exit.json','resource_exhaustion_claimed':False,'new_cap_request_pending':False,'principal_C33':'OPEN',
      'result':'source-solvent reset-block augmentation/working2 proved conditionally; uniform geometric-summary natural-packet debt class refuted; universal source block/credit existence OPEN'}
    out('resources_checkpoint.json',ledger)
    with (B/'CHECKPOINT_1440_SOURCE_AUGMENTATION_02.md').open('x',encoding='utf-8') as f:f.write('# Latest C33 source augmentation checkpoint\n\nC33 remains OPEN. Read [SOURCE_AUGMENTATION_02/CHECKPOINT.md](SOURCE_AUGMENTATION_02/CHECKPOINT.md) and its current resources_checkpoint.json. No old checkpoint, owner or charge was overwritten.\n')
    files={p.name:pin(p) for p in sorted(F.iterdir()) if p.is_file()}
    scripts={p.name:pin(p) for p in (B/'audit_proof165.py',B/'audit_verify78.py',Path(__file__))}
    out('publication_manifest.json',{'files':files,'new_scripts':scripts,'root_checkpoint_sha256':pin(B/'CHECKPOINT_1440_SOURCE_AUGMENTATION_02.md'),'principal_C33':'OPEN','all_frozen_artifacts_preserved':True})
    out('publication_seal.json',{'manifest_sha256':pin(F/'publication_manifest.json'),'status':'SOURCE_AUGMENTATION_02_OPEN_CHECKPOINT_PUBLISHED','universal_proof_sealed':False,'metadata_only':True})
    print(json.dumps({k:ledger[k] for k in ('status','global_CPU','symbolic_CPU','independent_CPU','source_queries','remaining_queries','principal_C33')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:out('publication_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True,'error':error,'source_queries':0})
