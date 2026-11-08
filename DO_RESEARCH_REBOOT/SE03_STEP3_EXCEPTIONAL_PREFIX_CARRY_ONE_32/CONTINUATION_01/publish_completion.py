"""Metadata/provenance publication only. Does not run a semantic check."""
import json,hashlib,time,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent.parent
START=time.process_time()
def rd(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    entry=rd(B/'entry_authorized.json');pins=rd(B/'dependency_pins.json')
    for p in pins['pins']:assert sha(ROOT/p['path'])==p['sha256'],p['path']
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    status=subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    assert head==entry['head'] and branch==entry['branch'] and not status
    assert rd(B/'FR32_COMPLETE_INDEPENDENT_AUDIT.json')['status']=='PASS_COMPLETE_FR32_CARRY_ONE_STATIC_CERTIFICATE'
    sourceaudit=rd(B/'SOURCE_CONTRACT_INDEPENDENT_AUDIT.json');assert sourceaudit['status']=='PASS_INDEPENDENT_SOURCE_CONTRACTS'
    for n,h in sourceaudit['proof_sha256'].items():assert sha(B/n)==h
    phases=[];total=entry['prior_uniform_CPU'];groups=dict(entry['inherited_group_CPU']);queries=entry['inherited_conservative_queries']
    for p in sorted(B.glob('run_*_result.json')):
        r=rd(p);ctrl=rd(B/('controller_'+r['phase']+'_exit.json'));charge=r['child_CPU']+ctrl['whole_process_CPU_seconds']
        total+=charge;groups[r['group']]+=charge;queries+=r.get('source_queries',0)
        assert r.get('source_queries',0)<=r['allocated_query_cap']<=50000
        phases.append(dict(r,controller_CPU=ctrl['whole_process_CPU_seconds'],total_charge=charge))
    assert total<7200 and groups['symbolic']<240 and groups['independent']<600 and queries<=3000000
    resource={'status':'CUMULATIVE_NO_RESET','cumulative_CPU':total,'global_cap':7200,'global_remaining':7200-total,
        'cumulative_group_CPU':groups,'group_caps':entry['group_caps'],'group_remaining':{g:entry['group_caps'][g]-v for g,v in groups.items()},
        'conservative_all_queries':queries,'query_limit':3000000,'conservative_remaining_queries':3000000-queries,
        'per_source_batch_limit':50000,'all_failed_successful_child_controller_charges_retained':True,'phases':phases,
        'Bank25':25,'live_state_limit':2000000,'DAG_limit':4000000,'edge_limit':5000000,'memory_limit_bytes':32*1024**3,
        'global_reserve':5,'controller_reserve':1,'wall_limit_hours':12,'resource_amendment':'resource_amendment.json',
        'prior_checkpoint_unchanged':True,'semantic_runs_after_this_checkpoint':False,
        'outcome':'A','principal_FR32_CARRY1':'PROVED_AT_FROZEN_EXC_SCOPE','Gate_U':'OPEN',
        'metadata_CPU_excluded_under_inherited_convention':{'entry':rd(B/'entry.json')['metadata_CPU_excluded'],'publication_before_manifest':time.process_time()-START}}
    out('resources_checkpoint.json',resource)
    cert={'theorem':'FR32-CARRY1','outcome':'A','mathematical_status':'PROVED_AT_FROZEN_EXC_SCOPE','bound':'D_out<=1','sharp':True,
        'source_spec':'SOURCE_SPEC.md','proof':'FULL_PROOF.md','source_lift':'SOURCE_LIFTING_PROOF.md',
        'certificate':'threephase2_analysis.json','independent_audits':['FR32_COMPLETE_INDEPENDENT_AUDIT.json','SOURCE_CONTRACT_INDEPENDENT_AUDIT.json'],
        'external_peer_review':False,'formal_kernel_proof':False,'new_physical_owner_assignment':False,
        'branch':branch,'head':head,'tracked_tree_clean':True,'inherited_pins_preserved':len(pins['pins']),
        'Gate_U':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'}
    out('FR32_RESULT_CERTIFICATE.json',cert)
    files=[]
    for p in sorted(B.rglob('*')):
        if p.is_file() and '__pycache__' not in p.parts:files.append({'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
    pointer=B.parent/'CURRENT_CONTINUATION.md';files.append({'path':pointer.relative_to(ROOT).as_posix(),'sha256':sha(pointer),'bytes':pointer.stat().st_size})
    out('campaign_manifest.json',{'outcome':'A','files':files,'scope':'append-only FR32 continuation; immutable parent preserved','branch':branch,'head':head})
    out('publication_seal.json',{'campaign_manifest_sha256':sha(B/'campaign_manifest.json'),'file_count':len(files),
        'principal_FR32':'PROVED_AT_FROZEN_EXC_SCOPE','all4111_inherited_hashes_match':len(pins['pins'])==4111,
        'independent_same_agent_implementation_checks':'PASS','external_or_formal_audit':False})
    print(json.dumps({'status':'FR32_COMPLETION_PUBLISHED','files':len(files),'CPU':total,'groups':groups,'queries':queries,'remaining_queries':3000000-queries}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('publication_exit.json',{'metadata_CPU_excluded':time.process_time()-START,'error':error})
