from delivery_support import *
from periodic_payment import periodic_cost
import subprocess


def inherited_pins():
    inp=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    assert file_hash(C1/'CONT01_DELIVERY_MANIFEST.json')==inp['Continuation01_manifest_sha256']
    for p,h in inp['Continuation01_files'].items():assert file_hash(C1/p)==h,p
    import finalize as prior_finalize
    prior_finalize.ROOT=C1
    counts=prior_finalize.verify_pins()
    assert counts==inp['historical_hash_pin_counts']
    return counts


if __name__=='__main__':
    counts=inherited_pins()
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    depfiles=['DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md',
              'DO_RESEARCH_REBOOT/CD5_BASE01/dependency_pins.json',
              'DO_RESEARCH_REBOOT/02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md',
              'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/CW_MARKED_CORE_MONOTONICITY.md']
    pins={p:file_hash(REPO/p) for p in depfiles}
    declared=json.loads((REPO/depfiles[1]).read_text())['pins']
    for p in depfiles[2:]:assert next(z['sha256'] for z in declared if z['path']==p)==pins[p]
    write('C2_DEPENDENCY_PINS.json',{'files':pins,'scope':'B-only marked-core geometry; no CD(5) cost leaf imported',
        'already_declared_selected_geometry_hashes_match':True})
    sources,scopes,provenance=source_archive();names={s['name'] for s in sources}
    full=json.loads((ROOT/'FINAL_COMPLETE_SOURCE_VERIFICATION.json').read_text())
    assert {z['source'] for z in full}==names and len(full)==18
    assert all(z['all_complete_intermediate_states_equal_by_exact_edge_and_fringe_induction'] and
               z['original_S_is_full_physical_population'] and z['paired_closure'] for z in full)
    verification={z['source']:z for z in full}
    periodic={}
    for f in ['DILATED_RESULTS.json','PRIVATE_ANCESTOR_RESULTS.json','ADAPTIVE_RESULTS.json']:
        zs=json.loads((ROOT/f).read_text())
        for z in zs:
            name=z.get('source',z.get('name'))
            for key in ['G_periodic','H_periodic','G','H']:
                c=z.get(key)
                if c and c.get('eligible_periodic'):
                    periodic.setdefault(name,{'artifact':f,'key':key,'cost':c['B_cyclic'],
                                              'variant':c.get('variant',key),'cut_before':c.get('cut_before',1)})
    optimum=json.loads((ROOT/'PERIODIC_OPTIMUM_CERTIFICATE.json').read_text())
    assert optimum['eligible_periodic'] and optimum['A']==48849
    periodic[optimum['source']]={'artifact':'PERIODIC_OPTIMUM_CERTIFICATE.json','variant':'G','cut_before':1,
        'cost':optimum['minimum_over_all_permitted_full_period_cuts_and_raw_G_H_variants'],
        'all_cut_minimum_proved':True}
    records=[]
    for s in sources:
        name=s['name'];targets=[x for tag,x in s['operations'] if tag=='K']
        c=periodic_cost(targets,set(int(k) for k in s['initial_B']['children']))
        if c['B_cyclic']<=10*s['A']:
            periodic.setdefault(name,{'variant':'raw','cut_before':1,'cost':c['B_cyclic'],
                                     'artifact':'EXP04_RESIDUAL_INVENTORY.json','computed_from_full_source':True})
        assert name in periodic,(name,'no saved positive certificate')
        assert periodic[name]['cost']<=10*s['A']
        if 'adaptive' in name:s['corrected_body_predicate']='original q_B<=4; permits depth9'
        records.append({'source':name,'population':len(s['initial_B']['children']),
            'operations':len(s['operations']),'A':s['A'],'Q_B':s['Q_B'],**scopes[name],
            'raw_cyclic_certificate':c,'funded_old_periodic_certificate':periodic[name],
            'original_R_next_P_occurrences':[],
            'R_next_P_zero_status':'proved for THIS source by the inherited periodic theorem; not inferred from absent Pi enumeration',
            'independent_complete_physical_verification':'FINAL_COMPLETE_SOURCE_VERIFICATION.json'})
    write('EXP04_SOURCE_WITNESSES.json',{'inherited_original_archive':'../EXP04_SOURCE_WITNESSES.json',
        'inherited_original_archive_sha256':file_hash(PARENT/'EXP04_SOURCE_WITNESSES.json'),
        'Continuation01_archive':'../CONTINUATION_01_COVERAGE_PROOF/EXP04_SOURCE_WITNESSES.json',
        'Continuation01_archive_sha256':file_hash(C1/'EXP04_SOURCE_WITNESSES.json'),
        'new_unique_complete_original_source_count':18,'new_unique_complete_original_sources':sources,
        'source_batches':sorted(set(provenance.values())),
        'active_cycle_prototypes_not_full_original_classifications':288,
        'interrupted_input_not_counted_as_completed':'INTERRUPTED_P9_INPUT.json'})
    write('EXP04_RESIDUAL_INVENTORY.json',{'immutable_original_R_star_definition':'Inherited EXP03 unhandled minus original equality-restart paid occurrences; unchanged',
        'immutable_R_next_P_definition':'Original R_star minus frozen carrier, four skipped-rank, cheap KEEP-gap and periodic-or-local hybrid paid sets; unchanged',
        'auxiliary_R_upper_wide_definition':'Literal original R_next_P outside prefix j<=2A_gap, current-A-ancestor, and actual <=8-genuine-key B-return classes',
        'unrestricted_absolute_K_status':'OPEN','new_sources':records,
        'full_original_Pi_U_cohorts_R6_enumerated_sources':sum(scopes[n]['full_original_Pi_U_cohorts_R6_classification'] for n in names),
        'direct_neutral_internal_parent_free_control_sources':1,'other_screened_without_full_Pi_sources':13,
        'finite_source_results_do_not_imply_universal_availability':True})
    private=json.loads((ROOT/'PRIVATE_ANCESTOR_RESULTS.json').read_text())[0]
    upper=json.loads((ROOT/'PRIVATE_UPPER_VERIFICATION.json').read_text())
    write('EXP04_PHYSICAL_LIFECYCLES.json',{'critical_new_original_upper_parent':upper,
        'original_upper_U_certificates':private['upper_U_certificates'],
        'original_gap_events':private['original_R_star'],
        'full_source_and_state_pool':'PRIVATE_UPPER_FULL_TRACE.json',
        'independent_primitive_SET_Pi_U':'PRIVATE_UPPER_INDEPENDENT_PI.json',
        'additional_original_lifecycles':['HELPER_TRACE_5.json','DILATED_FULL_ORIGINAL_TRACE.json'],
        'inherited_lifecycles':'../CONTINUATION_01_COVERAGE_PROOF/EXP04_PHYSICAL_LIFECYCLES.json',
        'no_shadow_reclassification':True})
    write('EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',{'current_operation_payments':'PROOF_LEDGER.md A1',
        'current_ancestor_6A_is_inherited_optional_T7':True,
        'private_upper_parent_verification':upper,
        'inherited_finite_local_payment_audit':'INHERITED_LOCAL_PAYMENT_AUDIT.json',
        'upper_original_R_star_parents_exist':True,'upper_R_next_P_existence':'OPEN',
        'raw_ancestry_mass_bound_claimed':False,'arbitrary_historical_last_loss_injection_claimed':False})
    write('EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',{'analytic_proofs':'PROOF_LEDGER.md R1,A1',
        'source_uniform_loads':{'original_cyclic_KEEP_gap_A_partition':1,'small_return_extended_arc_subcover':2,
            'prefix_gaps_per_double':3,'current_A_rotation_bit_gap_load':3},
        'proved_new_or_activated_budgets':{'prefix_A_coefficient':6,'current_ancestor_A_coefficient':6,
            'small_return_b8_A_coefficient':42,'combined_target_partial_A_coefficient':54},
        'combined_optimized_Q_A_coefficient':'89+48 C_seq+102 C_DF',
        'unbounded_support_return_sharing_bound':'OPEN',
        'finite_implementation_checks':['STRUCTURAL_VERIFICATION.json','COMPULSORY_MODEL_VERIFICATION.json'],
        'old_hybrid_comparison_budget_unchanged':'30 C_DF A, source-disjoint periodic/local cases'})
    resources=[{'file':p.name,**json.loads(p.read_text())} for p in sorted(ROOT.glob('RESOURCE_*.json'))]
    measured=sum(z['process_CPU_seconds'] for z in resources if isinstance(z.get('process_CPU_seconds'),(int,float)))
    assert measured<2400
    write('EXP04_EXPERIMENT_LOG.json',{'measured_CPU_seconds_including_both_interrupted_processes':measured,
        'measured_subtotal_is_exact_total_campaign_CPU':False,
        'additional_unmetered_research_pass':'RESOURCE_final_audit_unmetered.json',
        'other_unmetered':'small shell inspections, report authoring and final index/hash verification',
        'initial_staged_CPU_allocation':1800,'reviewed_staged_CPU_allocation':2400,
        'initial_allocation_overrun_preserved':True,'exact_total_budget_compliance_claimed':False,
        'allocation_is_not_observed_host_quota':True,'peak_observed_working_set_bytes':5049520128,
        'working_set_aim_bytes':3*1024**3,'memory_aim_exceeded':True,'resources':resources,
        'new_unique_completed_sources':18,'full_original_Pi_U_cohorts_R6_enumerations':4,
        'direct_zero_control_sources':1,'other_physical_screen_sources':13,
        'active_cycle_prototypes':288,'interrupted_original_input_population':2049,
        'largest_completed_population':max(z['population'] for z in records),
        'longest_completed_original_operation_count':max(z['operations'] for z in records),
        'universal_K_proved':False,'genuine_simultaneous_escape_verified':False,
        'conclusion':'C. Open checkpoint'})
    required=['EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_THEOREM_LEDGER.md',
        'EXP04_COUNTEREXAMPLE_LEDGER.md','EXP04_RESIDUAL_INVENTORY.json','EXP04_PHYSICAL_LIFECYCLES.json',
        'EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json','EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',
        'EXP04_SOURCE_WITNESSES.json','EXP04_EXPERIMENT_LOG.json','EXP04_REPRODUCTION.md','EXP04_FINAL_VERDICT.md']
    assert all((ROOT/p).exists() for p in required)
    write('FINAL_VERIFICATION.json',{'HEAD':head,'branch':branch,'tracked_changes':[],
        'Continuation01_files_unchanged':len(json.loads((ROOT/'INPUT_MANIFEST.json').read_text())['Continuation01_files']),
        'historical_hash_pin_counts':counts,'new_geometry_dependency_pins':'C2_DEPENDENCY_PINS.json',
        'all18_sources_complete_state_verified':'FINAL_COMPLETE_SOURCE_VERIFICATION.json',
        'private_original_Pi_independent_verification':'PRIVATE_UPPER_VERIFICATION.json',
        'periodic_all_cut_exact_minimum':'PERIODIC_OPTIMUM_CERTIFICATE.json',
        'compulsory_model_implementation_verification':'COMPULSORY_MODEL_VERIFICATION.json',
        'four_double_grammar_runtime_verification':'RESTRICTED_GRAMMAR_VERIFICATION.json',
        'measured_CPU_subtotal':measured,'unmetered_research_receipt':'RESOURCE_final_audit_unmetered.json',
        'universal_target_status':'OPEN','required_outcome':'C. Open checkpoint',
        'audit_scope':'same-agent analytic proofs and independent implementations; not external/formal certification'})
    files={str(p.relative_to(ROOT)).replace('\\','/'):file_hash(p) for p in sorted(ROOT.rglob('*'))
           if p.is_file() and p.name!='CONT02_DELIVERY_MANIFEST.json'}
    write('CONT02_DELIVERY_MANIFEST.json',{'HEAD':head,'branch':branch,'files':files,
        'required_deliverables':required,'historical_hash_pin_counts':counts,
        'mathematical_verdict':'C. Open checkpoint','target':'R_next_P<=K A for every admissible original source',
        'strongest_new_partial_bound':'R_next_P<=54A+R_upper_wide',
        'excluded_self':'CONT02_DELIVERY_MANIFEST.json','new_unique_complete_original_sources':18})
    print('PASS preserved pins',counts,'sources',len(sources),'files',len(files),
          'measured CPU subtotal',measured,'plus disclosed unmetered work; Outcome C',flush=True)
