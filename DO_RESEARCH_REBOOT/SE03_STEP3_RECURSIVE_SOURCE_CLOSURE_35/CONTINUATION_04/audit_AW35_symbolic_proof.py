"""Free-term source identities and independent paper-proof interface review.

No bounded BST enumeration, generic source engine or new source queries.
The variables below are arbitrary ordered subtree terms. The identities
are the inherited ordinary LL/RR/zig formulas, substituted symbolically.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1];B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';S=F.parent/'CONTINUATION_01'
CAP=float(sys.argv[1]);START=time.process_time()
def N(k,l=None,r=None):return (k,l,r)
def LL(g,p,x,a,b,c,d):return N(x,a,N(p,b,N(g,c,d)))
def RR(g,p,x,a,b,c,d):return N(x,N(p,N(g,a,b),c),d)
def ZR(p,x,a,b,c):return N(x,a,N(p,b,c))
def ZL(p,x,a,b,c):return N(x,N(p,a,b),c)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    # Forward generic i>=2: L=V-(3,2i-2), C=C(i+2,r-1).
    g,p,x,old,mid='g','2i+2','xi','x_(i-1)','2i'
    lo='L';hi='C';right=N(p,None,N(g,hi,None))
    a=LL(g,p,x,None,None,hi,None);assert a==N(x,None,right)
    b=RR(old,mid,x,lo,None,None,right)
    assert b==N(x,N(mid,N(old,lo,None),None),right)
    v=N(mid,N(old,lo,None),None)
    end=RR('1','2',x,None,None,v,right)
    assert end==N(x,N('2',N('1'),v),right)
    # Forward first consumer, same opaque suffix; i=1 has no middle vine.
    first=RR('1','2','3',None,None,None,N('4',None,N(g,'C3',None)))
    assert first==N('3',N('2',N('1'),None),N('4',None,N(g,'C3',None)))
    # The F_i -> KEEP1 form is the exact LL frame, with arbitrary V and R.
    down=LL('xi','2','1',None,None,'V','R')
    assert down==N('1',None,N('2',None,N('xi','V','R')))
    # Reverse i>=2: V-(3,2i)=mid(old(L,0),0).
    a=LL('xi',mid,old,lo,None,None,'R')
    assert a==N(old,lo,N(mid,None,N('xi',None,'R')))
    rev=RR('1','2',old,None,None,lo,N(mid,None,N('xi',None,'R')))
    assert rev==N(old,N('2',N('1'),lo),N(mid,None,N('xi',None,'R')))
    # Initial right-vine RR induction and the following first KEEP1.
    comb=RR('2j-1','2j','g',None,None,'Cnext',None)
    assert comb==N('g',N('2j',N('2j-1'),'Cnext'),None)
    init=LL('g','2','1',None,None,'C2',None)
    assert init==N('1',None,N('2',None,N('g','C2',None)))
    final=LL('3','2','1',None,None,None,'R4')
    assert final==N('1',None,N('2',None,N('3',None,'R4')))
    # Independent A odd/even invariant; L and S are arbitrary opaque trees.
    odd_reset=ZR('p','1',None,'L',N('q','leaf(p+1)','S'))
    assert odd_reset==N('1',None,N('p','L',N('q','leaf(p+1)','S')))
    even=RR('1','p','q',None,'L','leaf(p+1)','S')
    assert even==N('q',N('p',N('1',None,'L'),'leaf(p+1)'),'S')
    even_reset=LL('q','p','1',None,'L','leaf(p+1)',N('k','leaf(q+1)','S2'))
    assert even_reset==N('1',None,N('p','L',N('q','leaf(p+1)',N('k','leaf(q+1)','S2'))))
    low=RR('p','q','k','L','leaf(p+1)','leaf(q+1)','S2')
    assert low==N('k',N('q',N('p','L','leaf(p+1)'),'leaf(q+1)'),'S2')
    odd_next=ZL('1','k',None,low[1],low[2])
    assert odd_next==N('k',N('1',None,N('q',N('p','L','leaf(p+1)'),'leaf(q+1)')),'S2')
    # Affine polynomial arithmetic in the arbitrary parameter r.
    counts=[(0,1),(1,-2),(0,1),(1,-3),(1,-2),(1,-3)]
    assert tuple(map(sum,zip(*counts)))==(4,-8)
    costs=[(1,-1),(1,-2),(0,2),(3,-9),(1,-2),(2,-6)]
    assert tuple(map(sum,zip(*costs)))==(8,-18)
    assert (1-1,-2-(-3))==(0,1) # reverse donors minus worst initial deficit
    for receipt in ('independent_symbolic_source_audit.json','independent_critical_source_audit.json'):
        assert (S/receipt).exists()
    fp=json.loads((F/'independent_FP_SI34_source_countercut.json').read_text())
    assert fp['demands']==9 and fp['eligible_units']==8 and fp['deficiency']==1
    for n in ('independent_native12_hard_word.json','independent_ranked13_word_02.json'):
        r=json.loads((F/n).read_text());assert r['status'].startswith('PASS_COMPLETE_') and r['H_ge_2_minimum_margin']>=0
        for p,h in r['input_sha256'].items():assert sha(Path(p))==h
    paths=[F/'ARBITRARY_SUPPORT_ANCHORED_WORD_FUNDING.md',F/'UNBOUNDED_FP_POOL_OBSTRUCTION.md',
      F/'NATIVE12_13_FIXED_WORD_SOURCE_THEOREMS.md',F/'audit_AW35_symbolic_proof.py',
      S/'SOURCE_CONSTRUCTION.md',S/'SYMBOLIC_B_CLOSURE.md',S/'EXACT_NEGATIVE_CUT.md',
      F/'independent_FP_SI34_source_countercut.json',B/'STREAMED_BLOCK_THEOREM.md',
      P/'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md']
    out={'status':'PASS_FREE_TERM_IDENTITIES_AND_SOURCE_PROOF_REVIEW',
      'AW35_scope':'all r>=4 on the specified B orbit; arbitrary A/private/helper geometry and finite repetitions',
      'reviewed_uniform_bridges':['B forward/reverse induction and empty interval endpoints',
        'H>=1 from different synchronized genuine boundary roots, including zero-event final KEEP',
        'Q1 tails nonempty; Q3 forward residual<=1; initial residual<=r-3<r-2 reverse donors',
        'F/G supplier classes disjoint; exact local h0 untouched; original static block Bank<=2',
        'original macro gap belongs to exactly one block; both-endpoint transport; no frozen fE claim',
        'UF35 first entry tags and exhaustive whole-tenure retirement proof; unbounded m-2 relaxed-pool deficit',
        'N12/N13 all H regimes, actual selected units and K+4 working bound'],
      'new_source_kernel_queries':0,'source_queries':0,'source_engine_calls':0,
      'not_a_finite_population_or_support_test':True,'independent_is_same_agent_distinct_implementation':True,
      'verification_boundary':'symbolic identity algebra plus written proof inspection, not formal proof-assistant verification',
      'JR35':'OPEN','reservation':'DEFERRED','Gate_U14':'CONDITIONAL',
      'input_sha256':{str(p):sha(p) for p in paths}}
    with (F/'independent_AW35_UF35_proof_review.json').open('x',encoding='utf8') as f:json.dump(out,f,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='input_sha256'}),flush=True);assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify148_exit.json').open('x',encoding='utf8') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
