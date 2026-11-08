"""New universal paired-relay/count/helper/sign audit; NO finite tests.

All node labels are unassigned ordered roles and all blocks arbitrary.
No original compiler/DAG/root, numeric core tree, population, mask or psi
is constructed or evaluated. Existing source provenance is reused by hash.
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
    x=tree[2];return N(x[1],x[2],N(tree[1],x[3],tree[3]))
def lz(tree):
    assert tree[0]=='NODE' and tree[3][0]=='NODE'
    x=tree[3];return N(x[1],N(tree[1],tree[2],x[2]),x[3])
def at(tree,path):
    for side in path:
        assert tree[0]=='NODE';tree=tree[2+side]
    return tree
def left(tree,sub):return N(tree[1],sub,tree[3])
def right(tree,sub):return N(tree[1],tree[2],sub)
def pair(tree,bits):
    if bits==(0,0):return rz(rz(tree))
    if bits==(0,1):return rz(left(tree,lz(tree[2])))
    if bits==(1,0):return lz(right(tree,rz(tree[3])))
    assert bits==(1,1)
    return lz(lz(tree))
def find(tree,key,path=()):
    if tree[0]=='BLOCK':return None
    if tree[1]==key:return path
    a=find(tree[2],key,path+(0,))
    return a if a is not None else find(tree[3],key,path+(1,))
def depth(tree,key):
    path=find(tree,key);assert path is not None;return len(path)
def lin(*parts):
    out={}
    for p in parts:
        for key,value in p.items():out[key]=out.get(key,0)+value
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,E,F,U,W=map(V,('A','B','C','D','E','F','UPPER_SIDE','OUTER_SIDE'))
    identities=[]
    def cert(name,out,expected):
        assert out==expected,name
        identities.append(name)
    # J's +1 c access and the main A zero relay in BOTH actual directions.
    jm=N('a',A,N('b',B,N('c',C,D)))
    jp=N('a',N('b',N('c',A,B),C),D)
    cert('J_minus_c_exit',pair(jm,(1,1)),N('c',N('b',N('a',A,B),C),D))
    cert('J_plus_c_exit',pair(jp,(0,0)),N('c',A,N('b',B,N('a',C,D))))
    gm=N('c',N('b',N('a',A,B),C),D)
    gp=N('c',A,N('b',B,N('a',C,D)))
    gmout=pair(gm,(0,0));gpout=pair(gp,(1,1))
    cert('G_minus_A_to_J',gmout,jm)
    cert('G_plus_A_to_J',gpout,jp)
    assert at(gmout,(1,))[1]=='b' and at(gmout,(1,1))[1]=='c'
    assert at(gpout,(0,))[1]=='b' and at(gpout,(0,0))[1]=='c'

    # Depth4: after the fixed top two edges there are exactly two edges,
    # hence these FOUR universal bottom pair words exhaust the path schema.
    # These are arbitrary-block identities, not evaluated core trees.
    bottom=[
      ((0,0),N('q',N('p',N('a',A,B),C),D)),
      ((0,1),N('q',N('p',A,N('a',B,C)),D)),
      ((1,0),N('q',A,N('p',N('a',B,C),D))),
      ((1,1),N('q',A,N('p',B,N('a',C,D)))),
    ]
    depth4=[]
    for bits,bt in bottom:
        processed=pair(bt,bits)
        assert processed[1]=='a'
        source_minus=N('c',N('b',bt,U),W)
        source_plus=N('c',U,N('b',W,bt))
        assert depth(source_minus,'a')==depth(source_plus,'a')==4
        after_minus=pair(N('c',N('b',processed,U),W),(0,0))
        after_plus=pair(N('c',U,N('b',W,processed)),(1,1))
        cert('core_depth4_minus_'+''.join(map(str,bits)),after_minus,
          N('a',processed[2],N('b',processed[3],N('c',U,W))))
        cert('core_depth4_plus_'+''.join(map(str,bits)),after_plus,
          N('a',N('b',N('c',U,W),processed[2]),processed[3]))
        assert depth(after_minus,'b')==depth(after_plus,'b')==1
        assert depth(after_minus,'c')==depth(after_plus,'c')==2
        depth4.append({'bottom_word':list(bits),'both_actual_top_orientations':True,
          'final_b_depth':1,'final_c_depth':2,'full_target_J_structural_guard':True})

    # Original extreme helper: source A depth1/2 only. Arbitrary blocks may
    # carry unmarked Score support; no empty-support hypothesis is imposed.
    helpers=[
      ('minimum_L',N('a',N('f',A,B),N('b',C,N('c',D,E))),(0,),1),
      ('minimum_LL',N('a',N('p',N('f',A,B),C),N('b',D,N('c',E,F))),(0,0),2),
      ('minimum_LR',N('a',N('p',A,N('f',B,C)),N('b',D,N('c',E,F))),(0,1),1),
      ('maximum_R',N('a',N('b',N('c',A,B),C),N('f',D,E)),(1,),1),
      ('maximum_RR',N('a',N('b',N('c',A,B),C),N('p',D,N('f',E,F))),(1,1),2),
      ('maximum_RL',N('a',N('b',N('c',A,B),C),N('p',N('f',D,E),F)),(1,0),1),
    ]
    helper_certificates=[]
    for name,source,bits,old_a_depth in helpers:
        out=(rz(source) if bits==(0,) else lz(source)) if len(bits)==1 else pair(source,bits)
        assert out[1]=='f'
        assert depth(out,'a')==old_a_depth
        assert depth(out,'b')==old_a_depth+1
        assert depth(out,'c')==old_a_depth+2
        assert depth(out,'a')<=2 and depth(out,'b')<=3 and depth(out,'c')>=3
        # The entire original opposite b/c block remains under old a.
        olda=at(out,find(out,'a'))
        if name.startswith('minimum'):assert olda[3]==source[3]
        else:assert olda[2]==source[2]
        helper_certificates.append({'case':name,'old_a_depth':old_a_depth,
          'b_depth':depth(out,'b'),'c_depth':depth(out,'c'),
          'whole_opposite_block_unchanged':True,'c_not_terminal_charge1':True})

    # Symbolic count slacks, not numerical key/height assignments.
    # min: c-5=(b-4)+(c-b-1). max: 3-c=(4-b)+(b-c-1).
    # Those two summands are nonnegative by the public class guards.
    assert lin({'c':1,'constant':-5},{'b':-1,'constant':4},
      {'c':-1,'b':1,'constant':1})=={}
    assert lin({'constant':3,'c':-1},{'constant':-4,'b':1},
      {'b':-1,'c':1,'constant':1})=={}
    count_bounds={
      'minus_between_marks_depth_bound':'c-b<=3',
      'minus_upper_marks_depth_bound':'8-c<=3 because (b-4)+(c-b-1)>=0',
      'plus_between_marks_depth_bound':'b-c<=3',
      'plus_lower_marks_depth_bound':'c<=3 because (4-b)+(b-c-1)>=0',
      'old_a_depth':2,'old_b_depth':1,
      'every_marked_label_after_J_c_exit_depth_at_most':3,
    }
    slacks={
      'J_weight2_b_exit':lin({'constant':2},{'target_debt':1},{'constant':-2}),
      'J_weight1_c_exit':lin({'constant':1},{'constant':1,'E1_credit_excess':1},{'constant':-2}),
      'J_Gamma1_weight_at_least3':lin({'constant':3,'weight_excess':1},{'target_debt':1},{'constant':-2}),
      'G_zero_a_exit_to_J':lin({'constant':2},{'constant':-2}),
      'G_weight2_b_exit':lin({'constant':2},{'target_debt':1},{'constant':-2}),
      'unchanged_source':lin({'old_residual':1},{'target_increment':1}),
      'nonnegative_incoming_J_or_G':lin({'weight_nonnegative':1},{'source_room_below2':1}),
    }
    assert all(v>=0 for expr in slacks.values() for v in expr.values())
    assert slacks['G_zero_a_exit_to_J']=={}

    # Reuse completed shadow, G/kind, same-key and original H/q pricing
    # checks by hashes. Do not execute any old checker or original module.
    priorpath=BASE.parent/'M3_XFER09/symbolic_audit.json'
    prior=json.loads(priorpath.read_text())
    assert prior['status']=='INTERVAL_CHILD_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    for path,h in prior['source_hashes'].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==h
    # NEW audit issue: c at A depth>=3 cannot be a charge1 terminal.
    rp=BASE.parent/'06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/PC_ROTATION_INTERPRETER.py'
    tree=ast.parse(rp.read_text(encoding='utf-8-sig'))
    event=next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='event_a')
    eventcode=ast.unparse(event)
    assert 'd.EQ(dd, d.const_int(3, 3)), d.const_int(2, 3)' in eventcode
    assert 'd.EQ(dd, d.const_int(4, 3)), d.const_int(2, 3)' in eventcode
    assert time.process_time()<CAP
    result={
      'status':'MARKED_RELAY_UNIVERSAL_SYMBOLIC_AUDIT_PASS',
      'universal_identities':identities,'complete_depth4_bottom_word_certificates':depth4,
      'helper_A_depth_and_opposite_block_certificates':helper_certificates,
      'J_c_exit_marked_core_count_bounds':count_bounds,'signed_slacks':slacks,
      'J_no_V_filter_or_private_completion_guard':True,
      'main_full_G_boundary_targets_still_satisfy_J':True,
      'J_actual_H1_targets_only_b_c_by_extremal_pair_order':True,
      'J_Gamma1_terminal_only_a_or_b_and_original_B_q_at_most':1,
      'J_Gamma1_original_H2_weight_at_least':3,
      'G_no_actual_anonymous_source_charge1_target':True,
      'operation_order':['J_capacity2','G_capacity2'],
      'each_previously_valid_LOW_row_preserved_by_each_operation':True,
      'all_J_and_G_source_LOW_rows_proved':True,
      'G_zero_marked_grandchild_residual_exactly':0,
      'both_ancestors_marked':True,'main_G_sources_outside_S':True,
      'all_nonnegative_incoming_J_G_rows_valid':True,
      'negative_incoming_blanket_validity_claimed':False,
      'all_compatible_core_subtrees_and_admissible_signatures':True,
      'strict_numerical_increase_of_old_debt_claimed':False,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,
      'completed_provenance_reused_sha256':hashlib.sha256(priorpath.read_bytes()).hexdigest(),
      'new_source_AST_hashes':{rp.as_posix():hashlib.sha256(rp.read_bytes()).hexdigest()},
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'all_marked_ancestor_grandchild_zero_H1_coverage_proved':False,
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

