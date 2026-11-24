"""Exact falsification of a direct adaptive weighted access-lemma potential."""
from exp04_core import *


def depths(tree):
    ds={};stack=[(tree.root,0)]
    while stack:
        v,d=stack.pop();ds[v]=d;stack.extend((x,d+1) for x in tree.ch[v] if x is not None)
    return ds


def product_potential(A,B):
    ds=depths(A);weights={k:Fraction(1,4**d) for k,d in ds.items()};mass={};stack=[(B.root,False)]
    while stack:
        k,done=stack.pop()
        if not done:
            stack.append((k,True));stack.extend((x,False) for x in B.ch[k] if x is not None)
        else:mass[k]=weights[k]+sum((mass[x] for x in B.ch[k] if x is not None),Fraction(0))
    result=Fraction(1)
    for k in B.keys:result*=mass[k]/weights[k]
    return result


if __name__=='__main__':
    meter=Meter('EXP04_cycle9_weighted_potential');results=[]
    for n in (65,129,257,513):
        k=n//2;a=Tree(vine(range(1,n+1)));b=Tree(vine(range(1,n+1)))
        # These are precisely the actual DELETE2..k prefix in the archived
        # omitted/mixed family, not an unclosed-fragment counterexample.
        for x in range(2,k+1):Replay.plain_splay(a,x)
        before=a.state();p0=product_potential(a,b);Replay.plain_splay(a,k+1);p1=product_potential(a,b);ratio=p1/p0
        formula=Fraction(4**k)
        for i in range(1,k+1):
            left=sum((Fraction(1,4**d) for d in range(k-i+1)),Fraction(0))
            right=sum((Fraction(1,4**d) for d in range(n-k)),Fraction(0))
            formula*= (left/4+right)/(left+right/4)
        assert ratio==formula and ratio>2**k
        results.append({'n':n,'A_root_before':k,'A_root_after':k+1,'original_operation':k,
            'original_bit':['A',k,1,0],'A_StepEv':1,'B_unchanged':True,'A_before':before,'A_after':a.state(),'B':b.state(),
            'exact_potential_product_ratio_hex':[hex(ratio.numerator),hex(ratio.denominator)],
            'certified_log2_potential_increase_greater_than':k,
            'archived_complete_source':'mixed_p7_Gcopies2' if n==513 else f'O_p{(n-1).bit_length()-3}_q1_L2_hits5_c1'})
        print('n',n,'one A rotation: Delta Phi >',k,flush=True)
    write('EXP04_WEIGHTED_POTENTIAL_REFUTATION.json',{'potential':'Phi(A,B)=log2 product_{v in B} (sum_{u in B-subtree(v)}4^(-depth_A(u)))/4^(-depth_A(v))',
        'result':'REFUTED constant A-primitive Lipschitz bound; B access-lemma side remains valid with fixed post-A weights',
        'parametric_proof':'For A rooted at k with two monotone chains and B a right vine: ratio=4^k product_{i=1}^k ((L_i/4+R)/(L_i+R/4)), where1<=L_i,R<=4/3. Each factor>=16/19, so ratio>2^k.',
        'sources':results});meter.success=True
