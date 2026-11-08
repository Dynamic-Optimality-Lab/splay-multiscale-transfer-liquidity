"""Independent free-term source proof audit; no numerical source replay.
Checks universal SS schemata and exact countercut/repair arithmetic.
"""
import hashlib,json,sys,time
from pathlib import Path
F=Path(__file__).resolve().parent;C=F.parent;P=C.parent;B=P/'SE03_STEP3_DIRECT_UNIVERSAL_SOURCE_FUNDING_33/CONTINUATION_01';START=time.process_time();CAP=float(sys.argv[1])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def L(t):
    g,p,D=t;x,A,Bb=p;return x,A,(g,Bb,D)
def R(t):
    g,A,p=t;x,Bb,Cc=p;return x,(g,A,Bb),Cc
def LL(t):return L(L(t))
def RR(t):return R(R(t))
def main():
    # Free terms A,D,H are arbitrary independent ordered hangers. None
    # of these checks executes a new original source access query.
    a,b,p,c,q,d,g='a','b','p','c','q','d','g'
    G=(g,(d,(q,None,None),'D'),None)
    first=LL(G);assert first==(q,None,(d,None,(g,'D',None)))
    middle=RR((p,'A',(c,None,first)))
    final=RR((a,None,(b,None,middle)))
    expected=(q,(b,(a,None,None),(c,(p,'A',None),None)),(d,None,(g,'D',None)))
    assert final==expected # forward three-double induction step
    anchor=LL(expected)
    assert anchor==(a,None,(b,None,(q,(c,(p,'A',None),None),(d,None,(g,'D',None)))))
    # Reverse: arbitrary right hanger H, left vine extended by c,p.
    src=(q,(b,(a,None,None),(c,(p,'A',None),None)),'H')
    ar=LL(src);inner=LL(ar[2][2]);back=RR((a,None,(b,None,inner)))
    assert back==(p,(b,(a,None,None),'A'),(c,None,(q,None,'H')))
    # First forward double-pair and final inverse.
    first_pair=RR((a,None,(b,None,LL((g,(d,(q,None,None),'D'),None)))))
    assert first_pair==(q,(b,(a,None,None),None),(d,None,(g,'D',None)))
    assert LL((q,(b,(a,None,None),None),'H'))==(a,None,(b,None,(q,None,'H')))
    # One outer RR step appends exactly one two-node tooth to max-star comb.
    max_step=RR(('G',None,('P',None,('n','C',None))))
    assert max_step==('n',('P',('G',None,None),'C'),None)
    # Initial DELETE1 LL, with upper fringe and target's right term.
    retire=LL(('g',('h',('a',None,'E'),None),None))
    assert retire==('a',None,('h','E',('g',None,None)))
    # g is an off-path largest leaf; Gamma over low keys never makes
    # that leaf an operand. Written lifting proof supplies every Gamma
    # letter, not a numerical stream assumed to have been checked.
    costs=dict(initial_max=7,initial_anchor=1,first_consumer=2,other_forward_pairs=5*(1+3),reverse_pairs=5*(1+2),final_anchor=1)
    assert sum(costs.values())==46
    first=read(F/'independent_critical_source_audit.json')
    for name,h in first['input_sha256'].items():assert sha(F/name)==h
    arows=read(F/'new_A_primitive_rows.json')['rows'];assert sum(z['a'] for z in arows)==13
    # Literal local replacement comparison; this is not a frozen owner update.
    repairs=[];allunits=set()
    for i,target in ((2,5),(4,9),(6,13)):
        pred=arows[(2*i-2)-1]
        cons=arows[(2*i-1)-1]
        assert pred['key']==1 and pred['a']==1 and cons['key']==target and cons['a']==1
        h=f'h{i}';v=f'v{target}';pairs=[((h,1),(h,1,0)),((v,1),(v,1,0)),((v,2),(v,1,1)),((v,3),(h,1,1))]
        assert not allunits&{u for dd,u in pairs};allunits|={u for dd,u in pairs}
        repairs.append(dict(target=target,comparison_pairs=pairs,bank_trace=[0,2,1,3,0],working_peak=3,natural_owners_preserved=True,scope='independent source-block comparison, not actual arbitrary a0 update'))
    common={('c',1,0),('c',1,1)};N=[common|{(v,1,0),(v,1,1)} for v in ('v5','v9','v13')]
    un=set().union(*N);assert len(un)==8 and sum(len(s)-3 for s in N)==3 and sum(map(len,N))-len(un)==4
    assert all(len(s-set().union(*(N[j] for j in range(3) if j!=i)))==2 for i,s in enumerate(N))
    docs=['SYMBOLIC_B_CLOSURE.md','SOURCE_CONSTRUCTION.md','EXACT_NEGATIVE_CUT.md','DEPENDENCIES_AND_SCOPE.md','SOURCE_REPAIR_AND_PARENT_STATUS.md']
    certificate=dict(status='PASS_SYMBOLIC_SOURCE_CLOSURE_POOL_EXHAUSTIVENESS_AND_LOCAL_REPAIR_AUDIT',input_sha256={n:sha(F/n) for n in docs},critical_audit_sha256=sha(F/'independent_critical_source_audit.json'),source_queries=0,source_engine_calls=0,mathematical_source_proof='SS frame induction, same-key transformation with rigid largest-leaf lift, finite erased/chart recurrence, exact birth-interval pool exhaustion',Gamma_words='canonical shortest words, finite by accepted theorem; not expanded/replayed',no_DELETE_only_return_loops='shortest words and initial root15 separation',selected_demand_count=9,joint_pool_size=8,sigma=3,overlap=4,local_unused=0,SI34_mathematical_result='REFUTED_AT_DECLARED_SOURCE_SCOPE',entire_source_CD_margin_lower_bound_per_word=4,independent_block_repairs=repairs,universal_owner_or_Bank25_refuted=False,full_numerical_source_replay=False,trust='same-agent distinct implementation/static mathematical audit; not external peer review or formal proof assistant')
    with (F/'independent_symbolic_source_audit.json').open('x',encoding='utf-8') as f:json.dump(certificate,f,indent=2)
    assert time.process_time()-START<CAP-1
    print(certificate['status'],flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as ex:error=repr(ex);raise
    finally:
        with (B/'audit_verify88_exit.json').open('x') as f:json.dump(dict(whole_process_CPU_seconds=time.process_time(),error=error,source_queries=0,source_engine_calls=0),f)
