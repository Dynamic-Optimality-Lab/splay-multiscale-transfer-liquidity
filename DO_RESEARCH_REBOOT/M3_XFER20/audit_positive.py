"""Uniform +1 LOW target floors on the complete necessary failure domain."""
import json,sys,time
import z3
from support import BASE,trees,ids,psi,depth,destination,opp,opposite_alpha,build,PATHS,gamma_words
from support import cheap_floor,full_floor,seed_two,necessary_two,kernel
from complete_floor import hidden_min
CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    assert json.loads((BASE/'audit_reductions.json').read_text())['status']=='UNIVERSAL_POSITIVE_SOURCE_AND_WORD_REDUCTIONS_PASS'
    inv=json.loads((BASE/'positive_inventory.json').read_text())
    m=[z3.Bool('pos_mark'+str(k)) for k in range(9)];legal=z3.PbEq([(v,1) for v in m],5)
    proto=tuple(z3.Ints('pos_L pos_R pos_LL pos_LR pos_RL pos_RR'));cache={}
    def floor(i,a,full):
        if (i,full) not in cache:
            b=(z3.IntVal(trees[i][0]),)+proto
            cache[i,full]=z3.simplify((full_floor if full else cheap_floor)(i,b,m,1))
        return z3.substitute(cache[i,full],*((v,a[p+1]) for p,v in enumerate(proto)))
    jobs=[]
    for i,x,j in inv['H1_critical_core_rows']:
        for p in PATHS:
            if p[0]==int(x>trees[i][0]):jobs.append(('H1',i,x,j,None,(p,)))
    for q in inv['Gamma1_gap0_critical_rows']:
        i,x,j=q['entry_core'],q['target'],q['exit_core']
        for h,i,x,j in ((0,i,x,j),(9,ids[opp(trees[i])],8-x,ids[opp(trees[j])])):
            for word in gamma_words(trees[i][0],x,h):jobs.append(('Gamma1',i,x,j,h,word))
    proofs=queries=refined=0;unresolved=None
    with (BASE/'positive_checkpoints.jsonl').open('x',encoding='utf-8') as cert:
        for number,(kind,i,x,j,h,word) in enumerate(jobs):
            if time.process_time()>=CAP-5:
                unresolved={'kind':'CAP','job':number};break
            u=build(word,trees[i][0],x,h,'pos'+str(number));a,b=u['source'],u['target']
            sol=z3.Solver();sol.add(*u['constraints'],legal,m[trees[i][0]],m[x])
            if kind=='Gamma1':
                sol.add(seed_two(i,a,m),necessary_two(i,a,m),
                  z3.Not(z3.Or(hidden_min(trees[i],a),hidden_min(opp(trees[i]),opposite_alpha(a)))))
            for full in (False,True):
                sol.push();sol.add(z3.Not(floor(j,b,full)))
                sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-3)))))
                result=sol.check();queries+=1
                if result==z3.unsat:sol.pop();break
                if not full and result==z3.sat:sol.pop();refined+=1;continue
                unresolved={'kind':'UNPAID_UNIVERSAL_TARGET_FLOOR' if result==z3.sat else 'UNKNOWN',
                  'job':number,'normal_form':kind,'source_core':i,'target_key':x,'destination_core':j,'helper':h,'word':word,
                  'B_source':trees[i],'B_target':trees[j],'original_negative_cycle_claimed':False}
                if result==z3.sat:
                    model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long()
                    unresolved.update({'source_alpha':[val(v) for v in a],'target_alpha':[val(v) for v in b],
                      'marked_keys':[k for k in range(9) if z3.is_true(model.eval(m[k],model_completion=True))],
                      'source_psi':psi[i],'destination_psi':psi[j],
                      'source_full_floor2':z3.is_true(model.eval(full_floor(i,a,m,2),model_completion=True))})
                else:unresolved['reason']=sol.reason_unknown()
                with (BASE/'positive_unresolved.smt2').open('x',encoding='utf-8') as f:f.write(sol.to_smt2())
                sol.pop();break
            if unresolved:break
            cert.write(json.dumps({'job':number,'normal_form':kind,'source_core':i,'target_key':x,
              'destination_core':j,'helper':h,'word':word,'full_floor_refinement':full,'proof':'UNIVERSAL_UNSAT'})+'\n');cert.flush();proofs+=1
            if proofs%200==0:print(json.dumps({'positive_jobs_proved':proofs,'required':len(jobs),'CPU':time.process_time()}),flush=True)
    report={'status':'COMPLETE_POSITIVE_LOW_TARGET_AUDIT_PASS' if unresolved is None else 'POSITIVE_NOT_PROVED',
      'required_jobs':len(jobs),'proved_jobs':proofs,'queries':queries,'full_floor_refinements':refined,
      'unresolved':unresolved,'new_finite_tests':0,'completed_semantic_checks_replayed':0,'M3_complete':False}
    write('audit_positive.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_positive_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
