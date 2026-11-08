"""Metadata only: retain every charge, increase only the authorized audit cap."""
import copy,hashlib,json,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,z):
    with p.open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    old=B/'entry_authorized1680_q3050000.json';z=json.loads(old.read_text());new=copy.deepcopy(z)
    assert z['group_caps']=={'symbolic':1680,'independent':600}
    new['group_caps']['independent']=720;new['audit_resource_amendment']='resource_amendment_audit720.json'
    save(B/'entry_authorized1680_audit720_q3050000.json',new)
    src=(B/'run_phase_1680_q3050000.py').read_text();changed=src.replace('entry_authorized1680_q3050000.json','entry_authorized1680_audit720_q3050000.json')
    assert changed.replace('entry_authorized1680_audit720_q3050000.json','entry_authorized1680_q3050000.json')==src
    with (B/'run_phase_1680_audit720_q3050000.py').open('x',encoding='utf-8') as f:f.write(changed)
    r={'authorization':'Authorize audit cap 720; keep all other caps','question_reference':'call_bcdde84037b04aac876984d138f001d2',
      'old_audit_cap':600,'new_audit_cap':720,'audit_usage_at_request':592.984375,
      'symbolic_cap':1680,'global_cap':7200,'query_cap':3050000,'query_batch':50000,'Bank25':25,
      'usage_reset':False,'every_prior_successful_and_failed_charge_retained':True,'all_other_caps_unchanged':True,
      'previous_entry_sha256':sha(old),'new_entry_sha256':sha(B/'entry_authorized1680_audit720_q3050000.json'),
      'new_controller_sha256':sha(B/'run_phase_1680_audit720_q3050000.py'),'controller_change':'entry filename only'}
    save(B/'resource_amendment_audit720.json',r);save(F/'audit_authorization_720.json',r)
    save(F/'audit_authorization_metadata_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True})
    print('AUDIT_CAP_720_RECORDED_WITH_ALL_CUMULATIVE_CHARGES_RETAINED')
if __name__=='__main__':main()
