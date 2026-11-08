"""Bounded source-geometry search for an obstruction to extending MC29-X.
Only actual SS source operations are explored. No universal conclusion
from an absent finite witness. Separate source-admissibility levels kept.
"""
import collections,importlib.util,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;CAP=float(sys.argv[1]);START=time.process_time()
sp=importlib.util.spec_from_file_location('C29_nonextreme_source',P/'SE03_STEP3_GUARDED_E4_REALIZABILITY_27/CONTINUATION_01/audit_construct.py')
C=importlib.util.module_from_spec(sp);sp.loader.exec_module(C)

def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)

def fr(t):return tuple(fr(x) for x in t) if isinstance(t,list) else t

def main():
    src=json.loads((B/'comb_source_fixtures.json').read_text());T=fr(src['reports'][0]['original_diagonal_tree']);queue=collections.deque([(T,[])])
    seen={T};candidates=[];expanded=0
    while queue and C.queries<900:
        t,route=queue.popleft();expanded+=1
        for x in sorted(C.M-{t[0]}):
            path=C.path(t,x)
            if len(path)%2 or any(path[j:j+2] not in ('LL','RR') for j in range(0,len(path),2)):continue
            q=len(path)//2;pa,ch=C.L.marked_tree(t,C.M);v=pa[x];beta=0
            while v is not None:beta+=len(ch[v])>=2;v=pa[v]
            if q==3 and beta==3 and not ch[x] and {x,t[0]}!={1,13} and len(route)>=2:
                beforej=T
                for k in route[:-2]:beforej=C.tr(beforej,k)[0]
                Z=beforej[0];Y,R=route[-2:]
                if len({x,Y,Z,R})==4:
                    candidates.append({'route':route,'comb_target':x,'roots':[Z,Y,R],'comb_B':t,'before_j_B':beforej})
            z,_,ev=C.tr(t,x)
            if all(e['G'] in C.M and e['P'] not in C.M for e in ev) and z not in seen:
                seen.add(z);queue.append((z,route+[x]))
        if candidates:break
    # For exact discovered B candidates, search only four-key A preparation
    # suffixes after an actual all-key reset. This is an existential source
    # construction, not a quotient realization assertion.
    found=None
    for cand in candidates[:8]:
        x=cand['comb_target'];Z,Y,R=cand['roots'];a=T
        for k in range(13,0,-1):a=C.tr(a,k)[0]
        todo=collections.deque([(a,[])]);visited={a}
        while todo and C.queries<1600:
            a,prep=todo.popleft()
            if a[0]==Z:
                z=a;cost=[]
                for k in (Y,R,x):z,path,ev=C.tr(z,k);cost.append(len(ev))
                if cost==[1,1,1]:
                    found=dict(cand,A_before_j=a,A_preparation=list(range(13,0,-1))+prep,A_after_comb=z,H_triplet=cost,
                        status='GENUINE_B_ROUTE_AND_A_DELETE_PREPARATION; CLOSED_PERIOD_EMBEDDING_NOT_YET_CONSTRUCTED')
                    break
            if len(prep)>=7:continue
            for k in (x,Y,Z,R):
                z=C.tr(a,k)[0]
                if z not in visited:visited.add(z);todo.append((z,prep+[k]))
        if found:break
    out('nonextreme_source_search.json',{'status':'BOUNDED_SOURCE_GEOMETRY_SEARCH','B_states_seen':len(seen),'B_states_expanded':expanded,
        'candidate_B_routes':candidates,'witness':found,'no_witness_does_not_prove_impossibility':True,'queries':C.queries})
    print(json.dumps({'status':'NONEXTREME_GEOMETRY_RESULT','queries':C.queries,'B_states':len(seen),'candidates':len(candidates),'found':found is not None}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_nonextreme_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':C.calls,'source_queries':C.queries})
