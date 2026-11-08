"""Check universal source-term identities and assemble the one-active-max proof.
The letters at leaves are arbitrary ordered private terms, not finite trees.
"""
import json,time,sys,hashlib,pickle,itertools,math
from pathlib import Path
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1]);rewrites=0
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def node(t):return isinstance(t,tuple)
def path(t,x):
    a=[]
    while t[0]!=x:a.append(1 if x<t[0] else 2);t=t[a[-1]];assert node(t)
    return a
def at(t,p):
    for d in p:t=t[d]
    return t
def put(t,p,u):
    if not p:return u
    k=p[0];return (t[0],put(t[1],p[1:],u),t[2]) if k==1 else (t[0],t[1],put(t[2],p[1:],u))
def rotate(t,p):
    k=p[-1];base=at(t,p[:-1]);v=base[k]
    q=(v[0],v[1],(base[0],v[2],base[2])) if k==1 else (v[0],(base[0],base[1],v[1]),v[2])
    return put(t,p[:-1],q)
def splay(t,x):
    global rewrites
    events=0
    while (p:=path(t,x)):
        if len(p)==1:t=rotate(t,p);rewrites+=1
        elif p[-1]==p[-2]:t=rotate(t,p[:-1]);t=rotate(t,path(t,x));rewrites+=2
        else:t=rotate(t,p);t=rotate(t,path(t,x));rewrites+=2
        events+=1
    return t,events
def project(t,z):
    if not node(t):return t
    return project(t[1],z) if t[0]==z else (t[0],project(t[1],z),project(t[2],z))
def formal_path(word):
    counter=iter(range(100));gap=iter('ABCDEFGHIJKLMNO')
    def shape(k):
        if k==len(word):return ('key',next(gap),next(gap))
        return ('key',shape(k+1),next(gap)) if word[k]=='L' else ('key',next(gap),shape(k+1))
    def label(t):
        if not node(t):return t
        left=label(t[1]);key=next(counter);right=label(t[2]);return key,left,right
    t=label(shape(0));x=at(t,[1 if v=='L' else 2 for v in word])[0];return t,x
def main():
    proof=json.loads((B/'private_max_pullback_independent_audit.json').read_text());assert proof['status']=='PASS_COMPLETE_PRIVATE_MAX_COEFFICIENT_OBLIGATIONS'
    # Bind the independently read JSON export literally to the unchanged checked debt.
    receipt=json.loads((B/'native10_complete_independent_audit.json').read_text());raw=(B/'native10_debt_03.pkl').read_bytes();assert hashlib.sha256(raw).hexdigest()==receipt['input_sha256'];save=pickle.loads(raw);export=json.loads((B/'native10_credit_certificate.json').read_text());assert dict(export['nonzero_debt'])==save['level'] and not save['queue'];assert receipt['HIGH_envelope_checks']==151164;del save,raw,export
    rows=[]
    for d in (2,3,4):
        for pos in range(1,d):
            for suffix in itertools.product('LR',repeat=d-pos-1):
                word='R'*pos+'L'+''.join(suffix);t,x=formal_path(word);z=at(t,[2]*pos)[0];assert z==d
                old=project(t,z);actual,h=splay(t,x);native,h0=splay(old,x);p=project(actual,z)
                assert h==math.ceil(d/2) and h0==math.ceil((d-1)/2)
                if p==native:kind='COMMUTING'
                elif d==3:
                    xx,left,right=native;pp,gg,C=left;g,A,BB=gg;assert p==(xx,(g,A,(pp,BB,C)),right);kind='RR_EXTRA_EVENT_CRITICAL_QUARTET'
                elif d==4:
                    g,A,pr=old;pp,BB,ur=pr;u,ul,rr=ur
                    if x>u:
                        xx,dd,ee=rr;expected=(xx,(pp,(g,A,BB),(u,ul,dd)),ee);kind='INTERNAL_RRR'
                    else:
                        xx,cc,dd=ul;expected=(xx,(pp,(g,A,BB),cc),(u,dd,rr));kind='INTERNAL_RRL'
                    assert p==expected
                else:raise AssertionError('UNCLASSIFIED_SCHEMA')
                rows.append({'actual_path':word,'private_max_depth':pos,'class':kind,'actual_source':t,'actual_target':actual,'old_source':old,'old_native_target':native,'projected_actual_target':p,'actual_H':h,'old_H':h0})
    assert len(rows)==11 and sum(v['class']=='COMMUTING' for v in rows)==6
    # All genuine one-event-private-helper/one-event-marked-target frames.
    examples=[((3,(1,'A','B'),(11,(5,'C','D'),'E')),1),((3,(1,'A','B'),(11,(5,'C','D'),'E')),5),((3,'A',(5,'B',(11,(7,'C','D'),'E'))),5),((3,'A',(5,'B',(11,(7,'C','D'),'E'))),7)]
    helpers=[]
    for t,x in examples:
        u,h1=splay(t,11);v,h2=splay(u,x);native,h0=splay(project(t,11),x);assert h1==h2==h0==1 and project(v,11)==native
        helpers.append({'source_term':t,'target':x,'actual_after_DELETE_max':u,'actual_final':v,'projected_final':native,'whole_actual_H':2,'comparison_H':1})
    assert time.process_time()-START<CAP-1
    deps=('PRIVATE_MAX_ONE_EVENT_PROJECTION.md','PRIVATE_MAX_DIRECT_LIFT.md','ONE_ACTIVE_MAX_SOURCE_THEOREM.md','private_max_pullback_independent_audit.json','native10_complete_independent_audit.json','native10_source_independent_audit.json')
    result={'status':'PASS_COMPLETE_RESTRICTED_ONE_ACTIVE_MAX_SOURCE_THEOREM','formal_term_path_schemas':rows,'formal_private_helper_schemas':helpers,'formal_rotation_identity_instantiations':rewrites,'not_finite_population_samples':True,'source_queries':0,'source_engine_calls':0,'original_source_primitives':'accepted six ordinary bottom-up identities, instantiated with arbitrary free ordered terms; no fresh source engine','LOW_coverage':'all event-word partitions; every noncommuting H2 on-path maximum case is one of the checked critical/coefficient classes','HIGH_coverage':'unchanged accepted151164 all-endpoint envelopes on projected A shapes','arbitrary_active_anonymous_nodes':False,'arbitrary_r':False,'scope':'ten old anchors plus one active DELETE-only extreme maximum or reflected minimum; arbitrary untouched ordered gap payloads','width':3,'c':'min(actual whole H,3)','working_bank':9,'normalized_owner_composition':'conditional on unchanged C14 original exchange/eligibility licenses; no claim every old spare is free','principal_U33':'OPEN','external_or_formal_proof_assistant_verification':False,'input_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in deps}}
    out('one_active_max_source_independent_audit.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('formal_term_path_schemas','formal_private_helper_schemas','input_sha256')}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_verify35_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
