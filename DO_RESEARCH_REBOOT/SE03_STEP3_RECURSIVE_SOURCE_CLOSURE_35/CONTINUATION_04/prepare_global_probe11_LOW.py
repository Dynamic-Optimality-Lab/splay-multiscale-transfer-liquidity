"""All literal one/two-event natural A source rows; no HIGH quotient."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:z=pickle.load(f)
    n=len(z['trees']);ad=z['destination'];H=z['H'];roots=z['roots'];classes=[np.flatnonzero(roots==g).astype(np.int32) for g in range(1,12)]
    local=np.empty(n,dtype=np.int32)
    for cl in classes:local[cl]=np.arange(len(cl))
    groups={};edges=0;hcounts={1:0,2:0}
    for g in range(1,12):
        cl=classes[g-1]
        for x in range(1,12):
            if x==g:continue
            s=cl[H[cl,x-1]==1];t=ad[s,x-1];groups[1,g,x]=np.column_stack((local[s],local[t],np.zeros(len(s),dtype=np.int32)));hcounts[1]+=len(s)
            s=cl[H[cl,x-1]==2];ss=[local[s]];tt=[local[ad[s,x-1]]];yy=[np.zeros(len(s),dtype=np.int32)]
            for y in range(1,12):
                src=cl[H[cl,y-1]==1];mid=ad[src,y-1];ok=H[mid,x-1]==1;s=src[ok];end=ad[mid[ok],x-1]
                ss.append(local[s]);tt.append(local[end]);yy.append(np.full(len(s),y,dtype=np.int32))
            s,t,y=map(np.concatenate,(ss,tt,yy));key=s.astype(np.int64)*len(classes[x-1])+t
            _,idx=np.unique(key,return_index=True);groups[2,g,x]=np.column_stack((s[idx],t[idx],y[idx]));hcounts[2]+=len(idx)
    edges=sum(len(v) for v in groups.values());assert edges<4000000
    out={'status':'EXACT_ALL_ELEVEN_KEY_NATURAL_LOW_ROWS','A_count':n,'B_count':n,'classes':classes,'local':local,'groups':groups,
      'roots':roots,'B_destination':ad,'B_Q':z['Q'],'H_counts':hcounts,'stored_source_rows':edges,
      'source_queries':0,'source_engine_calls':0,'input_sha256':{'source':sha(F/'probe11_source_actions.pkl'),'audit':sha(F/'independent_probe11_source_actions.json')},
      'negative_cycle_is_actual_source_candidate':True,'positive_result_not_full_JR35':True}
    with (F/'global_probe11_LOW_model.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k not in ('classes','local','groups','roots','B_destination','B_Q')}
    with (F/'global_probe11_LOW_model.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof230_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
