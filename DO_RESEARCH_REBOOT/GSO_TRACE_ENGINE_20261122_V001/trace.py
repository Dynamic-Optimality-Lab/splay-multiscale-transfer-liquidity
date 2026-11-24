"""Exact original StepEv / interval rotation / external-port compiler.

The old physical source kernel is read-only. Projected traces are never called
ordinary local splays. Every original B double costs one, including zero-mask
and one-mask projections. Named outside endpoints remain in port records.
"""
import sys
import json
from pathlib import Path
from collections import Counter
sys.dont_write_bytecode=True
sys.setrecursionlimit(20000)
HERE=Path(__file__).resolve().parent
PREV=HERE.parent/'GSO_COMPOSITION_AUDIT_20261121_V001'
sys.path.insert(0,str(PREV));import composition as C;sys.path.pop(0)
K=C.K


def write(name,value):
    assert not (HERE/'FINAL_MANIFEST.json').exists(),'sealed output'
    p=HERE/name;assert not p.exists(),'use a fresh artifact name'
    K.dump(p,value)


def partition(keys,width):
    return [keys[i:i+width] for i in range(0,len(keys),width)]


def block_view(step,part,block):
    """An annotated view of one original step, never a local splay request."""
    target=step['target'];where='inside' if part[0]<=target<=part[-1] else 'below' if target<part[0] else 'above'
    return {'original_id':step['id'],'actor':step['actor'],'mode':step['mode'],'type':step['type'],'target':target,'target_position':where,'mask':step['retained_bit_masks'].get(str(block),[0]*len(step['bits'])),'original_cost':{'a':step['a'],'q':step['q']},'original_pairing_retained':True,'warning':'The cost is attached to the original ID and must not be summed once per view.'}


def ports(t,part,owner):
    answer=[];i=owner[part[0]]
    for x in part:
        p=t.parent[x]
        if p is None:answer.append(['root',x])
        elif owner[p]!=i:answer.append(['in',p,x,'L' if x<p else 'R'])
        for side,h in enumerate(t.ch[x]):
            if h is not None and owner[h]!=i:answer.append(['out',x,h,'LR'[side]])
    return sorted(answer,key=str)


def descriptor(t,part,owner):
    return {'tree':C.project(t.state(),part[0],part[-1]),'ports':ports(t,part,owner)}


def anonymous(t,part,owner):
    """Finite block observer: local shape + relative exterior stubs, not IDs.

    Arbitrary joint functions of the A/B observer are learned. The named-port
    trace is richer and is retained even when this scoped observer fails.
    """
    rank={x:i for i,x in enumerate(part)};idx=owner[part[0]]
    def ref(x):
        if x is None:return 'nil'
        return rank[x] if owner[x]==idx else 'lo' if x<part[0] else 'hi'
    def proj(x):
        if x is None:return None
        left,right=t.ch[x]
        if x<part[0]:return proj(right)
        if x>part[-1]:return proj(left)
        return (x,proj(left),proj(right))
    shape=proj(t.root)
    def rel(z):return [rank[z[0]],rel(z[1]),rel(z[2])] if z else None
    stubs=[[ref(t.parent[x]),ref(t.ch[x][0]),ref(t.ch[x][1])] for x in part]
    return [rel(shape),stubs]


def signature(trees,part,owner):
    return json.dumps([len(part),anonymous(trees['A'],part,owner),anonymous(trees['B'],part,owner)],separators=(',',':'))


def histogram(trees,blocks,owner):
    return Counter(signature(trees,p,owner) for p in blocks)


def compile_source(source,width=5,explicit_blocks=None):
    original=K.OLD.replay(source)
    keys=sorted(original['keys']);blocks=explicit_blocks or partition(keys,width)
    assert all(p==list(range(p[0],p[-1]+1)) for p in blocks)
    owner={x:i for i,p in enumerate(blocks) for x in p};assert len(owner)==len(keys) and set(owner)==set(keys)
    trees={a:K.OLD.Tree(source['initial_'+a],original['S']) for a in ('A','B')}
    steps=[];operations=[];total_ports=0;R_A=0
    def desc(scope):return {str(i):{a:descriptor(trees[a],blocks[i],owner) for a in ('A','B')} for i in sorted(scope)}
    for op,(mode,x) in enumerate(source['operations'],1):
        before_hist=histogram(trees,blocks,owner)
        before_full={a:trees[a].state() for a in trees}
        start=len(steps);da=len(trees['A'].path(x))-1;db=len(trees['B'].path(x))-1 if mode=='K' else 0
        k=int(mode=='K' and db>0)
        for actor in ('A','B') if mode=='K' else ('A',):
            t=trees[actor];j=0
            while t.parent[x] is not None:
                j+=1;p=t.parent[x];g=t.parent[p]
                typ='ZIG' if g is None else ('L' if p<g else 'R')+('L' if x<p else 'R')
                pivots=[x] if g is None else [p,x] if typ in ('LL','RR') else [x,x]
                # Precompute the complete physical step, retaining the original
                # two-rotation order and opaque hanging subtrees in the tree.
                old={a:trees[a].state() for a in trees};bits=[];scope=set()
                before_sig={i:signature(trees,part,owner) for i,part in enumerate(blocks)}
                for bit,y in enumerate(pivots):
                    parent=t.parent[y];grand=t.parent[parent]
                    middle=t.ch[y][int(y<parent)]
                    footprint={owner[z] for z in (y,parent,grand,middle) if z is not None}
                    bp={i:ports(t,blocks[i],owner) for i in footprint}
                    event=t.rotate(y)
                    ap={i:ports(t,blocks[i],owner) for i in footprint}
                    packet=[{'block':i,'before':bp[i],'after':ap[i]} for i in sorted(footprint) if bp[i]!=ap[i]]
                    assert len(packet)<=4
                    inside=owner[y] if owner[y]==owner[parent] else None
                    bits.append({'id':[actor,op,j,bit],'promoted':y,'demoted':parent,'grandparent':grand,'middle':middle,'internal_block':inside,'footprint':sorted(footprint),'port_packets':packet})
                    scope|=footprint
                    if actor=='A':total_ports+=len(packet);R_A+=1
                now={a:trees[a].state() for a in trees}
                # Descriptors of unmodified blocks cannot change. This catches
                # an omitted outside endpoint before it reaches the optimizer.
                after_sig={i:signature(trees,part,owner) for i,part in enumerate(blocks)}
                assert all(before_sig[i]==after_sig[i] for i in range(len(blocks)) if i not in scope)
                before_desc={str(i):{a:{'tree':C.project(old[a],blocks[i][0],blocks[i][-1])} for a in trees} for i in sorted(scope)}
                inside=[b['internal_block'] for b in bits]
                assert len({i for i in inside if i is not None})<=1
                steps.append({'id':[actor,op,j],'actor':actor,'mode':mode,'target':x,'type':typ,'a':int(actor=='A'),'q':int(actor=='B' and len(bits)==2),'k':0,'scope':sorted(scope),'bits':bits,'retained_bit_masks':{str(i):[int(v==i) for v in inside] for i in sorted(scope)},'before_local':{i:{a:v['tree'] for a,v in z.items()} for i,z in before_desc.items()},'after_local':{str(i):{a:C.project(now[a],blocks[i][0],blocks[i][-1]) for a in trees} for i in sorted(scope)},'signature_before':{str(i):before_sig[i] for i in scope},'signature_after':{str(i):after_sig[i] for i in scope}})
        after_hist=histogram(trees,blocks,owner);delta=after_hist.copy();delta.subtract(before_hist);delta={s:v for s,v in delta.items() if v}
        operations.append({'id':op,'mode':mode,'target':x,'a':(da+1)//2,'q':db//2,'k':k,'steps':[start,len(steps)],'delta':delta,'full_before':before_full,'full_after':{a:trees[a].state() for a in trees},'local_only_unchanged':all(C.project(before_full[a],p[0],p[-1])==C.project(trees[a].state(),p[0],p[-1]) for a in trees for p in blocks)})
    assert all(trees[a].state()==source['initial_'+a] for a in trees)
    A=sum(s['a'] for s in steps);Q=sum(s['q'] for s in steps);KB=sum(r['k'] for r in operations)
    assert A==original['A'] and Q==original['Q_B'] and KB<=A and R_A<=2*A and total_ports<=4*R_A
    return {'schema':'GSO.original-trace-ports.v1','source':source,'blocks':blocks,'width':width,'A':A,'Q_B':Q,'K_B':KB,'R_A':R_A,'A_port_packets':total_ports,'original_S':original['S'],'original_U':original['demands'],'steps':steps,'operations':operations,'closure':True,'reaching_prefix_checked':True,'scope':'Full original source. Anonymous signatures are a deliberately restricted learner observer; named ports and literal original events are retained.'}


def basic_build():
    z=K.load(PREV/'source_02.json.gz')
    out=compile_source(z['source'],explicit_blocks=z['blocks'])
    write('bootstrap/trace_noncommutation.json.gz',out)
    write('bootstrap/WORKING_UPGRADE.json',{'status':'WORKING_TRACE_BACKEND','source':out['source']['name'],'A':out['A'],'Q_B':out['Q_B'],'steps':len(out['steps']),'named_ports':True,'zero_one_two_bit_masks':True,'ordinary_local_splay_assumption':False,'full_original_closure':out['closure'],'universal_acceptance':'OPEN'})
    return out


if __name__=='__main__':
    z=basic_build();print(json.dumps({'bootstrap_source':z['source']['name'],'steps':len(z['steps']),'A':z['A'],'Q_B':z['Q_B']}))
