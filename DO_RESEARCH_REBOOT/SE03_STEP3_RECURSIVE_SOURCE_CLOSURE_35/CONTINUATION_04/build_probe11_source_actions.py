"""Complete actual eleven-key actions by certified leaf substitution.
Only1024 whole Hamiltonian actions require new source-engine calls.
"""
import functools,hashlib,importlib.util,json,pickle,sys,time
from pathlib import Path
import numpy as np
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);QCAP=int(sys.argv[2]);START=time.process_time();V=None
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bare(t):return (t[0],bare(t[1]),bare(t[2])) if isinstance(t,(tuple,list)) else None
@functools.lru_cache(None)
def family(lo,hi):
    if lo>hi:return (None,)
    return tuple((k,l,r) for k in range(lo,hi+1) for l in family(lo,k-1) for r in family(k+1,hi))
def leaves(t):return [t[0]] if t[1] is None and t[2] is None else ([] if t[1] is None else leaves(t[1]))+([] if t[2] is None else leaves(t[2]))
def remove(t,x):
    if t is None:return None
    if t[0]==x:assert t[1] is None and t[2] is None;return None
    return (t[0]-(t[0]>x),remove(t[1],x),remove(t[2],x))
def main():
    global V
    native=json.loads((B/'native10_source_actions.json').read_text());old=[bare(t) for t in native['trees']];idx={t:i for i,t in enumerate(old)}
    T=family(1,11);assert len(T)==58786;index={t:i for i,t in enumerate(T)};n=len(T)
    insert=np.full((11,len(old)),65535,dtype=np.uint16);first=np.empty(n,dtype=np.int8);last=first.copy();delfirst=np.empty(n,dtype=np.int32);dellast=delfirst.copy()
    for i,t in enumerate(T):
        ll=leaves(t);first[i],last[i]=ll[0],ll[-1]
        for x in ll:
            j=idx[remove(t,x)];assert insert[x-1,j]==65535;insert[x-1,j]=i
            if x==ll[0]:delfirst[i]=j
            if x==ll[-1]:dellast[i]=j
    assert np.all(insert!=65535)
    oldD=np.array(native['destination'],dtype=np.uint16);oldH=np.array(native['H'],dtype=np.uint8);oldQ=np.array(native['Q'],dtype=np.uint8)
    D=np.full((n,11),65535,dtype=np.uint16);H=np.full((n,11),255,dtype=np.uint8);Q=H.copy();missing=[]
    for x in range(1,12):
        excepted=(first==x)&(last==x);leaf=np.where(first!=x,first,last);source=np.where(first!=x,delfirst,dellast)
        col=x-1-(leaf<x);col[excepted]=0;source[excepted]=0;ok=~excepted
        D[ok,x-1]=insert[leaf[ok]-1,oldD[source[ok],col[ok]]];H[ok,x-1]=oldH[source[ok],col[ok]];Q[ok,x-1]=oldQ[source[ok],col[ok]]
        missing.extend((int(i),x) for i in np.flatnonzero(excepted))
    assert len(missing)==1024 and QCAP>=len(missing)
    spec=importlib.util.spec_from_file_location('CS35_original_functional',B/'audit_core39.py');V=importlib.util.module_from_spec(spec);spec.loader.exec_module(V)
    V.CAP=CAP;V.START=START;V.QCAP=QCAP;V.CALLS=0
    for i,x in missing:
        t,h,q,_=V.splay(T[i],x);D[i,x-1]=index[t];H[i,x-1]=h;Q[i,x-1]=q;assert (h,q)==(5,5)
    assert np.all(D!=65535) and np.all(H!=255)
    z={'trees':T,'destination':D,'H':H,'Q':Q,'roots':np.array([t[0] for t in T],dtype=np.uint8),
      'fresh_actions':missing,'source_queries':V.CALLS,'source_engine_calls':V.CALLS,'cached_source_substitutions':n*11-len(missing),
      'independent_status':'PENDING','purpose':'actual closed-source counterexample search; no universal passing promotion',
      'input_sha256':{str(p):sha(p) for p in [B/'native10_source_actions.json',B/'native10_source_independent_audit.json',
        B/'OFF_PATH_LEAF_SOURCE_LIFT.md',F/'ACTUAL_CLOSED_SOURCE_FALSIFICATION_BOX.md']}}
    with (F/'probe11_source_actions.pkl').open('xb') as f:pickle.dump(z,f,protocol=5)
    report={k:v for k,v in z.items() if k not in ('trees','destination','H','Q','roots','fresh_actions')};report.update({'actual_trees':n,'actual_actions':n*11})
    with (F/'probe11_source_actions.json').open('x',encoding='utf8') as f:json.dump(report,f,indent=2)
    print(json.dumps(report),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_core47_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,
          'source_queries':0 if V is None else V.CALLS,'source_engine_calls':0 if V is None else V.CALLS},f)
