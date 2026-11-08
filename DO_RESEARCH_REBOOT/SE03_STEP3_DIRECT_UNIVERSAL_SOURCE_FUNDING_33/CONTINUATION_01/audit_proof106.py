"""Uniform FIRST-GAP predecessor projection source normal forms.
Arbitrary off-path payloads are first projected; E denotes no old anchor,
X_i an arbitrary old-anchor subtree. No private-population sample is used.
"""
import json,time,sys,itertools,collections
from pathlib import Path
from audit_verify35 import formal_path,at,splay,node
B=Path(__file__).resolve().parent
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def leaves(t):return [t] if not node(t) else leaves(t[1])+leaves(t[2])
def replace_leaves(t,m):return m[t] if not node(t) else (t[0],replace_leaves(t[1],m),replace_leaves(t[2],m))
def pathword(t,x):
    p=''
    while t[0]!=x:
        k=1 if x<t[0] else 2;p+='L' if k==1 else 'R';t=t[k];assert node(t)
    return p
def pred(t,P,one):
    if not node(t):return t
    k,L,R=t;L=pred(L,P,one);R=pred(R,P,one)
    if k not in P:return k,L,R
    if L=='E':return R
    assert L==(one,'E','E');return one,'E',R
def classify(s,p,x,actual_h,one):
    native,old_h=splay(s,x);word=pathword(s,x)
    if native==p:return 'COMMUTING',word,old_h
    if len(word)==2 and actual_h==2:
        g,L,R=s
        if word=='RR':a,A,pr=s;b,BB,xr=pr;xx,C,D=xr;expected=(xx,(a,A,(b,BB,C)),D)
        elif word=='LL':a,pl,D=s;b,xl,C=pl;xx,A,BB=xl;expected=(xx,A,(a,(b,BB,C),D))
        else:return 'UNCLASSIFIED_EXTRA',word,old_h
        return ('EXTRA_EVENT_'+word if p==expected else 'UNCLASSIFIED_EXTRA_FORMULA'),word,old_h
    if len(word)!=3 or actual_h!=2:return 'UNCLASSIFIED_DEPTH',word,old_h
    g,L,R=s
    if word=='RRR':g,A,pr=s;a,BB,ur=pr;b,C,xr=ur;xx,D,E=xr;expected=(xx,(a,(g,A,BB),(b,C,D)),E);label='INHERITED_RRR'
    elif word=='RRL':g,A,pr=s;a,BB,ur=pr;b,xl,E=ur;xx,C,D=xl;expected=(xx,(a,(g,A,BB),C),(b,D,E));label='INHERITED_RRL'
    elif word=='LLL':g,pl,E=s;a,ul,D=pl;b,xl,C=ul;xx,A,BB=xl;expected=(xx,A,(a,(b,BB,C),(g,D,E)));label='INHERITED_LLL'
    elif word=='LLR':g,pl,E=s;a,ul,D=pl;b,A,xr=ul;xx,BB,C=xr;expected=(xx,(b,A,BB),(a,C,(g,D,E)));label='INHERITED_LLR'
    elif word=='RLL':g,A,ur=s;a,vl,E=ur;b,xl,D=vl;xx,BB,C=xl;expected=(xx,(g,A,BB),(a,(b,C,D),E));label='RLL_MIN_ROOT' if g==one else 'UNCLASSIFIED_RLL_ROOT'
    elif word=='LRR':g,pl,E=s;a,A,ur=pl;b,BB,xr=ur;xx,C,D=xr;expected=(xx,(a,A,(b,BB,C)),(g,D,E));label='LRR_MIN_LEFT' if a==one else 'UNCLASSIFIED_LRR_LEFT'
    else:return 'UNCLASSIFIED_PATTERN',word,old_h
    return (label if p==expected else 'UNCLASSIFIED_'+word+'_FORMULA'),word,old_h
def main():
    rows=[]
    for depth in range(2,5):
        for bits in itertools.product('LR',repeat=depth):
            word=''.join(bits);bare,target=formal_path(word)
            for explicit in (True,False):
                for count in range(1,depth):
                    P=set(range(1,count+1)) if explicit else set(range(count));one=0 if explicit else -1
                    if bare[0] in P or target in P:continue
                    L=leaves(bare);m={}
                    for j,name in enumerate(L):
                        if not explicit and j==0:m[name]=(one,'E','E')
                        elif j<=(count if explicit else count-1):m[name]='E'
                        else:m[name]='X'+str(j)
                    actual_source=replace_leaves(bare,m);actual,h=splay(actual_source,target);source=pred(actual_source,P,one);projected=pred(actual,P,one);label,oldword,h0=classify(source,projected,target,h,one);assert h0<=h
                    rows.append({'actual_path':word,'anchor1_on_path':explicit,'private_keys_on_path':sorted(P),'anchor1_symbol':one,'target_symbol':target,'actual_source_term_after_payload_projection':actual_source,'actual_target_term_after_payload_projection':actual,'projected_old_source':source,'projected_actual_target':projected,'old_path':oldword,'actual_H':h,'old_H':h0,'class':label})
    bad=[r for r in rows if r['class'].startswith('UNCLASSIFIED')];counts=dict(collections.Counter(r['class'] for r in rows));result={'status':'COMPLETE_FIRST_GAP_DIRECT_LOW_SOURCE_NORMAL_FORMS' if not bad else 'FIRST_GAP_DIRECT_LOW_CLASSIFICATION_OPEN','schemas':rows,'class_counts':counts,'unclassified_schemas':bad,'private_population_scope':'arbitrary finite; only actual length<=4 search-path operands exposed; all remaining first-gap private terms represented by E or the single anchor1 payload','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('first_gap_predecessor_direct_LOW_normal_forms.json',result);print(json.dumps({'status':result['status'],'schemas':len(rows),'class_counts':counts,'unclassified':len(bad)}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof106_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
