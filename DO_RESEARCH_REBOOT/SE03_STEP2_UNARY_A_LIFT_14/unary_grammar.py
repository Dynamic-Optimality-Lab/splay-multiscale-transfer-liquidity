"""Exhaustive zero/one unary-core syntax with arbitrary rigid private gaps.
Only primitive rotations and marked-core walk are supplied by a kernel.
"""
import importlib.util,json,time
from pathlib import Path
B=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('original_unary14',B.parent/'SE03_STEP2_COLD_NEG2_01/source_model.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
M=set(range(1000,6001,1000));calls=0
def freeze(v):return tuple(map(freeze,v)) if isinstance(v,list) else v
def keys(t):return [] if t is None else keys(t[1])+[t[0]]+keys(t[2])
def expand_mark(t):return None if t is None else (1000*t[0],expand_mark(t[1]),expand_mark(t[2]))
def put(t,path,v):
    if not path:return v
    return (t[0],put(t[1],path[1:],v),t[2]) if path[0]=='L' else (t[0],t[1],put(t[2],path[1:],v))
def subtrees(t,path=''):
    if t is None:return []
    return ([(path,t)] if path else [])+subtrees(t[1],path+'L')+subtrees(t[2],path+'R')
def contraction(t):
    if t is None:return None
    if t[0] in M:return (t[0]//1000,contraction(t[1]),contraction(t[2]))
    assert (t[1] is None)!=(t[2] is None)
    return contraction(t[1] if t[1] is not None else t[2])
def states_from_base(base):
    trees=[expand_mark(freeze(t)) for t in base];new=[]
    for t in trees:
        for path,S in subtrees(t):
            kk=keys(S)
            new.append(put(t,path,((max(kk)//1000)*1000+500,S,None)))
            new.append(put(t,path,((min(kk)//1000-1)*1000+500,None,S)))
    assert len(new)==len(set(new))==1320
    return trees+new
def material(t):
    j=0
    def go(t):
        nonlocal j
        if t is None:v='F'+str(j);j+=1;return v
        return (t[0],go(t[1]),go(t[2]))
    result=go(t);kk=[0]+keys(t)+[7000]
    return result,{('F'+str(i)):(kk[i],kk[i+1]) for i in range(len(kk)-1)}
def gaps(t,d=0):
    if isinstance(t,str):return [(t,d)]
    return gaps(t[1],d+1)+gaps(t[2],d+1)
def replace(t,gap,u):
    if isinstance(t,str):return u if t==gap else t
    return (t[0],replace(t[1],gap,u),replace(t[2],gap,u))
def project(t,K):
    c=K.core(t,M);unmark=[]
    def walk(v):
        if v is None:return
        if v[0] not in M:
            if (v[1] is None)==(v[2] is None):unmark.extend([0,0])
            else:unmark.append(v[0])
        walk(v[1]);walk(v[2])
    walk(c)
    if len(unmark)>1 or c is None or c[0] not in M:return None
    def conv(v):
        if v is None:return None
        key=v[0] if v[0] in M else 1000*sum(x<v[0] for x in M)+500
        return (key,conv(v[1]),conv(v[2]))
    return conv(c)
def generate(base,K=p):
    global calls
    aa=states_from_base(base);ids={t:i for i,t in enumerate(aa)};baseidx={freeze(t):i for i,t in enumerate(base)}
    contract=[baseidx[contraction(t)] for t in aa];relations={1:set(),2:set()};witness={}
    def trace(t,x):
        global calls
        calls+=1;assert calls<1800000;return K.trace(t,x)
    def record(a,x,H,TT,accesses,dest,kind):
        end=project(dest,K)
        if end is None:return
        b=ids[end];edge=(a,x//1000,b);relations[H].add(edge)
        key=(H,)+edge
        if key not in witness:witness[key]={'H':H,'a':a,'x':x//1000,'b':b,
            'source':TT,'positive_accesses':accesses,'kind':kind}
    for a,raw in enumerate(aa):
        T,intervals=material(raw);g=T[0]
        for x in sorted(M-{g}):
            dep=len(K.path(T,x))
            if dep in (1,2,3,4):
                dest,_,ev=trace(T,x);H=len(ev);assert H in (1,2)
                record(a,x,H,T,[x],dest,'single_marked_access')
        first=[(T,y,'known_core_first') for y in keys(raw) if 1<=len(K.path(T,y))<=2]
        for gap,d in gaps(T):
            if d>2:continue
            lo,hi=intervals[gap];mid=(lo+hi)//2;q1=lo+(hi-lo)//3;q2=lo+2*(hi-lo)//3
            assert lo<q1<q2<hi and lo<mid<hi
            F=[gap+'_'+str(i) for i in range(3)]
            first.append((replace(T,gap,(mid,F[0],F[1])),mid,'private_gap_root'))
            if d==1:
                first.append((replace(T,gap,(q2,(q1,F[0],F[1]),F[2])),q1,'private_left_grandchild'))
                first.append((replace(T,gap,(q1,F[0],(q2,F[1],F[2]))),q2,'private_right_grandchild'))
        for TT,y,kind in first:
            mid,_,ev=trace(TT,y);assert len(ev)==1
            for x in sorted(M-{g}):
                if not 1<=len(K.path(mid,x))<=2:continue
                dest,_,ev2=trace(mid,x);assert len(ev2)==1
                record(a,x,2,TT,[y,x],dest,kind)
    return {'states':aa,'contract_ids':contract,'H1':sorted(relations[1]),'H2':sorted(relations[2]),
        'witnesses':[witness[k] for k in sorted(witness)],'source_engine_calls':calls,
        'coverage':'all132 marked6 cores plus all1320 unary insertions; free-gap path grammar, not bounded private populations'}
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
