"""Source identity reuse for eleven nodes and exact anchor-contraction sets."""
from functools import lru_cache
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def isnode(v):return isinstance(v,tuple)
def known(t):return [] if not isnode(t) else known(t[1])+[t[0]]+known(t[2])
def normalize(t,rank=None):
    rank=rank or {v:i+1 for i,v in enumerate(known(t))}
    def walk(v,hi):return 'F'+str(hi) if not isnode(v) else (rank[v[0]],walk(v[1],rank[v[0]]-1),walk(v[2],hi))
    return walk(t,len(rank))
def scale(t):return t if not isnode(t) else (2*t[0],scale(t[1]),scale(t[2]))
def path(t,x):
    p=[]
    while t[0]!=x:p.append(t[0]);t=t[1 if x<t[0] else 2]
    return p
class Lift:
    def __init__(self,z):
        self.Z=z;self.T=list(map(fr,z['trees']));self.idx={t:i for i,t in enumerate(self.T)};self.calls=0
    def access(self,t,x):
        # Some leaf differs from x for every H<=2 eleven-node action.
        leaf=next(v for v in known(t) if v!=x and not isnode(self.sub(t,v)[1]) and not isnode(self.sub(t,v)[2]));keys=[k for k in known(t) if k!=leaf];rank={k:j+1 for j,k in enumerate(keys)};payload={}
        def compress(v,hi):
            if not isnode(v) or v[0]==leaf:payload[hi]=v;return 'F'+str(hi)
            r=rank[v[0]];return r,compress(v[1],r-1),compress(v[2],hi)
        reduced=compress(t,10);s=self.idx[reduced];xr=rank[x];dest=self.Z['destination'][s][xr-1]
        def expand(v):return payload[int(v[1:])] if not isnode(v) else (keys[v[0]-1],expand(v[1]),expand(v[2]))
        self.calls+=1;return expand(self.T[dest]),self.Z['H'][s][xr-1]
    @staticmethod
    def sub(t,x):
        while t[0]!=x:t=t[1 if x<t[0] else 2]
        return t
@lru_cache(maxsize=20000)
def merges(L,R):
    if not isnode(L):return (R,)
    if not isnode(R):return (L,)
    return tuple(dict.fromkeys([(L[0],L[1],v) for v in merges(L[2],R)]+[(R[0],v,R[2]) for v in merges(L,R[1])]))
def projections(t,z):
    def walk(v):
        if not isnode(v):return (v,)
        if v[0]==z:return merges(v[1],v[2])
        return tuple((v[0],l,r) for l in walk(v[1]) for r in walk(v[2]))
    return tuple(dict.fromkeys(normalize(v,{k:k//2 for k in known(v)}) for v in walk(t)))
