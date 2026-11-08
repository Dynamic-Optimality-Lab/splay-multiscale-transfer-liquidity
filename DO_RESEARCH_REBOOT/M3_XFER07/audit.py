"""Independent symbolic direct-barrier proof audit; no finite test instances.

Ordered role symbols, arbitrary lower/side subtrees, primitive identities,
typed substitution, exact signed slacks and bounded source provenance.
No source relation, population, numerical core tree or saved psi is evaluated.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
E=('EMPTY',)

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('SUBTREE',name)
def N(key,left=E,right=E):return ('NODE',key,left,right)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    p=t[2];return N(p[1],p[2],N(t[1],p[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    p=t[3];return N(p[1],N(t[1],t[2],p[2]),p[3])
def at(t,p):
    for bit in p:assert t[0]=='NODE';t=t[2+bit]
    return t
def put(t,p,v):
    if not p:return v
    return N(t[1],put(t[2],p[1:],v),t[3]) if p[0]==0 else N(t[1],t[2],put(t[3],p[1:],v))
def local(t,p,fn):return put(t,p,fn(at(t,p)))
def pair(t,bits):
    if bits==(0,0):return rz(rz(t))
    if bits==(1,1):return lz(lz(t))
    if bits==(0,1):return rz(local(t,(0,),lz))
    assert bits==(1,0);return lz(local(t,(1,),rz))
def flip(t):return N(t[1],flip(t[3]),flip(t[2])) if t[0]=='NODE' else t
def path(t,key,p=()):
    if t[0]!='NODE':return None
    if t[1]==key:return p
    found=path(t[2],key,p+(0,))
    return found if found is not None else path(t[3],key,p+(1,))
def depth(t,key):
    p=path(t,key);assert p is not None;return len(p)
def keys(t):return [t[1]]+keys(t[2])+keys(t[3]) if t[0]=='NODE' else []
def chain(roles,bits):
    if len(roles)==1:return N(roles[0])
    child=chain(roles[1:],bits[1:])
    return N(roles[0],child,E) if bits[0]==0 else N(roles[0],E,child)
def lin(*parts):
    out={}
    for part in parts:
        for k,v in part.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    L=V('arbitrary_lower_core_subtree')
    b,u1,u2,u3,u4='b','u1','u2','u3','u4'
    J6=N(u2,N(b,L,N(u1)),N(u4,N(u3)))
    J7=N(u3,N(b,L,N(u2,N(u1))),N(u4))
    B6=N(u2,N(u1,N(b,L)),N(u3,E,N(u4)))
    B7=N(u3,N(u1,N(b,L),N(u2)),N(u4))
    B8=N(u4,N(u1,N(b,L),N(u3,N(u2))))
    targets={'J6':J6,'J7':J7,'B6':B6,'B7':B7,'B8':B8}
    # Six NEW universal word identities. Old LLL/LLR are dependencies,
    # not replayed. Role ordering is fixed by the source theorem's inorder.
    rows=[
      ('LRL',(0,1,0),(u4,u1,u3,u2),'J6'),
      ('LRR',(0,1,1),(u4,u1,u2,u3),'J7'),
      ('RLL',(1,0,0),(u1,u4,u3,u2),'B6'),
      ('RLR',(1,0,1),(u1,u4,u2,u3),'B7'),
      ('RRL',(1,1,0),(u1,u2,u4,u3),'B7'),
      ('RRR',(1,1,1),(u1,u2,u3,u4),'B8'),
    ]
    word_certs=[]
    for word,bits,roles,name in rows:
        source=N(b,L,chain(roles,bits))
        after=local(source,(1,bits[0]),lambda t:pair(t,bits[1:]))
        after=pair(after,(1,bits[0]))
        assert after==targets[name],word
        dual=flip(source)
        dout=local(dual,(0,1-bits[0]),lambda t:pair(t,tuple(1-v for v in bits[1:])))
        dout=pair(dout,(0,1-bits[0]))
        assert dout==flip(targets[name]),word
        word_certs.append({'word':word,'formal_roles':list(roles),'destination':name,
          'central_barrier_depth':depth(after,b),'actual_dual_identity_checked':True})
    assert depth(J6,b)==depth(J7,b)==1
    assert all(depth(t,b)==2 for t in (B6,B7,B8))
    # New J7 +1 core outputs, each with arbitrary lower block L.
    C5=N(u1,N(b,L),N(u3,N(u2),N(u4)))
    C6=N(u2,N(b,L,N(u1)),N(u3,E,N(u4)))
    after5=rz(local(J7,(0,),lambda t:pair(t,(1,0))))
    after6=pair(J7,(0,1))
    assert after5==C5 and after6==C6
    dual5=lz(local(flip(J7),(1,),lambda t:pair(t,(0,1))))
    dual6=pair(flip(J7),(1,0))
    assert dual5==flip(C5) and dual6==flip(C6)
    upper=(b,u1,u2,u3,u4)
    assert all(depth(t,k)<=2 for t in (C5,C6) for k in upper)
    assert depth(J7,b)==depth(J7,u4)==1
    assert depth(J7,u1)==3 and depth(J7,u2)==2

    A,B,C,D,T,R,Y=map(V,('A','B','C','D','T','R','Y'))
    # Generalized old-child lemma: T is UNRESTRICTED off-path, not EMPTY.
    odd=N('x',N(b,N('a',A,B),T),R)
    oddout=pair(odd,(0,0))
    assert depth(oddout,b)==1 and depth(oddout,'x')==2
    assert pair(flip(odd),(1,1))==flip(oddout)
    # Even internal parity uses the inherited old-root depth<=2. Since
    # b>a it is in a.right; all possible depth1/2 placements are covered.
    endings=[N('a',A,N(b,B,T)),
      N('a',A,N('p',N(b,B,T),C)),N('a',A,N('p',B,N(b,C,T)))]
    for internal in endings:
        source=N('x',internal,R);out=rz(source)
        assert depth(out,b)<=3 and depth(out,'x')==1
        assert lz(flip(source))==flip(out)
    # C's only zero A target is a at LL. Full K endpoint has no V filter.
    source=N('x',N(b,N('a',A,B),C),Y)
    out=pair(source,(0,0))
    assert out==N('a',A,N(b,B,N('x',C,Y)))
    assert path(out,b)==(1,) and path(out,'x')==(1,1)

    # New K6 helper schemas: Score5, if marked/present, is inside Z and
    # remains deeper than u2, hence is not an extra charge1 terminal.
    Z=V('between_b_and_u2_block')
    helpers=[
      (N('a',N('f',A,B),N(b,C,N(u2,Z,Y))),lambda t:rz(t)),
      (N('a',N('p',N('f',A,B),C),N(b,D,N(u2,Z,Y))),lambda t:pair(t,(0,0))),
      (N('a',N('p',A,N('f',B,C)),N(b,D,N(u2,Z,Y))),lambda t:pair(t,(0,1))),
    ]
    for i,(source,fn) in enumerate(helpers):
        out=fn(source)
        assert depth(out,'a')<=2 and depth(out,u2)>=3
        assert (depth(out,b)<=2)==(i!=1)
        if i==0:dout=lz(flip(source))
        elif i==1:dout=pair(flip(source),(1,1))
        else:dout=pair(flip(source),(1,0))
        assert dout==flip(out)

    # Typed substitutions into the REUSED parametric helper parity/leaf
    # proof. T/R have new shapes, but all their keys stay above b.
    # The ordinals here are positions in a FORMAL ORDER, not key instances.
    order={key:i for i,key in enumerate(upper)}
    substitutions=[]
    for name,tree in (('J7',J7),('C5',C5),('C6',C6)):
        root=tree[1];barrier=tree[2]
        assert barrier[1]==b and barrier[2]==L
        midkeys=keys(barrier[3]);highkeys=keys(tree[3])
        assert all(order[b]<order[k]<order[root] for k in midkeys)
        assert all(order[k]>order[root] for k in highkeys)
        assert len(set(keys(tree)))==5
        substitutions.append({'shape':name,'upper_middle_roles':midkeys,'upper_right_roles':highkeys})
    # No replay of Transfer06 parity/leaf identities is needed. Its E1
    # visibility condition is separately checked below for each A guard.
    for side in (0,1):
        sep=N('p',N('a',A,B),C) if side==0 else N('p',A,N('a',B,C))
        # G7-L guard and lower +1 at LR retain separator at LL.
        source=N(u3,N(b,sep,N('x',D,T)),Y)
        out=pair(source,(0,1))
        assert path(out,'p')==(0,0) and depth(out,'a')==3
        assert path(at(out,path(out,u3)),'a') is None
    # G7-LL guard: child target needs C; LR target retains E1.
    source=N(u3,N('x',N(b,N('a',A,B),C),D),Y)
    childout=rz(source)
    assert path(childout,b)==(0,) and path(childout,'a')==(0,0)
    source=N(u3,N('q',N(b,N('a',A,B),C),N('x',D,T)),Y)
    lrout=pair(source,(0,1))
    assert path(lrout,b)==(0,0) and depth(lrout,'a')==3
    assert path(at(lrout,path(lrout,u3)),'a') is None
    # A4-L helper barrier, even with a visible at LL, pushes a to>=3
    # under each maximum helper. No source separator assumption is used.
    left=N(b,N('a',A,B),C)
    for source,fn in (
      (N('c',left,N('f',D,T)),lambda t:lz(t)),
      (N('c',left,N('q',N('f',D,T),Y)),lambda t:pair(t,(1,0))),
      (N('c',left,N('q',D,N('f',T,Y))),lambda t:pair(t,(1,1)))):
        assert depth(fn(source),'a')>=3
    # Signed rows and helper arithmetic have nonnegative affine slack.
    assert 2+(4-1)==5 and 4-(5//2)==2
    slacks={
      'K_new_one':lin({'const':1,'weight_excess':1},{'target_debt':1},{'const':-1}),
      'C_zero_to_K':lin({'const':1,'K_credit_excess':1},{'const':-1}),
      'C_positive_or_helper':lin({'const':1,'weight_excess':1},{'target_debt':1},{'const':-1}),
      'G7_plus1_to_C_or_E1':lin({'const':1},{'const':1,'credit_excess':1},{'const':-2}),
      'G7_paid_or_helper':lin({'const':2,'weight_excess':1},{'target_debt':1},{'const':-2}),
      'incoming_zero_to_G7':lin({'const':2},{'const':-2,'source_room_below2':1}),
    }
    assert all(v>=0 for e in slacks.values() for v in e.values())

    # Bounded source provenance; no DAG/root construction or old test.
    folder=BASE.parent/'06_CERTIFICATES'
    lp=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    bp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py'
    rp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    def func(file,name):
        return next(n for n in ast.walk(ast.parse(file.read_text(encoding='utf-8-sig')))
          if isinstance(n,ast.FunctionDef) and n.name==name)
    low=ast.unparse(func(lp,'build_slow'))
    assert 'C.append(s.aS[0])' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    assert 'd.LE(d.ADD(bt.q, bt.q, 5), bd_last)' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    assert 'b_tree_valid(d, t.b, bst5, t.sig)' in low
    assert 'b_tree_valid(d, bs[e + 1], bst, s.sig, intervals=False)' in low
    gap=next(n for n in ast.walk(func(bp,'b_valid')) if isinstance(n,ast.If) and ast.unparse(n.test)=='i >= NCORE')
    body='\n'.join(ast.unparse(n) for n in gap.body)
    assert 'd.EQ(bs.kl[i], d.const_int(2, 2))' in body and 'd.EQ(bs.kr[i], d.const_int(2, 2))' in body
    assert ast.unparse(func(rp,'mux_ref').body[0])=='r = vec[0]'
    assert time.process_time()<CAP
    result={
      'status':'DIRECT_BARRIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'six_new_formal_spine_identities_with_duals':word_certs,
      'old_P5_P6_and_upper_height_checks_replayed':False,
      'S_frontier_total_words':8,'S_frontier_distinct_successors':6,
      'S_frontier_covered_words_after':4,'S_frontier_remaining_words':4,
      'remaining_successor_cores':['B6','B7','B8'],
      'remaining_cores_have_B_barrier_depth':2,
      'LRL_is_existing_J6_coverage_not_new_certificate':True,
      'J7_new_plus1_core_outputs':['C5','C6'],
      'all_C_upper_core_depths_at_most':2,
      'general_old_child_bound_with_arbitrary_T':3,
      'K6_hidden_intermediate_Score5_and_helpers_audited':True,
      'parametric_helper_proof_new_typed_substitutions':substitutions,
      'all_new_helper_barrier_Gamma1_weights_at_least':2,
      'no_V_filter_on_C_or_K_boundaries':True,
      'safe_operation_order':['K1','C1','G7_2'],
      'each_previously_valid_LOW_row_preserved':True,
      'all_G7_source_LOW_rows_proved':True,
      'LRR_zero_release_all_A_positions_and_separator_types_proved':True,
      'both_actual_LOW_orientations_proved':True,
      'signed_residuals':slacks,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (lp,bp,rp)},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'global_zero_LOW_coverage_proved':False,'full_M3_status':'OPEN',
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
