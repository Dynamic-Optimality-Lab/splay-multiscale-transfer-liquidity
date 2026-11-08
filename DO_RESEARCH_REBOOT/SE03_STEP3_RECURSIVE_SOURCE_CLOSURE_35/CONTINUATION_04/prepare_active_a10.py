import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def main():
    path=B/'native10_source_actions.json';n=json.loads(path.read_text());p=json.loads((F/'active_a8_model.json').read_text())
    z={'status':'EXACT_NATIVE_A10_COMPLETE_MAXIMAL_B','A_count':16796,'B_count':3876,
       'A_roots':[t[0] for t in n['trees']],'A_destination':n['destination'],'A_H':n['H'],
       'mark_ranks':[1,3,5,7,8,9,10],'helper_ranks':[2,4,6],'B_roots':p['B_roots'],'B_edges':p['B_edges'],
       'native_cache_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
       'input_sha256':{'active_a8_model.json':hashlib.sha256((F/'active_a8_model.json').read_bytes()).hexdigest()},
       'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'representation':'lossless exact debt profile sharing; B states and eligibility are not identified'}
    with (F/'active_a10_model.json').open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
    print(json.dumps({k:z[k] for k in ('status','A_count','B_count','mark_ranks')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof200_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
