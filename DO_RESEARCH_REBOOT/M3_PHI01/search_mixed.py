"""Finite concrete mixed-cycle search; no finite absence is a universal result."""
import sys,json,time
from pathlib import Path
from functools import lru_cache
from collections import Counter
sys.path.insert(0,'python/independent')
import splay as S
OUT=Path('DO_RESEARCH_REBOOT/M3_PHI01/mixed_search.json')
M=(0,2,4,6,8)

@lru_cache(None)
def trees(lo,hi):
    if lo==hi:return (S.LEAF,)
    return tuple(S.node(r,l,t) for r in range(lo,hi) for l in trees(lo,r) for t in trees(r+1,hi))

@lru_cache(None)
def step(t,x):return S.lookup(t,x)[1],S.trace(t,x)[0]

def serial(t):return None if t==S.LEAF else [t[1],serial(t[2]),serial(t[3])]

def main():
    assert not OUT.exists()
    start=time.process_time();extensions=returns=source_count=0
    counts=Counter();minimum={};best={};negative_edge=None;negative_cycles=[]
    for B0 in trees(0,9):
        r=B0[1]
        if r not in M:continue
        source_count+=1
        A0=S.node(r,S.balanced(range(r)),S.balanced(range(r+1,9)))
        stack=[(A0,B0,[],0)]
        while stack:
            a,b,legs,total=stack.pop()
            if len(legs)==3:continue
            for x in M:
                extensions+=1
                assert extensions<=500000 and time.process_time()-start<120,'UNKNOWN: finite search cap'
                da,an=step(a,x);db,bn=step(b,x)
                if not 1<=da<=4 or db==0:continue
                h=(da+1)//2;q=db//2;w=2*h-q
                leg={'target':x,'dA':da,'dB':db,'H':h,'q':q,'w':w}
                newlegs=legs+[leg];u=total+w;k=len(newlegs)
                stack.append((an,bn,newlegs,u));counts[f'legal_low_prefix_{k}']+=1
                if negative_edge is None or w<negative_edge['leg']['w']:
                    negative_edge={'A':serial(a),'B':serial(b),'leg':leg,'root':b[1]}
                dh,back=step(bn,r)
                if dh==0 or back!=B0:continue
                returns+=1;wh=6-dh//2;weight=u+wh
                record={'A0':serial(A0),'B0':serial(B0),'low_legs':newlegs,
                        'A_before_high':serial(an),'B_before_high':serial(bn),
                        'high_target':r,'high_d':dh,'high_q':dh//2,'high_w':wh,
                        'low_weight':u,'total_weight':weight,'mask':list(M),
                        'closure':'exact concrete B; high resets endpoint A shadow to A0'}
                key=str(k)
                if key not in minimum or weight<minimum[key]:minimum[key]=weight;best[key]=record
                if any(z['w']<0 for z in newlegs):
                    key=f'{k}_with_negative_low'
                    if key not in minimum or weight<minimum[key]:minimum[key]=weight;best[key]=record
                if weight<0:negative_cycles.append(record)
        if source_count%500==0:
            print(json.dumps({'sources':source_count,'extensions':extensions,'returns':returns,
                              'minimum':minimum,'cpu_seconds':round(time.process_time()-start,3)}),flush=True)
    result={'status':'COMPLETE','core_B_trees':4862,'examined_B_sources':source_count,
            'low_extensions':extensions,'low_prefix_counts':dict(counts),'closed_return_candidates':returns,
            'minima':minimum,'best_candidates':best,'most_negative_low_edge':negative_edge,
            'negative_cycle_candidates':negative_cycles,'cpu_seconds':round(time.process_time()-start,3),
            'scope':'fixed mask; balanced A source per marked B root; 1..3 fused low accesses then one canonical high return; no claim beyond corpus'}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('best_candidates','most_negative_low_edge','negative_cycle_candidates')}),flush=True)
if __name__=='__main__':main()
