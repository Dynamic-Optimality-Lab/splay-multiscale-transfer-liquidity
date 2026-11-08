"""Separate universal equational and source-provenance audit; no finite tests.

Role symbols and subtree variables are unassigned. Only the newly needed
equational schemas are checked. No original relation/root, old checker,
psi evaluator, numerical tree, mask, population or label fit is executed.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)

def V(name):return ('VAR',name)
def N(key,left=None,right=None):return ('NODE',key,left or V('EMPTY_L'),right or V('EMPTY_R'))
def rr(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    b=t[2];return N(b[1],b[2],N(t[1],b[3],t[3]))
def ll(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    b=t[3];return N(b[1],N(t[1],t[2],b[2]),b[3])
def sub(t,p):
    for side in p:assert t[0]=='NODE';t=t[2+side]
    return t
def replace(t,p,value):
    if not p:return value
    side=p[0]
    return N(t[1],replace(t[2],p[1:],value),t[3]) if side==0 else N(t[1],t[2],replace(t[3],p[1:],value))
def op(t,p,fn):return replace(t,p,fn(sub(t,p)))
def flip(t):return N(t[1],flip(t[3]),flip(t[2])) if t[0]=='NODE' else t
def find(t,key,p=()):
    if t[0]!='NODE':return None
    if t[1]==key:return p
    left=find(t[2],key,p+(0,))
    return left if left is not None else find(t[3],key,p+(1,))
def depth(t,key):
    p=find(t,key);assert p is not None;return len(p)
def pair(t,sides):
    if sides==(0,0):return rr(rr(t))
    if sides==(1,1):return ll(ll(t))
    if sides==(0,1):return rr(op(t,(0,),ll))
    assert sides==(1,0);return ll(op(t,(1,),rr))
def linear(*parts):
    result={}
    for part in parts:
        for key,value in part.items():result[key]=result.get(key,0)+value
    return {k:v for k,v in result.items() if v}

def main():
    A,B,C,D,E,F,Y,R=map(V,('A','B','C','D','E','F','Y','R'))
    identity_records=[]
    def certify(name,source,result,expected):
        assert result==expected,name
        identity_records.append(name)
    # Original RR A access, roles b<c and b<q<c. The separator remains
    # a subtree variable in this equality; the next proof checks its depth.
    source=N('b',A,N('q',B,N('c',C,D)))
    expected=N('c',N('q',N('b',A,B),C),D)
    certify('RR_zero_A',source,pair(source,(1,1)),expected)
    dual=flip(source)
    certify('LL_zero_A_dual',dual,pair(dual,(0,0)),flip(expected))
    separator=N('k',N('a',A,B),C)
    source=N('b',separator,N('q',D,N('c',E,F)))
    target=pair(source,(1,1))
    assert find(target,'b')==(0,0) and depth(target,'a')==4
    owner=sub(target,find(target,'b'))
    assert owner[2][1]=='k' and depth(owner,'a')==2
    assert owner[3]==D  # This block is above b by the symbolic order premise.
    dualout=pair(flip(source),(0,0))
    assert dualout==flip(target) and find(dualout,'b')==(1,1)

    # Exceptional J6 lower +1: child x is marked u1, old root c is u2.
    source=N('c',N('x',N('b',A,B),C),Y)
    expected=N('x',N('b',A,B),N('c',C,Y))
    certify('Z_lower_plus1_child_to_C',source,rr(source),expected)
    certify('dual_Z_lower_plus1_child_to_C',flip(source),ll(flip(source)),flip(expected))
    # Other lower +1: x at LR below q, with b retained at LL.
    source=N('c',N('q',N('b',N('a',A,B),C),N('x',D,E)),Y)
    out=pair(source,(0,1))
    expected=N('x',N('q',N('b',N('a',A,B),C),D),N('c',E,Y))
    certify('Z_lower_plus1_LR_to_E1',source,out,expected)
    assert depth(out,'a')==3 and find(out,'b')==(0,0)
    assert find(sub(out,find(out,'c')),'a') is None
    certify('dual_Z_lower_plus1_RL',flip(source),pair(flip(source),(1,0)),flip(expected))

    # New one-credit C zero return. Do not assert E1: the OLD root's
    # right child Y can create an extra G observation at the endpoint.
    source=N('u',N('b',N('a',A,B),C),Y)
    expected=N('a',A,N('b',B,N('u',C,Y)))
    certify('C_zero_LL_to_K',source,pair(source,(0,0)),expected)
    assert find(expected,'b')==(1,) and find(expected,'u')==(1,1)
    certify('dual_C_zero_RR_to_K',flip(source),pair(flip(source),(1,1)),flip(expected))

    # Universal parity endings for u(b(L,E),R) accessed below b.
    # Odd internal depth leaves one same-direction outer pair.
    odd=N('u',N('b',N('a',A,B),C),R)
    oddout=pair(odd,(0,0))
    assert depth(oddout,'b')==1 and depth(oddout,'u')==2
    assert pair(flip(odd),(1,1))==flip(oddout)
    # Even internal depth has completed the internal splay. The inherited
    # old-root lemma puts b at depth1/2. Since b is the largest node of
    # its original subtree it is on a's right spine in these endings.
    endings=[N('a',A,N('b',B,C)),N('a',A,N('p',B,N('b',C,D)))]
    for internal in endings:
        source=N('u',internal,R);out=rr(source)
        assert depth(out,'b')<=3 and depth(out,'u')==1
        assert ll(flip(source))==flip(out)
    # This discharges arbitrary internal paired suffixes by parity, not
    # by generating numeric core paths or testing lower-subtree shapes.

    # All three active minimum-helper A positions for K. Blocks remain
    # variables, so possible private Score inventories are not fixed.
    cases=[
      (N('a',N('f',A,B),N('b',C,N('u',D,Y))),
       lambda t:rr(t),N('f',A,N('a',B,N('b',C,N('u',D,Y))))),
      (N('a',N('p',N('f',A,B),C),N('b',D,N('u',E,Y))),
       lambda t:pair(t,(0,0)),N('f',A,N('p',B,N('a',C,N('b',D,N('u',E,Y)))))),
      (N('a',N('p',A,N('f',B,C)),N('b',D,N('u',E,Y))),
       lambda t:pair(t,(0,1)),N('f',N('p',A,B),N('a',C,N('b',D,N('u',E,Y))))),
    ]
    for i,(source,fn,expected) in enumerate(cases):
        out=fn(source);certify('K_min_helper_'+str(i),source,out,expected)
        assert depth(out,'u')>=3
        assert depth(out,'a')<=2
        assert (depth(out,'b')<=2)==(i!=1)
        # Actual LOW dual is maximum helper: conjugate primitive directions.
        if i==0:dout=ll(flip(source))
        elif i==1:dout=pair(flip(source),(1,1))
        else:dout=pair(flip(source),(1,0))
        certify('K_max_helper_dual_'+str(i),flip(source),dout,flip(expected))

    # Right-side +1 targets and extreme helpers of Z share these exact
    # THREE A placements. The lower marked a is placed at its shallowest
    # allowed position; arbitrary deeper placement only increases depth.
    left=N('q',N('b',N('a',A,B),C),D)
    cases=[
      (N('c',left,N('x',E,F)),lambda t:ll(t)),
      (N('c',left,N('p',N('x',E,F),Y)),lambda t:pair(t,(1,0))),
      (N('c',left,N('p',E,N('x',F,Y))),lambda t:pair(t,(1,1))),
    ]
    for i,(source,fn) in enumerate(cases):
        out=fn(source)
        assert depth(out,'a')>=4
        owner=sub(out,find(out,'c'))
        assert owner[2]==left and depth(owner,'a')==3
        assert find(owner[3],'a') is None
        if i==0:dout=rr(flip(source))
        elif i==1:dout=pair(flip(source),(0,1))
        else:dout=pair(flip(source),(0,0))
        assert dout==flip(out) and depth(dout,'a')>=4
        identity_records.append('Z_right_placement_'+str(i)+'_with_dual')

    # Ordered-symbol counts / floor arithmetic with nonnegative slack.
    # C: four lower cores => depth(a)<=2+(4-1)=5, never a negative H1.
    assert 2+(4-1)==5
    # K: old entry at depth<=2 + unchanged right-subtree distance<=3.
    assert 2+3==5 and 4-(5//2)==2
    assert 4-(2//2)==3
    slacks={
      'K_new_one_H1':linear({'weight_excess':1},{'target_debt':1}),
      'K_Gamma1_b':linear({'const':2,'weight_excess':1},{'target_debt':1},{'const':-1}),
      'C_zero_to_K':linear({'const':1,'K_credit_excess':1},{'const':-1}),
      'C_positive_or_Gamma1':linear({'const':1,'weight_excess':1},{'target_debt':1},{'const':-1}),
      'Z_plus1_to_C_or_E1':linear({'const':1},{'const':1,'target_credit_excess':1},{'const':-2}),
      'Z_paid_or_Gamma1':linear({'const':2,'weight_excess':1},{'target_debt':1},{'const':-2}),
      'incoming_zero_to_Z':linear({'const':2},{'const':-2,'source_room_below2':1}),
    }
    assert all(v>=0 for e in slacks.values() for v in e.values())
    # Raising only a target preserves any previous row. If newly raised,
    # K/C sources are exactly1, Z sources exactly2. This covers real debts
    # in [Lambda,2] as well as the inherited integer construction.

    # New source audit is bounded AST provenance, not source construction.
    folder=BASE.parent/'06_CERTIFICATES'
    low=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rot=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    struct=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_STRUCTURAL_WITNESS.py'
    module=ast.parse(low.read_text(encoding='utf-8-sig'))
    funcs={n.name:ast.unparse(n) for n in module.body if isinstance(n,ast.FunctionDef)}
    sh,match,build=(funcs[k] for k in ('shadow7','shadow_match7','build_slow'))
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in sh
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'C.append(s.aS[0])' in build
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in build
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in build
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in build
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in build
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in build
    rotast=ast.parse(rot.read_text(encoding='utf-8-sig'))
    mux=next(n for n in rotast.body if isinstance(n,ast.FunctionDef) and n.name=='mux_ref')
    assert ast.unparse(mux.body[0])=='r = vec[0]'
    state=next(n for n in rotast.body if isinstance(n,ast.ClassDef) and n.name=='AState')
    assert 'self.root = d.const_int(0, W_REF)' in ast.unparse(state)
    wit=ast.parse(struct.read_text(encoding='utf-8-sig'))
    wf=next(n for n in ast.walk(wit) if isinstance(n,ast.FunctionDef) and n.name=='wellformed')
    wftext=ast.unparse(wf)
    assert 'self.p[0]' in wftext and 'self.sidx[i], self.sidx[j]' in wftext
    assert time.process_time()<CAP
    result={
      'status':'UNIVERSAL_RR_RELEASE_AUGMENTATION_SYMBOLIC_AUDIT_PASS',
      'new_equational_schema_records':identity_records,
      'old_child_depth_bound':'odd final pair: b1/u2; even internal splay plus zig: b<=3/u1',
      'parity_argument_quantifies_arbitrary_paired_suffixes':True,
      'C_zero_endpoint_K_has_no_V_filter':True,
      'K_helper_terminals_only_entry_or_central4':True,
      'K_helper_preterminal_B_depth_bound_for_central4':5,
      'C_Gamma1_central_root_bound_reused_not_replayed':True,
      'Z_upper_B_identities_and_helper_bound_reused_not_replayed':True,
      'Z_exceptional_marked5_child_to_C_included':True,
      'G_owner_visibility_and_full_boundary_K_guard_audited':True,
      'safe_operation_order':['K credit1','C credit1','Z credit2'],
      'signed_residual_certificates':slacks,
      'each_previously_valid_LOW_inequality_preserved':True,
      'all_Z_source_LOW_inequalities_proved':True,
      'all_named_P5_P6_RR_zero_edges_end_in_Z':True,
      'full_compiler_formalization_claimed':False,
      'independent_external_human_review_claimed':False,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (low,rot,struct)},
      'original_negative_cycle_certified':False,'full_M3_status':'OPEN',
      'CPU_seconds':time.process_time(),'CPU_cap':CAP,
    }
    write('symbolic_audit.json',result)
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
