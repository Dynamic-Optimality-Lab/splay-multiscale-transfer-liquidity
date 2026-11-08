"""Publish exact cumulative receipts and new all-support source proof pins."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,z):
    with p.open('x',encoding='utf8') as f:json.dump(z,f,indent=2)
def main():
    ep=B/'entry_authorized2400_audit750_q3100000.json';e=json.loads(ep.read_text(encoding='utf-8-sig'));total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);q=e['inherited_conservative_queries'];runs=[]
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=json.loads((B/f"controller_{r['phase']}_exit.json").read_text());v=r['child_CPU']+c['whole_process_CPU_seconds']
        total+=v;groups[r['group']]+=v;q+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    latest=max(F.glob('full_source15_beam_*.json'));search=json.loads(latest.read_text());assert search['candidate'] is None
    assert groups['symbolic']<=2400 and groups['independent']<=750 and total<=7200 and q<=3100000
    for name,status in [('independent_USR35.json','PASS_USR35_UNIFORM_PROOF_REVIEW_WITH_M4_SOURCE_CONTROL'),('independent_USR35_all_support.json','PASS_USR35_R_ALL_SUPPORT_SOURCE_LIFT_AND_CAPACITY_REVIEW')]:
        r=json.loads((F/name).read_text());assert r['status']==status
        for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    save(F/'resources_checkpoint_06.json',{'global_CPU_before_this_publication':total,'group_CPU_before_this_publication':groups,
      'global_cap':7200,'group_caps':e['group_caps'],'queries':q,'query_cap':3100000,'query_remaining':3100000-q,
      'usage_reset':False,'Bank25':25,'query_batch_cap':50000,'live_record_cap':2000000,'DAG_cap':4000000,
      'stored_edge_cap':5000000,'memory_GiB':32,'wall_hours':12,'global_reserve':5,'controller_reserve':1,
      'all_runs_including_failures':runs,'latest_source_search':latest.name,'JR35':'OPEN','reservation':'DEFERRED',
      'publication_charge_reference':'add run_proof293_result.json and controller_proof293_exit.json'})
    names=['dependency_manifest_05.json','CHECKPOINT_06.md','query_authorization_3100000.json',
      'UNBOUNDED_SHARED_RETURN_SOURCE_FAMILY.md','ALL_SUPPORT_RETURN_ESCAPE_NECESSITY.md',
      'construct_USR35_control.py','USR35_m4_control.json','audit_USR35.py','independent_USR35.json',
      'audit_USR35_all_support.py','independent_USR35_all_support.json','search_full_source15_beam_last_queries.py',
      'publish_joint_repayment_checkpoint_06.py',latest.name,latest.with_suffix('.pkl').name]
    paths=[F/n for n in names]+[ep,B/'run_phase_2400_audit750_q3100000.py',B/'resource_amendment_3100000.json',B/'STREAMED_BLOCK_THEOREM.md']
    save(F/'dependency_manifest_06.json',{'branch':e['branch'],'head':e['head'],'input_sha256':{str(p.relative_to(P)):sha(p) for p in paths},
      'root_JR35':'OPEN','reservation':'DEFERRED','MFR_frozen_all_return_rule':'UNBOUNDED_SOURCE_DEFICIENCY_EVERY_SUPPORT_R_GE_11',
      'new_source_full_cost_status':'all specified sources funded with natural h0, distinct earlier tails and static Bank25; not CD counterexamples',
      'old_source_or_owners_changed':False,'independent_review_boundary':'same agent distinct implementation/proof review; not external or formal'})
    print(json.dumps({'global_before_publication':total,'groups_before_publication':groups,'queries':q,'query_remaining':3100000-q,
      'latest_source_search':latest.name,'JR35':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof293_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
