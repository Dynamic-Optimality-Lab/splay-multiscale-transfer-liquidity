"""Complete-source affine constraint discovery and exact grammar dual.

The mathematical proof of all-parameter necessity uses the explicit spine/rigid
subtree identities recorded in the manuscript. Finite affine interpolation alone
is never a universal proof. Exact matrix certificates check the deduction only.
"""
from fractions import Fraction
from itertools import combinations
import sympy as sp
from kernel import OLD,PARAM,dump,load,selected_replay


KINDS=['root_inverse','stem3_delete','stem3_keep','stem2_delete','stem2_keep','reverse_guard3','reverse_guard2']


def vine(n):return {'root':0,'children':{str(k):[None,k+1 if k<n else None] for k in range(n+1)}}


def reset(n,mode):return [[mode,x] for x in range(n+1)]+[[mode,x] for x in range(n-1,-1,-1)]


def reach(diagonal,prefix):
    keys=sorted(map(int,diagonal['children']));trees={a:OLD.Tree(diagonal,keys) for a in ('A','B')}
    for mode,x in prefix:
        OLD.plain(trees['A'],x)
        if mode=='K':OLD.plain(trees['B'],x)
    return trees['A'].state(),trees['B'].state()


def make(n,kind):
    assert n>=8 and n%2==0 and kind in KINDS
    v=vine(n)
    if kind.startswith('reverse_'):
        B=vine(n)
        if kind=='reverse_guard3':
            B['children']['1']=[None,n];B['children'][str(n)]=[2,None];B['children'][str(n-1)]=[None,None]
            keep=[['K',1],['K',0]]
        else:
            B['children']['0']=[None,n];B['children'][str(n)]=[1,None];B['children'][str(n-1)]=[None,None]
            keep=[['K',n],['K',0]]
        # No visited private vertex is erased: common B plus an A-only full
        # reset reaches the literal full pair (V,B). Closure below is exact.
        prefix=reset(n,'D');A,B2=reach(B,prefix);assert A==v and B2==B
        period=[['D',1],['D',0]]+keep+reset(n,'D')
        return {'name':f'{kind}_N{n}','initial_A':A,'initial_B':B,'diagonal':B,'prefix':prefix,'operations':period,'parameter_N':n,'template':kind}
    T=vine(n);T['root']=2;T['children']['0']=[None,None];T['children']['1']=[0,None];T['children']['2']=[1,3]
    prefix=[['D',n],['K',1],['K',0],['D',1]]
    if kind.startswith('stem3'):prefix += [['D',2],['D',0]]
    elif kind.startswith('stem2'):prefix += [['D',0]]
    A,B=reach(T,prefix);assert B==v
    word=[['D',n],['D',1]] if kind=='root_inverse' else [['K' if kind.endswith('keep') else 'D',1],['K' if kind.endswith('keep') else 'D',0]]
    word+=reset(n,'K')+[['K',2]]+prefix
    return {'name':f'{kind}_N{n}','initial_A':A,'initial_B':B,'diagonal':T,'prefix':prefix,'operations':word,'parameter_N':n,'template':kind}


def expected(n,kind):
    if kind=='root_inverse':base=[n-1,1,1,1,0,0];guard=[0]*6
    elif kind=='stem3_delete':base=[1,1,0,0,n-3,0];guard=[0]*6
    elif kind=='stem3_keep':base=[0,0,0,0,n-3,1];guard=base[:]
    elif kind=='stem2_delete':base=[1,1,n-2,0,-1,0];guard=[0,0,0,0,-(n-2),-1]
    elif kind=='stem2_keep':base=[0,0,n-2,1,-1,0];guard=base[:]
    elif kind=='reverse_guard3':base=[1,1,1,0,0,0];guard=[0,0,0,0,-1,-(n-2)]
    else:base=[2,1,0,0,0,0];guard=[0,0,-1,-(n-1),-1,-(n-2)]
    return base+guard


def run(out):
    observations=[];source_count=0;period_rotations=0
    for kind in KINDS:
        for n in (8,16,32,128):
            s=make(n,kind);w=selected_replay(s,{1,2});r0,r1=w['rows'];d=expected(n,kind)
            assert r0['delta']==d and r1['delta']==[-z for z in d],(kind,n,r0['delta'],d)
            assert r0['a']==r1['a']==1 and r0['q']==r1['q']==0
            dump(out/(s['name']+'.json.gz'),w);source_count+=1;period_rotations+=w['period_rotations']
            observations.append({'template':kind,'N':n,'first_vector':d,'inverse_exact':True,'A':w['A'],'Q_B':w['Q_B'],'full_pair_closure':True})
    # Infer the affine coefficient vectors, then cross-check the remaining
    # instances. Universal validity requires the explicit spine proofs.
    slopes=[];intercepts=[]
    for kind in KINDS:
        a=expected(8,kind);b=expected(16,kind);s=[Fraction(v-u,8) for u,v in zip(a,b)];c=[Fraction(u)-8*v for u,v in zip(a,s)]
        assert all(all(Fraction(z)==v*n+k for z,v,k in zip(expected(n,kind),s,c)) for n in (32,128))
        slopes.append([int(z) for z in s]);intercepts.append([int(z) for z in c])
    M=sp.Matrix(slopes);rref,pivots=M.rref();assert pivots==(0,2,4,8,9,10,11)
    terminal=sp.Matrix([[-2,0,-1,0,-1,0,0,0,1,16,1,16]])
    multipliers=M.T.gauss_jordan_solve(terminal.T)[0]
    assert multipliers.T*M==terminal
    exact=[Fraction(int(sp.numer(z)),int(sp.denom(z))) for z in multipliers]
    minimum=None;tested=0
    for size in range(len(KINDS)+1):
        for indices in combinations(range(len(KINDS)),size):
            tested+=1
            if not indices:continue
            sub=M[list(indices),:]
            if sub.col_join(terminal).rank()!=sub.rank():continue
            weights=sub.T.gauss_jordan_solve(terminal.T)[0]
            minimum={'size':size,'template_indices':list(indices),'templates':[KINDS[i] for i in indices],
                     'multipliers':list(map(str,weights)),'subsets_examined_through_first_minimum':tested,
                     'scope':'Minimum number among these seven recorded affine-template equality rows needed to imply the terminal contradiction, not a globally shortest proof.'}
            break
        if minimum is not None:break
    assert minimum['size']==5
    # Terminal q-limit inequality has RHS -1. Subtract its equality-row
    # representation; each signed equality is available in both directions.
    combined=[Fraction(terminal[i])-sum(w*Fraction(row[i]) for w,row in zip(exact,slopes)) for i in range(12)]
    assert combined==[0]*12
    for q in (1,5,17,65,257):
        s=PARAM.H(3,q);n=len(s['initial_A']['children']);w=selected_replay(s,{n+7});r=w['rows'][0]
        d=[-2*q-4,-3,-q+3,-2,-q-1,-1,0,0,q+5,16*q+10,q+3,16*q+9]
        assert r['delta']==d and r['a']==1 and r['q']==q+1,(q,r['delta'],d)
        # These are already included in the28 principal parametric sources.
        dump(out/f'terminal_H3_q{q}.json.gz',w)
    cert={'status':'EXACT_ALGEBRA_VERIFIED; source-uniform necessity requires the accompanying spine/closure proof',
          'source_templates':KINDS,'affine_slopes':slopes,'affine_intercepts':intercepts,
          'forced_zero_indices':list(pivots),'root_guard_zero_features':[6,7],
          'remaining_effective_indices':[1,3,5],'terminal_q_slope':list(map(int,terminal)),
          'equality_multipliers':[str(z) for z in exact],
          'optimized_universal_obstruction_core':minimum,
          'nonnegative_dual_rows':[{'template':kind,'equality_orientation':-1 if w>0 else 1,'weight':str(abs(w))} for kind,w in zip(KINDS,exact) if w],
          'combined_lhs':list(map(str,combined)),'combined_rhs':'-1','contradiction':'0<=-1',
          'declared_grammars':['frontier3','frontier3_roots_guarded'],'observations':observations,
          'new_parameter_source_instances':source_count,'period_rotations':period_rotations,
          'scope':'Fixed full-physical depth-frontier3 linear span, including fixed root-equality guards, arbitrary fixed signed real coefficients and any universal finite C. Not arbitrary potentials or the original global cost theorem.'}
    dump(out/'PARAMETRIC_DUAL_CERTIFICATE.json',cert);print({'parametric_sources':source_count,'exact_terminal_contradiction':'0<=-1','dual':list(map(str,exact))},flush=True)
    return cert


if __name__=='__main__':
    import sys
    from pathlib import Path
    run(Path(sys.argv[1]))
