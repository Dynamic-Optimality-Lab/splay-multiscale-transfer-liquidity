"""Uniform debt difference constraints on the exact cached native domain."""
import json,pickle,time
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();z=json.loads((B/'nine_label_native_action_cache.json').read_text());N=len(z['trees']);D=z['destination'];H=z['H'];Q=z['Q'];T=z['trees']
    with (B/('pair9_debt_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    nodes,index,level,parent,op,queue,inside,mirror=(s[k] for k in ('nodes','index','debt','parent','parent_op','queue','inside','mirror'));ceiling=False
    while queue and time.process_time()-start<cap-4:
        i=queue.popleft();inside[i]=0;a,b=divmod(nodes[i],N);root=T[b][0]-1;aa=D[a];bb=D[b];hh=H[a];qq=Q[b];edges=[]
        for x in range(9):
            if x!=root:edges.append((aa[x],bb[x],0,x+1,2*hh[x]-qq[x]))
        for y in range(9):
            if hh[y]!=1:continue
            at=aa[y]
            for x in range(9):
                if x!=root and H[at][x]==1:edges.append((D[at][x],bb[x],y+1,x+1,4-qq[x]))
        for at,bt,y,x,w in edges:
            s['checks']+=1;code=at*N+bt;ref=mirror[at]*N+mirror[bt];flip=ref<code;j=index[min(code,ref)];v=level[i]-w
            if v>level[j]:
                if v>250:ceiling=True;break
                level[j]=v;parent[j]=i;op[j]=(y,x,w,flip);s['updates']+=1
                if not inside[j]:inside[j]=1;queue.append(j)
        if ceiling:break
    with (B/('pair9_debt_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':'DEBT_REPRESENTATION_CEILING' if ceiling else 'COMPLETE_NATIVE_DEBT_CANDIDATE' if not queue else 'DEBT_BATCH_CHECKPOINT','batch':number,'nodes':len(nodes),'width_so_far':max(level),'checks':s['checks'],'updates':s['updates'],'pending':len(queue),'source_queries':0,'principal_U33':'OPEN','verification':'PRODUCER_ONLY; arbitrary A ancestors/support NOT covered'}
    with (B/('pair9_debt_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
