import importlib.util
import sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent.parent


def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m


OLD=module('accounting_readonly_physical',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/replay.py')
SRC=module('accounting_readonly_sources',ROOT/'DO_RESEARCH_REBOOT/INTERNAL_PIVOT_DONOR_20261121_V001/sources.py')
REF=module('accounting_readonly_functional',ROOT/'python/independent/splay.py')
NAMES=['C_AB','C_BA','depth_sum_A','depth_sum_B','depth_B_of_A_root','depth_A_of_B_root','full_X_SET_discordance','physical_edge_discordance','Mersenne_defect','full_X_size_weighted_defect']


def depths_order(t):
    out={};order=[];stack=[(t.root,0)]
    while stack:
        k,d=stack.pop();out[k]=d;order.append(k)
        stack.extend((c,d+1) for c in t.ch[k] if c is not None)
    return out,order


def cross(t,weights,order):
    minima={};total=0
    for k in reversed(order):
        l,r=t.ch[k];v=min(weights[k],minima.get(l,10**20),minima.get(r,10**20));minima[k]=v;total+=v
    return sum(weights.values())-total


def features(A,B):
    da,oa=depths_order(A);db,ob=depths_order(B)
    cab=cross(B,da,ob);cba=cross(A,db,oa)
    la={A.label(k) for k in A.keys};lb={B.label(k) for k in B.keys};missing=lb-la
    ea={(k,c,s) for k in A.keys for s,c in enumerate(A.ch[k]) if c is not None}
    eb={(k,c,s) for k in B.keys for s,c in enumerate(B.ch[k]) if c is not None}
    mersenne=-sum(hi-lo+1>=3 and not ((hi-lo+1)&(hi-lo+2)) for lo,hi in missing)
    out=[cab,cba,sum(da.values()),sum(db.values()),db[A.root],da[B.root],len(missing),len(eb-ea),mersenne,sum(hi-lo+1 for lo,hi in missing)]
    assert cab>=0 and cba>=0
    if cab==0 or cba==0:assert cab==cba==0 and A.root==B.root and A.ch==B.ch
    return tuple(out)


def step(tree,x):
    depth=len(tree.path(x))-1;OLD.plain(tree,x);return depth


def H(p,q):
    n=2**(p+1)*(q+1)+1;marked={n+1-2**j for j in range(p+1)}
    word=[['D',x] for x in range(2,n+1)]+[['K' if x in marked else 'D',x] for x in range(n,0,-1)]
    word += [['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    v=SRC.vine(n)
    return {'name':f'H_{p}_{q}','initial_A':v,'initial_B':v,'operations':word,'prefix':[],'diagonal':v,'p':p,'q':q,'expected_A':4*(n-1)}


def family(s,kind):
    n=2**s+2;v=SRC.vine(n);T={'root':2,'children':dict(v['children'])};T['children']=dict(T['children']);T['children']['1']=[None,None];T['children']['2']=[1,3]
    reset=[['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    if kind=='F1':A,B=v,T;prefix=[['K',2],['D',1]];word=[['D',2],['D',1]]+reset+prefix
    elif kind=='F2':A=B=v;prefix=[];word=[['D',2],['D',1]]+reset
    else:A=B=v;prefix=[];word=[['K',2],['K',1]]+reset
    return {'name':f'{kind}_s{s}','initial_A':A,'initial_B':B,'operations':word,'prefix':prefix,'diagonal':v}


def F4(s):
    k=2**s;n=2*k-1;v=SRC.vine(n);prefix=[['D',x] for x in range(2,k)]
    tmp=OLD.Tree(v,list(range(1,n+1)))
    for _,x in prefix:step(tmp,x)
    reset=[['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    return {'name':f'F4_s{s}','initial_A':tmp.state(),'initial_B':v,'operations':[['D',k],['D',k-1]]+reset+prefix,'prefix':prefix,'diagonal':v,'k':k}


def compressed(q):
    n=16*(q+1)+1;v=SRC.vine(n)
    word=[['D',x] for x in range(2,n+1)]+[['K',n],['K',n-1],['K',n-3],['K',n-7]]
    word += [['K',x] for x in range(1,n+1)]+[['K',x] for x in range(n-1,0,-1)]
    return {'name':f'compressed_H3_q{q}','initial_A':v,'initial_B':v,'operations':word,'prefix':[],'diagonal':v,'q':q}
