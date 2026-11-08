"""Independent whole-union signed proof, with shared symbolic expressions."""
import json,sys,time,collections
from pathlib import Path
import z3
from universal_grammar_v2 import build
from symbolic_prefix_v2 import prefix,PATHS
from baseline19 import floor
from target_floor import opp
from complete_floor import hidden_min
BASE=Path(__file__).resolve().parent;CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def freeze(t):return None if t is None else (t[0],freeze(t[1]),freeze(t[2]))
def main():
    assert json.loads((BASE/'audit_normalization_v2.json').read_text())['status']=='UNIVERSAL_CHEAP_TARGET_AND_MAXIMAL_LEVEL_REDUCTION_PASS'
    old=json.loads((BASE/'audit_anchor_union.json').read_text())
    bank=json.loads((BASE.parent/'M3_LDR01/negative_run_census.json').read_text())
    tab=json.loads((BASE.parent/'M3_H1F01/cheap_census.json').read_text())
    ker=json.loads((BASE.parent/'M3_H2R01/fringe_kernel_certificate.json').read_text())
    ts=[freeze(r['tree']) for r in bank['nodes']];ids={t:i for i,t in enumerate(ts)}
    psi=[r['psi'] for r in bank['nodes']];dd=tab['B_depth'];nx=tab['B_destination']
    anchors={}
    for i,t in enumerate(ts):
        if not psi[i]:continue
        for y in range(9):
            j=nx[i][y]
            if dd[i][y] in (4,5) and psi[i]>psi[j]:
                anchors.setdefault(j,{})[t[0]]=max(anchors.get(j,{}).get(t[0],0),psi[i])
    assert len(anchors)==303
    m=[z3.Bool('union_mark'+str(k)) for k in range(9)]
    legal=z3.PbEq([(v,1) for v in m],5)
    proto=tuple(z3.Ints('union_L union_R union_LL union_LR union_RL union_RR'))
    lp={};le={};up={};ue={};cp={};grammar={};jobs={};pending={};queue=collections.deque();cheap_cache={};done={}
    def canonical(v):return tuple(canonical(q) for q in v) if isinstance(v,list) else v
    for line in (BASE/'anchor_closure_checkpoints.jsonl').read_text().splitlines():
        r=json.loads(line);key=(r['source_core'],r['level'],r['helper'],canonical(r['word']),r['target'],r['destination_core'],r['weight'])
        done.setdefault(key,set()).add(r['clause'])
    for line in (BASE/'anchor_union_checkpoints.jsonl').read_text().splitlines():
        r=json.loads(line);done.setdefault(canonical(r['job']),set()).update(r['source_clause_ids'])
    clauses=[];bycore={};known=set();version={}
    def subst(expr,a):return z3.substitute(expr,*((v,a[j+1]) for j,v in enumerate(proto)))
    def Cproto(cid):
        if cid not in cp:
            c=clauses[cid];i=c['core'];k=c['level'];a=(z3.IntVal(ts[i][0]),)+proto
            if c['kind']=='anchor':
                q=z3.And(*(a[p]!=ts[i][0] for p in range(1,7)),z3.Or(*(z3.And(m[r],
                  z3.Or(*(a[p]==r for p in ((1,3) if r<ts[i][0] else (2,6)))))
                  for r,v in anchors[i].items() if v>=k)))
            else:q=z3.And(*(a[p]==v for p,v in c['score_equalities']),*(m[r] for r in c['marks']))
            cp[cid]=q
        return cp[cid]
    def Lproto(i,k):
        if (i,k) not in lp:
            a=(z3.IntVal(ts[i][0]),)+proto
            margins=[2-dd[i][y]//2+psi[nx[i][y]] for y in range(9)]
            lp[i,k]=z3.simplify(floor(i,ts[i],a,m,psi[i],margins,k))
        return lp[i,k]
    def Cheap(i,k):
        if (i,k) not in cheap_cache:
            t=ts[i];a=(z3.IntVal(t[0]),)+proto
            if psi[i]>=k:q=z3.BoolVal(True)
            else:
                bad=[x for x in range(9) if x!=t[0] and 2-dd[i][x]//2+psi[nx[i][x]]<k]
                q=z3.And(*(z3.Implies(m[x],z3.And(*(a[p]!=x for p in range(1,7)))) for x in bad))
                if k==2:q=z3.And(q,z3.Not(z3.Or(hidden_min(t,a),hidden_min(opp(t),__import__('target_floor').opposite_alpha(a)))))
            cheap_cache[i,k]=z3.simplify(q)
        return cheap_cache[i,k]
    def Gproto(i,k):
        key=i,k,version.get(i,0)
        if key not in up:up[key]=z3.Or(*(Cproto(cid) for cid in bycore.get(i,[]) if clauses[cid]['level']>=k))
        return up[key]
    mirror=[ids[opp(t)] for t in ts];helpers={}
    for row in ker['rows']:
        if not row['gap0_childless_at_exit'] or row['w']>=2:continue
        for h,i,x,j in ((0,row['entry_core'],row['target'],row['exit_core']),
                       (9,mirror[row['entry_core']],8-row['target'],mirror[row['exit_core']])):
            helpers.setdefault(i,set()).add((h,x,j,row['w']))
    def J(i,k):
        if (i,k) in jobs:return jobs[i,k]
        out=[]
        if psi[i]<k:
            for x in range(9):
                j=nx[i][x];w=2-dd[i][x]//2
                if w+psi[j]>=k or w>=k:continue
                for p in PATHS:
                    if p[0]==int(x>ts[i][0]):out.append((i,k,None,(p,),x,j,w))
            if k==2:
                for h,x,j,w in helpers.get(i,set()):
                    if w+psi[j]>=k:continue
                    for p in PATHS:
                        if p[0]!=int(h==9):continue
                        for p2 in PATHS:
                            if p2[0]==int(h==0):out.append((i,k,h,(p,p2),x,j,w))
        jobs[i,k]=sorted(set(out),key=lambda q:(q[-1],str(q)))
        return jobs[i,k]
    def add(c):
        key=json.dumps(c,sort_keys=True)
        if key in known:return None
        known.add(key);cid=len(clauses);clauses.append(c);i=c['core'];bycore.setdefault(i,[]).append(cid)
        version[i]=version.get(i,0)+1
        for key in J(i,c['level']):
            if cid in done.get(key,set()):continue
            if key not in pending:pending[key]=set();queue.append(key)
            pending[key].add(cid)
        return cid
    for c in old['clauses']:add(c)
    initial=len(clauses);queries=proved=new=0;unresolved=None;required=0
    with (BASE/'maximal_new_clauses.jsonl').open('x',encoding='utf-8') as suggested, (BASE/'maximal_checkpoints.jsonl').open('x',encoding='utf-8') as cert:
        while queue and unresolved is None:
            key=queue.popleft();cids=sorted(pending.pop(key));i,k,h,word,x,j,w=key
            if time.process_time()>=CAP-6:
                unresolved={'kind':'CAP','job':key,'source_clause_ids':cids};break
            gkey=i,h,word,x
            if gkey not in grammar:
                name='union'+str(len(grammar))
                u=prefix(word[0],ts[i][0],x,name) if h is None else build(word,ts[i][0],x,h,name)
                a,b=u['source'],u['target'];static=z3.And(*u['constraints'],legal,m[ts[i][0]],m[x])
                grammar[gkey]=(a,b,static)
            a,b,static=grammar[gkey]
            if (gkey,k,'source') not in le:le[gkey,k,'source']=z3.simplify(subst(Cheap(i,k),a))
            need=k-w
            if need<=2 and (gkey,need,'target') not in le:
                le[gkey,need,'target']=z3.simplify(subst(Cheap(j,need),b))
            source=z3.Or(*(subst(Cproto(cid),a) for cid in cids))
            sol=z3.Solver();sol.add(static,source,z3.Not(le[gkey,k,'source']),*(a[p]!=ts[i][0] for p in range(1,7)))
            if k==1:sol.add(z3.Not(subst(Gproto(i,2),a)))
            while True:
                vkey=gkey,need,version.get(j,0)
                if need<=2:
                    if vkey not in ue:ue[vkey]=subst(Gproto(j,need),b)
                    paid=z3.Or(le[gkey,need,'target'],ue[vkey])
                else:paid=z3.BoolVal(False)
                sol.push();sol.add(z3.Not(paid));sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-4)))))
                r=sol.check();queries+=1;refined=False
                if r==z3.sat:
                    if (gkey,k,'full_source') not in le:le[gkey,k,'full_source']=z3.simplify(subst(Lproto(i,k),a))
                    sol.add(z3.Not(le[gkey,k,'full_source']))
                    if need<=2:
                        if (gkey,need,'full_target') not in le:le[gkey,need,'full_target']=z3.simplify(subst(Lproto(j,need),b))
                        sol.add(z3.Not(le[gkey,need,'full_target']))
                    r=sol.check();queries+=1;refined=True
                if r==z3.unsat:
                    sol.pop();proved+=1;required+=len(cids)
                    cert.write(json.dumps({'job':key,'source_clause_ids':cids,'result':'UNIVERSAL_UNSAT','full_baseline_refinement':refined,'normalized_maximal_source':True})+'\n');cert.flush();break
                if r!=z3.sat or need>2 or time.process_time()>=CAP-6:
                    unresolved={'kind':'RANGE_OBSTRUCTION' if need>2 else 'UNKNOWN_OR_CAP','job':key,
                      'source_clause_ids':cids,'required_target':need,'result':str(r),'B_source':ts[i],'B_target':ts[j]}
                    if r==z3.sat:
                        model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                        unresolved.update({'source_alpha':[value(v) for v in a],'target_alpha':[value(v) for v in b],
                          'mask':[q for q in range(9) if z3.is_true(model.eval(m[q],model_completion=True))],
                          'active_source_clause_ids':[cid for cid in cids if z3.is_true(model.eval(subst(Cproto(cid),a),model_completion=True))]})
                    sol.pop();break
                model=sol.model();value=lambda v:model.eval(v,model_completion=True).as_long()
                source_values=[value(v) for v in a];target=[value(v) for v in b]
                active=next(cid for cid in cids if z3.is_true(model.eval(subst(Cproto(cid),a),model_completion=True)))
                c=clauses[active]
                if c['kind']=='anchor':
                    carrier=next(q for q,v in anchors[i].items() if v>=k and z3.is_true(model.eval(m[q],model_completion=True))
                      and any(source_values[p]==q for p in ((1,3) if q<ts[i][0] else (2,6))))
                    marks={carrier}
                else:marks=set(c['marks'])
                marks.add(ts[i][0]);sol.pop()
                nc={'core':j,'level':need,'kind':'score_cube','marks':sorted(marks),
                  'score_equalities':[(p,v) for p,v in enumerate(target) if p and v<9]}
                cid=add(nc);assert cid is not None,'duplicate fails its model'
                suggested.write(json.dumps({'clause_id':cid,'clause':nc,'from_clause':active,'job':key})+'\n');suggested.flush();new+=1
                assert len(clauses)<2000000 and queries<2000000
            if proved%100==0:print(json.dumps({'universal_union_jobs':proved,'pending_jobs':len(queue),
              'clauses':len(clauses),'queries':queries,'CPU':time.process_time()}),flush=True)
        write('audit_maximal.json',{'status':'COMPLETE_NORMALIZED_MAXIMAL_SIGNED_AUDIT_PASS' if unresolved is None else 'UNION_NOT_PROVED',
          'clauses':clauses,'initial_clauses':initial,'new_clauses':new,'queries':queries,'universal_union_jobs_proved':proved,
          'clause_job_obligations_proved':required,'pending_jobs':len(queue),'unresolved':unresolved,
          'new_finite_tests':0,'completed_checks_transported_not_replayed':sum(map(len,done.values())),'Step4_complete':False})
        print(json.dumps({'status':'PASS' if unresolved is None else 'NOT_PROVED','proved':proved,'pending':len(queue),
          'clauses':len(clauses),'unresolved':unresolved}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_maximal_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
