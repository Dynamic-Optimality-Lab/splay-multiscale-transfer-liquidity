"""Backward ZERO closure for Campaign09's NEW paired-destination final +1 seeds.
The generic inverse calculus is inherited; no old terminal frames are used.
"""
import collections,functools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
from audit_seeds import s,g,c,tr,serial
B=Path(__file__).resolve().parent;started=time.process_time();CAP=min(45,float(sys.argv[1])-4)
stats=collections.Counter();MAXREC=80000
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>=900000 or stats['predecessor_proposals']>=500000:raise c.Bound()
s.guard=guard;c.limit=guard
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def readA(t):
    if isinstance(t,dict):return g.Hole(F(t['gap'][0]),F(t['gap'][1]))
    return (F(t[0]),readA(t[1]),readA(t[2]))
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def main():
    states=[t for t in g.BF(1,11) if t[0] in c.MM];SS=set(states);inc=collections.defaultdict(list)
    for b in states:
        for x in c.M:
            if x==b[0]:continue
            n=c.bm(b,x)
            if n:assert n[0] in SS;inc[n[0]].append((b,x,n[1]))
    seeds=json.loads((B/'terminal_seeds.json').read_text())
    records=[];groups=collections.defaultdict(list);todo=collections.deque();goal=None;bound=None
    def insert(a,b,r,parent,word,origin):
        guard();a=s.canon(a);key=(b,r)
        for i in groups[key]:
            if s.covers(records[i]['A'],a):stats['covered_proposals']+=1;return i
        i=len(records);records.append({'A':a,'BF':b,'recent':r,'parent':parent,'word':word,'origin_seed_group':origin})
        groups[key].append(i);todo.append(i);stats['records']=len(records)
        if len(records)>=MAXREC:raise c.Bound()
        return i
    for origin,seed in enumerate(seeds['groups']):
        a=readA(seed['A']);b=freeze(seed['BF']);assert b in SS and inc[b]
        for r in seed['recent']:insert(a,b,tuple(r),None,(),origin)
    seed_records=len(records)
    try:
        while todo:
            guard();i=todo.popleft();v=records[i];a,b,r=v['A'],v['BF'],v['recent'];ll=c.leaves(b)
            if ll==4:
                stats['L4_records_examined']+=1
                # Do not identify an arbitrary L4 frame with a cold NEG2 target.
                for old,x,q in inc[b]:
                    if q==4 and r[0]==x and r[1]==old[0]:
                        rr=tuple(r[1:])+(x,)
                        if s.heap(old,rr):
                            for pa,ww in s.pre(a,F(old[0]),1):
                                goal={'kind':'NEG2-S','record':i,'negative_before_BF':old,'negative_before_recent':rr,
                                    'negative_before_A':pa,'negative_word':ww};break
                    if q==1:
                        for older,y,q0 in inc[old]:
                            if q0!=5:continue
                            for rm in s.rinv(r,x,y):
                                if not s.heap(old,rm):continue
                                for rr in s.rinv(rm,y,older[0]):
                                    if rr[-1]!=y or not s.heap(older,rr):continue
                                    for amid,w2 in s.pre(a,F(old[0]),1):
                                        for pa,w1 in s.pre(amid,F(older[0]),1):
                                            goal={'kind':'NEG2-P','record':i,'negative_before_BF':older,'negative_before_recent':rr,
                                                'negative_before_A':pa,'negative_word':w1+w2};break
                                        if goal:break
                                    if goal:break
                                if goal:break
                            if goal:break
                    if goal:break
                if goal:break
            for old,x,q in inc[b]:
                if q in (2,4):
                    H=q//2
                    for rr in s.rinv(r,x,old[0]):
                        if not s.heap(old,rr):continue
                        for pa,word in s.pre(a,F(old[0]),H):
                            stats['predecessor_proposals']+=1
                            insert(pa,old,rr,i,word,v['origin_seed_group'])
                if q==1:
                    # ALL actual q5/q1 successor labels; paired H3/Q6 zeros.
                    for older,y,q0 in inc[old]:
                        if q0!=5:continue
                        for rm in s.rinv(r,x,y):
                            if not s.heap(old,rm):continue
                            for rr in s.rinv(rm,y,older[0]):
                                if not s.heap(older,rr):continue
                                for h1,h2 in ((1,2),(2,1)):
                                    for amid,w2 in s.pre(a,F(old[0]),h2):
                                        for pa,w1 in s.pre(amid,F(older[0]),h1):
                                            stats['predecessor_proposals']+=1
                                            insert(pa,older,rr,i,w1+w2,v['origin_seed_group'])
    except c.Bound:bound='PREDECLARED_SYMBOLIC_BOUND'
    leaves=collections.Counter(c.leaves(v['BF']) for v in records)
    closed=not todo and goal is None and bound is None
    result={'status':'ABSTRACT_NEG2_INTERSECTION' if goal else 'COMPLETE_SYMBOLIC_ZERO_CLOSURE' if closed else 'BOUNDED_INTERNAL_CHECKPOINT',
        'closed':closed,'goal':serial(goal),'records':serial(records),'queue':list(todo),'bound':bound,
        'initial_seed_records_after_coverage':seed_records,'leaf_distribution':dict(leaves),'statistics':dict(stats),
        'source_engine_calls':c.account['source_engine_calls'],'new_finite_tests':0,'CPU':time.process_time()-started,
        'status_limit':'abstract intersection requires genuine source realization; closure requires independent lifting/coverage audit'}
    out('zero_closure.json',result)
    print(json.dumps({k:v for k,v in result.items() if k not in ('records','queue','goal')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_closure_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
