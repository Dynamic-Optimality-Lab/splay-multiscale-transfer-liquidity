"""Attack image-preserving debt/owner splices on the exact frozen examples.
No source is regenerated and no desired global capacity is assumed.
"""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def unpack(v):return {tuple(z['demand']):tuple(z['unit']) for z in v}
def main():
    reports=[]
    for name in ('leaf_source_certificates2.json','zero_run_source_certificates.json'):
        data=json.loads((B/name).read_text())
        for f in data['reports']:
            if not f['owners']:continue
            h=unpack(f['leaf_partial_h']);a=unpack(f['owners']['prior']);fresh=set(h.values())-set(a.values())
            reports.append({'source':name,'source_sha256':hashlib.sha256((B/name).read_bytes()).hexdigest(),
                'r':f['r'],'reflected':f['mirrored'],'comparison_image':len(h),'prior_paid':len(a),
                'comparison_units_outside_old_image':sorted(fresh),'all_comparison_units_already_owned':not fresh,
                'claim_if_all_owned':'No operation preserving this candidate donor IMAGE and all a values can pay any additional root. A genuinely new source unit or a different donor image is required; full U is not refuted.'})
    out('splice_image_audit.json',{'status':'EXACT_SOURCE_CANDIDATE_IMAGE_AUDIT','reports':reports,'source_engine_calls':0})
    print(json.dumps({'status':'IMAGE_SPLICE_AUDIT_COMPLETED','results':[{k:v for k,v in r.items() if k not in ('source_sha256','claim_if_all_owned','comparison_units_outside_old_image')} for r in reports]}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_splice_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0})
