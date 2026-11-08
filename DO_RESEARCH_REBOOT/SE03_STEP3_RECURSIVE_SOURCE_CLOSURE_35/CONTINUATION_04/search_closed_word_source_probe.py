"""Exact full-state source cycles: literal DELETE or next KEEP, no quotient."""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'probe11_source_actions.pkl').open('rb') as f:src=pickle.load(f)
    with (F/'closed_word_source_probe_models.pkl').open('rb') as f:allm=pickle.load(f)
    N=len(src['trees']);ad=src['destination'].astype(np.int32);hh=src['H'].astype(np.int32);ar=np.arange(N,dtype=np.int64);reports=[]
    if BATCH==1:mi=0;state=None;processed=updates=0
    else:
        with (F/f'closed_word_source_probe_{BATCH-1:02d}.pkl').open('rb') as f:old=pickle.load(f)
        assert old['status']=='CHECKPOINT';mi,state,processed,updates,reports=(old[k] for k in ('model_index','state','processed','updates','reports'))
    cycle=None
    while mi<len(allm['models']) and time.process_time()-START<CAP-5:
        m=allm['models'][mi];L=m['phase_count'];assert N*L+N<2000000
        if state is None:
            D=np.zeros((L,N),dtype=np.int32);pn=np.full((L,N),-1,dtype=np.int32);op=np.zeros((L,N),dtype=np.int8)
            todo=collections.deque(range(L));inq=bytearray([1])*L
        else:D,pn,op,todo,inq=(state[k] for k in ('D','parent_node','parent_op','pending','inqueue'));state=None
        def find_cycle(v):
            seen={};walk=[];u=v
            while u not in seen:
                p,a=divmod(u,N);pr=int(pn[p,a])
                if pr<0:return None
                seen[u]=len(walk);walk.append(u);u=pr
                if len(walk)%10000==0 and time.process_time()-START>CAP-5:return None
            nodes=walk[seen[u]:];edges=[];weight=0
            for v in nodes:
                pt,at=divmod(v,N);s=int(pn[pt,at]);ps,aa=divmod(s,N);act=int(op[pt,at]);x=abs(act)-1
                assert int(ad[aa,x])==at
                if act<0:assert pt==ps;q=0
                else:assert x+1==m['phase_rows'][ps][1] and pt==(ps+1)%L;q=m['phase_rows'][ps][2]
                w=2*int(hh[aa,x])-q;weight+=w
                edges.append({'source':s,'target':v,'kind':'D' if act<0 else 'K','key':x+1,'a':int(hh[aa,x]),'qF':q,'w':w})
            return {'edges':list(reversed(edges)),'weight':weight,'model_index':mi,'genuine_support':m['genuine_support']} if weight<0 else None
        while todo and time.process_time()-START<CAP-5:
            p=todo.popleft();inq[p]=0;values=D[p].astype(np.int64);trigger=None
            actions=[(x,p,-(x+1),0) for x in range(11)]+[(m['phase_rows'][p][1]-1,(p+1)%L,m['phase_rows'][p][1],m['phase_rows'][p][2])]
            for x,pt,action,q in actions:
                candidate=(values+q-2*hh[:,x]+10000)*N+ar
                best=np.full(N,-10**15,dtype=np.int64);np.maximum.at(best,ad[:,x],candidate)
                v=best//N-10000;changed=np.flatnonzero(v>D[pt])
                if not len(changed):continue
                D[pt,changed]=v[changed];pn[pt,changed]=p*N+(best[changed]%N).astype(np.int32);op[pt,changed]=action;updates+=len(changed)
                if not inq[pt]:inq[pt]=1;todo.append(pt)
                high=changed[np.argmax(v[changed])]
                if v[high]>8:trigger=pt*N+int(high)
            processed+=1
            if trigger is not None:cycle=find_cycle(trigger)
            if cycle:break
        if cycle:state={'D':D,'parent_node':pn,'parent_op':op,'pending':todo,'inqueue':inq};break
        if todo:
            state={'D':D,'parent_node':pn,'parent_op':op,'pending':todo,'inqueue':inq};break
        reports.append({'model_index':mi,'W':m['W'],'phase_count':L,'status':'NO_NEGATIVE_CYCLE_IN_THIS_EXACT_WORD_GRAPH',
          'max_D':int(D.max()),'positive_states':int((D>0).sum()),'not_universal_proof':True});mi+=1
        del D,pn,op
    status='ACTUAL_NEGATIVE_CYCLE_CANDIDATE' if cycle else ('BOUNDED_WORD_SEARCH_COMPLETE' if mi==len(allm['models']) else 'CHECKPOINT')
    out={'status':status,'model_index':mi,'models':len(allm['models']),'state':state,'processed':processed,'updates':updates,'reports':reports,'cycle':cycle,
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','independent_witness_audit':'REQUIRED_IF_NEGATIVE',
      'input_sha256':{'source':sha(F/'probe11_source_actions.pkl'),'models':sha(F/'closed_word_source_probe_models.pkl')}}
    with (F/f'closed_word_source_probe_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(out,f,protocol=5)
    report={k:v for k,v in out.items() if k!='state'}
    with (F/f'closed_word_source_probe_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps({k:v for k,v in report.items() if k not in ('cycle','reports','input_sha256')}),flush=True)
    if cycle:print(json.dumps({'cycle_weight':cycle['weight'],'cycle_edges':len(cycle['edges'])}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
