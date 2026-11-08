"""Metadata-only explicit user cap amendment; every usage stays cumulative."""
import copy,hashlib,json,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,x):
    with p.open('x',encoding='utf8') as f:json.dump(x,f,indent=2)
def main():
    old=B/'entry_authorized1680_audit720_q3050000.json';z=json.loads(old.read_text());new=copy.deepcopy(z)
    assert z['group_caps']=={'symbolic':1680,'independent':720} and z['query_limit']==3050000
    new['group_caps']['symbolic']=1920;new['symbolic_resource_amendment']='resource_amendment_1920.json'
    entry=B/'entry_authorized1920_audit720_q3050000.json';save(entry,new)
    oldcontroller=B/'run_phase_1680_audit720_q3050000.py';text=oldcontroller.read_text();changed=text.replace(old.name,entry.name)
    assert changed!=text and changed.replace(entry.name,old.name)==text
    controller=B/'run_phase_1920_audit720_q3050000.py'
    with controller.open('x',encoding='utf8') as f:f.write(changed)
    r={'authorization':'Authorize symbolic cap 1,920; keep all other caps','question_reference':'call_f06bec57ae354b5e9e177b797d532a31',
      'old_symbolic_cap':1680,'new_symbolic_cap':1920,'symbolic_usage_at_request':1675.59375,
      'independent_cap':720,'global_cap':7200,'query_cap':3050000,'query_batch_cap':50000,'Bank25':25,
      'all_other_caps_unchanged':True,'usage_reset':False,'all_prior_successful_and_failed_charges_retained':True,
      'prior_entry_sha256':sha(old),'entry_sha256':sha(entry),'prior_controller_sha256':sha(oldcontroller),'controller_sha256':sha(controller),
      'controller_change':'entry filename only; all accounting and safeguards unchanged',
      'purpose':'actual-source counterexample search and uniform source donor proof; passing bounded checks do not prove JR35'}
    save(B/'resource_amendment_1920.json',r);save(F/'symbolic_authorization_1920.json',r)
    save(F/'symbolic_authorization_1920_metadata_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True})
    print('SYMBOLIC_1920_AUTHORIZED_CUMULATIVE_ALL_OTHER_CAPS_UNCHANGED')
if __name__=='__main__':main()
