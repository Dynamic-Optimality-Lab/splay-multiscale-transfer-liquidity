"""Continued cached exact-source falsification, folded by reflection."""
import json,pickle,time
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();z=json.loads((B/'nine_label_native_action_cache.json').read_text());N=len(z['trees']);D=z['destination'];H=z['H'];Q=z['Q'];T=z['trees']
    with (B/('pair9_reflect_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    nodes,index,dist,parent,op,reach,rop,queue,inside,mirror=(s[k] for k in ('nodes','index','dist','parent','parent_op','reach','reach_op','queue','inside','mirror'));cycle=None;ceiling=1900000
    def inspect(v):
        seen={};path=[]
        while v>=0 and len(path)<128:
            if v in seen:
                cc=path[seen[v]:];cc.reverse();ee=[[parent[t],t,*op[t]] for t in cc]
                if sum(e[4] for e in ee)<0:return ee
                return None
            seen[v]=len(path);path.append(v);v=parent[v]
        return None
    while queue and len(nodes)<ceiling and time.process_time()-start<cap-4 and cycle is None:
        i=queue.popleft();inside[i]=0;a,b=divmod(nodes[i],N);r=T[b][0]-1;aa=D[a];bb=D[b];hh=H[a];qq=Q[b];edges=[]
        for x in range(9):
            if x!=r:edges.append((aa[x],bb[x],0,x+1,2*hh[x]-qq[x]))
        for y in range(9):
            if hh[y]!=1:continue
            at=aa[y]
            for x in range(9):
                if x!=r and H[at][x]==1:edges.append((D[at][x],bb[x],y+1,x+1,4-qq[x]))
        for at,bt,y,x,w in edges:
            s['checks']+=1;code=at*N+bt;ref=mirror[at]*N+mirror[bt];flip=ref<code;code=min(code,ref);j=index.get(code)
            if j is None:
                if len(nodes)>=ceiling:break
                j=len(nodes);index[code]=j;nodes.append(code);dist.append(10**15);parent.append(-1);op.append(None);reach.append(i);rop.append((y,x,w,flip));inside.append(0)
            value=dist[i]+w
            if value<dist[j]:
                dist[j]=value;parent[j]=i;op[j]=(y,x,w,flip);s['relaxations']+=1
                if not inside[j]:inside[j]=1;queue.append(j)
                if s['relaxations']%512==0:cycle=inspect(j)
                if cycle is not None:break
        s['pops']+=1
    status='EXACT_PAIR_CYCLE_CANDIDATE' if cycle else 'STATE_CAP_CHECKPOINT' if len(nodes)>=ceiling else 'COMPLETE_RESTRICTED_GRAPH_NO_NEGATIVE_CYCLE' if not queue else 'BATCH_CHECKPOINT'
    if cycle:
        v=cycle[0][0];prefix=[]
        while reach[v]>=0:prefix.append([reach[v],v,*rop[v]]);v=reach[v]
        prefix.reverse()
        with (B/('pair9_reflected_candidate_%02d.json'%number)).open('x') as f:json.dump({'nodes':nodes,'prefix':prefix,'cycle':cycle,'orientation_note':'apply reflected operands whenever lifting flag changes; if cyclic net reflection is odd use two reflected laps','source_queries':0},f)
    with (B/('pair9_reflect_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':status,'batch':number,'nodes':len(nodes),'stored_edges':sum(p>=0 for p in parent)+sum(p>=0 for p in reach),'static_cached_edge_checks':s['checks'],'relaxations':s['relaxations'],'pops':s['pops'],'pending_queue':len(queue),'minimum_reaching_path_weight':min(dist),'maximum_reaching_distance':max(dist),'source_queries':0,'positive_claim':'NONE; arbitrary-support/private-ancestor theorem not inferred','principal_U33':'OPEN'}
    with (B/('pair9_reflect_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
