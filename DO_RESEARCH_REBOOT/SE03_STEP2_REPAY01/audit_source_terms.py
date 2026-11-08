"""Normalize prescribed free-BST proof terms, never enumerate trees or paths.

Fi are distinct arbitrary ordered BST variables, not empty test fringes.
Only supplied source frames are rewritten; no target-path search is used.
"""
import json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent
CAP=float(sys.argv[1])
def save(name,value):
    with (B/name).open('x',encoding='utf-8') as f:json.dump(value,f,indent=2)
def N(k,l,r):return (k,l,r)
def at(t,p):
    for c in p:
        assert isinstance(t,tuple)
        t=t[1 if c=='L' else 2]
    return t
def put(t,p,v):
    if not p:return v
    k,l,r=t
    return N(k,put(l,p[1:],v),r) if p[0]=='L' else N(k,l,put(r,p[1:],v))
def pair(t,kind):
    a,l,r=t
    if kind=='RR':
        b,bb,br=r;c,cc,d=br
        return N(c,N(b,N(a,l,bb),cc),d)
    if kind=='LL':
        b,bl,cc=l;c,aa,bb=bl
        return N(c,aa,N(b,bb,N(a,cc,r)))
    if kind=='LR':
        b,aa,br=l;c,bb,cc=br
        return N(c,N(b,aa,bb),N(a,cc,r))
    if kind=='RL':
        b,bl,dd=r;c,bb,cc=bl
        return N(c,N(a,l,bb),N(b,cc,dd))
    raise AssertionError(kind)
def zig(t,side):
    a,l,r=t
    if side=='L':b,x,y=l;return N(b,x,N(a,y,r))
    b,x,y=r;return N(b,N(a,l,x),y)
def inorder(t):
    return inorder(t[1])+[t[0]]+inorder(t[2]) if isinstance(t,tuple) else [t]
def derive(t,target,path):
    before=t
    assert at(t,path)[0]==target
    p=path;steps=[]
    while len(p)>=2:
        prefix=p[:-2];kind=p[-2:]
        t=put(t,prefix,pair(at(t,prefix),kind));steps.append([prefix,kind]);p=prefix
    if p:t=zig(t,p);steps.append(['',p])
    assert t[0]==target and inorder(t)==inorder(before)
    return t,steps
def vine(keys,left):
    t='F11'
    for k in reversed(keys):t=N(k,left[k],t)
    return t
F={i:'F'+str(i) for i in range(12)}
R=vine(list(range(1,12)),{i:F[i-1] for i in range(1,12)})
T=vine([1,2,5,6,7,8,9,10,11],{1:F[0],2:F[1],5:N(4,N(3,F[2],F[3]),F[4]),6:F[5],7:F[6],8:F[7],9:F[8],10:F[9],11:F[10]})
# Each tuple is mode,target,A-path,F-path,E-path. None freezes that B.
rows=[
 ('K',3,'RR','RR',None),('K',5,'RR','RR','RR'),
 ('K',7,'RR','RR','RR'),('K',9,'RR','RR','RR'),
 ('K',11,'RR','RR','RR'),('K',9,'LL','LL','LL'),
 ('K',7,'LL','LL','LL'),('K',5,'LL','LL','LL'),
 ('K',3,'LL','LL',None),('D',11,'RRRRRRRR',None,None),
 ('D',1,'LLLL',None,None),('K',1,'','LL','LL'),
 ('K',11,'RR','RRRRRRRRRR','RRRRRRRR'),
 ('D',2,'LLR',None,None),('D',11,'R',None,None),
 ('K',1,'LL','LL','LL'),('K',3,'RRLL','RRLL',None),
 ('K',5,'RRLL','RRLL','RRLL'),('K',7,'RRLL','RRLL','RRLL'),
 ('K',9,'RRLL','RRLL','RRLL'),('K',11,'RR','RR','RR'),
 ('K',9,'LL','LL','LL'),('K',7,'LL','LL','LL'),
 ('K',5,'LL','LL','LL'),('K',3,'LL','LL',None),
 ('K',1,'LL','LL','LL')]
error=None
try:
    a=f=R;e=T;trace=[];totals=[0,0,0];D=J=0
    for i,(mode,k,pa,pf,pe) in enumerate(rows,1):
        assert time.process_time()<CAP
        a,sa=derive(a,k,pa);sf=se=[]
        if pf is not None:f,sf=derive(f,k,pf)
        if pe is not None:e,se=derive(e,k,pe)
        ca=(len(pa)+1)//2;qf=0 if pf is None else len(pf)//2;qe=0 if pe is None else len(pe)//2
        totals=[totals[0]+ca,totals[1]+qf,totals[2]+qe]
        if mode=='K' and k==3:D+=qf
        elif mode=='K':J+=qf-qe
        trace.append({'occurrence':i,'mode':mode,'key':k,'paths':[pa,pf,pe],
                      'frames':[sa,sf,se],'costs':[ca,qf,qe],'end_terms':[a,f,e]})
        if i==15:assert a==f
    assert a==R and f==R and e==T
    assert totals==[34,30,24] and D==5 and J==1
    # First erased K5 from diagonal R and steady K5 from T have the same
    # source normal form. The remaining prescribed E derivation is shared.
    warm,ws=derive(R,5,'RRRR');steady,ss=derive(T,5,'RR')
    assert warm==steady
    save('source_term_derivation.json',{'quantification':'all twelve independent ordered BST variables F0..F11',
      'normalization':'prescribed source frames; no enumeration, path search, or source-engine calls',
      'initial_full_and_A':R,'initial_recurrent_E':T,'erased_key':3,
      'trace':trace,'totals':{'A':34,'QF':30,'QE_recurrent':24,'QE_first':25,'D':D,'J':J},
      'warm_join':{'first_path':'RRRR','steady_path':'RR','common_term':warm,'frames_first':ws,'frames_steady':ss},
      'alignment':{'preperiod':1,'period':1},'full_genuine_support':[1,3,5,7,9,11],
      'aux_genuine_support':[1,5,7,9,11],'core_sizes':[11,9],
      'new_finite_tests':0,'source_engine_calls':0,'old_rows_replayed':0})
    print('UNIVERSAL_SOURCE_TERM_DERIVATION_PASS',totals,D,J)
except BaseException as ex:
    error={'type':type(ex).__name__,'message':str(ex)};raise
finally:save('audit_source_terms_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error})
