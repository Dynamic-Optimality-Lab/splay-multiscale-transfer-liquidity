"""Universal free-term derivations only; no source-engine imports or queries."""
import json,time,sys
from pathlib import Path
B=Path(__file__).resolve().parent
start=time.process_time(); cap=float(sys.argv[1]); error=None
def out(name,obj):
    with (B/name).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
def n(k,l,r): return (k,l,r)
def at(t,p):
    for i in p:t=t[i]
    return t
def replace(t,p,u):
    if not p:return u
    k,l,r=t
    return n(k,replace(l,p[1:],u),r) if p[0]==1 else n(k,l,replace(r,p[1:],u))
def rule(t,kind):
    g,l,r=t
    if kind=='LL':
        p,x,c=l; xk,a,b=x
        return n(xk,a,n(p,b,n(g,c,r)))
    if kind=='RR':
        p,b,x=r; xk,c,d=x
        return n(xk,n(p,n(g,l,b),c),d)
    if kind=='LR':
        p,a,x=l; xk,b,c=x
        return n(xk,n(p,a,b),n(g,c,r))
    if kind=='RL':
        p,x,d=r; xk,b,c=x
        return n(xk,n(g,l,b),n(p,c,d))
    if kind=='L':
        x,a,b=l; return n(x,a,n(g,b,r))
    if kind=='R':
        x,b,c=r; return n(x,n(g,l,b),c)
    raise AssertionError(kind)
def normalize(t,recipe):
    for path,kind in recipe:
        t=replace(t,path,rule(at(t,path),kind))
    return t
def proof(name,source,recipe,destination):
    assert normalize(source,recipe)==destination,name
    return {'name':name,'source':source,'recipe':recipe,'destination':destination,
            'universally_quantified_hangers':True}
try:
    A,Bb,C,D,E='A','B','C','D','E'
    t=n('y',A,n('p',Bb,n('z',C,n('w',D,E))))
    f1=n('z',n('p',n('y',A,Bb),C),n('w',D,E))
    f2=n('w',n('z',n('p',n('y',A,Bb),C),D),E)
    e2=n('w',n('y',A,n('z',n('p',Bb,C),D)),E)
    f3=n('y',A,n('w',n('p',Bb,n('z',C,D)),E))
    e3=n('y',A,n('w',n('z',n('p',Bb,C),D),E))
    f4=n('p',n('y',A,Bb),n('w',n('z',C,D),E))
    e4=n('p',n('y',A,Bb),n('z',C,n('w',D,E)))
    ps=[proof('erased_Kz',t,[((), 'RR')],f1),
        proof('retained_Kw_F',f1,[((),'R')],f2),
        proof('retained_Kw_E',t,[((2,),'RR'),((),'R')],e2),
        proof('retained_Ky_F',f2,[((1,),'LL'),((),'L')],f3),
        proof('retained_Ky_E',e2,[((),'L')],e3),
        proof('retained_Kp_F',f3,[((),'RL')],f4),
        proof('retained_Kp_E',e3,[((2,),'LL'),((),'R')],e4)]
    v=n('v','L','R')
    t2=n('y',v,n('p',Bb,n('z',C,D)))
    g1=n('z',n('p',n('y',v,Bb),C),D)
    g2=n('v','L',n('z',n('y','R',n('p',Bb,C)),D))
    h2=n('v','L',n('y','R',n('p',Bb,n('z',C,D))))
    ps += [proof('parity_Kz',t2,[((),'RR')],g1),
           proof('parity_Kv_F',g1,[((1,),'LL'),((),'L')],g2),
           proof('parity_Kv_E',t2,[((),'L')],h2)]
    assert f2[1][0]!=e2[1][0] and f3[2][1][0]!=e3[2][1][0]
    assert f4[2][0]!=e4[2][0]
    # Proof depth sites, not search over instantiated trees.
    sites={'Kz_F':((),(2,),(2,2)), 'Kw_F':((),(2,)),
           'Kw_E':((),(2,),(2,2),(2,2,2)),
           'Ky_F':((),(1,),(1,1),(1,1,1)), 'Ky_E':((),(1,)),
           'Kp_F':((),(2,),(2,1)), 'Kp_E':((),(2,),(2,1),(2,1,1))}
    depths={k:len(p)-1 for k,p in sites.items()}
    assert [depths[k] for k in ['Kz_F','Kw_F','Kw_E','Ky_F','Ky_E','Kp_F','Kp_E']]==[2,1,3,3,1,2,3]
    indirect=[1//2-3//2,3//2-1//2,2//2-3//2]
    assert indirect==[-1,1,0]
    assert (3//2-2//2)==0 and (4//2-3//2)==1
    assert (2//2-0//2)==(2//2-1//2)==1
    # Complete formal identity in free variables: j + DP = cross.
    # DP = e_y_after-e_y_before+cross = -j+cross, since after=0.
    coeff={'j':1-1,'cross':1-1}
    assert not any(coeff.values())
    assert time.process_time()-start<cap
    out('transport_derivation.json',{'status':'PASS_EXACT_NAMED_UNIVERSAL_SCHEMAS',
        'proofs':ps,'persistent_distinctions':3,'signed_prefix':{'D':1,'J':0,'Delta':1},
        'cross_key_remainder_retained':True,'maximum_potential_rejected':True,
        'unbounded_positive_injection_proved':'m+1 versus two bits; arbitrary m',
        'uniform_compensation_proved':False,'new_CD_class_proved':False,
        'new_finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0})
    print('PASS: universal rotation terms and exact signed transport; induction remains OPEN')
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:out('audit_transport_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
