"""Independent completeness/zipper check of unary helper activation."""
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
    Z=json.loads((B/'unary_helper_protected_activation_forms.json').read_text());assert not Z['exceptions'];rows={(skeleton(fr(r['source'])),r['helper'],r['terminal'],r['private_mask'],r['leaf_mask']):r for r in Z['schemas']};seen=set()
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
                    for mask in range(1,1<<m):
                        if mask>>g&1 or mask>>x&1 or not mask>>y&1:continue
                        def unary(v):
                            if not node(v):return v
                            L,R=unary(v[1]),unary(v[2])
                            if L is None or R is None:return None
                            if mask>>v[0]&1:return R if L=='E' else L if R=='E' else None
                            return v[0],L,R
                        for flags in range(1<<(m+1)):
                            def bind(v):
                                if not node(v):j=int(v[1:]);return 'X'+str(j) if flags>>j&1 else 'E'
                                return v[0],bind(v[1]),bind(v[2])
                            actual=bind(t);s=unary(actual)
                            if s is None:continue
                            mid,h1=calc(actual,y);after,h2=calc(mid,x);key=t,y,x,mask,flags;r=rows[key];seen.add(key);W=r['witness'];assert W is not None;tags={int(k):v for k,v in W['tags'].items()};left=set();right=set();v=after
                            while node(v):left.add(v[0]);v=v[1]
                            v=after
                            while node(v):right.add(v[0]);v=v[2]
                            def phi(v):
                                if not node(v):return v
                                k,L,R=v;L=phi(L);R=phi(R)
                                if not mask>>k&1:return k,L,R
                                if L=='E':return R
                                if R=='E':return L
                                if tags[k]=='L':assert k not in right and node(L) and L[2]=='E';return L[0],L[1],R
                                assert tags[k]=='R' and k not in left and node(R) and R[1]=='E';return R[0],L,R[2]
                            p=phi(after);old,c1=calc(s,W['old_DELETE_proxy']);old,c2=calc(old,x);assert p==old==fr(W['comparison_after']) and c1<=1 and c2<=1 and h1==h2==1;assert [c1,c2]==W['old_event_costs'];assert (actual,after,s)==tuple(fr(r[k]) for k in ('source','actual_after','projected_old_source'))
    assert seen==set(rows) and len(rows)==916 and time.process_time()-START<CAP-1
    deps=('UNARY_HELPER_ACTIVATION_AND_H1_CONTINUATION.md','unary_helper_protected_activation_forms.json','protected_fringe_H1_independent_audit.json')
    out('unary_helper_activation_independent_audit.json',{'status':'PASS_UNIFORM_UNARY_HELPER_ACTIVATION_AND_H1_CONTINUATION','free_term_schemas':916,'method':'independent insertion-permutation source grammar, zipper rotations, final actual spine guards and recursive protected-fringe equations','all_finite_anchor_supports_and_private_populations':True,'comparison_helper_and_terminal_cost_at_most_one_each':True,'actual_helper_bits_retained_even_if_proxy_zero':True,'generalized_H1_fringe_induction':'retirement requires actual marked child and is literal old case; survival substitutes entire projected fringe hanger; off-path guards/fringes preserved','repeated_activation_from_protected_branching_source':False,'direct_H2_covered':False,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_ALL_SUPPORT_SINGLE_ACTIVATION_PLUS_H1_CONTINUATION','schemas':916,'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify59_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
