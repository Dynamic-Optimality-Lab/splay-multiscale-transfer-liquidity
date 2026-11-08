"""All branch choices in a finite observed-prefix superrelation.

P forgets empty/opaque kind; G keeps out-of-range slot0 lookup behavior.
Private gap labels are not present in a shared shadow key.
"""
from functools import lru_cache
from itertools import product
import json,time
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_TWOGAP01')
P=None
G='G'
KEYS=(-8,0,8,16,32,48,64,80,96,112,128)
PATHS=((0,),(1,),(0,0),(0,1),(1,0),(1,1))
OBS=((),(0,),(1,),(0,0),(0,1),(1,0),(1,1))
def core(k):return isinstance(k,int) and k>=0 and k%16==0
def rr(t):
    k,l,r=t;x,a,b=l
    return (x,a,(k,b,r))
def rl(t):
    k,l,r=t;x,a,b=r
    return (x,(k,l,a),b)
def access_path(t,p):
    if len(p)==1:return (rr if p[0]==0 else rl)(t)
    a,b=p;k,l,r=t
    if a==b:return (rr(rr(t)) if a==0 else rl(rl(t)))
    return rr((k,rl(l),r)) if a==0 else rl((k,l,rr(r)))
def full(depth=5,p=()):
    return None if len(p)>depth else (p,full(depth,p+(0,)),full(depth,p+(1,)))
def get(t,p):
    for s in p:t=t[1+s]
    return t
def positions(path,ghost=False):
    t=full();dst=access_path(t,path);out=set(OBS)
    out.update(get(dst,p)[0] for p in OBS)
    if ghost:
        # A depth1 ghost reads the current children of the original slot0.
        def find(n):
            if n is None:return None
            if n[0]==():return n
            return find(n[1]) or find(n[2])
        z=find(dst)
        out.update(c[0] for c in z[1:] if c is not None)
    for p in tuple(out):out.update(p[:i] for i in range(len(p)))
    return frozenset(out)
def generator(path,ghost=False,anon=True):
    required={path[:i] for i in range(len(path)+1)}
    obs=positions(path,ghost)
    keys=KEYS if anon else tuple(k for k in KEYS if core(k))
    @lru_cache(None)
    def count(pos,lo,hi):
        if pos not in obs:return 1
        n=0
        if pos not in required:
            n=1+int(ghost and not any(core(k) for k in keys[lo:hi]))
        for i in range(lo,hi):
            if pos in ((),path) and not core(keys[i]):continue
            n+=count(pos+(0,),lo,i)*count(pos+(1,),i+1,hi)
        return n
    def gen(pos,lo,hi):
        if pos not in obs:
            yield P;return
        if pos not in required:
            yield P
            if ghost and not any(core(k) for k in keys[lo:hi]):yield G
        for i in range(lo,hi):
            if pos in ((),path) and not core(keys[i]):continue
            for l in gen(pos+(0,),lo,i):
                for r in gen(pos+(1,),i+1,hi):yield (keys[i],l,r)
    return count((),0,len(keys)),lambda:gen((),0,len(keys)),obs
def shadow(t,owner):
    def find(n):
        if n in (P,G):return None
        if n[0]==owner:return n
        return find(n[1]) or find(n[2])
    slot0=find(t);assert slot0 is not None
    out=[]
    for path in OBS:
        n=t
        for s in path:
            if n is P:break
            if n==G:n=slot0
            n=n[1+s]
        if n is P:out.append((1,0,0))
        else:
            if n==G:n=slot0
            out.append((0,1,n[0]//16) if core(n[0]) else (0,0,0))
    return tuple(out)
def normalize(alpha):
    a=[tuple(x) for x in alpha];a[0]=(0,int(a[0][1]),a[0][2] if a[0][1] else 0)
    for i in range(1,7):
        k,s,x=a[i];a[i]=(1,0,0) if k!=0 else (0,int(s),x if s else 0)
    for i,ch in ((1,(3,4)),(2,(5,6))):
        if a[i][0]:
            for j in ch:a[j]=(1,0,0)
    return tuple(a)
def main():
    start=time.process_time();rows=[]
    for ghost,anon,path in product((False,True),(False,True),PATHS):
        n,_,obs=generator(path,ghost,anon)
        rows.append({'ghosts':ghost,'anonymous':anon,'path':path,'representatives':n,'observed_source_positions':sorted(obs)})
    result={'status':'FINITE_EXACT_SYMBOLIC_COUNTS','rows':rows,'cpu_seconds':time.process_time()-start,
      'enumeration_complete':False,'potential_constructed':False}
    with (BASE/'representation_counts.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
