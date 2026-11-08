"""Exact geodesic-debt candidate, actual seven-anchor source realization."""
import json,time,sys,collections,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('geodesic_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);oldpath=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_CAP')
        queries+=1;return oldpath(t,x)
    S.path=path
    def trees(lo,hi):
        if lo>hi:return ['F'+str(hi)]
        return [(k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi)]
    T=trees(1,7);N=len(T);index={t:i for i,t in enumerate(T)};assert N==429
    dest=[];cost=[];doubles=[]
    for t in T:
        dd=[];hh=[];qq=[]
        for x in range(1,8):
            u,p,e=S.trace(t,x);dd.append(index[u]);hh.append(len(e));qq.append(len(p)//2)
        dest.append(dd);cost.append(hh);doubles.append(qq)
    def rotations(t):
        if isinstance(t,str):return []
        k,l,r=t;ans=[]
        if not isinstance(l,str):a,b,c=l;ans.append((a,b,(k,c,r)))
        if not isinstance(r,str):a,b,c=r;ans.append((a,(k,l,b),c))
        ans.extend((k,u,r) for u in rotations(l));ans.extend((k,l,u) for u in rotations(r));return ans
    adj=[[index[u] for u in rotations(t)] for t in T];assert all(len(a)==6 for a in adj)
    distance=[]
    for s in range(N):
        d=[-1]*N;d[s]=0;q=collections.deque([s])
        while q:
            v=q.popleft()
            for u in adj[v]:
                if d[u]<0:d[u]=d[v]+1;q.append(u)
        assert min(d)>=0;distance.append(d)
    roots={k:[i for i,t in enumerate(T) if t[0]==k] for k in range(1,8)};chosen=None;checks=0
    for helper_count in (0,1):
        for a in range(N):
            if chosen:break
            for b in roots[T[a][0]]:
                if chosen:break
                for y in (range(1,8) if helper_count else [0]):
                    aa=dest[a][y-1] if y else a;hy=cost[a][y-1] if y else 0
                    for x in range(1,8):
                        if x==T[b][0]:continue
                        at=dest[aa][x-1];bt=dest[b][x-1];h=hy+cost[aa][x-1];q=doubles[b][x-1];margin=2*h-q+distance[a][b]-distance[at][bt];checks+=1
                        if margin<0:chosen=(a,b,y,x,at,bt,h,q,margin);break
                    if chosen:break
        if chosen:break
    out('geodesic_seven_metric_table.json',{'trees':T,'rotation_neighbors':adj,'distances':distance,'source_destinations':dest,'source_H':cost,'source_Q':doubles,'checked_candidate_packets':checks,'counterexample_indices':chosen,'source_queries':queries})
    if chosen is None:
        print(json.dumps({'status':'NO_SMALL_COUNTEREXAMPLE_NOT_A_PROOF','checks':checks}));return
    a,b,y,x,at,bt,h,q,margin=chosen
    def bfs(s,t):
        par={s:None};queue=collections.deque([s])
        while queue and t not in par:
            v=queue.popleft()
            for k,u in enumerate(dest[v],1):
                if u not in par:par[u]=(v,k);queue.append(u)
        if t not in par:raise ValueError('NO_SOURCE_REACHABILITY_BRIDGE')
        ans=[];v=t
        while v!=s:v,k=par[v];ans.append(k)
        return ans[::-1]
    g=T[b][0];bpre=next(s for s,t in enumerate(T) if t[0]!=g and dest[s][g-1]==b)
    prefix=[('D',k) for k in bfs(bpre,a)]+[('K',g)];window=([('D',y)] if y else [])+[('K',x)];vine=index[S.vine(7)];suffixK=bfs(bt,vine)+list(range(2,8))+list(range(6,0,-1))+bfs(vine,bpre);acur=at
    for k in suffixK:acur=dest[acur][k-1]
    word=prefix+window+[('K',k) for k in suffixK]+[('D',k) for k in bfs(acur,bpre)];initial=T[bpre];state=(initial,initial,initial);seen={};copies=[];copy=0
    while state[2] not in seen:
        assert copy<20;seen[state[2]]=copy;rows=[]
        for local,(mode,k) in enumerate(word,1):
            t=copy*len(word)+local;before=state;aa,bb,ee=state;aa,pa,ea=S.trace(aa,k);pb=pe='';eb=ev=[]
            if mode=='K':bb,pb,eb=S.trace(bb,k)
            if mode=='K' and k!=7:ee,pe,ev=S.trace(ee,k)
            state=(aa,bb,ee);rows.append({'occurrence':t,'mode':mode,'target':k,'before':before,'after':state,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ev,'genuine_F':mode=='K' and before[1][0]!=k})
        assert state[:2]==(initial,initial);copies.append(rows);copy+=1
    u=seen[state[2]];L=copy-u;rows=sum(copies[u:u+L],[]);assert rows[0]['before']==rows[-1]['after'];offset=u*len(word);lo=offset+len(prefix)+1;hi=lo+len(window)-1;seg=[r for r in rows if lo<=r['occurrence']<=hi];before=seg[0]['before'];after=seg[-1]['after'];assert (before[0],before[1])==(T[a],T[b]) and (after[0],after[1])==(T[at],T[bt]);assert sum(r['a'] for r in seg)==h and sum(r['qF'] for r in seg)==q
    prev=next(r for r in rows if r['occurrence']==lo-1);assert prev['genuine_F'] and all(not r['genuine_F'] for r in seg[:-1]) and seg[-1]['genuine_F'];marks=sorted({r['target'] for r in rows if r['genuine_F']});assert marks==list(range(1,8))
    z={'status':'SOURCE_EXACT_GEODESIC_DEBT_REFUTED','candidate':'D(A,B)=constant-rho(A,B), rho exact minimum SINGLE BST rotations','initial_diagonal':initial,'word':word,'reaching_prefix':word*u,'erased_key':7,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'natural_window':[lo,hi],'H':h,'Q':q,'rho_before':distance[a][b],'rho_after':distance[at][bt],'candidate_margin':margin,'genuine_KEEP_keys':marks,'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),'only_refuted':'specified rotation-distance potential on genuine natural packets','CD_counterexample':False,'principal_U33':'OPEN','metric_table_sha256':hashlib.sha256((B/'geodesic_seven_metric_table.json').read_bytes()).hexdigest(),'source_queries':queries}
    assert 2*z['A']>=z['QF'];out('geodesic_source_countercertificate.json',z);print(json.dumps({k:z[k] for k in ('status','H','Q','rho_before','rho_after','candidate_margin','A','QF','source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core13_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
