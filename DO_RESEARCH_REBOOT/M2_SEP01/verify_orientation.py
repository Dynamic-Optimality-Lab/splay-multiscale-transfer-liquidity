"""Finite diagnostic for the first static conflict, not a universal graph search."""
import sys,json,time
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path.insert(0,str(Path(__file__).parent))
from experiment import D,V,pack,annotate,trace
from PC_B_CONTROLLER import verify_bpath
OUT=Path('DO_RESEARCH_REBOOT/M2_SEP01/orientation_controls.json')
assert not OUT.exists()
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (None,)
    return tuple((r,L,R) for r in range(lo,hi)
                 for L in trees(lo,r) for R in trees(r+1,hi))
start=time.process_time();total=ordinary=special=checked=0;hist=Counter();geometries=set()
for t in trees(0,9):
    raw={'root':t[0],'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    parents=[19]*9;depths=[0]*9;empty=[]
    def build(n,p=19,z=0):
        if n is None:return
        i,l,r=n;parents[i]=p;depths[i]=z
        for child,k,f,side in ((l,'kl','rl','L'),(r,'kr','rr','R')):
            if child is None:empty.append((i,k,f,side))
            else:raw[k][i]=0;raw[f][i]=child[0];build(child,i,z+1)
    build(t)
    assert len(empty)==10
    for c,k,f,side in empty:
        assert time.process_time()-start<120,'CPU cap: diagnostic incomplete'
        total+=1
        if c==8 and side=='R':special+=1;continue
        m={a:(list(v) if isinstance(v,list) else v) for a,v in raw.items()}
        m[k][c]=0;m[f][c]=19
        path=[8];dirs=[];node=8;firstbad=None
        for j in range(18):
            par=c if node==19 else parents[node]
            direction=(side=='R') if node==19 else (
                par!=19 and m['kr'][par]==0 and m['rr'][par]==node)
            dirs.append(direction);path.append(par)
            if par<9 and not direction and firstbad is None:firstbad=j+1
            node=par
        assert firstbad is not None and firstbad<=10,(t,c,side,path,dirs)
        ordinary+=1;hist[firstbad]+=1
        aset=set();node=8
        while node!=19:aset.add(node);node=parents[node]
        node=c
        while node not in aset:node=parents[node]
        lca=node
        geom=(depths[8],depths[c],depths[lca],c,side)
        if geom not in geometries:
            geometries.add(geom)
            state=annotate(m);assert state is not None
            b,bt,_,_=trace(state,8,10)
            assert not verify_bpath(D,b,bt,0).v,geom
            checked+=1
result={'status':'COMPLETE','core_trees':len(trees(0,9)),
        'single_phantom_states':total,'chi8_states_covered_by_other_certificate':special,
        'complement_states_static_rejected_at_d10':ordinary,
        'first_bad_path_entry_histogram':dict(sorted(hist.items())),
        'original_verify_bpath_geometry_checks':checked,
        'cpu_seconds':round(time.process_time()-start,3),
        'scope':'finite zero-gap single-phantom diagnostic; universal conclusion requires source path-union proof'}
with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))

