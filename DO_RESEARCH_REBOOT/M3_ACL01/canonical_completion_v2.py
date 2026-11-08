"""State-only canonical port completion, fixed mu=341/sigma=(1,0,...,0).

This evaluates a potential. It never identifies actual graph endpoints.
The witness lifting retains every original explicit node; representative()
only supplies the parts of a physical alpha that the state can observe.
"""
import sys
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_H1F01','DO_RESEARCH_REBOOT/M3_FRC01',
 'DO_RESEARCH_REBOOT/M3_H2R01','DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
from one_gap_potential import OneGapPotential
U=tuple(range(-1,9)); MARKED=(0,2,4,6,8)

def representative(alpha):
    if len(alpha)!=7:raise ValueError('alpha length')
    a=tuple(tuple(x) for x in alpha)
    if not a[0][1] or a[0][2] not in range(9):raise ValueError('noncore root')
    def sub(pos,keys,depth):
        kind,iss,x=a[pos]
        if kind not in (0,1,2):raise ValueError('kind')
        if kind in (1,2):
            if depth==1 and any(a[j][0]!=kind for j in ((3,4) if pos==1 else (5,6))):
                raise ValueError('opaque propagation')
            if kind==2 and keys:raise ValueError('missing keys under empty')
            return S.balanced(keys)
        k=x if iss else -1
        if k not in keys:raise ValueError('real key outside interval')
        left=tuple(y for y in keys if y<k);right=tuple(y for y in keys if y>k)
        if depth==2:return S.node(k,S.balanced(left),S.balanced(right))
        li,ri=((1,2) if depth==0 else ((3,4) if pos==1 else (5,6)))
        return S.node(k,sub(li,left,depth+1),sub(ri,right,depth+1))
    # Root ak is ignored by the original low shadow_match7.
    a=((0,1,a[0][2]),)+a[1:]
    return sub(0,U,0)

def rho(alpha):return tuple(tuple(r) for r in V.shadow(representative(alpha)))

class CompleteOneGapPotential:
    def __init__(self):
        self.physical=OneGapPotential()
    def inspect(self,s):
        if s['mu']!=341 or s['sigma']!=[1]+[0]*9 or not(s['b']['kr'][8]==0 and s['b']['rr'][8]==19):
            raise ValueError('outside fixed sector')
        root=s['b']['root'];a=s['alpha']
        if root not in MARKED or not a[0][1] or a[0][2]!=root:
            return {'value':0,'rule':'boundary_zero','image_alpha':None,'table_node':None}
        try:image=rho(a)
        except ValueError:
            return {'value':0,'rule':'invalid_low_shape_zero','image_alpha':None,'table_node':None}
        si={**s,'alpha':[list(r) for r in image]}
        try:info=self.physical.inspect(si)
        except (AssertionError,KeyError):
            return {'value':0,'rule':'invalid_low_B_zero','image_alpha':None,'table_node':None}
        assert info['table_node'] is not None
        return {'value':info['one_gap_joint'],'rule':'canonical_completion','image_alpha':si['alpha'],
                'table_node':info['table_node'],'core_tree_id':info['core_tree_id'],'psi':info['psi']}
    def __call__(self,s):return self.inspect(s)['value']
