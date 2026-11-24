"""Actual present-key splay words implementing a linear-size exact reset."""
from stage5 import *
from collections import deque
from functools import lru_cache
sys.path.insert(0,str(REPO/'python'))
from independent import splay as ind
Tree=inherited.Tree
L=ind.LEAF

def from_tuple(t):
    assert t!=L
    ch={}; todo=[t]
    while todo:
        _,k,l,r=todo.pop()
        ch[str(k)]=[l[1] if l!=L else None,r[1] if r!=L else None]
        if l!=L:todo.append(l)
        if r!=L:todo.append(r)
    return {'root':t[1],'children':ch}

def as_tuple(s,rank=None):
    if rank is None:rank={int(k):int(k) for k in s['children']}
    out={None:L};todo=[(s['root'],False)]
    while todo:
        k,done=todo.pop()
        l,r=s['children'][str(k)]
        if done:out[k]=ind.node(rank[k],out[l],out[r])
        else:
            todo.append((k,True))
            if l is not None:todo.append((l,False))
            if r is not None:todo.append((r,False))
    return out[s['root']]

@lru_cache(None)
def shapes(lo,hi):
    if lo>hi:return (L,)
    return tuple(ind.node(k,l,r) for k in range(lo,hi+1)
                 for l in shapes(lo,k-1) for r in shapes(k+1,hi))

def hull_table():
    universe=set(shapes(1,4));assert len(universe)==14
    table={}
    for t in universe:
        paths={t:()};queue=deque([t])
        while queue:
            q=queue.popleft()
            for x in range(1,5):
                z,ev=ind.trace(q,x)
                assert z in universe and len(ev)<=2
                if z not in paths:paths[z]=paths[q]+(x,);queue.append(z)
        assert len(paths)==14
        for z,w in paths.items():
            # Independent mutable pointer replay on all 196 entries.
            a=Tree(from_tuple(t))
            for x in w:inherited.Replay.plain_splay(a,x)
            assert a.state()==from_tuple(z)
            table[t,z]=w
    assert max(map(len,table.values()))<=13
    return table

TABLE=None
def flatten(st):
    a=Tree(st);rotations=[]
    def rot(u,side):
        v=a.ch[u][side];assert v is not None
        rotations.append((u,side,v));a.rotate(u,side)
    while a.ch[a.root][0] is not None:rot(a.root,0)
    while a.ch[a.root][1] is not None:
        r=a.ch[a.root][1]
        while a.ch[r][0] is not None:
            rot(r,0);r=a.ch[a.root][1]
        rot(a.root,1)
    assert a.root==max(a.keys)
    assert all(a.ch[k]==[a.keys[i-1] if i else None,None] for i,k in enumerate(a.keys))
    assert len(rotations)<=3*(len(a.keys)-1)
    return rotations

def projection(a,J):
    ks=sorted(J);rank={k:i+1 for i,k in enumerate(ks)}
    return as_tuple({'root':a.root,'children':{str(k):[c if c in J else None for c in a.ch[k]]
                    for k in ks}},rank)

def coerce(start,finish):
    global TABLE
    if TABLE is None:TABLE=hull_table()
    assert set(start['children'])==set(finish['children']) and len(start['children'])>=4
    if start==finish:return [],{'macros':0,'StepEv':0}
    todo=[(u,s) for u,s,v in flatten(start)]
    todo += [(v,1-s) for u,s,v in reversed(flatten(finish))]
    a=Tree(start);word=[];A=0
    for u,side in todo:
        v=a.ch[u][side];J=set(a.path(v));assert len(J)<=3
        while len(J)<4:
            J.add(min(c for k in J for c in a.ch[k] if c is not None and c not in J))
        before=projection(a,J)
        want=Tree(a.state());want.rotate(u,side);after=projection(want,J)
        ks=sorted(J)
        for i in TABLE[before,after]:
            x=ks[i-1];path=a.path(x);assert set(path)<=J
            A+=len(path)//2;inherited.Replay.plain_splay(a,x);word.append(x)
        assert a.state()==want.state()
    assert a.state()==finish and A<=156*(len(a.keys)-1)
    return word,{'macros':len(todo),'StepEv':A}

def advance(st,xs):
    t=as_tuple(st);A=0
    for x in xs:
        t,ev=ind.trace(t,x);A+=len(ev)
    return from_tuple(t),A

def finish_pair(a,b,initial_a,initial_b,visit_all=True):
    sync,c0=coerce(a,b)
    n=len(b['children']);scan=sorted(map(int,b['children'])) if visit_all else []
    if scan:scan.append(scan[0])  # ensure the least key is also a genuine KEEP
    t,cscan=advance(b,scan)
    ret,c1=coerce(t,initial_b)
    repair,c2=coerce(initial_b,initial_a)
    return ([['D',x] for x in sync]+[['K',x] for x in scan+ret]+[['D',x] for x in repair],
            {'sync_A':c0,'all_KEEP_scan_StepEv':cscan,'paired_return':c1,'final_A_repair':c2,
             'phase_lengths':[len(sync),len(scan),len(ret),len(repair)],'physical_population':n})
