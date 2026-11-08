"""New universal P identity and noncommuting projection proof terms only."""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;start=time.process_time();cap=float(sys.argv[1]);error=None
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
def n(k,l,r):return (k,l,r)
def at(v,p):
    for q in p:v=v[q]
    return v
def put(v,p,w):
    if not p:return w
    a=list(v);a[p[0]]=put(a[p[0]],p[1:],w);return tuple(a)
def step(v,k):
    g,l,r=v
    if k=='L':
        x,a,b=l;return n(x,a,n(g,b,r))
    if k=='R':
        x,b,c=r;return n(x,n(g,l,b),c)
    if k=='LL':
        p,x,c=l;xk,a,b=x;return n(xk,a,n(p,b,n(g,c,r)))
    if k=='RR':
        p,b,x=r;xk,c,d=x;return n(xk,n(p,n(g,l,b),c),d)
    if k=='LR':
        p,a,x=l;xk,b,c=x;return n(xk,n(p,a,b),n(g,c,r))
    if k=='RL':
        p,x,d=r;xk,b,c=x;return n(xk,n(g,l,b),n(p,c,d))
    raise AssertionError(k)
def lemma(name,source,recipe,dest,target,path):
    assert at(source,path)[0]==target
    v=source
    for p,k in recipe:v=put(v,p,step(at(v,p),k))
    assert v==dest,name
    return {'name':name,'source':source,'recipe':recipe,'destination':dest,
            'target':target,'target_source_path':path,'source_depth':len(path)}
try:
    A,C,D,E='A','C','D','E'; BB='B'
    t=n('g',n('p',A,n('s',n('x',BB,C),D)),E)
    f1=n('p',A,n('g',n('s',n('x',BB,C),D),E))
    u=n('x',n('p',A,BB),n('s',C,n('g',D,E)))
    v=n('p',A,n('x',BB,n('s',C,n('g',D,E))))
    ex=n('x',n('p',A,BB),n('g',n('s',C,D),E))
    e0=n('g',n('x',n('p',A,BB),n('s',C,D)),E)
    proofs=[lemma('P_full_p1',t,[((),'L')],f1,'p',(1,)),
        lemma('P_full_x',f1,[((2,),'LL'),((),'R')],u,'x',(2,1,1)),
        lemma('P_full_p2',u,[((),'L')],v,'p',(1,)),
        lemma('P_full_g',v,[((2,),'RR'),((),'R')],t,'g',(2,2,2)),
        lemma('P_erased_first_x',t,[((1,),'RL'),((),'L')],ex,'x',(1,2,1)),
        lemma('P_erased_first_g',ex,[((),'R')],e0,'g',(2,)),
        lemma('P_erased_recurrent_x',e0,[((),'L')],ex,'x',(1,)),
        lemma('P_erased_recurrent_g',ex,[((),'R')],e0,'g',(2,))]
    source=n('g',n('z','EMPTY',n('p',n('x','A','B'),'C')),'D')
    dest=n('x',n('z','EMPTY','A'),n('g',n('p','B','C'),'D'))
    proofs.append(lemma('minimum_contraction_full',source,[((1,),'RL'),((),'L')],dest,'x',(1,2,1)))
    projected=n('g',n('p',n('x','A','B'),'C'),'D')
    projected_dest=n('x','A',n('p','B',n('g','C','D')))
    proofs.append(lemma('minimum_contraction_projected',projected,[((),'LL')],projected_dest,'x',(1,1)))
    qfull=sum(p['source_depth']//2 for p in proofs[:4]);afull=sum((p['source_depth']+1)//2 for p in proofs[:4])
    qfirst=sum(p['source_depth']//2 for p in proofs[4:6]);qrecur=sum(p['source_depth']//2 for p in proofs[6:8])
    assert (qfull,afull,qfirst,qrecur)==(2,6,1,0)
    assert proofs[0]['source_depth']//2==proofs[2]['source_depth']//2==0
    assert u[2][0]!=ex[2][0] and t[1][0]!=e0[1][0]
    assert time.process_time()-start<cap
    out('transport_derivation02.json',{'status':'PASS_NAMED_UNIVERSAL_SOURCE_IDENTITIES','proofs':proofs,
        'P':{'A':afull,'Q_F':qfull,'Q_E_first':qfirst,'Q_E_recurrent':qrecur,'D':0,'J_per_recurrent_period':2},
        'six_key_amplification':'J>=2m-2 on aligned block; m>=4, not exact Q_E',
        'genuinely_new_CD_domain_established':False,'uniform_support_extension':False,
        'source_engine_calls':0,'new_finite_tests':0,'old_semantic_rows_replayed':0})
    print('PASS: zero-direct persistent transport and source projection obstruction')
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_transport02_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
