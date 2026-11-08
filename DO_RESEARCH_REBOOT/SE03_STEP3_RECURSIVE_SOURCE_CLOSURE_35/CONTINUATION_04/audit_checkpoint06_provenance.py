"""Audit only the NEW publication and query-controller amendment, not old source runs."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    old=read(B/'entry_authorized2400_audit750_q3050000.json');new=read(B/'entry_authorized2400_audit750_q3100000.json')
    assert set(old)==set(new)
    changed={k for k in old if old[k]!=new[k]};assert changed=={'remaining_conservative_queries','query_limit','query_resource_amendment'}
    assert new['remaining_conservative_queries']-old['remaining_conservative_queries']==50000
    assert new['query_limit']==3100000 and new['inherited_conservative_queries']+new['remaining_conservative_queries']==3100000
    assert new['group_caps']=={'symbolic':2400,'independent':750}
    ot=(B/'run_phase_2400_audit750_q3050000.py').read_text(encoding='utf-8-sig').rstrip()
    nt=(B/'run_phase_2400_audit750_q3100000.py').read_text(encoding='utf-8-sig').rstrip()
    assert nt==ot.replace('entry_authorized2400_audit750_q3050000.json','entry_authorized2400_audit750_q3100000.json')
    auth=read(F/'query_authorization_3100000.json');assert auth['charged_queries_at_authorization']==3050000 and not auth['usage_reset']
    mf=read(F/'dependency_manifest_06.json')
    for p,h in mf['input_sha256'].items():assert sha(P/p)==h
    assert mf['root_JR35']=='OPEN' and mf['reservation']=='DEFERRED' and not mf['old_source_or_owners_changed']
    ck=read(F/'resources_checkpoint_06.json');groups=dict(new['inherited_group_CPU']);total=new['prior_uniform_CPU'];q=new['inherited_conservative_queries'];post=[]
    for p in B.glob('run_*_result.json'):
        r=read(p);c=read(B/f"controller_{r['phase']}_exit.json");charge=r['child_CPU']+c['whole_process_CPU_seconds']
        if r['phase']=='proof293':post.append(charge);continue
        total+=charge;groups[r['group']]+=charge;q+=r.get('source_queries',0)
    assert total==ck['global_CPU_before_this_publication'] and groups==ck['group_CPU_before_this_publication'] and q==ck['queries']==3050000
    assert len(post)==1 and groups['symbolic']+post[0]==2390.4375
    out={'status':'PASS_CHECKPOINT06_PINS_CUMULATIVE_QUERY_AMENDMENT_AND_CHARGES',
      'manifest_pins_checked':len(mf['input_sha256']),'query_cap':3100000,'charged_queries':q,'query_remaining':50000,
      'symbolic_CPU_after_publication':groups['symbolic']+post[0],'symbolic_cap':2400,
      'no_controller_logic_change':True,'no_cumulative_reset':True,'source_queries':0,'source_engine_calls':0,
      'new_USR35_uniform_proof_receipts':'verify156/verify157; same-agent distinct implementation and static proof review, not external/formal',
      'JR35':'OPEN','reservation':'DEFERRED','input_sha256':{str(p):sha(p) for p in (F/'dependency_manifest_06.json',F/'resources_checkpoint_06.json',F/'query_authorization_3100000.json',F/'audit_checkpoint06_provenance.py')}}
    with (F/'independent_checkpoint06_provenance.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify158_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
