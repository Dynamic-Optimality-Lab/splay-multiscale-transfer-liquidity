"""Export the independently checked native10 debt unchanged."""
import json,pickle,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    audit=json.loads((B/'native10_complete_independent_audit.json').read_text());assert audit['status']=='PASS_COMPLETE_NATIVE10_SOURCE_CREDIT_CERTIFICATE'
    path=B/'native10_debt_03.pkl';assert hashlib.sha256(path.read_bytes()).hexdigest()==audit['input_sha256']
    with path.open('rb') as f:s=pickle.load(f)
    assert not s['queue'] and max(s['level'].values())==3
    z={'status':'INDEPENDENTLY_CHECKED_NATIVE10_SOURCE_CREDIT_CERTIFICATE','anchor_count':10,'tree_count':16796,'state_code':'min(A*16796+B,reflect(A)*16796+reflect(B))','nonzero_debt':sorted(s['level'].items()),'omitted_debt':0,'width':3,'c':'min(H,3)','working_bound':9,'source_actions_sha256':hashlib.sha256((B/'native10_source_actions.json').read_bytes()).hexdigest(),'checked_input_pickle_sha256':audit['input_sha256'],'audit_sha256':hashlib.sha256((B/'native10_complete_independent_audit.json').read_bytes()).hexdigest(),'scope':'fixed ten-anchor A/B backbones, original operations on anchors, arbitrary rigid unaccessed private gaps','principal_U33':'OPEN'}
    with (B/'native10_credit_certificate.json').open('x') as f:json.dump(z,f,separators=(',',':'))
    print(json.dumps({'status':z['status'],'coefficients':len(s['level']),'width':3,'working_bound':9}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof27_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
