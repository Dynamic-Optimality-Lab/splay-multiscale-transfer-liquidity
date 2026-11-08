"""Generic single-interior-gap finite profile machinery (exact ordered trees)."""
import sys,json,time
from functools import lru_cache
from pathlib import Path
from array import array
from collections import Counter
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
import splay as S
import verify_full_mixed as V
PORT=('leaf','opaque')
def iscore(k):return k%16==0 and 0<=k<=128
def hascore(t):return t[0]!='leaf' and (iscore(t[1]) or hascore(t[2]) or hascore(t[3]))
def collapse(t):return PORT if not hascore(t) else S.node(t[1],collapse(t[2]),collapse(t[3]))
def shadow(t):
    def at(path):
        n=t
        for side in path:
            if n[0]=='leaf':return (1,0,0)
            n=n[2+side]
        return (1,0,0) if n[0]=='leaf' else (0,int(iscore(n[1])),n[1]//16 if iscore(n[1]) else 0)
    return tuple(at(p) for p in ((),(0,),(1,),(0,0),(0,1),(1,0),(1,1)))
def visible(t):
    stack=[(t,0)]
    while stack:
        n,d=stack.pop()
        if n[0]=='leaf':continue
        if d in (1,2) and iscore(n[1]):yield n[1],d
        if d<2:stack.extend(((n[3],d+1),(n[2],d+1)))
def encode(t):return None if t[0]=='leaf' else [t[1],encode(t[2]),encode(t[3])]
def decode(t):return PORT if t is None else S.node(t[0],decode(t[1]),decode(t[2]))
def grammar(g):
    @lru_cache(None)
    def trees(lo,hi,m,start=0):
        if lo>hi:return (PORT,) if m==0 else ()
        ans=[]
        for k in range(lo,hi+1):
            lm,rm=(0,m) if k<g else (m,0)
            for l in trees(lo,k-1,lm,start if lm else 0):
                for r in trees(k+1,hi,rm,start if rm else 0):ans.append(S.node(16*k,l,r))
        if m and lo<=g<=hi+1:
            ll,lh=lo,min(hi,g-1);rl,rh=max(lo,g),hi
            for lm in range(m):
                rm=m-1-lm
                for l in trees(ll,lh,lm,start if lm else 0):
                    for r in trees(rl,rh,rm,start+lm+1 if rm else 0):ans.append(S.node(16*g-8+start+lm,l,r))
        return tuple(ans)
    return trees
def rho(alpha,g):
    a=tuple(tuple(r) for r in alpha)
    if len(a)!=7 or not a[0][1] or a[0][2] not in range(9):raise ValueError('root')
    a=((0,1,a[0][2]),)+a[1:]
    def bal(keys):return collapse(S.balanced([16*k for k in keys]))
    def at(p,keys,d):
        if not keys:return PORT
        k,ss,x=a[p]
        if k==1:return bal(keys)
        if k!=0:raise ValueError('empty/nonempty')
        if ss:
            if x not in keys:raise ValueError('core outside bounds')
            l=tuple(y for y in keys if y<x);r=tuple(y for y in keys if y>x);code=16*x
        else:
            l=tuple(y for y in keys if y<g);r=tuple(y for y in keys if y>=g)
            # An exposed anonymous cannot cross an ancestor S bound.
            if g<min(keys) or g>max(keys)+1:raise ValueError('gap outside interval')
            code=16*g-8+d
        if d==2:return S.node(code,bal(l),bal(r))
        li,ri=(1,2) if d==0 else ((3,4) if p==1 else (5,6))
        return S.node(code,at(li,l,d+1),at(ri,r,d+1))
    return shadow(at(0,tuple(range(9)),0))
def reflect_tree(t):return S.LEAF if t==S.LEAF else S.node(8-t[1],reflect_tree(t[3]),reflect_tree(t[2]))
def reflect_alpha(a):
    out=[]
    for p in (0,2,1,6,5,4,3):
        k,s,x=a[p];out.append([k,s,8-x if s and (p==0 or k==0) else x])
    return out
def build(g,folder):
    folder=Path(folder);out=folder/'catalog.json';assert not out.exists();start=time.process_time()
    bc=json.loads(Path('DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json').read_text());bt=[V.from_serial(r['tree']) for r in bc['nodes']];psi=[r['psi'] for r in bc['nodes']]
    tr=grammar(g);sh=[];sid={};opts=[];seen=[];witnesses=[];wid={};models=queries=0
    def ident(a):
        if a not in sid:sid[a]=len(sh);sh.append(a);opts.append([]);seen.append(set())
        return sid[a]
    for m in range(4):
        for t in tr(0,8,m):
            if not iscore(t[1]):continue
            models+=1;sa=shadow(t);assert rho(sa,g)==sa;ai=ident(sa)
            for x,h in visible(t):
                queries+=1;aa=shadow(collapse(S.trace(t,x)[0]));assert rho(aa,g)==aa;aj=ident(aa);key=(x//16,aj)
                if key not in seen[ai]:
                    seen[ai].add(key)
                    if t not in wid:wid[t]=len(witnesses);witnesses.append(encode(t))
                    opts[ai].append({'H':1,'target':x//16,'destination_shadow':aj,'witness':wid[t],'A_depth':h})
            assert queries<1000000 and models<2000000 and time.process_time()-start<120,'UNKNOWN profile cap'
    cache=tr.cache_info();tr.cache_clear();wid.clear()
    byroot={r:[i for i,s in enumerate(sh) if s[0]==(0,1,r)] for r in range(9)};local={ai:j for r in range(9) for j,ai in enumerate(byroot[r])}
    ob=array('H');aa=array('H');bases=[]
    for bi,t in enumerate(bt):
        bases.append(len(ob))
        for ai in byroot[t[1]]:ob.append(bi);aa.append(ai)
    assert len(ob)+models<2000000 and len(sh)<65536,'UNKNOWN state cap'
    cc=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json').read_text());arrays={'offsets':array('I',[0]),'targets':array('I'),'weights':array('b'),'meta':array('I')};cnt=Counter();safe=0
    for u,(bi,ai) in enumerate(zip(ob,aa)):
        for j,o in enumerate(opts[ai]):
            x=o['target'];h=cc['B_depth'][bi][x]
            if h==0:continue
            bj=cc['B_destination'][bi][x];w=2-h//2
            if w>=2:safe+=1;continue
            if len(arrays['targets'])==5000000:raise RuntimeError('UNKNOWN edge cap before append')
            v=bases[bj]+local[o['destination_shadow']];arrays['targets'].append(v);arrays['weights'].append(w);arrays['meta'].append(j);cnt[w]+=1
        arrays['offsets'].append(len(arrays['targets']))
        if u%8192==0:assert time.process_time()-start<120,'UNKNOWN graph cap'
    arrays.update(ordinary_a=aa,ordinary_b=ob)
    for n,a in arrays.items():
        with (folder/(n+'.bin')).open('xb') as f:a.tofile(f)
    c={'status':'BUILT_UNAUDITED','gap':g,'reflected_gap':9-g,'byteorder':sys.byteorder,'nodes':len(ob),'edges':len(arrays['targets']),
      'shadows':sh,'shadows_by_root':byroot,'low_options':opts,'witnesses':witnesses,'B_bases':bases,'psi':psi,
      'models':models,'source_case_queries':queries,'grammar_cache_entries':cache.currsize,'counts':dict(cnt),'range_safe':safe,'cpu_seconds':round(time.process_time()-start,3)}
    with out.open('x',encoding='utf-8') as f:json.dump(c,f,indent=2)
    print(json.dumps({k:v for k,v in c.items() if k not in ('shadows','shadows_by_root','low_options','witnesses','B_bases','psi')},indent=2),flush=True)
def load(folder):
    folder=Path(folder);c=json.loads((folder/'catalog.json').read_text());a={}
    for n,typ in {'ordinary_a':'H','ordinary_b':'H','offsets':'I','targets':'I','weights':'b','meta':'I'}.items():
        z=array(typ);z.frombytes((folder/(n+'.bin')).read_bytes())
        if c['byteorder']!=sys.byteorder:z.byteswap()
        a[n]=z
    return c,a
