"""Universal arbitrary-label helper-target and maximal-credit audit."""
import json,sys,time
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix_v2 import PATHS
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    root,x=z3.Ints('normalized_root normalized_terminal');proofs=[]
    for h in (0,9):
        for p in PATHS:
            if p[0]!=int(h==9):continue
            for q in PATHS:
                if q[0]!=int(h==0):continue
                u=build((p,q),root,x,h,'norm'+str(len(proofs)))
                sol=z3.Solver();sol.add(*u['constraints'],root!=x,
                  z3.Or(*(u['target'][j]==x for j in range(1,7))))
                r=sol.check();assert r==z3.unsat,(h,p,q,str(r))
                proofs.append({'helper':h,'word':[p,q],'symbolic_root_terminal_negation':'UNSAT'})
    # Any previously proved source row transports when its target correction
    # is unchanged and its source correction decreases.
    d,e,c,b,w=z3.Ints('norm_d norm_e norm_c norm_b norm_w');n=z3.Bool('norm_source_N')
    D=z3.If(d>=c,d,c);E=z3.If(e>=b,e,b);DN=z3.If(n,D,d)
    sol=z3.Solver();sol.add(c>=0,b>=0,w+E-D>=0,w+E-DN<0)
    assert sol.check()==z3.unsat
    g1,g2,h1,h2=z3.Bools('max_g1 max_g2 max_h1 max_h2')
    D=z3.If(g2,2,z3.If(g1,z3.If(d<1,1,d),d));E=z3.If(h2,2,z3.If(h1,z3.If(e<1,1,e),e))
    sol=z3.Solver();sol.add(d>=0,d<=2,e>=0,e<=2,w+e-d>=0,
      z3.Implies(z3.And(g2,d<2),w+E>=2),
      z3.Implies(z3.And(g1,z3.Not(g2),d<1),w+E>=1),w+E-D<0)
    assert sol.check()==z3.unsat
    assert len(proofs)==18 # nine possible A word pairs per extremal helper
    assert time.process_time()<CAP
    write('audit_normalization.json',{'status':'UNIVERSAL_CHEAP_TARGET_AND_MAXIMAL_LEVEL_REDUCTION_PASS',
      'helper_word_proofs':proofs,'original_H1_six_word_theorem_reused':True,
      'transport_and_maximal_level_arithmetic_UNSAT':True,'original_last_top_pair_old_root_depth_bound_reused':True,
      'Gamma1_same_old_root_price_at_least3':True,'new_finite_tests':0,'Step4_complete':False})
    print(json.dumps({'status':'PASS','symbolic_helper_word_schemas':len(proofs)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_normalization_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
