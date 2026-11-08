"""Universal signed closure of both anchor levels, no population tests."""
import json,sys,time
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix_v2 import PATHS
from baseline19 import floor
from target_floor import opp
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    assert json.loads((BASE/'audit_seven_independent.json').read_text())['status']=='INDEPENDENT_WHOLE_UNION_ONE_CREDIT_AUDIT_PASS'
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ker=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    ts=[freeze(r['tree']) for r in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[r['psi'] for r in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination']
    anchors={}
    for i,t in enumerate(ts):
        if psi[i]==0:continue
        for y in range(9):
            j=nx[i][y]
            if dd[i][y] in (4,5) and psi[i]>psi[j]:
                anchors.setdefault(j,{})[t[0]]=max(anchors.get(j,{}).get(t[0],0),psi[i])
    assert len(anchors)==303
    m=[z3.Bool('ac_mark'+str(k)) for k in range(9)]
    proto=tuple(z3.Ints('ac_L ac_R ac_LL ac_LR ac_RL ac_RR'));cache={}
    def L(i,a,k):
        if (i,k) not in cache:
            t=ts[i];b=(z3.IntVal(t[0]),)+proto
            margins=[2-dd[i][y]//2+psi[nx[i][y]] for y in range(9)]
            cache[i,k]=z3.simplify(floor(i,t,b,m,psi[i],margins,k))
        return z3.simplify(z3.substitute(cache[i,k],*((v,a[j+1]) for j,v in enumerate(proto))))
    clauses=[];bycore={};known=set()
    def add(c):
        key=json.dumps(c,sort_keys=True)
        if key in known:return False
        known.add(key);bycore.setdefault(c['core'],[]).append(c);clauses.append(c);return True
    for i in sorted(anchors):
        for k in range(1,max(anchors[i].values())+1):add({'core':i,'level':k,'kind':'anchor'})
    def C(c,a):
        i=c['core'];k=c['level']
        if c['kind']=='anchor':
            no=z3.And(*(a[p]!=ts[i][0] for p in range(1,7)))
            return z3.And(no,z3.Or(*(z3.And(m[r],z3.Or(*(a[p]==r for p in ((1,3) if r<ts[i][0] else (2,6)))))
              for r,v in anchors[i].items() if v>=k)))
        return z3.And(*(a[p]==v for p,v in c['score_equalities']),*(m[r] for r in c['marks']))
    def G(i,a,k):return z3.Or(*(C(c,a) for c in bycore.get(i,[]) if c['level']>=k))
    mirror=[ids[opp(t)] for t in ts];helpers={}
    for row in ker['rows']:
        if not row['gap0_childless_at_exit'] or row['w']>=2:continue
        for h,i,x,j in ((0,row['entry_core'],row['target'],row['exit_core']),
                       (9,mirror[row['entry_core']],8-row['target'],mirror[row['exit_core']])):
            helpers.setdefault(i,[]).append((h,x,j,row['w']))
    cached={}
    for f in BASE.glob('anchor_signed*checkpoints.jsonl'):
        for line in f.read_text().splitlines():
            r=json.loads(line)
            key=(r['helper'],tuple(tuple(p) for p in r['word']),r['source_core'],r['target'],r['destination_core'],r['weight'])
            cached[key]=True
    queries=proved=created=reused=0;idx=0;unresolved=None
    with (BASE/'anchor_closure_checkpoints.jsonl').open('x',encoding='utf-8') as checkpoint:
        while idx<len(clauses) and unresolved is None:
            c=clauses[idx];i=c['core'];k=c['level'];idx+=1
            if psi[i]>=k:continue
            jobs=[]
            for x in range(9):
                j=nx[i][x];w=2-dd[i][x]//2
                if w+psi[j]>=k or w>=k:continue
                for p in PATHS:
                    if p[0]==int(x>ts[i][0]):jobs.append((None,(p,),x,j,w))
            if k==2:
                for h,x,j,w in helpers.get(i,[]):
                    if w+psi[j]>=k:continue
                    for p in PATHS:
                        if p[0]!=int(h==9):continue
                        for p2 in PATHS:
                            if p2[0]==int(h==0):jobs.append((h,(p,p2),x,j,w))
            for h,word,x,j,w in jobs:
                key=(h,word,i,x,j,w)
                if c['kind']=='anchor' and key in cached:reused+=1;continue
                if time.process_time()>=CAP-5:
                    unresolved={'kind':'CAP','unfinished_clause':idx-1,'job':key};break
                u=build(word,ts[i][0],x,h,'ac'+str(queries));a,b=u['source'],u['target'];need=k-w
                while True:
                    paid=z3.Or(L(j,b,need),G(j,b,need)) if need<=2 else z3.BoolVal(False)
                    sol=z3.Solver();sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-3)))))
                    sol.add(*u['constraints'],z3.PbEq([(v,1) for v in m],5),m[ts[i][0]],m[x],
                      C(c,a),z3.Not(L(i,a,k)),z3.Not(paid))
                    result=sol.check();queries+=1
                    if result==z3.unsat:
                        checkpoint.write(json.dumps({'clause':idx-1,'helper':h,'word':word,'source_core':i,
                          'target':x,'destination_core':j,'weight':w,'level':k,'proof':'UNIVERSAL_UNSAT'})+'\n')
                        checkpoint.flush();proved+=1;break
                    if result!=z3.sat or need>2 or time.process_time()>=CAP-5:
                        unresolved={'kind':'RANGE_OBSTRUCTION' if need>2 else 'UNKNOWN_OR_CAP','clause':idx-1,
                          'source_core':i,'target':x,'destination_core':j,'helper':h,'word':word,'weight':w,'level':k,
                          'required_target':need,'result':str(result),'B_source':ts[i],'B_target':ts[j]}
                        if result==z3.sat:
                            model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                            unresolved.update({'source_alpha':[value(v) for v in a],'target_alpha':[value(v) for v in b],
                              'mask':[r for r in range(9) if z3.is_true(model.eval(m[r],model_completion=True))]})
                        break
                    model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                    source=[value(v) for v in a];target=[value(v) for v in b]
                    if c['kind']=='anchor':
                        carriers=[r for r,v in anchors[i].items() if v>=k and z3.is_true(model.eval(m[r],model_completion=True))
                          and any(source[p]==r for p in ((1,3) if r<ts[i][0] else (2,6)))]
                        assert carriers;marks={carriers[0]}
                    else:marks=set(c['marks'])
                    marks.add(ts[i][0])
                    nc={'core':j,'level':need,'kind':'score_cube','marks':sorted(marks),
                      'score_equalities':[(p,v) for p,v in enumerate(target) if p and v<9]}
                    assert add(nc),'duplicate does not cover its generating model'
                    created+=1
                    assert queries<2000000 and len(clauses)<2000000
                if unresolved:break
            if idx%20==0:print(json.dumps({'clauses_audited':idx,'pending':len(clauses)-idx,
              'queries':queries,'CPU':time.process_time()}),flush=True)
    report={'status':'COMPLETE_SYMBOLIC_ANCHOR_CLOSURE_PENDING_INDEPENDENT_AUDIT' if unresolved is None else 'ANCHOR_CLOSURE_NOT_PROVED',
      'initial_anchor_core_count':303,'clauses':clauses,'clauses_audited':idx,'new_score_cubes':created,
      'new_universal_queries':queries,'universal_obligations_proved':proved,'old_anchor_checks_transported_not_replayed':reused,
      'unresolved':unresolved,'new_finite_population_or_mask_tests':0,'Step4_complete':False}
    write('audit_anchor_closure.json',report);print(json.dumps({k:v for k,v in report.items() if k!='clauses'},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_anchor_closure_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
