"""Universal arbitrary-signature zero-H1 lower-floor proof branches.

NOT population tests: prefix production variables, anonymous gaps and
mask are universally quantified via refutation of the negated formula.
The frozen complete nine-core facts are reused, not regenerated.
An incomplete-floor SAT branch is unresolved, never a D refutation.
"""
import json,sys,time,hashlib
from pathlib import Path
import z3
from symbolic_prefix_v2 import prefix,PATHS
from complete_floor import lower_floor
BASE=Path(__file__).resolve().parent;CAP=min(120,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    assert z3.get_version_string()=='5.1.0'
    saved=BASE.parent/'M3_LDR01/negative_run_census.json'
    access=BASE.parent/'M3_H1F01/cheap_census.json'
    bank=json.loads(saved.read_text());table=json.loads(access.read_text())
    assert bank['status']==table['status']=='COMPLETE' and bank['core_topologies']==4862
    trees=[freeze(r['tree']) for r in bank['nodes']];psi=[r['psi'] for r in bank['nodes']]
    Bdepth=table['B_depth'];Bdest=table['B_destination']
    # Reuse the exact complete old facts. No new splay, bank, census or
    # original-root evaluation, no tree-population models are generated.
    cases={}
    for i,t in enumerate(trees):
        if psi[i]==0:continue
        for x in range(9):
            if Bdepth[i][x] not in (4,5):continue
            j=Bdest[i][x]
            if psi[j]>=psi[i]:continue
            key=(t[0],x,j,psi[i]);cases.setdefault(key,[]).append(i)
    branches=len(cases)*6;assert branches<2000000
    completed=[];unknown=None;queries=0
    for (root,target,j,k),sources in cases.items():
        margin=[2-Bdepth[j][y]//2+psi[Bdest[j][y]] for y in range(9)]
        for path in PATHS:
            assert time.process_time()<CAP and queries<2000000
            u=prefix(path,root,target,'q'+str(queries))
            m=[z3.Bool('m'+str(queries)+'_'+str(v)) for v in range(9)]
            solver=z3.Solver();solver.set(timeout=5000)
            solver.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[root],m[target])
            floor=lower_floor(trees[j],u['target'],m,psi[j],margin,k)
            solver.add(z3.Not(floor));queries+=1
            result=solver.check()
            if result!=z3.unsat:
                unknown={'kind':'SYMBOLIC_INCOMPLETE_LOWER_FLOOR_BRANCH' if result==z3.sat else 'SMT_UNKNOWN',
                  'source_core_ids':sources,'target_core_id':j,'source_root':root,'target_key':target,'source_psi':k,
                  'target_psi':psi[j],'actual_A_word':path,'B_target_core':bank['nodes'][j]['tree'],
                  'B_source_core':bank['nodes'][sources[0]]['tree'],
                  'omitted_old_caps_may_still_prove_this_row':True,'original_counterexample_claimed':False}
                if result==z3.sat:
                    model=solver.model()
                    val=lambda a:[model.eval(v,model_completion=True).as_long() for v in a]
                    unknown.update({'source_alpha':val(u['source']),'target_alpha':val(u['target']),
                      'marked_keys':[q for q,v in enumerate(m) if z3.is_true(model.eval(v))],
                      'protected_production_types':[[list(p),model.eval(v,model_completion=True).as_long()] for p,v in sorted(u['types'].items())],
                      'protected_anonymous_gaps':[[list(p),model.eval(v,model_completion=True).as_long()] for p,v in sorted(u['gaps'].items())]})
                else:unknown['reason']=solver.reason_unknown()
                with (BASE/'first_unresolved_lower_v2.smt2').open('x',encoding='utf-8') as f:f.write(solver.to_smt2())
                break
            completed.append({'root':root,'target':target,'target_core':j,'psi_source':k,'word':path,'source_ids':sources})
        if unknown:break
    write('audit_lower_v2.json',{'status':'UNIVERSAL_LOWER_FLOOR_ALL_BRANCHES_UNSAT' if unknown is None else 'UNRESOLVED_SYMBOLIC_BRANCH_NOT_A_FINITE_TEST',
      'canonical_B_case_groups':len(cases),'universal_branches_required':branches,'new_symbolic_queries':queries,
      'completed_UNSAT_branches':completed,'first_unresolved':unknown,
      'original_signatures_quantified':'ALL, by completed count-free source coverage',
      'finite_population_or_mask_tests':0,'completed_semantic_checks_replayed':0,
      'new_original_root_evaluations':0,'saved_core_fact_files_read':[str(saved),str(access)],
      'frozen_Z3_version':z3.get_version_string(),'Step4_complete':False})
    print(json.dumps({'queries':queries,'completed_universal_UNSAT_branches':len(completed),'first_unresolved':unknown},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_lower_v2_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
