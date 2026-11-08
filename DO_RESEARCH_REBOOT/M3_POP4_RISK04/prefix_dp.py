"""Exact retained-population prefix DP; F colors are private existential choices."""
import sys,json,time
from pathlib import Path
from itertools import product
from functools import lru_cache
sys.path.insert(0,'DO_RESEARCH_REBOOT/M3_UNITPAIR01')
from profiles import specification,PATHS
BASE=Path('DO_RESEARCH_REBOOT/M3_POP4_RISK04')
CPU_CAP=min(120,float(sys.argv[11])) if len(sys.argv)>11 else 120
CASES=tuple(map(tuple,json.loads((BASE/'targets.json').read_text())['canonical_signatures']))
SELECTOR=json.loads((BASE.parent/'M3_POP3_RISK01/risk_selector.json').read_text())
RISK={k:set(map(tuple,v)) for k,v in SELECTOR['risk'].items()}
PLANS={(p['helper'],tuple(map(tuple,p['word']))):tuple(p['terminal_source_address']) for p in SELECTOR['plans']}
P=-1;G=-2;F=9
def families(sig):
    for p in PATHS:yield None,(p,)
    for gap in (0,9):
        if sig[gap]:
            for p,q in product(PATHS,repeat=2):yield gap,(p,q)
@lru_cache(None)
def splits(counts):
    return tuple((left,tuple(n-x for n,x in zip(counts,left))) for left in product(*(range(n+1) for n in counts)))
class PrefixDP:
    def __init__(self,sigma,helper,word,start):
        self.sigma=tuple(sigma);self.helper=helper;self.word=word;self.start=start
        self.observed,self.required,forced=specification(helper,word)
        self.forced={p:('core' if v is None else helper) for p,v in forced.items()}
        self.target_address=PLANS[helper,tuple(word)];self.risky=RISK['H1' if helper is None else str(helper)];self.root_joins=0;self.analytic_rejections=0
        self.nodes=[];self.ids={};self.cache={};self.cached=0;self.working=0;self.root_members=0;self.peak=0;self.operations=0
    def guard(self):
        live=len(self.nodes)+self.cached+self.working+self.root_members;self.peak=max(self.peak,live)
        if live>=2000000:raise RuntimeError('live DP record cap')
        if len(self.nodes)>=4000000:raise RuntimeError('DP DAG node cap')
        if time.process_time()-self.start>=CPU_CAP:raise RuntimeError('finite CPU cap')
    def node(self,label,left,right):
        key=(label,left,right);n=self.ids.get(key)
        if n is None:n=len(self.nodes);self.ids[key]=n;self.nodes.append(key)
        return n
    def add(self,result,node):
        if node not in result:
            result.add(node);self.working+=1;self.operations+=1
            if self.operations%2048==0:self.guard()
    def admit_root(self,k,left,right):
        self.root_joins+=1
        if self.root_joins%2048==0:self.guard()
        if not self.target_address:x=k
        else:
            n=(left,right)[self.target_address[0]]
            for side in self.target_address[1:]:
                assert n>=0,'required terminal ancestor must be real'
                n=self.nodes[n][1+side]
            assert n>=0;x=self.nodes[n][0];assert x<9
        ok=(k,x) in self.risky
        if not ok:self.analytic_rejections+=1
        return ok
    def dp(self,p,lo,hi,mask,counts):
        if any(n and (not(mask>>g&1) or not lo<=g<=hi+1) for g,n in enumerate(counts)):return frozenset()
        key=(p,lo,hi,mask,counts)
        old=self.cache.get(key)
        if old is not None:return old
        if p not in self.observed:
            ans=frozenset((P,)) if not any(counts) else frozenset();self.cache[key]=ans;self.cached+=len(ans);return ans
        result=set();kind=self.forced.get(p,'any')
        if p not in self.required and not any(counts):
            self.add(result,P)
            if lo>hi:self.add(result,G)
        if kind in ('any','core'):
            for k in range(lo,hi+1):
                lm=mask & sum(1<<g for g in range(10) if g<=k);rm=mask & sum(1<<g for g in range(10) if g>k)
                for lc,rc in splits(counts):
                    left=self.dp(p+(0,),lo,k-1,lm,lc)
                    if not left:continue
                    right=self.dp(p+(1,),k+1,hi,rm,rc)
                    for l in left:
                        for r in right:
                            if p==() and not self.admit_root(k,l,r):continue
                            self.add(result,self.node(k,l,r))
        if kind!='core':
            for gap,n in enumerate(counts):
                if n==0 or not mask>>gap&1 or not lo<=gap<=hi+1 or (kind!='any' and kind!=gap):continue
                remaining=list(counts);remaining[gap]-=1;lm=mask & ((1<<(gap+1))-1);rm=mask & ~((1<<gap)-1)
                for lc,rc in splits(tuple(remaining)):
                    left=self.dp(p+(0,),lo,gap-1,lm,lc)
                    if not left:continue
                    right=self.dp(p+(1,),gap,hi,rm,rc)
                    for l in left:
                        for r in right:self.add(result,self.node(F,l,r))
        self.working-=len(result);ans=frozenset(result);self.cached+=len(ans);self.cache[key]=ans;return ans
    def roots(self):
        roots=set()
        for counts in product(*(range(n+1) for n in self.sigma)):
            for n in self.dp((),0,8,1023,counts):
                if n not in roots:roots.add(n);self.root_members+=1
            self.guard()
        self.cache.clear();self.cached=0;return roots
    def move(self,n,path):
        label,l,r=self.nodes[n]
        def rr(x):
            k,a,b=self.nodes[x];q,c,d=self.nodes[a];return self.node(q,c,self.node(k,d,b))
        def rl(x):
            k,a,b=self.nodes[x];q,c,d=self.nodes[b];return self.node(q,self.node(k,a,c),d)
        if len(path)==1:return rr(n) if path[0]==0 else rl(n)
        a,b=path
        if a==b:return rr(rr(n)) if a==0 else rl(rl(n))
        return rr(self.node(label,rl(l),r)) if a==0 else rl(self.node(label,l,rr(r)))
    def find(self,n,label):
        if n<0:return None
        k,l,r=self.nodes[n]
        if k==label:return n
        a=self.find(l,label);return a if a is not None else self.find(r,label)
    def alpha(self,n,owner):
        zero=self.find(n,owner);assert zero is not None;out=[]
        for path in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)):
            a=n
            for side in path:
                if a==P:break
                if a==G:a=zero
                a=self.nodes[a][1+side]
            if a==P:out.append((1,0,0))
            else:
                if a==G:a=zero
                k=self.nodes[a][0];out.append((0,1,k) if k<9 else (0,0,0))
        return tuple(out)
    def code(self,n):
        if n==P:return 'a'
        if n==G:return 'b'
        label,l,r=self.nodes[n];return format(label,'x')+self.code(l)+self.code(r)
def main():
    sigma=tuple(map(int,sys.argv[1:11]));assert sigma in CASES;folder=BASE/('s'+''.join(map(str,sigma)));folder.mkdir(exist_ok=False);start=time.process_time()
    out=folder/'build_status.json';sh=[];sid={};opts=[];seen=[];cases=[];queries=edges=peak=joins=rejections=0;reason=None
    def ident(a):
        if a not in sid:sid[a]=len(sh);sh.append(a);opts.append([]);seen.append(set())
        return sid[a]
    try:
        for helper,word in families(sigma):
            dp=PrefixDP(sigma,helper,word,start);roots=dp.roots();n=len(roots);peak=max(peak,dp.peak);joins+=dp.root_joins;rejections+=dp.analytic_rejections
            if queries+n>1000000:raise RuntimeError('canonical source-query cap')
            if not n:continue
            fi=len(cases);cases.append({'helper':helper,'word':word,'count':n})
            for root in roots:
                owner=dp.nodes[root][0];a=ident(dp.alpha(root,owner));dst=root
                for path in word:dst=dp.move(dst,path)
                b=ident(dp.alpha(dst,owner));target=dp.nodes[dst][0];assert target<9;H=len(word);key=(H,target,b,helper)
                if key not in seen[a]:
                    seen[a].add(key);opts[a].append([H,target,b,helper,fi,dp.code(root)]);edges+=1
                queries+=1
                if queries%4096==0:
                    dp.guard();peak=max(peak,dp.peak)
                    if len(sh)+len(dp.nodes)+len(roots)>=2000000 or edges>=5000000:raise RuntimeError('live profile/edge cap')
            print(json.dumps({'sigma':sigma,'helper':helper,'word':word,'profiles':n,'total_queries':queries,'classes':len(sh),'options':edges,'CPU':round(time.process_time()-start,3)}),flush=True)
    except RuntimeError as e:reason=str(e)
    result={'status':'UNKNOWN_CAP' if reason else 'COMPLETE_RISK_GUARDED_PREFIX_RELATION_UNAUDITED','sigma':sigma,'reason':reason,'queries':queries,'private_root_production_visits':joins,'analytic_root_production_rejections':rejections,
      'classes':len(sh),'option_count':edges,'peak_DP_records':peak,'allocated_CPU_cap':CPU_CAP,'cpu_seconds':round(time.process_time()-start,3),'families':cases,'full_M3_proved':False}
    if not reason:
        with (folder/'relation.json').open('x',encoding='utf-8') as f:json.dump({**result,'shadows':sh,'options':opts},f,separators=(',',':'))
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:
        main()
    except BaseException as exc:
        error={'type':type(exc).__name__,'message':str(exc)}
        raise
    finally:
        phase_exit=BASE/('s'+''.join(sys.argv[1:11]))/'prefix_dp_exit.json'
        payload={'whole_process_CPU_seconds':time.process_time(),'error':error,'per_phase_cap':CPU_CAP,'mathematical_checks_changed':False}
        with phase_exit.open('x',encoding='utf-8') as f:json.dump(payload,f,indent=2)

