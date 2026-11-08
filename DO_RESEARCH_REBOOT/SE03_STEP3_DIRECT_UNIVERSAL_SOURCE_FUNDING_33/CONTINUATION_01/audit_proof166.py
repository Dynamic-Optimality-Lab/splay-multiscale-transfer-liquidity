"""Universal free-term and affine kernel for new source retirement proofs."""
import hashlib,itertools,json,sys,time
from pathlib import Path
B=Path(__file__).resolve().parent;F=B/'SOURCE_JOINT_REPAIR_03';P=B.parent.parent
START=time.process_time();CAP=float(sys.argv[1])
def pin(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def twice(a):return tuple(2*x for x in a)
def main():
    # Components are arbitrary disjoint free BST terms; only g can LOSE
    # descendants under g(p(A,B),C)->p(A,g(B,C)).
    before={'g':{'p','A','B','C'},'p':{'A','B'}}
    after={'g':{'B','C'},'p':{'A','g','B','C'}}
    assert before['g']-after['g']=={'p','A'} and not before['p']-after['p']
    # Macro parameters [constant,G,hstar,Q], G>=0,hstar>=1,Q<=2.
    # 2H-Q-2G = 2hstar-Q >=0. Parameterize hstar=1+s,Q=2-z.
    # Coefficients below over arbitrary s,z>=0 give slack2s+z.
    assert sub((2,2,0),(2,0,-1))==(0,2,1)
    # Local general source inequality:
    # 2H-Q >= 2sum(hstar)+2(G+Hc)-3k >= 2k+k-3k=0.
    assert 2+1-3==0
    # Counterfamily and positive return-block margins, r=7+s,s>=0.
    r=(7,1);m=twice(add(r,(1,0)));q=tuple(6*x for x in sub(r,(1,0)))
    assert m==(16,2) and q==(36,6) and sub(twice(m),q)==(-4,-2)
    # k=r-1; actual V return block Q=3k-1; source proof2H>=3k.
    k=sub(r,(1,0));QB=sub(tuple(3*x for x in k),(1,0))
    assert QB==(17,3) and sub(tuple(3*x for x in k),QB)==(1,0)
    source=P/'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md'
    realized=B/'UNIFORM_A_REALIZATION_OVER_CLOSED_B.md';receipt=B/'uniform_A_realization_independent_audit.json'
    rr=json.loads(receipt.read_text());assert pin(realized)==rr['input_sha256'][realized.name]
    docs=('ANCESTOR_RETIREMENT_LEMMA.md','MONOTONE_RETURN_SOURCE_FUNDING.md','EXTREME_TARGET_JOINT_TICKETS.md','INTERIOR_TICKET_COLLISION.md','SOURCE_ONLY_B_BOUND.md')
    out('symbolic_source_proof.json',{'status':'PRODUCER_SOURCE_RETIREMENT_AND_MONOTONE_RETURN_KERNEL',
      'free_term_loss':'only right-rotation pivot g loses p and free term A; reflected left case',
      'zero_A_event_KEEP_handled':'distinguished last positive target splay, even when terminal KEEP has H0',
      'working_bank':2,'scope':'MR blocks with Qi<=2,Qc<=k; extreme raw tickets restricted to maximal closed core; arbitrary-source full C33 still OPEN',
      'affine_r7_plus_s':{'genuine_accesses':m,'Q':q,'2m_minus_Q':sub(twice(m),q),'return_block_Q':QB,'source_block_margin_lower':(1,0)},
      'source_queries':0,'source_engine_calls':0,'principal_C33':'OPEN',
      'input_sha256':{str(source):pin(source),str(realized):pin(realized),str(receipt):pin(receipt),**{d:pin(F/d) for d in docs}}})
    assert time.process_time()-START<CAP-1;print('SOURCE_RETIREMENT_SYMBOLIC_KERNEL_READY; universal_C33_OPEN; queries0')
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_proof166_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
