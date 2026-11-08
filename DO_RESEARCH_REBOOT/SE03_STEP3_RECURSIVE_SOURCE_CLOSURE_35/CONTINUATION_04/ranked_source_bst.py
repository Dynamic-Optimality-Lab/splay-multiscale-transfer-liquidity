"""Lossless Catalan ranks and accepted off-path-leaf source substitutions.

This changes source representation only. No two distinct full trees
have one rank. Source costs are inherited only through the proved
non-target-leaf identity, never by erasing an active ancestor.
"""
import functools
C=[1]
for n in range(1,14):C.append(sum(C[i]*C[n-1-i] for i in range(n)))
OFF={}
for n in range(1,14):
    a=[0]
    for i in range(n):a.append(a[-1]+C[i]*C[n-1-i])
    OFF[n]=a
@functools.lru_cache(maxsize=18000)
def unrank(n,lo,r):
    if n==0:assert r==0;return None
    assert 0<=r<C[n]
    i=next(i for i in range(n) if r<OFF[n][i+1]);r-=OFF[n][i];q=C[n-1-i]
    return (lo+i,unrank(i,lo,r//q),unrank(n-1-i,lo+i+1,r%q))
@functools.lru_cache(maxsize=18000)
def rank_tree(t,lo,n):
    if n==0:assert t is None;return 0
    k,l,r=t;i=k-lo;assert 0<=i<n
    return OFF[n][i]+rank_tree(l,lo,i)*C[n-1-i]+rank_tree(r,k+1,n-1-i)
def first_other_leaf(t,x):
    if t[1] is None and t[2] is None:return t[0] if t[0]!=x else None
    return (first_other_leaf(t[1],x) if t[1] else None) or (first_other_leaf(t[2],x) if t[2] else None)
@functools.lru_cache(maxsize=16000)
def remove_leaf(t,y):
    if t is None:return None
    if t[0]==y:assert t[1] is None and t[2] is None;return None
    return (t[0]-(t[0]>y),remove_leaf(t[1],y),remove_leaf(t[2],y))
@functools.lru_cache(maxsize=16000)
def raise_tree(t,y):
    if t is None:return None
    return (t[0]+(t[0]>=y),raise_tree(t[1],y),raise_tree(t[2],y))
def insert_leaf(t,y):
    if t is None:return (y,None,None)
    return (t[0],insert_leaf(t[1],y),t[2]) if y<t[0] else (t[0],t[1],insert_leaf(t[2],y))
class Lift:
    def __init__(self,old,fresh=None):
        self.old=old;self.index={t:i for i,t in enumerate(old['trees'])};self.fresh=fresh;self.substitutions=0
        self.action=functools.lru_cache(maxsize=22000)(self._action)
    def _action(self,t,n,x):
        if n==11:
            a=self.index[t];j=x-1
            return self.old['trees'][int(self.old['destination'][a,j])],int(self.old['H'][a,j]),int(self.old['Q'][a,j])
        y=first_other_leaf(t,x)
        if y is None:
            assert self.fresh is not None
            return self.fresh(t,n,x)
        u=remove_leaf(t,y);xx=x-(x>y);z,h,q=self.action(u,n-1,xx);self.substitutions+=1
        return insert_leaf(raise_tree(z,y),y),h,q
    def clear(self):
        self.action.cache_clear();unrank.cache_clear();rank_tree.cache_clear();remove_leaf.cache_clear();raise_tree.cache_clear()
def near(t):
    out=[]
    for c in t[1:]:
        if c:
            out.append(c[0]);out.extend(d[0] for d in c[1:] if d)
    return out
def depth_at_most(t,x,limit):
    for d in range(limit+1):
        if t[0]==x:return d
        t=t[1] if x<t[0] else t[2]
        if t is None:return None
    return None
