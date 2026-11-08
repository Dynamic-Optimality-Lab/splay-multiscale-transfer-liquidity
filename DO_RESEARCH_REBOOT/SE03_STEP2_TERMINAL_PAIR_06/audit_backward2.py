"""Recursive child: two-event and paired predecessors of the shallow tail.
Exact inverses are checked by the original source trace before retention.
"""
import collections,json,sys,time
from pathlib import Path
import audit_backward as p
from source_model import at,put,path
c=p.c;B=Path(__file__).resolve().parent;started=time.process_time();CAP=min(42,float(sys.argv[1])-4)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>=1000000:raise c.Bound()
def inv_all(t,double=None):
    x,l,r=t;opts=[]
    if isinstance(l,tuple):
        a,L,R=l
        if double is not True:opts.append(c.N(a,L,c.N(x,R,r)))
        if isinstance(L,tuple) and double is not False:
            g,A,Z=L;opts.append(c.N(g,A,c.N(a,Z,c.N(x,R,r))))
    if isinstance(r,tuple):
        a,L,R=r
        if double is not True:opts.append(c.N(a,c.N(x,l,L),R))
        if isinstance(R,tuple) and double is not False:
            g,Z,D=R;opts.append(c.N(g,c.N(a,c.N(x,l,L),Z),D))
    if isinstance(l,tuple) and isinstance(r,tuple) and double is not False:
        a,L,R=l;g,C,D=r
        opts += [c.N(g,c.N(a,L,c.N(x,R,C)),D),c.N(a,L,c.N(g,c.N(x,R,C),D))]
    return list(dict.fromkeys(opts))
def ip(a,g,H):
    x=a[0]
    if H==1:return [(u,[('K',x)]) for u in p.inv(a,g)]
    opts=[]
    for double in (False,True):
        for mid in inv_all(a,double):
            if mid[0]!=g:continue
            loc=path(mid,x);v=at(mid,loc)
            for oldv in inv_all(v,True):
                old=put(mid,loc,oldv)
                if c.move(old,x)[:2]==(a,2):opts.append((old,[('K',x)]))
    for y in range(1,12):
        if y==x or y==g:continue
        for mid in p.inv(a,y):
            for old in p.inv(mid,g):opts.append((old,[('D',y),('K',x)]))
    unique={}
    for a,w in opts:unique.setdefault(a,w)
    return list(unique.items())
def main():
    local=json.loads((B/'backward.json').read_text())['local_frame']
    def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
    aa,bs=freeze(local['A_before']),freeze(local['BF_before']);T0=c.canonical()
    pred={T0:None};todo=collections.deque([T0]);incoming=collections.defaultdict(list)
    while todo:
        guard();t=todo.popleft()
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n is None:continue
            z,q=n;incoming[z].append((t,x,q))
            if z not in pred:pred[z]=(t,x);todo.append(z)
    candidates=[];seen={(aa,bs):0};queue=collections.deque([(aa,bs,0,[])]);stopped=None
    try:
        while queue:
            guard();a,b,cost,word=queue.popleft()
            if seen.get((a,b))!=cost:continue
            for old,x,q in incoming[b]:
                if q==4 and x!=9:
                    for pa,w in ip(a,old[0],1):
                        candidates.append({'source_A':pa,'source_BF':old,'negative_target':x,'negative_word':w,
                            'return_word':word+[('K',11),('K',3)],'return_weight':cost,'final_cold':9})
                if q==1:
                    for older,y,q0 in incoming[old]:
                        if q0!=5 or y==9 or x==9:continue
                        for amid,w2 in ip(a,old[0],1):
                            for pa,w1 in ip(amid,older[0],1):
                                candidates.append({'source_A':pa,'source_BF':older,'negative_target':y,'negative_word':w1+w2,
                                    'return_word':word+[('K',11),('K',3)],'return_weight':cost,'final_cold':9})
                if len(candidates)>=32:break
                if q not in (1,2,3,4) or x==9:continue
                H=1 if q<=2 else 2;nc=cost+2*H-q
                if nc>1:continue
                for pa,w in ip(a,old[0],H):
                    key=(pa,old)
                    if seen.get(key,2)<=nc:continue
                    seen[key]=nc;queue.append((pa,old,nc,w+word))
                    if len(seen)>=12000:raise c.Bound()
            if len(candidates)>=32:break
    except c.Bound:stopped='PREDECLARED_BOUND'
    result={'status':'BACKWARD_CANDIDATES' if candidates else 'NO_BACKWARD_COUNTERCERTIFICATE',
        'BF_records':len(pred),'backward_records':len(seen),'queue':len(queue),'candidates':candidates,
        'stop':stopped or ('CANDIDATE_BOUND' if candidates else 'DECLARED_BACKWARD_FAMILY_EXHAUSTED'),
        'scope':'two-event singleton and negative-pair inverses; zero paired predecessors not included',
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,'proof_from_negative_search':False}
    out('backward2.json',result);print(json.dumps({k:v for k,v in result.items() if k!='candidates'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_backward2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
