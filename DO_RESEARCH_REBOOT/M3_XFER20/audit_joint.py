"""Signed public clause completion over the sealed Step4 baseline."""
import json,sys,time,collections
import z3
from support import BASE,trees,ids,psi,depth,destination,opp,opposite_alpha,kernel,build,PATHS,gamma_words
from support import full_floor,capacity,correction,seed_two,necessary_two
from complete_floor import hidden_min
CAP=min(300,float(sys.argv[1]))
def write(n,o):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(o,f,indent=2)
def main():
    inv=json.loads((BASE/'positive_inventory.json').read_text());anchors={}
    assert json.loads((BASE/'audit_visibility.json').read_text())['status']=='UNIVERSAL_VISIBLE_TERMINAL_CAPACITY_EXCLUSION_PASS'
    old=json.loads((BASE/'audit_completion_v2.json').read_text())
    def canonical(v):return tuple(canonical(q) for q in v) if isinstance(v,list) else v
    done={}
    for line in (BASE/'completion_v2_checkpoints.jsonl').read_text().splitlines():
        q=json.loads(line);done.setdefault(canonical(q['job']),set()).update(q['source_clause_ids'])
    for i,x,j in inv['H1_critical_core_rows']:anchors.setdefault(j,set()).add(trees[i][0])
    m=[z3.Bool('completion_mark'+str(k)) for k in range(9)];legal=z3.PbEq([(v,1) for v in m],5)
    proto=tuple(z3.Ints('completion_L completion_R completion_LL completion_LR completion_RL completion_RR'))
    clauses=[];bycore={};known=set();version={};cp={};up={};ue={};cheap={};full={};expr={};gram={};jobs={};pending={};queue=collections.deque()
    def sub(e,a):return z3.substitute(e,*((v,a[j+1]) for j,v in enumerate(proto)))
    def C(cid):
        if cid not in cp:
            c=clauses[cid];i=c['core'];a=(z3.IntVal(trees[i][0]),)+proto
            if c['kind']=='positive_anchor':q=z3.Or(*(z3.And(m[r],z3.Or(*(a[p]==r for p in ((1,3) if r<trees[i][0] else (2,6))))) for r in anchors[i]))
            else:q=z3.And(*(a[p]==v for p,v in c['score_equalities']),*(m[r] for r in c['marks']))
            cp[cid]=q
        return cp[cid]
    def G(i,k):
        key=i,k,version.get(i,0)
        if key not in up:up[key]=z3.Or(*(C(cid) for cid in bycore.get(i,[]) if clauses[cid]['level']>=k))
        return up[key]
    def L(i,k,allfloors):
        cache=full if allfloors else cheap
        if (i,k) not in cache:
            a=(z3.IntVal(trees[i][0]),)+proto
            if allfloors:q=full_floor(i,a,m,k)
            else:
                q=capacity(i,a,m,k)
                if k==2:q=z3.And(q,z3.Not(z3.Or(hidden_min(trees[i],a),hidden_min(opp(trees[i]),opposite_alpha(a)))))
                q=z3.Or(z3.BoolVal(psi[i]>=k),q,correction(i,a,m,k))
            cache[i,k]=z3.simplify(q)
        return cache[i,k]
    mirror=[ids[opp(t)] for t in trees];helpers={}
    for q in kernel['rows']:
        if not q['gap0_childless_at_exit'] or q['w']>=2:continue
        i,x,j,w=q['entry_core'],q['target'],q['exit_core'],q['w']
        for h,i,x,j in ((0,i,x,j),(9,mirror[i],8-x,mirror[j])):helpers.setdefault(i,set()).add((h,x,j,w))
    def J(i,k):
        if (i,k) not in jobs:
            result=[]
            if psi[i]<k:
                for x in range(9):
                    j=destination[i][x];w=2-depth[i][x]//2
                    if w>=k or w+psi[j]>=k:continue
                    for p in PATHS:
                        if p[0]==int(x>trees[i][0]):result.append((i,k,None,(p,),x,j,w))
                if k==2:
                    for h,x,j,w in helpers.get(i,set()):
                        if w+psi[j]>=k:continue
                        assert x!=trees[i][0]
                        for word in gamma_words(trees[i][0],x,h):result.append((i,k,h,word,x,j,w))
            jobs[i,k]=sorted(set(result),key=lambda r:(r[-1],str(r)))
        return jobs[i,k]
    def add(c):
        key=json.dumps(c,sort_keys=True)
        if key in known:return None
        known.add(key);cid=len(clauses);clauses.append(c);i=c['core'];bycore.setdefault(i,[]).append(cid);version[i]=version.get(i,0)+1
        for key in J(i,c['level']):
            if cid in done.get(key,set()):continue
            if key not in pending:pending[key]=set();queue.append(key)
            pending[key].add(cid)
        return cid
    for c in old['clauses']:add(c)
    assert len(clauses)==len(old['clauses'])
    initial=len(clauses);queries=proved=new=obligations=0;unresolved=None
    gamma_jobs=[]
    for q in inv['Gamma1_gap0_critical_rows']:
        i,x,j=q['entry_core'],q['target'],q['exit_core']
        for h,i,x,j in ((0,i,x,j),(9,ids[opp(trees[i])],8-x,ids[opp(trees[j])])):
            for word in gamma_words(trees[i][0],x,h):gamma_jobs.append((i,x,j,h,word))
    gamma_saved=json.loads((BASE/'audit_gamma.json').read_text());gamma_index=gamma_saved['proved_jobs']
    for number,line in enumerate((BASE/'gamma_checkpoints.jsonl').read_text().splitlines()):
        q=json.loads(line);assert q['job']==number and q['proof']=='UNIVERSAL_UNSAT'
        assert canonical([q['source_core'],q['target_key'],q['destination_core'],q['helper'],q['word']])==gamma_jobs[number]
    assert number+1==gamma_index
    visible={((0,),(1,0)):4,((0,0),(1,)):1,((0,),(1,1)):2,((0,1),(1,1)):2}
    def statically_empty(i,x,h,word):
        minimum_word=word if h==0 else tuple(tuple(1-v for v in p) for p in word)
        return psi[i]<2 and minimum_word in visible and 2-depth[i][x]//2+psi[destination[i][x]]<2
    gamma_new=gamma_suggestions=0
    with (BASE/'joint_checkpoints.jsonl').open('x',encoding='utf-8') as cert, (BASE/'joint_suggestions.jsonl').open('x',encoding='utf-8') as suggestions, (BASE/'joint_gamma_checkpoints.jsonl').open('x',encoding='utf-8') as gc:
        while (queue or gamma_index<len(gamma_jobs)) and unresolved is None:
            if not queue:
                if time.process_time()>=CAP-6:unresolved={'kind':'CAP','Gamma1_job':gamma_index};break
                i,x,j,h,word=gamma_jobs[gamma_index]
                if statically_empty(i,x,h,word):
                    gc.write(json.dumps({'job':gamma_index,'source_core':i,'target_key':x,'destination_core':j,'helper':h,'word':word,'proof':'STATIC_VISIBLE_SEED_CAPACITY_CONTRADICTION'})+'\n');gc.flush();gamma_index+=1;gamma_new+=1;continue
                gkey=i,h,word,x
                if gkey not in gram:
                    u=build(word,trees[i][0],x,h,'completion'+str(len(gram)));a,b=u['source'],u['target']
                    gram[gkey]=(a,b,z3.And(*u['constraints'],legal,m[trees[i][0]],m[x]))
                a,b,static=gram[gkey]
                if (gkey,1,False,'t') not in expr:expr[gkey,1,False,'t']=z3.simplify(sub(L(j,1,False),b))
                sol=z3.Solver();sol.add(static,seed_two(i,a,m),necessary_two(i,a,m),z3.Not(z3.Or(hidden_min(trees[i],a),hidden_min(opp(trees[i]),opposite_alpha(a)))))
                vkey=gkey,1,version.get(j,0)
                if vkey not in ue:ue[vkey]=sub(G(j,1),b)
                sol.add(z3.Not(z3.Or(expr[gkey,1,False,'t'],ue[vkey])))
                sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-4)))))
                r=sol.check();queries+=1;refined=False
                if r==z3.sat:
                    if (gkey,1,True,'t') not in expr:expr[gkey,1,True,'t']=z3.simplify(sub(L(j,1,True),b))
                    sol.add(z3.Not(expr[gkey,1,True,'t']));r=sol.check();queries+=1;refined=True
                if r==z3.unsat:
                    gc.write(json.dumps({'job':gamma_index,'source_core':i,'target_key':x,'destination_core':j,'helper':h,'word':word,'proof':'UNIVERSAL_UNSAT','full_refinement':refined})+'\n');gc.flush();gamma_index+=1;gamma_new+=1;continue
                if r!=z3.sat or time.process_time()>=CAP-6:
                    unresolved={'kind':'GAMMA_UNKNOWN_OR_CAP','job':gamma_index,'result':str(r)};break
                model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long();bv=[val(v) for v in b]
                marks=[q for q in range(9) if z3.is_true(model.eval(m[q],model_completion=True))]
                assert len(marks)==5
                nc={'kind':'score_cube','core':j,'level':1,'marks':marks,'score_equalities':[(p,v) for p,v in enumerate(bv) if p and v<9]}
                cid=add(nc);assert cid is not None
                suggestions.write(json.dumps({'clause_id':cid,'clause':nc,'from_Gamma1_job':gamma_index})+'\n');suggestions.flush();new+=1;gamma_suggestions+=1
                assert queries<2000000 and len(clauses)<2000000
                continue
            key=queue.popleft();cids=sorted(pending.pop(key));i,k,h,word,x,j,w=key
            if time.process_time()>=CAP-6:unresolved={'kind':'CAP','job':key,'source_clause_ids':cids};break
            gkey=i,h,word,x
            if gkey not in gram:
                u=build(word,trees[i][0],x,h,'completion'+str(len(gram)));a,b=u['source'],u['target']
                gram[gkey]=(a,b,z3.And(*u['constraints'],legal,m[trees[i][0]],m[x]))
            a,b,static=gram[gkey];need=k-w
            if (gkey,k,False,'s') not in expr:expr[gkey,k,False,'s']=z3.simplify(sub(L(i,k,False),a))
            if need<=2 and (gkey,need,False,'t') not in expr:expr[gkey,need,False,'t']=z3.simplify(sub(L(j,need,False),b))
            sol=z3.Solver();sol.add(static,z3.Or(*(sub(C(cid),a) for cid in cids)),z3.Not(expr[gkey,k,False,'s']),*(a[p]!=trees[i][0] for p in range(1,7)))
            if k==1:sol.add(z3.Not(sub(G(i,2),a)))
            while True:
                vkey=gkey,need,version.get(j,0)
                if need<=2:
                    if vkey not in ue:ue[vkey]=sub(G(j,need),b)
                    paid=z3.Or(expr[gkey,need,False,'t'],ue[vkey])
                else:paid=z3.BoolVal(False)
                sol.push();sol.add(z3.Not(paid));sol.set(timeout=min(10000,max(1,int(1000*(CAP-time.process_time()-4)))))
                r=sol.check();queries+=1;refined=False
                if r==z3.sat:
                    if (gkey,k,True,'s') not in expr:expr[gkey,k,True,'s']=z3.simplify(sub(L(i,k,True),a))
                    sol.add(z3.Not(expr[gkey,k,True,'s']))
                    if need<=2:
                        if (gkey,need,True,'t') not in expr:expr[gkey,need,True,'t']=z3.simplify(sub(L(j,need,True),b))
                        sol.add(z3.Not(expr[gkey,need,True,'t']))
                    r=sol.check();queries+=1;refined=True
                if r==z3.unsat:
                    sol.pop();cert.write(json.dumps({'job':key,'source_clause_ids':cids,'proof':'UNIVERSAL_UNSAT','full_refinement':refined})+'\n');cert.flush();proved+=1;obligations+=len(cids);break
                if r!=z3.sat or need>2 or time.process_time()>=CAP-6:
                    unresolved={'kind':'RANGE_OBSTRUCTION' if need>2 else 'UNKNOWN_OR_CAP','job':key,'source_clause_ids':cids,'result':str(r),'required_target_level':need}
                    if r==z3.sat:
                        model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long()
                        unresolved.update({'source_alpha':[val(v) for v in a],'target_alpha':[val(v) for v in b],
                          'marks':[q for q in range(9) if z3.is_true(model.eval(m[q],model_completion=True))],
                          'active_clauses':[cid for cid in cids if z3.is_true(model.eval(sub(C(cid),a),model_completion=True))]})
                    sol.pop();break
                model=sol.model();val=lambda v:model.eval(v,model_completion=True).as_long();av=[val(v) for v in a];bv=[val(v) for v in b]
                active=next(cid for cid in cids if z3.is_true(model.eval(sub(C(cid),a),model_completion=True)));c=clauses[active]
                if c['kind']=='positive_anchor':
                    carrier=next(q for q in anchors[i] if z3.is_true(model.eval(m[q],model_completion=True)) and any(av[p]==q for p in ((1,3) if q<trees[i][0] else (2,6))))
                    marks={carrier}
                else:marks=set(c['marks'])
                marks.add(trees[i][0]);sol.pop()
                nc={'kind':'score_cube','core':j,'level':need,'marks':sorted(marks),'score_equalities':[(p,v) for p,v in enumerate(bv) if p and v<9]}
                cid=add(nc);assert cid is not None
                suggestions.write(json.dumps({'clause_id':cid,'clause':nc,'from_clause':active,'job':key})+'\n');suggestions.flush();new+=1
                assert queries<2000000 and len(clauses)<2000000
            if proved%100==0:print(json.dumps({'proved_unions':proved,'pending':len(queue),'clauses':len(clauses),'queries':queries,'CPU':time.process_time()}),flush=True)
    report={'status':'COMPLETE_ALL_LOW_JOINT_CLOSURE' if unresolved is None else 'POSITIVE_CLOSURE_NOT_PROVED',
      'anchors':{i:sorted(v) for i,v in anchors.items()},'clauses':clauses,'initial_clauses':initial,'new_clauses':new,
      'queries':queries,'proved_unions':proved,'clause_word_obligations':obligations,'pending_jobs':len(queue),'unresolved':unresolved,
      'Gamma1_required_jobs':len(gamma_jobs),'Gamma1_next_job':gamma_index,'Gamma1_new_proved_jobs':gamma_new,'Gamma1_suggestions':gamma_suggestions,
      'new_finite_tests':0,'completed_semantic_checks_replayed':0,'M3_complete':False}
    write('audit_joint.json',report);print(json.dumps({k:v for k,v in report.items() if k not in ('clauses','anchors')},indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:write('audit_joint_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
