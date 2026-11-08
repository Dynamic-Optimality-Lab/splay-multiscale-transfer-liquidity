"""Metadata-only recording of explicit user query-cap authorization; no reset."""
import hashlib,json,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,z):
    with p.open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    old=B/'run_phase_1440.py';assert sha(old)=='f630e39f4fac093f3ab62cf6458dacbda7d17ac4e8e83be83c215a212e1cb40f'
    entry=json.loads((B/'entry_authorized1440.json').read_text());new=dict(entry)
    new['remaining_conservative_queries']+=50000;new['query_limit']=3050000
    new['query_resource_amendment']='resource_amendment_3050000.json'
    save(B/'entry_authorized3050000.json',new)
    text=old.read_text();changed=text.replace('entry_authorized1440.json','entry_authorized3050000.json')
    assert changed!=text and changed.replace('entry_authorized3050000.json','entry_authorized1440.json')==text
    with (B/'run_phase_3050000.py').open('x',encoding='utf-8') as f:f.write(changed)
    amendment={'authorization':'Authorize 50,000 additional queries; keep other caps',
      'question_reference':'call_bfaf6ce77f33444aae8e1aaf4ddb1cd2',
      'old_query_cap':3000000,'new_query_cap':3050000,'additional_queries':50000,
      'cumulative_queries_before':2999999,'remaining_before':1,'remaining_after':50001,
      'symbolic_cap':1440,'independent_cap':600,'global_cap':7200,'phase_batch_queries':50000,'Bank25':25,
      'CPU_caps_or_prior_usage_changed':False,'usage_reset':False,
      'prior_entry_sha256':sha(B/'entry_authorized1440.json'),'new_entry_sha256':sha(B/'entry_authorized3050000.json'),
      'original_controller_sha256':sha(old),'amended_controller_sha256':sha(B/'run_phase_3050000.py'),
      'controller_change':'entry filename only; all CPU/query accounting, phase limits and verifier safeguards unchanged',
      'purpose':'complete source-exact seven-key maximal-core B transition construction and distinct verification; passing is not universal Joint Repayment'}
    save(B/'resource_amendment_3050000.json',amendment);save(F/'query_authorization.json',amendment)
    save(F/'query_authorization_metadata_exit.json',{'whole_process_CPU_seconds':time.process_time(),'metadata_only':True})
    print('QUERY_CAP_3050000_AUTHORIZATION_RECORDED_WITH_CUMULATIVE_USAGE_UNCHANGED')
if __name__=='__main__':main()
