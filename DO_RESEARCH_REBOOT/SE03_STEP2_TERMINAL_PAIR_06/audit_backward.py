"""Backward source-rotation reconstruction; a distinct proof/falsification child.

No positive conclusion is drawn from finite failure. Every retained edge is an
actual ordinary splay on a full named tree with unchanged arbitrary gap terms.
"""
import collections,json,sys,time
from pathlib import Path
import audit_counterattack as c
B=Path(__file__).resolve().parent;started=time.process_time();CAP=min(35,float(sys.argv[1])-4)
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>500000:raise c.Bound()
def tree(children,root):
    def go(k):
        l,r=children.get(k,(None,None))
        return c.N(k,go(l) if l is not None else 'Q'+str(k),go(r) if r is not None else 'Q'+str(k+1))
    return go(root)
def inv(t,g):
    x,l,r=t;opts=[]
    if isinstance(l,tuple):
        p,a,b=l
        opts.append(c.N(p,a,c.N(x,b,r)))
        if isinstance(a,tuple):
            gg,aa,bb=a;opts.append(c.N(gg,aa,c.N(p,bb,c.N(x,b,r))))
    if isinstance(r,tuple):
        p,b,d=r
        opts.append(c.N(p,c.N(x,l,b),d))
        if isinstance(d,tuple):
            gg,cc,dd=d;opts.append(c.N(gg,c.N(p,c.N(x,l,b),cc),dd))
    if isinstance(l,tuple) and isinstance(r,tuple):
        p,a,b=l;gg,cc,dd=r
        opts.append(c.N(gg,c.N(p,a,c.N(x,b,cc)),dd))
        opts.append(c.N(p,a,c.N(gg,c.N(x,b,cc),dd)))
    return [u for u in opts if u[0]==g and c.move(u,x)[0]==t and c.move(u,x)[1]==1]
def main():
    T0=c.canonical()
    # Exact universal local-frame challenge, all 13 physical keys retained.
    bs=tree({1:(0,4),4:(2,5),2:(None,3),5:(None,10),10:(6,11),6:(None,7),7:(None,8),8:(None,9),11:(None,12)},1)
    aa=tree({1:(0,11),11:(3,12),3:(2,9),9:(7,10),7:(5,8),5:(4,6)},1)
    a,b=aa,bs;local=[]
    for x in (11,3,9):
        na,h,_,_=c.move(a,x);bb=c.bm(b,x)
        assert bb is not None
        nb,q=bb;local.append({'x':x,'H':h,'Q':q,'leaves':[c.leaves(b),c.leaves(nb)]});a,b=na,nb
    assert [(p['H'],p['Q']) for p in local]==[(1,2),(1,2),(1,4)]
    assert [p['leaves'] for p in local[:2]]==[[3,2],[2,2]]
    # Full actual BF graph from the common source, independent of A.
    pred={T0:None};todo=collections.deque([T0]);incoming=collections.defaultdict(list);exhausted=False
    while todo:
        guard();t=todo.popleft()
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n is None:continue
            z,q=n;incoming[z].append((t,x,q))
            if z not in pred:
                pred[z]=(t,x);todo.append(z)
                if len(pred)>=15000:raise c.Bound()
    exhausted=True
    candidates=[];seen={(aa,bs,0)};queue=collections.deque([(aa,bs,0,[])])
    while queue:
        guard();a,b,cost,word=queue.popleft()
        for old,x,q in incoming[b]:
            oldA=inv(a,old[0])
            if q==4:
                for pa in oldA:
                    # Last cold9 was not refreshed on the cheap continuation.
                    if x==9:continue
                    candidates.append({'source_A':pa,'source_BF':old,'negative_target':x,
                        'negative_word':[('K',x)],'return_word':word+[('K',11),('K',3)],
                        'return_weight':cost,'final_cold':9,
                        'status':'NEEDS_ACTUAL_COLD_RECENCY_AND_CLOSED_SOURCE_EMBEDDING'})
                    if len(candidates)>=24:break
            if len(candidates)>=24:break
            if q not in (1,2) or x==9:continue
            nc=cost+(2-q)
            if nc>1:continue
            for pa in oldA:
                key=(pa,old,nc)
                if key in seen:continue
                seen.add(key);queue.append((pa,old,nc,[('K',x)]+word))
                if len(seen)>=15000:raise c.Bound()
        if len(candidates)>=24:break
    result={'status':'BACKWARD_CANDIDATES' if candidates else 'LOCAL_GUARD_REFUTED_BUT_NO_PROVENANCE_BRIDGE',
        'local_frame':{'A_before':aa,'BF_before':bs,'word':[11,3,9],'costs':local,
            'meaning':'refutes only the claim with ALL negative-source provenance removed'},
        'BF_graph_records':len(pred),'BF_graph_exhausted':exhausted,'local_BF_reachable':bs in pred,
        'backward_records':len(seen),'backward_queue':len(queue),'candidates':candidates,
        'source_engine_calls':c.account['source_engine_calls'],'proof_from_negative_search':False,'new_finite_tests':0}
    out('backward.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('candidates','local_frame')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_backward_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
