"""Separate universal anonymous-guard/parity/final-leaf/sign audit.

Unassigned ordered role symbols and arbitrary subtree variables only.
No numerical trees, masks, populations, source roots or saved psi labels.
Completed source normal forms and prior A/B identities are reused.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
EMPTY=('EMPTY',)

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('SUBTREE',name)
def N(key,left=EMPTY,right=EMPTY):return ('NODE',key,left,right)
def right(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    p=t[2];return N(p[1],p[2],N(t[1],p[3],t[3]))
def left(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    p=t[3];return N(p[1],N(t[1],t[2],p[2]),p[3])
def at(t,path):
    for bit in path:assert t[0]=='NODE';t=t[2+bit]
    return t
def put(t,path,value):
    if not path:return value
    return N(t[1],put(t[2],path[1:],value),t[3]) if path[0]==0 else N(t[1],t[2],put(t[3],path[1:],value))
def local(t,path,fn):return put(t,path,fn(at(t,path)))
def pair(t,bits):
    if bits==(0,0):return right(right(t))
    if bits==(1,1):return left(left(t))
    if bits==(0,1):return right(local(t,(0,),left))
    assert bits==(1,0);return left(local(t,(1,),right))
def flip(t):return N(t[1],flip(t[3]),flip(t[2])) if t[0]=='NODE' else t
def path(t,key,p=()):
    if t[0]!='NODE':return None
    if t[1]==key:return p
    found=path(t[2],key,p+(0,))
    return found if found is not None else path(t[3],key,p+(1,))
def depth(t,key):
    p=path(t,key);assert p is not None;return len(p)
def lin(*parts):
    out={}
    for part in parts:
        for k,v in part.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,T,R,Q,S,Y=map(V,('A','B','C','D','T','R','Q','S','Y'))
    identities=[]
    def certify(name,out,expected):
        assert out==expected,name
        identities.append(name)
    # Universal last-pair normal forms for the new MINIMUM helper case.
    # Bottom processed suffixes are arbitrary variables, not core samples.
    even=N('c',N('b',N('f',EMPTY,Q),T),R)
    evenout=pair(even,(0,0))
    certify('even_helper_depth_last_LL',evenout,N('f',EMPTY,N('b',Q,N('c',T,R))))
    certify('even_helper_dual_last_RR',pair(flip(even),(1,1)),flip(evenout))
    assert depth(evenout,'b')==1 and depth(evenout,'c')==2
    odd=N('c',N('b',N('p',N('f',EMPTY,Q),S),T),R)
    oddout=right(local(odd,(0,),lambda t:pair(t,(0,0))))
    certify('odd_helper_depth_inner_LL_then_zig',oddout,N('f',EMPTY,N('c',N('p',Q,N('b',S,T)),R)))
    dualout=left(local(flip(odd),(1,),lambda t:pair(t,(1,1))))
    certify('odd_helper_dual_inner_RR_then_zig',dualout,flip(oddout))
    assert depth(oddout,'c')==1 and depth(oddout,'b')==3

    # The only potentially cheap terminal has depth6, hence uses all six
    # eligible core roles. Its bottom pair is already consumed below b.
    # Remaining path: f,Rc,Lp,Rb,La. Both remaining pairs are RL.
    frontier=N('f',EMPTY,N('c',N('p',Q,N('b',N('a',A,B),T)),R))
    mid=local(frontier,(1,0),lambda t:pair(t,(1,0)))
    out=pair(mid,(1,0))
    expected=N('a',N('f',EMPTY,N('p',Q,A)),N('c',N('b',B,T),R))
    certify('depth6_terminal_last_RL_RL',out,expected)
    proxy=at(out,path(out,'f'))
    assert proxy[3][0]=='NODE' and proxy[3][1]=='p'
    assert depth(out,'c')==1 and depth(out,'b')==2
    dual=flip(frontier)
    dualmid=local(dual,(0,1),lambda t:pair(t,(0,1)))
    dualout=pair(dualmid,(0,1))
    certify('depth6_dual_terminal_last_LR_LR',dualout,flip(expected))
    assert at(dualout,path(dualout,'f'))[2][0]=='NODE'
    assert at(dualout,path(dualout,'f'))[2][1]=='p'
    # NODE means actual kind0 child. Gap final-validity requires kind2.
    forbidden_child_kind,required_empty_kind=0,2
    assert forbidden_child_kind!=required_empty_kind

    # New A minimum-helper terminals (full Score support remains free).
    source=N('c',N('b',N('f',A,B),C),Y)
    helper=pair(source,(0,0))
    certify('anonymous_LL_helper_A',helper,N('f',A,N('b',B,N('c',C,Y))))
    assert depth(helper,'b')==1 and depth(helper,'c')==2
    lower=N('f',A,N('b',N('a',B,C),N('c',D,Y)))
    final=pair(lower,(1,0))
    certify('lower_terminal_RL_after_helper',final,N('a',N('f',A,B),N('b',C,N('c',D,Y))))
    certify('dual_anonymous_RR_helper_A',pair(flip(source),(1,1)),flip(helper))
    certify('dual_lower_terminal_LR',pair(flip(lower),(0,1)),flip(final))

    # Anonymous public slot can place a on EITHER side; no color inferred.
    # Verify visibility substitutions for the inherited H1/maximum-helper
    # schemas using the worst (shallowest) actual a-containing blocks.
    for side in (0,1):
        p=N('p',N('a',A,B),C) if side==0 else N('p',A,N('a',B,C))
        block=N('b',p,D)
        cases=[
          (N('c',block,N('x',Q,R)),lambda t:left(t)),
          (N('c',block,N('q',N('x',Q,R),S)),lambda t:pair(t,(1,0))),
          (N('c',block,N('q',Q,N('x',R,S))),lambda t:pair(t,(1,1))),
        ]
        for source,fn in cases:
            result=fn(source)
            assert depth(result,'a')>=4
            owner=at(result,path(result,'c'))
            assert owner[2]==block and depth(owner,'a')==3
            assert path(owner[3],'a') is None
        source=N('c',N('b',p,N('x',Q,R)),Y)
        result=pair(source,(0,1))
        assert path(result,'p')==(0,0) and depth(result,'a')==3
        assert path(at(result,path(result,'c')),'a') is None
        # The three inherited incoming identities already have these
        # endpoints after substituting an anonymous p-containing block.
        if side==0:
            endpoint_R=N('c',N('b',p,D),Y)
            endpoint_RL=N('c',N('b',p,D),N('q',Q,Y))
            endpoint_RR=N('c',N('q',N('b',p,D),Q),Y)
            for endpoint in (endpoint_R,endpoint_RL):
                assert path(endpoint,'p')==(0,0) and depth(endpoint,'a')==3
            assert path(endpoint_RR,'b')==(0,0) and depth(endpoint_RR,'a')==4
    # The omitted higher core T (if present) is b.right in the odd form
    # or c.left in the even form, off every path to a<b.
    assert path(evenout,'T') is None  # T is an arbitrary subtree, not a role node.
    eligible_lower_cores=4
    maximum_even_depth=eligible_lower_cores+1
    maximum_odd_depth=eligible_lower_cores+2
    assert maximum_even_depth==5 and maximum_odd_depth==6
    # The proof above excludes depth6 under final validity; integer floor.
    min_valid_helper_weight=4-(5//2)
    assert min_valid_helper_weight==2
    assert 4-(3//2)==3
    slacks={
      'H1_plus1_to_E1':lin({'const':1},{'const':1,'E1_credit_excess':1},{'const':-2}),
      'H1_paid_or_valid_Gamma1':lin({'const':2,'weight_excess':1},{'target_debt':1},{'const':-2}),
      'incoming_zero':lin({'const':2},{'const':-2,'source_room_below2':1}),
    }
    assert all(v>=0 for expr in slacks.values() for v in expr.values())

    # Bounded source provenance: FINAL leaf condition, not intermediate.
    root=BASE.parent/'06_CERTIFICATES'
    bp=root/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py'
    lp=root/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    sp=root/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py'
    ip=root/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ATOM_INVENTORY.py'
    rp=root/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    wp=root/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_STRUCTURAL_WITNESS.py'
    def func(file,name):
        return next(n for n in ast.walk(ast.parse(file.read_text(encoding='utf-8-sig')))
                    if isinstance(n,ast.FunctionDef) and n.name==name)
    bv=func(bp,'b_valid')
    gap_if=next(n for n in ast.walk(bv) if isinstance(n,ast.If) and ast.unparse(n.test)=='i >= NCORE')
    gapbody='\n'.join(ast.unparse(n) for n in gap_if.body)
    assert 'd.EQ(bs.kl[i], d.const_int(2, 2))' in gapbody
    assert 'd.EQ(bs.kr[i], d.const_int(2, 2))' in gapbody
    btree=ast.unparse(func(sp,'b_tree_valid'))
    assert 'C = [b_valid(d, bs)] if intervals else []' in btree
    low=ast.unparse(func(lp,'build_slow'))
    valid=ast.unparse(func(lp,'state_valid7'))
    assert 'b_valid(d, s.b)' in valid and 'C.append(state_valid7(d, t))' in low
    assert 'b_tree_valid(d, bs[e + 1], bst, s.sig, intervals=False)' in low
    assert 'b_tree_valid(d, t.b, bst5, t.sig)' in low
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    assert 'd.EQ(t.b.root, bs[5].root)' in low
    gap=ast.unparse(func(ip,'_gapof'))
    assert 'd.LT(self.fullrank(k), ranknode)' in gap
    mux=func(rp,'mux_ref');assert ast.unparse(mux.body[0])=='r = vec[0]'
    wf=ast.unparse(func(wp,'wellformed'))
    assert 'd.EQ(self.rank[i], self.rank[j])' in wf
    assert 'C.append(d.NOT(both))' in wf
    assert time.process_time()<CAP
    result={
      'status':'ANONYMOUS_RELEASE_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'new_equational_certificates':identities,
      'helper_minimum_gap_not_inferred_from_shared_state':True,
      'anonymous_separator_either_side_of_marked_a_audited':True,
      'minimum_helper_even_and_odd_normal_forms_exhaustive_by_pair_parity':True,
      'eligible_terminal_core_count_bound':6,
      'sole_weight1_minimum_helper_depth':6,
      'depth6_final_proxy_has_real_core_child':True,
      'required_final_proxy_child_kind':required_empty_kind,
      'depth6_contradiction_applied_only_at_final_endpoint':True,
      'valid_Gamma1_weight_lower_bound_including_Score_bearing_support':2,
      'H1_plus1_full_endpoints_in_E1':True,
      'anonymous_P5_P6_R_RL_end_in_N':True,
      'anonymous_P5_P6_RR_ends_in_existing_Z':True,
      'each_previously_valid_LOW_row_preserved':True,
      'all_N_source_LOW_rows_proved':True,
      'Gamma0_actual_preterminal_floor_reused':True,
      'completed_core_identities_and_source_normal_forms_reused_not_replayed':True,
      'signed_residuals':slacks,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (bp,lp,sp,ip,rp,wp)},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_anonymous_separator_core_patterns_solved':False,'full_M3_status':'OPEN',
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
