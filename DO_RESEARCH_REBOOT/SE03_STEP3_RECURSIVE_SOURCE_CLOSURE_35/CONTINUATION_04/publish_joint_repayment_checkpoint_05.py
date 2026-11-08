"""Pin the new source refutation/proofs and retain exact cumulative caps."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,z):
    with p.open('x',encoding='utf8') as f:json.dump(z,f,indent=2)
def main():
    ep=B/'entry_authorized2400_audit750_q3050000.json';e=json.loads(ep.read_text());total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);q=e['inherited_conservative_queries'];runs=[]
    for p in sorted(B.glob('run_*_result.json')):
        r=json.loads(p.read_text());c=json.loads((B/f"controller_{r['phase']}_exit.json").read_text());v=r['child_CPU']+c['whole_process_CPU_seconds']
        total+=v;groups[r['group']]+=v;q+=r.get('source_queries',0)
        runs.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    latest=max(F.glob('full_source15_beam_*.json'));search=json.loads(latest.read_text());assert search['candidate'] is None
    assert groups['symbolic']<=2400 and groups['independent']<=750 and total<=7200 and q<=3050000
    save(F/'resources_checkpoint_05.json',{'global_CPU_before_this_publication':total,'group_CPU_before_this_publication':groups,
      'global_cap':7200,'group_caps':e['group_caps'],'queries':q,'query_cap':3050000,'query_remaining':3050000-q,
      'usage_reset':False,'Bank25':25,'query_batch_cap':50000,'live_record_cap':2000000,'DAG_cap':4000000,
      'stored_edge_cap':5000000,'memory_GiB':32,'wall_hours':12,'global_reserve':5,'controller_reserve':1,
      'all_runs_including_failures':runs,'latest_source_search':latest.name,'JR35':'OPEN','reservation':'DEFERRED',
      'publication_charge_reference':'add run_proof291_result.json and controller_proof291_exit.json'})
    names=['dependency_manifest_04.json','CHECKPOINT_05.md','symbolic_authorization_2400.json',
      'BALANCED_LOCAL_ALPHABET_COMPOSITION.md','independent_BLC35_proof_review.json',
      'REVERSE_LOSS_COLLISION_NORMAL_FORM.md','independent_RLC35_and_B_only_control.json',
      'MAXIMAL_SELF_FRINGE_RETURN_THEOREM.md','independent_MFR35_theorem.json',
      'MFR35_CANDIDATE_STATUS.md','MFR35_all_return_options.json','independent_MFR35_all_return_control.json',
      'SS_SPLAY_INVERSE_SOURCE_THEOREM.md','MFR35_ALL_RETURN_SOURCE_REFUTATION.md','MFR35_unpaid_source_countercut.json',
      'construct_MFR35_source_countercut.py','independent_MFR35_unpaid_source_countercut.json',
      'SOURCE_REPAIR_OF_RETURN_COUNTERCUT.md','independent_return_countercut_repair.json',
      'source13_tight_graph_01.pkl','source13_tight_cycle_extraction.json','maximal_B_only_bound_result.json',
      'ranked_source_bst15.py','search_full_source15_beam.py','search_full_source15_beam_v2.py',
      'search_full_source15_beam_fullA.py','search_full_source15_beam_fullAB.py',
      'search_full_source15_beam_fullAB_reserve8.py','search_full_source15_beam_diverse.py',latest.name,latest.with_suffix('.pkl').name]
    paths=[F/n for n in names]+[ep,B/'run_phase_2400_audit750_q3050000.py',B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md',B/'STREAMED_BLOCK_THEOREM.md']
    save(F/'dependency_manifest_05.json',{'branch':e['branch'],'head':e['head'],'input_sha256':{str(p.relative_to(P)):sha(p) for p in paths},
      'root_JR35':'OPEN','reservation':'DEFERRED','MFR_frozen_all_return_rule':'REFUTED_SOURCE_EXACT',
      'new_source_full_cost_status':'funded with h0, earlier tails and original Bank25; not a CD counterexample',
      'old_source_or_owners_changed':False,'independent_review_boundary':'same agent, distinct implementation/proof review; not external/formal'})
    print(json.dumps({'global_before_publication':total,'groups_before_publication':groups,'queries':q,'query_remaining':3050000-q,
      'latest_source_search':latest.name,'JR35':'OPEN','MFR_rule':'REFUTED'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof291_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
