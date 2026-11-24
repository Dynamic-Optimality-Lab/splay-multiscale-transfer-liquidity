"""Physical oracle acceptance tests, all bounded and exact."""
from collections import Counter
from functools import lru_cache
from sharp01_oracle import Tree, replay, vine, canonical_gap
from sharp01_sources import H, reflect, source
from sharp01_validate import validate

@lru_cache(None)
def trees(lo,hi):
    if lo>hi:return (None,)
    return tuple((k,l,r) for k in range(lo,hi+1) for l in trees(lo,k-1) for r in trees(k+1,hi))

def state(t):
    ch={}
    def put(t):
        if t is None:return None
        k,l,r=t; ch[str(k)]=[put(l),put(r)]; return k
    return {'root':put(t),'children':ch}

def run():
    primitive=0
    for n in range(1,6):
        for shape in trees(1,n):
            st=state(shape)
            for u,cs in Tree(st).ch.items():
                for side,v in enumerate(cs):
                    if v is None:continue
                    t=Tree(st); before={(a,x) for x in t.keys for a in t.path(x)[:-1]}; edges=t.edges()
                    info=t.rotate(u,side); t.validate()
                    after={(a,x) for x in t.keys for a in t.path(x)[:-1]}
                    assert before-after=={(info['ancestry_removed'][0],x) for x in info['ancestry_removed'][1]}
                    assert after-before=={(info['ancestry_added'][0],x) for x in info['ancestry_added'][1]}
                    assert edges-t.edges()==set(map(tuple,info['edges_removed']))
                    assert t.edges()-edges==set(map(tuple,info['edges_added']))
                    primitive+=1
    src=H(1); led=replay(src); validate(src,led)
    signatures=Counter(canonical_gap(g,led) for g in led['gaps'])
    # Test EVERY seam, including cuts in DELETE runs and before the first KEEP.
    for cut in range(1,len(src['operations'])):
        boundary=led['operations'][cut-1]['post']
        shifted={**src,'name':f'seam{cut}','initial_A':led['states'][boundary[0]],'initial_B':led['states'][boundary[1]],
                 'diagonal_initial':src['initial_A'],'reaching_prefix':src['operations'][:cut],
                 'operations':src['operations'][cut:]+src['operations'][:cut],
                 'original_operation_ids':list(range(cut+1,len(src['operations'])+1))+list(range(1,cut+1))}
        ll=replay(shifted); validate(shifted,ll)
        assert Counter(canonical_gap(g,ll) for g in ll['gaps'])==signatures
    mirrored=replay(reflect(src)); assert all(mirrored['summary'][k]==led['summary'][k] for k in ('A','Q','U','C'))
    doubled=replay({**src,'name':'twice','operations':src['operations']*2})
    assert all(doubled['summary'][k]==2*led['summary'][k] for k in ('A','Q','U','C'))
    cases=[source('empty',0,[]),source('root',1,[['K',1],['D',1],['K',1]]),
           source('no_KEEP',3,[['D',3],['D',2],['D',1]]),source('one_KEEP',3,[['K',1],['D',3],['D',2],['D',1]])]
    for s in cases:validate(s,replay(s))
    return {'status':'PASS','primitive_rotations_all_BSTs_n_le_5':primitive,'all_H11_seams':len(src['operations']),
            'reflection':True,'repeated_copies':True,'empty_zero_and_no_KEEP':True}

if __name__=='__main__':
    import json,time
    from pathlib import Path
    t=time.process_time(); ans=run(); ans['cpu_seconds']=time.process_time()-t
    Path(__file__).with_name('SHARP01_ORACLE_TESTS.json').write_text(json.dumps(ans,indent=2)); print(json.dumps(ans))
