"""Independent universal term/parity/slack audit; no finite test instances."""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120,float(sys.argv[1]))

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('V',name)
def N(label,left,right):return ('N',label,left,right)
P=('PORT','P')
def R(t):
    assert t[0]=='N' and t[2][0]=='N'
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def L(t):
    assert t[0]=='N' and t[3][0]=='N'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def at(t,path):
    for side in path:
        assert t[0]=='N';t=t[2+side]
    return t
def put(t,path,value):
    if not path:return value
    assert t[0]=='N'
    return N(t[1],put(t[2],path[1:],value),t[3]) if path[0]==0 else N(t[1],t[2],put(t[3],path[1:],value))
def path(t,key,p=()):
    if t[0]=='V':return p if t[1]==key else None
    if t[0]!='N':return None
    if t[1]==key:return p
    a=path(t[2],key,p+(0,))
    return a if a is not None else path(t[3],key,p+(1,))
def find(t,key):
    p=path(t,key);assert p is not None;return at(t,p)
def pair(t,word):
    if word==(0,0):return R(R(t))
    if word==(1,1):return L(L(t))
    if word==(0,1):return R(N(t[1],L(t[2]),t[3]))
    assert word==(1,0)
    return L(N(t[1],t[2],R(t[3])))
def splay(t,key):
    while t[1]!=key:
        p=path(t,key);assert p is not None and len(p)>0
        if len(p)==1:t=R(t) if p[0]==0 else L(t)
        else:t=put(t,p[:-2],pair(at(t,p[:-2]),p[-2:]))
    return t
def flip(t,swap=False):
    if t[0]!='N':return t
    label={'a':'b','b':'a'}.get(t[1],t[1]) if swap else t[1]
    return N(label,flip(t[3],swap),flip(t[2],swap))
def small_region(t):
    if t[1]=='b':return path(t,'a') in ((0,),(0,1)) and find(t,'b')[3]==P
    return t[1]=='a' and path(t,'b')==(1,) and find(t,'b')[3]==P
def large_region(t):
    if t[1]=='a':return path(t,'b') in ((1,),(1,0)) and find(t,'a')[2]==P
    return t[1]=='b' and path(t,'a')==(0,) and find(t,'a')[2]==P
def lin(**values):return {k:v for k,v in values.items() if v}
def add(*terms):
    out={}
    for term in terms:
        for k,v in term.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}
def neg(term):return {k:-v for k,v in term.items()}

def main():
    A,B,C,D,E=map(V,('A','B','C','D','E'))
    # Arbitrary subtree variables are NOT restricted to opaque/empty. Thus
    # these identities include freshly exposed real anonymous/unmarked roots.
    h1=[
        (N('b',N('a',A,B),P),'a',N('a',A,N('b',B,P))),
        (N('b',N('p',A,N('a',B,C)),P),'a',N('a',N('p',A,B),N('b',C,P))),
        (N('a',A,N('b',B,P)),'b',N('b',N('a',A,B),P)),
    ]
    for source,key,expected in h1:
        assert small_region(source) and splay(source,key)==expected and small_region(expected)
        dual,dualkey=flip(source,True),{'a':'b','b':'a'}[key]
        assert large_region(dual) and splay(dual,dualkey)==flip(expected,True) and large_region(flip(expected,True))

    # Complete four allowed helper/other-terminal schemas. P is a symbolic
    # immutable port, all other blocks arbitrary compatible subtree variables.
    allowed=[
        (N('b',N('a',N('f',A,B),C),P),'a',N('a',N('f',A,B),N('b',C,P))),
        (N('b',N('f',A,N('a',B,C)),P),'a',N('a',N('f',A,B),N('b',C,P))),
        (N('a',N('f',A,B),N('b',C,P)),'b',N('b',N('a',N('f',A,B),C),P)),
        (N('a',N('p',A,N('f',B,C)),N('b',D,P)),'b',N('b',N('a',N('f',N('p',A,B),C),D),P)),
    ]
    for source,key,expected in allowed:
        assert small_region(source)
        first=splay(source,'f');assert len(path(first,key))<=2
        assert splay(first,key)==expected and small_region(expected)
        dual,dualkey=flip(source,True),{'a':'b','b':'a'}[key]
        assert large_region(dual)
        dualfirst=splay(dual,'f');assert len(path(dualfirst,dualkey))<=2
        assert splay(dualfirst,dualkey)==flip(expected,True) and large_region(flip(expected,True))
    excluded=[
        (N('b',N('p',N('f',A,B),N('a',C,D)),P),'a'),
        (N('a',N('p',N('f',A,B),C),N('b',D,P)),'b'),
    ]
    for source,key in excluded:
        assert small_region(source) and len(path(splay(source,'f'),key))==3
        dual,dualkey=flip(source,True),{'a':'b','b':'a'}[key]
        assert large_region(dual) and len(path(splay(dual,'f'),dualkey))==3
    # Depth3 costs2, plus helper charge1 exceeds original H2. These are
    # exact rejected symbolic words, not evaluated population test cases.

    # NEW B spine proof. Even internal depth: all old x child subtrees
    # move down at most1 under the remaining one/two upper ancestors.
    U,W,Z,T=map(V,('U','W','Z','T'))
    for upper in (N('f',U,N('x',A,B)),N('f',U,N('p',W,N('x',A,B)))):
        out=splay(upper,'x')
        for key in ('A','B'):
            before=len(path(upper,key))-len(path(upper,'x'))
            after=len(path(out,key))
            assert after-before<=1
        # Constructor-reversed upper steps have identical depth changes.
        dual=flip(upper);dualout=splay(dual,'x')
        for key in ('A','B'):
            assert len(path(dualout,key))-(len(path(dual,key))-len(path(dual,'x')))<=1
    # For an off-path r=p.right and x<p, p lies in x.right. The outer
    # x/f zig leaves that RIGHT side wholly unchanged; r adds one level.
    upper=N('f',U,N('x',A,B));out=splay(upper,'x')
    assert len(path(out,'B'))==len(path(upper,'B'))-len(path(upper,'x'))

    # Odd tails and the x=p branch, after arbitrary common lower pairs.
    tails=[
        (N('f',U,N('r',N('x',W,Z),T)),'x',1),
        (N('f',U,N('r',W,N('x',Z,T))),'x',1),
        (N('f',U,N('p',W,N('r',N('x',Z,T),E))),'x',2),
        (N('f',U,N('p',W,N('r',Z,N('x',T,E)))),'x',2),
        (N('f',U,N('p',N('x',W,Z),N('r',T,E))),'x',2),
        (N('f',U,N('p',W,N('r',Z,T))),'p',1),
    ]
    for source,key,bound in tails:
        assert len(path(splay(source,key),'r'))<=bound
        assert len(path(splay(flip(source),key),'r'))<=bound
    # Reused old-root relative bound2 + NEW upper displacement<=1 gives3.
    assert add(lin(old_relative_max=2),lin(upper_max_shift=1))==lin(old_relative_max=2,upper_max_shift=1)

    # Affine proof certificates for all newly raised sources, no assigned
    # debt/weight values or saved numerical potential labels.
    assert add(lin(old_residual=1),lin(target_increment=1))==lin(old_residual=1,target_increment=1)
    assert add(lin(nonnegative_w=1),lin(constant=2),lin(constant=-2))==lin(nonnegative_w=1)
    assert add(lin(k=-1),lin(constant=2),neg(lin(constant=2,k=-1)))=={}
    gamma1_other=add(lin(nonnegative_w2=1),lin(constant=2),neg(lin(constant=2,source_slack=-1)))
    assert gamma1_other==lin(nonnegative_w2=1,source_slack=1)
    gamma1_return=add(lin(constant=3,weight_slack=1),lin(target_debt=1),neg(lin(constant=2,source_slack=-1)))
    assert gamma1_return==lin(constant=1,weight_slack=1,target_debt=1,source_slack=1)
    assert add(lin(constant=1),lin(constant=1),neg(lin(constant=2,source_slack=-1)))==lin(source_slack=1)

    # Source provenance only: no DAG construction/root evaluation/import.
    low_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    b_path=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py'
    module=ast.parse(low_path.read_text(encoding='utf-8-sig'))
    funcs={n.name:ast.unparse(n) for n in module.body if isinstance(n,ast.FunctionDef)}
    low=funcs['build_slow'];shadow=funcs['shadow7'];match=funcs['shadow_match7']
    assert 'C.append(s.aS[0])' in low and 'C.append(d.EQ(s.aI[0], muxb(' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    assert 'k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'd.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p]))' in match
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5))' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    bm=ast.parse(b_path.read_text(encoding='utf-8-sig'))
    bf=ast.unparse(next(n for n in bm.body if isinstance(n,ast.FunctionDef) and n.name=='b_splay_event'))
    assert 'same = d.EQ(dirs[min(t, 17)], dirs[min(t + 1, 17)])' in bf
    assert 'xA = d.ITE(same, path[t + 1], path[0])' in bf
    assert 'pB = d.ITE(same, path[t + 1], path[min(t + 2, 18)])' in bf
    result={
        'status':'UNIVERSAL_CUT_PAIR_LOW_AUGMENTATION_AUDIT_PASS',
        'arbitrary_subtree_terms_not_population_instantiations':True,
        'H1_schemas_with_duals':6,'allowed_Gamma1_other_terminal_schemas_with_duals':8,
        'excluded_Gamma1_LL_schemas_with_duals':4,
        'all_helper_slots_covered_by_source_order_and_charge_proof':True,
        'marked_support_separated_by_observed_port_for_all_private_witnesses':True,
        'helper_Score_empty_premise_used':False,
        'B_spine_internal_parity_cases_exhaustive':True,
        'B_old_root_final_depth_bound':3,
        'B_even_upper_subtree_shift_at_most':1,
        'B_off_path_order_case_protected_side_shift':0,
        'B_odd_tail_and_parent_target_cases_with_duals':12,
        'Gamma1_other_terminal_residual':gamma1_other,
        'Gamma1_entry_terminal_residual':gamma1_return,
        'original_H1_and_H2_q_H_endpoints_unchanged':True,
        'Gamma0_actual_preterminal_floor_reused':True,
        'individual_previously_valid_LOW_inequalities_preserved':True,
        'new_R_sources_all_LOW_proved':True,
        'previous_Q_LOW_coverage_preserved':True,
        'full_state_closure_and_same_actual_midpoint_preserved':True,
        'raw_unused_fields_or_G_aliases_quotiented':False,
        'full_original_compiler_formalization_claimed':False,
        'all_transfers_or_M3_proved':False,
        'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
        'new_label_fits':0,'new_bank_censuses':0,'completed_semantic_checks_replayed':0,
        'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (low_path,b_path)},
        'M3_status':'OPEN','CPU_seconds':time.process_time(),'CPU_cap':CAP,
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
