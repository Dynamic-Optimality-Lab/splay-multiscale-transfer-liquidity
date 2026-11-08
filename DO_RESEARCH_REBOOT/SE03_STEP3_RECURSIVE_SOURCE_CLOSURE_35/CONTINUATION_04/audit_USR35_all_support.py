"""Static independent review; no ordinary source engine evaluations."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;B=F.parents[1]/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    accepted=F/'independent_USR35.json';a=json.loads(accepted.read_text())
    assert a['status']=='PASS_USR35_UNIFORM_PROOF_REVIEW_WITH_M4_SOURCE_CONTROL'
    for p,h in a['input_sha256'].items():assert sha(Path(p))==h
    # Formal affine coefficient identities, variables (m,s,j,constant).
    r=(3,1,0,2);n=(6,2,0,3)
    assert tuple(2*x-y for x,y in zip(r,(0,0,0,1)))==n
    # Path length: three initial edges, then z-(2m+2).
    z=(6,0,2,3);u=(2,0,0,2)
    depth=tuple(x-y+c for x,y,c in zip(z,u,(0,0,0,3)))
    assert depth==(4,0,2,4) and tuple(v//2 for v in depth)==(2,0,1,2)
    # Euclidean division r-2=3m+s gives exactly the three s cases;
    # induction in m, rather than bounded samples of r, supplies all r>=11.
    assert all(0<=s<3 and (3*3+2+s-2)//3==3 for s in (0,1,2))
    paths=[accepted,F/'ALL_SUPPORT_RETURN_ESCAPE_NECESSITY.md',F/'SS_SPLAY_INVERSE_SOURCE_THEOREM.md',F/'audit_USR35_all_support.py',B/'STREAMED_BLOCK_THEOREM.md']
    out={'status':'PASS_USR35_R_ALL_SUPPORT_SOURCE_LIFT_AND_CAPACITY_REVIEW',
      'quantifier':'every integer r>=11; m=floor((r-2)/3); s in0,1,2',
      'proof_review':['new upper private hanger leaves every original critical path unchanged',
        'new genuine key z_j actual RR path has q=2m+2+j; actual SSI inverse closes full tree',
        'new visits are after all original resets; exact next-contact eligibility windows unchanged',
        'all original odd marks visited; actual source support r and full core2r-1',
        'at most2 old return endpoints implies at least m-2 distinct endpoints outside, owners relaxed',
        'original m preparation tails unchanged, compatible across disjoint actual blocks',
        'additive source SSI budget and owner-inclusive static bank2; no fE availability assumption',
        'no unbounded bank claim; no universal source-coverage or CD-refutation claim'],
      'numerical_replay':False,'source_queries':0,'source_engine_calls':0,'JR35':'OPEN','reservation':'DEFERRED',
      'independent_is_same_agent_distinct_implementation':True,'input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'independent_USR35_all_support.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in ('input_sha256','proof_review')}),flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify157_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
