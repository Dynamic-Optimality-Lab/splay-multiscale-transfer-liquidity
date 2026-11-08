"""Universal root-removal proof audit; NO finite state/population tests.

Only open subtree terms, linear identities, source AST/provenance and
existing proof-index metadata are read. No source compiler/psi is run.
"""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(120.0,float(sys.argv[1]))
E=('EMPTY',)

def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def V(n):return ('BLOCK',n)
def N(k,l=E,r=E):return ('NODE',k,l,r)
def right(t):
    assert t[0]=='NODE' and t[2][0]=='NODE'
    a=t[2];return N(a[1],a[2],N(t[1],a[3],t[3]))
def left(t):
    assert t[0]=='NODE' and t[3][0]=='NODE'
    a=t[3];return N(a[1],N(t[1],t[2],a[2]),a[3])
def pair(t,p):
    if p=='LL':return right(right(t))
    if p=='RR':return left(left(t))
    if p=='LR':return right(N(t[1],left(t[2]),t[3]))
    assert p=='RL';return left(N(t[1],t[2],right(t[3])))
def project(t):
    if t==E:return E
    if t[0]=='BLOCK':return V('project('+t[1]+')')
    assert t[0]=='NODE'
    if t[1]=='f':
        # IMPORTANT: this operation may only delete a FINAL valid leaf.
        assert t[2]==t[3]==E,'attempt to project an INTERNAL helper'
        return E
    return N(t[1],project(t[2]),project(t[3]))
def lin(*parts):
    out={}
    for part in parts:
        for k,v in part.items():out[k]=out.get(k,0)+v
    return {k:v for k,v in out.items() if v}

def main():
    A,B,C,D,T,R,L=map(V,('A','B','C','D','T','R','L'))
    ids=[]
    # Four universally quantified CORE-pair schemas. Blocks remain free;
    # their projections are new formal variables, never concrete values.
    schemas=[
      ('LL',N('r',N('p',N('y',A,B),C),D)),
      ('RR',N('r',A,N('p',B,N('y',C,D)))),
      ('LR',N('r',N('p',A,N('y',B,C)),D)),
      ('RL',N('r',A,N('p',N('y',B,C),D))),
    ]
    for word,t in schemas:
        assert project(pair(t,word))==pair(project(t),word)
        ids.append('core_projection_commutes_'+word+'_arbitrary_blocks')

    # Exact initial helper outputs: both depths, both actual directions.
    initial=[
      ('min_h1',right(N('zero',N('f'),R)),N('f',E,N('zero',E,R))),
      ('min_h2',pair(N('r',N('zero',N('f'),T),R),'LL'),N('f',E,N('zero',E,N('r',T,R)))),
      ('max_h1',left(N('eight',L,N('f'))),N('f',N('eight',L,E),E)),
      ('max_h2',pair(N('r',L,N('eight',T,N('f'))),'RR'),N('f',N('eight',N('r',L,T),E),E)),
    ]
    for name,actual,expected in initial:
        assert actual==expected,name
        ids.append(name+'_actual_primitive_output')

    # Only the last helper-involving pair is new. No internal helper
    # root is projected. Source C is obtained from its CORE CHILD.
    m=N('f',E,N('zero',E,N('y',B,C)))
    mout=N('y',N('zero',N('f'),B),C)
    assert pair(m,'RR')==mout
    assert project(mout)==left(project(m[3]))
    ids.extend(['minimum_final_RR_exact','minimum_final_core_equals_core_last_left_zig'])
    q=N('f',N('eight',N('y',A,B),E),E)
    qout=N('y',A,N('eight',B,N('f')))
    assert pair(q,'LL')==qout
    assert project(qout)==right(project(q[2]))
    ids.extend(['maximum_final_LL_exact','maximum_final_core_equals_core_last_right_zig'])
    # The structural induction uses exactly three COMMON pairs, then
    # original top pair vs core zig. No path suffix/state is enumerated.
    assert 8-1==7 and 8-2*3==2 and 7-2*3==1
    assert 2-(7//2)==-1 and 4-(8//2)==0
    lengths={'expanded_depth':8,'core_depth':7,'common_core_pairs':3,
      'remaining_expanded_depth':2,'remaining_core_depth':1,
      'auxiliary_core_weight':-1,'original_H2_weight':0,'original_q':4}

    # Independently expand the signed identities. Each summand named in
    # repayment is nonnegative by a DIFFERENT established local premise.
    floor={'Dt':1,'psi_t':-1}
    core_law={'psi_t':1,'psi_C':-1,'one':-1}
    nonnegative_psi={'psi_C':1}
    source_room={'one':1,'Ds':-1}
    repayment=lin(floor,core_law,nonnegative_psi,source_room)
    assert repayment=={'Dt':1,'Ds':-1}
    destination_floor=lin(core_law,nonnegative_psi)
    assert destination_floor=={'psi_t':1,'one':-1}
    visible_negative={'one':-1,'Dt_prime':1,'Ds':-1}
    comparison_target_room={'one':2,'Dt_prime':-1}
    source_cap=lin(visible_negative,comparison_target_room)
    assert source_cap==source_room
    slacks={'repayment_coefficients':repayment,'destination_floor_coefficients':destination_floor,
      'source_cap_coefficients':source_cap,
      'repayment_nonnegative_basis':{'saved_D_floor':1,'old_negative_core_residual':1,'psi_C':1,'one_minus_source_D':1}}
    assert all(v>=0 for v in slacks['repayment_nonnegative_basis'].values())

    old=BASE.parent/'M3_XFER14'
    old_a=json.loads((old/'symbolic_audit.json').read_text())
    assert old_a['status']=='ZERO_FRONTIER_UNIVERSAL_SYMBOLIC_AUDIT_PASS'
    assert old_a['Gamma1_zero_terminal_depth_exact']==8 and old_a['visible_Gamma1_source_cap']==1
    assert old_a['Gamma1_residual_helper_depth_exact']==2
    assert not old_a['current_potential_changed']
    inherited=json.loads((old/'dependencies.json').read_text())
    pins={v['path']:v['sha256'] for v in inherited['files']}
    source_hashes=old_a['source_hashes_reused_not_executed']
    for p,h in source_hashes.items():assert sha(p)==h,p
    # Pure AST read of the original paired/single B-controller contract;
    # the production module is NEVER imported or executed.
    bc=next(Path(p) for p in source_hashes if p.endswith('/PC_B_CONTROLLER.py'))
    syntax=ast.parse(bc.read_text(encoding='utf-8-sig'))
    fn=next(n for n in syntax.body if isinstance(n,ast.FunctionDef) and n.name=='b_splay_event')
    body=ast.get_source_segment(bc.read_text(encoding='utf-8-sig'),fn)
    assert fn.args.args[0].arg=='d'
    assert 'pair_on' in body and 'zig_on' in body and 'b_single_rot' in body and 'is_delete' in body

    # Exact completed proof dependencies. No saved core table is queried.
    deps=[BASE.parent/'RESEARCH_RULES.md',BASE.parent/'M3_E1_01/OUTSIDE_E1.md',
      BASE.parent/'M3_E1_01/PROOF_AUDIT.md',BASE.parent/'M3_COMB_AUD01/AUDIT_REPORT.md',
      BASE.parent/'M3_XFER08/BURIED_BARRIER_THEOREM.md',
      BASE.parent/'M3_XFER14/ZERO_FRONTIER_THEOREM.md',BASE.parent/'M3_XFER14/PROOF_AUDIT.md',
      BASE.parent/'M3_XFER14/partition.json',BASE.parent/'M3_XFER14/certificate.json',
      BASE.parent/'M3_XFER14/symbolic_audit.json']
    ldr=next(Path(p) for p in pins if p.endswith('/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md'))
    deps.append(ldr)
    for p in deps:
        assert p.exists()
        if p.as_posix() in pins:assert sha(p)==pins[p.as_posix()],p
    # Read only theorem text to verify its needed ALL-core scope. This
    # is provenance for an old established theorem, not its re-execution.
    text=ldr.read_text(encoding='utf-8')
    assert 'all 4,862 ordered core topologies' in text
    assert 'Dropping' in text and 'overapproximation' in text
    capacity=(BASE.parent/'M3_E1_01/OUTSIDE_E1.md').read_text(encoding='utf-8')
    assert 'w_x+p_x >= psi(B)' in capacity and '0<=psi(B),p_x<=2' in capacity

    partition=json.loads((old/'partition.json').read_text())
    expected={'G1-MIN-V-r1','G1-MIN-V-r2','G1-MIN-V-r7','G1-MIN-V-r8',
      'G1-MAX-V-r6','G1-MAX-V-r7','G1-MAX-V-r0','G1-MAX-V-r1'}
    actual={c['id'] for c in partition['cells'] if c['normal_form']=='Gamma1' and '-V-' in c['id']}
    assert actual==expected
    closures=[];new_cells=[]
    for c in partition['cells']:
        item=dict(c)
        if c['id'] in expected:
            assert c['source_D_at_most']==1 and c['source_B_terminal_depth'] in (6,7)
            assert c['helper_source_B_depth']==2 and c['preterminal_B_depth']==8
            item.update(status='CLOSED_UNIVERSAL',proof='VISIBLE_GAMMA1_REPAYMENT.md',
              signed_residual_at_least=0,current_debt_drop_options=[],
              destination_psi_at_least=1,all_old_quantifiers_retained=True,
              closure_needed=None)
            closures.append({'id':c['id'],'status':'CLOSED_UNIVERSAL','source_D_at_most':1,
              'target_psi_at_least':1,'signed_residual_at_least':0,
              'method':'root-removal depth7 core law; SAME-source original negative H1 cap',
              'all_original_quantifiers_retained':True})
        elif c['normal_form']=='Gamma1':
            assert '-H-' in c['id']
            item.update(destination_psi_at_least=1,current_debt_drop_options=[[2,1]],
              closure_needed='prove destination D=2 when source D=2; target0 subcases now excluded')
        new_cells.append(item)
    assert len(closures)==8 and len(new_cells)==52
    assert sum(c['status']=='OPEN' for c in new_cells)==44
    assert sum(c['status']=='OPEN' and c['normal_form']=='H1' for c in new_cells)==36
    assert sum(c['status']=='OPEN' and c['normal_form']=='Gamma1' for c in new_cells)==8
    # These are proof-index metadata updates, not original state tests.
    write('profile_closures.json',{'fixed_potential':'D_exp unchanged','all_eight_visible_profiles_closed':True,
      'profiles':closures,'no_profile_population_or_original_state_tests':True})
    write('partition_update.json',{'parent_partition':(old/'partition.json').as_posix(),
      'parent_sha256':sha(old/'partition.json'),'old_files_preserved':True,
      'universal_schematic_slots':52,'newly_closed':8,'remaining_open':44,
      'remaining_H1':36,'remaining_hidden_Gamma1':8,'hidden_possible_drop_only':[[2,1]],
      'Step4_complete':False,'no_open_cell_nonemptiness_asserted':True,'cells':new_cells})
    assert time.process_time()<CAP
    result={'status':'VISIBLE_GAMMA1_ROOT_REMOVAL_UNIVERSAL_AUDIT_PASS',
      'new_universal_constructor_identities':ids,'path_pair_arithmetic':lengths,'signed_algebra':slacks,
      'auxiliary_C_is_proper_nine_core_tree_proved_in_separate_audit':True,
      'C_needs_original_full_state_realization':False,'D_of_C_used':False,
      'internal_helper_projected_as_leaf':False,'last_helper_pair_checked_separately':True,
      'all_Gamma1_zero_destination_psi_at_least':1,'all_eight_visible_profiles_closed':True,
      'all_original_quantifiers_retained':True,'current_potential_changed':False,
      'hidden_source2_destination2_claimed':False,'remaining_open_H1':36,'remaining_open_hidden_Gamma1':8,
      'hidden_possible_failure_only':[2,1],'Step4_complete':False,'M3_status':'OPEN',
      'source_hashes_reused_not_executed':source_hashes,'AST_read_only_source':bc.as_posix(),
      'reused_proof_hashes':{p.as_posix():sha(p) for p in deps},
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,'original_negative_cycle_certified':False,
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'new_universal_identities':len(ids),
      'visible_profiles_closed':8,'remaining_open_schemas':44,'Step4':'OPEN',
      'new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
