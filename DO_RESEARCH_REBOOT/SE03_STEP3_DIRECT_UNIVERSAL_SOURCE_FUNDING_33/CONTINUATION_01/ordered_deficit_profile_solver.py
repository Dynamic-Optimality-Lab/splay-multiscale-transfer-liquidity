"""Capped projected-feature relaxation; no assertion of actual path lifting."""
import os
for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[name]='1'
import json,time,pickle
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    import numpy as np
    start=time.process_time();graph=np.load(B/'ordered_deficit_profile_graph.npz');src=graph['src'];dst=graph['dst'];w=graph['w'];order=graph['order'];offset=graph['offset'];rec=graph['source_records'];N=len(offset)-1
    with (B/('ordered_deficit_profile_work_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    level=s['level'];parent=s['parent'];queue=s['queue'];pending=s['pending'];head=s['head'];cycle=None
    def trace(v):
        seen={};walk=[]
        while parent[v]>=0 and len(walk)<2048:
            if v in seen:
                edges=list(reversed(walk[seen[v]:]));return edges if sum(int(w[e]) for e in edges)<0 else None
            seen[v]=len(walk);e=int(parent[v]);walk.append(e);v=int(src[e])
        return None
    while head<len(queue) and time.process_time()-start<cap-2:
        v=queue[head];head+=1;pending[v]=False
        for pos in range(offset[v],offset[v+1]):
            e=int(order[pos]);t=int(dst[e]);cand=int(level[v])-int(w[e]);s['checks']+=1
            if cand>level[t]:
                level[t]=cand;parent[t]=e;s['updates']+=1
                if not pending[t]:pending[t]=True;queue.append(t)
                if cand>=6 and s['updates']%128==0:
                    cycle=trace(t)
                    if cycle:break
        if cycle:break
        if head>100000 and head*2>len(queue):queue=queue[head:];head=0
    if cycle is None and head<len(queue):
        for v in np.argsort(level)[-20:]:
            cycle=trace(int(v))
            if cycle:break
    s.update(queue=queue,head=head)
    with (B/('ordered_deficit_profile_work_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f)
    result={'status':'NEGATIVE_PROJECTED_FEATURE_CYCLE_CANDIDATE' if cycle else ('COMPLETE_FINITE_PROJECTED_FEASIBILITY_NOT_UNIVERSAL' if head==len(queue) else 'PROJECTED_FEATURE_RELAXATION_CHECKPOINT'),'number':number,'nodes':N,'edges':len(w),'checks':s['checks'],'updates':s['updates'],'pending':len(queue)-head,'max_level':int(level.max()),'cycle_edges':cycle,'cycle_weight':sum(int(w[e]) for e in cycle) if cycle else None,'cycle_source_records':rec[cycle].tolist() if cycle else None,'only_claim':'source-summary factorization test, no actual source path inferred','principal_U33':'OPEN'}
    with (B/('ordered_deficit_profile_result_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
