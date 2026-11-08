"""Universal source observation implications for visible Gamma1 terminals."""
import json,sys,time
import z3
from support import BASE,build
CAP=min(120,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    root,x=z3.Ints('visible_root visible_terminal');proofs=[]
    cases=[(((0,),(1,0)),4),(((0,0),(1,)),1),(((0,),(1,1)),2),(((0,1),(1,1)),2)]
    reverse={1:2,2:1,3:6,4:5,5:4,6:3}
    for h in (0,9):
        for word,pos in cases:
            if h==9:word=tuple(tuple(1-v for v in p) for p in word);pos=reverse[pos]
            u=build(word,root,x,h,'visible'+str(len(proofs)));sol=z3.Solver()
            sol.add(*u['constraints'],root>=0,root<9,x>=0,x<9,x!=root,u['source'][pos]!=x)
            assert sol.check()==z3.unsat
            proofs.append({'helper':h,'word':word,'visible_source_position':pos,'negation':'UNSAT'})
    ps,margin=z3.Ints('visible_psi visible_margin');mark,seen,c2=z3.Bools('visible_mark visible_seen visible_c2')
    sol=z3.Solver();sol.add(ps<2,margin<2,mark,seen,z3.Implies(c2,z3.Implies(z3.And(mark,seen),margin>=2)),z3.Or(ps==2,c2))
    assert sol.check()==z3.unsat
    assert time.process_time()<CAP-2
    write('audit_visibility.json',{'status':'UNIVERSAL_VISIBLE_TERMINAL_CAPACITY_EXCLUSION_PASS','proofs':proofs,
      'capacity_contradiction_UNSAT':True,'new_finite_tests':0,'completed_semantic_checks_replayed':0})
    print(json.dumps({'status':'PASS','source_observation_implications':8}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_visibility_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
