"""Bounded monotone integer construction with persistent exact path provenance."""
import json,time,sys
from array import array
from collections import deque,Counter
from build import BASE,load,edge_info
def main():
    out=BASE/'completion.json';assert not out.exists();c,a=load();start=time.process_time();N=c['nodes']
    initial=array('i',[-c['psi'][b] for b in a['ordinary_b']]);labels=array('i',initial)
    queue=deque(range(N));queued=bytearray([1])*N;latest=array('i',[-1])*N;history=[];scans=pops=updates=0;obstruction=None;reason=None
    while queue:
        u=queue.popleft();queued[u]=0;pops+=1;du=labels[u]
        if time.process_time()-start>=300:reason='CPU cap';break
        for e in range(a['offsets'][u],a['offsets'][u+1]):
            scans+=1;v=a['targets'][e];alt=du+a['weights'][e]
            if alt>=labels[v]:continue
            history.append((u,e,latest[u]));latest[v]=len(history)-1;labels[v]=alt;updates+=1
            if alt< -2:
                path=[];k=latest[v]
                while k>=0:
                    src,ee,k=history[k];path.append(edge_info(c,a,src,ee))
                path.reverse();origin=path[0]['source'];assert initial[origin]+sum(r['w'] for r in path)==alt
                assert all(x['destination']==y['source'] for x,y in zip(path,path[1:]))
                seen={origin:(0,0)};prefix=0;cycle=None
                for j,r in enumerate(path):
                    prefix+=r['w'];state=r['destination']
                    if state in seen and prefix<seen[state][1]:cycle=path[seen[state][0]:j+1];break
                    if state not in seen or prefix>seen[state][1]:seen[state]=(j+1,prefix)
                obstruction={'origin':origin,'initial_upper_bound':initial[origin],'derived_upper_bound':alt,'lower_bound':-2,'path':path,'negative_cycle':cycle,'original_roots_verified':False}
                break
            if not queued[v]:queue.append(v);queued[v]=1
        if obstruction:break
        assert updates<=2*N and scans<=3*c['edges'] and pops<=3*N
    result={'nodes':N,'edges':c['edges'],'edge_scans':scans,'queue_pops':pops,'updates':updates,
      'new_fit_method':'exact bounded monotone recurrence','cpu_seconds':round(time.process_time()-start,3)}
    if obstruction:result.update(status='RANGE_TWO_TEMPLATE_REFUTED_EXACT',obstruction=obstruction)
    elif reason:result.update(status='UNKNOWN_CAP',reason=reason)
    else:
        assert min(labels)>=-2 and max(labels)<=0 and all(labels[u]<=initial[u] for u in range(N))
        with (BASE/'potential.bin').open('xb') as f:labels.tofile(f)
        result.update(status='COMPLETED_UNAUDITED',range=[min(labels),max(labels)],histogram=dict(Counter(labels)),changed_nodes=sum(x!=y for x,y in zip(initial,labels)))
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
