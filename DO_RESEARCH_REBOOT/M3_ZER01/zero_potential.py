"""Explicit U9 completion then synthetic min-leaf augmentation; no new table."""
import sys
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_MSK01']
from uniform_potential import UniformPotential,S,V,core_tree

def representative(alpha):
    a=tuple(tuple(r) for r in alpha)
    if len(a)!=7 or not a[0][1] or a[0][2] not in range(9):raise ValueError('root')
    a=((0,1,a[0][2]),)+a[1:]
    def sub(pos,keys,depth):
        if depth>0 and not keys:return S.LEAF
        kind,ss,k=a[pos]
        if kind==1:
            if depth==1 and any(a[j][0]!=1 for j in ((3,4) if pos==1 else (5,6))):raise ValueError('propagation')
            return S.balanced(keys)
        if kind!=0 or not ss or k not in keys:raise ValueError('key')
        l=tuple(y for y in keys if y<k);r=tuple(y for y in keys if y>k)
        if depth==2:return S.node(k,S.balanced(l),S.balanced(r))
        li,ri=(1,2) if depth==0 else ((3,4) if pos==1 else (5,6))
        return S.node(k,sub(li,l,depth+1),sub(ri,r,depth+1))
    return sub(0,tuple(range(9)),0)
def augment(t):
    assert t!=S.LEAF
    if t[1]==0:
        assert t[2]==S.LEAF
        return S.node(0,S.node(-1,S.LEAF,S.LEAF),t[3])
    return S.node(t[1],augment(t[2]),t[3])
def rho(alpha):return tuple(tuple(r) for r in V.shadow(augment(representative(alpha))))
class ZeroPotential:
    def __init__(self):self.positive=UniformPotential()
    def inspect(self,s):
        if not(0<=s['mu']<512 and s['mu'].bit_count()==5 and s['sigma']==[0]*10 and s['b']['kr'][8]==0 and s['b']['rr'][8]==19):raise ValueError('sector')
        a=s['alpha'];b=s['b'];P=self.positive
        if b['root'] not in range(9) or not a[0][1] or a[0][2]!=b['root']:return {'value':0,'rule':'boundary_zero','table_node':None}
        try:image=rho(a);ai=P.sid[image];bi=P.ids[core_tree(b)];u=P.c['B_bases'][bi]+P.local[ai]
        except (ValueError,KeyError,AssertionError):return {'value':0,'rule':'invalid_low_state_zero','table_node':None}
        v=P.p[u];assert -2<=v<=-P.c['psi'][bi]<=0
        return {'value':v,'rule':'synthetic_min_leaf','table_node':u,'psi':P.c['psi'][bi],'image_alpha':[list(r) for r in image]}
    def __call__(self,s):return self.inspect(s)['value']
