"""Metadata-only authorization; cumulative accounting is unchanged."""
import copy,hashlib,json,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    old= B/'entry_authorized3050000.json';z=json.loads(old.read_text());new=copy.deepcopy(z)
    assert z['group_caps']['symbolic']==1440 and z['query_limit']==3050000
    new['group_caps']['symbolic']=1680;new['symbolic_resource_amendment']='resource_amendment_1680.json'
    save(B/'entry_authorized1680_q3050000.json',new)
    source=(B/'run_phase_3050000.py').read_text();changed=source.replace('entry_authorized3050000.json','entry_authorized1680_q3050000.json')
    assert changed!=source and changed.replace('entry_authorized1680_q3050000.json','entry_authorized3050000.json')==source
    with (B/'run_phase_1680_q3050000.py').open('x',encoding='utf-8') as f:f.write(changed)
    r={'authorization':'Authorize symbolic cap 1,680; keep all other caps',
       'question_reference':'call_8e38df25ce794557ba33d1a5a284716c',
       'old_symbolic_cap':1440,'new_symbolic_cap':1680,'symbolic_usage_at_request':1429.28125,
       'independent_cap':600,'global_cap':7200,'query_cap':3050000,'query_batch':50000,'Bank25':25,
       'all_other_caps_unchanged':True,'usage_reset':False,'prior_successful_and_failed_charges_retained':True,
       'prior_entry_sha256':sha(old),'new_entry_sha256':sha(B/'entry_authorized1680_q3050000.json'),
       'prior_controller_sha256':sha(B/'run_phase_3050000.py'),'controller_sha256':sha(B/'run_phase_1680_q3050000.py'),
       'controller_change':'entry filename only; no accounting or safeguard change',
       'purpose':'remaining source-lifting and joint-repayment proof work, not automatic promotion from finite certificates'}
    save(B/'resource_amendment_1680.json',r);save(F/'symbolic_authorization_1680.json',r)
    save(F/'symbolic_authorization_metadata_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True})
    print('SYMBOLIC_CAP_1680_AUTHORIZED_CUMULATIVE_ACCOUNTING_UNCHANGED')
if __name__=='__main__':main()
