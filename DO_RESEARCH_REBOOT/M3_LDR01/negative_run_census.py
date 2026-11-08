"""Complete nine-core negative-access graph and exact longest-deficit recurrence."""
import sys,json,time
from collections import deque,Counter
from pathlib import Path
from functools import lru_cache
sys.path.insert(0,'python/independent')
import splay as S
OUT=Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json')
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(r,l,t) for r in range(lo,hi) for l in trees(lo,r) for t in trees(r+1,hi))
def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]
def main():
    assert not OUT.exists();start=time.process_time();alltrees=trees(0,9)
    ids={t:i for i,t in enumerate(alltrees)};edges=[];out=[[] for _ in alltrees]
    indeg=[0]*len(alltrees);depths=Counter();queries=0
    for i,t in enumerate(alltrees):
        assert time.process_time()-start<120,'UNKNOWN: census cap'
        for x in range(9):
            queries+=1;h=S.lookup(t,x)[1]
            if h<6:continue
            dest=S.trace(t,x)[0];j=ids[dest];delta=h//2-2
            row={'source':i,'destination':j,'target':x,'depth':h,'deficit':delta}
            out[i].append(len(edges));edges.append(row);indeg[j]+=1;depths[h]+=1
    queue=deque(i for i,v in enumerate(indeg) if v==0);topo=[]
    psi=[0]*len(alltrees);prev=[None]*len(alltrees);length=[0]*len(alltrees)
    while queue:
        i=queue.popleft();topo.append(i)
        for e in out[i]:
            r=edges[e];j=r['destination'];v=psi[i]+r['deficit']
            if v>psi[j]:psi[j]=v;prev[j]=e
            length[j]=max(length[j],length[i]+1)
            indeg[j]-=1
            if indeg[j]==0:queue.append(j)
    acyclic=len(topo)==len(alltrees);witness=[]
    if acyclic:
        j=max(range(len(psi)),key=psi.__getitem__)
        while prev[j] is not None:
            e=prev[j];witness.append(edges[e]);j=edges[e]['source']
        witness.reverse()
        assert all(psi[r['destination']]-psi[r['source']]>=r['deficit'] for r in edges)
    result={'status':'COMPLETE','core_topologies':len(alltrees),'access_queries':queries,
            'negative_edges':len(edges),'depth_counts':dict(depths),'acyclic':acyclic,
            'max_run_deficit':max(psi) if acyclic else None,
            'max_run_length':max(length) if acyclic else None,
            'potential_histogram':dict(Counter(psi)) if acyclic else {},
            'maximal_deficit_witness':witness,'topological_order':topo,
            'nodes':[{'id':i,'tree':serial(t),'psi':psi[i]} for i,t in enumerate(alltrees)],
            'edges':edges,'cpu_seconds':round(time.process_time()-start,3),
            'scope':'complete B-only overapproximation of fused negative low edges; source projection/lifting scopes need separate proof'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('nodes','edges','topological_order')}),flush=True)
if __name__=='__main__':main()
