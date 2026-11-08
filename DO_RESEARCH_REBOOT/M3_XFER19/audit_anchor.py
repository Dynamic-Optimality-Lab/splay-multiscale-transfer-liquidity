"""Independent universal signed audit of the explicit anchor correction.

No function fitting or finite population/mask tests. Every QF check
refutes a UNIVERSALLY quantified source-production/mask statement.
Completed UNSAT statements stream to an append-only checkpoint.
"""
import json,sys,time,itertools
from pathlib import Path
import z3
from symbolic_prefix_v2 import prefix,PATHS
from universal_grammar_v2 import build
from target_floor import lower_floor as cheap_floor,N,opp,opposite_alpha
from complete_floor import lower_floor as full_floor
from compatibility import source_compatible
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    start=time.process_time();r,x=z3.Ints('oldRoot newRoot')
    rootpos={(0,):2,(1,):1,(0,0):6,(0,1):2,(1,0):1,(1,1):3}
    generic=[];queries=0
    for p in PATHS:
        u=prefix(p,r,x,'anchorGeneric'+''.join(map(str,p)))
        s=z3.Solver();s.set(timeout=10000)
        s.add(*u['constraints'],r>=0,r<9,x>=0,x<9,r!=x,
          z3.Or(u['target'][0]!=x,u['target'][rootpos[p]]!=r,
            *(u['target'][j]==x for j in range(1,7))))
        v=s.check();queries+=1;assert v==z3.unsat,('GENERIC_H1_ANCHOR',p,str(v))
        generic.append({'word':p,'old_root_observation':rootpos[p],'no_nonroot_new_root_observation':True})
    write('anchor_generic_certificate.json',{'status':'UNIVERSAL_H1_NO_DUPLICATE_AND_OLD_ROOT_ANCHOR_PASS',
      'proofs':generic,'new_symbolic_queries':queries,'all_original_masks_signatures_and_private_blocks_free':True,
      'generic_zero_coverage_for_critical_core_table':'PROVED','signed_safety_not_yet_assumed':True})
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ker=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    ts=[freeze(q['tree']) for q in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[q['psi'] for q in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination']
    anchors={};critical={}
    for i,t in enumerate(ts):
        if psi[i]==0:continue
        for y in range(9):
            j=nx[i][y]
            if dd[i][y] not in (4,5) or psi[i]<=psi[j]:continue
            critical.setdefault((t[0],y,j,psi[i]),[]).append(i)
            anchors.setdefault(j,{})[t[0]]=max(anchors.get(j,{}).get(t[0],0),psi[i])
    assert len(critical)==378 and len(anchors)==303
    m=[z3.Bool('mark_'+str(k)) for k in range(9)]
    legal=z3.PbEq([(v,1) for v in m],5)
    proto=tuple(z3.Ints('alpha_L alpha_R alpha_LL alpha_LR alpha_RL alpha_RR'))
    T=N(2,N(0,None,N(1)),N(5,N(3,None,N(4)),N(6,None,N(7,None,N(8)))))
    cache={}
    def correction(i,a):
        root=ts[i][0]
        if i not in anchors:return z3.IntVal(0)
        no_dup=z3.And(*(a[j]!=root for j in range(1,7)))
        one=[];two=[]
        for old,k in anchors[i].items():
            pos=(1,3) if old<root else (2,6)
            guard=z3.And(m[old],z3.Or(*(a[j]==old for j in pos)))
            one.append(guard)
            if k==2:two.append(guard)
        return z3.If(no_dup,z3.If(z3.Or(*two),2,z3.If(z3.Or(*one),1,0)),0)
    def lower(i,a,full=False):
        key=(i,full)
        if key not in cache:
            t=ts[i];b=(z3.IntVal(t[0]),)+proto
            margins=[2-dd[i][y]//2+psi[nx[i][y]] for y in range(9)]
            vals=[]
            for k in (1,2):
                q=(full_floor if full else cheap_floor)(t,b,m,psi[i],margins,k)
                q=z3.Or(q,z3.Not(source_compatible(b)))
                if k==1:
                    if t==T:q=z3.Or(q,z3.And(z3.Not(m[4]),b[2]==4,b[6]==8))
                    if opp(t)==T:
                        bm=opposite_alpha(b);q=z3.Or(q,z3.And(z3.Not(m[4]),bm[2]==4,bm[6]==8))
                vals.append(z3.simplify(q))
            cache[key]=z3.simplify(z3.If(vals[1],2,z3.If(vals[0],1,0)))
        return z3.simplify(z3.substitute(cache[key],*((v,a[j+1]) for j,v in enumerate(proto))))
    maxR={i:max(v.values()) for i,v in anchors.items()}
    jobs=[];range_omitted=0
    for i in sorted(anchors):
        root=ts[i][0]
        for y in range(9):
            j=nx[i][y];w=2-dd[i][y]//2
            if w+psi[j]>=maxR[i]:range_omitted+=1;continue
            for p in PATHS:
                if p[0]==int(y>root):jobs.append((None,(p,),i,y,j,w))
    mirror=[ids[opp(t)] for t in ts]
    for q in ker['rows']:
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        for h,i,y,j in [(0,q['entry_core'],q['target'],q['exit_core']),
                        (9,mirror[q['entry_core']],8-q['target'],mirror[q['exit_core']])]:
            if i not in anchors:continue
            w=q['w']
            if w+psi[j]>=maxR[i]:range_omitted+=1;continue
            for p in PATHS:
                if p[0]!=int(h==9):continue
                for p2 in PATHS:
                    if p2[0]==int(h==0):jobs.append((h,(p,p2),i,y,j,w))
    assert len(jobs)<2000000
    completed=0;unresolved=None;refinements=0
    with (BASE/'anchor_signed_checkpoints.jsonl').open('x',encoding='utf-8') as checkpoint:
        for number,(h,word,i,y,j,w) in enumerate(jobs):
            if time.process_time()>=CAP-5:
                unresolved={'kind':'AUDIT_CPU_CAP','unfinished_job':number};break
            u=build(word,ts[i][0],y,h,'signed'+str(number))
            static=z3.And(legal,m[ts[i][0]],m[y],*u['constraints'])
            a,b=u['source'],u['target'];R=correction(i,a);Rt=correction(j,b)
            for full in (False,True):
                Li=lower(i,a,full);Lj=lower(j,b,full);target=z3.If(Lj>=Rt,Lj,Rt)
                sol=z3.Solver();sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-3)))))
                sol.add(static,R>Li,w+target<R)
                result=sol.check();queries+=1
                if result==z3.unsat:break
                if not full and result==z3.sat:refinements+=1;continue
                unresolved={'kind':'SYMBOLIC_SIGNED_SAFETY_COUNTERMODEL' if result==z3.sat else 'SMT_UNKNOWN',
                  'job':number,'helper':h,'word':word,'source_core':i,'target_key':y,'destination_core':j,'weight':w,
                  'B_source':bank['nodes'][i]['tree'],'B_destination':bank['nodes'][j]['tree'],
                  'original_negative_cycle_claimed':False}
                if result==z3.sat:
                    model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long()
                    unresolved.update({'source_alpha':[val(v) for v in a],'target_alpha':[val(v) for v in b],
                      'marked_keys':[k for k,v in enumerate(m) if z3.is_true(model.eval(v,model_completion=True))],
                      'anchor_source':val(R),'anchor_target':val(Rt),'old_floor_source':val(Li),'old_floor_target':val(Lj),
                      'actual_new_residual_with_translated_floor':w+max(val(Lj),val(Rt))-max(val(Li),val(R)),
                      'protected_types':[[list(p),val(v)] for p,v in sorted(u.get('types',{}).items())]})
                else:unresolved['reason']=sol.reason_unknown()
                with (BASE/'anchor_unresolved.smt2').open('x',encoding='utf-8') as f:f.write(sol.to_smt2())
                break
            if unresolved:break
            checkpoint.write(json.dumps({'job':number,'helper':h,'word':word,'source_core':i,'target':y,
              'destination_core':j,'weight':w,'proof':'UNIVERSAL_UNSAT','full_floor_refinement':full})+'\n');checkpoint.flush()
            completed+=1
            if completed%100==0:print(json.dumps({'universal_jobs_proved':completed,'of':len(jobs),'CPU':time.process_time()}),flush=True)
    report={'status':'COMPLETE_ANCHOR_SIGNED_AUDIT_PASS_PENDING_PROVENANCE' if unresolved is None else 'ANCHOR_SIGNED_SAFETY_NOT_PROVED',
      'generic_zero_target_coverage':'PROVED','signed_jobs_required':len(jobs),'signed_jobs_proved':completed,
      'new_symbolic_queries':queries,'cheap_floor_refinements':refinements,'range_floor_omissions':range_omitted,
      'unresolved':unresolved,'new_finite_population_or_mask_tests':0,'completed_semantic_checks_replayed':0,
      'new_original_root_evaluations':0,'Step4_complete':False}
    write('audit_anchor.json',report);print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:
        error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_anchor_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
