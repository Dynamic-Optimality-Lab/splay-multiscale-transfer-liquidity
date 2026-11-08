"""Targeted independent source-contract supplement; no accepted check repeated."""
import json,time,hashlib
from pathlib import Path
B=Path(__file__).resolve().parent;P=B.parent.parent;O=P/'SE03_STEP2_UNARY_A_LIFT_14'
def rd(p):return json.loads(p.read_text())
def fr(v):return tuple(map(fr,v)) if isinstance(v,list) else v
def main():
    h=rd(B/'cold013_h1_relation.json');A7=h['states'];z=rd(B/'threephase2_analysis.json');g=rd(O/'branch_grammar2.json');c=rd(O/'branch_core11_mask0.json')
    F=[1];RR=[0]
    for n in range(1,8):
        r=sum(F[i]*F[n-1-i] for i in range(n));RR.append(r)
        F.append(r+sum(F[i]*F[n-i] for i in range(1,n)))
    assert RR[6]==974 and RR[7]==5947==len(A7)
    assert len({fr(t) for t in A7})==5947
    def valid(t,lo=0,hi=8000):
        if t is None:return set(),set()
        x=t[0];assert lo<x<hi
        ml,ul=valid(t[1],lo,x);mr,ur=valid(t[2],x,hi)
        if x%1000==0:
            assert 1000<=x<=7000;return ml|mr|{x},ul|ur
        assert x%1000==500 and ml and mr and x==500+1000*sum(m<x for m in range(1000,7001,1000))
        return ml|mr,ul|ur|{x}
    for t in A7:
        mm,uu=valid(t);assert mm==set(range(1000,7001,1000)) and t[0]%1000==0 and len(uu)<=5
    assert sum(t[0] not in (4000,5000) for t in A7)==5577
    # Exact prescribed initial B, all three A parameters, and initial labels.
    lower=(4,(3,(2,(1,'F0','F1'),'F2'),'F3'),'F4')
    BF=(9,(8,(5,lower,(6,'F5',(7,'F6','F7'))),'F8'),(10,'F9',(11,'F10','F11')))
    bi={fr(t):i for i,t in enumerate(c['BF_trees'])};ai={fr(t):i for i,t in enumerate(g['states'])};qi={fr(t):i for i,t in enumerate(A7)}
    b=bi[BF];roots={r:[a for a,t in enumerate(g['states']) if t[0]==r*1000] for r in range(1,7)}
    offset=sum(len(roots[c['marks'].index(t[0])+1]) for t in c['BF_trees'][:b]);cc={tuple(v['key']):v['slack'] for v in z['canonical_states']}
    initial=[]
    for small in [(1500,(1000,None,None),(2000,None,None)),(1000,None,(2000,None,None)),(2000,(1000,None,None),None)]:
        a7=qi[(6000,(4000,(3000,small,None),(5000,None,None)),(7000,None,None))]
        a6=ai[(5000,(4000,(3000,small,None),None),(6000,None,None))]
        d=c['debt'][offset+roots[5].index(a6)];assert cc[0,a7,b]<=d and a7 in h['initial'];initial.append(d)
    assert sorted(initial)==[1,1,2] and len(h['initial'])==3
    # The previous independent verifier pins every completed batch result;
    # this supplement pins the mathematical source contracts themselves.
    docs=('SOURCE_SPEC.md','SOURCE_LIFTING_PROOF.md','COLD_CHART_COMPARISON.md','FULL_PROOF.md')
    result={'status':'PASS_INDEPENDENT_SOURCE_CONTRACTS','boundary_grammar_count':5947,'pre_cold_bases':5577,
        'initial_debts':initial,'initial_BF_index':b,'all_seven_boundary_terms_valid_and_exhaustive_by_count':True,
        'new_source_queries':0,'external_or_formal_audit':False,
        'source_proof_review':'complete LOW operand partition, four-rotation depth guard, full H1 phase, exact single cold seam, complete q5/q1 packets, all terminal H and cutoff argument inspected',
        'proof_sha256':{n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in docs}}
    with (B/'SOURCE_CONTRACT_INDEPENDENT_AUDIT.json').open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps(result))
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_sourcecontracts_exit.json').open('x') as f:json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
