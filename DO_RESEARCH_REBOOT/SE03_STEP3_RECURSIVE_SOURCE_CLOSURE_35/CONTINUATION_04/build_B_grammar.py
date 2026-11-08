"""Exact static grammar generation, not original access evaluation."""
import functools,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
@functools.lru_cache(None)
def T(n,start):
    return tuple((start+2*a,l,r) for a in range(n) for l in Zp(a,start) for r in Zm(n-1-a,start+2*a+1))
@functools.lru_cache(None)
def Zp(n,start):
    if n==0:return (None,)
    return tuple((start+2*a-1,l,r) for a in range(1,n+1) for l in T(a,start) for r in Zp(n-a,start+2*a))
@functools.lru_cache(None)
def Zm(n,start):
    if n==0:return (None,)
    return tuple((start+2*b,l,r) for b in range(n) for l in Zm(b,start) for r in T(n-b,start+2*b+1))
def main():
    trees=T(7,1);assert len(set(trees))==len(trees)==3876
    def validate(t):
        if t is None:return [],0
        l,ml=validate(t[1]);r,mr=validate(t[2]);mass=ml+mr+(1 if t[0]%2 else -1)
        assert mass==(1 if t[0]%2 else 0)
        return l+[t[0]]+r,mass
    for tree in trees:assert validate(tree)==(list(range(1,14)),1)
    counts=[len(T(n,1)) for n in range(1,8)];assert counts==[1,2,7,30,143,728,3876]
    out('maximal_B_grammar.json',{'r':7,'physical_core_keys':list(range(1,14)),'marks':list(range(1,14,2)),
      'trees':trees,'state_count':len(trees),'count_sequence':counts,
      'source_queries':0,'source_engine_calls':0,'all_candidate_trees_dynamically_realizable_claimed':False})
    print('EXHAUSTIVE_STATIC_MAXIMAL_CORE_GRAMMAR_3876',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_proof184_exit.json').open('x',encoding='utf-8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
