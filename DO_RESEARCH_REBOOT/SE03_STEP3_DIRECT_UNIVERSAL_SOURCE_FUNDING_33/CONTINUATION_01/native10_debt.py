"""Full native10 source law candidate, sparse and reflection invariant."""
import json,pickle,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();z=json.loads((B/'native10_source_actions.json').read_text());T=z['trees'];N=len(T);AD=z['destination'];H=z['H'];Q=z['Q'];mirror=z['mirror'];byroot=collections.defaultdict(list)
    for a,t in enumerate(T):byroot[t[0]].append(a)
    def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
    if number==1:
        cheap=collections.defaultdict(list)
        for a,t in enumerate(T):
            for x in range(10):
                if H[a][x]==1:cheap[t[0],x].append(a)
        level={};parent={};checks=0
        for b,t in enumerate(T):
            for x in range(10):
                q=Q[b][x]
                if q<3:continue
                for a in cheap[t[0],x]:
                    checks+=1;code=canon(AD[a][x],AD[b][x]);v=q-2
                    if v>level.get(code,0):level[code]=v;parent[code]=('ACTUAL_H1',canon(a,b),0,x+1,-v)
        s={'level':level,'parent':parent,'queue':collections.deque(level),'inside':set(level),'high':{},'checks':checks,'updates':0,'seed_coefficients':len(level)}
    else:
        with (B/('native10_debt_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    level,parent,queue,inside,high=(s[k] for k in ('level','parent','queue','inside','high'));limit=None
    def relax(code,val,edge):
        nonlocal limit
        if val<=level.get(code,0):return
        level[code]=val;parent[code]=edge;s['updates']+=1
        if code not in inside:inside.add(code);queue.append(code)
        if len(level)>=1850000:limit='LIVE_STATE_RESERVE'
        if val>19:limit='WIDTH_EXCEEDS_BANK25_C3_LICENSE'
    while queue and limit is None and time.process_time()-start<cap-3:
        code=queue.popleft();inside.remove(code);a,b=divmod(code,N);d=level[code];root=T[b][0]-1
        for x in range(10):
            if x==root or H[a][x]>2:continue
            w=2*H[a][x]-Q[b][x];s['checks']+=1;relax(canon(AD[a][x],AD[b][x]),d-w,('ACTUAL_DIRECT_LOW',code,0,x+1,w))
        for y in range(10):
            if H[a][y]!=1:continue
            at=AD[a][y]
            for x in range(10):
                if x!=root and H[at][x]==1:
                    w=4-Q[b][x];s['checks']+=1;relax(canon(AD[at][x],AD[b][x]),d-w,('ACTUAL_TWO_EVENT',code,y+1,x+1,w))
        for bs in {b,mirror[b]}:
            if d<=high.get(bs,0):continue
            high[bs]=d
            if d<3:continue
            for x in range(10):
                if x==T[bs][0]-1:continue
                w=6-Q[bs][x];v=d-w
                if v<=0:continue
                for at in byroot[x+1]:s['checks']+=1;relax(canon(at,AD[bs][x]),v,('HIGH_ANY_ENDPOINT',code,0,x+1,w))
        if limit:break
    with (B/('native10_debt_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':limit if limit else 'COMPLETE_NATIVE10_SOURCE_DEBT' if not queue else 'NATIVE10_BATCH_CHECKPOINT','batch':number,'coefficients':len(level),'width':max(level.values(),default=0),'pending':len(queue),'checks':s['checks'],'updates':s['updates'],'seed_coefficients':s['seed_coefficients'],'source_queries':0,'principal_U33':'OPEN','verification':'PRODUCER ONLY until complete independently audited','scope':'fixed ten-anchor A/B backbones, all original KEEP/DELETE words and rigid unaccessed gaps'}
    with (B/('native10_debt_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
