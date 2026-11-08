"""Exact integer label correction; outputs a fully checked potential or raw negative cycle."""
import json,time
from pathlib import Path
from array import array
from collections import deque,Counter
from fragment_graph import BASE,load,edge_info
OUT=BASE/'fragment_result.json'

def main():
    assert not OUT.exists();c,a=load();N=c['nodes'];no=c['ordinary_nodes'];start=time.process_time()
    off=a['offsets'];dst=a['targets'];w=a['weights']
    dist=array('i',[-c['psi'][b] for b in a['ordinary_b']]+[-c['psi'][b] for b in c['M_B_indices']])
    pred=array('i',[-1])*N;pe=array('i',[-1])*N;queued=bytearray([1])*N;q=deque(range(N))
    scans=updates=pops=0;cycle=None;reason=None;checks=0
    def extract(v):
        seen={};path=[];u=v
        while u>=0 and u not in seen and len(path)<=N:
            seen[u]=len(path);path.append(u);u=pred[u]
        if u<0 or u not in seen:return None
        vertices=path[seen[u]:][::-1]
        es=[edge_info(c,a,pred[t],pe[t]) for t in vertices]
        if sum(e['weight'] for e in es)>=0:return None
        for e,f in zip(es,es[1:]+es[:1]):
            assert e['destination']==f['source']
            assert off[e['source']]<=e['csr_edge']<off[e['source']+1]
        return es
    while q:
        u=q.popleft();queued[u]=0;pops+=1;du=dist[u]
        if time.process_time()-start>=300:reason='CPU cap';break
        for e in range(off[u],off[u+1]):
            if scans>=50000000:reason='edge-scan cap';break
            scans+=1;v=dst[e];alt=du+w[e]
            if alt>=dist[v]:continue
            assert -2147483648<alt<2147483647,'storage bound; exact Int may not wrap'
            dist[v]=alt;pred[v]=u;pe[v]=e;updates+=1
            if not queued[v]:q.append(v);queued[v]=1
            if updates%32768==0:
                checks+=1;cycle=extract(v)
                if cycle:break
        if cycle or reason:break
        if pops%65536==0:
            print(json.dumps({'pops':pops,'queue':len(q),'edge_scans':scans,'updates':updates,
                              'min_label':min(dist),'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    result={'nodes':N,'edges':len(dst),'edge_scans':scans,'updates':updates,'queue_pops':pops,
            'cycle_extraction_checks':checks,'solver_invoked':False,
            'cpu_seconds':round(time.process_time()-start,3)}
    if cycle:
        result.update(status='NEGATIVE_CYCLE_RAW',cycle=cycle,total_weight=sum(e['weight'] for e in cycle),
                      mixed=any(e['kind']=='OM' for e in cycle),original_roots_verified=False)
    elif reason:result.update(status='UNKNOWN_CAP',reason=reason)
    else:
        check_start=time.process_time();hist=Counter();minimum=None
        for u in range(N):
            for e in range(off[u],off[u+1]):
                residual=w[e]+dist[u]-dist[dst[e]]
                assert residual>=0,(u,dst[e],w[e],dist[u],dist[dst[e]])
                hist[residual]+=1;minimum=residual if minimum is None else min(minimum,residual)
            assert time.process_time()-check_start<120,'UNKNOWN: final edge audit cap'
        with (BASE/'potential.bin').open('xb') as f:dist.tofile(f)
        result.update(status='POTENTIAL_VERIFIED',potential_min=min(dist),potential_max=max(dist),
                      exact_inequalities=len(dst),minimum_residual=minimum,residual_histogram=dict(hist),
                      final_audit_cpu_seconds=round(time.process_time()-check_start,3))
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result),flush=True)
if __name__=='__main__':main()
