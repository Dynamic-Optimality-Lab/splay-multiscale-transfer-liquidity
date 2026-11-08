"""Bounded original-source falsification using cached native actions only.
No positive universal conclusion follows from a completed or interrupted run.
Each search edge is one real natural macro, starting/ending synchronized.
"""
import json,pickle,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();z=json.loads((B/'nine_label_native_action_cache.json').read_text());T=z['trees'];N=len(T);D=z['destination'];H=z['H'];Q=z['Q']
    def vine(t,lo=1):return t=='F9' if lo==10 else isinstance(t,list) and t[0]==lo and t[1]=='F'+str(lo-1) and vine(t[2],lo+1)
    root=next(i for i,t in enumerate(T) if vine(t));initial=root*N+root
    if number==1:s={'nodes':[initial],'index':{initial:0},'dist':[0],'parent':[-1],'parent_op':[None],'reach':[-1],'reach_op':[None],'queue':collections.deque([0]),'inside':bytearray([1]),'checks':0,'relaxations':0,'pops':0}
    else:
        with (B/('pair9_search_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    nodes,index,dist,parent,op,reach,rop,queue,inside=(s[k] for k in ('nodes','index','dist','parent','parent_op','reach','reach_op','queue','inside'));cycle=None;status='BATCH_CHECKPOINT';ceiling=1900000
    def inspect(v):
        seen={};path=[]
        while v>=0 and len(path)<128:
            if v in seen:
                cyc=path[seen[v]:];cyc.reverse();edges=[]
                for t in cyc:
                    p=parent[t];yy,xx,w=op[t];edges.append([p,t,yy,xx,w])
                if sum(e[-1] for e in edges)<0:return edges
                return None
            seen[v]=len(path);path.append(v);v=parent[v]
        return None
    while queue and len(nodes)<ceiling and time.process_time()-start<cap-4 and cycle is None:
        i=queue.popleft();inside[i]=0;a,b=divmod(nodes[i],N);r=T[b][0]-1;aa=D[a];bb=D[b];hh=H[a];qq=Q[b];edges=[]
        for x in range(9):
            if x!=r:edges.append((aa[x]*N+bb[x],0,x+1,2*hh[x]-qq[x]))
        for y in range(9):
            if hh[y]!=1:continue
            at=aa[y]
            for x in range(9):
                if x!=r and H[at][x]==1:edges.append((D[at][x]*N+bb[x],y+1,x+1,4-qq[x]))
        for code,y,x,w in edges:
            s['checks']+=1;j=index.get(code)
            if j is None:
                if len(nodes)>=ceiling:break
                j=len(nodes);index[code]=j;nodes.append(code);dist.append(10**15);parent.append(-1);op.append(None);reach.append(i);rop.append((y,x,w));inside.append(0)
            value=dist[i]+w
            if value<dist[j]:
                dist[j]=value;parent[j]=i;op[j]=(y,x,w);s['relaxations']+=1
                if not inside[j]:inside[j]=1;queue.append(j)
                if s['relaxations']%512==0:cycle=inspect(j)
                if cycle is not None:break
        s['pops']+=1
    if cycle:
        status='EXACT_PAIR_CYCLE_CANDIDATE';v=cycle[0][0];prefix=[]
        while reach[v]>=0:
            prefix.append([reach[v],v,*rop[v]]);v=reach[v]
        prefix.reverse();assert nodes[v]==initial
        witness={'initial_tree_index':root,'nodes':[nodes[v] for v in range(len(nodes))],'prefix':prefix,'cycle':cycle,'cycle_weight':sum(e[-1] for e in cycle),'source_queries':0,'status':status,'source_note':'cached actual macros; independent original replay and support/closure audit still required'}
        with (B/('pair9_candidate_%02d.json'%number)).open('x') as f:json.dump(witness,f)
    elif len(nodes)>=ceiling:status='STATE_CAP_CHECKPOINT'
    elif not queue:status='COMPLETE_RESTRICTED_GRAPH_NO_NEGATIVE_CYCLE'
    with (B/('pair9_search_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':status,'batch':number,'nodes':len(nodes),'stored_edges':sum(p>=0 for p in parent)+sum(p>=0 for p in reach),'static_cached_edge_checks':s['checks'],'relaxations':s['relaxations'],'pops':s['pops'],'pending_queue':len(queue),'minimum_path_weight':min(dist),'source_queries':0,'positive_claim':'NONE; restricted source falsification only','principal_U33':'OPEN'}
    with (B/('pair9_search_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
