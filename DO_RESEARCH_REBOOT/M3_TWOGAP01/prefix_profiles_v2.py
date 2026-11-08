"""Generic one- or two-access observation unions, preserving private branches."""
from prefix_profiles import *
def specification(word):
    src=full(depth=7);t=src;required={()};forced={(): 'core'}
    for j,path in enumerate(word):
        for i in range(len(path)+1):required.add(get(t,path[:i])[0])
        label=get(t,path)[0]
        forced[label]='core' if j==len(word)-1 else -8
        t=access_path(t,path)
    obs=set(OBS);obs.update(get(t,p)[0] for p in OBS)
    def find(n):
        if n is None:return None
        if n[0]==():return n
        return find(n[1]) or find(n[2])
    z=find(t);obs.update(c[0] for c in z[1:] if c is not None)
    obs.update(required)
    for p in tuple(obs):obs.update(p[:i] for i in range(len(p)))
    return frozenset(obs),frozenset(required),forced
def genword(word,ghost=True):
    obs,required,forced=specification(word);keys=KEYS
    def allowed(pos,k):return pos not in forced or (core(k) if forced[pos]=='core' else k==forced[pos])
    @lru_cache(None)
    def count(pos,lo,hi):
        if pos not in obs:return 1
        n=0 if pos in required else 1+int(ghost and not any(core(k) for k in keys[lo:hi]))
        for i in range(lo,hi):
            if allowed(pos,keys[i]):n+=count(pos+(0,),lo,i)*count(pos+(1,),i+1,hi)
        return n
    def gen(pos,lo,hi):
        if pos not in obs:
            yield P;return
        if pos not in required:
            yield P
            if ghost and not any(core(k) for k in keys[lo:hi]):yield G
        for i in range(lo,hi):
            if not allowed(pos,keys[i]):continue
            for l in gen(pos+(0,),lo,i):
                for r in gen(pos+(1,),i+1,hi):yield (keys[i],l,r)
    return count((),0,len(keys)),lambda:gen((),0,len(keys)),obs
def cases():
    for p in PATHS:yield (p,)
    for p,q in product(PATHS,repeat=2):yield (p,q)
def main():
    start=time.process_time();rows=[]
    for word in cases():
        n,_,obs=genword(word)
        rows.append({'word':word,'representatives':n,'observed_positions':len(obs),'max_depth':max(map(len,obs))})
    result={'status':'FINITE_EXACT_SYMBOLIC_COUNTS','rows':rows,'total':sum(r['representatives'] for r in rows),
      'cpu_seconds':time.process_time()-start,'enumeration_complete':False,'potential_constructed':False}
    with (BASE/'representation_counts_v2.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
