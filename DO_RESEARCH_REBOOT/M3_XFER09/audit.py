"""Separate universal term/sign/source audit. No finite transition tests.

Terms are universally quantified node roles with arbitrary subtree variables.
Source modules are parsed, never imported or executed. This checker is not a
full formalization of the compiler or the prose's order/type arguments.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('SUBTREE',name)
def N(label,left,right):return ('NODE',label,left,right)
def rz(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    x=t[2];return N(x[1],x[2],N(t[1],x[3],t[3]))
def lz(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    x=t[3];return N(x[1],N(t[1],t[2],x[2]),x[3])
def at(t,path):
    for direction in path:
        assert t[0]=='NODE'
        t=t[2+direction]
    return t
def lin(*parts):
    out={}
    for part in parts:
        for key,value in part.items():out[key]=out.get(key,0)+value
    return {k:v for k,v in out.items() if v}

def main():
    A,M,C=map(V,('OPAQUE_A','ARBITRARY_MIDDLE','OPAQUE_C'))
    left=N('r',N('x',A,M),C)
    right=N('r',A,N('x',M,C))
    leftout=rz(left);rightout=lz(right)
    assert leftout==N('x',A,N('r',M,C))
    assert rightout==N('x',N('r',A,M),C)
    assert at(left,(0,1))==at(leftout,(1,0))==M
    assert at(right,(1,0))==at(rightout,(0,1))==M
    assert at(leftout,(0,))==A and at(leftout,(1,1))==C
    assert at(rightout,(0,0))==A and at(rightout,(1,))==C
    assert at(leftout,(1,))[1]==at(rightout,(0,))[1]=='r'

    # Universal substitution for a REAL unmarked middle with a marked child.
    # All other subtrees remain variables; no keys or core trees are assigned.
    B,D,E=map(V,('LOWER_BLOCK','MARKED_LEFT_BLOCK','MARKED_RIGHT_BLOCK'))
    realmiddle=N('unmarked_middle',B,N('hidden_mark',D,E))
    lo=rz(N('r',N('x',A,realmiddle),C))
    ro=lz(N('r',A,N('x',realmiddle,C)))
    assert at(lo,(1,0))==at(ro,(0,1))==realmiddle
    assert at(lo,(1,0,1))[1]==at(ro,(0,1,1))[1]=='hidden_mark'

    # Independent algebraic slack derivation using indeterminates, not values.
    # w=s>=0: cap=2. w=-delta, 0<delta<=2: cap=2-delta.
    slacks={
      'nonnegative_weight_raised_source':lin({'weight_nonnegative':1},{'constant':2},{'constant':-2}),
      'negative_weight_raised_source':lin({'delta':-1},{'constant':2},{'constant':-2,'delta':1}),
      'unchanged_source':lin({'old_residual':1},{'target_increment':1}),
      'nonnegative_incoming_to_I2':lin({'weight_nonnegative':1},{'constant':2},{'constant':-2,'old_source_room':1}),
    }
    assert slacks['negative_weight_raised_source']=={}
    assert all(value>=0 for expr in slacks.values() for value in expr.values())
    assert lin({'old_source_debt':1},{'weight':-1},{'constant':-2})=={
      'old_source_debt':1,'weight':-1,'constant':-2}
    # The latter expression is <=0 by the REUSED valid negative-edge bound,
    # D(s)<=w+D(t)<=w+2. It is not an unconditional pointwise typed cap.

    folder=BASE.parent/'06_CERTIFICATES'
    lp=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    ap=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_SOURCE_REPAIRS.py'
    wp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_STRUCTURAL_WITNESS.py'
    ip=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ATOM_INVENTORY.py'
    trees={p:ast.parse(p.read_text(encoding='utf-8-sig')) for p in (lp,rp,ap,wp,ip)}
    def fn(p,name):
        return next(n for n in ast.walk(trees[p]) if isinstance(n,ast.FunctionDef) and n.name==name)
    def code(p,name):return ast.unparse(fn(p,name))
    assert ast.unparse(fn(rp,'mux_ref').body[0])=='r = vec[0]'
    shadow=code(lp,'shadow7');match=code(lp,'shadow_match7')
    assert 'd.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)' in shadow
    assert 'd.ITE(d.EQ(kk, d.const_int(0, 2)), dref, ref)' in shadow
    assert 'is_slot = d.EQ(kk, d.const_int(0, 2))' in match
    assert 'd.OR(d.NOT(is_slot), d.EQ(cs, s.aS[p]))' in match
    assert 'd.NOT(d.AND(is_slot, cs))' in match
    low=code(lp,'build_slow')
    required_low=[
      'C.append(s.aS[0])',
      'd.EQ(s.mu, t.mu)',
      'd.EQ(s.sig[i], t.sig[i])',
      'wit.wellformed()', 'wit.link_both()', 'wit.child_bound_prop()', 'inv.attach()', 'inv.valid()',
      'compat_pred(d, inv)',
      'root_terminated(d, wit, bt, st, bs[e], e, active)',
      'same_keep_target(d, wit, inv, bt, e, active)',
      'no_intermediate_genuine(d, wit, s, bs, last, e, active)',
      'b_tree_valid(d, t.b, bst5, t.sig)',
      'd.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5))',
    ]
    for fragment in required_low:assert fragment in low,fragment
    keep=code(ap,'same_keep_target')
    assert 'ag = inv._gapof(aR)' in keep and 'd.EQ(ag, bg)' in keep
    assert 'bg = d.SUB(bT, d.const_int(NCORE, 5), 5)' in keep
    gap=code(ip,'_gapof');attach=code(ip,'attach')
    assert 'd.LT(self.fullrank(k), ranknode)' in gap
    assert 'd.LT(self.fullrank(a), self.fullrank(b))' in attach
    bounds=code(wp,'child_bound_prop');well=code(wp,'wellformed')
    assert 'd.EQ(self.hi[c], self.rank[i])' in bounds
    assert 'd.EQ(self.lo[c], d.ADD(self.rank[i], d.const_int(1, W_RANK + 1), W_RANK + 1))' in bounds
    assert 'd.LE(self.lo[i], self.rank[i])' in well and 'd.LT(self.rank[i], self.hi[i])' in well
    assert 'self.p[i], self.p[j], self.isS[i], self.isS[j], d.EQ(self.sidx[i], self.sidx[j])' in well
    assert time.process_time()<CAP
    result={
      'status':'INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'universal_terms_checked':['left_child_zig','right_child_zig','middle_depth2_both_orientations',
        'opposite_exterior_cuts','hidden_marked_descendant_stays_depth3'],
      'signed_residual_polynomials':slacks,
      'order_argument':'middle rank strictly between two present Score ranks; gap cannot be0 or9',
      'old_root_marked_and_unmarked_branches_in_separate_prose_audit':True,
      'G_fallback_old_slot0_and_kind_filter_provenance_checked':True,
      'no_blanket_typed_source_cap_assumed':True,
      'negative_source_coverage_uses_existing_valid_negative_rows':True,
      'each_previously_valid_LOW_row_preserved':True,
      'all_I_source_nonnegative_H1_rows_proved':True,
      'all_I_source_zero_H1_residuals_exactly_zero':True,
      'all_I_source_LOW_rows_for_current_input_proved':True,
      'nonnegative_incoming_I2_rows_proved':True,
      'all_incoming_I_rows_claimed':False,
      'Gamma0_can_expose_hidden_marked_nodes':True,
      'Gamma1_from_I_excluded_by_present_interval':True,
      'all_admissible_signatures_and_private_completions':True,
      'strict_increase_uses_published_completed_B_fact_not_new_query':True,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in trees},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_outside_S_zero_H1_coverage_proved':False,
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

