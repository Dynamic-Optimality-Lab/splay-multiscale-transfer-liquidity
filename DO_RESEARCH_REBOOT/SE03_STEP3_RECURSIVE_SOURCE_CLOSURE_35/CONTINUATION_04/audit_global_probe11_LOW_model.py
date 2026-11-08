"""Nodewise independent completeness and literal source-witness audit."""
import hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:primitive=pickle.load(f)
    with (F/'global_probe11_LOW_model.pkl').open('rb') as f:m=pickle.load(f)
    AD,H=primitive['destination'],primitive['H'];classes=m['classes'];pos=m['local'];roots=primitive['roots'];total={1:0,2:0};compositions=0
    assert np.array_equal(m['B_destination'],AD) and np.array_equal(m['B_Q'],primitive['Q'])
    for g,cl in enumerate(classes,1):
        expected={(h,x):[] for h in (1,2) for x in range(1,12) if x!=g}
        for s in cl.tolist():
            for x in range(1,12):
                if x==g:continue
                h=int(H[s,x-1])
                if h in (1,2):expected[h,x].append(int(pos[s])*len(classes[x-1])+int(pos[int(AD[s,x-1])]))
            for y in np.flatnonzero(H[s]==1).tolist():
                mid=int(AD[s,y])
                for x0 in np.flatnonzero(H[mid]==1).tolist():
                    x=x0+1
                    if x==g:continue
                    t=int(AD[mid,x0]);expected[2,x].append(int(pos[s])*len(classes[x0])+int(pos[t]));compositions+=1
        for (h,x),pairs in expected.items():
            rows=m['groups'][h,g,x];nt=len(classes[x-1]);packed=rows[:,0].astype(np.int64)*nt+rows[:,1]
            assert np.array_equal(np.sort(packed),np.unique(np.array(pairs,dtype=np.int64)))
            assert len(np.unique(packed))==len(rows);total[h]+=len(rows)
            s=cl[rows[:,0]];t=classes[x-1][rows[:,1]];helpers=rows[:,2]
            direct=helpers==0
            assert np.all(H[s[direct],x-1]==h) and np.array_equal(AD[s[direct],x-1],t[direct])
            assisted=~direct
            if np.any(assisted):
                assert h==2;yy=helpers[assisted]-1;ss=s[assisted];mid=AD[ss,yy]
                assert np.all(H[ss,yy]==1) and np.all(H[mid,x-1]==1) and np.array_equal(AD[mid,x-1],t[assisted])
        assert time.process_time()-START<CAP-2
    assert total==m['H_counts'] and sum(total.values())==m['stored_source_rows']
    out={'status':'PASS_COMPLETE_ACTUAL_NATIVE11_LOW_RELATION','H1_rows':total[1],'H2_rows':total[2],
      'uncoalesced_actual_helper_compositions':compositions,'source_queries':0,'source_engine_calls':0,
      'all_rows_have_literal_full_A_witnesses':True,'completeness':'independent source-node-first enumeration, not producer root/target-first grouping',
      'JR35':'OPEN','HIGH_or_arbitrary_support_claim':False,
      'input_sha256':{p:sha(F/p) for p in ('probe11_source_actions.pkl','global_probe11_LOW_model.pkl','independent_probe11_source_actions.json')}}
    with (F/'independent_global_probe11_LOW_model.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps(out),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify118_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
