"""Backward symbolic ordered-tree languages, with exact recent-six histories.

Safety requires closure and an independently checked lifting theorem. A bound
or a projected intersection is never a universal proof or a source witness.
"""
import collections,functools,itertools,json,sys,time
from fractions import Fraction as F
from pathlib import Path
import audit_tailrefine as tr
g=tr.g;c=g.c;B=Path(__file__).resolve().parent
started=time.process_time();CAP=min(55,float(sys.argv[1])-4)
stats=collections.Counter();MAXREC=12000
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>800000 or stats['proposals']>250000:raise c.Bound()
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def canon(t,with_map=False):
    keys=g.vars_of(t);groups=collections.defaultdict(list)
    for k in keys:
        if k.denominator!=1:groups[int(k)].append(k)
    mp={F(0):F(0),F(12):F(12)}
    for k in range(1,12):mp[F(k)]=F(k)
    for lo,vs in groups.items():
        for j,k in enumerate(sorted(vs),1):mp[k]=F(lo)+F(j,len(vs)+1)
    def go(v):
        if isinstance(v,g.Hole):return g.Hole(mp[v.lo],mp[v.hi])
        return (mp[v[0]],go(v[1]),go(v[2]))
    z=go(t)
    return (z,mp) if with_map else z
def fit_hole(v,lo,hi):
    if isinstance(v,g.Hole):return lo<=v.lo<v.hi<=hi
    return lo<v[0]<hi and fit_hole(v[1],lo,hi) and fit_hole(v[2],lo,hi)
def covers(p,q):
    mp={F(k):F(k) for k in range(13)}
    def go(a,b):
        if isinstance(a,g.Hole):return fit_hole(b,mp[a.lo],mp[a.hi])
        if isinstance(b,g.Hole):return False
        ka,kb=a[0],b[0]
        if ka.denominator==1:
            if ka!=kb:return False
        else:
            if kb.denominator==1 or int(ka)!=int(kb):return False
            if any((ka<z)!=(kb<v) for z,v in mp.items()):return False
            mp[ka]=kb
        return go(a[1],b[1]) and go(a[2],b[2])
    return go(p,q)
def replace(t,p,u):return g.expand_at(t,p,u)
def at(t,p):
    for ch in p:
        if isinstance(t,g.Hole):return None
        t=t[1 if ch=='L' else 2]
    return t
def choices(t,h):
    keys=sorted(set(g.vars_of(t)+[F(i) for i in range(1,12)]+[h.lo,h.hi]))
    return [v for v in keys if h.lo<v<h.hi]+[(a+b)/2 for a,b in zip(keys,keys[1:]) if h.lo<=a<b<=h.hi]
def expose(t,p,k=None):
    """Instantiate the node at an output-frame position; no hidden depth cut."""
    u=at(t,p)
    if u is None:return []
    if not isinstance(u,g.Hole):return [t] if k is None or u[0]==k else []
    opts=choices(t,u) if k is None else [k] if u.lo<k<u.hi else []
    return [replace(t,p,g.node(v,u.lo,u.hi)) for v in opts]
def inv_event(t,oldroot=None,double=None):
    x=t[0];result=[]
    specs=[]
    if double is not True:specs += [('L','R',None),('R','L',None)]
    if double is not False:specs += [('LL','RR','R'),('RR','LL','L'),('LR','R','L'),('RL','L','R')]
    for w,gpos,ppos in specs:
        current=[t]
        # Parent position precedes grandparent when nested in output.
        if ppos is not None:current=[v for z in current for v in expose(z,ppos)]
        current=[v for z in current for v in expose(z,gpos,oldroot)]
        for z in current:
            l,r=z[1:]
            if w=='L':gg,A,D=r;before=(gg,(x,l,A),D)
            elif w=='R':gg,A,D=l;before=(gg,A,(x,D,r))
            elif w=='LL':pp,A,R=r;gg,C,D=R;before=(gg,(pp,(x,l,A),C),D)
            elif w=='RR':pp,L,C=l;gg,A,Z=L;before=(gg,A,(pp,Z,(x,C,r)))
            elif w=='LR':pp,A,Z=l;gg,C,D=r;before=(gg,(pp,A,(x,Z,C)),D)
            else:gg,A,Z=l;pp,C,D=r;before=(gg,A,(pp,(x,Z,C),D))
            z2,h,_,_=c.move(before,x)
            assert z2==z and h==1
            result.append((before,z,w))
    return result
@functools.lru_cache(maxsize=15000)
def pre(t,oldroot,H):
    guard();result=[];x=t[0]
    if H==1:
        result=[(u,[('K',x)]) for u,z,w in inv_event(t,oldroot)]
    else:
        # One original access at depth3/4: reverse its last root event,
        # then its initial double in the actual target subtree.
        for mid,z,w in inv_event(t,oldroot):
            from source_model import path
            loc=path(mid,x)
            for oldv,refined,ww in inv_event(at(mid,loc),None,True):
                u=replace(mid,loc,oldv)
                # refined target hole instantiations must also refine endpoint.
                endpoint,Hh,_,_=c.move(u,x)
                assert Hh==2 and covers(t,endpoint)
                result.append((u,[('K',x)]))
        # Two one-event original accesses; the helper is any Score or any
        # private order cell, including equal-gap anonymous alternatives.
        outer=g.Hole(F(0),F(12))
        for y in choices(t,outer):
            if y==x or y==oldroot:continue
            for mid,z,w in inv_event(t,y):
                for u,zz,ww in inv_event(mid,oldroot):
                    end=c.move(c.move(u,y)[0],x)[0]
                    assert covers(t,end)
                    result.append((u,[('D',y),('K',x)]))
    result2=[]
    for u,w in result:
        uu,mp=canon(u,True)
        result2.append((uu,tuple((mode,mp[k]) for mode,k in w)))
    return tuple(result2)
def parentmap(t):
    result={}
    def walk(v,p):
        if not isinstance(v,tuple):return
        k=v[0]
        if k in c.MM:result[k]=p;p=k
        walk(v[1],p);walk(v[2],p)
    walk(t,None);return result
def heap(t,r):
    pos={k:i for i,k in enumerate(r)}
    return all(p is None or pos[p]<pos[k] for k,p in parentmap(t).items())
def rinv(r,x,oldroot):
    if r[0]!=x or r[1]!=oldroot:return []
    base=list(r[1:]);return [tuple(base[:i]+[x]+base[i:]) for i in range(1,6)]
def main():
    # Use EVERY symbolic density context, including transient/unrealizable
    # contexts. No reachability or SCC completeness premise is needed.
    states=[t for t in g.BF(1,11) if t[0] in c.MM]
    idx={t:i for i,t in enumerate(states)};inc=collections.defaultdict(list)
    for t in states:
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n is None or n[0] not in idx:continue
            z,q=n;inc[z].append((t,x,q))
    assert len(states)==2394
    seeds=json.loads((B/'sourceclosure.json').read_text())['remaining_compatible_tails']
    records=[];groups=collections.defaultdict(list);todo=collections.deque();goal=None;closed=False;stopped=None
    def insert(a,b,r,budget,parent,word,origin):
        nonlocal goal
        guard();a=canon(a);key=(b,r,budget)
        if any(covers(records[i]['A'],a) for i in groups[key]):stats['subsumed']+=1;return
        n=len(records);records.append({'A':a,'BF':b,'recent':r,'budget':budget,'parent':parent,'word':word,'origin':origin})
        groups[key].append(n);todo.append(n);stats['records']=len(records)
        if len(records)>=MAXREC:raise c.Bound()
    for si,s in enumerate(seeds):
        word=s['word'];initial,final=tr.starts(word);b=freeze(s['previous_BF']);spent=2-s['previous_Q']
        assert b in idx and inc[b], 'seed and predecessor gap vocabulary must agree'
        assert spent in (0,1)
        for r in itertools.permutations(c.M):
            if r[0]!=b[0] or not heap(b,r):continue
            rr=r
            for x in word[1:-1]:rr=c.recent(rr,x)
            if rr[-1]!=word[-1]:continue
            for a in initial:insert(a,b,r,1-spent,None,tuple(('K',x) for x in word[1:-1]),si)
    try:
        while todo:
            guard();i=todo.popleft();s=records[i];a,b,r,budget=s['A'],s['BF'],s['recent'],s['budget']
            for old,x,q in inc[b]:
                # Actual cold singleton NEG2 target intersection.
                if q==4:
                    rr=tuple(r[1:])+(x,)
                    if r[0]==x and r[1]==old[0] and heap(old,rr):
                        ps=pre(a,F(old[0]),1)
                        if ps:goal={'record':i,'negative_source_BF':old,'negative_before_recent':rr,
                            'negative_word':ps[0][1],'negative_source_A_pattern':ps[0][0],'kind':'NEG2-S'};break
                if q in (1,2,3,4):
                    H=1 if q<=2 else 2;w=2*H-q
                    if w<=budget:
                        for rr in rinv(r,x,old[0]):
                            if not heap(old,rr):continue
                            for pa,word in pre(a,F(old[0]),H):
                                stats['proposals']+=1;insert(pa,old,rr,budget-w,i,word,s['origin'])
                if q==1:
                    for older,y,q0 in inc[old]:
                        if q0!=5:continue
                        for rm in rinv(r,x,y):
                            if not heap(old,rm):continue
                            for rr in rinv(rm,y,older[0]):
                                if not heap(older,rr):continue
                                if rr[-1]==y:
                                    for amid,w2 in pre(a,F(old[0]),1):
                                        for pa,w1 in pre(amid,F(older[0]),1):
                                            goal={'record':i,'negative_source_BF':older,'negative_before_recent':rr,
                                                'negative_word':w1+w2,'negative_source_A_pattern':pa,'kind':'NEG2-P'};break
                                        if goal:break
                                if goal:break
                                for h1,h2 in ((1,2),(2,1)):
                                    for amid,w2 in pre(a,F(old[0]),h2):
                                        for pa,w1 in pre(amid,F(older[0]),h1):
                                            stats['proposals']+=1;insert(pa,older,rr,budget,i,w1+w2,s['origin'])
                            if goal:break
                        if goal:break
                if goal:break
            if goal:break
        closed=not todo and goal is None
    except c.Bound:stopped='PREDECLARED_SYMBOLIC_BOUND'
    def serial(v):
        if isinstance(v,g.Hole):return {'gap':[str(v.lo),str(v.hi)]}
        if isinstance(v,F):return str(v)
        if isinstance(v,dict):return {k:serial(q) for k,q in v.items()}
        if isinstance(v,(tuple,list)):return [serial(q) for q in v]
        return v
    result={'status':'ABSTRACT_NEGATIVE_TARGET_INTERSECTION' if goal else 'SYMBOLIC_BACKWARD_CLOSED' if closed else 'SYMBOLIC_BOUND',
        'goal':serial(goal),'records':serial(records),'queue':list(todo),'closed':closed,'stop':stopped,
        'statistics':dict(stats),'source_engine_calls':c.account['source_engine_calls'],'CPU':time.process_time()-started,
        'new_finite_tests':0,'proof_status':'requires independent completeness/closure audit; abstract goal requires source realization'}
    out('saturation3.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('records','goal','queue')}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_saturation3_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
