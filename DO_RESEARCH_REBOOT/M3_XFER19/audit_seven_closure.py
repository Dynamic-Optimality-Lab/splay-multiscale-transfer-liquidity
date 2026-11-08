"""Universal symbolic one-credit closure; every model-suggested clause provisional."""
import json,sys,time
from pathlib import Path
import z3
from symbolic_prefix_v2 import prefix,PATHS
from complete_floor import lower_floor
from target_floor import opp,N,opposite_alpha
from compatibility import source_compatible
from paired_floors import paired_one
from lower_return_floors import lower_return_one
from seven_anchor import REGIONS,seven_one
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ts=[freeze(r['tree']) for r in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[r['psi'] for r in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination']
    m=[z3.Bool('closure_mark'+str(k)) for k in range(9)]
    proto=tuple(z3.Ints('closure_L closure_R closure_LL closure_LR closure_RL closure_RR'));cache={}
    T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(6,None,N(7,None,N(8)))))
    def lower(i,a,k):
        key=i,k
        if key not in cache:
            t=ts[i];b=(z3.IntVal(t[0]),)+proto
            margins=[2-dd[i][y]//2+psi[nx[i][y]] for y in range(9)]
            q=z3.Or(lower_floor(t,b,m,psi[i],margins,k),z3.Not(source_compatible(b)))
            if k==1:
                if t==T:q=z3.Or(q,z3.And(z3.Not(m[4]),b[2]==4,b[6]==8))
                if opp(t)==T:
                    bm=opposite_alpha(b);q=z3.Or(q,z3.And(z3.Not(m[4]),bm[2]==4,bm[6]==8))
                q=z3.Or(q,paired_one(t,b),lower_return_one(t,b))
            cache[key]=z3.simplify(q)
        return z3.simplify(z3.substitute(cache[key],*((v,a[j+1]) for j,v in enumerate(proto))))
    # The canonical family plus its ACTUAL opposite, with the corresponding mark.
    initial=[]
    for t in REGIONS:
        initial.append({'core':ids[t],'kind':'initial','marks':[7]})
        initial.append({'core':ids[opp(t)],'kind':'initial_opposite','marks':[1]})
    clauses=[];known=set();bycore={}
    def add(c):
        key=json.dumps(c,sort_keys=True)
        if key in known:return False
        known.add(key);bycore.setdefault(c['core'],[]).append(c);clauses.append(c);return True
    for c in initial:add(c)
    def clause(c,a):
        if c['kind']=='initial':g=seven_one(ts[c['core']],a)
        elif c['kind']=='initial_opposite':g=seven_one(ts[c['core']],a)
        else:g=z3.And(*(a[int(p)]==v for p,v in c['score_equalities']))
        return z3.And(g,*(m[k] for k in c['marks']))
    def G(i,a):return z3.Or(*(clause(c,a) for c in bycore.get(i,[])))
    old=json.loads((BASE/'audit_seven.json').read_text())
    oldjobs={(p['source'],p['target'],tuple(p['word'])) for p in old['proofs']}
    checked=queries=created=0;idx=0;unresolved=None;reused=0
    with (BASE/'seven_closure_checkpoints.jsonl').open('x',encoding='utf-8') as checkpoint:
        while idx<len(clauses) and unresolved is None:
            c=clauses[idx];i=c['core'];idx+=1
            if psi[i]>=1:continue
            for x in range(9):
                j=nx[i][x];w=2-dd[i][x]//2
                if w>=1 or w+psi[j]>=1:continue
                for p in PATHS:
                    if p[0]!=int(x>ts[i][0]):continue
                    if c['kind'].startswith('initial') and (i,x,p) in oldjobs:
                        reused+=1;continue
                    if time.process_time()>=CAP-5:
                        unresolved={'kind':'CAP','clause':idx-1,'x':x,'word':p};break
                    u=prefix(p,ts[i][0],x,'close'+str(queries));a,b=u['source'],u['target']
                    while True:
                        need=1-w
                        paid=lower(j,b,need) if need<=2 else z3.BoolVal(False)
                        if need==1:paid=z3.Or(paid,G(j,b))
                        sol=z3.Solver();sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-3)))))
                        sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[ts[i][0]],m[x],
                          clause(c,a),z3.Not(lower(i,a,1)),z3.Not(paid))
                        result=sol.check();queries+=1
                        if result==z3.unsat:
                            row={'clause':idx-1,'source':i,'target':x,'destination':j,'weight':w,'word':p,'result':'UNIVERSAL_UNSAT'}
                            checkpoint.write(json.dumps(row)+'\n');checkpoint.flush();checked+=1;break
                        if result!=z3.sat or w<0 or time.process_time()>=CAP-5:
                            unresolved={'kind':'UNPAID_NEGATIVE' if w<0 else 'UNKNOWN_OR_CAP','clause':idx-1,
                              'source':i,'target':x,'destination':j,'w':w,'word':p,'result':str(result),
                              'B_source':ts[i],'B_target':ts[j]}
                            if result==z3.sat:
                                model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                                unresolved.update({'source_alpha':[value(v) for v in a],'target_alpha':[value(v) for v in b],
                                  'mask':[k for k in range(9) if z3.is_true(model.eval(m[k],model_completion=True))]})
                            break
                        model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                        target=[value(v) for v in b]
                        nc={'core':j,'kind':'score_cube','marks':sorted(set(c['marks'])|{ts[i][0]}),
                          'score_equalities':[(p,v) for p,v in enumerate(target) if p and v<9]}
                        assert add(nc),'duplicate cannot pay its generating model'
                        created+=1
                        assert queries<2000000 and len(clauses)<2000000
                    if unresolved:break
                if unresolved:break
            if idx%20==0:print(json.dumps({'audited_clauses':idx,'pending':len(clauses)-idx,'queries':queries,'CPU':time.process_time()}),flush=True)
    report={'status':'UNIVERSAL_ONE_CREDIT_CLOSURE_PASS_PENDING_INDEPENDENT_AUDIT' if unresolved is None else 'CLOSURE_NOT_PROVED',
      'clauses':clauses,'audited_clauses':idx,'new_clauses':created,'new_universal_queries':queries,
      'universal_obligations_proved':checked,'completed_obligations_transported_not_replayed':reused,
      'unresolved':unresolved,'new_finite_population_or_mask_tests':0,'Step4_complete':False}
    write('audit_seven_closure.json',report);print(json.dumps({k:v for k,v in report.items() if k!='clauses'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_seven_closure_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
