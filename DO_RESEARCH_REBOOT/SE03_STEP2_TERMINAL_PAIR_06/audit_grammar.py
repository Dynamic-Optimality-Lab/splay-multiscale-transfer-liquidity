"""Symbolic original-rotation frames for the three-packet predecessor bridge.

The finite object is a grammar of universally quantified ordered gap terms,
not a finite population test. A proof of coverage is required separately.
"""
import collections,functools,json,sys,time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path
import audit_counterattack as c
from source_model import event
B=Path(__file__).resolve().parent;started=time.process_time();CAP=min(40,float(sys.argv[1])-4)
@dataclass(frozen=True)
class Hole:
    lo:F
    hi:F
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def guard():
    if time.process_time()-started>CAP or c.account['source_engine_calls']>=900000:raise c.Bound()
def node(k,lo,hi):return (k,Hole(lo,k),Hole(k,hi))
def vars_of(t):return [] if isinstance(t,Hole) else vars_of(t[1])+[t[0]]+vars_of(t[2])
def expand_at(t,p,u):
    if not p:return u
    k,l,r=t
    return (k,expand_at(l,p[1:],u),r) if p[0]=='L' else (k,l,expand_at(r,p[1:],u))
def expand_target(t,x,n):
    u=t;p=''
    while not isinstance(u,Hole):
        if u[0]==x:
            return [t] if len(p) in (1,2) else []
        p+='L' if x<u[0] else 'R'
        if len(p)>2:return []
        u=u[1 if p[-1]=='L' else 2]
    if not u.lo<x<u.hi:return []
    result=[expand_at(t,p,node(x,u.lo,u.hi))]
    if len(p)==1:
        allkeys=sorted(set(vars_of(t)+[F(i) for i in range(n)]+[u.lo,u.hi]))
        parents=[k for k in allkeys if u.lo<k<u.hi and k!=x]
        # A fresh parent is represented by its order cell among ALL word keys.
        parents += [(l+r)/2 for l,r in zip(allkeys,allkeys[1:]) if u.lo<=l<r<=u.hi]
        for y in parents:
            yy=node(y,u.lo,u.hi)
            yy=(y,node(x,u.lo,y),yy[2]) if x<y else (y,yy[1],node(x,y,u.hi))
            result.append(expand_at(t,p,yy))
    return result
def A_frames(word):
    n=len(set(word));states={node(F(word[0]),F(-1),F(n))};sizes=[1]
    for x in word[1:]:
        new=set()
        for t in states:
            guard()
            for u in expand_target(t,F(x),n):
                v,h,_,_=c.move(u,F(x))
                assert h==1;new.add(v)
        states=new;sizes.append(len(states))
        if not states:break
    return states,sizes
@functools.lru_cache(None)
def BF(lo,hi):
    if lo>hi:return ('Q'+str(lo),)
    count=hi-lo+1;m=sum(k in c.MM for k in range(lo,hi+1));result=[]
    for k in range(lo,hi+1):
        if count>2*m-int(k in c.MM):continue
        for l in BF(lo,k-1):
            for r in BF(k+1,hi):result.append(c.N(k,l,r))
    return tuple(result)
def normal(word):
    keys=sorted(set(word));return tuple(keys.index(k) for k in word)
def main():
    states=[t for t in BF(1,11) if t[0] in c.MM];S=set(states)
    incoming=collections.defaultdict(list);fwd=collections.defaultdict(list)
    # Full eleven-Score symbolic core; every omitted interval is arbitrary.
    for t in states:
        guard()
        for x in c.M:
            if x==t[0]:continue
            n=c.bm(t,x)
            if n is None:continue
            b,q=n
            if b not in S:continue
            incoming[b].append((t,x,q));fwd[t].append((b,x,q))
    profiles=collections.defaultdict(list);tails=0
    for pre in states:
        if c.leaves(pre)!=3:continue
        for mid,a,q in fwd[pre]:
            if q!=2 or c.leaves(mid)!=2:continue
            for end,b,q2 in fwd[mid]:
                if q2!=2 or c.leaves(end)!=2:continue
                for target,x,q3 in fwd[end]:
                    if q3!=4 or x in (pre[0],a,b):continue
                    # Cold x must be a marked leaf before the terminal pair.
                    ct=c.core(pre,c.MM)
                    def kids(t,z):
                        if t is None:return None
                        if t[0]==z:return c.labels(t)-{z}
                        v=kids(t[1],z);return v if v is not None else kids(t[2],z)
                    if kids(ct,x):continue
                    for old,g,q0 in incoming[pre]:
                        if q0 not in (1,2) or old[0]==x:continue
                        word=(old[0],g,a,b,x);pat=normal(word);tails+=1
                        profiles[pat].append({'word':word,'previous_Q':q0,'pre_loss_BF':pre,'previous_BF':old})
    report=[];possible=[]
    for pat,examples in sorted(profiles.items()):
        fs,sizes=A_frames(pat)
        row={'rank_word':pat,'B_templates':len(examples),'A_frame_counts':sizes,'A_compatible':bool(fs),
            'example':examples[0]}
        report.append(row)
        if fs:possible.append(row)
    result={'status':'LOCAL_THREE_PACKET_SEPARATION' if not possible else 'LOCAL_THREE_PACKET_BRIDGE_REQUIRES_PROVENANCE',
        'symbolic_BF_contexts':len(states),'terminal_source_contexts':tails,'order_profiles':report,
        'compatible_profiles':len(possible),'source_engine_calls':c.account['source_engine_calls'],
        'new_finite_tests':0,'coverage_requires':'ordered subtree grammar plus symbolic frame lifting proof',
        'no_claim_from_finite_population_tests':True}
    out('grammar.json',result)
    print(json.dumps({k:v for k,v in result.items() if k!='order_profiles'}),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};raise
    finally:out('audit_grammar_exit.json',{'whole_process_CPU_seconds':time.process_time(),'error':error,**c.account})
