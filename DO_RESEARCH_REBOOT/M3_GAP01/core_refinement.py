"""Population-opaque core completion for signatures supported in gap0 only."""
import sys
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
PORT=('leaf','population_opaque')

def has_core(t):
    if t[0]=='leaf':return False
    return t[1]>=0 or has_core(t[2]) or has_core(t[3])
def collapse(t):
    if not has_core(t):return PORT
    return S.node(t[1],collapse(t[2]),collapse(t[3]))
def shadow(t):
    def at(path):
        z=t
        for side in path:
            if z[0]=='leaf':return (1,0,0)
            z=z[2+side]
        if z[0]=='leaf':return (1,0,0)
        return (0,int(z[1]>=0),max(z[1],0))
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def representative(alpha):
    a=tuple(tuple(r) for r in alpha)
    if len(a)!=7 or not a[0][1] or a[0][2] not in range(9):raise ValueError('root')
    a=((0,1,a[0][2]),)+a[1:]
    def balanced(keys):return collapse(S.balanced(keys))
    def sub(pos,keys,depth):
        if not keys:return PORT
        kind,iss,k=a[pos]
        if kind==1:return balanced(keys)
        if kind!=0:raise ValueError('empty under nonempty core set')
        if not iss:
            if 0 not in keys:raise ValueError('non-gap0 anonymous')
            left=();right=keys;key=-1-depth
        else:
            if k not in keys:raise ValueError('core outside interval')
            left=tuple(v for v in keys if v<k);right=tuple(v for v in keys if v>k);key=k
        if depth==2:return S.node(key,balanced(left),balanced(right))
        li,ri=(1,2) if depth==0 else ((3,4) if pos==1 else (5,6))
        return S.node(key,sub(li,left,depth+1),sub(ri,right,depth+1))
    return sub(0,tuple(range(9)),0)
def rho(alpha):return shadow(representative(alpha))
def visible(t):
    out=[];stack=[(t,0)]
    while stack:
        n,d=stack.pop()
        if n[0]=='leaf':continue
        if d in (1,2):out.append((n[1],d))
        if d<2:stack.extend(((n[3],d+1),(n[2],d+1)))
    return out
