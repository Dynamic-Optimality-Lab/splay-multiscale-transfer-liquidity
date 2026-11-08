"""Complete source frames with unary anonymous core at both genuine boundaries."""
import json,time,sys,itertools,collections,functools
from pathlib import Path
from audit_verify35 import splay,node,path,at
from audit_proof106 import classify
B=Path(__file__).resolve().parent;START=time.process_time();CAP=float(sys.argv[1])
def out(n,z):
    with (B/n).open('x') as f:json.dump(z,f,indent=2)
@functools.lru_cache(None)
def trees(lo,hi):
    if lo==hi:return ('G'+str(lo),)
    return tuple((k,L,R) for k in range(lo,hi) for L in trees(lo,k) for R in trees(k+1,hi))
def visit(t,x):return {at(t,path(t,x)[:j])[0] for j in range(len(path(t,x))+1)}
def bind(t,mask):
    if not node(t):j=int(t[1:]);return 'X'+str(j) if mask>>j&1 else 'E'
    return t[0],bind(t[1],mask),bind(t[2],mask)
def project(t,P):
    if not node(t):return t
    L,R=project(t[1],P),project(t[2],P)
    if L is None or R is None:return None
    if t[0] in P:return R if L=='E' else L if R=='E' else None
    return t[0],L,R
def label(s,p,x,H):
    g=s[0];z,w,h=classify(s,p,x,H,g)
    if z=='RLL_MIN_ROOT':return 'GENERIC_RLL',w,h
    if z=='UNCLASSIFIED_LRR_LEFT':
        z,w,h=classify(s,p,x,H,s[1][0]);z='GENERIC_LRR' if z=='LRR_MIN_LEFT' else z
    elif z=='LRR_MIN_LEFT':z='GENERIC_LRR'
    return z,w,h
def main():
    rows=[];tested=0;templates=0;complete=True
    for m in range(2,6):
        for ti,t in enumerate(trees(0,m)):
            g=t[0]
            words=[]
            for x in range(m):
                if x==g:continue
                if 0<len(path(t,x))<=4 and visit(t,x)==set(range(m)):words.append((None,x))
                for y in range(m):
                    if y==g or len(path(t,y))>2:continue
                    mid,hy=splay(t,y)
                    if x==y or len(path(mid,x))>2:continue
                    if visit(t,y)|visit(mid,x)==set(range(m)):words.append((y,x))
            for y,x in words:
                templates+=1
                for mask in range(1,1<<m):
                    P={k for k in range(m) if mask>>k&1}
                    if g in P or x in P:continue
                    for leafmask in range(1<<(m+1)):
                        if time.process_time()-START>CAP-2:complete=False;break
                        actual=bind(t,leafmask);s=project(actual,P)
                        if s is None:continue
                        if y is None:after,H=splay(actual,x)
                        else:mid,h1=splay(actual,y);after,h2=splay(mid,x);assert h1==h2==1;H=2
                        p=project(after,P)
                        if p is None:continue
                        tested+=1;comparison=None
                        if y is not None:
                            for z in range(m):
                                if z in P:continue
                                a,h0=splay(s,z);a,hx=splay(a,x)
                                if h0+hx<=H and a==p:comparison={'helper':z,'old_H':h0+hx};break
                        if comparison:kind='COMPARISON_WORD';oldword=None;h0=comparison['old_H']
                        else:kind,oldword,h0=label(s,p,x,H)
                        rows.append({'m':m,'tree_index':ti,'helper':y,'target':x,'private_mask':mask,'leaf_mask':leafmask,'source':actual,'actual_after':after,'projected_source':s,'projected_after':p,'actual_H':H,'class':kind,'old_path':oldword,'old_H':h0,'comparison':comparison})
                    if not complete:break
                if not complete:break
            if not complete:break
        if not complete:break
    bad=[r for r in rows if r['class'].startswith('UNCLASSIFIED') or r['old_H']>r['actual_H']];z={'status':'COMPLETE_UNARY_BOUNDARY_LOW_SOURCE_GRAMMAR' if complete and not bad else 'UNARY_BOUNDARY_LOW_SOURCE_GRAMMAR_OPEN','source_templates':templates,'accepted_schemas':len(rows),'class_counts':dict(collections.Counter(r['class'] for r in rows)),'schemas':rows,'unresolved':bad,'enumeration_complete':complete,'scope':'all LOW direct or two-H1 packet frames, arbitrary ordered old-anchor terms, anonymous core unary at both genuine boundaries; arbitrary private key gaps and populations','source_queries':0,'source_engine_calls':0,'principal_U33':'OPEN'};out('unary_boundary_LOW_source_normal_forms.json',z);print(json.dumps({k:v for k,v in z.items() if k not in ('schemas','unresolved')}));print(json.dumps({'unresolved_count':len(bad),'first_unresolved':bad[0] if bad else None}))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:out('audit_proof114_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0})
