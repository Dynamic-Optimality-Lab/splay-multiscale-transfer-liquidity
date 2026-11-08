"""Exhaustive core-topology diagnostic of the two dirty-negative path families."""
import sys,json,time
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path.insert(0,str(Path.cwd()/'DO_RESEARCH_REBOOT/M2_SEP01'))
from experiment import D,annotate,trace
from PC_B_CONTROLLER import verify_bpath
OUT=Path('DO_RESEARCH_REBOOT/M2_DSK01/static_partition.json')
assert not OUT.exists()
@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (None,)
    return tuple((r,L,R) for r in range(lo,hi) for L in trees(lo,r) for R in trees(r+1,hi))
start=time.process_time();total=compatible=rejected=checked=0;families=Counter();geometries=set();examples={}
for t in trees(0,9):
    raw={'root':t[0],'kl':[2]*19,'rl':[19]*19,'kr':[2]*19,'rr':[19]*19}
    par=[19]*9;dep=[0]*9;empty=[]
    def build(n,parent=19,depth=0):
        i,l,r=n;par[i]=parent;dep[i]=depth
        for child,k,f,side in ((l,'kl','rl','L'),(r,'kr','rr','R')):
            if child is None:empty.append((i,k,f,side))
            else:raw[k][i]=0;raw[f][i]=child[0];build(child,i,depth+1)
    build(t)
    for c,k,f,side in empty:
        m={a:list(v) if isinstance(v,list) else v for a,v in raw.items()}
        m[k][c]=0;m[f][c]=19
        for x in range(9):
            assert time.process_time()-start<120,'Static diagnostic cap: UNKNOWN'
            total+=1;node=x;path=[x];dirs=[];bad=None
            for j in range(18):
                parent=c if node==19 else par[node]
                direction=(side=='R') if node==19 else (
                    parent!=19 and m['kr'][parent]==0 and m['rr'][parent]==node)
                path.append(parent);dirs.append(direction)
                if parent<9 and ((not direction)!=(x<parent)) and bad is None:bad=j+1
                node=parent
            predicted=(side=='R' and x==c) or (side=='L' and c==x+1)
            assert (bad is None)==predicted,(x,c,side,path,dirs,bad)
            if not predicted:
                assert bad<=10,(x,c,side,bad)
                rejected+=1
            else:
                compatible+=1;family='RIGHT_SELF' if side=='R' else 'LEFT_SUCCESSOR'
                families[family]+=1
                target_path=[];node=x
                while node!=19:target_path.append(node);node=par[node]
                bits=[m['kr'][par[u]]==0 and m['rr'][par[u]]==u for u in target_path[:-1]]
                h=dep[x]
                if family=='LEFT_SUCCESSOR':
                    s=dep[c]-h
                    assert s>=1 and h+s<=8
                    if 0 in target_path:
                        z=target_path.index(0)
                        assert z==max((j+1 for j,v in enumerate(bits) if v),default=0)
                        mode='TARGET0' if z==0 else 'ANCESTOR0'
                    else:
                        assert h+s<=7;mode='OFF0'
                else:s=0;mode='NO_SENTINEL_CHILD_READ'
                key=(family,mode,h%2,s%2)
                if h>0 and key not in examples:
                    examples[key]={'family':family,'zero_case':mode,'h':h,'s':s,
                                   'source':annotate(m),'target':x,'claimant':c,'side':side}
            geom=(x,c,side,dep[x],dep[c])
            if geom not in geometries:
                geometries.add(geom);state=annotate(m);assert state is not None
                b,bt,_,_=trace(state,x,14)
                assert verify_bpath(D,b,bt,0).v==predicted,geom
                checked+=1
result={'status':'COMPLETE','core_trees':4862,'single_phantom_source_models':48620,
        'target_queries':total,'compatible_queries':compatible,'rejected_queries':rejected,
        'families':dict(families),'original_verify_bpath_checks':checked,
        'positive_control_sources':list(examples.values()),
        'cpu_seconds':round(time.process_time()-start,3),
        'scope':'finite zero-gap, single-phantom diagnostic; universal coverage requires the source reduction'}
with OUT.open('x',encoding='utf-8') as file:json.dump(result,file,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='positive_control_sources'}),flush=True)

