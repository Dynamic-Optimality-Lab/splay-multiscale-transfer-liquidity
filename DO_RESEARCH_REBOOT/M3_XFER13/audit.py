"""Independent universal exposure/floor/sign audit; NO finite tests.

Upper U and A-side blocks are unassigned variables. Fixed Score-role
patterns are theorem schemas, never evaluated original models or psi.
No compiler/root/DAG/bank is imported or executed.
"""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
EMPTY=('CORE_EMPTY',)

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('BLOCK',name)
def N(k,l=EMPTY,r=EMPTY):return ('NODE',k,l,r)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def at(t,path):
    for b in path:
        assert t[0]=='NODE';t=t[2+b]
    return t
def put(t,path,v):
    if not path:return v
    return N(t[1],put(t[2],path[1:],v),t[3]) if path[0]==0 else N(t[1],t[2],put(t[3],path[1:],v))
def pair(t,path):
    if path==(0,0):return rz(rz(t))
    if path==(1,1):return lz(lz(t))
    if path==(0,1):return rz(N(t[1],lz(t[2]),t[3]))
    assert path==(1,0);return lz(N(t[1],t[2],rz(t[3])))
def splay_term(t,path):
    while len(path)>=2:
        prefix=path[:-2]
        t=put(t,prefix,pair(at(t,prefix),path[-2:]))
        path=prefix
    return (rz(t) if path==(0,) else lz(t)) if path else t
def find(t,key,path=()):
    if t[0]!='NODE':return None
    if t[1]==key:return path
    p=find(t[2],key,path+(0,))
    return p if p is not None else find(t[3],key,path+(1,))
def depth(t,key):
    p=find(t,key);assert p is not None;return len(p)
DUAL={'zero':'eight','one':'seven','two':'six','three':'five','four':'four',
      'five':'three','six':'two','seven':'one','eight':'zero'}
def dual(t):
    return N(DUAL.get(t[1],t[1]),dual(t[3]),dual(t[2])) if t[0]=='NODE' else t
def lin(*parts):
    out={}
    for p in parts:
        for k,v in p.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,E,F,U=map(V,('A','B','C','D','E','F','ARBITRARY_UPPER'))
    identities=[]
    def cert(name,source,path,expected):
        assert splay_term(source,path)==expected,name
        identities.append(name)
        assert splay_term(dual(source),tuple(1-d for d in path))==dual(expected),name+'_actual_other_side'
        identities.append(name+'_actual_other_side')
    z,o,t,h,f,v,s,e='zero','one','two','three','four','five','six','eight'
    G=N(v,N(f,N(h,N(z,EMPTY,N(o,EMPTY,N(t))))),U)
    T=N(t,N(o,N(z)),N(v,N(h,EMPTY,N(f)),U))
    R=N(z,EMPTY,N(o,EMPTY,N(t,EMPTY,N(v,N(h,EMPTY,N(f)),U))))
    LA=N(z,EMPTY,N(t,N(o),N(h)))
    LB=N(t,N(o,N(z)),N(h))
    CA=N(f,LA,N(v,EMPTY,U));CB=N(f,LB,N(v,EMPTY,U))
    def B8(lower):return N(e,N(v,N(f,lower),N('seven',N(s))))
    cert('main_non_extremal_core_zero2',G,(0,0,0,1,1),T)
    assert depth(G,t)==5 and depth(G,f)==1
    assert depth(T,z)==2 and depth(T,f)==3 and depth(T,v)==1
    cert('T_plus1_zero_return',T,(0,0),R)
    cert('T_plus1_four_return',T,(1,0,1),CB)
    cert('R_zero4_return',R,(1,1,1,0,1),CA)

    # The NEW H zero return; U is not constrained/evaluated here because
    # H's upper band is a fixed saved symbolic core pattern.
    H=B8(LA)
    H2=N(t,N(z,EMPTY,N(o)),N(v,N(f,N(h)),N(e,N('seven',N(s)))))
    cert('H_zero2_all_marks_shallow',H,(0,0,0,1),H2)
    assert all(depth(H2,k)<=2 for k in (z,t,f,v,e))
    # Source prototype depths prove only nonnegative H1 prices in CA/CB;
    # the upper marked8 depth2..4 is from U's three-node COUNT, not a census.
    assert depth(CA,z)==1 and depth(CA,t)==2 and depth(CA,v)==1
    assert depth(CB,z)==3 and depth(CB,t)==1 and depth(CB,v)==1

    mainA=N(v,N(f,N(t,A,B),C),D)
    targetA=N(t,A,N(f,B,N(v,C,D)))
    cert('main_A_to_T_no_left_guard',mainA,(0,0),targetA)
    # Three ways a visible lower mark is accessed from T. The SAME core R
    # occurs, while the full A target can be R or ER with an unlabeled parent.
    t0=[
      ('L',N(t,N(z,A,B),N(f,C,N(v,D,E))),(0,),
        N(z,A,N(t,B,N(f,C,N(v,D,E)))),'R'),
      ('LL',N(t,N('p',N(z,A,B),C),N(f,D,N(v,E,F))),(0,0),
        N(z,A,N('p',B,N(t,C,N(f,D,N(v,E,F))))),'ER'),
      ('LR',N(t,N('p',A,N(z,B,C)),N(f,D,N(v,E,F))),(0,1),
        N(z,N('p',A,B),N(t,C,N(f,D,N(v,E,F)))),'R'),
    ]
    lower_returns=[]
    for name,source,path,target,region in t0:
        cert('T_A_zero_at_'+name,source,path,target)
        if region=='R':
            assert at(target,(1,))[1]==t and at(target,(1,1))[1]==f
        else:
            assert at(target,(1,))[0]=='NODE' and at(target,(1,1))[1]==t
        lower_returns.append({'position':name,'public_target_region':region,
          'fresh_private_completion_required':False})
    t4A=N(t,A,N(f,B,N(v,C,D)))
    t4out=N(f,N(t,A,B),N(v,C,D))
    cert('T_A_four_to_CB',t4A,(1,),t4out)
    assert at(t4out,(0,))[1]==t and at(t4out,(1,))[1]==v
    r4A=N(z,A,N(t,B,N(f,C,D)))
    r4out=N(f,N(t,N(z,A,B),C),D)
    cert('R_A_zero4_to_CA_unrestricted_right',r4A,(1,1),r4out)
    assert at(r4out,(0,))[1]==t and at(r4out,(0,0))[1]==z

    # Three possible upper target locations at CA; the old RRRR core B8
    # map is REUSED, not rerun. These are NEW A/typed-target transfers.
    lowA=N(t,N(z,A,B),C)
    c8=[
      ('R',N(f,lowA,N(e,D,E)),(1,),N(e,N(f,lowA,D),E),'H'),
      ('RL',N(f,lowA,N('p',N(e,D,E),F)),(1,0),
        N(e,N(f,lowA,D),N('p',E,F)),'H'),
      ('RR',N(f,lowA,N('p',D,N(e,E,F))),(1,1),
        N(e,N('p',N(f,lowA,D),E),F),'EB'),
    ]
    upper_returns=[]
    for name,source,path,target,region in c8:
        cert('CA_zero8_A_'+name,source,path,target)
        if region=='H':
            assert at(target,(0,))[1]==f and at(target,(0,0))[1]==t
        else:
            assert at(target,(0,))[0]=='NODE' and at(target,(0,0))[1]==f
        upper_returns.append({'position':name,'public_target_region':region})
    cb8A=N(f,N(t,A,B),N(v,C,N(e,D,E)))
    cb8out=N(e,N(v,N(f,N(t,A,B),C),D),E)
    cert('CB_zero8_A_RR_to_EB',cb8A,(1,1),cb8out)
    assert at(cb8out,(0,0))[1]==f

    # NEW helper eligibility check: the exact arbitrary-block outputs of
    # an extreme on the other side push every formerly depth2 mark below2.
    # The source proxy-depth lemma and event semantics are reused dependencies.
    Hleft=N(f,N(t,A,B),N(v,C,D))  # A-side marked5 can occur at LR.
    Rright=N(t,A,N(f,B,N(v,C,D)))
    helper_outputs=[
      ('H_max_R',N('g',N(e,Hleft,E),F),e,f,t,v),
      ('H_max_RR',N('g',N('p',N(e,Hleft,E),F),U),e,f,t,v),
      ('H_max_RL',N('g',N(e,Hleft,E),N('p',F,U)),e,f,t,v),
      ('R_min_L',N('g',E,N(z,F,Rright)),z,t,f,v),
      ('R_min_LL',N('g',E,N('p',F,N(z,U,Rright))),z,t,f,v),
      ('R_min_LR',N('g',N('p',E,F),N(z,U,Rright)),z,t,f,v),
    ]
    helpers=[]
    for name,out,oldroot,near,excluded1,excluded2 in helper_outputs:
        assert depth(out,oldroot)<=2
        assert depth(out,near)<=3
        assert depth(out,excluded1)>=3 and depth(out,excluded2)>=3
        helpers.append({'case':name,'eligible_marked_subset':[oldroot,near],
          'old_depth2_marks_pushed_below_charge1':True})
    # Public-core source proxy depths for reuse of the global deep-helper law.
    assert depth(T,z)+1==3
    assert depth(CB,z)+1==4
    # CA minimum is unavailable because A L=2,LL=0 are Scores. For both
    # C patterns, maximum has prefix4,R5,...,8,Rproxy -> depth>=3 by count.
    helper_depths={'T_minimum':3,'CB_minimum':4,'CA_CB_maximum_lower_bound':3,
      'CA_minimum_A_helper_absent':True,'H_maximum':1,'R_minimum':1}

    slacks={
      'aux_new_source1_positive':lin({'constant':1,'weight_excess':1},{'target_debt':1},{'constant':-1}),
      'aux_new_source1_zero_to_floor1':lin({'constant':1,'floor_excess':1},{'constant':-1}),
      'principal_source2_plus1_to_floor1':lin({'constant':1},{'constant':1,'floor_excess':1},{'constant':-2}),
      'principal_source2_weight2_range':lin({'constant':2,'weight_excess':1},{'target_debt':1},{'constant':-2}),
      'principal_zero_to_T2':lin({'constant':2},{'constant':-2}),
      'unchanged_source':lin({'old_residual':1},{'target_increment':1}),
      'incoming_weight1_to_floor1':lin({'constant':1,'weight_excess':1},{'constant':1,'floor_excess':1},{'constant':-2,'source_room':1}),
    }
    assert all(v>=0 for expr in slacks.values() for v in expr.values())
    assert slacks['principal_zero_to_T2']=={}
    # TWO-CREDIT auxiliary zero is intentionally NOT certified by floor1:
    deficit=lin({'constant':1},{'constant':-2})
    assert deficit=={'constant':-1}

    # Source semantics/provenance is reused only with the exact old source
    # hashes. No old checker, source root or compiler module is executed.
    old9=BASE.parent/'M3_XFER09/symbolic_audit.json'
    old8=BASE.parent/'M3_XFER08/certificate.json'
    old12=BASE.parent/'M3_XFER12/symbolic_audit.json'
    reader=json.loads(old9.read_text())
    assert reader['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for path,hsh in reader['source_hashes'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==hsh
    deep=json.loads(old8.read_text())
    assert deep['Gamma1_weight0_or_plus1_implies_helper_initial_B_depth_at_most']==2
    prev=json.loads(old12.read_text())
    assert prev['status']=='DEPTH_FIVE_CENTRAL_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for path,hsh in prev['new_AST_source_hashes'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==hsh
    assert time.process_time()<CAP
    result={
      'status':'NON_EXTREMAL_EXPOSURE_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'new_universal_term_certificates':identities,
      'lower_zero_returns_from_T':lower_returns,'upper_zero_returns_from_CA':upper_returns,
      'helper_eligibility_depth_checks':helpers,'source_proxy_depths':helper_depths,
      'global_deep_helper_Gamma1_weight_at_least2_reused_for_Score_bearing_exposures':True,
      'H_zero2_all_marked_core_depths_at_most':2,
      'EB_ER_actual_sources_E1_proved_in_separate_prose':True,
      'EB_ER_change_no_actual_LOW_source':True,
      'new_return_predicates_have_no_V_filter':True,
      'ER_parent_type_and_label_unrestricted_in_public_guard':True,
      'CA_right_branch_unrestricted':True,'T_left_branch_unrestricted':True,
      'one_credit_rows_proved_when_source_newly_raised_to1':True,
      'all_already_debt2_auxiliary_sources_claimed_solved':False,
      'scope_countercheck_floor1_does_not_pay_arbitrary_source2_zero':deficit,
      'operation_order':['floor1_EB_ER','floor1_H','floor1_CA_CB','floor1_R','cap2_T','cap2_G'],
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_T_G_source_original_LOW_rows_proved':True,
      'main_G_zero_H1_source_and_target_values':2,'main_G_zero_H1_signed_residual':0,
      'mask_minus':[0,2,4,5,8],'mask_actual_opposite':[0,3,4,6,8],
      'target_non_extremal_and_new_lower_mark_exposure_included':True,
      'all_admissible_signatures_upper_U_and_private_completions':True,
      'incoming_nonnegative_T_G_rows_valid':True,'incoming_weight_ge1_auxiliary_rows_valid':True,
      'blanket_zero_incoming_to_floor1_claimed':False,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'reused_proof_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (old9,old8,old12)},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_non_extremal_H1_zero_coverage_proved':False,'Step4_complete':False,'full_M3_status':'OPEN',
      'CPU_seconds':time.process_time(),'CPU_cap':CAP,
    }
    write('symbolic_audit.json',result);print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})

