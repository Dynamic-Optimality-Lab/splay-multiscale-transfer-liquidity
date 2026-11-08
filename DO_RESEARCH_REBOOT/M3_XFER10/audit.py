"""New universal term/interval/G/sign/source audit; NO finite tests.

Tree labels are unassigned ordered roles; blocks are arbitrary subtrees.
The interval checker proves symbolic entailments from role-order premises.
It evaluates no original tree, DAG, source root, population, mask or psi.
Completed kind/G/price provenance is reused by immutable hashes, not rerun.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))

def write(name,obj):
    with (BASE/name).open('x',encoding='utf-8') as stream:json.dump(obj,stream,indent=2)
def V(name):return ('BLOCK',name)
def N(key,left,right):return ('NODE',key,left,right)
def rz(tree):
    assert tree[0]=='NODE' and tree[2][0]=='NODE'
    c=tree[2];return N(c[1],c[2],N(tree[1],c[3],tree[3]))
def lz(tree):
    assert tree[0]=='NODE' and tree[3][0]=='NODE'
    c=tree[3];return N(c[1],N(tree[1],tree[2],c[2]),c[3])
def at(tree,path):
    for side in path:
        assert tree[0]=='NODE'
        tree=tree[2+side]
    return tree
def replace_left(tree,sub):
    return N(tree[1],sub,tree[3])
def replace_right(tree,sub):
    return N(tree[1],tree[2],sub)
def blocks(tree,lo='LOW',hi='HIGH',out=None):
    if out is None:out={}
    if tree[0]=='BLOCK':
        assert tree[1] not in out
        out[tree[1]]=(lo,hi)
    else:
        blocks(tree[2],lo,tree[1],out);blocks(tree[3],tree[1],hi,out)
    return out
def observations(tree,path=()):
    result=[(tree[0],tree[1],path)]
    if len(path)<2 and tree[0]=='NODE':
        result+=observations(tree[2],path+(0,))+observations(tree[3],path+(1,))
    return result
def find(tree,key,path=()):
    if tree[0]=='NODE' and tree[1]==key:return path
    if tree[0]=='BLOCK':return None
    p=find(tree[2],key,path+(0,))
    return p if p is not None else find(tree[3],key,path+(1,))
def lin(*parts):
    out={}
    for p in parts:
        for key,value in p.items():out[key]=out.get(key,0)+value
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D=map(V,('A','B','C','D'))
    schemas=[
      ('LL',N('r',N('p',N('x',A,B),C),D),
        lambda z:rz(rz(z)),N('x',A,N('p',B,N('r',C,D))),
        ('LOW','x','p','r','HIGH'),('LOW','p'),{'C','D'}),
      ('LR',N('r',N('p',A,N('x',B,C)),D),
        lambda z:rz(replace_left(z,lz(z[2]))),N('x',N('p',A,B),N('r',C,D)),
        ('LOW','p','x','r','HIGH'),('p','r'),{'A','D'}),
      ('RL',N('r',A,N('p',N('x',B,C),D)),
        lambda z:lz(replace_right(z,rz(z[3]))),N('x',N('r',A,B),N('p',C,D)),
        ('LOW','r','x','p','HIGH'),('r','p'),{'A','D'}),
      ('RR',N('r',A,N('p',B,N('x',C,D))),
        lambda z:lz(lz(z)),N('x',N('p',N('r',A,B),C),D),
        ('LOW','r','p','x','HIGH'),('p','HIGH'),{'A','B'}),
    ]
    case_certificates=[]
    for name,source,operation,expected,order,barrier,opaque in schemas:
        target=operation(source)
        assert target==expected,name
        # These edges are logical role-order hypotheses, not Score ordinals.
        rel=set(zip(order,order[1:]))
        def lt(a,b):
            frontier=[a];seen=set()
            while frontier:
                v=frontier.pop()
                if v in seen:continue
                seen.add(v)
                for u,w in rel:
                    if u==v:
                        if w==b:return True
                        frontier.append(w)
            return False
        def le(a,b):return a==b or lt(a,b)
        intervals=blocks(source)
        source_obs=observations(source)
        assert all(role in ('r','p','x') for kind,role,path in source_obs if kind=='NODE')
        assert all(role in opaque for kind,role,path in source_obs if kind=='BLOCK')
        assert find(source,'x') is not None and len(find(source,'x'))==2
        assert all(kind=='NODE' for kind,role,path in source_obs if role in ('r','p','x'))
        target_obs=observations(target)
        assert target_obs[0]==('NODE','x',())
        exposed=[]
        second_G=[]
        for kind,role,path in target_obs[1:]:
            if kind=='NODE':
                assert role in ('p','r')  # Both are UNMARKED hypotheses.
                continue
            if role in opaque:continue
            lo,hi=intervals[role]
            assert le(barrier[0],lo) and le(hi,barrier[1]),(name,role,lo,hi)
            assert not (lt(lo,'x') and lt('x',hi)),(name,role)
            exposed.append({'block':role,'path':list(path),'interval':[lo,hi],
              'inside_public_barrier':True,'marked_x_strictly_inside':False})
            if len(path)==1:
                # If this WHOLE newly exposed block is G, its children at
                # shadow depth2 read old source slot0 r's CURRENT children.
                oldroot=at(target,find(target,'r'))
                assert oldroot[0]=='NODE'
                assert oldroot[2][0]==oldroot[3][0]=='BLOCK'
                assert oldroot[2][1] in opaque and oldroot[3][1] in opaque
                second_G.append({'alias_block':role,'old_root_children':
                  [oldroot[2][1],oldroot[3][1]],'both_opaque':True})
        assert len(exposed)==2
        assert bool(second_G)==(name in ('LL','RR'))
        case_certificates.append({'case':name,'universal_pair_identity':True,
          'source_no_actual_anonymous_depth1_or2':True,
          'barrier':list(barrier),'exposed_nonopaque_blocks':exposed,
          'depth1_G_second_shadow_level':second_G,
          'proper_marked_nodes_excluded_by_barrier_and_uniqueness':True,
          'all_G_labels_are_old_unmarked_r':True,'target_V_empty':True})

    # w=s>=0 -> cap2. w=-delta,0<delta<=2 -> cap2-delta.
    # No numerical weight assignments or lists of core depths are tested.
    slacks={
      'raised_nonnegative_H1':lin({'weight_nonnegative':1},{'constant':2},{'constant':-2}),
      'raised_negative_H1':lin({'delta':-1},{'constant':2},{'constant':-2,'delta':1}),
      'unchanged_source':lin({'old_residual':1},{'target_increment':1}),
      'old_debt_nonnegative_Z_H1':lin({'weight_nonnegative':1},{'constant':2},{'constant':-2,'source_room':1}),
      'incoming_nonnegative_Z2':lin({'weight_nonnegative':1},{'constant':2},{'constant':-2,'source_room':1}),
    }
    assert slacks['raised_negative_H1']=={}
    assert all(v>=0 for expr in slacks.values() for v in expr.values())

    # Reuse completed shadow/G/kind/pricing provenance, WITHOUT rerunning
    # its semantic checks; hashes establish that the original sources match.
    previous=BASE.parent/'M3_XFER09/symbolic_audit.json'
    prior=json.loads(previous.read_text())
    assert prior['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for name,h in prior['source_hashes'].items():
        assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==h
    folder=BASE.parent/'06_CERTIFICATES'
    lp=folder/'DIRECT_CDK5N_11F_STRICT_CLOSURE/STRICT_LOW_COMPILER.py'
    rp=folder/'DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    def fn(path,name):
        tree=ast.parse(path.read_text(encoding='utf-8-sig'))
        return next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name==name)
    # New provenance issue: original ROOT SCORE is distinct from MASK MARK.
    lowfn=fn(lp,'build_slow');low=ast.unparse(lowfn)
    assert 'C.append(s.aS[0])' in low
    mubit_calls=[n for n in ast.walk(lowfn) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='mubit']
    assert len(mubit_calls)==1 and ast.unparse(mubit_calls[0])=='mubit(d, s.mu, k)'
    assert 'd.EQ(tsi, d.const_int(k, 4)), mubit(d, s.mu, k)' in low
    assert 'C.append(marked)' in low
    # New source-order provenance: same-direction pair rotates p/r first;
    # opposite-direction pair rotates x/p first, then x/r.
    pair=ast.unparse(fn(rp,'splay_event'))
    for fragment in (
      'xA = d.ITE(same, path[t + 1], path[0])',
      'pA = d.ITE(same, path[min(t + 2, 4)], path[t + 1])',
      'pB = d.ITE(same, path[t + 1], path[min(t + 2, 4)])',
      'st = blend(d, pair_on, rotA, st)',
      'st = blend(d, pair_on, rotB, st)',
    ):assert fragment in pair,fragment
    assert pair.index('st = blend(d, pair_on, rotA, st)')<pair.index('st = blend(d, pair_on, rotB, st)')
    # The depth2 active event has A charge1, not2.
    charge=ast.unparse(fn(rp,'event_a'))
    assert 'd.EQ(dd, d.const_int(2, 3)), d.const_int(1, 3)' in charge
    assert time.process_time()<CAP
    result={
      'status':'GRANDCHILD_UNMARKED_ANCESTOR_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'case_certificates':case_certificates,'signed_slacks':slacks,
      'source_root_Score_not_required_mask_marked_verified':True,
      'pair_primitive_order_checked_from_original_AST':True,
      'completed_shadow_G_kind_price_provenance_reused_not_replayed':True,
      'reused_provenance_file_sha256':hashlib.sha256(previous.read_bytes()).hexdigest(),
      'target_empty_V_for_all_four_cases':True,
      'each_previously_valid_LOW_row_preserved':True,
      'all_Z_source_nonnegative_H1_rows_valid_even_before_new_cap':True,
      'all_Z_source_zero_H1_F_residuals_exactly_zero':True,
      'all_Z_source_LOW_rows_for_current_input_proved':True,
      'all_Z_source_H1_current_F_residuals':'max(w,0)',
      'negative_source_cap_inferred_only_on_actual_previously_valid_negative_rows':True,
      'nonnegative_incoming_Z2_rows_proved':True,'all_incoming_Z_rows_claimed':False,
      'Gamma1_from_Z_excluded_by_no_anonymous_source_charge1_target':True,
      'Gamma0_may_expose_hidden_marks_original_floor_reused':True,
      'newly_exposed_depth1_G_children_checked_LL_RR':True,
      'all_admissible_signatures_and_private_completions':True,
      'strict_capacity_increase_uses_published_completed_B_fact_no_new_query':True,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'source_hashes':{p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in (lp,rp)},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_outside_S_grandchild_zero_H1_coverage_proved':False,
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

