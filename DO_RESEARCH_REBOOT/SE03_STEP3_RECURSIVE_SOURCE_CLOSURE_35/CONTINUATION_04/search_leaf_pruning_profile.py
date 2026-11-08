"""Falsify an entire recursive information class with original LOW rows.
No HIGH relaxation and no source path-realization claim are used.
"""
import collections,functools,hashlib,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time();PHASE=sys.argv[3];BATCH=int(sys.argv[4])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    with (F/'leaf_profile_inputs.pkl').open('rb') as f:z=pickle.load(f)
    na=5947;nb=3876;radix=4096
    groups={}
    for h in (1,2):
        for rid,(s,x,t) in enumerate(z[f'H{h}_rows']):groups.setdefault((h,z['A_roots'][s],x),[]).append((s,t,rid))
    groups={k:np.array(v,dtype=np.int32) for k,v in groups.items()}
    @functools.lru_cache(maxsize=64)
    def features(b):
        values=np.zeros(na,dtype=np.int32)
        root=(z['B_roots'][b]-1)//2;valid=np.array(z['A_roots'])==root
        for e,b6 in zip(z['B_leaves'][b],z['B_projection'][b]):
            ap=z['A_projection'][e];assert np.all(ap[valid]>=0)
            vals=z['old_debt'][z['old_offsets'][b6]+z['A6_local'][ap]]
            values=values*4+vals
        values[~valid]=-1;return values
    if BATCH==1:
        first=0;edges=[];adj={};dist={};parent={};processed=0;constraints=0
    else:
        with (F/f'leaf_profile_search_{BATCH-1:02d}.pkl').open('rb') as f:old=pickle.load(f)
        first,edges,adj,dist,parent,processed,constraints=(old[k] for k in ('next_B','edges','adj','dist','parent','processed','source_constraints'))
    bedges=collections.defaultdict(list)
    for eid,e in enumerate(z['B_edges']):bedges[e['source']].append((eid,e))
    cycle=None;nextb=first;why=None
    def relax_all():
        nonlocal processed
        queue=collections.deque(dist);pending=set(dist);count=0
        while queue:
            s=queue.popleft();pending.remove(s);processed+=1
            for ei in adj.get(s,()):
                edge=edges[ei];t=edge[1];gain=-edge[2];v=dist[s]+gain
                if v<=dist[t]:continue
                dist[t]=v;parent[t]=ei;count+=1
                if t not in pending:pending.add(t);queue.append(t)
                if v>8 and (count%100==0 or v>100):
                    seen={};walk=[];u=t
                    while u in parent and u not in seen:
                        seen[u]=len(walk);pe=parent[u];walk.append(pe);u=edges[pe][0]
                    if u in seen:
                        cc=walk[seen[u]:]
                        if sum(edges[i][2] for i in cc)<0:return cc
                if time.process_time()-START>CAP-5:return None
            if time.process_time()-START>CAP-5:return None
        return None
    for b in range(first,nb):
        fs=features(b);g=(z['B_roots'][b]-1)//2
        for eid,e in bedges[b]:
            bt,x=e['target'],(e['key']-1)//2;ft=features(bt)
            for h in (1,2):
                aa=groups[h,g,x];src,dst=aa[:,0],aa[:,1];assert np.all(fs[src]>=0) and np.all(ft[dst]>=0)
                pairs=fs[src].astype(np.int64)*radix+ft[dst]
                unique,index=np.unique(pairs,return_index=True);constraints+=len(aa)
                for code,j in zip(unique.tolist(),index.tolist()):
                    s=b*radix+code//radix;t=bt*radix+code%radix
                    edge=(s,t,2*h-e['q'],eid,h,int(aa[j,2]),int(src[j]),int(dst[j]))
                    i=len(edges);edges.append(edge);adj.setdefault(s,[]).append(i);dist.setdefault(s,0);dist.setdefault(t,0)
        nextb=b+1
        if nextb%32==0:
            cycle=relax_all()
            if cycle:why='NEGATIVE_INFORMATION_CYCLE';break
        if len(edges)>600000 or len(dist)>300000:why='LIVE_RECORD_CHECKPOINT';break
        if time.process_time()-START>CAP-6:why='CPU_CHECKPOINT';break
    if cycle is None and time.process_time()-START<CAP-6:cycle=relax_all()
    status='INFORMATION_CLASS_REFUTED' if cycle else ('LOW_QUOTIENT_FEASIBLE' if nextb==nb and why is None else 'CHECKPOINT')
    report={'status':status,'next_B':nextb,'B_count':nb,'nodes':len(dist),'edges':len(edges),'source_constraints':constraints,
      'processed':processed,'max_D':max(dist.values(),default=0),'reason':why,
      'source_queries':0,'source_engine_calls':0,'input_sha256':sha(F/'leaf_profile_inputs.pkl'),'JR35':'OPEN',
      'cycle_edges':[{'s':edges[i][0],'t':edges[i][1],'w':edges[i][2],'B_edge':edges[i][3],
         'H':edges[i][4],'source_row':edges[i][5],'A_source':edges[i][6],'A_target':edges[i][7]} for i in cycle] if cycle else None}
    if cycle:report.update({'cycle_weight':sum(edges[i][2] for i in cycle),'cycle_length':len(cycle),
         'scope':'ALL functions of full B and the complete leaf-indexed unchanged D6 vector',
         'is_original_source_cycle':False,'Coarse_Double_refuted':False})
    with (F/f'leaf_profile_search_{BATCH:02d}.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    state=dict(report,edges=edges,adj=adj,dist=dist,parent=parent)
    with (F/f'leaf_profile_search_{BATCH:02d}.pkl').open('xb') as f:pickle.dump(state,f,protocol=5)
    print(json.dumps({k:v for k,v in report.items() if k!='cycle_edges'}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/f'audit_{PHASE}_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
