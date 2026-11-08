"""Realize every exact feature-dual edge in its own original closed history."""
import json,time,sys,collections,importlib.util,hashlib,fractions
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    global queries
    z=json.loads((B/'native10_source_actions.json').read_text());T=list(map(fr,z['trees']));idx={t:i for i,t in enumerate(T)};dest=z['destination'];dual=json.loads((B/'uniform_feature_exact_dual.json').read_text())['certificate'];assert dual;sp=importlib.util.spec_from_file_location('feature_dual_actual_source33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S);oldpath=S.path
    def path(t,x):
        global queries
        if queries>=min(QCAP,8000) or time.process_time()-START>CAP-2:raise TimeoutError('SOURCE_EMBEDDING_CAP')
        queries+=1;return oldpath(t,x)
    S.path=path
    def bfs(s,t):
        par={s:None};queue=collections.deque([s])
        while queue and t not in par:
            v=queue.popleft()
            for x,u in enumerate(dest[v],1):
                if u not in par:par[u]=(v,x);queue.append(u)
        if t not in par:raise ValueError('SOURCE_REALIZATION_UNAVAILABLE')
        ans=[];v=t
        while v!=s:v,x=par[v];ans.append(x)
        return ans[::-1]
    vine=idx[S.vine(10)];witnesses=[]
    for number,((a,b,x),weight) in enumerate(zip(dual['native10_source_records'],dual['weights'])):
        g=T[b][0];assert T[a][0]==g and z['H'][a][x-1]==1;bpre=next(s for s,t in enumerate(T) if t[0]!=g and dest[s][g-1]==b);prefix=[('D',k) for k in bfs(bpre,a)]+[('K',g)];at,bt=dest[a][x-1],dest[b][x-1];suffixK=bfs(bt,vine)+list(range(2,11))+list(range(9,0,-1))+bfs(vine,bpre);acur=at
        for k in suffixK:acur=dest[acur][k-1]
        word=prefix+[('K',x)]+[('K',k) for k in suffixK]+[('D',k) for k in bfs(acur,bpre)];initial=T[bpre];state=(initial,initial,initial);copies=[];seen={};copy=0
        def onecopy():
            nonlocal state,copy
            rows=[]
            for local,(mode,k) in enumerate(word,1):
                before=state;aa,bb,ee=state;aa,pa,ea=S.trace(aa,k);pb=pe='';eb=ev=[]
                if mode=='K':bb,pb,eb=S.trace(bb,k)
                if mode=='K' and k!=10:ee,pe,ev=S.trace(ee,k)
                state=(aa,bb,ee);rows.append({'occurrence':copy*len(word)+local,'mode':mode,'target':k,'before':before,'after':state,'a':len(ea),'qF':len(pb)//2,'qE':len(pe)//2,'A_path':pa,'BF_path':pb,'BE_path':pe,'A_events':ea,'BF_events':eb,'BE_events':ev,'genuine_F':mode=='K' and before[1][0]!=k})
            assert state[:2]==(initial,initial);copies.append(rows);copy+=1
        while state[2] not in seen:
            assert copy<20;seen[state[2]]=copy;onecopy()
        u0=seen[state[2]];L=copy-u0;u=max(1,u0)
        while copy<u+L:onecopy()
        rows=sum(copies[u:u+L],[]);assert rows[0]['before']==rows[-1]['after'];occ=u*len(word)+len(prefix)+1;hit=next(r for r in rows if r['occurrence']==occ);prev=next(r for r in rows if r['occurrence']==occ-1);assert prev['genuine_F'] and hit['genuine_F'] and hit['a']==1 and hit['before'][:2]==(T[a],T[b]);assert sorted({r['target'] for r in rows if r['genuine_F']})==list(range(1,11));A=sum(r['a'] for r in rows);Q=sum(r['qF'] for r in rows);assert 2*A>=Q
        witnesses.append({'dual_edge_number':number,'dual_coefficient':weight,'source_indices':[a,b,x],'initial_diagonal':initial,'word':word,'reaching_prefix':word*u,'erased_key':10,'u':u,'L':L,'period':[rows[0]['occurrence'],rows[-1]['occurrence']],'rows':rows,'natural_packet':[occ,occ],'packet_H':1,'packet_Q':hit['qF'],'packet_weight':2-hit['qF'],'A':A,'QF':Q,'QE':sum(r['qE'] for r in rows),'all_genuine_KEEP_keys':list(range(1,11))})
    result={'status':'ALL_EXACT_FEATURE_DUAL_EDGES_SOURCE_REALIZED','witnesses':witnesses,'feature_count':20,'source_histories':len(witnesses),'weighted_price':dual['weighted_price'],'not_one_source_negative_cycle':True,'CD_counterexample':False,'source_queries':queries,'source_scope':'native ten-anchor original reachable exactly triple-closed histories; one distinct history per dual inequality','independent_audit':'PENDING','principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('uniform_feature_exact_dual.json','uniform_feature_extended_arrays.npz','native10_source_actions.json')}};out('uniform_feature_dual_source_certificate.json',result);print(json.dumps({'status':result['status'],'histories':len(witnesses),'source_queries':queries,'weighted_price':dual['weighted_price']}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core15_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
