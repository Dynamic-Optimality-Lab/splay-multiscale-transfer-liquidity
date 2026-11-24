"""Independent checker. Imports no new producer/compiler/learner code.

Old immutable rotations are a pinned read-only primitive library. Tree universe
uses insertion permutations; pruning uses a reverse-key leaf worklist; context
insertion uses recursive null-gap ordinals. Finite checking does not replace
the separately recorded arbitrary-subtree and all-parameter proofs.
"""
import bisect
import gzip
import hashlib
import heapq
import importlib.util
import itertools
import json
import sys
import time
from collections import Counter,defaultdict
from fractions import Fraction
from pathlib import Path
sys.dont_write_bytecode=True
sys.setrecursionlimit(20000)
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent
spec=importlib.util.spec_from_file_location('context_independent_immutable',ROOT/'DO_RESEARCH_REBOOT/COVER_FLOW_AUDIT_20261121_V001/verify.py')
V=importlib.util.module_from_spec(spec);sys.modules[spec.name]=V;spec.loader.exec_module(V)


def read(p):
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8')) as f:return json.load(f)


def raw(t):return None if t is None else (t.k,raw(t.l),raw(t.r))
def imm(t):return None if t is None else V.node(t[0],imm(t[1]),imm(t[2]))


def flat(t):
    if t is None:return (0,)
    ch={};stack=[t]
    while stack:
        v=stack.pop();ch[v.k]=[v.l.k if v.l else 0,v.r.k if v.r else 0];stack.extend(x for x in (v.l,v.r) if x)
    keys=sorted(ch);rank={k:i+1 for i,k in enumerate(keys)};rank[0]=0
    return tuple([rank[t.k]]+[rank[x] for k in keys for x in ch[k]])


def from_flat(e):
    def make(k):return V.node(k,make(e[2*k-1]),make(e[2*k])) if k else None
    return make(e[0])


def from_state(s):
    ch=s['children']
    def make(k):return V.node(k,*(make(c) if c is not None else None for c in ch[str(k)]))
    return make(s['root'])


def prune(a,b):
    def describe(t):
        ch={};pa={};stack=[(t,None)]
        while stack:
            v,p=stack.pop();ch[v.k]=[v.l.k if v.l else None,v.r.k if v.r else None];pa[v.k]=p
            stack.extend((c,v.k) for c in (v.l,v.r) if c)
        return ch,pa
    if a is None:return ((0,),(0,)),[],[]
    ca,pa=describe(a);cb,pb=describe(b);roots=[a.k,b.k];removed=[]
    heap=[-k for k in ca if ca[k]==[None,None] and cb[k]==[None,None]];heapq.heapify(heap)
    while heap:
        k=-heapq.heappop(heap)
        if k not in ca:continue
        assert ca[k]==cb[k]==[None,None];removed.append(k)
        for i,(ch,par) in enumerate(((ca,pa),(cb,pb))):
            p=par[k];del ch[k]
            if p is None:roots[i]=None
            else:ch[p][int(ch[p][1]==k)]=None
        for p in (pa[k],pb[k]):
            if p in ca and ca[p]==cb[p]==[None,None]:heapq.heappush(heap,-p)
    keys=sorted(ca);rank={k:i+1 for i,k in enumerate(keys)};rank[None]=0
    enc=lambda ch,r:tuple([rank[r]]+[rank[x] for k in keys for x in ch[k]])
    return (enc(ca,roots[0]),enc(cb,roots[1])),keys,removed


def ck(pair):return json.dumps(pair,separators=(',',':'))
def csize(pair):return (len(pair[0])-1)//2
def mu(a,b):return max(len(prune(a,b)[1])-1,0)


def insert(t,k):
    if t is None:return (k,None,None)
    return (t[0],insert(t[1],k),t[2]) if k<t[0] else (t[0],t[1],insert(t[2],k))


def universe(n):
    out=set()
    for perm in itertools.permutations(range(1,n+1)):
        t=None
        for k in perm:t=insert(t,k)
        out.add(t)
    return out


def path_shapes(n):
    answer=[]
    for t in universe(n):
        v=t
        while v:
            if v[1] and v[2]:break
            if v[1] is None and v[2] is None:answer.append((t,v[0]));break
            v=v[1] or v[2]
    assert len(answer)==2**(n-1)
    return answer


def gap_tree(t,m,gap,path,p):
    def shift(v):return None if v is None else (v[0]+gap,shift(v[1]),shift(v[2]))
    lifted=shift(path)
    def rec(v,lo,hi):
        if v is None:
            assert lo==hi
            return lifted if lo==gap else None
        k=v[0]
        return (k+(p if k>gap else 0),rec(v[1],lo,k-1),rec(v[2],k,hi))
    return imm(rec(t,0,m))


def gap_distance(t,gap):
    d=0;v=t;probe=gap+Fraction(1,2)
    while v:d+=1;v=v[1] if probe<v[0] else v[2]
    return d


def splay(t,x,emit=None,double=None):return V.rebuild(t,x,emit or (lambda *x:0),double or (lambda *x:None))


def verify_context(folder,limit,complete_patterns=False):
    g=read(folder/'CONTEXT_GRAPH.json.gz');z=read(folder/'CONTEXT_CERTIFICATE.json');p=z['upper_certificate']['potential_numerators'];den=z['upper_certificate']['potential_denominator'];C=Fraction(z['C'])
    cores={ck(tuple(map(tuple,q))):i for i,q in enumerate(g['pairs'])};assert len(cores)==len(g['pairs'])
    expected_cores={ck(((0,),(0,)))}
    universes={n:universe(n) for n in range(1,limit+1)}
    for n,trees in universes.items():
        for a in trees:
            for b in trees:
                q,keys,_=prune(imm(a),imm(b))
                if len(keys)==n:expected_cores.add(ck(q))
    assert expected_cores==set(cores)
    recorded={tuple(e[:4]) for e in g['edges']};assert len(recorded)==len(g['edges'])
    assert len(p)==len(cores) and all(den*q+p[v]-p[u]<=C*den*a for u,v,a,q in recorded)
    def row(a,b,x,mode):
        aa,da=splay(a,x);bb,db=splay(b,x) if mode=='K' else (b,0)
        pre=prune(a,b)[0];post=prune(aa,bb)[0]
        if csize(pre)>limit or csize(post)>limit:return None
        return (cores[ck(pre)],cores[ck(post)],(da+1)//2,db//2)
    for e,ref in zip(g['edges'],g['row_provenance']):
        if 'A' in ref:a,b=map(from_flat,(ref['A'],ref['B']))
        else:
            old=read(HERE.parent/'GSO_ENGINE_20261121_V001/run_001'/f"graph_{ref['support']}.json.gz")
            a=from_flat(old['trees'][ref['A_tree']]);b=from_flat(old['trees'][ref['B_tree']])
        assert row(a,b,ref['target'],ref['mode'])==tuple(e[:4])
    patterns=0
    if complete_patterns:
        generated=set();paths={n:path_shapes(n) for n in range(1,limit+1)}
        def add(a,b,x,mode):
            nonlocal patterns
            patterns+=1;r=row(a,b,x,mode)
            if r is not None:generated.add(r)
        for pair in g['pairs']:
            a,b=map(from_flat,pair);m=csize(pair)
            if m:
                for x in range(1,m+1):
                    for mode in ('D','K'):add(a,b,x,mode)
                ar,br=raw(a),raw(b)
                for gap in range(m+1):
                    for length in (1,2):
                        for t,x in paths[length]:add(gap_tree(ar,m,gap,t,length),gap_tree(br,m,gap,t,length),gap+x,'K')
                    for length in range(1,limit-gap_distance(br,gap)+1):
                        for t,x in paths[length]:add(gap_tree(ar,m,gap,t,length),gap_tree(br,m,gap,t,length),gap+x,'D')
            else:
                for length in range(1,limit+1):
                    for t,x in paths[length]:add(imm(t),imm(t),x,'D')
        assert generated==recorded and patterns==g['counters']['raw_context_rows']
    return {'limit':limit,'states':len(cores),'exact_inequalities':len(recorded),'independently_enumerated_context_patterns':patterns,'C':str(C),'potential_range':str(Fraction(max(p)-min(p),den))}


def rotate_at(t,k,direction):
    if t.k==k:return V.right(t) if direction=='R' else V.left(t)
    return V.node(t.k,rotate_at(t.l,k,direction),t.r) if k<t.k else V.node(t.k,t.l,rotate_at(t.r,k,direction))


def verify_source(file):
    z=read(file);s=z['source'];initial={act:from_state(s['initial_'+act]) for act in ('A','B')}
    if s.get('diagonal') is None:assert s['initial_A']==s['initial_B'] and not s.get('prefix')
    reach={act:from_state(s.get('diagonal') or s['initial_'+act]) for act in ('A','B')}
    for mode,x in s.get('prefix',[]):
        reach['A'],_=splay(reach['A'],x)
        if mode=='K':reach['B'],_=splay(reach['B'],x)
    assert all(raw(reach[a])==raw(initial[a]) for a in ('A','B'))
    genuine=set();prev=initial['B'].k
    for mode,x in s['operations']:
        if mode=='K':
            if x!=prev:genuine.add(x)
            prev=x
    support=set()
    for x in genuine:
        v=initial['B']
        while v:
            support.add(v.k)
            if v.k==x:break
            v=v.l if x<v.k else v.r
    S=sorted(support);assert S==z['original_S']
    def label(t):
        lo=bisect.bisect_left(S,t.lo);hi=bisect.bisect_right(S,t.hi)
        return (lo+1,hi) if hi>lo else None
    def census(t):
        result=Counter();stack=[t]
        while stack:
            v=stack.pop();lab=label(v)
            if lab:result[lab]+=1
            stack.extend(c for c in (v.l,v.r) if c)
        return result
    trees=initial.copy();counts={a:census(t) for a,t in trees.items()};aset=set(counts['A']);born=defaultdict(list);died=defaultdict(list);changes=defaultdict(list);doubles=[];clock=A=Q=rotations=0
    selected={r['op']:r for r in z['rows']};saved_bits={tuple(r['id']):r for r in z['selected_B_bits']};checked_bits=0;maxcore=0
    for op,(mode,x) in enumerate(s['operations'],1):
        core_before=len(prune(trees['A'],trees['B'])[1]);ma=mu(trees['A'],trees['B']);clock+=1
        depths={}
        for actor in ('A','B') if mode=='K' else ('A',):
            if actor=='B':clock+=1;postA=clock
            tracker=trees[actor]
            def emit(step,bit,typ,promoted,pivot,demoted):
                nonlocal clock,rotations,tracker,checked_bits
                clock+=1;rotations+=1;identifier=[actor,op,step,bit];old,new=label(promoted),label(demoted);labs={v for v in (old,new) if v};before={v:counts[actor][v] for v in labs}
                if old:counts[actor][old]-=1
                if new:counts[actor][new]+=1
                lost={v for v in labs if before[v] and not counts[actor][v]};gain={v for v in labs if not before[v] and counts[actor][v]}
                if actor=='A':
                    for v in lost:changes[v].append((clock,False,identifier))
                    for v in gain:changes[v].append((clock,True,identifier))
                    return 0
                assert len(lost)==len(gain)==1
                for v in lost:died[v].append((clock,identifier))
                for v in gain:born[v].append((clock,identifier))
                neutral=not any(counts['A'][v] for v in gain)
                if op in selected:
                    old_mu=mu(trees['A'],tracker);tracker=rotate_at(tracker,pivot.k,'R' if promoted.k<pivot.k else 'L');new_mu=mu(trees['A'],tracker)
                    saved=saved_bits[tuple(identifier)]
                    assert saved['kappa_before']==old_mu and saved['kappa_after']==new_mu and saved['neutral']==neutral
                    assert new_mu<=old_mu and (not neutral or new_mu==old_mu);checked_bits+=1
                return -int(not neutral)
            def double(step,typ,span,left,right):
                if actor=='B':
                    lo=bisect.bisect_left(S,span[0]);hi=bisect.bisect_right(S,span[1]);doubles.append({'id':[op,step],'F':(lo+1,hi),'neutral':left==right==0,'postA':postA})
            trees[actor],depth=splay(trees[actor],x,emit,double);depths[actor]=depth
            assert +counts[actor]==census(trees[actor])
            if actor=='A':
                A+=(depth+1)//2;core_mid=len(prune(trees['A'],trees['B'])[1]);assert max(core_mid-1,0)-ma<=depth
            else:
                Q+=depth//2
                if op in selected:assert raw(tracker)==raw(trees['B'])
        if mode!='K':clock+=1
        clock+=1;core_after=len(prune(trees['A'],trees['B'])[1]);maxcore=max(maxcore,core_before,core_after)
        if mode=='K':assert core_after<=core_mid
        if op in selected:
            r=selected[op];assert (r['before_core'],r['post_A_core'],r['after_core'],r['A_depth'],r['B_depth'])==(core_before,core_mid,core_after,depths['A'],depths.get('B',0))
    assert all(raw(trees[a])==raw(initial[a]) for a in ('A','B')) and (A,Q,maxcore)==(z['A'],z['Q_B'],z['maximum_boundary_core'])
    def previous(seq,end):
        lap,local=divmod(end,clock);i=bisect.bisect_left([t for t,_ in seq],local)-1
        if i<0:lap-=1;i=len(seq)-1
        t,e=seq[i];return t+lap*clock,e
    demands=[]
    for d in doubles:
        f=d['F'];end=d['postA']
        if not d['neutral'] or f[0]<=1 or f[1]>=len(S):continue
        gamma,gid=previous(born[f],end);kap,kid=previous(died[f],gamma);pos=bisect.bisect_right([t for t,_,_ in changes[f]],kap%clock)-1
        present=changes[f][pos][1] if pos>=0 else f in aset
        exposed=present or any(v and kap<t+lap*clock<=end for t,v,_ in changes[f] for lap in (-1,0))
        if not exposed:demands.append({'id':d['id'],'F':list(f),'Gamma':gid,'kappa':kid,'Gamma_clock':gamma,'kappa_clock':kap,'postA':end,'span':[S[f[0]-1],S[f[1]-1]]})
    assert demands==z['original_U']
    assert checked_bits==len(saved_bits)
    return {'name':s['name'],'operations':len(s['operations']),'real_rotations':rotations,'A':A,'Q_B':Q,'literal_U':len(demands),'selected_bits':checked_bits,'maximum_boundary_core':maxcore,'full_Pi_and_reaching_prefix_checked':True}


def main():
    start=time.process_time();contexts=[verify_context(HERE/'run_001',3),verify_context(HERE/'core5_001',5,True)]
    sources=[verify_source(p) for p in sorted((HERE/'sources_001').glob('source_*.json.gz'))]
    result={'passed':True,'contexts':contexts,'sources':sources,'operations':sum(x['operations'] for x in sources),'real_rotations':sum(x['real_rotations'] for x in sources),'literal_U':sum(x['literal_U'] for x in sources),'cpu_seconds':time.process_time()-start,'independence':'No new producer/compiler/teacher imports; pinned immutable rotations, insertion-permutation universe, reverse-key worklist pruning, recursive gap insertion, full original cyclic Pi reconstruction. Same agent, not external peer review or complete formal verification.','symbolic_scope':'The arbitrary-subtree compression, global growth lemma and all-q obstruction require the explicit mathematical proof; finite agreement alone is not that proof.'}
    if not (HERE/'FINAL_MANIFEST.json').exists():(HERE/'INDEPENDENT_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result))


if __name__=='__main__':main()
