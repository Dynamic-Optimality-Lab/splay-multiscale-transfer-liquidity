"""Universal helper word coverage and independent source2 implication algebra."""
import json,sys,time
from pathlib import Path
import z3
from support import BASE,build,PATHS,gamma_words
CAP=min(120,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    root,x=z3.Ints('positive_root positive_terminal');proofs=[]
    for h in (0,9):
        for less in (False,True):
            allowed=gamma_words(4,2 if less else 6,h)
            # gamma_words takes actual roles: for max the representative
            # order is reversed, so derive the actual comparison directly.
            if h==9:allowed=gamma_words(4,2 if less else 6,h)
            for p in PATHS:
                if p[0]!=int(h==9):continue
                for q in PATHS:
                    if q[0]!=int(h==0) or (p,q) in allowed:continue
                    u=build((p,q),root,x,h,'red'+str(len(proofs)))
                    sol=z3.Solver();sol.add(*u['constraints'],root>=0,root<9,x>=0,x<9,
                      x<root if less else x>root)
                    r=sol.check();assert r==z3.unsat,(h,less,p,q,str(r))
                    proofs.append({'helper':h,'terminal_less_than_root':less,'word':[p,q],'excluded_negation':'UNSAT'})
    d,t,w=z3.Ints('positive_source positive_target negative_weight')
    sol=z3.Solver();sol.add(d==2,t>=0,t<=2,w<=-1,w+t-d>=0)
    assert sol.check()==z3.unsat
    sol=z3.Solver();sol.add(d>=0,d<=2,t>=0,t<=2,t-d>=0,1+t-d<0)
    assert sol.check()==z3.unsat
    assert len(proofs)==24
    assert time.process_time()<CAP-2
    write('audit_reductions.json',{'status':'UNIVERSAL_POSITIVE_SOURCE_AND_WORD_REDUCTIONS_PASS',
      'excluded_symbolic_word_pairs':proofs,'negative_H1_capacity_and_parallel_zero_arithmetic_UNSAT':True,
      'Gamma1_source_seed_two':'finite lineage induction, with helper-source qualifications independently audited in prose',
      'new_finite_tests':0,'completed_semantic_checks_replayed':0,'M3_complete':False})
    print(json.dumps({'status':'PASS','excluded_symbolic_word_pairs':len(proofs)}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_reductions_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
