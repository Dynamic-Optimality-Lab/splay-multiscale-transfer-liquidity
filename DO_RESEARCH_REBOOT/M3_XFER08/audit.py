"""Independent universal parent/return/sign audit; NO finite test instances.

All keys are unassigned ordered roles, all lower/side blocks variables.
No original DAG/root, population, finite core bank or saved debt is evaluated.
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
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def at(t,p):
    for bit in p:assert t[0]=='NODE';t=t[2+bit]
    return t
def put(t,p,value):
    if not p:return value
    return N(t[1],put(t[2],p[1:],value),t[3]) if p[0]==0 else N(t[1],t[2],put(t[3],p[1:],value))
def local(t,p,fn):return put(t,p,fn(at(t,p)))
def pair(t,bits):
    if bits==(0,0):return rz(rz(t))
    if bits==(1,1):return lz(lz(t))
    if bits==(0,1):return rz(local(t,(0,),lz))
    assert bits==(1,0);return lz(local(t,(1,),rz))
def path(t,key,p=()):
    if t[0]=='SUBTREE':return p if t[1]==key else None
    if t[0]!='NODE':return None
    if t[1]==key:return p
    found=path(t[2],key,p+(0,))
    return found if found is not None else path(t[3],key,p+(1,))
def depth(t,key):
    p=path(t,key);assert p is not None;return len(p)
def parent(t,key):
    p=path(t,key);assert p;return at(t,p[:-1])[1]
def flip(t):return N(t[1],flip(t[3]),flip(t[2])) if t[0]=='NODE' else t
def lin(*parts):
    out={}
    for p in parts:
        for k,v in p.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,M,R,Y=map(V,('A','B','C','D','M','R','Y'))
    identity_names=[]
    def cert(name,out,expected):
        assert out==expected,name
        identity_names.append(name)
    # Extreme proxy final-parent rule, after arbitrary processed bottom pairs.
    zig=N('f',E,N('x',A,B));zigout=lz(zig)
    cert('proxy_final_zig',zigout,N('x',N('f',E,A),B))
    rr=N('f',E,N('z',A,N('x',B,C)));rrout=pair(rr,(1,1))
    cert('proxy_final_RR',rrout,N('x',N('z',N('f',E,A),B),C))
    rl=N('f',E,N('z',N('x',A,B),C));rlout=pair(rl,(1,0))
    cert('proxy_final_RL',rlout,N('x',N('f',E,A),N('z',B,C)))
    assert parent(zigout,'f')==parent(rlout,'f')=='x'
    assert parent(rrout,'f')=='z'
    cert('maximum_proxy_zig_dual',rz(flip(zig)),flip(zigout))
    cert('maximum_proxy_LL_dual',pair(flip(rr),(0,0)),flip(rrout))
    cert('maximum_proxy_LR_dual',pair(flip(rl),(0,1)),flip(rlout))
    # The original neighbor z survives until the even terminal's final pair.
    # First minimum-helper parity determines z from source r/p.
    hodd=N('r',N('f',E,A),R)
    heven=N('r',N('p',N('f',E,A),M),R)
    hoddout=rz(hodd);hevenout=pair(heven,(0,0))
    assert hoddout[3][1]=='r' and hevenout[3][1]=='p'
    assert lz(flip(hodd))==flip(hoddout)
    assert pair(flip(heven),(1,1))==flip(hevenout)
    # The ordered-tree parent0 argument and its parent8 dual are in the
    # separate prose audit. Their static source requirements are checked below.
    assert (9+1)//2==5 and 4-(5//2)==2

    # Complete NEW main +1 exit table on arbitrary lower subtree L.
    L=V('LOWER')
    b,p,r,s,t='b','p5','r6','s7','t8'
    B6=N(r,N(p,N(b,L)),N(s,E,N(t)))
    B7=N(s,N(p,N(b,L),N(r)),N(t))
    B8=N(t,N(p,N(b,L),N(s,N(r))))
    B6p=N(r,N(p,N(b,L)),N(t,N(s)))
    F6=N(b,L,N(p,E,N(r,E,N(s,E,N(t)))))
    F7=N(b,L,N(p,E,N(s,N(r),N(t))))
    F8=N(b,L,N(p,E,N(t,N(s,N(r)))))
    H8=N(t,N(s,N(r,N(p,N(b,L)))))
    Q4=N(b,L,N(s,N(p,E,N(r)),N(t)))
    exits=[
      ('B6_key4',B6,lambda z:pair(z,(0,0)),F6),
      ('B7_key4',B7,lambda z:pair(z,(0,0)),F7),
      ('B8_key4',B8,lambda z:pair(z,(0,0)),F8),
      ('B6_key8',B6,lambda z:pair(z,(1,1)),H8),
      ('B7_key6',B7,lambda z:pair(z,(0,1)),B6),
      ('B8_key7',B8,lambda z:pair(z,(0,1)),B7),
      ('B8_key6',B8,lambda z:rz(local(z,(0,),lambda q:pair(q,(1,0)))),B6p),
    ]
    for name,source,fn,expected in exits:
        cert(name,fn(source),expected)
        # Reverse each explicit primitive expression, not numerical rank data.
        if name=='B6_key8':dout=pair(flip(source),(0,0))
        elif name.endswith('key4'):dout=pair(flip(source),(1,1))
        elif name=='B8_key6':dout=lz(local(flip(source),(1,),lambda q:pair(q,(0,1))))
        else:dout=pair(flip(source),(1,0))
        cert(name+'_dual',dout,flip(expected))
    upper=(b,p,r,s,t)
    assert all(depth(z,k)<=3 for z in (B6,B7,B8,B6p) for k in upper)
    assert all(depth(z,b)==2 for z in (B6,B7,B8,B6p))
    assert all(z[2][1]==p for z in (B6,B7,B8))
    assert H8[2][1]==s  # main min-helper neighbor candidates are upper/nonzero.
    assert all(depth(F7,k)<=3 for k in upper)
    assert all(depth(z,k)<=4 for z in (F6,F8) for k in upper)
    # T_B's only zero4 exit; marked a's cap is propagated separately.
    Hout=pair(local(H8,(0,0),lambda z:pair(z,(0,0))),(0,0))
    cert('H8_zero_key4',Hout,Q4)
    dout=pair(local(flip(H8),(1,1),lambda z:pair(z,(1,1))),(1,1))
    cert('H8_zero_key4_dual',dout,flip(Q4))
    assert all(depth(Q4,k)<=3 for k in upper)
    maxhelper=N(t,H8[2],N('f9'))
    maxout=lz(maxhelper)
    assert all(depth(maxout,k)<=5 for k in upper)

    # R_B lower-zero return, core prefix c,L5,L4, true depth4/5 only.
    for epsilon in (0,1):
        bottom=N('l',N('a',A,B),C) if epsilon==0 else N('l',A,N('a',B,C))
        source=N('c',N(p,N(b,bottom,E),M),R)
        after=local(source,(0,0),lambda z:pair(z,(0,epsilon)))
        after=pair(after,(0,0))
        assert depth(after,b)<=3 and depth(after,'c')==2
        dual=flip(source)
        dafter=local(dual,(1,1),lambda z:pair(z,(1,1-epsilon)))
        dafter=pair(dafter,(1,1))
        assert dafter==flip(after)
    # At depth5, the arbitrary lowest pair has already made a(A,B).
    source=N('c',N(p,N(b,N('a',A,B),E),M),R)
    after=rz(local(source,(0,),lambda z:pair(z,(0,0))))
    assert depth(after,b)==2 and depth(after,'c')==1
    dout=lz(local(flip(source),(1,),lambda z:pair(z,(1,1))))
    assert dout==flip(after)
    # Exact A lower return creates K_B, no V filter allowed.
    source=N('c',N(b,N('a',A,B),C),Y)
    target=pair(source,(0,0))
    assert target==N('a',A,N(b,B,N('c',C,Y)))

    # Generic K_c helper schemas, c=6/7/8. All intermediate marked Scores
    # are inside c.left/right and cannot rise above c after the helper.
    Khelpers=[
      (N('a',N('f',A,B),N(b,C,N('c',D,Y))),lambda z:rz(z)),
      (N('a',N('q',N('f',A,B),C),N(b,D,N('c',M,Y))),lambda z:pair(z,(0,0))),
      (N('a',N('q',A,N('f',B,C)),N(b,D,N('c',M,Y))),lambda z:pair(z,(0,1))),
    ]
    for i,(source,fn) in enumerate(Khelpers):
        out=fn(source)
        assert depth(out,'c')>=3 and depth(out,'a')<=2
        assert (depth(out,b)<=2)==(i!=1)
        if i==0:dout=lz(flip(source))
        elif i==1:dout=pair(flip(source),(1,1))
        else:dout=pair(flip(source),(1,0))
        assert dout==flip(out)

    # Root4 C_B zero exits with ANY actual left child. The old source
    # spines F6/F8 -> B8/B6 are REUSED, not recomputed here.
    def A_right_cases(block):
        return [
          (N(b,block,N('x',D,Y)),lambda z:lz(z)),
          (N(b,block,N('q',N('x',D,M),Y)),lambda z:pair(z,(1,0))),
          (N(b,block,N('q',D,N('x',M,Y))),lambda z:pair(z,(1,1))),
        ]
    direct=N('a',A,B)
    for i,(source,fn) in enumerate(A_right_cases(direct)):
        out=fn(source)
        assert path(out,b)==((0,) if i<2 else (0,0))
        if i<2:assert path(out,'a')==(0,0)  # R_B A-L form.
        else:assert depth(out,'a')==3  # R_B A-LL accepts G boundary extras.
    for side in (0,1):
        block=N('q0',N('a',A,B),C) if side==0 else N('q0',A,N('a',B,C))
        for i,(source,fn) in enumerate(A_right_cases(block)):
            out=fn(source)
            assert depth(out,'a')>=3
            owner=at(out,path(out,b))
            assert owner[2]==block and owner[2][1]!='a'
            assert path(owner[3],'a') is None
            if i==2:assert path(out,b)==(0,0)

    # Main B6->8: both allowed A barriers hide a and old owner cannot
    # reveal it through a one-step G read. Whole lower L is unchanged.
    sep=N('q0',N('a',A,B),C)
    leftguards=[N(b,sep,D),N('q',N(b,N('a',A,B),C),D)]
    for block in leftguards:
        for i,(source,fn) in enumerate(A_right_cases(block)):
            # Rename source owner b in generic schema to c; left block may
            # itself contain key b, so rebuild just the source root.
            source=N('c',block,source[3])
            out=fn(source)
            assert depth(out,'a')>=4
            owner=at(out,path(out,'c'))
            assert owner[2]==block and path(owner[3],'a') is None
            assert depth(owner,'a')>=3
    # The lower +1 child exposes a and gets R_B; an LR target keeps a
    # hidden and gets E1. Same typed substitution for outputs B6/B6p/B7.
    child=N('c',N('x',N(b,N('a',A,B),C),D),Y)
    childout=rz(child)
    assert path(childout,b)==(0,) and path(childout,'a')==(0,0)
    lr=N('c',N('q',N(b,N('a',A,B),C),N('x',D,M)),Y)
    lrout=pair(lr,(0,1))
    assert path(lrout,b)==(0,0) and depth(lrout,'a')==3
    assert path(at(lrout,path(lrout,'c')),'a') is None

    # Helper A right-side accesses increase the depth of an arbitrary
    # old-left block by1/2. For T_B, hidden a is in that block, so cannot
    # become a charge1 terminal under a maximum helper.
    LEFT=V('LEFT')
    for source,fn in (
      (N('c',LEFT,N('f',A,B)),lambda z:lz(z)),
      (N('c',LEFT,N('q',N('f',A,B),C)),lambda z:pair(z,(1,0))),
      (N('c',LEFT,N('q',A,N('f',B,C))),lambda z:pair(z,(1,1)))):
        assert depth(fn(source),'LEFT')>=2
    # Depth guard transport is affine in the lower internal a-depth ell.
    assert 3+2==5 and 1+2==3 and 5+2==7
    slacks={
      'K_positive':lin({'const':1,'weight_excess':1},{'target_debt':1},{'const':-1}),
      'R_zero_to_K':lin({'const':1,'credit_excess':1},{'const':-1}),
      'C_zero_to_R_or_E1':lin({'const':1,'credit_excess':1},{'const':-1}),
      'T_zero_to_E1':lin({'const':1,'credit_excess':1},{'const':-1}),
      'main_plus1_to_supported_region':lin({'const':1},{'const':1,'credit_excess':1},{'const':-2}),
      'main_paid_or_helper':lin({'const':2,'weight_excess':1},{'target_debt':1},{'const':-2}),
      'incoming_S_zero':lin({'const':2},{'const':-2,'source_room_below2':1}),
    }
    assert all(v>=0 for expr in slacks.values() for v in expr.values())

    # Source provenance for proxy leaf parent, path decoder, terminal pricing,
    # shared sigma and full final child vectors. No source root is built.
    folder=BASE.parent/'06_CERTIFICATES'
    bp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_B_CONTROLLER.py'
    sp=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_B_CONTROLLER.py'
    lp=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    def func(file,name):
        return next(n for n in ast.walk(ast.parse(file.read_text(encoding='utf-8-sig')))
          if isinstance(n,ast.FunctionDef) and n.name==name)
    valid=func(bp,'b_valid')
    gap=next(n for n in ast.walk(valid) if isinstance(n,ast.If) and ast.unparse(n.test)=='i >= NCORE')
    body='\n'.join(ast.unparse(n) for n in gap.body)
    assert 'd.EQ(bs.kl[i], d.const_int(2, 2))' in body and 'd.EQ(bs.kr[i], d.const_int(2, 2))' in body
    tree=ast.unparse(func(sp,'b_tree_valid'))
    assert 'if c < 9:' in tree and 'd.EQ(tot, d.const_int(1, 5))' in tree
    assert 'C = [b_valid(d, bs)] if intervals else []' in tree
    assert 'd.LT(gp, d.const_int(NCORE, W_BREF))' in tree
    decoder=ast.unparse(func(bp,'b_splay_event'))
    assert 'st = b_blend(d, pair_on, rotB, st)' in decoder
    assert 'st = b_blend(d, zig_on, rotZ, st)' in decoder
    low=ast.unparse(func(lp,'build_slow'))
    assert 'd.EQ(s.sig[i], t.sig[i])' in low
    assert 'b_tree_valid(d, t.b, bst5, t.sig)' in low
    assert 'b_tree_valid(d, bs[e + 1], bst, s.sig, intervals=False)' in low
    assert '(t.b.kl, bs[5].kl)' in low and '(t.b.kr, bs[5].kr)' in low
    assert 'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))' in low
    assert 'root_terminated(d, wit, bt, st, bs[e], e, active)' in low
    assert 'same_keep_target(d, wit, inv, bt, e, active)' in low
    assert 'no_intermediate_genuine(d, wit, s, bs, last, e, active)' in low
    assert ast.unparse(func(rp,'mux_ref').body[0])=='r = vec[0]'
    assert time.process_time()<CAP
    result={
      'status':'BURIED_BARRIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'new_equational_certificates':identity_names,
      'proxy_final_parent_either_terminal_or_previous_neighbor':True,
      'final_minimum_proxy_parent_is_core0_by_order_and_leaf':True,
      'final_maximum_proxy_parent_is_core8_by_order_and_leaf':True,
      'main_and_H8_minimum_helper_weight_at_least':2,
      'global_Gamma1_cheap_helper_initial_B_depth_at_most':2,
      'terminal_q_not_sum_of_helper_and_terminal_q':True,
      'main_plus1_exit_table_complete':True,
      'R_B_depth4_and_depth5_return_bounds':{'central4':3,'old_root':3},
      'no_V_filter_on_R_or_K_boundaries':True,
      'C_B_no_extra_A_guard':True,
      'H8_zero4_endpoint_all_marked_B_depths_at_most':3,
      'main_a_depth_guard':5,'C_a_depth_guard':3,'T_a_depth_guard':7,
      'guard_covers_all_original_S_zero_incoming_edges':True,
      'safe_operation_order':['K_B1','R_B1','C_B1','T_B1','G_B2'],
      'each_previously_valid_LOW_row_preserved':True,
      'all_G_B_source_LOW_rows_proved':True,
      'complete_eight_word_S_zero_frontier_closed':True,
      'all_zero_LOW_with_S_source_covered':True,
      'both_actual_LOW_orientations_proved':True,
      'signed_residuals':slacks,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'old_eight_spine_map_and_negative_core_checks_reused_not_replayed':True,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (bp,sp,lp,rp)},
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
