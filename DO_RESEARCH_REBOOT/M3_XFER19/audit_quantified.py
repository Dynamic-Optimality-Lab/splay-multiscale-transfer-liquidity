"""Bounded universal certificate construction, not finite tests.

Frozen Int-exact Z3; one unknown function on existing observables, ALL
symbolic prefix productions/masks quantified. Complete old core/kernel
facts are reused. SAT requires independent extraction/audit before proof.
"""
import json,sys,time,itertools,hashlib
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix import PATHS
from compatibility import source_compatible
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]));NCORE=4862
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def opposite(t):return None if t is None else (8-t[0],opposite(t[2]),opposite(t[1]))
def const_array(values,default=0):
    a=z3.K(z3.IntSort(),z3.IntVal(default))
    for i,v in enumerate(values):
        if v!=default:a=z3.Store(a,i,z3.IntVal(v))
    return a
def ast_count(expressions):
    seen=set();todo=list(expressions)
    while todo:
        e=todo.pop();k=e.get_id()
        if k in seen:continue
        seen.add(k);assert len(seen)<=4000000,'INPUT_DAG_CAP'
        todo.extend(e.children())
    return len(seen)
def main():
    assert z3.get_version_string()=='5.1.0'
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    kernel=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    assert bank['status']==tab['status']=='COMPLETE' and bank['core_topologies']==NCORE
    ts=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[q['psi'] for q in bank['nodes']];depth=tab['B_depth'];dest=tab['B_destination']
    mir=[ids[opposite(t)] for t in ts]
    rootA=const_array([t[0] for t in ts]);psiA=const_array(psi)
    costA=const_array([2-depth[i][x]//2 for i in range(NCORE) for x in range(9)],2)
    nextA=const_array([dest[i][x] for i in range(NCORE) for x in range(9)])
    marginA=const_array([2-depth[i][x]//2+psi[dest[i][x]] for i in range(NCORE) for x in range(9)],2)
    hcost=[[2]*(9*NCORE) for _ in range(2)];hnext=[[0]*(9*NCORE) for _ in range(2)]
    for q in kernel['rows']:
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        i,x,j,w=q['entry_core'],q['target'],q['exit_core'],q['w']
        hcost[0][i*9+x]=w;hnext[0][i*9+x]=j
        hcost[1][mir[i]*9+8-x]=w;hnext[1][mir[i]*9+8-x]=mir[j]
    HC=[const_array(v,2) for v in hcost];HN=[const_array(v) for v in hnext]
    raw=z3.Function('RawPublicDebt',*[z3.IntSort()]*8,z3.IntSort())
    def bits(mu):return [(mu/(1<<k))%2==1 for k in range(9)]
    def marked(mu,k):
        b=bits(mu);return z3.Or(*(z3.And(k==j,b[j]) for j in range(9)))
    def legal(mu):return z3.And(mu>=0,mu<512,z3.Sum(*(z3.If(v,1,0) for v in bits(mu)))==5)
    def value(i,mu,a):
        r=z3.Select(rootA,i);p=z3.Select(psiA,i)
        sc=source_compatible(a,r)
        c1=z3.And(*(z3.Implies(z3.And(a[j]>=0,a[j]<9,a[j]!=r,marked(mu,a[j])),
          z3.Select(marginA,i*9+a[j])>=1) for j in range(1,7)))
        base=z3.If(z3.And(p<1,c1),z3.IntVal(1),p)
        candidate=raw(i,mu,*a[1:])
        bounded=z3.If(candidate<base,base,z3.If(candidate>2,z3.IntVal(2),candidate))
        return z3.If(marked(mu,r),z3.If(sc,bounded,z3.IntVal(2)),z3.IntVal(0))
    solver=z3.Solver();schemas=[];forms=[]
    families=[(None,(p,)) for p in PATHS]+[(g,(p,q)) for g in (0,9) for p,q in itertools.product(PATHS,repeat=2)]
    for number,(helper,word) in enumerate(families):
        assert time.process_time()<CAP-5
        i,mu,x=z3.Ints('B_'+str(number)+' mask_'+str(number)+' target_'+str(number))
        root=z3.Select(rootA,i);flat=i*9+x
        if helper is None:w=z3.Select(costA,flat);j=z3.Select(nextA,flat)
        else:h=int(helper==9);w=z3.Select(HC[h],flat);j=z3.Select(HN[h],flat)
        u=build(word,root,x,helper,'s'+str(number))
        static=z3.And(i>=0,i<NCORE,x>=0,x<9,legal(mu),marked(mu,root),marked(mu,x),w<2,
          z3.Select(rootA,j)==x,*u['constraints'])
        residual=w+value(j,mu,u['target'])-value(i,mu,u['source'])
        formula=z3.ForAll([i,mu,x]+u['private_variables'],z3.Implies(static,residual>=0))
        solver.add(formula);forms.append(formula)
        schemas.append({'helper':helper,'word':word,'observed_addresses':sorted(u['observed']),
          'real_required_addresses':sorted(u['required']),
          'terminal_source_address':u['terminal_source_address'],'private_variable_count':len(u['private_variables'])})
    assert len(schemas)==78
    dag=ast_count(forms);assert dag<=4000000
    write('quantified_schema.json',{'universal_schemas':schemas,'input_DAG_nodes':dag,
      'new_source_transition_or_population_tests':0,'canonical_prefix_terms_enumerated':0,
      'old_core_kernel_facts_reused':True,'candidate_range_and_floor_built_in':True,
      'omitted_original_classes':'ONLY proved w>=2 range and Gamma0/unmarked-source source theorems',
      'R1_R4_h0_fullstate_and_scope_preserved':True})
    with (BASE/'quantified_problem.smt2').open('x',encoding='utf-8') as f:f.write(solver.to_smt2())
    remaining=CAP-time.process_time()-5;assert remaining>0
    solver.set(timeout=int(remaining*1000))
    print(json.dumps({'universal_formulas':78,'input_DAG_nodes':dag,'construction_CPU_before_solve':time.process_time(),
      'remaining_construction_CPU':remaining}),flush=True)
    result=solver.check();model_exported=False
    report={'status':'UNIVERSAL_MODEL_REQUIRES_INDEPENDENT_AUDIT' if result==z3.sat else 'NO_UNIVERSAL_CERTIFICATE_CONSTRUCTED',
      'solver_result':str(result),'reason':solver.reason_unknown() if result==z3.unknown else None,
      'new_symbolic_queries':1,'universal_schemas':78,'input_DAG_nodes':dag,
      'new_finite_population_or_mask_tests':0,'original_root_or_psi_bank_regenerated':False,
      'completed_semantic_checks_replayed':0,'Step4_complete':False,
      'UNSAT_would_only_refute_this_stronger_count_free_range_template':True}
    if result==z3.sat:
        model=solver.model()
        params=z3.Ints('public_core public_mask public_L public_R public_LL public_LR public_RL public_RR')
        body=model.eval(raw(*params),model_completion=True)
        with (BASE/'quantified_model.txt').open('x',encoding='utf-8') as f:f.write(str(model))
        body_script=z3.Solver();body_script.add(z3.Int('exported_debt')==body)
        with (BASE/'raw_model_function.smt2').open('x',encoding='utf-8') as f:f.write(body_script.to_smt2())
        model_exported=True;report['raw_function_exported_for_independent_audit']=True
    write('audit_quantified.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_quantified_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
