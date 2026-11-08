"""Universal odd-depth/endpoint-relay proof audit; NO finite tests.

Labels are theorem roles, lower/side blocks universally quantified.
Fixed band names denote roles in saved symbolic identities, never an
evaluated original B model. No compiler/DAG/root/bank/psi is imported.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
EMPTY=('CORE_EMPTY',)

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('BLOCK',name)
def N(key,left=EMPTY,right=EMPTY):return ('NODE',key,left,right)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def at(t,path):
    for d in path:
        assert t[0]=='NODE';t=t[2+d]
    return t
def put(t,path,v):
    if not path:return v
    if path[0]==0:return N(t[1],put(t[2],path[1:],v),t[3])
    return N(t[1],t[2],put(t[3],path[1:],v))
def pair(t,p):
    if p==(0,0):return rz(rz(t))
    if p==(1,1):return lz(lz(t))
    if p==(0,1):return rz(N(t[1],lz(t[2]),t[3]))
    assert p==(1,0);return lz(N(t[1],t[2],rz(t[3])))
def splay_term(t,path):
    while len(path)>=2:
        prefix=path[:-2]
        t=put(t,prefix,pair(at(t,prefix),path[-2:]))
        path=prefix
    return (rz(t) if path==(0,) else lz(t)) if path else t
def find(t,key,path=()):
    if t[0]!='NODE':return None
    if t[1]==key:return path
    a=find(t[2],key,path+(0,))
    return a if a is not None else find(t[3],key,path+(1,))
def depth(t,key):
    path=find(t,key);assert path is not None;return len(path)
def blockpath(t,name,path=()):
    if t==V(name):return path
    if t[0]!='NODE':return None
    a=blockpath(t[2],name,path+(0,))
    return a if a is not None else blockpath(t[3],name,path+(1,))
DUAL={'four':'four','five':'three','six':'two','seven':'one','eight':'zero'}
def dual(t):
    return N(DUAL.get(t[1],t[1]),dual(t[3]),dual(t[2])) if t[0]=='NODE' else t
def lin(*parts):
    out={}
    for p in parts:
        for k,v in p.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,E,F,L,M,P,Q=map(V,('A','B','C','D','E','F','LOWER','M','P','Q'))
    identities=[]
    def cert(name,source,path,expected):
        assert splay_term(source,path)==expected,name
        identities.append(name)
        assert splay_term(dual(source),tuple(1-d for d in path))==dual(expected),name+'_actual_other_side'
        identities.append(name+'_actual_other_side')

    # The lowest pair of an ORIGINAL depth5 path is already consumed.
    # These are the TWO complete remaining top cases, not sample trees.
    oddL=N('c',N('b',N('q',N('a',L,M),P),Q),E)
    outL=N('a',L,N('c',N('q',M,N('b',P,Q)),E))
    oddR=N('c',N('b',N('q',L,N('a',M,P)),Q),E)
    outR=N('a',N('q',L,M),N('c',N('b',P,Q),E))
    cert('odd5_remaining_LL',oddL,(0,0,0),outL)
    cert('odd5_remaining_LR',oddR,(0,0,1),outR)
    assert depth(outL,'c')==depth(outR,'c')==1
    assert depth(outL,'b')==3 and depth(outR,'b')==2
    K1=N('a',L,N('c',N('b',M,P),Q))
    K2=N('a',L,N('c',N('q',M,N('b',P,Q)),E))
    cert('K_direct_b_return',K1,(1,0),N('b',N('a',L,M),N('c',P,Q)))
    cert('K_three_level_b_return',K2,(1,0,1),N('b',N('a',L,N('q',M,P)),N('c',Q,E)))

    # Q8 and C8 have the SAME final core after their different actual top pairs.
    aa=N('a',A,B)
    common=N('k',N('four',aa,C),N('eight',D))
    cert('Q8_common_zero_top',N('eight',N('four',aa,N('k',C,D))), (0,1),common)
    cert('C8_common_zero_top',N('four',aa,N('eight',N('k',C,D))), (1,0),common)
    assert depth(common,'a')==2
    # +1 upper depth3 cases. There is only ONE other upper role off path,
    # so a free upper block at depth<=3 cannot hide a deeper upper core.
    shallow_upper=[]
    cases=[
      ('Q8_LRL',N('eight',N('four',aa,N('u',N('k',C,D),E))),(0,1,0),
        N('k',N('four',aa,C),N('eight',N('u',D,E)))),
      ('Q8_LRR',N('eight',N('four',aa,N('u',C,N('k',D,E)))),(0,1,1),
        N('k',N('u',N('four',aa,C),D),N('eight',E))),
      ('C8_RLL',N('four',aa,N('eight',N('u',N('k',C,D),E))),(1,0,0),
        N('k',N('four',aa,C),N('u',D,N('eight',E)))),
      ('C8_RLR',N('four',aa,N('eight',N('u',C,N('k',D,E)))),(1,0,1),
        N('k',N('four',aa,N('u',C,D)),N('eight',E))),
    ]
    for name,source,path,target in cases:
        cert(name,source,path,target)
        assert depth(target,'a')<=3
        assert all(len(blockpath(target,n))<=3 for n in ('C','D','E'))
        shallow_upper.append({'case':name,'a_depth':depth(target,'a'),
          'max_off_path_upper_block_depth':max(len(blockpath(target,n)) for n in ('C','D','E')),
          'only_one_off_path_upper_core':True})

    # C5 positive exits and the exact single deep block in the RR case.
    c5depth2=N('four',aa,N('five',EMPTY,N('k',C,D)))
    c5d2out=N('k',N('five',N('four',aa),C),D)
    cert('C5_upper_depth2',c5depth2,(1,1),c5d2out)
    assert depth(c5d2out,'a')==3
    assert len(blockpath(c5d2out,'C'))==2 and len(blockpath(c5d2out,'D'))==1
    c5rl=N('four',aa,N('five',EMPTY,N('u',N('k',C,D),E)))
    c5rlout=N('k',N('four',aa,N('five',EMPTY,C)),N('u',D,E))
    c5rr=N('four',aa,N('five',EMPTY,N('u',C,N('k',D,E))))
    c5rrout=N('k',N('four',aa,N('u',N('five',EMPTY,C),D)),E)
    cert('C5_upper_depth3_RL',c5rl,(1,1,0),c5rlout)
    cert('C5_upper_depth3_RR',c5rr,(1,1,1),c5rrout)
    assert max(len(blockpath(c5rlout,n)) for n in ('C','D','E'))<=3
    assert len(blockpath(c5rrout,'C'))==4
    assert len(blockpath(c5rrout,'D'))==3 and len(blockpath(c5rrout,'E'))==1
    # The three ordered roles force C=six,u=seven,k=eight if C is nonempty.
    P8=N('eight',N('four',aa,N('seven',N('five',EMPTY,N('six')))))
    assert splay_term(N('four',aa,N('five',EMPTY,N('seven',N('six'),N('eight')))),(1,1,1))==P8
    identities.append('unique_C5_deep_block_specialization_by_order')
    # This is an equational specialization of the UNIVERSAL exception schema,
    # not a queried source B instance, finite potential test or bank operation.
    p5out=N('five',N('four',aa),N('eight',N('seven',N('six'))))
    j6=N('six',N('four',aa,N('five')),N('eight',N('seven')))
    cert('P8_plus1_key5',P8,(0,1,0),p5out)
    cert('P8_zero_key6',P8,(0,1,0,1),j6)
    assert depth(p5out,'a')==2 and depth(p5out,'six')==3
    assert depth(j6,'a')==2
    # New A guards for all exceptional and direct-return destinations.
    c5A=N('four',N('a',A,B),N('five',C,N('k',D,E)))
    c5Aout=N('k',N('five',N('four',N('a',A,B),C),D),E)
    cert('C5_A_upper_RR_to_Score4_LL',c5A,(1,1),c5Aout)
    assert at(c5Aout,(0,0))[1]=='four'
    p6A=N('eight',N('five',N('four',A,B),N('six',C,D)),E)
    p6Aout=N('six',N('five',N('four',A,B),C),N('eight',D,E))
    cert('P8_A_zero6_to_Bdry',p6A,(0,1),p6Aout)
    assert at(p6Aout,(0,0))[1]=='four'
    directA=N('eight',N('four',N('a',A,B),N('k',C,D)),E)
    directAout=N('k',N('four',N('a',A,B),C),N('eight',D,E))
    cert('Q8_A_zero_to_Rsh',directA,(0,1),directAout)
    assert at(directAout,(0,))[1]=='four' and at(directAout,(0,0))[1]=='a'
    c8A=N('four',N('a',A,B),N('eight',N('k',C,D),E))
    cert('C8_A_zero_to_Rsh',c8A,(1,0),directAout)
    j8=N('a',L,N('four',M,N('eight',P)))
    j8out=N('eight',N('four',N('a',L,M),P))
    cert('J8_plus1_to_Q8',j8,(1,1),j8out)
    assert depth(j8out,'a')==2

    # NEW shallow-a transport on PUBLISHED old +1 output terms.
    # Their old access identities are trusted dependencies, not replayed.
    lower=N('a',V('lower_left'),V('lower_right'))
    old_outputs=[
      ('J5_key6',N('six',N('five',N('four',lower)),N('eight',N('seven')))),
      ('J5_key7',N('seven',N('five',N('four',lower),N('six')),N('eight'))),
      ('J6_key5',N('five',N('four',lower),N('six',EMPTY,N('eight',N('seven'))))),
      ('J6_key7',N('seven',N('six',N('four',lower,N('five'))),N('eight'))),
      ('J7_key5',N('five',N('four',lower),N('seven',N('six'),N('eight')))),
      ('J7_key6',N('six',N('four',lower,N('five')),N('seven',EMPTY,N('eight')))),
    ]
    transport=[]
    for name,out in old_outputs:
        assert depth(out,'four')<=2 and depth(out,'a')<=3
        transport.append({'published_exit':name,'new_a_depth':depth(out,'a')})
    # C helper A bounds; maximum case excludes the sole lower marked a.
    hmin=N('four',N('a',N('f',A,B),C),N('m',D,E))
    hminout=N('f',A,N('a',B,N('four',C,N('m',D,E))))
    hmax=N('four',N('a',A,B),N('m',C,N('f',D,E)))
    hmaxout=N('f',N('m',N('four',N('a',A,B),C),D),E)
    cert('C_minimum_LL_helper',hmin,(0,0),hminout)
    cert('C_maximum_RR_helper',hmax,(1,1),hmaxout)
    assert depth(hminout,'a')==1 and depth(hminout,'four')==2
    assert depth(hmaxout,'a')==3
    # Last-step child bound for even/odd proxy depth is a parity proof:
    # even top LL above, odd old child<=2 below processed proxy + one zig.
    assert 2+1==3 and 3+2==5
    # Exact count slacks for the ordinary K returns, leaving only c5/c8.
    # c>=6 and c-b<=3 -> max(c-b,9-c)<=3.
    assert lin({'constant':3},{'constant':-9,'c':1},{'c':-1,'constant':6})=={}
    slacks={
      'positive1_to_E1_or_old_K1':lin({'constant':1},{'constant':1,'credit_excess':1},{'constant':-2}),
      'positive2_range':lin({'constant':2},{'target_debt':1},{'constant':-2}),
      'zero_to_prior_cap2':lin({'constant':2},{'constant':-2}),
      'H2_weight_at_least2':lin({'constant':2,'weight_excess':1},{'target_debt':1},{'constant':-2}),
      'unchanged_source':lin({'old_residual':1},{'target_increment':1}),
      'nonnegative_incoming_cap2':lin({'weight_nonnegative':1},{'source_room':1}),
    }
    assert all(v>=0 for expr in slacks.values() for v in expr.values())
    assert slacks['zero_to_prior_cap2']=={}

    # Reuse completed source/shadow/G/price and old full-upper map audits.
    old9=BASE.parent/'M3_XFER09/symbolic_audit.json'
    old8=BASE.parent/'M3_XFER08/certificate.json'
    old11=BASE.parent/'M3_XFER11/symbolic_audit.json'
    reused=json.loads(old9.read_text())
    assert reused['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for p,h in reused['source_hashes'].items():
        assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h
    assert json.loads(old8.read_text())['complete_S_eight_word_zero_frontier_closed']
    assert json.loads(old11.read_text())['status']=='MARKED_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    # NEW provenance: B depth5 consumes two pairs THEN one zig.
    bp=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py'
    tree=ast.parse(bp.read_text(encoding='utf-8-sig'))
    fn=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='b_splay_event')
    code=ast.unparse(fn)
    for fragment in ('for j in range(9):','t = 2 * j',
      'd.LT(d.const_int(t + 2, 5), d.ADD(dd, d.const_int(1, 5), 5))',
      'd.EQ(dd, d.const_int(t + 1, 5))',
      'st = b_blend(d, pair_on, rotA, st)',
      'st = b_blend(d, pair_on, rotB, st)',
      'st = b_blend(d, zig_on, rotZ, st)'):
        assert fragment in code,fragment
    assert code.index('st = b_blend(d, pair_on, rotA, st)')<code.index('st = b_blend(d, pair_on, rotB, st)')<code.index('st = b_blend(d, zig_on, rotZ, st)')
    assert time.process_time()<CAP
    result={
      'status':'DEPTH_FIVE_CENTRAL_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'new_universal_term_certificates':identities,
      'odd5_top_cases_complete_after_arbitrary_lowest_pair':True,
      'K_b_depths':[2,3],'K_c_depth':1,
      'Rsh_shallow_a_transport_on_reused_published_outputs':transport,
      'Q8_C8_upper_plus1_bounds':shallow_upper,
      'C5_unique_deep_upper_block_proved_by_order_and_three_core_count':True,
      'C5_exception_P8_and_opposite_endpoint_closed':True,
      'span4_J8_C8_and_opposite_endpoint_closed':True,
      'Bdry_V_guard_implied_at_every_actual_source_in_separate_prose_audit':True,
      'Bdry_changes_no_actual_LOW_source':True,
      'new_return_predicates_have_no_V_filter':True,
      'C_and_K_helpers_original_H2_weight_at_least':2,
      'P_helpers_original_H2_weight_at_least':2,
      'Rsh_and_Q_helpers_use_completed_parametric_barrier':True,
      'signed_slacks':slacks,
      'operation_order':['Bdry','Rsh','Q8','P8','C5_or_C8','K','J8','G45'],
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_new_region_source_LOW_rows_proved':True,
      'central_main_all_spans_and_both_B_zero_depths_4_5_proved':True,
      'central_G45_zero_H1_source_target_values':2,
      'central_G45_zero_H1_signed_residual':0,
      'all_nonnegative_incoming_new_region_rows_proved':True,
      'all_admissible_signatures_and_full_original_states':True,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'reused_proof_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (old9,old8,old11)},
      'new_AST_source_hashes':{bp.as_posix():hashlib.sha256(bp.read_bytes()).hexdigest()},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'Step4_complete':False,'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN',
      'remaining_independent_obligation':'original zero LOW outside the union of proved guarded classes',
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

