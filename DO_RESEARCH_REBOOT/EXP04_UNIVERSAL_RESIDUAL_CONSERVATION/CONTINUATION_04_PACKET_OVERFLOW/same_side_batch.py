from campaign4 import *
from fast_physics import FullTree
from functools import lru_cache

@lru_cache(None)
def shapes(lo,hi):
    if lo>hi:return (None,)
    return tuple((k,l,r) for k in range(lo,hi+1) for l in shapes(lo,k-1) for r in shapes(k+1,hi))

def state(z):
    children={};stack=[z]
    while stack:
        k,l,r=stack.pop();children[str(k)]=[l[0] if l else None,r[0] if r else None]
        if l:stack.append(l)
        if r:stack.append(r)
    return {'root':z[0],'children':children}

def disjoint(tree,details):
    gs=[g for case,p,g,signs in details if case in ('LL','RR')]
    intervals=[(tree.lo[g],tree.hi[g]) for g in gs]
    for i,(lo,hi) in enumerate(intervals):
        for ll,hh in intervals[i+1:]:assert hi<ll or hh<lo
    return gs,intervals

if __name__=='__main__':
    meter=Meter('same_side_batch');count=0
    for n in range(1,8):
        for z in shapes(1,n):
            st=state(z)
            for x in range(1,n+1):
                a=FullTree(st);b=FullTree(st);_,_,_,details=a.splay(x,b,'A');disjoint(a,details);count+=1
    s=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())[0]
    row=json.loads((ROOT/'WIDTH_RESULTS.json').read_text())[0];h=s['target_consumer']
    a=FullTree(s['initial_A']);b=FullTree(s['initial_B'])
    critical=[(2566,3),(2566,4),(2566,5)];gs=[row['original_U'][str(p)]['g'] for p in critical]
    for t,(tag,x) in enumerate(s['operations'][:h],1):
        a.splay(x,b,'A')
        if tag=='K':_,_,_,details=b.splay(x,a,'B')
    disjoint(b,details)
    outputs=[]
    for p,g in zip(critical,gs):
        assert row['original_U'][str(p)]['case']=='LL'
        lo,hi=b.lo[g],b.hi[g]
        lab=((1<<hi)-1)^((1<<(lo-1))-1)
        assert lab==row['original_U'][str(p)]['J']
        outputs.append({'original_parent':p,'old_g':g,'complete_output_interval':[lo,hi]})
    maximum=max(sum(lo<=y<=hi for lo,hi in (z['complete_output_interval'] for z in outputs)) for y in range(1,b.n+1))
    assert maximum==1
    write('SIMULTANEOUS_RECREATION_BATCH.json',{'source':s['name'],'after_original_KEEP':h,
        'actual_same_side_parent_outputs':outputs,'maximum_shared_target_membership':maximum,
        'necessary_B_ancestry_gains_to_reuse_all_three_at_one_later_KEEP':2,
        'small_full_tree_orientation_checks':count,'exhaustive_small_physical_populations':'1..7 only; universal argument is PROOF_LEDGER P7',
        'fresh_A_work_inferred_from_B_gain':False})
    meter.success=True;print('PASS disjoint completed same-side grandparent outputs and two necessary B restorations',flush=True)
