"""New audit-only parent-map splay and observation implementation."""
from functools import lru_cache
PORT=None
GHOST='alias'
PATHS=((0,),(1,),(0,0),(0,1),(1,0),(1,1))
SHADOW=((),(0,),(1,),(0,0),(0,1),(1,0),(1,1))
def real(n):return isinstance(n,tuple)
def frozen(n):return tuple(frozen(x) for x in n) if isinstance(n,list) else n
def tree(n):
    if n=='G':return GHOST
    if n is None:return None
    return (n[0],tree(n[1]),tree(n[2]))
def splay(t,target):
    children={};up={}
    def load(n,p=None):
        if not real(n):return n
        k,l,r=n;up[k]=p;children[k]=[load(l,k),load(r,k)];return k
    root=load(t);assert target in children
    def rotate(k):
        nonlocal root
        p=up[k];g=up[p];right=children[p][1]==k;side=int(right);middle=children[k][1-side]
        children[p][side]=middle
        if middle in children:up[middle]=p
        children[k][1-side]=p;up[p]=k;up[k]=g
        if g is None:root=k
        else:children[g][int(children[g][1]==p)]=k
    while up[target] is not None:
        p=up[target];g=up[p]
        if g is None:rotate(target)
        elif (children[g][1]==p)==(children[p][1]==target):rotate(p);rotate(target)
        else:rotate(target);rotate(target)
    def output(k):return (k,output(children[k][0]),output(children[k][1])) if k in children else k
    return output(root)
def at(t,path):
    for s in path:
        assert real(t);t=t[s+1]
    return t
def find(t,key):
    if not real(t):return None
    if t[0]==key:return t
    return find(t[1],key) or find(t[2],key)
def observations(t,slot0):
    owner=find(t,slot0);assert owner is not None
    out=[]
    for p in SHADOW:
        n=t
        for s in p:
            if n is None:break
            if n==GHOST:n=owner
            n=n[1+s]
        if n is None:out.append((1,0,0))
        else:
            if n==GHOST:n=owner
            k=n[0];out.append((0,1,k//16) if k>=0 and k%16==0 else (0,0,0))
    return tuple(out)
def raw_normalize(a):
    out=[]
    for i,(kind,iss,label) in enumerate(a):
        if i and kind!=0:out.append((1,0,0))
        else:out.append((0,int(iss),label if iss else 0))
    for p,children in ((1,(3,4)),(2,(5,6))):
        if out[p][0]:
            for c in children:out[c]=(1,0,0)
    return tuple(out)
def universe(depth=7,p=()):return None if len(p)>depth else (p,universe(depth,p+(0,)),universe(depth,p+(1,)))
def spec(word):
    t=universe();need=set();labeltypes={():None}
    for j,p in enumerate(word):
        for i in range(len(p)+1):need.add(at(t,p[:i])[0])
        k=at(t,p)[0];labeltypes[k]=(-8 if j<len(word)-1 else None);t=splay(t,k)
    observed=set(SHADOW)|{at(t,p)[0] for p in SHADOW}
    owner=find(t,());observed.update(n[0] for n in owner[1:] if real(n));observed|=need
    for p in tuple(observed):observed.update(p[:i] for i in range(len(p)))
    return observed,need,labeltypes
def prefixes(word):
    observed,need,types=spec(word);keys=(-8,0,8,16,32,48,64,80,96,112,128)
    def rec(address,values):
        if address not in observed:
            yield None;return
        if address not in need:
            yield None
            if not any(x>=0 and x%16==0 for x in values):yield GHOST
        for i,k in enumerate(values):
            if address in types:
                typ=types[address]
                if typ is None and (k<0 or k%16):continue
                if typ is not None and k!=typ:continue
            for l in rec(address+(0,),values[:i]):
                for r in rec(address+(1,),values[i+1:]):yield (k,l,r)
    return rec((),keys)
@lru_cache(None)
def bsts(keys):
    if not keys:return (None,)
    return tuple((x,l,r) for i,x in enumerate(keys) for l in bsts(keys[:i]) for r in bsts(keys[i+1:]))
def depth(t,x):
    n=0
    while t[0]!=x:t=t[1] if x<t[0] else t[2];n+=1
    return n
def insert(t,x):
    if t is None:return (x,None,None)
    k,l,r=t
    return (k,insert(l,x),r) if x<k else (k,l,insert(r,x))
def without_fringe(t):
    if t is None:return None
    k,l,r=t
    if k==-1:assert l is None and r is None;return None
    return (k,without_fringe(l),without_fringe(r))
def core_view(b):
    seen=set()
    def visit(k):
        assert k in range(9) and k not in seen;seen.add(k);children=[]
        for kind,ref in (('kl','rl'),('kr','rr')):
            c=b[ref][k];children.append(visit(c) if b[kind][k]==0 and c<9 else None)
        return (k,*children)
    t=visit(b['root']);assert len(seen)==9;return t
