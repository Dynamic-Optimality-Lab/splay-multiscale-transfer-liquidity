"""Monotone exact integer completion from FRC01, with persistent path obstruction provenance."""
import json,time
from array import array
from collections import deque,Counter
from build_fragment import BASE,load,edge_info
OUT=BASE/'completion_result.json'
def main():
    assert not OUT.exists();c,a=load();N=c['nodes'];start=time.process_time()
    ds=array('i',[c['initial_by_B'][b] for b in a['ordinary_b']]);initial=array('i',ds)
    queue=deque(range(N));queued=bytearray([1])*N;history=[];latest=array('i',[-1])*N
    off=a['offsets'];dst=a['targets'];weights=a['weights'];scans=pops=updates=0;obstruction=None;reason=None
    while queue:
        u=queue.popleft();queued[u]=0;pops+=1;du=ds[u]
        if time.process_time()-start>=300:reason='CPU cap';break
        for e in range(off[u],off[u+1]):
            scans+=1
            if scans>50000000:reason='edge scan cap';break
            v=dst[e];alt=du+weights[e]
            if alt>=ds[v]:continue
            history.append((u,e,latest[u]));latest[v]=len(history)-1;ds[v]=alt;updates+=1
            if alt< -2:
                edges=[];k=latest[v]
                while k>=0:
                    src,ee,k=history[k];edges.append(edge_info(c,a,src,ee))
                edges.reverse();origin=edges[0]['source'];upper=initial[origin]
                assert all(l['destination']==r['source'] for l,r in zip(edges,edges[1:]))
                assert upper+sum(r['weight'] for r in edges)==alt
                seen={origin:0};cycle=None
                for j,r in enumerate(edges):
                    if r['destination'] in seen:
                        chunk=edges[seen[r['destination']]:j+1]
                        if sum(x['weight'] for x in chunk)<0:cycle=chunk;break
                    else:seen[r['destination']]=j+1
                obstruction={'destination':v,'derived_upper_bound':alt,'required_lower_bound':-2,
                     'initial_source':origin,'initial_source_upper_bound':upper,'edges':edges,
                     'negative_cycle':cycle,'full_original_roots_verified':False}
                break
            if not queued[v]:queue.append(v);queued[v]=1
        if obstruction or reason:break
    result={'nodes':N,'edges':c['edges'],'edge_scans':scans,'queue_pops':pops,'updates':updates,
            'cpu_seconds':round(time.process_time()-start,3),'solver_invoked':False}
    if obstruction:
        result.update(status='NEGATIVE_CYCLE_RAW' if obstruction['negative_cycle'] else 'RANGE_TWO_COMPLETION_REFUTED',obstruction=obstruction)
    elif reason:result.update(status='UNKNOWN_CAP',reason=reason)
    else:
        assert min(ds)>=-2 and max(ds)<=0
        assert all(ds[u]<=initial[u] and ds[u]<=-c['psi'][a['ordinary_b'][u]] for u in range(N))
        with (BASE/'potential.bin').open('xb') as f:ds.tofile(f)
        result.update(status='COMPLETED_LABELS_UNAUDITED',minimum=min(ds),maximum=max(ds),
                      changed_nodes=sum(x!=y for x,y in zip(ds,initial)),histogram=dict(Counter(ds)))
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
