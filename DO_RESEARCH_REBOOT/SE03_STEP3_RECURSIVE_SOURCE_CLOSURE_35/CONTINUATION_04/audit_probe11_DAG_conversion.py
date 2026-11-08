"""Separate complete decoder, without importing the producer DAG class."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'global_probe11_LOW_02.pkl').open('rb') as f:old=pickle.load(f)
    with (F/'global_probe11_DAG_entry.pkl').open('rb') as f:new=pickle.load(f)
    for p,h in new['input_sha256'].items():assert sha(F/p)==h
    nodes=new['nodes'];assert len(set(nodes.values()))==len(nodes)
    for i,(l,r) in nodes.items():assert l<i and r<i and not (l==r and l<0)
    values=padding=0;reach=set()
    for pid,(g,items) in old['profiles'].items():
        n=len(m['classes'][g-1]);size=1<<(n-1).bit_length();expected=dict(items);arr=np.empty(size,dtype=np.int32)
        stack=[(new['old_profile_roots'][pid],0,size)]
        while stack:
            node,start,stop=stack.pop()
            if node<0:arr[start:stop]=-node-1;continue
            assert stop-start>=2;reach.add(node);l,r=nodes[node];mid=(start+stop)//2;stack.extend(((r,mid,stop),(l,start,mid)))
        assert all(int(arr[i])==expected.get(i,0) for i in range(n)) and np.all(arr[n:]==0)
        values+=n;padding+=size-n
        if values%100000< n:assert time.process_time()-START<CAP-2
    assert set(nodes)==reach
    assert new['columns']==[new['old_profile_roots'][p] for p in old['columns']]
    assert list(new['pending'])==list(range(m['B_count'])) and all(new['inqueue'])
    out={'status':'PASS_COMPLETE_LOSSLESS_COEFFICIENT_DAG_CONVERSION','domain_coefficients_checked':values,'padding_coefficients_checked':padding,
      'DAG_nodes':len(nodes),'B_states_retained':len(new['columns']),'all_B_rescheduled':True,
      'source_queries':0,'source_engine_calls':0,'new_source_oracle_calls':False,'root_JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('global_probe11_DAG_entry.pkl','global_probe11_LOW_02.pkl','DECISION_DAG_REPRESENTATION.md')}}
    with (F/'independent_probe11_DAG_conversion.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify117_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
