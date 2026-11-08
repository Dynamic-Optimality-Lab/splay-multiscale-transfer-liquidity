"""Append-only checkpoint and exact cumulative resource/provenance publication."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,z):
    with p.open('x',encoding='utf8') as f:json.dump(z,f,indent=2)
def main():
    ep=B/'entry_authorized2160_audit750_q3050000.json';e=json.loads(ep.read_text());total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);q=e['inherited_conservative_queries'];runs=[]
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=json.loads((B/f"controller_{r['phase']}_exit.json").read_text());v=r['child_CPU']+c['whole_process_CPU_seconds']
        total+=v;groups[r['group']]+=v;q+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    latest=max(F.glob('full_source13_beam_*.json'));search=json.loads(latest.read_text());assert search['candidate'] is None
    assert groups['symbolic']<=2160 and groups['independent']<=750 and total<=7200 and q<=3050000
    save(F/'resources_checkpoint_04.json',{'global_CPU_before_this_publication':total,'group_CPU_before_this_publication':groups,
      'global_cap':7200,'group_caps':e['group_caps'],'queries':q,'query_cap':3050000,'query_remaining':3050000-q,
      'usage_reset':False,'Bank25':25,'query_batch_cap':50000,'live_record_cap':2000000,'DAG_cap':4000000,
      'stored_edge_cap':5000000,'memory_GiB':32,'wall_hours':12,'global_reserve':5,'controller_reserve':1,
      'all_runs_including_failures':runs,'latest_source_search':latest.name,'JR35':'OPEN','reservation':'DEFERRED',
      'publication_charge_reference':'add run_proof285_result.json and controller_proof285_exit.json'})
    names=['dependency_manifest_03.json','CHECKPOINT_04.md','symbolic_authorization_2160.json','audit_authorization_750.json',
      'NATIVE11_FULL_SOURCE_THEOREM.md','native11_full_source_certificate.json','global_probe11_H3B_DAG_01.pkl',
      'independent_probe11_LOW_B_01.json','independent_probe11_LOW_B_02.json','independent_probe11_LOW_B_03.json',
      'independent_probe11_HIGH_envelope_B01.json','independent_probe11_H3_actual_signs_B01.json','independent_native11_physical_control.json',
      'NATURAL_OWNER_CREATOR_THEOREM.md','independent_natural_owner_creator.json','FP_SI34_source_countercut.json','independent_FP_SI34_source_countercut.json',
      'NATIVE12_13_FIXED_WORD_SOURCE_THEOREMS.md','native12_HARD_word_LOW_result.pkl','native12_hard_B_word.json','independent_native12_hard_word.json',
      'native13_hard_B_word.json','ranked_source_bst.py','ranked13_LOW_build_06.pkl','ranked13_LOW_search_01.pkl',
      'independent_ranked13_word_01.json','independent_ranked13_word_02.json','audit_ranked13_word.py',
      'ARBITRARY_SUPPORT_ANCHORED_WORD_FUNDING.md','UNBOUNDED_FP_POOL_OBSTRUCTION.md','independent_AW35_UF35_proof_review.json',
      'search_full_source13_beam.py','search_full_source13_beam_v2.py','search_full_source13_beam_v3.py',latest.name,latest.with_suffix('.pkl').name]
    paths=[F/n for n in names]
    paths += [ep,B/'run_phase_2160_audit750_q3050000.py',B/'STREAMED_BLOCK_THEOREM.md',B/'OFF_PATH_LEAF_SOURCE_LIFT.md',
      P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/ABSOLUTE_PERIOD_ALIGNMENT.md']
    save(F/'dependency_manifest_04.json',{'branch':e['branch'],'head':e['head'],'input_sha256':{str(p.relative_to(P)):sha(p) for p in paths},
      'root_JR35':'OPEN','reservation':'DEFERRED','old_source_or_owners_changed':False,'Coarse_Double_counterexample':False,
      'independent_review_boundary':'same agent distinct implementation and symbolic proof inspection; not external/formal'})
    print(json.dumps({'global_before_publication':total,'group_before_publication':groups,'queries':q,'query_remaining':3050000-q,'latest_search':latest.name,'root':'OPEN'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof285_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
