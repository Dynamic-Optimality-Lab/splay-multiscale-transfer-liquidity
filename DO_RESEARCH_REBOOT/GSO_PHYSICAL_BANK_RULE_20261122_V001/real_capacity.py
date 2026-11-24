"""Same frozen transfer law: obstruction also for arbitrary finite real capacity.

Runtime examples use exact rational arithmetic. Real universal statements are
linear-arithmetic identities plus the finite coarsening/source proof, not a
rounding argument from integer capacities.
"""
import sys
import math
from fractions import Fraction
import z3
sys.dont_write_bytecode=True
import bank_rule as B


def rational_recipe(H):
    H=Fraction(H);assert H>0;a=b=H;profiles=[];burns=[]
    while 2*a+b>=1:
        I=2*a+b
        if I>=2*H+1:burn=2
        else:burn=math.ceil(H/(2*H-I+1))+4
        carry=(H,H,H)
        for _ in range(burn):
            s=sum(carry)+I-1;out=tuple(min(H,max(0,s-j*H)) for j in range(6));new=(out[0],out[1],out[4])
            if new==carry:break
            carry=new
        else:raise AssertionError('finite real upper-carry burn bound failed')
        aa=out[5];bb=out[2];assert aa==max(0,I-2*H-1) and bb==min(H,I-1) and 2*aa+bb<=I-1
        profiles.append({'a':str(a),'b':str(b),'I':str(I),'a_next':str(aa),'b_next':str(bb),'burn':burn});burns.append(burn);a,b=aa,bb
        assert len(profiles)<=math.floor(3*H)
    I=2*a+b;dry=math.floor(3*H/(1-I))+1;burn=max([1,dry,*burns]);p=len(profiles)+4;q=4*burn+8
    assert dry*(1-I)>3*H
    return {'H':str(H),'p':p,'q':q,'N':2**(p+1)*(q+1)+1,'global_burn':burn,'dry_packet':dry,'terminal_fresh_input':str(I),'profiles':profiles,'materialized':False}


def symbolic():
    H,a,b,t,p,r=z3.Reals('H a b t p r');I=2*a+b;s=t+p+r+I-1
    clamp=lambda v:z3.If(v<=0,0,z3.If(v>=H,H,v))
    out=[clamp(s-j*H) for j in range(6)];base=[H>0,a>=0,a<=H,b>=0,b<=H,t>=0,t<=H,p>=0,p<=H,r>=0,r<=H,I>=1,t==out[0],p==out[1],r==out[4]]
    claims={'real_weighted_loss':2*out[5]+out[2]<=I-1,'real_a_formula':out[5]==z3.If(I-2*H-1>0,I-2*H-1,0),'real_b_formula':out[2]==z3.If(I-1<H,I-1,H)}
    checked=[]
    for name,claim in claims.items():
        sol=z3.Solver();sol.add(*base,z3.Not(claim));assert sol.check()==z3.unsat;checked.append(name)
    # Scalar sum of the three carry outputs. In the decreasing region its
    # decrement is the fixed positive delta, so convergence is finite even
    # when capacities are irrational. No global funding theorem is assumed.
    c=z3.Real('c');fresh=z3.Real('fresh');sigma=c+fresh-1
    cs=clamp(sigma)+clamp(sigma-H)+clamp(sigma-4*H);delta=2*H-fresh+1
    sol=z3.Solver();sol.add(H>0,fresh>=1,fresh<2*H+1,c>=2*H,c<=3*H,z3.Not(cs==z3.If(sigma<=4*H,2*H,c-delta)));assert sol.check()==z3.unsat;checked.append('finite_scalar_carry_descent')
    burn,q,u,l=z3.Ints('burn q u l');sol=z3.Solver();sol.add(burn>=1,q==4*burn+8,l>=1,l<=4,u>=2*(q+1)-2*burn-3,u/2-(l+3)/2+1<burn);assert sol.check()==z3.unsat;checked.append('general_burn_window')
    return checked


def main():
    queries=symbolic();cases=[rational_recipe(h) for h in ('1/5','1/2','1','3/2','8/3','5','8','17/2','128/13')]
    out={'status':'REAL_CAPACITY_EXTENSION_SYMBOLICALLY_VERIFIED','universal_queries':queries,
         'general_recipe':['Start a=b=H for any finite H>0.','While I=2a+b>=1, let a_next=max(0,I-2H-1), b_next=min(H,I-1). Weighted mass drops at least1; stop after at most floor(3H) stages.','For I>=2H+1 the upper carry is immediately stationary; otherwise delta=2H-I+1>0, and ceil(H/delta)+4 steps suffice.','At terminal I<1 choose dry packet L=floor(3H/(1-I))+1. Let burn dominate every local burn and L.','Choose p=number_of_stages+4, q=4*burn+8 in the complete original H_(p,q). The same nested interior proof forces an unpaid original U RR.'],
         'exact_rational_arithmetic_crosschecks':cases,
         'scope':'Same target-first/increasing-order rule with fractional balances permitted. No rounding assumption and no exclusion of other redistribution kernels. The general real-source proof is mathematical, not full Lean formalization.',
         'universal_CD':'OPEN'}
    B.write('REAL_CAPACITY_CERTIFICATE.json',out);print({'symbolic_real_queries':len(queries),'exact_rational_recipe_crosschecks':len(cases),'root_status':'OPEN'})


if __name__=='__main__':main()
