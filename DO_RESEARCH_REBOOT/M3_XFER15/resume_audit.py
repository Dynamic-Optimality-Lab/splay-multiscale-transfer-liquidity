"""Resume unfinished provenance/coverage ONLY; completed math is not rerun."""
import ast,hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(119.546875,float(sys.argv[1]))
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def read(p):return json.loads(lp(p).read_text(encoding='utf-8'))
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    first=read(BASE/'run_result.json');first_c=read(BASE/'controller_exit.json')
    first_e=read(BASE/'symbolic_audit_exit.json')
    log=(BASE/'log_symbolic_audit.txt').read_text(encoding='utf-8')
    assert first['status']=='FAILED_OR_UNKNOWN_STOP' and first['error']['type']=='AssertionError'
    assert first_e['error']['type']=='AssertionError' and first_c['error']['type']=='AssertionError'
    assert 'line 137, in main' in log and 'assert p.exists()' in log
    assert first['child_CPU']==0.234375 and first_c['whole_process_CPU_seconds']==0.21875
    source=(BASE/'audit.py').read_text(encoding='utf-8')
    syntax=ast.parse(source)
    mainfn=next(n for n in syntax.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    assert any(isinstance(n,ast.Assert) and n.lineno==137 for n in ast.walk(mainfn))
    assert not any(isinstance(n,ast.Try) and n.lineno<137 for n in ast.walk(mainfn))
    # This records previously completed checks using the pinned executable
    # and exact traceback point. None of those mathematical calls is rerun.
    ids=['core_projection_commutes_'+w+'_arbitrary_blocks' for w in ('LL','RR','LR','RL')]
    ids += [n+'_actual_primitive_output' for n in ('min_h1','min_h2','max_h1','max_h2')]
    ids += ['minimum_final_RR_exact','minimum_final_core_equals_core_last_left_zig',
      'maximum_final_LL_exact','maximum_final_core_equals_core_last_right_zig']
    lengths={'expanded_depth':8,'core_depth':7,'common_core_pairs':3,
      'remaining_expanded_depth':2,'remaining_core_depth':1,
      'auxiliary_core_weight':-1,'original_H2_weight':0,'original_q':4}
    slacks={'repayment_coefficients':{'Dt':1,'Ds':-1},
      'destination_floor_coefficients':{'psi_t':1,'one':-1},
      'source_cap_coefficients':{'one':1,'Ds':-1},
      'repayment_nonnegative_basis':{'saved_D_floor':1,'old_negative_core_residual':1,'psi_C':1,'one_minus_source_D':1}}
    prefix={'status':'COMPLETED_PREFIX_REUSED_NOT_RERUN','executed_source':(BASE/'audit.py').as_posix(),
      'executed_source_sha256':sha(BASE/'audit.py'),'traceback_log_sha256':sha(BASE/'log_symbolic_audit.txt'),
      'failed_later_at_line':137,'completed_constructor_identities':ids,'completed_path_arithmetic':lengths,
      'completed_signed_algebra':slacks,'old_source_hash_and_AST_checks_completed':True,
      'mathematical_prefix_reexecuted':False}
    write('successful_prefix_checkpoint.json',prefix)

    old=BASE.parent/'M3_XFER14';old_a=read(old/'symbolic_audit.json')
    inherited=read(old/'dependencies.json')
    pins={v['path']:v['sha256'] for v in inherited['files']}
    deps=[BASE.parent/'RESEARCH_RULES.md',BASE.parent/'M3_E1_01/OUTSIDE_E1.md',
      BASE.parent/'M3_E1_01/PROOF_AUDIT.md',BASE.parent/'M3_COMB_AUD01/AUDIT_REPORT.md',
      BASE.parent/'M3_XFER08/BURIED_BARRIER_THEOREM.md',old/'ZERO_FRONTIER_THEOREM.md',
      old/'PROOF_AUDIT.md',old/'partition.json',old/'certificate.json',old/'symbolic_audit.json']
    ldr=next(Path(p) for p in pins if p.endswith('/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md'))
    assert len(str(ldr))>260 and lp(ldr).exists()
    assert sha(ldr)==pins[ldr.as_posix()]
    deps.append(ldr)
    # Only the previously unfinished theorem-scope provenance checks.
    text=lp(ldr).read_text(encoding='utf-8')
    assert 'all 4,862 ordered core topologies' in text
    assert 'Dropping' in text and 'overapproximation' in text
    capacity=lp(BASE.parent/'M3_E1_01/OUTSIDE_E1.md').read_text(encoding='utf-8')
    assert 'w_x+p_x >= psi(B)' in capacity and '0<=psi(B),p_x<=2' in capacity

    partition=read(old/'partition.json')
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
              destination_psi_at_least=1,all_old_quantifiers_retained=True,closure_needed=None)
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
      'source_hashes_reused_not_executed':old_a['source_hashes_reused_not_executed'],
      'reused_proof_hashes':{p.as_posix():sha(p) for p in deps},
      'successful_prefix_checkpoint':'successful_prefix_checkpoint.json',
      'first_component_status_retained':first['status'],'long_path_repair_within_same_bounded_audit':True,
      'mathematical_prefix_reexecuted':False,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_label_fits':0,'new_bank_censuses':0,
      'completed_semantic_checks_replayed':0,'original_negative_cycle_certified':False,
      'full_compiler_formalization_claimed':False,'external_human_or_model_review_claimed':False,
      'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'completed_prefix_reused':True,
      'visible_profiles_closed':8,'remaining_open_schemas':44,'Step4':'OPEN',
      'new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_resume_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
