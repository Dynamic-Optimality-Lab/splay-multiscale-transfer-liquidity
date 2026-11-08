"""Unary private-helper activation into the protected-fringe source invariant."""
import json,time,sys,itertools
from pathlib import Path
from audit_proof114 import trees,visit,bind,project
from audit_verify35 import splay,path,node
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
def spines(t):
    L=set();R=set();v=t
    while node(v):L.add(v[0]);v=v[1]
    v=t
    while node(v):R.add(v[0]);v=v[2]
    return L,R
def phi(t,P,tags,Lsp,Rsp):
    if not node(t):return t
    k,A,B=t;A=phi(A,P,tags,Lsp,Rsp);B=phi(B,P,tags,Lsp,Rsp)
    if A is None or B is None:return None
    if k not in P:return k,A,B
    if A=='E':return B
    if B=='E':return A
    if tags[k]=='L' and k not in Rsp and node(A) and A[2]=='E':return A[0],A[1],B
    if tags[k]=='R' and k not in Lsp and node(B) and B[1]=='E':return B[0],A,B[2]
    return None
def main():
    rows=[];bad=[]
    for m in range(2,6):
        for ti,t in enumerate(trees(0,m)):
            g=t[0]
            for y in range(m):
                if y==g or len(path(t,y))>2:continue
                middle,h=splay(t,y)
                for x in range(m):
                    if x==y or len(path(middle,x))>2 or visit(t,y)|visit(middle,x)!=set(range(m)):continue
                    for mask in range(1,1<<m):
                        P={k for k in range(m) if mask>>k&1}
                        if g in P or x in P or y not in P:continue
                        for flags in range(1<<(m+1)):
                            actual=bind(t,flags);s=project(actual,P)
                            if s is None:continue
                            mid,h1=splay(actual,y);after,h2=splay(mid,x);assert h1==h2==1;LS,RS=spines(after);witness=None
                            for bits in itertools.product('LR',repeat=len(P)):
                                tags=dict(zip(sorted(P),bits));p=phi(after,P,tags,LS,RS)
                                if p is None:continue
                                for z in range(m):
                                    if z in P:continue
                                    old,c1=splay(s,z);old,c2=splay(old,x)
                                    if old==p and c1<=1 and c2<=1:witness={'tags':tags,'old_DELETE_proxy':z,'comparison_after':p,'old_event_costs':[c1,c2]};break
                                if witness:break
                            row={'m':m,'tree_index':ti,'source':actual,'helper':y,'terminal':x,'private_mask':mask,'leaf_mask':flags,'actual_after':after,'projected_old_source':s,'witness':witness};rows.append(row)
                            if witness is None:bad.append(row)
    assert time.process_time()-START<CAP-1
    out('unary_helper_protected_activation_forms.json',{'status':'UNIFORM_UNARY_HELPER_PROTECTED_ACTIVATION_DERIVATION' if not bad else 'UNARY_HELPER_PROTECTED_ACTIVATION_HAS_EXCEPTIONS','free_term_schemas':len(rows),'schemas':rows,'exceptions':bad,'source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'});print(json.dumps({'status':'UNARY_HELPER_ACTIVATION_ANALYSIS','schemas':len(rows),'exceptions':len(bad),'first_exception':bad[0] if bad else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof130_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
