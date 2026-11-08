"""Resume unfinished pinned provenance and coverage; no source/sign rerun."""
import hashlib,json,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
CAP=min(119.5,float(sys.argv[1]))
def lp(p):return Path('\\\\?\\'+str(Path(p).resolve()))
def sha(p):return hashlib.sha256(lp(p).read_bytes()).hexdigest()
def read(p):return json.loads(lp(p).read_text(encoding='utf-8'))
def write(n,v):
    with (BASE/n).open('x',encoding='utf-8') as stream:json.dump(v,stream,indent=2)

def main():
    first=read(BASE/'run_result.json');fc=read(BASE/'controller_exit.json')
    ex=read(BASE/'symbolic_audit_exit.json');log=lp(BASE/'log_symbolic_audit.txt').read_text(encoding='utf-8')
    assert first['status']=='FAILED_OR_UNKNOWN_STOP' and first['error']['type']=='AssertionError'
    assert 'line 113, in main' in log and 'p.as_posix() in pins' in log
    assert first['child_CPU']==0.28125 and fc['whole_process_CPU_seconds']==0.21875
    assert ex['error']['type']=='AssertionError'
    sc=read(BASE/'checkpoint01_source.json');sg=read(BASE/'checkpoint02_sign.json')
    assert sc['status']==sg['status']=='PASS'
    assert sc['all_LOW_destinations_P_proved_with_reused_splay_root_postcondition']
    assert sg['any_previously_valid_LOW_row_preserved'] and sg['all_off_P_LOW_rows_proved']
    # Read existing completed proof/checkpoint results. No old audit module
    # is imported, and no original source AST/sign calculation is repeated.
    source_hashes=sc['source_hashes'];clauses=sc['asserted_terminal_clauses'];signs=sg['symbolic_coefficients']
    baseline=read(BASE/'entry_baseline.json');pins={v['path']:v['sha256'] for v in baseline['files']}
    old=BASE.parent/'M3_XFER16';dp=old/'dependencies.json'
    assert dp.as_posix() in pins and sha(dp)==pins[dp.as_posix()]
    inherited=read(dp);ipins={v['path']:v['sha256'] for v in inherited['files']}
    ldr=next(Path(p) for p in ipins if p.endswith('/IAGS_11G_S03_M3_LDR01_LOW_DEFICIT_RUN_REPAYMENT.md'))
    assert ldr.as_posix() not in pins and len(str(ldr))>260
    assert sha(ldr)==ipins[ldr.as_posix()]
    write('supplemental_dependency_pin.json',{'path':ldr.as_posix(),'sha256':ipins[ldr.as_posix()],
      'inherited_from':dp.as_posix(),'inherited_metadata_entry_sha256':pins[dp.as_posix()],
      'entry_traversal_omitted_path':True,'inherited_preexisting_hash_verified':True})
    text=lp(ldr).read_text(encoding='utf-8')
    assert 'psi(source)=2, psi(destination)=0' in text and 'all 4,862 ordered core topologies' in text
    deps=[BASE.parent/'RESEARCH_RULES.md',BASE.parent/'M3_AER01/RESULT.md',
      BASE.parent/'M3_E1_01/OUTSIDE_E1.md',old/'HIDDEN_GAMMA1_REPAYMENT.md',
      old/'PROOF_AUDIT.md',old/'PARTITION_UPDATE.md',old/'certificate.json',
      old/'symbolic_audit.json',old/'partition_update.json']
    # These short-file pins passed before the interrupted last dependency.
    assert all(p.as_posix() in pins for p in deps)
    deps_hashes={p.as_posix():pins[p.as_posix()] for p in deps}
    deps_hashes[ldr.as_posix()]=ipins[ldr.as_posix()]
    zerofloor={'blanket_H1_zero_target_psi_at_least1':'REFUTED_BY_REUSED_ESTABLISHED_ZERO_RESET',
      'new_saved_psi_query_or_control_replay':False,'current_D_hid_or_D_term_refuted_by_this_fact':False}
    part=read(old/'partition_update.json');cells=[]
    for c in part['cells']:
        v=dict(c);v['current_potential']='D_term = D_hid on P, 0 outside P'
        if c['normal_form']=='H1':
            assert c['status']=='OPEN'
            v.update(source_P_required_for_any_failure=True,source_root_must_be_marked=True,
              root_mark_status_axis_closed_for_unmarked_sources=True,current_failure_both_values_equal_D_hid=True,
              closure_needed='prove signed repayment on the full remaining MARKED-source original H1 zero schema',
              remaining_quantifiers='marked synchronized source; all remaining original masks/core topologies/parent types/exposures/G/raw fields/sigma/private witnesses')
            if c['psi_source']==1:v['source_core_height_at_most']=6
        else:
            assert 'CLOSED' in c['status']
            v.update(status='CLOSED_UNIVERSAL_FOR_D_term',transport='terminal-root source reduction preserves every valid LOW row')
        cells.append(v)
    assert len(cells)==52 and sum(c['status']=='OPEN' for c in cells)==36
    assert all(c['source_root_must_be_marked'] for c in cells if c['status']=='OPEN')
    write('partition_update.json',{'parent_partition':(old/'partition_update.json').as_posix(),
      'parent_sha256':sha(old/'partition_update.json'),'all_old_files_preserved':True,
      'every_unmarked_source_LOW_row_closed':True,'marked_source_required_for_any_remaining_failure':True,
      'remaining_H1_schematic_slots':36,'remaining_Gamma1_zero_slots':0,
      'slots_are_universal_formulas_not_tested_instances':True,'all_remaining_signed_leaves_closed':False,
      'Step4_complete':False,'no_remaining_cell_nonemptiness_asserted':True,'cells':cells})
    assert time.process_time()<CAP
    result={'status':'TERMINAL_ROOT_NORMALIZATION_UNIVERSAL_AUDIT_PASS',
      'all_original_LOW_destinations_P':True,'source_marked_requirement_added_to_original_graph':False,
      'new_public_debt':'D_term=D_hid on marked synchronized Score roots, 0 elsewhere',
      'every_previously_valid_LOW_row_preserved':True,'all_unmarked_source_LOW_rows_proved':True,
      'global_psi_floor_for_new_debt_claimed':False,'global_E1_floor1_for_new_debt_claimed':False,
      'psi_floor_at_all_LOW_destinations_preserved':True,'HIGH_h0_glue_preserved':True,
      'all_completed_Gamma1_zero_rows_preserved':True,'all_original_quantifiers_and_full_coordinates_preserved':True,
      'new_source_AST_conjuncts_checked':clauses,'symbolic_sign_certificates':signs,
      'reused_zero_reset_scope_audit':zerofloor,'source_hashes_reused_not_executed':source_hashes,
      'reused_proof_hashes':deps_hashes,'remaining_H1_schemas':36,'remaining_sources_marked_only':True,
      'remaining_Gamma1_zero_schemas':0,'all_remaining_marked_H1_leaves_closed':False,
      'requested_full_Step4_closure_achieved':False,'Step4_complete':False,'M3_status':'OPEN',
      'first_failed_component_retained':True,'completed_source_sign_checkpoints_reexecuted':False,
      'long_dependency_pin_supplemented_from_old_frozen_metadata':True,
      'new_finite_tests':0,'new_source_transition_queries':0,'new_original_root_evaluations':0,
      'new_saved_psi_queries':0,'new_bank_censuses':0,'new_label_fits':0,'completed_semantic_checks_replayed':0,
      'original_negative_cycle_certified':False,'full_compiler_formalization_claimed':False,
      'external_human_or_model_review_claimed':False,'CPU_seconds':time.process_time(),'CPU_cap':CAP}
    write('symbolic_audit.json',result)
    print(json.dumps({'status':result['status'],'completed_checkpoints_reused':True,
      'all_unmarked_source_LOW':'PROVED','remaining_marked_H1_schemas':36,
      'Step4':'OPEN','requested_full_closure_achieved':False,'new_finite_tests':0},indent=2),flush=True)

if __name__=='__main__':
    error=None
    try:main()
    except BaseException as exception:
        error={'type':type(exception).__name__,'message':str(exception)}
        raise
    finally:write('symbolic_audit_resume_exit.json',{'whole_process_CPU_seconds':time.process_time(),'CPU_cap':CAP,'error':error})
