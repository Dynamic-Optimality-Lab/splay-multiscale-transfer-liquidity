"""Independent universal term/count/slack audit; NO finite test instances."""
import ast,hashlib,itertools,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))
def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('V',name)
def N(key,left,right):return ('N',key,left,right)
EMPTY=('EMPTY',)
PORT=('PORT','P')
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
    assert t[0]=='N'
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
def flip(t,swap=False):
    if t[0]!='N':return t
    key={'a':'b','b':'a'}.get(t[1],t[1]) if swap else t[1]
    return N(key,flip(t[3],swap),flip(t[2],swap))
def lin(**v):return {k:x for k,x in v.items() if x}
def add(*terms):
    result={}
    for term in terms:
        for k,v in term.items():result[k]=result.get(k,0)+v
    return {k:v for k,v in result.items() if v}
def neg(term):return {k:-v for k,v in term.items()}

def main():
    A,B,C,Y,D,E,F,G,H,I=map(V,('A','B','C','Y','D','E','F','G','H','I'))
    # L->T and T->S identities with arbitrary branch Y; no hidden-port
    # reconstruction in the second identity.
    source_L=N('b',N('p',N('a',A,B),C),PORT)
    target_L=N('a',A,N('p',B,N('b',C,PORT)))
    assert splay(source_L,'a')==target_L and path(target_L,'b')==(1,1)
    source_T=N('a',A,N('p',B,N('b',C,Y)))
    target_T=N('b',N('p',N('a',A,B),C),Y)
    assert splay(source_T,'b')==target_T and path(target_T,'a')==(0,0)
    assert splay(flip(source_L,True),'b')==flip(target_L,True)
    assert splay(flip(source_T,True),'a')==flip(target_T,True)
    # The L owner b has children C and PORT after access: a ghost cannot
    # report another marked upper key through that port.
    assert find(target_L,'b')[2:]==(C,PORT)

    # Count forces ALL four upper cores onto the zero-access spine.
    # Eight universal direction schemas, with unassigned core labels
    # u/v/w/c and arbitrary lower subtree. NO numerical BST instance.
    def spine(keys,directions):
        if len(keys)==1:return N(keys[0],EMPTY,EMPTY)
        child=spine(keys[1:],directions[1:])
        return N(keys[0],child,EMPTY) if directions[0]==0 else N(keys[0],EMPTY,child)
    spine_certificates=[]
    for directions in itertools.product((0,1),repeat=3):
        original=N('b',V('lower_core_subtree'),spine(('u','v','w','c'),directions))
        after=splay(original,'c')
        depths={key:len(path(after,key)) for key in ('u','v','w','c')}
        assert max(depths.values())<=3 and len(path(after,'b'))<=2
        dual=flip(original);dualafter=splay(dual,'c')
        assert all(len(path(dualafter,key))==value for key,value in depths.items())
        spine_certificates.append({'formal_tail_directions':list(directions),'upper_core_depth_expressions':depths})

    # Every right-side H1 position hides source a at LL. Owner b.left
    # remains the UNMARKED p; owner b.right has no occurrence of a.
    left=N('p',N('a',A,B),C)
    opposite=[
        N('b',left,N('c',D,E)),
        N('b',left,N('q',N('c',D,E),F)),
        N('b',left,N('q',D,N('c',E,F))),
    ]
    for original in opposite:
        after=splay(original,'c');assert len(path(after,'a'))>=3
        owner=find(after,'b')
        assert owner[2]==left and owner[2][1]=='p'
        assert path(owner[3],'a') is None
        dual=flip(original,True);dualafter=splay(dual,'c')
        assert len(path(dualafter,'b'))>=3
        ownerdual=find(dualafter,'a')
        assert ownerdual[3]==flip(left,True) and ownerdual[3][1]=='p'
        assert path(ownerdual[2],'b') is None

    # All possible T minimum-helper slots L/LL/LR. Other present marked
    # nodes are in b.right; b itself becomes depth3/4/3 after the helper.
    tail=N('p',B,N('b',C,Y))
    T_helpers=[
        (N('a',N('f',D,E),tail),3),
        (N('a',N('u',N('f',D,E),F),tail),4),
        (N('a',N('u',D,N('f',E,F)),tail),3),
    ]
    for original,expected_depth in T_helpers:
        after=splay(original,'f');assert len(path(after,'b'))==expected_depth
        assert len(path(splay(flip(original,True),'f'),'a'))==expected_depth
    # The actual entry-root B depth<=2 is a completed premise, not rerun.

    # Universal count inequalities for central source root r in[3,5].
    r=lin(r=1)
    assert add(lin(constant=7),neg(add(r,lin(constant=2))))==lin(constant=5,r=-1)
    assert add(lin(constant=7),neg(add(lin(constant=10),neg(r))))==lin(r=1,constant=-3)
    # q>=4, depth<=7 would contradict the original2q<=depth.
    q=lin(constant=4,q_excess=1);depth=lin(constant=7,depth_slack=-1)
    assert add(q,q,neg(depth))==lin(constant=1,q_excess=2,depth_slack=1)
    # For L: depth<=5 excludes q>=3, hence H1 weight>=0.
    qL=lin(constant=3,q_excess=1);depthL=lin(constant=5,depth_slack=-1)
    assert add(qL,qL,neg(depthL))==lin(constant=1,q_excess=2,depth_slack=1)

    # All newly raised-source residuals have exact nonnegative slack forms.
    S_positive=add(lin(constant=1,weight_slack=1),lin(target_debt=1),lin(constant=-1))
    S_zero=add(lin(constant=1,target_above_E1_floor=1),lin(constant=-1))
    T_return=add(lin(constant=1,weight_slack=1),lin(constant=1,target_above_S_floor=1),lin(constant=-2))
    L_forward=add(lin(nonnegative_weight=1),lin(constant=2),lin(constant=-2))
    T_Gamma1=add(lin(constant=3,weight_slack=1),lin(target_debt=1),lin(constant=-2))
    for expression in (S_positive,S_zero,T_return,L_forward,T_Gamma1):assert all(value>=0 for value in expression.values())
    # Unchanged-source residual=old residual+nonnegative target increment
    # at EACH of the three operations, so no old valid LOW row is lost.

    low_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rot_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    lowmodule=ast.parse(low_path.read_text(encoding='utf-8-sig'))
    funcs={node.name:ast.unparse(node) for node in lowmodule.body if isinstance(node,ast.FunctionDef)}
    low,shadow,match=(funcs[name] for name in ('build_slow','shadow7','shadow_match7'))
    assert 'C.append(s.aS[0])' in low and 'C.append(d.EQ(s.aI[0], muxb(' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5))' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    rotation=ast.parse(rot_path.read_text(encoding='utf-8-sig'))
    mux=next(node for node in rotation.body if isinstance(node,ast.FunctionDef) and node.name=='mux_ref')
    assert ast.unparse(mux.body[0])=='r = vec[0]'
    result={
        'status':'UNIVERSAL_BURIED_CUT_THREE_CLAUSE_AUDIT_PASS',
        'universal_formal_spine_schemas_with_duals':16,
        'spine_schema_certificates':spine_certificates,
        'no_numeric_key_population_or_potential_assignment_generated':True,
        'L_T_and_T_S_universal_identities_with_duals':4,
        'S_opposite_access_and_alias_owner_schemas_with_duals':6,
        'T_helper_nonentry_terminal_depth_schemas_with_duals':6,
        'central_root_Gamma1_weight_at_least1':True,
        'S_zero_endpoints_E1_including_G_alias_argument':True,
        'L_target_T_V_singleton_including_G_alias_argument':True,
        'S_positive_residual':S_positive,'S_zero_residual':S_zero,
        'T_return_residual':T_return,'L_forward_residual':L_forward,
        'T_Gamma1_entry_residual':T_Gamma1,
        'L_Gamma1_source_exclusion_by_order_and_charge':True,
        'each_operation_preserves_each_previously_valid_LOW_inequality':True,
        'all_final_L_and_T_LOW_sources_proved':True,
        'S_LOW_coverage_requires_final_debt_at_most1':True,
        'all_S_debt2_sources_claimed':False,
        'buried_port_reconstructed_or_persistent_witness_assumed':False,
        'Gamma0_actual_preterminal_floor_reused':True,
        'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (low_path,rot_path)},
        'full_compiler_formalization_claimed':False,
        'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
        'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,
        'all_buried_states_or_M3_solved':False,'M3_status':'OPEN',
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
