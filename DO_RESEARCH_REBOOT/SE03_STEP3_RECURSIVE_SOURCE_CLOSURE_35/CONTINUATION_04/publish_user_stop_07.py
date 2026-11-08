"""Stopping-point publication only; no new research or ordinary source evaluations."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ep=B/'entry_authorized2640_audit750_q3100000.json';e=json.loads(ep.read_text(encoding='utf-8-sig'));g=dict(e['inherited_group_CPU']);total=e['prior_uniform_CPU'];q=e['inherited_conservative_queries']
    for p in B.glob('run_*_result.json'):
        r=json.loads(p.read_text());c=json.loads((B/f"controller_{r['phase']}_exit.json").read_text());v=r['child_CPU']+c['whole_process_CPU_seconds'];total+=v;g[r['group']]+=v;q+=r.get('source_queries',0)
    assert total==6379.53125 and g=={'symbolic':2440.125,'independent':738.03125} and q==3050192
    paths=[F/n for n in ['CHECKPOINT_07_USER_STOP.md','dependency_manifest_06.json','independent_checkpoint06_provenance.json',
      'query_authorization_3100000.json','symbolic_authorization_2640.json','EIGHT_CORE_SOURCE_FALSIFICATION_BOX.md',
      'eight_core_B_source_01.json','eight_core_B_source_01.pkl','eight_core_B_cycles.json',
      'eight_core_B_source_reach_prefix.json','fixed_B8_full_A_02.json','fixed_B8_full_A_02.pkl',
      'build_eight_core_source_falsifier.py','select_eight_core_B_cycles.py','search_fixed_B8_full_A.py',
      'derive_eight_core_source_reach_prefix.py','publish_user_stop_07.py']]+[ep,B/'run_phase_2640_audit750_q3100000.py']
    out={'status':'STOPPED_AT_EXPLICIT_USER_REQUEST','global_CPU_before_publication':total,'group_CPU_before_publication':g,
      'caps':{'global':7200,'symbolic':2640,'independent':750,'queries':3100000,'query_batch':50000,'Bank25':25},
      'queries':q,'queries_remaining':3100000-q,'publication_charge_reference':['run_proof296_result.json','controller_proof296_exit.json'],
      'JR35':'OPEN','reservation':'DEFERRED','source_workers_running':False,'old_sources_or_owners_changed':False,
      'query_and_symbolic_authorizations_are_cumulative':True,'usage_reset':False,
      'input_sha256':{str(p.relative_to(P)):sha(p) for p in paths}}
    with (F/'resources_stop_07.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof296_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
