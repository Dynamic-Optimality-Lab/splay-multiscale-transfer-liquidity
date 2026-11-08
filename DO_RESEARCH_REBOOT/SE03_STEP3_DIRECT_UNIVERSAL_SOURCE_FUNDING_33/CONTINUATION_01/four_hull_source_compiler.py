"""Construct original splay words via rooted four-node hull identities.
Restricted raw rotations are a planning device, NEVER charged source operations.
"""
import collections,itertools
from functools import lru_cache
from interior_projection_source_tools import isnode,known,path,normalize
from audit_verify35 import rotate
@lru_cache(None)
def shapes(lo,hi):
    if lo>hi:return ('F'+str(hi),)
    return tuple((r,L,R) for r in range(lo,hi+1) for L in shapes(lo,r-1) for R in shapes(r+1,hi))
def raw(t,x):
    p=[];v=t
    while v[0]!=x:p.append(1 if x<v[0] else 2);v=v[p[-1]]
    assert 1<=len(p)<=2
    parent=t
    for k in p[:-1]:parent=parent[k]
    return rotate(t,p),parent[0]
def flat(t):
    plan=[]
    def use(k):
        nonlocal t
        t,p=raw(t,k);plan.append((p,k))
    while isnode(t[1]):use(t[1][0])
    while isnode(t[2]):
        while isnode(t[2][1]):use(t[2][1][0])
        use(t[2][0])
    return t,plan
class HullCompiler:
    def __init__(self,trace):
        self.T=shapes(1,4);self.idx={t:i for i,t in enumerate(self.T)};self.dest=[];self.H=[]
        for t in self.T:
            row=[];hr=[]
            for x in range(1,5):a,p,e=trace(t,x);row.append(self.idx[a]);hr.append(len(e))
            self.dest.append(row);self.H.append(hr)
        self.words={}
        for s in range(14):
            reached={s:[]};q=collections.deque([s])
            while q:
                u=q.popleft()
                for x,v in enumerate(self.dest[u],1):
                    if v not in reached:reached[v]=reached[u]+[x];q.append(v)
            assert len(reached)==14
            for v,w in reached.items():self.words[s,v]=w
        self.instantiations=0
    def compile(self,source,target):
        st,forward=flat(source);tt,back=flat(target);assert st==tt;plan=[p for g,p in forward]+[g for g,p in back[::-1]];t=source;rows=[]
        for pivot in plan:
            goal,_=raw(t,pivot);include=set();v=t
            while True:
                include.add(v[0])
                if v[0]==pivot:break
                v=v[1 if pivot<v[0] else 2]
            while len(include)<4:
                frontier=[]
                def inspect(v):
                    if not isnode(v) or v[0] not in include:return
                    for child in v[1:]:
                        if isnode(child):
                            if child[0] not in include:frontier.append(child[0])
                            else:inspect(child)
                inspect(t);assert frontier;include.add(min(frontier))
            keys=sorted(include);ranks={v:i+1 for i,v in enumerate(keys)};payload={}
            def compress(v,hi,store):
                if not isnode(v) or v[0] not in include:
                    if store:payload[hi]=v
                    else:assert payload[hi]==v
                    return 'F'+str(hi)
                r=ranks[v[0]];return r,compress(v[1],r-1,store),compress(v[2],hi,store)
            s=self.idx[compress(t,4,True)];g=self.idx[compress(goal,4,False)]
            def expand(v):return payload[int(v[1:])] if not isnode(v) else (keys[v[0]-1],expand(v[1]),expand(v[2]))
            for x in self.words[s,g]:
                ns=self.dest[s][x-1];after=expand(self.T[ns]);rows.append({'key':keys[x-1],'before':t,'after':after,'H':self.H[s][x-1],'hull_keys':keys,'G4_before':s,'G4_after':ns,'G4_key':x});t=after;s=ns;self.instantiations+=1
            assert t==goal
        assert t==target;return rows
