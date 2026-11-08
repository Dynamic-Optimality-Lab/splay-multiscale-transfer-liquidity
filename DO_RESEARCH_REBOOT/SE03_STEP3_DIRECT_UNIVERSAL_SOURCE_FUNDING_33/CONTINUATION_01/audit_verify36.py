"""Independent zipper source calculus for arbitrary exterior-population lifting.
Does not run producer search/repair or use bounded private-population trees.
"""
import json,time,sys,itertools,hashlib,collections
from pathlib import Path
from audit_verify35 import formal_path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1]);identities=0
def node(t):return isinstance(t,tuple)
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def allkeys(t):return [] if not node(t) else allkeys(t[1])+[t[0]]+allkeys(t[2])
def pi(t,P,lower=False):
    if not node(t):return t
    return pi(t[2 if lower else 1],P,lower) if t[0] in P else (t[0],pi(t[1],P,lower),pi(t[2],P,lower))
def mirror(t,m):return t if not node(t) else (m-t[0],mirror(t[2],m),mirror(t[1],m))
def calc(t,x):
    global identities
    ancestors=[];v=t
    while v[0]!=x:ancestors.append(v);v=v[1 if x<v[0] else 2];assert node(v)
    h=0
    while len(ancestors)>=2:
        p=ancestors.pop();g=ancestors.pop();k,L,R=v
        if k<p[0]<g[0]:v=(k,L,(p[0],R,(g[0],p[2],g[2])))
        elif g[0]<p[0]<k:v=(k,(p[0],(g[0],g[1],p[1]),L),R)
        elif p[0]<k<g[0]:v=(k,(p[0],p[1],L),(g[0],R,g[2]))
        elif g[0]<k<p[0]:v=(k,(g[0],g[1],L),(p[0],R,p[2]))
        else:raise AssertionError('ORDINARY_DOUBLE_ORDER')
        identities+=1;h+=1
    if ancestors:
        p=ancestors.pop();k,L,R=v;v=(k,L,(p[0],R,p[2])) if k<p[0] else (k,(p[0],p[1],L),R);identities+=1;h+=1
    return v,h
def main():
    z=json.loads((B/'upper_private_low_source_normal_forms.json').read_text());assert z['status']=='COMPLETE_FORMAL_LOW_DIRECT_CLASSIFICATION';R={ (r['actual_path'],tuple(r['private_path_positions'])):r for r in z['direct_schemas']};expected=set();counts=collections.Counter()
    for d in range(2,5):
        for word_tuple in itertools.product('LR',repeat=d):
            word=''.join(word_tuple);t,x=formal_path(word);nodes=[t];v=t
            for c in word:v=v[1 if c=='L' else 2];nodes.append(v)
            for k in range(1,d):
                # Extreme order fixes the private set as the k largest path keys.
                P=set(sorted(allkeys(t))[-k:])
                if t[0] in P or x in P:continue
                positions=tuple(i for i,v in enumerate(nodes) if v[0] in P);key=word,positions;expected.add(key);row=R[key]
                actual,h=calc(t,x);old=pi(t,P);native,h0=calc(old,x);p=pi(actual,P);assert (t,actual,old,native,p)==tuple(fr(row[v]) for v in ('source_term','actual_target','old_source','native_target','projected_actual_target'));assert (h,h0)==(row['actual_H'],row['old_H'])
                kind=row['class'];counts[kind]+=1
                if kind=='COMMUTING':assert p==native and h>=h0
                elif kind=='RR_EXTRA_EVENT_CRITICAL_QUARTET':
                    xx,left,right=native;pp,gg,C=left;g,A,BB=gg;assert p==(xx,(g,A,(pp,BB,C)),right) and (h0,h)==(1,2)
                elif kind in ('INTERNAL_RRR','INTERNAL_RRL'):
                    assert (h,h0)==(2,2);g,A,pr=old;pp,BB,ur=pr;u,ul,rr=ur
                    if kind=='INTERNAL_RRR':xx,dd,ee=rr;assert p==(xx,(pp,(g,A,BB),(u,ul,dd)),ee)
                    else:xx,cc,dd=ul;assert p==(xx,(pp,(g,A,BB),cc),(u,dd,rr))
                else:raise AssertionError('UNCLASSIFIED')
                reflected=mirror(t,d);ref_after,ref_h=calc(reflected,d-x);assert ref_after==mirror(actual,d) and ref_h==h;assert pi(ref_after,{d-v for v in P},True)==mirror(p,d)
    assert expected==set(R) and len(R)==17 and dict(counts)==z['class_counts']
    helper_inputs=[((3,(1,'A','B'),(11,(5,'C','D'),'E')),1,{11}),((3,(1,'A','B'),(11,(5,'C','D'),'E')),5,{11}),((3,'A',(5,'B',(11,(7,'C','D'),'E'))),5,{11}),((3,'A',(5,'B',(11,(7,'C','D'),'E'))),7,{11}),((3,(1,'A','B'),(12,(11,(5,'C','D'),'E'),'F')),1,{11,12}),((3,(1,'A','B'),(12,(11,(5,'C','D'),'E'),'F')),5,{11,12})]
    helpers=[]
    for t,x,P in helper_inputs:
        u,h1=calc(t,11);v,h2=calc(u,x);native,h0=calc(pi(t,P),x);assert (h1,h2,h0)==(1,1,1) and pi(v,P)==native
        reflected=mirror(t,20);u2,h12=calc(reflected,9);v2,h22=calc(u2,20-x);assert v2==mirror(v,20) and h12==h22==1 and pi(v2,{20-p for p in P},True)==mirror(native,20)
        helpers.append({'source_term':t,'private_keys_exposed':sorted(P),'helper':11,'terminal_anchor':x,'actual_target':v,'old_comparison_target':native,'whole_H':2,'comparison_H':1})
    coeff=json.loads((B/'private_max_pullback_independent_audit.json').read_text());old=json.loads((B/'native10_complete_independent_audit.json').read_text());prior=json.loads((B/'one_active_max_source_independent_audit.json').read_text());assert coeff['status'].startswith('PASS_COMPLETE') and old['status']=='PASS_COMPLETE_NATIVE10_SOURCE_CREDIT_CERTIFICATE' and prior['status'].startswith('PASS_COMPLETE')
    assert len(coeff['critical_quartet_candidate_cases'])==66 and len(coeff['internal_positive_source_cases'])==2811 and old['HIGH_envelope_checks']==151164
    assert time.process_time()-START<CAP-1
    deps=('EXTERIOR_PRIVATE_POPULATION_SOURCE_THEOREM.md','upper_private_low_source_normal_forms.json','private_max_pullback_independent_audit.json','one_active_max_source_independent_audit.json','native10_complete_independent_audit.json')
    result={'status':'PASS_UNIFORM_EXTERIOR_PRIVATE_POPULATION_SOURCE_THEOREM','independent_source_method':'zipper four-double/two-zig free-term calculus, different from producer rotations','LOW_direct_schemas':17,'reflected_LOW_direct_schemas':17,'class_counts':dict(counts),'generic_private_helper_cases':helpers,'reflected_helper_cases':6,'formal_source_identity_instantiations':identities,'arbitrary_finite_active_exterior_population':True,'both_exterior_sides_simultaneously':True,'arbitrary_rigid_private_gap_payloads':True,'arbitrary_active_interior_population':False,'genuine_KEEP_support_increased':False,'width':3,'c':'min(actual whole H,3)','working_bound':9,'source_queries':0,'source_engine_calls':0,'finite_passing_population_tests':False,'physical_owner_normalization':'unchanged C14 licensed exchange required; no frozen spare assumed free','external_or_formal_proof_assistant_verification':False,'principal_U33':'OPEN','input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}}
    out('exterior_private_population_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('generic_private_helper_cases','input_sha256')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify36_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
