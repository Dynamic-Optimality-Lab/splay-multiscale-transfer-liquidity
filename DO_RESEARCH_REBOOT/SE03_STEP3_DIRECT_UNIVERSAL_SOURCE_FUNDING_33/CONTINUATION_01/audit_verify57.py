"""Independent all-support two-KEEP source identity proof, no coefficient oracle."""
import json,time,sys,itertools,hashlib
from pathlib import Path
from audit_verify36 import calc
from audit_verify55 import insert,label_gaps,skeleton,route
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def main():
    Z=json.loads((B/'two_KEEP_H1_unary_return_source_forms.json').read_text());assert not Z['failures'];rows={(skeleton(fr(r['source'])),r['first_KEEP'],r['second_KEEP'],r['private_mask'],r['leaf_mask']):r for r in Z['schemas']};seen=set();templates=0
    for m in range(2,6):
        shapes=set()
        for perm in itertools.permutations(range(m)):
            t=None
            for k in perm:t=insert(t,k)
            shapes.add(label_gaps(t))
        for t in shapes:
            g=t[0]
            for y in range(m):
                if y==g or len(route(t,y))>3:continue
                middle,h=calc(t,y)
                for x in range(m):
                    if x==y or len(route(middle,x))>3 or set(route(t,y))|set(route(middle,x))!=set(range(m)):continue
                    templates+=1
                    for oldmask in range(1<<m):
                        if any(not oldmask>>k&1 for k in (g,y,x)) or oldmask==(1<<m)-1:continue
                        P=((1<<m)-1)^oldmask
                        def project(v):
                            if not node(v):return v
                            L,R=project(v[1]),project(v[2])
                            if L is None or R is None:return None
                            if P>>v[0]&1:return R if L=='E' else L if R=='E' else None
                            return v[0],L,R
                        for flags in range(1<<(m+1)):
                            def bind(v):
                                if not node(v):j=int(v[1:]);return 'X'+str(j) if flags>>j&1 else 'E'
                                return v[0],bind(v[1]),bind(v[2])
                            actual=bind(t);s=project(actual)
                            if s is None:continue
                            mid,h1=calc(actual,y);after,h2=calc(mid,x);p=project(after)
                            if p is None:continue
                            old,c1=calc(s,y);old,c2=calc(old,x);assert old==p and h1==h2==c1==c2==1;key=t,y,x,P,flags;r=rows[key];seen.add(key);assert (actual,mid,after,s,p,old)==tuple(fr(r[k]) for k in ('source','actual_middle','actual_after','projected_source','projected_after','ordinary_old_two_KEEP_target'));assert r['old_H']==r['actual_H']==2
    assert seen==set(rows) and len(rows)==392 and templates==36 and time.process_time()-START<CAP-1
    names=('TWO_KEEP_UNARY_RETURN_THEOREM.md','two_KEEP_H1_unary_return_source_forms.json')
    out('two_KEEP_unary_return_independent_audit.json',{'status':'PASS_UNIFORM_ALL_SUPPORT_TWO_H1_GENUINE_PACKET_UNARY_RETURN','source_templates':36,'free_term_schemas':392,'arbitrary_finite_anchor_support':True,'arbitrary_finite_private_populations_and_depths':True,'anonymous_branching_at_shared_boundary_allowed':True,'initial_and_final_unary_required':True,'genuine_target_may_return_to_initial_root':True,'two_ordinary_event_counts':[1,1],'method':'independent insertion-permutation skeleton completeness and zipper algebra on arbitrary ordered terms','no_numerical_debt_or_population_samples':True,'physical_event_correspondence':'one original event at each positive target occurrence; bits retain original IDs, no new credit','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in names}});print(json.dumps({'status':'PASS_ALL_SUPPORT_TWO_KEEP_UNARY_RETURN','templates':36,'schemas':392,'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify57_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
