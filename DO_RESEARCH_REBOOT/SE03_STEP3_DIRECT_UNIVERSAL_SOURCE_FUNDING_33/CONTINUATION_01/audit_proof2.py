"""Exact cached nine-core difference constraints; no new source invocation."""
import json,time,sys,collections
from pathlib import Path
B=Path(__file__).resolve().parent;CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    z=json.loads((B/'nine_label_native_action_cache.json').read_text());N=len(z['trees']);dst=z['destination'];q=z['Q'];D=[0]*N;parent=[None]*N;length=[0]*N
    todo=collections.deque(range(N));inside=bytearray([1])*N;checks=0;bad=None
    while todo and bad is None:
        s=todo.popleft();inside[s]=0
        for x in range(9):
            t=dst[s][x];checks+=1;v=D[s]+q[s][x]-2
            if v>D[t]:
                D[t]=v;parent[t]=(s,x+1,t,q[s][x]);length[t]=length[s]+1
                if length[t]>=N:bad=t;break
                if not inside[t]:inside[t]=1;todo.append(t)
        if checks%8192<9 and time.process_time()-START>CAP-2:raise TimeoutError('STATIC_GRAPH_CAP')
    cycle=[]
    if bad is not None:
        v=bad
        for _ in range(N):v=parent[v][0]
        start=v
        while True:
            row=parent[v];cycle.append(row);v=row[0]
            if v==start:break
        cycle.reverse();assert sum(2-r[3] for r in cycle)<0
    else:assert all(2-q[s][x]+D[dst[s][x]]-D[s]>=0 for s in range(N) for x in range(9))
    result={'status':'NINE_CORE_B_ONLY_REFUTED' if cycle else 'NINE_CORE_B_ONLY_PROVED','D':None if cycle else D,'width':None if cycle else max(D),'cycle':cycle,'cycle_price':sum(2-r[3] for r in cycle),'checks':checks,'source_queries':0,'actual_CD_refutation':False}
    out('nine_core_B_only_result.json',result);print(json.dumps({k:result[k] for k in ('status','width','cycle_price','checks')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
