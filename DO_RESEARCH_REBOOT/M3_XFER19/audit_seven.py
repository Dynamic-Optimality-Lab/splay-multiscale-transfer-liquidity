"""Universal signed audit of a simultaneous one-credit constructor lemma."""
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
    m=[z3.Bool('seven_mark'+str(k)) for k in range(9)]
    proto=tuple(z3.Ints('seven_L seven_R seven_LL seven_LR seven_RL seven_RR'));cache={}
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
    cores=sorted({ids[t] for t in REGIONS}|{ids[opp(t)] for t in REGIONS})
    proofs=[];unresolved=None;queries=0
    for i in cores:
        if psi[i]>=1:continue
        for x in range(9):
            j=nx[i][x];w=2-dd[i][x]//2
            if w>=1 or w+psi[j]>=1:continue
            for p in PATHS:
                if p[0]!=int(x>ts[i][0]):continue
                assert time.process_time()<CAP-3
                u=prefix(p,ts[i][0],x,'seven'+str(queries));a,b=u['source'],u['target']
                sol=z3.Solver();sol.set(timeout=min(10000,int(1000*(CAP-time.process_time()-2))))
                need=1-w
                paid=lower(j,b,need) if need<=2 else z3.BoolVal(False)
                if need==1:paid=z3.Or(paid,seven_one(ts[j],b))
                sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[ts[i][0]],m[x],
                  seven_one(ts[i],a),z3.Not(lower(i,a,1)),z3.Not(paid))
                result=sol.check();queries+=1
                if result!=z3.unsat:
                    unresolved={'i':i,'x':x,'j':j,'w':w,'word':p,'result':str(result),
                      'B_source':ts[i],'B_target':ts[j]}
                    if result==z3.sat:
                        model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                        unresolved.update({'source_alpha':[value(v) for v in a],'target_alpha':[value(v) for v in b],
                          'mask':[k for k in range(9) if z3.is_true(model.eval(m[k],model_completion=True))]})
                    break
                proofs.append({'source':i,'target':x,'destination':j,'weight':w,'word':p,'result':'UNIVERSAL_UNSAT'})
            if unresolved:break
        if unresolved:break
    write('audit_seven.json',{'status':'UNIVERSAL_SEVEN_ANCHOR_FAMILY_PASS' if unresolved is None else 'FAMILY_NOT_PROVED',
      'new_universal_queries':queries,'proofs':proofs,'unresolved':unresolved,'new_finite_tests':0,
      'completed_checks_replayed':0,'Step4_complete':False})
    print(json.dumps({'queries':queries,'proved':len(proofs),'unresolved':unresolved}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_seven_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
