"""Static inherited certificate lookup and complete integer-class arithmetic.
No splay, source engine, new frame compiler or finite-source exploration.
Only TWO literal states projected by hand from already replayed C31 rows
are located in the previously audited six-key table. This is research
evidence, not the missing seven-key source-boundary bridge.
"""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent;OLD=P/'SE03_STEP2_UNARY_A_LIFT_14'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def fr(x):return tuple(fr(a) for a in x) if isinstance(x,list) else x
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    negative=set()
    for Q in range(1,7):
        for beta in range(Q+1):
            for k3 in range(beta+1):
                for d in range(7):
                    if Q+1+beta+k3+d>7:continue
                    for c in (1,2,3):
                        sig=2*c-k3-(0 if d>=2 else 1 if d==1 else min(Q,2))
                        if sig<0:
                            assert c==1 and d==0 and Q>=2
                            if k3==1:assert Q<=4 and sig==-1
                            else:assert (Q,beta,k3,sig)==(2,2,2,-2)
                            negative.add((Q,beta,k3,sig))
    a=read(OLD/'branch_grammar2.json')['states'];table=read(OLD/'branch_core11_mask0.json');bt=table['BF_trees']
    ai={fr(t):i for i,t in enumerate(a)};bi={fr(t):i for i,t in enumerate(bt)}
    roots={j:[i for i,t in enumerate(a) if t[0]==1000*j] for j in range(1,7)}
    offsets=[];offset=0
    for t in bt:offsets.append(offset);offset+=len(roots[table['marks'].index(t[0])+1])
    assert offset==len(table['debt'])
    left=(1500,(1000,None,None),(2000,None,None))
    A9=(4000,(3000,left,None),(5000,None,(6000,None,None)))
    A5=(3000,left,(4000,None,(5000,None,(6000,None,None))))
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    tail=(8,'F7',(9,'F8',(10,'F9',(11,'F10','F11'))))
    B9=(7,(6,(5,lower,'F5'),'F6'),tail)
    B5=(5,lower,(6,'F5',(7,'F6',tail)))
    lookup=[]
    for name,A,F in [('C31_after127_9',A9,B9),('C31_after128_5',A5,B5)]:
        i=ai[A];k=bi[F];rr=table['marks'].index(F[0])+1;index=offsets[k]+roots[rr].index(i)
        lookup.append({'name':name,'A_quotient':A,'BF_core':F,'A_index':i,'BF_index':k,'debt_index':index,'D6':table['debt'][index],
                       'source':'literal projection of existing C31 replay; no newly executed source transition'})
    out('static_inherited_debt_lookup.json',{'status':'PASS_STATIC_SAVED_CERTIFICATE_LOOKUP','new_source_queries':0,
        'negative_integer_classes':sorted(negative),'lookups':lookup,
        'scope':'six-mark debt entries only; no claimed open-seven-source boundary or terminal inequality',
        'input_sha256':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (OLD/'branch_grammar2.json',OLD/'branch_core11_mask0.json')}})
    print(json.dumps({'status':'STATIC_LOOKUP_PASS','D6':[(z['name'],z['D6']) for z in lookup],'new_source_queries':0}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_proof_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_engine_calls':0,'source_queries':0})
