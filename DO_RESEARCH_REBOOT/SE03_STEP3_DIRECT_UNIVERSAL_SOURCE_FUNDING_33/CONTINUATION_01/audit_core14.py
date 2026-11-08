"""Embed the equal-distance negative packet into the original closed source."""
import json,time,sys,collections,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'geodesic_seven_metric_table.json').read_text());T=list(map(fr,z['trees']));dest=z['source_destinations'];rho=z['distances'];idx={t:i for i,t in enumerate(T)};e=json.loads((B/'geodesic_seven_scalar_constraints.json').read_text())['constant_failure'];assert e and e['weight']<0 and e['rho_delta']==0;a,b,y,x,at,bt=(e[k] for k in ('a','b','helper','target','at','bt'))
    def bfs(s,t):
        par={s:None};queue=collections.deque([s])
        while queue and t not in par:
            v=queue.popleft()
            for k,u in enumerate(dest[v],1):
                if u not in par:par[u]=(v,k);queue.append(u)
        if t not in par:raise ValueError('NO_ORIGINAL_REACHABILITY_BRIDGE')
        ans=[];v=t
        while v!=s:v,k=par[v];ans.append(k)
        return ans[::-1]
    g=T[b][0];bpre=next(s for s,t in enumerate(T) if t[0]!=g and dest[s][g-1]==b);prefix=[('D',k) for k in bfs(bpre,a)]+[('K',g)];window=([('D',y)] if y else [])+[('K',x)];vine=idx[(1,'F0',(2,'F1',(3,'F2',(4,'F3',(5,'F4',(6,'F5',(7,'F6','F7')))))))]
    suffixK=bfs(bt,vine)+list(range(2,8))+list(range(6,0,-1))+bfs(vine,bpre);acur=at
    for k in suffixK:acur=dest[acur][k-1]
    word=prefix+window+[('K',k) for k in suffixK]+[('D',k) for k in bfs(acur,bpre)];initial=T[bpre]
    sp=importlib.util.spec_from_file_location('equal_metric_actual_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);oldpath=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_CAP')
        queries+=1;return oldpath(t,x)
    S.path=path;state=(initial,initial,initial);seen={};copies=[];copy=0
    while state[2] not in seen:
        assert copy<30;seen[state[2]]=copy;rows=[]
        for local,(mode,k) in enumerate(word,1):
            t=copy*len(word)+local;before=state;aa,bb,ee=state;aa,pa,ea=S.trace(aa,k);pb=pe='';eb=ev=[]
            if mode=='K':bb,pb,eb=S.trace(bb,k)
            if mode=='K' and k!=7:ee,pe,ev=S.trace(ee,k)
            state=(aa,bb,ee);rows.append({'occurrence':t,'mode':mode,'target':k,'before':before,'after':state,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ev,'genuine_F':mode=='K' and before[1][0]!=k})
        assert state[:2]==(initial,initial);copies.append(rows);copy+=1
    u=seen[state[2]];L=copy-u;rows=sum(copies[u:u+L],[]);assert rows[0]['before']==rows[-1]['after'];lo=u*len(word)+len(prefix)+1;hi=lo+len(window)-1;seg=[r for r in rows if lo<=r['occurrence']<=hi];assert fr(seg[0]['before'][0])==T[a] and fr(seg[0]['before'][1])==T[b] and fr(seg[-1]['after'][0])==T[at] and fr(seg[-1]['after'][1])==T[bt]
    assert sum(r['a'] for r in seg)==e['H'] and sum(r['qF'] for r in seg)==e['Q'];prev=next(r for r in rows if r['occurrence']==lo-1);assert prev['genuine_F'] and all(not r['genuine_F'] for r in seg[:-1]) and seg[-1]['genuine_F'];assert sorted({r['target'] for r in rows if r['genuine_F']})==list(range(1,8))
    result={'status':'SOURCE_EXACT_ALL_DISTANCE_ONLY_DEBTS_REFUTED','initial_diagonal':initial,'word':word,'reaching_prefix':word*u,'erased_key':7,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'natural_window':[lo,hi],'H':e['H'],'Q':e['Q'],'weight':e['weight'],'rho_before':rho[a][b],'rho_after':rho[at][bt],'source_indices':{'a':a,'b':b,'at':at,'bt':bt},'A':sum(r['a'] for r in rows),'QF':sum(r['qF'] for r in rows),'QE':sum(r['qE'] for r in rows),'refuted':'EVERY fixed debt F(rho(A,B)) on all genuine natural packets at this support; no chart-dependent supplemental term is included','CD_counterexample':False,'principal_U33':'OPEN','new_source_queries':queries,'metric_sha256':hashlib.sha256((B/'geodesic_seven_metric_table.json').read_bytes()).hexdigest()};assert result['rho_before']==result['rho_after'] and 2*result['A']>=result['QF'];out('equal_distance_source_countercertificate.json',result);print(json.dumps({k:result[k] for k in ('status','natural_window','H','Q','rho_before','rho_after','A','QF','u','L','new_source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core14_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
