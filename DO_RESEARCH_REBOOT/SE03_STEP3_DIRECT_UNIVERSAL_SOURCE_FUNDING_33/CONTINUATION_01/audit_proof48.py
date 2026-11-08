"""Proof composition of ACCEPTED primitive identities; no new splay-engine calls.
New words are certified finite compositions, explicitly not fresh kernel replays.
"""
import json,time,sys,collections,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    nativepath=B/'native10_source_actions.json';raw=nativepath.read_bytes();old=json.loads((B/'native10_source_independent_audit.json').read_text());assert hashlib.sha256(raw).hexdigest()==old['input_sha256'];z=json.loads(raw);T=z['trees'];D=z['destination'];H=z['H'];Q=z['Q'];N=len(T);root=[t[0] for t in T];inventory=json.loads((B/'diagonal_zero_dual_independent_algebra_audit.json').read_text())['source_inventory'];vine=0;assert root[vine]==1
    forward={vine:None};queue=collections.deque([vine]);reverse=[[] for _ in range(N)];incoming={}
    for s in range(N):
        for x,t in enumerate(D[s],1):
            reverse[t].append((s,x))
            if root[s]!=x and t not in incoming:incoming[t]=(s,x)
    while queue:
        s=queue.popleft()
        for x,t in enumerate(D[s],1):
            if t not in forward:forward[t]=(s,x);queue.append(t)
    backward={vine:None};queue=collections.deque([vine])
    while queue:
        t=queue.popleft()
        for s,x in reverse[t]:
            if s not in backward:backward[s]=(t,x);queue.append(s)
    assert len(forward)==len(backward)==len(incoming)==N
    def fromvine(t):
        ans=[]
        while t!=vine:t,x=forward[t];ans.append(x)
        return ans[::-1]
    def tovine(s):
        ans=[]
        while s!=vine:s,x=backward[s];ans.append(x)
        return ans
    records=[];complete=True
    for item in inventory:
        if time.process_time()-START>CAP-.3:complete=False;break
        if item['kind']=='already_closed_source_corpus':records.append(dict(item,reused_existing_closed_source=True));continue
        a,b,x=(item['source'][k] for k in ('a','b','target'));bpre,g=incoming[b];assert g==root[b] and root[a]==g;prefix=[('D',k) for k in tovine(bpre)+fromvine(a)]+[('K',g)];aa,bb=D[a][x-1],D[b][x-1];suffix=tovine(bb)+list(range(2,11))+list(range(9,0,-1))+fromvine(bpre);acur=aa
        for k in suffix:acur=D[acur][k-1]
        word=prefix+[('K',x)]+[('K',k) for k in suffix]+[('D',k) for k in tovine(acur)+fromvine(bpre)]
        def execute(E,copy):
            A=F=bpre;rows=[]
            for local,(mode,k) in enumerate(word,1):
                oldA,oldF,oldE=A,F,E;A=D[A][k-1];hh=H[oldA][k-1];q=qe=0
                if mode=='K':F=D[F][k-1];q=Q[oldF][k-1]
                if mode=='K' and k!=10:E=D[E][k-1];qe=Q[oldE][k-1]
                rows.append([copy*len(word)+local,mode,k,oldA,oldF,oldE,A,F,E,hh,q,qe])
            assert A==F==bpre;return E,rows
        E=bpre;seen={};copies=[];j=0
        while E not in seen:
            seen[E]=j;E,rr=execute(E,j);copies.append(rr);j+=1
        u0=seen[E];L=j-u0;u=max(1,u0)
        while j<u+L:E,rr=execute(E,j);copies.append(rr);j+=1
        rows=sum(copies[u:u+L],[]);occ=u*len(word)+len(prefix)+1;hit=next(r for r in rows if r[0]==occ);assert hit[3:5]==[a,b] and (hit[9],hit[10])==(item['H'],item['Q']) and rows[0][3:6]==rows[-1][6:9];records.append(dict(item,initial_diagonal_index=bpre,word=word,u=u,L=L,period=[rows[0][0],rows[-1][0]],selected_natural_occurrence=occ,rows=rows,primitive_compositions=(u+L)*len(word)))
    result={'status':'COMPLETE_CLOSED_SOURCE_COMPOSITION_AUDIT_PENDING' if complete else 'CAPPED_SOURCE_COMPOSITION_CHECKPOINT','completed':len(records),'required':len(inventory),'records':records,'complete_primitive_graph_strong_connectivity':{'nodes':N,'forward':len(forward),'backward':len(backward)},'new_source_engine_calls':0,'new_source_queries':0,'verification_method':'finite proof composition of immutable fully audited ordinary-splay primitive identities; NOT a new source-engine replay','principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ('native10_source_actions.json','native10_source_independent_audit.json','diagonal_zero_dual_independent_algebra_audit.json','diagonal_zero_quadratic_exact_dual.json')}};out('diagonal_zero_dual_closed_source_compositions.json',result);print(json.dumps({'status':result['status'],'completed':len(records),'required':len(inventory),'new_source_queries':0}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof48_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
