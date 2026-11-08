import json,time
from array import array
from collections import deque,Counter
from build import BASE,load,edge_info
def main():
    out=BASE/'completion.json';assert not out.exists();c,a=load();start=time.process_time();N=c['nodes'];p=array('i',[0]*N);latest=array('i',[-1]*N);history=[];queue=deque(range(N));queued=bytearray([1])*N;updates=scans=0;cycle=None;reason=None
    while queue:
        u=queue.popleft();queued[u]=0
        if time.process_time()-start>=300:reason='CPU cap';break
        for e in range(a['offsets'][u],a['offsets'][u+1]):
            scans+=1;v=a['targets'][e];alt=p[u]+a['weights'][e]
            if alt>=p[v]:continue
            history.append((u,e,latest[u]));latest[v]=len(history)-1;p[v]=alt;updates+=1
            if alt< -2:
                path=[];k=latest[v]
                while k>=0:
                    src,ee,k=history[k];path.append(edge_info(c,a,src,ee))
                path.reverse();assert sum(r['w'] for r in path)==alt
                seen={path[0]['source']:(0,0)};prefix=0
                for j,r in enumerate(path):
                    prefix+=r['w'];node=r['destination']
                    if node in seen and prefix<seen[node][1]:cycle=path[seen[node][0]:j+1];break
                    if node not in seen or prefix>seen[node][1]:seen[node]=(j+1,prefix)
                if cycle:break
            if not queued[v]:queue.append(v);queued[v]=1
        if cycle:break
    res={'status':'NEGATIVE_EVENT_CYCLE_RAW' if cycle else 'UNKNOWN_CAP' if reason else 'COMPLETED_UNAUDITED','nodes':N,'edges':c['edges'],'edge_scans':scans,'updates':updates,'range':[min(p),max(p)],'cpu_seconds':round(time.process_time()-start,3)}
    if cycle:res['cycle']=cycle;res['cycle_weight']=sum(r['w'] for r in cycle)
    elif reason:res['reason']=reason
    else:
        with (BASE/'potential.bin').open('xb') as f:p.tofile(f)
        res['histogram']=dict(Counter(p))
    with out.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
    print(json.dumps(res,indent=2),flush=True)
if __name__=='__main__':main()
