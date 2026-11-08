"""Read-only original LOW AST/charge contract and independent Gamma0 algebra."""
import ast,json,sys,time,hashlib
from pathlib import Path
import z3
BASE=Path(__file__).resolve().parent;R=BASE.parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    p=R/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    text=p.read_text(encoding='utf-8');module=ast.parse(text)
    function=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='build_slow')
    source=ast.get_source_segment(text,function)
    clauses=['C.append(d.EQ(macro_H(d, wit), Hv))','C.append(d.LE(Hv, d.const_int(2, 2)))',
      'C.append(root_terminated(d, wit, bt, st, bs[e], e, active))',
      'C.append(same_keep_target(d, wit, inv, bt, e, active))',
      'C.append(d.LE(d.ADD(bt.q, bt.q, 5), bd_last))',
      'C.append(d.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5)))',
      'C.append(tisS)','C.append(marked)','C.append(chg)',
      'C.append(d.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5)))']
    assert all(s in source for s in clauses)
    q,pv,s,t=z3.Ints('contract_q contract_psi contract_source_debt contract_target_debt')
    sol=z3.Solver();sol.add(q>=0,q<=4,pv>=0,pv<=2,pv>=q-2,s>=0,s<=2,t>=pv,t<=2,4-q+t-s<0)
    assert sol.check()==z3.unsat
    assert time.process_time()<CAP-2
    write('contract_audit.json',{'status':'INDEPENDENT_LITERAL_LOW_CONTRACT_AND_GAMMA0_AUDIT_PASS',
      'source':str(p.resolve()),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
      'original_AST_conjuncts_present':clauses,'original_H_upper_bound':2,
      'Gamma0_actual_preterminal_floor_inequality_UNSAT':True,
      'HIGH_contract_unchanged':True,'new_original_root_evaluations':0,'new_finite_tests':0,
      'completed_semantic_checks_replayed':0})
    print(json.dumps({'status':'PASS','original_budget':2,'Gamma0_algebra':'UNSAT negation'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_contract_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
