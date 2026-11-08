"""Publish the five direct one-helper cases; the ten gaps follow by reflection."""
import json,pickle,time,hashlib,sys
from pathlib import Path
B=Path(__file__).resolve().parent
def main():
    cases=[]
    for p in range(1,6):
        filename='one_helper_01.pkl' if p==3 else 'one_helper_p%d_01.pkl'%p
        with (B/filename).open('rb') as f:s=pickle.load(f)
        assert not s['queue'] and max(s['level'].values())==2
        z={'status':'PRODUCER_COMPLETE_ONE_HELPER_CASE','helper_physical_rank':p,'A_anchor_count':10,'BF_anchor_count':9,'A_tree_count':16796,'BF_tree_count':4862,'state_code':'A10_index*4862+BF9_index','nonzero_debt':sorted(s['level'].items()),'omitted_debt':0,'width':2,'c':'min(H,3)','working_bank_bound':8,'source_schema_sha256':hashlib.sha256((B/'ten_anchor_LOW_source_schemas.json').read_bytes()).hexdigest(),'BF_primitive_sha256':hashlib.sha256((B/'nine_label_native_action_cache.json').read_bytes()).hexdigest(),'principal_U33':'OPEN'}
        name='one_helper_p%d_certificate.json'%p
        with (B/name).open('x') as f:json.dump(z,f,separators=(',',':'))
        cases.append({'helper':p,'nonzero_coefficients':len(s['level']),'file':name,'sha256':hashlib.sha256((B/name).read_bytes()).hexdigest()});del s,z
    with (B/'one_helper_source_registry.json').open('x') as f:json.dump({'status':'FIVE_DIRECT_SOURCE_CASES_EXPORTED_AUDIT_PENDING','direct':cases,'all_ordered_helper_positions':[{'helper':p,'direct_case':min(p,11-p),'reflect_both_trees':p>5} for p in range(1,11)],'reflection':'Aphysical key k->11-k; BF normalized Score i->10-i; helper p->11-p','principal_U33':'OPEN'},f,indent=2)
    print(json.dumps({'status':'FIVE_SOURCE_CASES_EXPORTED','cases':cases}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof19_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
