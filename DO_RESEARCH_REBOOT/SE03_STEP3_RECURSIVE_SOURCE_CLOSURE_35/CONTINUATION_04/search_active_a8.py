"""Exact natural-boundary relaxation; complete cached ordinary source actions.

Only synchronized natural boundaries are live. A-only envelopes are transient
1430-node calculations, not omitted helper operations. No fresh source query.
"""
import array,bisect,collections,hashlib,heapq,json,pickle,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
PHASE=sys.argv[3];GAP=int(sys.argv[4]);BATCH=int(sys.argv[5])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    model=json.loads((F/'active_a8_model.json').read_text());na=model['A_count'];nb=model['B_count']
    roots=model['A_roots'];br=model['B_roots'];AD=model['A_destination'];AH=model['A_H']
    ar=[[a for a in range(na) if roots[a]==r] for r in range(1,9)]
    mr=[j+1+(j>=GAP) for j in range(7)]
    classes=[ar[mr[(r-1)//2]-1] for r in br]
    offsets=[0]
    for aa in classes:offsets.append(offsets[-1]+len(aa))
    n=offsets[-1];assert n+na+nb<2000000
    a_edges=[[(AD[a][k],2*AH[a][k]) for k in range(8) if AH[a][k]>0] for a in range(na)]
    be=[[] for _ in range(nb)]
    for i,e in enumerate(model['B_edges']):be[e['source']].append((e['target'],e['q'],i))
    prefix=f'active_a8_g{GAP}'
    if BATCH==1:
        levels=array.array('i',[0])*n;parent=array.array('i',[-1])*n
        pe=array.array('h',[-1])*n;ph=array.array('h',[0])*n
        pending=collections.deque(range(nb));inqueue=bytearray([1])*nb
        done=relax=checks=0;maxd=0
    else:
        with (F/f'{prefix}_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['model_sha256']==sha(F/'active_a8_model.json') and z['gap']==GAP and z['status']=='CHECKPOINT'
        levels,parent,pe,ph=z['levels'],z['parent'],z['parent_edge'],z['parent_H']
        pending,inqueue=z['pending'],z['inqueue'];done=z['processed'];relax=z['relaxations'];checks=z['cached_edge_examinations'];maxd=z['max_D']
    cycle=None;trigger=None
    while pending and time.process_time()-START<CAP-4:
        b=pending.popleft();inqueue[b]=0;aa=classes[b];off=offsets[b]
        best=[-1000000]*na;owner=[-1]*na;dist=[0]*na;pq=[]
        for pos,a in enumerate(aa):
            best[a]=levels[off+pos];owner[a]=off+pos
            pq.append((-best[a],a))
        heapq.heapify(pq)
        while pq:
            neg,a=heapq.heappop(pq);val=-neg
            if val!=best[a]:continue
            if val<-6:break
            for t,w in a_edges[a]:
                checks+=1;v=val-w
                if v>=-6 and v>best[t]:
                    best[t]=v;owner[t]=owner[a];dist[t]=dist[a]+w//2
                    heapq.heappush(pq,(-v,t))
        for bt,q,eid in be[b]:
            ot=offsets[bt]
            for pos,t in enumerate(classes[bt]):
                v=best[t]+q;code=ot+pos
                if v>levels[code]:
                    assert owner[t]>=0 and dist[t]>0
                    levels[code]=v;parent[code]=owner[t];pe[code]=eid;ph[code]=dist[t];relax+=1
                    if v>maxd:maxd=v;trigger=code
                    if not inqueue[bt]:inqueue[bt]=1;pending.append(bt)
        done+=1
        if maxd>100:
            seen={};walk=[];u=trigger
            while u>=0 and u not in seen:
                seen[u]=len(walk);walk.append(u);u=parent[u]
            if u>=0:
                cyc=walk[seen[u]:];weight=sum(2*ph[v]-model['B_edges'][pe[v]]['q'] for v in cyc)
                if weight<0:cycle={'nodes':cyc,'weight':weight};break
    status='NEGATIVE_CYCLE_CANDIDATE' if cycle else ('COMPLETE' if not pending else 'CHECKPOINT')
    z={'status':status,'gap':GAP,'batch':BATCH,'model_sha256':sha(F/'active_a8_model.json'),
       'levels':levels,'parent':parent,'parent_edge':pe,'parent_H':ph,'pending':pending,'inqueue':inqueue,
       'offsets':offsets,'state_count':n,'processed':done,'relaxations':relax,
       'cached_edge_examinations':checks,'max_D':maxd,'cycle':cycle}
    with (F/f'{prefix}_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('levels','parent','parent_edge','parent_H','pending','inqueue','offsets')}
    report.update({'pending_columns':len(pending),'nonzero_states':sum(v>0 for v in levels),
      'source_queries':0,'source_engine_calls':0,'root_JR35':'OPEN_UNTIL_ORIGINAL_COUNTERCERTIFICATE_OR_UNIVERSAL_PROOF',
      'scope':'complete core13 B, all A8 shapes, one anonymous A operand in specified gap; rigid private fringes'})
    with (F/f'{prefix}_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
