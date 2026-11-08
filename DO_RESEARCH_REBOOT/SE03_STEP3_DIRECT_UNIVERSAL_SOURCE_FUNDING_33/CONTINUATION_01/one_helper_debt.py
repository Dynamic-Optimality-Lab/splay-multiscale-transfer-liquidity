"""Nine BF anchors and one retained anonymous A operand, helper physical3.
Full A ten-anchor syntax; no unary suppression. HIGH is a conservative
any-endpoint source hyperedge, not a path-realization assertion.
"""
import json,pickle,time,collections
from pathlib import Path
B=Path(__file__).resolve().parent
def run(number,cap):
    start=time.process_time();A=json.loads((B/'ten_anchor_LOW_source_schemas.json').read_text());F=json.loads((B/'nine_label_native_action_cache.json').read_text());AT=A['trees'];BT=F['trees'];AN=len(AT);BN=len(BT);AD=A['LOW_destination'];AH=A['H'];BD=F['destination'];BQ=F['Q'];marks=[1,2]+list(range(4,11));roots=collections.defaultdict(list)
    for i,t in enumerate(AT):roots[t[0]].append(i)
    if number==1:
        cheap=collections.defaultdict(list)
        for a,t in enumerate(AT):
            for x in marks:
                if AH[a][x-1]==1:cheap[t[0],x].append(a)
        level={};parent={};checks=0
        for b,t in enumerate(BT):
            g=marks[t[0]-1]
            for x in range(9):
                q=BQ[b][x]
                if q<3:continue
                px=marks[x]
                for a in cheap[g,px]:
                    checks+=1;code=AD[a][px-1]*BN+BD[b][x];v=q-2
                    if v>level.get(code,0):level[code]=v;parent[code]=('ACTUAL_H1',a*BN+b,0,x+1,-v)
        s={'level':level,'parent':parent,'queue':collections.deque(level),'inside':set(level),'high':{},'checks':checks,'updates':0,'seed_coefficients':len(level)}
    else:
        with (B/('one_helper_%02d.pkl'%(number-1))).open('rb') as f:s=pickle.load(f)
    level,parent,queue,inside,high=(s[k] for k in ('level','parent','queue','inside','high'));limit=None
    def relax(code,val,edge):
        nonlocal limit
        if val<=level.get(code,0):return
        level[code]=val;parent[code]=edge;s['updates']+=1
        if code not in inside:inside.add(code);queue.append(code)
        if len(level)>=1850000:limit='LIVE_STATE_RESERVE'
        if val>19:limit='WIDTH_EXCEEDS_BANK25_C3_LICENSE'
    while queue and limit is None and time.process_time()-start<cap-3:
        code=queue.popleft();inside.remove(code);a,b=divmod(code,BN);d=level[code];br=BT[b][0]-1;assert AT[a][0]==marks[br]
        for x in range(9):
            px=marks[x];h=AH[a][px-1]
            if x==br or h>2:continue
            s['checks']+=1;relax(AD[a][px-1]*BN+BD[b][x],d-(2*h-BQ[b][x]),('ACTUAL_DIRECT_LOW',code,0,x+1,2*h-BQ[b][x]))
        for y in range(10):
            if AH[a][y]!=1:continue
            at=AD[a][y]
            for x in range(9):
                if x!=br and AH[at][marks[x]-1]==1:
                    w=4-BQ[b][x];s['checks']+=1;relax(AD[at][marks[x]-1]*BN+BD[b][x],d-w,('ACTUAL_TWO_EVENT',code,y+1,x+1,w))
        if d>high.get(b,0):
            high[b]=d
            if d>=3:
                for x in range(9):
                    if x==br:continue
                    w=6-BQ[b][x];v=d-w
                    if v<=0:continue
                    bt=BD[b][x]
                    for at in roots[marks[x]]:s['checks']+=1;relax(at*BN+bt,v,('HIGH_ANY_ENDPOINT',code,0,x+1,w))
        if limit:break
    with (B/('one_helper_%02d.pkl'%number)).open('xb') as f:pickle.dump(s,f,pickle.HIGHEST_PROTOCOL)
    result={'status':limit if limit else 'COMPLETE_ONE_HELPER_SOURCE_DEBT' if not queue else 'ONE_HELPER_BATCH_CHECKPOINT','batch':number,'nonzero_coefficients':len(level),'width':max(level.values(),default=0),'pending':len(queue),'checks':s['checks'],'updates':s['updates'],'seed_coefficients':s['seed_coefficients'],'source_queries':0,'source_schema_instantiations_reused':A['reused_free_gap_schema_instantiations'],'verification':'PRODUCER ONLY until complete independent check','scope':'fixed nine BF anchors plus retained A-only helper key3, full ten-anchor A syntax and rigid unaccessed gaps','principal_U33':'OPEN'}
    with (B/('one_helper_%02d.json'%number)).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
