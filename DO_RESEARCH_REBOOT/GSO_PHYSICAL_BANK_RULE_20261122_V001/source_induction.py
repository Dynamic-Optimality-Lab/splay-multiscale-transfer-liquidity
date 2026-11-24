"""Universal arithmetic/source-window obligations for the all-capacity recipe.

These checks quantify H symbolically; finite samples are listed separately.
The old physical H comb induction is a mathematical dependency, not an LP fit.
"""
import sys
import z3
sys.dont_write_bytecode=True
import bank_rule as B
import family as F
import coarsening as C


def main():
    H,u,l=z3.Ints('H u l');burn=3*H+1;q=12*H+32
    solver=z3.Solver();solver.add(H>=1,l>=1,l<=4,u>=2*(q+1)-2*burn-3)
    count=u/2-(l+3)/2+1
    solver.add(count<burn);assert solver.check()==z3.unsat
    solver=z3.Solver();solver.add(H>=1,2*(q+1)-2*burn-3<4);assert solver.check()==z3.unsat
    # Universal natural induction skeleton: initial mass<=3H, each positive
    # stage drops at least1, and zero cannot supply 3H+1 fresh-input-free RR.
    records=[]
    for h in (1,2,3,5,8,16,32,65):
        par=F.parameters(h);a=b=h;l0=1;u0=2**(par['p']-3)*(par['q']+1)-3;steps=[]
        for r in range(3*h):
            _,out,_=C.local_fixed(a,b,h);a,b=out['a_new'],out['b_new'];l0=(l0+3)//2+1;u0=u0//2-par['burn_in'];assert u0>=l0
            steps.append(2*a+b)
        assert a==b==0 and u0//2-(l0+3)//2+1>=par['burn_in']
        records.append({'H':h,'p':par['p'],'q':par['q'],'profile_zero':True,'last_old_good_window':[l0,u0],'good_RR_steps_in_final_phase':u0//2-(l0+3)//2+1,'max_carry':3*h,'last_phase_original_RR_count':par['q'],'finite_recipe_arithmetic_only':True})
    out={'status':'SYMBOLIC_WINDOW_ARITHMETIC_VERIFIED','universal_H_queries':['Final interior has at least3H+1 RR steps','All preceding retained interior windows are nonempty by the same lower bound'],
         'induction_invariants':['1<=l_r<=4','u_r>=2^(p-3-r)*(q+1)-2*(3H+1)-3','M_r<=max(3H-r,0) until a zero-input phase already forces failure'],
         'source_parameters':'p=3H+4,q=12H+32,N=2^(p+1)*(q+1)+1',
         'finite_arithmetic_crosschecks':records,
         'source_uniform_claim_dependency':'The explicit physical comb-role and untouched-interior proof in Notion, together with SYMBOLIC_COARSENING_CERTIFICATE.json. No finite sample supplies that dependency.',
         'universal_CD':'OPEN'}
    B.write('SOURCE_INDUCTION_CERTIFICATE.json',out);print({'symbolic_window_queries':'UNSAT','finite_recipe_crosschecks':len(records),'root_status':'OPEN'})


if __name__=='__main__':main()
