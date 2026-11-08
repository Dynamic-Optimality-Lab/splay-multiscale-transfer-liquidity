"""Independent whole-union audit, using the two-operation source grammar.

No per-clause synthesis check is repeated. Verify the final union directly,
with the separate universal grammar and every nonpositive core exit.
"""
import json,sys,time
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix_v2 import PATHS
from complete_floor import lower_floor
from target_floor import N,opp,opposite_alpha
from compatibility import source_compatible
from paired_floors import paired_one
from lower_return_floors import lower_return_one
from seven_closure_floors import BYCORE,closure_one,SAVED
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ts=[freeze(r['tree']) for r in bank['nodes']];psi=[r['psi'] for r in bank['nodes']]
    dd=tab['B_depth'];nx=tab['B_destination'];m=[z3.Bool('ind_mark'+str(k)) for k in range(9)]
    proto=tuple(z3.Ints('ind_L ind_R ind_LL ind_LR ind_RL ind_RR'));cache={}
    T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(6,None,N(7,None,N(8)))))
    def floor(i,a,k):
        if (i,k) not in cache:
            t=ts[i];b=(z3.IntVal(t[0]),)+proto
            margins=[2-dd[i][y]//2+psi[nx[i][y]] for y in range(9)]
            q=z3.Or(lower_floor(t,b,m,psi[i],margins,k),z3.Not(source_compatible(b)))
            if k==1:
                if t==T:q=z3.Or(q,z3.And(z3.Not(m[4]),b[2]==4,b[6]==8))
                if opp(t)==T:
                    bm=opposite_alpha(b);q=z3.Or(q,z3.And(z3.Not(m[4]),bm[2]==4,bm[6]==8))
                q=z3.Or(q,paired_one(t,b),lower_return_one(t,b))
            cache[i,k]=z3.simplify(q)
        return z3.simplify(z3.substitute(cache[i,k],*((v,a[j+1]) for j,v in enumerate(proto))))
    proofs=[];omitted=0
    for i in sorted(BYCORE):
        if psi[i]>=1:continue
        for x in range(9):
            j=nx[i][x];w=2-dd[i][x]//2
            if w>0 or w+psi[j]>=1:omitted+=1;continue
            for p in PATHS:
                if p[0]!=int(x>ts[i][0]):continue
                assert time.process_time()<CAP-4
                u=build((p,),ts[i][0],x,None,'independent'+str(len(proofs)));a,b=u['source'],u['target']
                need=1-w;paid=floor(j,b,need) if need<=2 else z3.BoolVal(False)
                if need==1:paid=z3.Or(paid,closure_one(j,ts[j],b,m))
                sol=z3.Solver();sol.set(timeout=min(10000,int(1000*(CAP-time.process_time()-3))))
                sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[ts[i][0]],m[x],
                  closure_one(i,ts[i],a,m),z3.Not(floor(i,a,1)),z3.Not(paid))
                r=sol.check()
                assert r==z3.unsat,(i,x,p,str(r),str(sol.model()) if r==z3.sat else sol.reason_unknown())
                proofs.append({'i':i,'x':x,'j':j,'w':w,'word':p,'negation':'UNSAT'})
    # Independent arithmetic proof of the simultaneous augmentation step.
    d,e,w=z3.Ints('old_source old_target edge_weight');g,h=z3.Bools('source_region target_region')
    D=z3.If(g,z3.If(d<1,1,d),d);E=z3.If(h,z3.If(e<1,1,e),e)
    sol=z3.Solver();sol.add(d>=0,d<=2,e>=0,e<=2,w+e-d>=0,
      z3.Implies(z3.And(g,d<1),w+E>=1),w+E-D<0)
    assert sol.check()==z3.unsat
    write('audit_seven_independent.json',{'status':'INDEPENDENT_WHOLE_UNION_ONE_CREDIT_AUDIT_PASS',
      'new_whole_union_universal_checks':len(proofs),'proofs':proofs,'range_core_omissions':omitted,
      'independent_signed_composition_UNSAT':True,'all_masks_and_signatures_quantified':True,
      'separate_source_generator':'universal_grammar_v2.build, not per-clause prefix',
      'scope':'independent whole-union derivation; not external review or full compiler formalization',
      'Gamma0_Gamma1_one_credit_theorem_reused':True,'full_state_HIGH_h0_preserved':True,
      'new_finite_tests':0,'completed_synthesis_checks_replayed':0,'Step4_complete':False})
    print(json.dumps({'status':'PASS','independent_whole_union_checks':len(proofs)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_seven_independent_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
