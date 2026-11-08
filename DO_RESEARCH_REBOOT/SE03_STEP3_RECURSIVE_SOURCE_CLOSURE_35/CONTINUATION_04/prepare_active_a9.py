"""Accepted exact native cache projection to nine active anchors."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    native=read(B/'native10_source_actions.json');prior=read(F/'active_a8_model.json')
    def eligible(t):
        if isinstance(t,str):return True
        if t[0]==9:return t[2]==[10,'F9','F10']
        if t[0]>9:return False
        return eligible(t[1]) and eligible(t[2])
    ids=[i for i,t in enumerate(native['trees']) if eligible(t)];assert len(ids)==4862
    loc={a:i for i,a in enumerate(ids)}
    def project(t):
        if isinstance(t,str) or t[0]>9:return None
        return [t[0],project(t[1]),project(t[2])]
    AD=[];AH=[];trees=[]
    for a in ids:
        ds=native['destination'][a][:9];assert all(d in loc for d in ds)
        AD.append([loc[d] for d in ds]);AH.append(native['H'][a][:9]);trees.append(project(native['trees'][a]))
    z={'status':'EXACT_NATIVE_A9_FULL_MAXIMAL_B_MODEL','A_trees':trees,'A_roots':[t[0] for t in trees],
       'A_destination':AD,'A_H':AH,'A_native10_indices':ids,'A_native10_columns':list(range(9)),
       'B_roots':prior['B_roots'],'B_edges':prior['B_edges'],'B_count':3876,'A_count':4862,
       'mark_ranks':[1,3,5,6,7,8,9],'helper_ranks':[2,4],
       'native_cache_sha256':sha(B/'native10_source_actions.json'),
       'input_sha256':{'active_a8_model.json':sha(F/'active_a8_model.json')},
       'storage':'only positive boundary potential cells are live; all zero cells implicit, per-B transient A envelope discarded before next column',
       'source_queries':0,'source_engine_calls':0,'JR35':'OPEN'}
    with (F/'active_a9_model.json').open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
    print(json.dumps({k:z[k] for k in ('status','A_count','B_count','mark_ranks','source_queries')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof196_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
