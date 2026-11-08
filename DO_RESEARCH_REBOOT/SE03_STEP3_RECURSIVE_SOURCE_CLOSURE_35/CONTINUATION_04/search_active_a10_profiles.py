"""Lossless symbolic debt profiles; full source B columns remain distinct.

Equal numerical functions on A are shared, not source states. Mutable
updates use copy on write. Live potential cells and predecessor cells are
counted explicitly. All original B edges and cached A actions are retained.
"""
import collections,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((F/'active_a10_model.json').read_text());na=m['A_count'];nb=m['B_count'];mr=m['mark_ranks']
    root=np.array(m['A_roots']);classes=[np.flatnonzero(root==mr[(r-1)//2]) for r in m['B_roots']]
    dest=np.array(m['A_destination'],dtype=np.int64).ravel();cost=2*na*np.array(m['A_H'],dtype=np.int64)
    be=[[] for _ in range(nb)]
    for eid,e in enumerate(m['B_edges']):be[e['source']].append((e['target'],e['q'],eid))
    if BATCH==1:
        empty={};level=[empty]*nb;parent={};pending=collections.deque(range(nb));inqueue=bytearray([1])*nb
        done=relax=checks=0;maxd=0;trigger=None;peakcells=0
    else:
        with (F/f'active_a10_{BATCH-1:02d}.pkl').open('rb') as f:z=pickle.load(f)
        assert z['model_sha256']==sha(F/'active_a10_model.json') and z['status']=='CHECKPOINT'
        level,parent,pending,inqueue=z['level'],z['parent'],z['pending'],z['inqueue']
        done,relax,checks,maxd=z['processed'],z['relaxations'],z['cached_edge_examinations'],z['max_D']
        trigger=z['trigger'];peakcells=z['peak_unique_profile_cells']
    pool={};rowkeys=[];cells=0
    for i,row in enumerate(level):
        key=tuple(sorted(row.items()))
        if key in pool:pool[key][1]+=1;level[i]=pool[key][0]
        else:pool[key]=[row,1];cells+=len(row)
        rowkeys.append(key)
    cycle=None;statecap=False
    while pending and time.process_time()-START<CAP-5:
        b=pending.popleft();inqueue[b]=0;lb=level[b];aa=classes[b]
        source=np.array([lb.get(int(a),0) for a in aa],dtype=np.int64)
        best=np.full(na,-10**12,dtype=np.int64);best[aa]=(source+1000)*na+aa
        L=(int(source.max())+5)//2
        for _ in range(L):
            candidates=(best[:,None]-cost).ravel();np.maximum.at(best,dest,candidates)
        vals=best//na-1000;owners=best%na;checks+=L*len(dest)
        for bt,q,eid in be[b]:
            target=level[bt];ta=classes[bt];vv=vals[ta]+q;changes=[]
            for ix in np.flatnonzero(vv>0):
                t=int(ta[ix]);v=int(vv[ix])
                if v>target.get(t,0):changes.append((t,v))
            if not changes:continue
            new=dict(target)
            for t,v in changes:
                new[t]=v;relax+=1
                if v>maxd:maxd=v;trigger=bt*na+t
                if maxd>6:
                    own=int(owners[t]);h=(lb.get(own,0)-int(vals[t]))//2
                    assert h>0 and lb.get(own,0)-2*h==int(vals[t])
                    parent[bt*na+t]=(b*na+own,eid,h)
            oldkey=rowkeys[bt];pool[oldkey][1]-=1
            if not pool[oldkey][1]:cells-=len(target);del pool[oldkey]
            key=tuple(sorted(new.items()))
            if key in pool:pool[key][1]+=1;new=pool[key][0]
            else:pool[key]=[new,1];cells+=len(new)
            rowkeys[bt]=key;level[bt]=new
            if not inqueue[bt]:inqueue[bt]=1;pending.append(bt)
            peakcells=max(peakcells,cells)
            if cells+len(parent)+na+nb+len(new)>=1850000:statecap=True;break
        done+=1
        if statecap:break
        if maxd>100:
            seen={};walk=[];u=trigger
            while u in parent and u not in seen:
                seen[u]=len(walk);walk.append(u);u=parent[u][0]
            if u in seen:
                cyc=walk[seen[u]:];w=sum(2*parent[v][2]-m['B_edges'][parent[v][1]]['q'] for v in cyc)
                if w<0:cycle={'nodes':cyc,'weight':w};break
    assert cells+len(parent)+na+nb<2000000
    status='NEGATIVE_CYCLE_CANDIDATE' if cycle else ('STATE_CAP_CHECKPOINT' if statecap else ('COMPLETE' if not pending else 'CHECKPOINT'))
    z={'status':status,'batch':BATCH,'model_sha256':sha(F/'active_a10_model.json'),'level':level,'parent':parent,
       'pending':pending,'inqueue':inqueue,'processed':done,'relaxations':relax,
       'cached_edge_examinations':checks,'max_D':maxd,'trigger':trigger,'cycle':cycle,
       'peak_unique_profile_cells':peakcells}
    with (F/f'active_a10_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('level','parent','pending','inqueue')}
    report.update({'pending_columns':len(pending),'unique_profiles':len(pool),'unique_profile_cells':cells,
       'expanded_positive_cells':sum(map(len,level)),'transient_A_envelope':na,
       'full_implicit_boundary_domain':sum(map(len,classes)),'source_queries':0,'source_engine_calls':0,'JR35':'OPEN',
       'source_state_identifications':0,'scope':'r7 maximal B core13; all A10 shapes with helper ranks 2,4,6; arbitrary rigid private populations'})
    with (F/f'active_a10_{BATCH:02d}.json').open('x',encoding='utf-8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
