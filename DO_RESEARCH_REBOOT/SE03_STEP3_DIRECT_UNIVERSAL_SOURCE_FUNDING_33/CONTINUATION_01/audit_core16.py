"""Original closed source realization of the new zero-price formula failure."""
import json,time,sys,collections,importlib.util,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;START=time.process_time();CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));D=z['destination'];idx={t:i for i,t in enumerate(T)};failure=json.loads((B/'diagonal_zero_vine_adversary.json').read_text());a,b,x=failure['failing_source_record'];g=T[b][0];bpre=next(i for i,t in enumerate(T) if t[0]!=g and D[i][g-1]==b)
    def bfs(s,t):
        queue=collections.deque([s]);par={s:None}
        while queue and t not in par:
            v=queue.popleft()
            for k,u in enumerate(D[v],1):
                if u not in par:par[u]=(v,k);queue.append(u)
        assert t in par;v=t;word=[]
        while v!=s:v,k=par[v];word.append(k)
        return word[::-1]
    sp=importlib.util.spec_from_file_location('diagonal_zero_actual_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);oldpath=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_LIMIT')
        queries+=1;return oldpath(t,x)
    S.path=path;vine=idx[S.vine(10)];prefix=[('D',k) for k in bfs(bpre,a)]+[('K',g)];aa,bb=D[a][x-1],D[b][x-1];kk=bfs(bb,vine)+list(range(2,11))+list(range(9,0,-1))+bfs(vine,bpre)
    for k in kk:aa=D[aa][k-1]
    word=prefix+[('K',x)]+[('K',k) for k in kk]+[('D',k) for k in bfs(aa,bpre)];initial=T[bpre];state=(initial,initial,initial);seen={};copies=[];copy=0
    def onecopy():
        nonlocal state,copy
        rows=[]
        for local,(mode,k) in enumerate(word,1):
            before=state;A,F,E=state;A,pa,ea=S.trace(A,k);pf=pe='';ef=ee=[]
            if mode=='K':F,pf,ef=S.trace(F,k)
            if mode=='K' and k!=10:E,pe,ee=S.trace(E,k)
            state=(A,F,E);rows.append({'occurrence':copy*len(word)+local,'mode':mode,'target':k,'genuine_F':mode=='K' and before[1][0]!=k,'before':before,'after':state,'A_path':pa,'BF_path':pf,'BE_path':pe,'A_events':ea,'BF_events':ef,'BE_events':ee,'a':len(ea),'qF':len(pf)//2,'qE':len(pe)//2})
        assert state[:2]==(initial,initial);copies.append(rows);copy+=1
    while state[2] not in seen:
        assert copy<20;seen[state[2]]=copy;onecopy()
    u0=seen[state[2]];L=copy-u0;u=max(u0,1)
    while copy<u+L:onecopy()
    rows=sum(copies[u:u+L],[]);occ=u*len(word)+len(prefix)+1;hit=next(r for r in rows if r['occurrence']==occ);assert rows[0]['before']==rows[-1]['after'] and hit['before'][:2]==(T[a],T[b]) and hit['a']==failure['H'] and hit['qF']==failure['Q'];assert sorted({r['target'] for r in rows if r['genuine_F']})==list(range(1,11));A=sum(r['a'] for r in rows);Q=sum(r['qF'] for r in rows);assert 2*A>=Q
    result={'status':'SOURCE_EXACT_ZERO_PRICE_DIAGONAL_ZERO_FORMULA_FAILURE','initial_diagonal':initial,'word':word,'reaching_prefix':word*u,'erased_key':10,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'natural_packet':[occ,occ],'H':hit['a'],'Q':hit['qF'],'price':2*hit['a']-hit['qF'],'A':A,'QF':Q,'QE':sum(r['qE'] for r in rows),'candidate_exact_margin':failure['exact_margin'],'new_source_queries':queries,'only_specific_formula_refuted':True,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('diagonal_zero_vine_adversary.json','diagonal_zero_result_02.json')}};out('diagonal_zero_source_countercertificate.json',result);print(json.dumps({k:result[k] for k in ('status','natural_packet','H','Q','price','A','QF','new_source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core16_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
