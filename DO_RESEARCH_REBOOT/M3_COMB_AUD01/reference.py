"""Independent mathematical tree operations; no campaign-generator imports."""
from functools import lru_cache
LEAF=None

def depth(t,x):
    d=0
    while t is not None and t[0]!=x:t=t[1] if x<t[0] else t[2];d+=1
    if t is None:raise KeyError(x)
    return d

def rotate_right(t):
    x,l,r=t;y,a,b=l
    return (y,a,(x,b,r))

def rotate_left(t):
    x,l,r=t;y,a,b=r
    return (y,(x,l,a),b)

def access(t,x):
    """Recursive bottom-up splay, with zigzig parent-first and zigzag child-first."""
    k,l,r=t
    if x==k:return t
    if x<k:
        assert l is not None
        if x<l[0]:
            l=(l[0],access(l[1],x),l[2]);t=rotate_right((k,l,r))
        elif x>l[0]:
            l=(l[0],l[1],access(l[2],x));t=(k,rotate_left(l),r)
        return rotate_right(t)
    assert r is not None
    if x>r[0]:
        r=(r[0],r[1],access(r[2],x));t=rotate_left((k,l,r))
    elif x<r[0]:
        r=(r[0],access(r[1],x),r[2]);t=(k,l,rotate_right(r))
    return rotate_left(t)

def insert(t,x):
    if t is None:return (x,None,None)
    k,l,r=t
    if x==k:return t
    return (k,insert(l,x),r) if x<k else (k,l,insert(r,x))

def tree(serial):return None if serial is None else (serial[0],tree(serial[1]),tree(serial[2]))
def serial(t):return None if t is None else [t[0],serial(t[1]),serial(t[2])]
def mirror(t):return None if t is None else (8-t[0],mirror(t[2]),mirror(t[1]))

@lru_cache(None)
def all_bsts(keys):
    if not keys:return (None,)
    return tuple((x,l,r) for i,x in enumerate(keys)
                 for l in all_bsts(keys[:i]) for r in all_bsts(keys[i+1:]))

def iscore(x):return x%16==0 and 0<=x<=128

def collapse(t):
    if t is None:return None
    k,l,r=t;l=collapse(l);r=collapse(r)
    return (k,l,r) if iscore(k) or l is not None or r is not None else None

def every_anonymous_has_core(t):
    if t is None:return True,False
    ok1,c1=every_anonymous_has_core(t[1]);ok2,c2=every_anonymous_has_core(t[2])
    has=iscore(t[0]) or c1 or c2
    return ok1 and ok2 and has,has

def shadow(t):
    def at(path):
        n=t
        for s in path:
            if n is None:return (1,0,0)
            n=n[1+s]
        if n is None:return (1,0,0)
        return (0,1,n[0]//16) if iscore(n[0]) else (0,0,0)
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))

def visible(t):
    q=[(t,0)]
    while q:
        n,d=q.pop()
        if n is None:continue
        if d in (1,2):yield n[0],d
        if d<2:q.extend(((n[1],d+1),(n[2],d+1)))
