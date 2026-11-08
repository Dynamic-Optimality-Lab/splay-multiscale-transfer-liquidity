"""Complete implicit native9 source syntax with sparse debt coefficients.
Zero coefficients need no state entry. LOW is exact; HIGH>=3 admits EVERY
same-root A endpoint conservatively. A positive certificate therefore covers
every natural macro on the nine operand anchors, not only explored words.
"""
import json,pickle,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();z=json.loads((B/'nine_label_native_action_cache.json').read_text());N=len(z['trees']);T=z['trees'];D=z['destination'];H=z['H'];Q=z['Q'];byroot=collections.defaultdict(list)
    for a,t in enumerate(T):byroot[t[0]].append(a)
    if number==1:
        with (B/'pair9_debt_02.pkl').open('rb') as f:old=pickle.load(f)
        mirror=old['mirror'];level={code:int(v) for code,v in zip(old['nodes'],old['debt']) if v};parent={};seeded=0
        del old
        def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
        cheap=collections.defaultdict(list)
        for a,t in enumerate(T):
            for x in range(9):
                if H[a][x]==1:cheap[t[0],x].append(a)
        for b,t in enumerate(T):
            for x in range(9):
                if Q[b][x]<3:continue
                for a in cheap[t[0],x]:
                    code=canon(D[a][x],D[b][x]);v=Q[b][x]-2
                    if v>level.get(code,0):level[code]=v;parent[code]={'kind':'ACTUAL_LOW','source':canon(a,b),'helper':0,'target':x+1,'weight':-v};seeded+=1
        s={'level':level,'parent':parent,'queue':collections.deque(level),'inside':set(level),'mirror':mirror,'high_envelope':{},'checks':0,'updates':0,'fresh_negative_seeds':seeded}
    else:
        with (B/('sparse_nine_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    level,parent,queue,inside,mirror,high=(s[k] for k in ('level','parent','queue','inside','mirror','high_envelope'))
    def canon(a,b):return min(a*N+b,mirror[a]*N+mirror[b])
    limit=False
    def relax(code,v,proof):
        nonlocal limit
        if v<=level.get(code,0):return
        level[code]=v;parent[code]=proof;s['updates']+=1
        if code not in inside:inside.add(code);queue.append(code)
        if len(level)>=1900000 or v>19:limit=True
    while queue and not limit and time.process_time()-start<cap-3:
        code=queue.popleft();inside.remove(code);a,b=divmod(code,N);d=level[code];root=T[b][0]-1;aa=D[a];bb=D[b];hh=H[a];qq=Q[b]
        for x in range(9):
            if x==root:continue
            w=2*hh[x]-qq[x];s['checks']+=1
            relax(canon(aa[x],bb[x]),d-w,{'kind':'ACTUAL_LOW_OR_SINGLE_HIGH','source':code,'helper':0,'target':x+1,'weight':w})
        for y in range(9):
            if hh[y]!=1:continue
            at=aa[y]
            for x in range(9):
                if x!=root and H[at][x]==1:
                    w=4-qq[x];s['checks']+=1;relax(canon(D[at][x],bb[x]),d-w,{'kind':'ACTUAL_TWO_EVENT','source':code,'helper':y+1,'target':x+1,'weight':w})
        # The complete HIGH endpoint condition is grouped by ACTUAL BF
        # state. It is a sufficient overapproximation, not a source-cycle
        # realization rule. Reflection sends its whole group bijectively.
        for bs,flip in ((b,False),(mirror[b],True)):
            if d<=high.get(bs,0):continue
            high[bs]=d;r=T[bs][0]-1
            if d<3:continue
            for x in range(9):
                if x==r:continue
                w=6-Q[bs][x];value=d-w
                if value<=0:continue
                bt=D[bs][x]
                for at in byroot[x+1]:
                    s['checks']+=1;relax(canon(at,bt),value,{'kind':'HIGH_ENDPOINT_OVERAPPROX','source':code,'reflected_source':flip,'target':x+1,'weight':w})
        if limit:break
    with (B/('sparse_nine_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':'RESOURCE_OR_WIDTH_CHECKPOINT' if limit else 'COMPLETE_NATIVE9_SOURCE_DEBT' if not queue else 'SPARSE_DEBT_CHECKPOINT','batch':number,'nonzero_coefficients':len(level),'implicit_pair_domain':2362043,'width':max(level.values(),default=0),'pending':len(queue),'checks':s['checks'],'updates':s['updates'],'fresh_negative_seeds':s['fresh_negative_seeds'],'source_queries':0,'producer_only':True,'scope':'all ordinary natural macros whose original A and BF operands belong to9 ordered anchors, arbitrary rigid unaccessed BST gaps; no arbitrary anonymous A operand lift','principal_U33':'OPEN'}
    with (B/('sparse_nine_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
