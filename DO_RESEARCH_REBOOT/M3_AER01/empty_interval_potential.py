"""Fixed-sector potential with source-complete empty-interval A erasure."""
import sys
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_ACL01','DO_RESEARCH_REBOOT/M3_H1F01']
from canonical_completion import S,V,U,MARKED,OneGapPotential

def representative(alpha):
    a=tuple(tuple(r) for r in alpha)
    if len(a)!=7 or not a[0][1] or a[0][2] not in range(9):raise ValueError('root')
    a=((0,1,a[0][2]),)+a[1:]
    def sub(pos,keys,depth):
        # Actual dangling references occupy branches with no logical key.
        # Their original shadow may read arbitrary slot-0 contents; ignore it.
        if depth>0 and not keys:return S.LEAF
        kind,iss,x=a[pos]
        if kind not in (0,1,2):raise ValueError('kind')
        if kind in (1,2):
            if kind==2:raise ValueError('nonempty interval under empty')
            if depth==1 and any(a[j][0]!=kind for j in ((3,4) if pos==1 else (5,6))):raise ValueError('propagation')
            return S.balanced(keys)
        k=x if iss else -1
        if k not in keys:raise ValueError('key')
        left=tuple(y for y in keys if y<k);right=tuple(y for y in keys if y>k)
        if depth==2:return S.node(k,S.balanced(left),S.balanced(right))
        li,ri=(1,2) if depth==0 else ((3,4) if pos==1 else (5,6))
        return S.node(k,sub(li,left,depth+1),sub(ri,right,depth+1))
    return sub(0,U,0)
def rho(alpha):return tuple(tuple(r) for r in V.shadow(representative(alpha)))

class EmptyIntervalPotential:
    def __init__(self):self.physical=OneGapPotential()
    def inspect(self,s):
        if s['mu']!=341 or s['sigma']!=[1]+[0]*9 or not(s['b']['kr'][8]==0 and s['b']['rr'][8]==19):raise ValueError('sector')
        a=s['alpha'];root=s['b']['root']
        if root not in MARKED or not a[0][1] or a[0][2]!=root:return {'value':0,'rule':'boundary_zero','image_alpha':None,'table_node':None}
        try:image=rho(a)
        except ValueError:return {'value':0,'rule':'invalid_low_shape_zero','image_alpha':None,'table_node':None}
        try:info=self.physical.inspect({**s,'alpha':[list(r) for r in image]})
        except (AssertionError,KeyError):return {'value':0,'rule':'invalid_low_B_zero','image_alpha':None,'table_node':None}
        assert info['table_node'] is not None
        return {'value':info['one_gap_joint'],'rule':'empty_interval_completion','image_alpha':[list(r) for r in image],
          'table_node':info['table_node'],'core_tree_id':info['core_tree_id'],'psi':info['psi']}
    def __call__(self,s):return self.inspect(s)['value']
