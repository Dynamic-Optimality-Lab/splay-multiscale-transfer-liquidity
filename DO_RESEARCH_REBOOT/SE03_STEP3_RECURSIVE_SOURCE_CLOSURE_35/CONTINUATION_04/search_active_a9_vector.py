"""Source-exact sparse boundary relaxation using packed Bellman envelopes.

To improve a nonnegative target cell with q<=6, an A path from source
value v must have H<=(v+5)//2. Every positive A access costs at least one.
The indicated number of Bellman layers therefore finds EVERY strict
improvement, with no lookback hypothesis on the actual original word.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((F/'active_a9_model.json').read_text());na=m['A_count'];nb=m['B_count'];mr=m['mark_ranks']
    root=np.array(m['A_roots']);classes=[np.flatnonzero(root==mr[(r-1)//2]) for r in m['B_roots']]
    dest=np.array(m['A_destination'],dtype=np.int64).ravel();cost=2*na*np.array(m['A_H'],dtype=np.int64)
    be=[[] for _ in range(nb)]
    for eid,e in enumerate(m['B_edges']):be[e['source']].append((e['target'],e['q'],eid))
    with (F/f'active_a9_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
    assert z['model_sha256']==sha(F/'active_a9_model.json') and z['status']=='CHECKPOINT'
    level,parent,pending,inqueue=z['level'],z['parent'],z['pending'],z['inqueue']
    done,relax,checks,nonzero,maxd=z['processed'],z['relaxations'],z['cached_edge_examinations'],z['nonzero_states'],z['max_D']
    trigger=z['trigger'];cycle=None;statecap=False
    while pending and time.process_time()-START<CAP-4:
        b=pending.popleft();inqueue[b]=0;lb=level[b];aa=classes[b]
        source=np.array([lb.get(int(a),0) for a in aa],dtype=np.int64)
        best=np.full(na,-10**12,dtype=np.int64);best[aa]=(source+1000)*na+aa
        L=(int(source.max())+5)//2
        for _ in range(L):
            candidates=(best[:,None]-cost).ravel();np.maximum.at(best,dest,candidates)
        vals=best//na-1000;owners=best%na;checks+=L*len(dest)
        for bt,q,eid in be[b]:
            target=level[bt];ta=classes[bt];v=vals[ta]+q
            for ix in np.flatnonzero(v>0):
                t=int(ta[ix]);value=int(v[ix])
                if value>target.get(t,0):
                    own=int(owners[t]);sourcevalue=lb.get(own,0);h=(sourcevalue-int(vals[t]))//2
                    assert root[own]==mr[(m['B_roots'][b]-1)//2] and h>0 and sourcevalue-2*h==int(vals[t])
                    if t not in target:nonzero+=1
                    target[t]=value;code=bt*na+t;parent[code]=(b*na+own,eid,h);relax+=1
                    if value>maxd:maxd=value;trigger=code
                    if not inqueue[bt]:inqueue[bt]=1;pending.append(bt)
        done+=1
        if nonzero+na+nb>=1900000:statecap=True;break
        if maxd>100:
            seen={};walk=[];u=trigger
            while u in parent and u not in seen:
                seen[u]=len(walk);walk.append(u);u=parent[u][0]
            if u in seen:
                cyc=walk[seen[u]:];weight=sum(2*parent[v][2]-m['B_edges'][parent[v][1]]['q'] for v in cyc)
                if weight<0:cycle={'nodes':cyc,'weight':weight};break
    assert nonzero+na+nb<2000000
    status='NEGATIVE_CYCLE_CANDIDATE' if cycle else ('STATE_CAP_CHECKPOINT' if statecap else ('COMPLETE' if not pending else 'CHECKPOINT'))
    z={'status':status,'batch':BATCH,'model_sha256':sha(F/'active_a9_model.json'),'level':level,'parent':parent,
       'pending':pending,'inqueue':inqueue,'processed':done,'relaxations':relax,'nonzero_states':nonzero,
       'cached_edge_examinations':checks,'max_D':maxd,'trigger':trigger,'cycle':cycle}
    with (F/f'active_a9_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('level','parent','pending','inqueue')}
    report.update({'pending_columns':len(pending),'live_boundary_states':nonzero,'transient_A_envelope':na,
       'full_implicit_boundary_domain':sum(map(len,classes)),'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'scope':'r7 maximal B core13; all A9 shapes with helper ranks 2,4; arbitrary rigid private populations',
       'envelope':'packed Bellman; all strict improvements source-cost bounded, not an original word-length restriction'})
    with (F/f'active_a9_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
