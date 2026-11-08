"""Independent static HIGH envelope for an immutable candidate debt.
A failed sufficient envelope is not an actual source counterexample.
"""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    with (F/'global_probe11_DAG_06.pkl').open('rb') as f:z=pickle.load(f)
    au=json.loads((F/'independent_probe11_DAG_checkpoint_06.json').read_text());assert au['input_sha256']['global_probe11_DAG_06.pkl']==sha(F/'global_probe11_DAG_06.pkl')
    nodes=z['nodes'];minimum={};maximum={}
    def lo(i):return -i-1 if i<0 else minimum[i]
    def hi(i):return -i-1 if i<0 else maximum[i]
    for i in sorted(nodes):
        l,r=nodes[i];assert l<i and r<i;minimum[i]=min(lo(l),lo(r));maximum[i]=max(hi(l),hi(r))
    def prefix_min(i,n,width):
        if i<0 or n==width:return lo(i)
        l,r=nodes[i];half=width//2
        if n<=half:return prefix_min(l,n,half)
        return min(lo(l),prefix_min(r,n-half,half))
    ranges={}
    for g,i in set((int(g),i) for g,i in zip(m['roots'],z['columns'])):
        n=len(m['classes'][g-1]);ranges[g,i]=(prefix_min(i,n,1<<(n-1).bit_length()),hi(i))
    mn=np.array([ranges[int(g),i][0] for g,i in zip(m['roots'],z['columns'])],dtype=np.int16)
    mx=np.array([ranges[int(g),i][1] for g,i in zip(m['roots'],z['columns'])],dtype=np.int16)
    margins=6-m['B_Q'].astype(np.int16)+mn[m['B_destination']]-mx[:,None]
    genuine=m['roots'][:,None]!=(np.arange(11)+1)[None,:];count=int(genuine.sum());worst=int(margins[genuine].min());fail=np.argwhere(genuine&(margins<0))
    failures=[{'B_source':int(b),'KEEP':int(x+1),'B_target':int(m['B_destination'][b,x]),'Q':int(m['B_Q'][b,x]),
      'D_source_max':int(mx[b]),'D_target_min':int(mn[m['B_destination'][b,x]]),'margin':int(margins[b,x]),
      'does_not_assert_H3_endpoint_realizability':True} for b,x in fail[:20].tolist()]
    out={'status':'PASS_ALL_HIGH_ANY_ENDPOINTS_FOR_THIS_CANDIDATE' if not len(fail) else 'SUFFICIENT_HIGH_ENVELOPE_NOT_PROVED',
      'genuine_B_edges':count,'minimum_margin':worst,'failed_envelopes':len(fail),'first_failures':failures,
      'candidate':'global_probe11_DAG_06.pkl','HIGH_threshold_H':3,'selected_actual_events_c':3,
      'scope':'eleven fixed ordered physical anchors and original accesses to anchors; arbitrary rigid untouched ordered payloads',
      'source_queries':0,'source_engine_calls':0,'LOW_closed':False,'physical_funding_injection_claimed':False,'JR35':'OPEN',
      'input_sha256':{p:sha(F/p) for p in ('global_probe11_DAG_06.pkl','global_probe11_LOW_model.pkl','independent_probe11_DAG_checkpoint_06.json','independent_probe11_source_actions.json')}}
    with (F/'independent_probe11_HIGH_envelope_06.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('first_failures','input_sha256')}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify121_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
