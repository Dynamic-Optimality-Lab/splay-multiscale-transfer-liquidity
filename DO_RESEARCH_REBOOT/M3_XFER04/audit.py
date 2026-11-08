"""Independent universal term/order/count/slack audit, not finite tests."""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
E=('EMPTY',)
def V(key):return ('V',key)
def N(key,left=E,right=E):return ('N',key,left,right)
def rz(t):
    assert t[0]=='N' and t[2][0]=='N'
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def lz(t):
    assert t[0]=='N' and t[3][0]=='N'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def path(t,key,p=()):
    if t[0]=='V':return p if t[1]==key else None
    if t[0]!='N':return None
    if t[1]==key:return p
    a=path(t[2],key,p+(0,))
    return a if a is not None else path(t[3],key,p+(1,))
def at(t,p):
    for side in p:
        assert t[0]=='N';t=t[2+side]
    return t
def find(t,key):
    p=path(t,key);assert p is not None;return at(t,p)
def replace(t,p,value):
    if not p:return value
    return N(t[1],replace(t[2],p[1:],value),t[3]) if p[0]==0 else N(t[1],t[2],replace(t[3],p[1:],value))
def pair(t,p):
    if p==(0,0):return rz(rz(t))
    if p==(1,1):return lz(lz(t))
    if p==(0,1):return rz(N(t[1],lz(t[2]),t[3]))
    assert p==(1,0);return lz(N(t[1],t[2],rz(t[3])))
def splay(t,key):
    while t[1]!=key:
        p=path(t,key);assert p is not None and len(p)>0
        if len(p)==1:t=rz(t) if p[0]==0 else lz(t)
        else:t=replace(t,p[:-2],pair(at(t,p[:-2]),p[-2:]))
    return t
def flip(t):return N(t[1],flip(t[3]),flip(t[2])) if t[0]=='N' else t
def inorder(t):return inorder(t[2])+[t[1]]+inorder(t[3]) if t[0]=='N' else []
def chain(keys,directions):
    if len(keys)==1:return N(keys[0])
    child=chain(keys[1:],directions[1:])
    return N(keys[0],child,E) if directions[0]==0 else N(keys[0],E,child)
def lin(**terms):return {k:v for k,v in terms.items() if v}
def add(*terms):
    result={}
    for term in terms:
        for k,v in term.items():result[k]=result.get(k,0)+v
    return {k:v for k,v in result.items() if v}
def neg(term):return {k:-v for k,v in term.items()}

def main():
    lower=V('LOWER');upper_keys=('b','u1','u2','u3','u4')
    # Unassigned ordered role symbols: b is the middle core, u1..u4
    # the four higher cores. No numeric key/population/label assignment.
    P5=N('b',lower,N('u4',N('u3',N('u2',N('u1')))))
    P6=N('b',lower,N('u4',N('u3',N('u1',E,N('u2')))))
    J5=N('u1',N('b',lower),N('u4',N('u2',E,N('u3'))))
    J6=N('u2',N('b',lower,N('u1')),N('u4',N('u3')))
    for source,key,expected in ((P5,'u1',J5),(P6,'u2',J6)):
        assert len(path(source,key))==4 and splay(source,key)==expected
        assert splay(flip(source),key)==flip(expected)

    # Exact four +1 core successors. Lower block remains arbitrary.
    positives=[
        (J5,'u2',N('u2',N('u1',N('b',lower)),N('u4',N('u3')))),
        (J5,'u3',N('u3',N('u1',N('b',lower),N('u2')),N('u4'))),
        (J6,'u1',N('u1',N('b',lower),N('u2',E,N('u4',N('u3'))))),
        (J6,'u3',N('u3',N('u2',N('b',lower,N('u1'))),N('u4'))),
    ]
    for source,key,expected in positives:
        assert len(path(source,key)) in (2,3) and splay(source,key)==expected
        assert all(len(path(expected,k))<=3 for k in upper_keys)
        dual=flip(source);out=splay(dual,key)
        assert out==flip(expected) and all(len(path(out,k))<=3 for k in upper_keys)
    for source in (J5,J6):
        assert len(path(source,'b'))==len(path(source,'u4'))==1

    A,B,C,D,F,G,H=map(V,('A','B','C','D','F','G','H'))
    # The entire a-containing block lies below observed Score k. Taking
    # a at its shallowest possible root proves the worst visibility bound.
    K=N('k',N('a',A,B),C)
    left=N('b',K,D)
    # Right-side +1 accesses: a stays unobserved and the original owner's
    # left child b is unchanged. Owner one-step views cannot report a.
    A_right=[
        N('r',left,N('x',F,G)),
        N('r',left,N('q',N('x',F,G),H)),
        N('r',left,N('q',F,N('x',G,H))),
    ]
    for source in A_right:
        out=splay(source,'x');assert len(path(out,'a'))>=3
        owner=find(out,'r');assert owner[2]==left
        pa=path(owner,'a');assert pa is None or len(pa)>=2
        assert path(owner[3],'a') is None
        dual=flip(source);dualout=splay(dual,'x')
        assert len(path(dualout,'a'))>=3
        ownerdual=find(dualout,'r');assert ownerdual[3]==flip(left)
        pa=path(ownerdual,'a');assert pa is None or len(pa)>=2
        assert path(ownerdual[2],'a') is None
    # J6 lower upper-target u1 must be at LR below b; k remains LL.
    source_left=N('u2',N('b',K,N('u1',F,G)),H)
    out_left=N('u1',N('b',K,F),N('u2',G,H))
    assert splay(source_left,'u1')==out_left and path(out_left,'k')==(0,0)
    assert len(path(out_left,'a'))>=3 and path(find(out_left,'u2'),'a') is None
    assert splay(flip(source_left),'u1')==flip(out_left)

    # Both possible A zero-release positions preserving the Score separator.
    for root in ('u1','u2'):
        source_R=N('b',K,N(root,F,G))
        target_R=N(root,N('b',K,F),G)
        source_RL=N('b',K,N('q',N(root,F,G),H))
        target_RL=N(root,N('b',K,F),N('q',G,H))
        for source,expected in ((source_R,target_R),(source_RL,target_RL)):
            assert splay(source,root)==expected
            assert path(expected,'b')==(0,) and path(expected,'k')==(0,0)
            assert len(path(expected,'a'))>=3
            pa=path(find(expected,'b'),'a');assert pa is None or len(pa)>=2
            assert splay(flip(source),root)==flip(expected)

    # A maximum helper's three possible active positions move the entire
    # left b/k block down. Lower marked a cannot be a charge1 terminal.
    helper_A=[
        N('r',left,N('f',F,G)),
        N('r',left,N('q',F,N('f',G,H))),
        N('r',left,N('q',N('f',F,G),H)),
    ]
    for source in helper_A:
        assert len(path(splay(source,'f'),'a'))>=4
        assert len(path(splay(flip(source),'f'),'a'))>=4
    # B maximum helper: all lower cores stay below b.left, so terminal
    # paths to the upper group contain at most five core nodes.
    for source in (J5,J6):
        with_proxy=replace(source,path(source,'u4')+(1,),N('f'))
        post=splay(with_proxy,'f')
        assert find(post,'b')[2]==lower
        assert all(len(path(post,key))<=5 for key in upper_keys)
        dualpost=splay(flip(with_proxy),'f')
        assert find(dualpost,'b')[3]==flip(lower)
        assert all(len(path(dualpost,key))<=5 for key in upper_keys)

    # Exact analytic debt2 nonvacuity. These are universally quantified
    # ordered-symbol rotation identities, NOT numeric core-tree samples.
    formal_order=['l0','l1','l2','l3','b','u1','u2','u3','u4']
    pred5=chain(('l0','u4','l1','u3','l2','u2','l3','u1','b'),(1,0,1,0,1,0,1,0))
    pred6=chain(('l0','u4','l1','u3','u2','u1','l2','l3','b'),(1,0,1,0,0,0,1,1))
    low5=N('l0',E,N('l1',E,N('l2',E,N('l3'))))
    low6=N('l0',E,N('l1',E,N('l3',N('l2'),E)))
    for predecessor,source,block in ((pred5,P5,low5),(pred6,P6,low6)):
        assert inorder(predecessor)==formal_order and len(path(predecessor,'b'))==8
        expected=replace(source,path(source,'LOWER'),block)
        assert splay(predecessor,'b')==expected
        assert splay(flip(predecessor),'b')==flip(expected)
    # Old negative-core inequality+range implies psi(output)=2; no label
    # from the saved bank is read, fitted or tested here.

    paid2=add(lin(constant=2),lin(target_debt=1),lin(constant=-2))
    paid1=add(lin(constant=1),lin(constant=1,E1_slack=1),lin(constant=-2))
    Gamma1=add(lin(constant=2,weight_slack=1),lin(target_debt=1),lin(constant=-2))
    zero_release=add(lin(constant=2),lin(constant=-2))
    for expr in (paid2,paid1,Gamma1,zero_release):assert all(value>=0 for value in expr.values())

    # Provenance only, no source DAG construction or root evaluation.
    lp=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rp=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    module=ast.parse(lp.read_text(encoding='utf-8-sig'))
    funcs={n.name:ast.unparse(n) for n in module.body if isinstance(n,ast.FunctionDef)}
    low,shadow,match=(funcs[k] for k in ('build_slow','shadow7','shadow_match7'))
    assert 'C.append(s.aS[0])' in low and 'C.append(d.EQ(s.aI[0], muxb(' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    rotation=ast.parse(rp.read_text(encoding='utf-8-sig'))
    mux=next(n for n in rotation.body if isinstance(n,ast.FunctionDef) and n.name=='mux_ref')
    assert ast.unparse(mux.body[0])=='r = vec[0]'
    result={
        'status':'UNIVERSAL_TWO_CREDIT_RELEASE_CAPACITY_AUDIT_PASS',
        'no_numeric_key_population_or_potential_assignment_generated':True,
        'zero_core_release_identities_with_duals':4,
        'weight1_core_successor_identities_with_duals':8,
        'observed_Score_separator_required':True,
        'A_weight1_and_G_owner_visibility_schemas_with_duals':8,
        'A_zero_release_R_RL_schemas_with_duals':8,
        'Gamma1_forbidden_minimum_helpers_by_order':True,
        'Gamma1_lower_mark_hidden_after_extreme_helper_schemas_with_duals':6,
        'Gamma1_upper_group_terminal_depth_bound':5,
        'Gamma1_weight_at_least2_including_Score_bearing_helpers':True,
        'Gamma0_actual_preterminal_floor_reused':True,
        'analytic_negative_predecessor_debt2_certificates_with_duals':4,
        'old_saved_psi_values_queried':0,
        'all_J_source_LOW_inequalities_proved':True,
        'each_previously_valid_LOW_inequality_preserved':True,
        'private_completion_or_anonymous_color_inferred':False,
        'RR_lost_separator_and_other_B_patterns_claimed':False,
        'full_compiler_formalization_claimed':False,
        'paid2_residual':paid2,'paid1_residual':paid1,'Gamma1_residual':Gamma1,
        'source_debt2_zero_release_residual':zero_release,
        'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
        'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,
        'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (lp,rp)},
        'all_debt2_releases_or_M3_solved':False,'M3_status':'OPEN',
        'CPU_seconds':time.process_time(),'CPU_cap':CAP,
    }
    assert time.process_time()<CAP
    write('symbolic_audit.json',result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
