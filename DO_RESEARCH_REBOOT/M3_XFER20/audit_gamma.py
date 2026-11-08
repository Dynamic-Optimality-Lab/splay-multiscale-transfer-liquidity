"""Uniform Gamma1+1 audit after signed H1 completion."""
import json,sys,time
import z3
from support import BASE,trees,ids,psi,opp,opposite_alpha,build,gamma_words,seed_two,necessary_two
from complete_floor import hidden_min
from positive_candidate import candidate_floor
CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    inv=json.loads((BASE/'positive_inventory.json').read_text());jobs=[]
    for q in inv['Gamma1_gap0_critical_rows']:
        i,x,j=q['entry_core'],q['target'],q['exit_core']
        for h,i,x,j in ((0,i,x,j),(9,ids[opp(trees[i])],8-x,ids[opp(trees[j])])):
            for word in gamma_words(trees[i][0],x,h):jobs.append((i,x,j,h,word))
    m=[z3.Bool('gp_mark'+str(k)) for k in range(9)];legal=z3.PbEq([(v,1) for v in m],5)
    proto=tuple(z3.Ints('gp_L gp_R gp_LL gp_LR gp_RL gp_RR'));cache={}
    def floor(i,a,full):
        if (i,full) not in cache:
            b=(z3.IntVal(trees[i][0]),)+proto;cache[i,full]=z3.simplify(candidate_floor(i,b,m,1,full))
        return z3.substitute(cache[i,full],*((v,a[p+1]) for p,v in enumerate(proto)))
    proofs=queries=refined=0;unresolved=None
    with (BASE/'gamma_checkpoints.jsonl').open('x',encoding='utf-8') as cert:
        for number,(i,x,j,h,word) in enumerate(jobs):
            if time.process_time()>=CAP-5:unresolved={'kind':'CAP','job':number};break
            u=build(word,trees[i][0],x,h,'gp'+str(number));a,b=u['source'],u['target']
            sol=z3.Solver();sol.add(*u['constraints'],legal,m[trees[i][0]],m[x],seed_two(i,a,m),necessary_two(i,a,m),
              z3.Not(z3.Or(hidden_min(trees[i],a),hidden_min(opp(trees[i]),opposite_alpha(a)))))
            for full in (False,True):
                sol.push();sol.add(z3.Not(floor(j,b,full)));sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-3)))))
                r=sol.check();queries+=1
                if r==z3.unsat:sol.pop();break
                if not full and r==z3.sat:sol.pop();refined+=1;continue
                unresolved={'kind':'UNPAID_GAMMA_TARGET' if r==z3.sat else 'UNKNOWN','job':number,
                  'source_core':i,'target_key':x,'destination_core':j,'helper':h,'word':word,
                  'B_source':trees[i],'B_target':trees[j],'source_psi':psi[i],'destination_psi':psi[j],
                  'original_negative_cycle_claimed':False}
                if r==z3.sat:
                    model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long()
                    unresolved.update({'source_alpha':[val(v) for v in a],'target_alpha':[val(v) for v in b],
                      'marked_keys':[k for k in range(9) if z3.is_true(model.eval(m[k],model_completion=True))],
                      'source_proved_floor2':z3.is_true(model.eval(candidate_floor(i,a,m,2,True),model_completion=True))})
                else:unresolved['reason']=sol.reason_unknown()
                with (BASE/'gamma_unresolved.smt2').open('x',encoding='utf-8') as f:f.write(sol.to_smt2())
                sol.pop();break
            if unresolved:break
            cert.write(json.dumps({'job':number,'source_core':i,'target_key':x,'destination_core':j,
              'helper':h,'word':word,'full_refinement':full,'proof':'UNIVERSAL_UNSAT'})+'\n');cert.flush();proofs+=1
            if proofs%200==0:print(json.dumps({'Gamma1_jobs_proved':proofs,'required':len(jobs),'CPU':time.process_time()}),flush=True)
    report={'status':'COMPLETE_GAMMA1_POSITIVE_AUDIT_PASS' if unresolved is None else 'GAMMA_POSITIVE_NOT_PROVED',
      'required_jobs':len(jobs),'proved_jobs':proofs,'queries':queries,'full_refinements':refined,
      'unresolved':unresolved,'new_finite_tests':0,'completed_semantic_checks_replayed':0,'M3_complete':False}
    write('audit_gamma.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_gamma_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
