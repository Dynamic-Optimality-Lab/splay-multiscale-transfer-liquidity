"""Original full BST semantics; graph encoding retains every physical vertex."""
import gzip
import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent


def readonly_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m


OLD=readonly_module('gso_pinned_physical',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/replay.py')
SOURCES=readonly_module('gso_pinned_sources',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/sources.py')
PARAM=readonly_module('gso_pinned_parameters',ROOT/'DO_RESEARCH_REBOOT/GLOBAL_ACCOUNTING_SYNTHESIS_20261121_V001/model.py')


def dump(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    if path.suffix=='.gz':
        with gzip.open(path,'wt',encoding='utf-8') as f:json.dump(value,f,separators=(',',':'))
    else:path.write_text(json.dumps(value,indent=2),encoding='utf-8')


def load(path):
    path=Path(path)
    with (gzip.open(path,'rt',encoding='utf-8') if path.suffix=='.gz' else path.open(encoding='utf-8')) as f:return json.load(f)


@lru_cache(maxsize=None)
def shapes(lo,hi):
    if lo>hi:return (None,)
    return tuple((k,l,r) for k in range(lo,hi+1) for l in shapes(lo,k-1) for r in shapes(k+1,hi))


def encode(t,n):
    out=[0]*(2*n+1);out[0]=t[0];stack=[t]
    while stack:
        k,l,r=stack.pop();out[2*k-1]=l[0] if l else 0;out[2*k]=r[0] if r else 0
        stack.extend(x for x in (l,r) if x)
    return tuple(out)


def json_state(t):
    return {'root':t[0],'children':{str(k):[t[2*k-1] or None,t[2*k] or None] for k in range(1,(len(t)+1)//2)}}


def original_splay(t,target):
    """Mutable parent-array splay; input/output encodings are full original trees."""
    n=(len(t)-1)//2;ch=[None]+[[t[2*k-1],t[2*k]] for k in range(1,n+1)];parent=[0]*(n+1);root=t[0]
    for k in range(1,n+1):
        for c in ch[k]:
            if c:parent[c]=k
    k=root;depth=0
    while k!=target:k=ch[k][int(target>k)];assert k;depth+=1
    def rotate(x):
        nonlocal root
        p=parent[x];g=parent[p];side=int(ch[p][1]==x);middle=ch[x][1-side]
        ch[p][side]=middle
        if middle:parent[middle]=p
        ch[x][1-side]=p;parent[p]=x;parent[x]=g
        if g:ch[g][int(ch[g][1]==p)]=x
        else:root=x
    while parent[target]:
        p=parent[target];g=parent[p]
        if not g:rotate(target)
        elif (p<g)==(target<p):rotate(p);rotate(target)
        else:rotate(target);rotate(target)
    return tuple([root]+[c for k in range(1,n+1) for c in ch[k]]),depth


def information(t):
    dep={};order=[];stack=[(t.root,0)]
    while stack:
        k,d=stack.pop();dep[k]=d;order.append(k);stack.extend((c,d+1) for c in t.ch[k] if c is not None)
    return dep,order


def frontier_features(A,B,guarded=False):
    da,oa=information(A);db,ob=information(B)
    def one(tree,depth,order):
        minima={};hist=[0,0,0]
        for k in reversed(order):
            l,r=tree.ch[k];m=min(depth[k],minima.get(l,10**30),minima.get(r,10**30));minima[k]=m
            if m<3:hist[m]+=1
            if depth[k]<3:hist[depth[k]]-=1
        return [hist[0],hist[0]+hist[1],sum(hist)]
    ab=one(B,da,ob);ba=one(A,db,oa)
    out=[z for pair in zip(ab,ba) for z in pair]
    assert out[0]==db[A.root] and out[1]==da[B.root] and min(out)>=0
    return out+[z*int(A.root==B.root) for z in out] if guarded else out


FEATURE_NAMES=[f'E{r}_{d}' for r in (1,2,3) for d in ('AB','BA')]


def source_from_cycle(graph,edge_ids,name):
    edges=graph['edges'];pairs=graph['pairs'];trees=graph['trees'];u=edges[edge_ids[0]][0];at=u
    for eid in edge_ids:
        e=edges[eid];assert e[0]==at;at=e[1]
    assert at==u
    prefix=[];cursor=u
    while graph['parents'][cursor] is not None:
        p,mode,key=graph['parents'][cursor];prefix.append([mode,key]);cursor=p
    prefix.reverse();ta,tb=pairs[u];d0,d1=pairs[cursor];assert d0==d1
    return {'name':name,'initial_A':json_state(trees[ta]),'initial_B':json_state(trees[tb]),'diagonal':json_state(trees[d0]),
            'prefix':prefix,'operations':[[edges[eid][4],edges[eid][5]] for eid in edge_ids],
            'expected_A':sum(edges[e][2] for e in edge_ids),'expected_Q':sum(edges[e][3] for e in edge_ids)}


def selected_replay(source,selected=None):
    keys=sorted(map(int,source['initial_A']['children']));trees={a:OLD.Tree(source['initial_'+a],keys) for a in ('A','B')}
    diagonal=source.get('diagonal')
    if diagonal is None:
        assert source['initial_A']==source['initial_B'] and not source.get('prefix');diagonal=source['initial_A']
    reach={a:OLD.Tree(diagonal,keys) for a in ('A','B')}
    for mode,x in source.get('prefix',[]):
        OLD.plain(reach['A'],x)
        if mode=='K':OLD.plain(reach['B'],x)
    assert all(reach[a].state()==source['initial_'+a] for a in ('A','B'))
    rows=[];A=Q=rot=0
    for op,(mode,x) in enumerate(source['operations'],1):
        save=selected is None or op in selected
        if save:before=frontier_features(trees['A'],trees['B'],True)
        bits=[]
        def run(actor):
            nonlocal rot
            tree=trees[actor];depth=len(tree.path(x))-1
            if not save:rot+=OLD.plain(tree,x);return depth
            j=0
            while tree.parent[x] is not None:
                j+=1;p=tree.parent[x];g=tree.parent[p]
                typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
                pivots=[x] if g is None else [p,x] if typ in ('LL','RR') else [x,x]
                for bit,k in enumerate(pivots):
                    parent=tree.parent[k];before=[tree.lo[k],tree.hi[k]];tree.rotate(k);rot+=1
                    bits.append({'id':[actor,op,j,bit],'type':typ,'promoted':k,'demoted':parent,'old_child_span':before,'new_demoted_span':[tree.lo[parent],tree.hi[parent]]})
            return depth
        da=run('A');db=run('B') if mode=='K' else 0
        a=(da+1)//2;q=db//2;A+=a;Q+=q
        if save:
            after=frontier_features(trees['A'],trees['B'],True)
            rows.append({'id':[source['name'],op],'mode':mode,'target':x,'a':a,'q':q,'before':before,'after':after,'delta':[v-u for u,v in zip(before,after)],'bits':bits})
    assert all(trees[a].state()==source['initial_'+a] for a in ('A','B'))
    if source.get('expected_A') is not None:assert A==source['expected_A']
    if source.get('expected_Q') is not None:assert Q==source['expected_Q']
    return {'source':source,'rows':rows,'A':A,'Q_B':Q,'period_rotations':rot,'full_pair_closure':True,'prefix_checked':True}
