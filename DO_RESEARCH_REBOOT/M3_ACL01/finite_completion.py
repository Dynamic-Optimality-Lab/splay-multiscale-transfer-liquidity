"""Complete normalized alpha grammar and rigid rotation frame checks; no new fit."""
import sys,json,time,itertools
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path[:0]=['DO_RESEARCH_REBOOT/M3_ACL01','DO_RESEARCH_REBOOT/M3_S3P01',
 'DO_RESEARCH_REBOOT/M3_G0P01','DO_RESEARCH_REBOOT/M3_H1F01',
 'DO_RESEARCH_REBOOT/M3_FRC01','DO_RESEARCH_REBOOT/M3_H2R01',
 'DO_RESEARCH_REBOOT/M3_PHI01','python/independent']
from canonical_completion import S,V,U,MARKED,rho,CompleteOneGapPotential
from certify_core3_v2 import load as old_load
BASE=Path('DO_RESEARCH_REBOOT/M3_ACL01')

@lru_cache(None)
def grammar(keys,depth):
    opaque=(1,0,0);empty=(2,0,0)
    if depth==2:
        return (opaque,)+((empty,) if not keys else ())+tuple((0,int(k>=0),max(k,0)) for k in keys)
    rows=[(opaque,opaque,opaque)]
    if not keys:rows.append((empty,empty,empty))
    for k in keys:
        for l in grammar(tuple(x for x in keys if x<k),2):
            for r in grammar(tuple(x for x in keys if x>k),2):
                rows.append(((0,int(k>=0),max(k,0)),l,r))
    return tuple(rows)

def main():
    out=BASE/'finite_completion.json';assert not out.exists();start=time.process_time()
    P=CompleteOneGapPotential();physical=P.physical;patterns=[];ids=set();counts=Counter();oldc,olda=old_load()
    for k in range(9):
        for l in grammar(tuple(x for x in U if x<k),1):
            for r in grammar(tuple(x for x in U if x>k),1):
                a=((0,1,k),l[0],r[0],l[1],l[2],r[1],r[2]);assert a not in ids;ids.add(a)
                im=rho(a);assert im in physical.ids
                counts[k]+=1;patterns.append({'alpha':a,'image':physical.ids[im]})
    byphysical={s:i for i,s in enumerate(tuple(tuple(x) for x in ss) for ss in physical.c['shadows'])}
    # All registered old port values, rather than a sample, retain their images.
    oldimages=[physical.ids[rho(a)] for a in oldc['shadows']]
    assert oldimages==oldc['refined_shadow']
    assert all(olda['images'][i]==physical.c['B_bases'][b]+physical.local[oldimages[a]]
               and olda['potential'][i]==physical.p[olda['images'][i]]
               for i,(b,a) in enumerate(zip(olda['ordinary_b'],olda['ordinary_a'])))
    # Finite frame checks use opaque blocks carrying their exact key set.
    # The universal proof treats side blocks as arbitrary recursive terms.
    def block(keys,opaque):return ('port',tuple(keys)) if opaque else S.balanced(keys)
    def fill(t):
        if t[0]=='port':return S.balanced(t[1])
        if t==S.LEAF:return t
        return S.node(t[1],fill(t[2]),fill(t[3]))
    frames=0
    for lo in range(-1,9):
        for hi in range(lo+2,10):
            keys=tuple(range(lo,hi))
            for x,p in itertools.combinations(keys,2):
                ranges=(tuple(k for k in keys if k<x),tuple(k for k in keys if x<k<p),tuple(k for k in keys if k>p))
                for bits in itertools.product((False,True),repeat=3):
                    a,b,c=(block(ks,bit) for ks,bit in zip(ranges,bits))
                    src=S.node(p,S.node(x,a,b),c);dst=S.node(x,a,S.node(p,b,c))
                    assert S.trace(fill(src),x)[0]==fill(dst)
                    assert S.trace(fill(dst),p)[0]==fill(src)
                    frames+=2
            assert time.process_time()-start<120,'UNKNOWN finite phase cap'
    result={'status':'FINITE_EXACT_VERIFIED','normalized_alpha_count':len(patterns),
      'by_core_root':dict(counts),'marked_root_patterns':sum(counts[k] for k in MARKED),
      'physical_image_classes':len(set(r['image'] for r in patterns)),
      'old_alpha_images_unchanged':len(oldimages),'old_state_values_unchanged':len(olda['potential']),
      'two_orientation_rotation_frames':frames,'new_potential_fit':False,
      'explicit_diagnostic_states':len(patterns)+len(physical.p),'cpu_seconds':round(time.process_time()-start,3),
      'patterns':patterns}
    assert result['explicit_diagnostic_states']<=2000000
    with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='patterns'}),flush=True)
if __name__=='__main__':main()
