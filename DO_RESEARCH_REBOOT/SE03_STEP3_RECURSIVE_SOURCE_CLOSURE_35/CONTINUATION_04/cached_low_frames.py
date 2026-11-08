"""Pinned source-action identities under arbitrary ordered term substitution.
NOT an uncharged fresh source-engine replay; see CF35 and CF35-2 proofs.
"""
import hashlib,json
from pathlib import Path
def freeze(t):return (t[0],freeze(t[1]),freeze(t[2])) if isinstance(t,list) else t
def node(t):return isinstance(t,tuple)
class Frames:
    def __init__(self,cache):
        self.cache_sha256=hashlib.sha256(cache.read_bytes()).hexdigest();n=json.loads(cache.read_text());trees=[freeze(t) for t in n['trees']];index={t:i for i,t in enumerate(trees)}
        self.templates={};self.applications=0
        def vine(k):return None if k>10 else (k,None,vine(k+1))
        def filler(t,k):
            if t is None:return None
            if t[0]==k:return (k,t[1],vine(k+1))
            return (t[0],filler(t[1],k),filler(t[2],k))
        def material(t):
            count=0
            def go(v):
                nonlocal count
                if v is None:z='F'+str(count);count+=1;return z
                return (v[0],go(v[1]),go(v[2]))
            out=go(t);assert count==11;return out
        for d in range(1,5):
            for mask in range(1<<d):
                dirs=tuple(1+(mask>>j&1) for j in range(d));counter=0;rank={}
                def comb(i):
                    if i==d:return (i,None,None)
                    sub=comb(i+1);return (i,sub,None) if dirs[i]==1 else (i,None,sub)
                def relabel(t):
                    nonlocal counter
                    if t is None:return None
                    l=relabel(t[1]);counter+=1;v=counter;rank[t[0]]=v;r=relabel(t[2]);return (v,l,r)
                bare=relabel(comb(0));k=d+1;src=material(filler(bare,k));sid=index[src];x=rank[d];tid=n['destination'][sid][x-1]
                assert n['H'][sid][x-1]==(d+1)//2
                def strip(v):
                    if isinstance(v,str):j=int(v[1:]);assert j<k;return '$'+str(j)
                    if v[0]==k+1:return '$'+str(k)
                    assert v[0]<=k;return (v[0],strip(v[1]),strip(v[2]))
                self.templates[dirs]={'native_source':sid,'native_target':tid,'target_rank':x,'H':(d+1)//2,
                    'source':strip(src),'target':strip(trees[tid])}
    def path(self,t,x):
        out=[]
        while node(t) and t[0]!=x:
            side=1 if x<t[0] else 2;out.append(side);t=t[side]
        assert node(t);return tuple(out)
    def apply(self,t,x):
        dd=self.path(t,x)
        if not dd:return t,0
        assert dd in self.templates
        template=self.templates[dd];active=[];v=t;active.append(v[0])
        for side in dd:v=v[side];active.append(v[0])
        keys=sorted(active);ss=set(active);ports=[]
        def collect(v):
            if not node(v) or v[0] not in ss:ports.append(v);return
            collect(v[1]);collect(v[2])
        collect(t);assert len(ports)==len(active)+1
        def instantiate(v):
            if isinstance(v,str):return ports[int(v[1:])]
            return (keys[v[0]-1],instantiate(v[1]),instantiate(v[2]))
        assert instantiate(template['source'])==t
        self.applications+=1;return instantiate(template['target']),template['H']
