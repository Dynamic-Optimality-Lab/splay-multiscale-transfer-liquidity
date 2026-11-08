"""Explicit audit-only amendment; cumulative entry usage is unchanged."""
import copy,hashlib,json,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    with p.open('x',encoding='utf8') as f:json.dump(x,f,indent=2)
old=B/'entry_authorized2160_audit720_q3050000.json';z=json.loads(old.read_text());new=copy.deepcopy(z)
assert z['group_caps']=={'symbolic':2160,'independent':720}
new['group_caps']['independent']=750;new['audit_resource_amendment']='resource_amendment_audit750.json'
entry=B/'entry_authorized2160_audit750_q3050000.json';save(entry,new)
prior=B/'run_phase_2160_audit720_q3050000.py';src=prior.read_text();changed=src.replace(old.name,entry.name)
assert changed!=src and changed.replace(entry.name,old.name)==src
controller=B/'run_phase_2160_audit750_q3050000.py'
with controller.open('x',encoding='utf8') as f:f.write(changed)
r={'authorization':'Authorize audit cap 750; keep other caps','question_reference':'call_86d3a534b77b432ea10edc715388b0cb',
   'old_audit_cap':720,'new_audit_cap':750,'audit_usage_at_request':717.609375,'symbolic_cap':2160,
   'global_cap':7200,'query_cap':3050000,'query_batch_cap':50000,'Bank25':25,
   'all_other_caps_unchanged':True,'usage_reset':False,'all_prior_successful_and_failed_charges_retained':True,
   'prior_entry_sha256':sha(old),'entry_sha256':sha(entry),'prior_controller_sha256':sha(prior),'controller_sha256':sha(controller),
   'controller_change':'entry filename only; all accounting and safeguards unchanged'}
save(B/'resource_amendment_audit750.json',r);save(F/'audit_authorization_750.json',r)
save(F/'audit_authorization_750_metadata_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True})
print('AUDIT_750_AUTHORIZED_CUMULATIVE_OTHER_CAPS_UNCHANGED')
