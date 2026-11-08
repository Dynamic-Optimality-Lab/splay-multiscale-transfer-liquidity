"""Pin the focused outcome P and exact cumulative research charges."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,z):
    with (F/name).open('x',encoding='utf8') as f:json.dump(z,f,indent=2)
def main():
    ep=B/'entry_authorized2640_audit750_q3100000.json';e=json.loads(ep.read_text(encoding='utf-8-sig'));g=dict(e['inherited_group_CPU']);total=e['prior_uniform_CPU'];q=e['inherited_conservative_queries'];newruns=[]
    for p in B.glob('run_*_result.json'):
        r=json.loads(p.read_text());c=json.loads((B/f"controller_{r['phase']}_exit.json").read_text());v=r['child_CPU']+c['whole_process_CPU_seconds'];total+=v;g[r['group']]+=v;q+=r.get('source_queries',0)
        if r['phase'] in ['core78','core79','proof297','proof298','proof299','proof300','proof301','proof302','verify159']:newruns.append({'phase':r['phase'],'group':r['group'],'CPU':v,'queries':r.get('source_queries',0),'status':r['status']})
    assert g['symbolic']<2640 and g['independent']<750 and total<7200 and q<=3100000
    a=json.loads((F/'independent_audit.json').read_text());assert a['status']=='PASS_ND08_UNIFORM_PARTIAL_PROOFS_AND_DISTINCT_SOURCE_CHALLENGES'
    for p,h in a['input_sha256'].items():assert sha(Path(p))==h
    save('resources_checkpoint.json',{'global_CPU_before_publication':total,'group_CPU_before_publication':g,'caps':{'global':7200,'symbolic':2640,'independent':750,'queries':3100000,'query_batch':50000,'Bank25':25},
      'queries':q,'query_remaining':3100000-q,'new_phase_receipts_including_failures':sorted(newruns,key=lambda x:x['phase']),
      'usage_reset':False,'other_caps_unchanged':True,'publication_charge_reference':['run_proof303_result.json','controller_proof303_exit.json'],
      'outcome':'P','Objective_I':'OPEN','Objective_II':'DEFERRED'})
    docs=[p for p in F.iterdir() if p.is_file() and p.name not in ('manifest.json','resources_checkpoint.json')]
    inherited=[C/'CONTINUATION_04/NEUTRAL_DOUBLE_SOURCE_DECOMPOSITION.md',C/'CONTINUATION_04/ND35_CSL35_PROOF_REVIEW.md',C/'CONTINUATION_04/independent_core_sector_neutral.json',
      C/'CONTINUATION_04/resources_stop_07.json',C/'CONTINUATION_04/symbolic_authorization_2640.json',C/'CONTINUATION_04/query_authorization_3100000.json',
      C/'CONTINUATION_02/GLOBAL_FULL_H_AND_FROZEN_EXCHANGE.md',B/'STREAMED_BLOCK_THEOREM.md',B/'audit_core39.py',B/'audit_verify79.py',ep,B/'run_phase_2640_audit750_q3100000.py']
    save('manifest.json',{'branch':e['branch'],'head':e['head'],'outcome':'P','uniform_partial_result':'ND35 raw universe audited; ZRC35 pays all terminal neutral demands while preserving original g+',
      'remaining_universal_class':'strictly internal neutral doubles with joint cyclic/shared capacity','Objective_I':'OPEN','Objective_II':'DEFERRED','no_CD_counterexample':True,
      'new_independent_status':a['status'],'old_owners_or_sources_modified':False,'source_search_resumed':False,
      'input_sha256':{str(p.relative_to(P)):sha(p) for p in docs+inherited}})
    print(json.dumps({'outcome':'P','global_before_publication':total,'groups_before_publication':g,'queries':q,'query_remaining':3100000-q,'Objective_I':'OPEN','ZRC35':'PROVED_AT_STATED_PARTIAL_SCOPE'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof303_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
