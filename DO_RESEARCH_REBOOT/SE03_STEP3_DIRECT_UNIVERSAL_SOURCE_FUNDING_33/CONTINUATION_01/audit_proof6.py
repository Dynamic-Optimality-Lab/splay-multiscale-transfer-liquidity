"""Fold unfinished source exploration by the inherited exact reflection.
Reuses all discovered native states, distances and reaching witnesses.
"""
import json,pickle,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'nine_label_native_action_cache.json').read_text());T=list(map(fr,z['trees']));N=len(T);idx={t:i for i,t in enumerate(T)}
    def reflect(t):return 'F'+str(9-int(t[1:])) if isinstance(t,str) else (10-t[0],reflect(t[2]),reflect(t[1]))
    mirror=[idx[reflect(t)] for t in T];D=z['destination'];H=z['H'];Q=z['Q']
    assert all(mirror[mirror[i]]==i for i in range(N))
    assert all(D[mirror[s]][8-x]==mirror[D[s][x]] and H[mirror[s]][8-x]==H[s][x] and Q[mirror[s]][8-x]==Q[s][x] for s in range(N) for x in range(9))
    with (B/'pair9_search_02.pkl').open('rb') as f:old=pickle.load(f)
    nodes=[];index={};oldnew=[];flips=[];dist=[];parent=[];op=[];reach=[];rop=[];best=[]
    for i,code in enumerate(old['nodes']):
        a,b=divmod(code,N);m=mirror[a]*N+mirror[b];c=min(code,m);flip=code!=c;j=index.get(c)
        if j is None:j=len(nodes);index[c]=j;nodes.append(c);dist.append(old['dist'][i]);parent.append(-1);op.append(None);reach.append(-1);rop.append(None);best.append(i)
        elif old['dist'][i]<dist[j]:dist[j]=old['dist'][i];best[j]=i
        oldnew.append(j);flips.append(flip)
        if i%16384==0 and time.process_time()-START>CAP-3:raise TimeoutError('REFLECTION_FOLD_RESERVE')
    def convert(i,field,ops):
        p=old[field][i]
        if p<0:return -1,None
        y,x,w=old[ops][i];f=flips[p]
        return oldnew[p],((10-y if y and f else y),(10-x if f else x),w,flips[p]!=flips[i])
    seen=set()
    for i,j in enumerate(oldnew):
        if j not in seen:
            seen.add(j);reach[j],rop[j]=convert(i,'reach','reach_op')
    for j,i in enumerate(best):parent[j],op[j]=convert(i,'parent','parent_op')
    assert len(nodes)<1900000 and all(p<j for j,p in enumerate(reach) if p>=0)
    s={'nodes':nodes,'index':index,'dist':dist,'parent':parent,'parent_op':op,'reach':reach,'reach_op':rop,'queue':collections.deque(range(len(nodes))),'inside':bytearray([1])*len(nodes),'checks':old['checks'],'relaxations':old['relaxations'],'pops':old['pops'],'mirror':mirror}
    with (B/'pair9_reflect_00.pkl').open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':'EXACT_REFLECTION_FOLD_CHECKPOINT','old_nodes':len(oldnew),'new_nodes':len(nodes),'source_queries':0,'old_reaching_witnesses_reused':True,'positive_universal_claim':False,'principal_U33':'OPEN'};out('pair9_reflection_fold.json',result);print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof6_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
