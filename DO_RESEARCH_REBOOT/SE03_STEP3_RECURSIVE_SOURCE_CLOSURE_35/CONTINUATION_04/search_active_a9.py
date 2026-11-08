"""Complete cached source class; sparse synchronized boundary potentials."""
import collections,hashlib,heapq,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((F/'active_a9_model.json').read_text());na=m['A_count'];nb=m['B_count']
    roots=m['A_roots'];AD=m['A_destination'];AH=m['A_H'];mr=m['mark_ranks']
    ar=[[a for a in range(na) if roots[a]==r] for r in range(1,10)]
    classes=[ar[mr[(r-1)//2]-1] for r in m['B_roots']]
    ae=[[(AD[a][k],2*AH[a][k]) for k in range(9) if AH[a][k]>0] for a in range(na)]
    be=[[] for _ in range(nb)]
    for eid,e in enumerate(m['B_edges']):be[e['source']].append((e['target'],e['q'],eid))
    if BATCH==1:
        level=[{} for _ in range(nb)];parent={};pending=collections.deque(range(nb));inqueue=bytearray([1])*nb
        done=relax=checks=nonzero=0;maxd=0;trigger=None
    else:
        with (F/f'active_a9_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['model_sha256']==sha(F/'active_a9_model.json') and z['status']=='CHECKPOINT'
        level,parent,pending,inqueue=z['level'],z['parent'],z['pending'],z['inqueue']
        done,relax,checks,nonzero,maxd=z['processed'],z['relaxations'],z['cached_edge_examinations'],z['nonzero_states'],z['max_D']
        trigger=z['trigger']
    cycle=None;statecap=False
    while pending and time.process_time()-START<CAP-5:
        b=pending.popleft();inqueue[b]=0;lb=level[b]
        best=[-1000000]*na;owner=[-1]*na;dist=[0]*na;pq=[]
        for a in classes[b]:
            v=lb.get(a,0);best[a]=v;owner[a]=a;pq.append((-v,a))
        heapq.heapify(pq)
        while pq:
            neg,a=heapq.heappop(pq);val=-neg
            if val!=best[a]:continue
            if val<-6:break
            for t,w in ae[a]:
                checks+=1;v=val-w
                if v>=-6 and v>best[t]:
                    best[t]=v;owner[t]=owner[a];dist[t]=dist[a]+w//2
                    heapq.heappush(pq,(-v,t))
        for bt,q,eid in be[b]:
            target=level[bt]
            for t in classes[bt]:
                v=best[t]+q
                if v>target.get(t,0):
                    assert owner[t]>=0 and dist[t]>0
                    if t not in target:nonzero+=1
                    target[t]=v;code=bt*na+t;parent[code]=(b*na+owner[t],eid,dist[t]);relax+=1
                    if v>maxd:maxd=v;trigger=code
                    if not inqueue[bt]:inqueue[bt]=1;pending.append(bt)
        done+=1
        if nonzero+na+nb+len(pq)>=1900000:statecap=True;break
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
      'full_implicit_boundary_domain':sum(map(len,classes)),
      'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
      'scope':'r7 maximal B core13; all A9 shapes with helper ranks 2,4; arbitrary rigid private populations'})
    with (F/f'active_a9_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
