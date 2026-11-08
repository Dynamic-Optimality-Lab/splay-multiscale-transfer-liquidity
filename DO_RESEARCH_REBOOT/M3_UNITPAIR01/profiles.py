"""Generic positional unit-pair builder, with compact complete prefix provenance."""
from functools import lru_cache
from itertools import product
import json,time
from pathlib import Path
BASE=Path('DO_RESEARCH_REBOOT/M3_UNITPAIR01')
P=None;G='G';PATHS=((0,),(1,),(0,0),(0,1),(1,0),(1,1));OBS=((),(0,),(1,),(0,0),(0,1),(1,0),(1,1))
def core(k):return isinstance(k,int) and k%16==0 and 0<=k<=128
def rr(t):
    k,l,r=t;x,a,b=l;return (x,a,(k,b,r))
def rl(t):
    k,l,r=t;x,a,b=r;return (x,(k,l,a),b)
def move(t,p):
    if len(p)==1:return (rr if p[0]==0 else rl)(t)
    a,b=p;k,l,r=t
    if a==b:return rr(rr(t)) if a==0 else rl(rl(t))
    return rr((k,rl(l),r)) if a==0 else rl((k,l,rr(r)))
def full(depth=7,p=()):return None if len(p)>depth else (p,full(depth,p+(0,)),full(depth,p+(1,)))
def get(t,p):
    for s in p:t=t[1+s]
    return t
def find(t,x):
    if t in (P,G):return None
    if t[0]==x:return t
    return find(t[1],x) or find(t[2],x)
def observation(t,owner):
    zero=find(t,owner);assert zero is not None;out=[]
    for p in OBS:
        n=t
        for s in p:
            if n is P:break
            if n==G:n=zero
            n=n[1+s]
        if n is P:out.append((1,0,0))
        else:
            if n==G:n=zero
            out.append((0,1,n[0]//16) if core(n[0]) else (0,0,0))
    return tuple(out)
def families(g,h):
    for p in PATHS:yield None,(p,)
    for gap in (g,h):
        if gap not in (0,9):continue
        for p,q in product(PATHS,repeat=2):yield gap,(p,q)
def specification(gap,word):
    t=full();need={()};forced={():None}
    for j,p in enumerate(word):
        need.update(get(t,p[:i])[0] for i in range(len(p)+1));where=get(t,p)[0]
        forced[where]=16*gap-8 if j<len(word)-1 else None;t=move(t,p)
    obs=set(OBS)|{get(t,p)[0] for p in OBS};zero=find(t,());obs.update(ch[0] for ch in zero[1:] if ch is not None);obs|=need
    for p in tuple(obs):obs.update(p[:i] for i in range(len(p)))
    return obs,need,forced
def generate(g,h,gap,word):
    keys=tuple(sorted([16*k for k in range(9)]+[16*g-8,16*h-8]));obs,need,forced=specification(gap,word)
    def allowed(p,k):return p not in forced or (core(k) if forced[p] is None else k==forced[p])
    @lru_cache(None)
    def size(p,lo,hi):
        if p not in obs:return 1
        n=0 if p in need else 1+int(not any(core(k) for k in keys[lo:hi]))
        for i in range(lo,hi):
            if allowed(p,keys[i]):n+=size(p+(0,),lo,i)*size(p+(1,),i+1,hi)
        return n
    def walk(p,lo,hi):
        if p not in obs:
            yield P;return
        if p not in need:
            yield P
            if not any(core(k) for k in keys[lo:hi]):yield G
        for i in range(lo,hi):
            if allowed(p,keys[i]):
                for l in walk(p+(0,),lo,i):
                    for r in walk(p+(1,),i+1,hi):yield (keys[i],l,r)
    return size((),0,len(keys)),lambda:walk((),0,len(keys)),keys
def encode(t,keys):
    codes={k:i for i,k in enumerate(keys)};out=bytearray()
    def go(n):
        if n is P:out.append(254)
        elif n==G:out.append(255)
        else:out.append(codes[n[0]]);go(n[1]);go(n[2])
    go(t);return out.hex()
def decode(code,keys):
    seq=iter(bytes.fromhex(code))
    def go():
        x=next(seq)
        if x==254:return P
        if x==255:return G
        return (keys[x],go(),go())
    t=go();assert next(seq,None) is None;return t
def main():
    out=BASE/'counts.json';assert not out.exists();start=time.process_time();pairs=[]
    for g in range(10):
        for h in range(g+1,10):
            if g+h>9:continue
            rows=[]
            for helper,word in families(g,h):
                n,_,keys=generate(g,h,helper,word)
                if n:rows.append({'helper':helper,'word':word,'count':n})
            pairs.append({'g':g,'h':h,'count':sum(r['count'] for r in rows),'families':rows})
    result={'status':'COUNTS_WITHIN_REGISTERED_CAPS' if all(p['count']<=1000000 for p in pairs) else 'UNKNOWN_REGISTERED_ENUMERATION_CAP',
      'canonical_pairs':len(pairs),'maximum':max(p['count'] for p in pairs),'total':sum(p['count'] for p in pairs),'pairs':pairs,'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({**{k:v for k,v in result.items() if k!='pairs'},'pair_counts':[[p['g'],p['h'],p['count']] for p in pairs]},indent=2),flush=True)
if __name__=='__main__':main()
