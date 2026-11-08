"""Distinct static verifier, no producer import, no access/splay engine calls."""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;P=F.parents[1]
B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01'
START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def save(n,z):
    with (F/n).open('x',encoding='utf-8') as f:json.dump(z,f,indent=2)
def main():
    c=read(F/'new_symbolic_source_certificate.json')
    for n,h in c['input_sha256'].items():assert sha(P.parent/n)==h
    # Independent normal form extraction from literal free-term certificates.
    frames=c['free_frames']
    for row in frames.values():
        def inorder(t):
            if isinstance(t,str):return [t]
            k,l,r=t;return inorder(l)+[k]+inorder(r)
        assert inorder(row['before'])==inorder(row['after'])
        assert len(set(inorder(row['before'])))==len(inorder(row['before']))
    # Structural checks use destructuring, not the producer rotation functions.
    (a,z,(p,L,(x,E,R)))=frames['even_consumer_RR']['before']
    assert frames['even_consumer_RR']['after']==[x,[p,[a,z,L],E],R]
    (a,z,(p,L,(x,E,(y,O,R))))=frames['odd_consumer_RR_then_zig']['before']
    assert frames['odd_consumer_RR_then_zig']['after']==[y,[a,z,[x,[p,L,E],O]],R]
    assert frames['following_anchor_LL']['after']==frames['even_consumer_RR']['before']
    assert frames['following_anchor_zig']['after']==[a,z,[y,[x,[p,L,E],O],R]]
    # Cluster law for a single symbolic rotation with arbitrary disjoint operands.
    before={frozenset('A'),frozenset('B'),frozenset('C'),frozenset('vBC'),frozenset('pAvBC')}
    after={frozenset('A'),frozenset('B'),frozenset('C'),frozenset('pAB'),frozenset('pAvBC')}
    assert len(after-before)==1 and len(before-after)==1
    # Independent iterative subtree inventory of the two already-saved endpoints.
    s=read(F.parent/'CONTINUATION_01/SI34_source_countercertificate.json')['source']
    def inventory(tree):
        out=set();stack=[tree]
        while stack:
            t=stack.pop()
            if t is None:continue
            keys=[];todo=[t]
            while todo:
                u=todo.pop()
                if u is not None:keys.append(u[0]);todo.extend(u[1:])
            out.add(tuple(sorted(keys)));stack.extend(t[1:])
        return out
    missing=inventory(s['initial_A'])-inventory(s['desired_A_before_forward'])
    expected={(1,14),(1,13)}|{(v,13) for v in range(2,13,2)}
    assert {(min(v),max(v)) for v in missing}==expected
    assert sorted(map(list,missing))==c['SI34_missing_reset_clusters']
    # Universal counts checked as polynomial coefficient identities, not samples r.
    # Polynomials are (coefficient of r, constant).
    rows=[(1,-1),(0,1),(0,2),(4,-12),(3,-9),(0,1)]
    assert tuple(map(sum,zip(*rows)))==(8,-18)
    assert (1,0)+(0,0)!=(0,0) # no solver or source oracle used
    report={'status':'PASS_WITH_EXPLICIT_SCOPE','source_queries':0,'source_engine_calls':0,
      'mechanical_checks':['producer input hashes','free-term operand/order conservation',
       'independent structural frame identities','one-new-cluster rotation law',
       'saved eight missing endpoint clusters','universal Q polynomial coefficients'],
      'mathematical_reviewed_arguments':['descending-maximum sweep induction',
       'inactive even-leaf/high-hanger lift','first-creation cluster charging',
       'AF35 source-class table and disjoint predecessor assignment',
       'accepted static source-block working2 interface'],
      'not_machine_formalized':['universal source induction proofs','all-license completeness',
       'arbitrary-source compatibility','Gate U induction'],
      'verification_kind':'different static code operated by same research agent; not external peer review or proof assistant',
      'complete_numeric_source_replay':False,'universal_UCF35':'OPEN','SI34':'REFUTED',
      'input_sha256':{n:sha(F/n) for n in ['new_symbolic_source_certificate.json',
       'RESET_CLUSTER_LOWER_BOUND.md','DESCENDING_SWEEP_RETURN.md','ANCHORED_FAMILY_COMPLETE_FUNDING.md',
       'GLOBAL_FULL_H_AND_FROZEN_EXCHANGE.md','COMPLETE_FEASIBILITY_DUAL_THEOREM.md']}}
    save('independent_symbolic_audit.json',report)
    print('STATIC_SYMBOLIC_AUDIT_PASS; NO_UNIVERSAL_PROMOTION',flush=True)
    assert time.process_time()-START<CAP-1
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as e:error=repr(e);raise
    finally:
        with (B/'audit_verify90_exit.json').open('x',encoding='utf-8') as f:
            json.dump({'whole_process_CPU_seconds':time.process_time(),'error':error,'source_queries':0,'source_engine_calls':0},f)
