from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
sys.path.insert(0,str(PARENT))
import exp04_core as frozen
from exp04_core import *
ROOT=Path(__file__).resolve().parent
PARENT=ROOT.parent
frozen.ROOT=ROOT;frozen.prior.ROOT=ROOT
inherited_distortion.ROOT=ROOT;inherited_frame.ROOT=ROOT
from exp04_monotone import enriched
from exp04_density import density_analysis
from exp04_cycles import physical_lifecycles
from exp04_sources import scramble,omitted_family,ops,source


def write(name,obj):
    (ROOT/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')


def saved_witnesses():
    a=json.loads((PARENT/'EXP04_SOURCE_WITNESSES.json').read_text())
    return a['inherited_sources']+a['new_sources']


def both_oscillations(p=4,left=64,right=64,style='ordinary',return_to_two=True,right_low=1,q=1):
    base=omitted_family(p,2,(5,),q=q)
    n=len(base['initial_B']['children'])
    if style!='ordinary':
        targets=list(range(3,n+1))
        if style=='bitreverse':
            width=(n-1).bit_length();targets.sort(key=lambda x:int(f'{x:0{width}b}'[::-1],2))
        elif style=='alternating':
            original=targets;targets=[]
            while original:
                targets.append(original.pop(0))
                if original:targets.append(original.pop())
        else:raise ValueError(style)
        base['operations']=base['operations'][:2*n+2]+ops('K',targets)+ops('K',range(n-1,0,-1))
    old=base['operations'];cut=2*n+1
    L=ops('K',[1,n])*left+([['K',2]] if return_to_two else [])
    word=old[:cut]+L+[old[cut]]+ops('K',[right_low,n])*right+old[cut+1:]
    name=f'bothosc_p{p}_l{left}_r{right}_{style}_ret{int(return_to_two)}'
    if right_low!=1:name+=f'_low{right_low}'
    if q!=1:name+=f'_q{q}'
    return source(name,n,word,family='both_sided_oscillations',p=p,left=left,right=right,style=style,
        return_to_two=return_to_two,right_low=right_low,q=q)


def interval_cost(boundaries,initial,start,end):
    tree=Tree(initial);J=set();xs=[];A=0
    for i in range(start,end+1):
        row=boundaries[i];A+=row['a']
        if row['tag']=='K' and (not xs or xs[-1]!=row['x']):xs.append(row['x']);J.update(tree.path(row['x']))
    rank={x:i for i,x in enumerate(sorted(J))}
    L=sum(abs(rank[y]-rank[x]).bit_length() for x,y in zip(xs,xs[1:]))
    return {'J':sorted(J),'targets':xs,'L':L,'A':A,'D':len(J)+len(xs)+L}


if __name__=='__main__':
    meter=Meter('CONT01_inheritance_preflight')
    m=json.loads((PARENT/'EXP04_DELIVERY_MANIFEST.json').read_text())
    for p,h in m['files'].items():assert file_hash(PARENT/p)==h,p
    write('INPUT_MANIFEST.json',{'parent_delivery_manifest_sha256':file_hash(PARENT/'EXP04_DELIVERY_MANIFEST.json'),
        'parent_files':m['files'],'HEAD':m['HEAD'],'branch':m['branch'],
        'frozen_predicate_files':{p:file_hash(PARENT/p) for p in ('exp04_core.py','exp04_monotone.py','exp04_density.py','EXP04_THEOREM_LEDGER.md')}})
    meter.success=True;meter.details['verified_parent_files']=len(m['files'])
