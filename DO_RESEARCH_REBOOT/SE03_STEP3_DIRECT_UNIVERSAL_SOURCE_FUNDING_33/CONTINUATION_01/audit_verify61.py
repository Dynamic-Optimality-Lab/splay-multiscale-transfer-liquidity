"""Independent symbolic unification and zipper audit of saturated activation."""
import json,time,sys,itertools,collections,hashlib
from pathlib import Path
from audit_verify36 import calc
from audit_verify55 import insert,label_gaps,route
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
class Invalid(Exception):pass
def node(t):return isinstance(t,tuple)
def fr(t):return tuple(map(fr,t)) if isinstance(t,list) else t
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def canonical(t,bounds):
    if not node(t):return 'E' if t=='E' else 'V'+repr(tuple(bounds[t]))
    return t[0],canonical(t[1],bounds),canonical(t[2],bounds)
def tokens(t,P):
    if not node(t):return [] if t=='E' else [('V',t)]
    return tokens(t[1],P)+[('P' if t[0] in P else 'K',t[0])]+tokens(t[2],P)
def conditions(t,P):
    allseq=tokens(t,P);marked=lambda seq:[a for a in seq if a[0]!='P'];allowed={};branches=set();LS=set();RS=set();v=t
    while node(v):LS.add(v[0]);v=v[1]
    v=t
    while node(v):RS.add(v[0]);v=v[2]
    def walk(v):
        if not node(v):return
        k,L,R=v
        if k in P:
            left,right=marked(tokens(L,P)),marked(tokens(R,P));pos=allseq.index(('P',k))
            if left and right:
                branches.add(k);allowed[k]=({'L'} if left==marked(allseq[:pos]) and k not in RS else set())|({'R'} if right==marked(allseq[pos+1:]) and k not in LS else set())
            else:allowed[k]={'L','R'}
        walk(L);walk(R)
    walk(t);return allowed,branches
def plain_phi(t,P,tags):
    allowed,branches=conditions(t,P)
    def walk(v):
        if not node(v):return v
        k,A,C=v;A=walk(A);C=walk(C)
        if k not in P:return k,A,C
        if A=='E':return C
        if C=='E':return A
        side=tags[k];assert side in allowed[k]
        if side=='L':assert node(A) and A[2]=='E';return A[0],A[1],C
        assert node(C) and C[1]=='E';return C[0],A,C[2]
    return walk(t)
def main():
    Z=json.loads((B/'saturated_source_activation_analysis.json').read_text());assert Z['enumeration_complete'] and Z['exception'] is None;rows={}
    for r in Z['schemas']:
        bounds={k:tuple(v) for k,v in r['variable_bounds'].items()};tags={int(k):v for k,v in r['source_tags'].items()};key=(canonical(fr(r['actual_source_after_virtual_fringe_exposure']),bounds),r['helper'],r['terminal'],r['private_mask'],tuple((k,tags[k]) for k in r['used_source_tags']));assert key not in rows;rows[key]=r
    seen=set();templates=0;costs=collections.Counter()
    for m in range(2,6):
        shapes=set()
        for perm in itertools.permutations(range(m)):
            t=None
            for k in perm:t=insert(t,k)
            shapes.add(label_gaps(t))
        for bare in shapes:
            g=bare[0]
            for y in range(m):
                if y==g or len(route(bare,y))>3:continue
                middle,_=calc(bare,y)
                for x in range(m):
                    if x==y or len(route(middle,x))>3 or set(route(bare,y))|set(route(middle,x))!=set(range(m)):continue
                    templates+=1
                    for mask in range(1,1<<m):
                        P={k for k in range(m) if mask>>k&1}
                        if g in P or x in P or y not in P:continue
                        for flags in range(1<<(m+1)):
                            def bind(v):
                                if not node(v):j=int(v[1:]);return 'X'+str(j) if flags>>j&1 else 'E'
                                return v[0],bind(v[1]),bind(v[2])
                            base=bind(bare);allowed,branches=conditions(base,P)
                            for bits in itertools.product('LR',repeat=len(P)):
                                tags=dict(zip(sorted(P),bits))
                                if any(tags[k] not in allowed[k] for k in P):continue
                                env={};types={'X'+str(j):'NE' for j in range(m+1)};bounds={'X'+str(j):(j-1,j) for j in range(m+1)}
                                def deref(v):
                                    while not node(v) and v in env:v=env[v]
                                    return v
                                def empty(v):
                                    v=deref(v)
                                    if v=='E':return
                                    if not node(v) and types[v]=='ANY':env[v]='E';return
                                    raise Invalid()
                                def fringe(v,side):
                                    v=deref(v)
                                    if not node(v):
                                        assert v!='E' and types[v]=='NE';lo,hi=bounds[v];j=(lo+hi)/2;name='U'+str(len(types));types[name]='ANY';bounds[name]=(lo,j) if side=='L' else (j,hi);env[v]=(j,name,'E') if side=='L' else (j,'E',name);v=env[v]
                                    empty(v[2] if side=='L' else v[1]);return v
                                def projected(v):
                                    if not node(v):return deref(v)
                                    k,L,R=v;L=projected(L);R=projected(R)
                                    if k not in P:return k,L,R
                                    if k not in branches:return R if not [a for a in tokens(v[1],P) if a[0]!='P'] else L
                                    if tags[k]=='L':j,A,E=fringe(L,'L');return j,A,R
                                    j,E,C=fringe(R,'R');return j,L,C
                                try:oldterm=projected(base)
                                except Invalid:continue
                                anyvars=[k for k,v in types.items() if v=='ANY' and k not in env]
                                for values in itertools.product((False,True),repeat=len(anyvars)):
                                    assignment=dict(env)
                                    for k,nonempty in zip(anyvars,values):
                                        if not nonempty:assignment[k]='E'
                                    def resolve(v):
                                        if not node(v):return resolve(assignment[v]) if v in assignment else v
                                        return v[0],resolve(v[1]),resolve(v[2])
                                    actual=resolve(base);oldsource=resolve(oldterm);key=(canonical(actual,bounds),y,x,mask,tuple((k,tags[k]) for k in sorted(branches)));r=rows[key];seen.add(key);W=r['witness'];assert W is not None;actual1,h1=calc(actual,y);after,h2=calc(actual1,x);dsttags={int(k):v for k,v in W['destination_tags'].items()};end=plain_phi(after,P,dsttags);start=plain_phi(actual,P,tags);assert start==oldsource
                                    old,c1=calc(oldsource,W['comparison_DELETE_proxy']);old,c2=calc(old,x);assert old==end and c1+c2<=2 and h1==h2==1;costs[c1,c2]+=1
                                    rb={k:tuple(v) for k,v in r['variable_bounds'].items()};assert canonical(start,bounds)==canonical(fr(r['old_source']),rb);assert canonical(after,bounds)==canonical(fr(r['actual_after']),rb);assert canonical(old,bounds)==canonical(fr(W['comparison_after']),rb)
    assert seen==set(rows) and len(rows)==1684 and templates==36 and time.process_time()-START<CAP-1
    deps=('SATURATED_FRINGE_REPEATED_ACTIVATION.md','saturated_source_activation_analysis.json','unary_activation_saturated_creator_forms.json','protected_fringe_H1_independent_audit.json','unary_helper_activation_independent_audit.json')
    out('saturated_repeated_activation_independent_audit.json',{'status':'PASS_UNIFORM_ARBITRARY_SUPPORT_SATURATED_FRINGE_REPEATED_ACTIVATION','source_templates':36,'free_term_schemas':1684,'old_comparison_cost_pairs':{str(k):v for k,v in costs.items()},'method':'independent insertion-permutation source grammar; first-order fringe-root unification with ANY/E constraints instead of producer restart refinement; inorder-prefix saturation checks; distinct zipper algebra','all_finite_anchor_supports_private_populations_and_repetitions':True,'block_cost_at_most_actual_two':True,'per_occurrence_bit_transport_not_assumed':True,'source_queries':0,'source_engine_calls':0,'Gate_U':'OPEN; direct H2 creation/unsaturated frames, ordinary all-support credit and ownership interfaces remain','principal_U33':'OPEN','external_or_formal_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}});print(json.dumps({'status':'PASS_ALL_SUPPORT_REPEATED_SATURATED_HELPER_ACTIVATION','schemas':1684,'cost_pairs':{str(k):v for k,v in costs.items()},'source_queries':0,'principal_U33':'OPEN'}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify61_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
