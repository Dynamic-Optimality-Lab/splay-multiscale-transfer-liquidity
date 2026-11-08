"""Complete eight-core B syntax, a sharply specified candidate source law.
Tests existence of2-Q+DeltaD>=0 without A assumptions beyond H>=1.
Positive result would lift by arbitrary private-term substitution; a failed
B-only law is not a failure of actual2H-Q source funding.
"""
import json,time,sys,importlib.util,functools,collections
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();queries=0
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
def main():
    global queries
    sp=importlib.util.spec_from_file_location('original_eight33',P/'SE03_STEP2_COLD_NEG2_01/source_model.py');S=importlib.util.module_from_spec(sp);sp.loader.exec_module(S)
    original=S.path
    def path(t,x):
        global queries
        if queries>=QCAP or time.process_time()-START>=CAP-2:raise TimeoutError('SOURCE_PHASE_CAP')
        queries+=1;return original(t,x)
    S.path=path
    @functools.lru_cache(None)
    def trees(lo,hi):
        if lo>hi:return ('F'+str(hi),)
        return tuple((k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))
    T=trees(1,8);assert len(T)==1430;index={t:i for i,t in enumerate(T)};rel=[];adj=[[] for _ in T]
    for b,t in enumerate(T):
        for x in range(1,9):
            dst,pa,ev=S.trace(t,x);row=(b,x,index[dst],len(pa)//2);rel.append(row)
            if x!=t[0]:adj[b].append(row)
    # Exact difference-constraint test on COMPLETE necessary syntax.
    D=[0]*len(T);length=[0]*len(T);parent=[None]*len(T);todo=collections.deque(range(len(T)));inside=set(todo);bad=None;checks=0
    while todo and bad is None:
        b=todo.popleft();inside.remove(b)
        for row in adj[b]:
            s,x,t,q=row;checks+=1;value=D[s]+q-2
            if value>D[t]:
                D[t]=value;parent[t]=row;length[t]=length[s]+1
                if length[t]>=len(T):bad=t;break
                if t not in inside:inside.add(t);todo.append(t)
        if checks%4096==0 and (time.process_time()-START>=CAP-2 or checks>4500000):raise TimeoutError('STATIC_RESERVE')
    cycle=[]
    if bad is not None:
        v=bad
        for _ in T:assert parent[v] is not None;v=parent[v][0]
        start=v
        while True:
            row=parent[v];cycle.append(row);v=row[0]
            if v==start:break
        cycle.reverse();assert all(cycle[i][2]==cycle[(i+1)%len(cycle)][0] for i in range(len(cycle)))
        assert sum(q-2 for _,_,_,q in cycle)>0
    else:assert all(2-q+D[t]-D[s]>=0 for s,x,t,q in rel)
    out('eight_core_B_source_relation.json',{'status':'COMPLETE_EIGHT_CORE_SYMBOLIC_RELATION','trees':T,'relation':rel,'source_queries':queries,
        'syntax':'all1430 ordered core8 trees, arbitrary independent ordered gap BSTs; no finite private population cutoff'})
    result={'status':'B_ONLY_SOURCE_LAW_REFUTED' if cycle else 'B_ONLY_SOURCE_LAW_PROVED','D':None if cycle else D,'width':None if cycle else max(D),
        'cycle':cycle,'cycle_price':sum(2-q for _,_,_,q in cycle),'checks':checks,'new_source_queries':queries,
        'counterexample_to_actual_CD':False,'claim':'only the specified2-Q B-only license is decided'}
    out('eight_core_B_law_result.json',result);print(json.dumps({k:result[k] for k in ('status','width','cycle_price','checks','new_source_queries')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_core_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':queries,'source_engine_calls':queries})
