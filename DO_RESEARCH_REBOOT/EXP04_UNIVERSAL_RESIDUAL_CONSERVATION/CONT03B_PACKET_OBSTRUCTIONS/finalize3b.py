from delivery_support3b import *
import ast


if __name__=='__main__':
    inp=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    assert file_hash(C3/'CONT03_DELIVERY_MANIFEST.json')==inp['C3_manifest_sha256']
    for p,h in inp['C3_files'].items():assert file_hash(C3/p)==h,('C3',p)
    for p,h in inp['C2_files'].items():assert file_hash(C2/p)==h,('C2',p)
    import checkpoint_finalize as prior
    prior.ROOT=C2;counts=prior.inherited_pins();assert counts==inp['historical_pin_counts']
    exp1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    for p,h in inp['EXP01_root_entry_inputs'].items():assert file_hash(exp1/p)==h,('EXP01',p)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head==inp['HEAD']=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
    sources,rows,provenance=collect();names={s['name'] for s in sources}
    checked=json.loads((ROOT/'ALL_SOURCE_VERIFICATION.json').read_text())
    assert len(checked)==301 and {z['source'] for z in checked}==names
    by={z['source']:z for z in checked};inventory=[];full_count=0
    for s in sources:
        z=rows[s['name']];v=by[s['name']]
        assert v['all_complete_intermediate_states_equal_by_exact_edge_and_fringe_induction'] and v['paired_closure']
        assert v['positive_old_raw_periodic_certificate']['B_cyclic']<=10*s['A']
        full=z.get('original_Pi_classification',z.get('full_original_Pi_classification',False));full_count+=full
        inventory.append({'source':s['name'],**provenance[s['name']],
            'population':len(s['initial_B']['children']),'original_S':v['original_raw_support'],
            'operations':len(s['operations']),'A':s['A'],'Q_B':s['Q_B'],
            'original_Pi_classified':full,'original_R_star':z.get('original_R_star'),
            'prehybrid_original_C':z.get('ordered_accounting',{}).get('C_after_frozen_and_prefix'),
            'literal_primary_R_upper':[],
            'zero_final_residual_reason':'Valid source with an explicit old raw periodic certificate; not inferred from an unrun Pi oracle.',
            'old_positive_raw_periodic':v['positive_old_raw_periodic_certificate'],
            'reaching_prefix_operations_verified':v['explicit_common_diagonal_reaching_prefix_operations_verified']})
    assert full_count==13
    write('EXP04_SOURCE_WITNESSES.json',{'date':'2026-11-11',
        'inherited_C3_archive':'../CONTINUATION_03_UPPER_PARENT/EXP04_SOURCE_WITNESSES.json',
        'inherited_C3_archive_sha256':file_hash(C3/'EXP04_SOURCE_WITNESSES.json'),
        'new_complete_source_count':301,'new_complete_sources':sources,
        'source_batches':[a for a,b in BATCHES],
        'incomplete_prototype_files':['INCOMPLETE_WARM_PROTOTYPES.json','PAIR_INCOMPLETE_PROTOTYPES.json'],
        'unbounded_family_scope':'Legal original words and exact paired restoration only; Pi counterexample properties are verified per saved instance.'})
    write('EXP04_RESIDUAL_INVENTORY.json',{'immutable_primary_R_upper':'Original R_star minus frozen carrier/skipped, original index-prefix, own-path and original hybrid in that order.',
        'new_counterexample_pool':'C before own-path and hybrid deductions, exactly the C3 definition.',
        'new_overflow_pool':'D=R_star minus F,E_old,H_all; first2A_gap distinct D parents selected; literal remaining overflow.',
        'primary_universal_K_status':'OPEN','new_sources':inventory,
        'full_original_Pi_sources':13,'physical_only_without_Pi_sources':288,
        'unrun_Pi_means_zero':False,'finite_success_is_universal_proof':False})
    cert=json.loads((ROOT/'COUNTEREXAMPLE_CERTIFICATE.json').read_text())
    assert cert['source']=='C3B_d9_x120_A118' and cert['population']==577 and cert['operations']==1933
    assert (cert['A'],cert['Q_B'])==(2715,1515)
    trace=json.loads((ROOT/cert['complete_original_trace']).read_text())
    s=next(s for s in sources if s['name']==cert['source'])
    assert trace['source']['name']==s['name'] and digest(trace['events'])==s['trace_hash']
    assert trace['source']['operations']==s['operations']
    assert cert['epoch_packet']['selected_first_parent']==[646,3] and cert['epoch_packet']['remaining_original_parents']==[[653,4]]
    assert len(cert['original_R_star'])==3 and not cert['original_R_upper_escape']
    pi=json.loads((ROOT/'COUNTEREXAMPLE_INDEPENDENT_PI.json').read_text())
    pairs=json.loads((ROOT/'COUNTEREXAMPLE_INDEPENDENT_R6.json').read_text())
    assert pi['complete_immutable_primitive_rotations']==8340 and len(pi['independently_reconstructed_all_original_U'])==23
    assert pairs['cohort_count']==16 and len(pairs['independently_recomputed_all_original_pairs'])==7
    write('EXP04_PHYSICAL_LIFECYCLES.json',{'main_original_counterexample':cert,
        'verified_B_ancestry_lifecycle':json.loads((ROOT/'B_ANCESTRY_LIFECYCLE_VERIFICATION.json').read_text()),
        'failed_193_key_cohort_filters':'COHORT_FILTER_AUDIT.json',
        'fixed_actual_A_component':'root154, complete key interval137..576, rigid through both consuming parents',
        'original_signed_ownership_and_first_hits_preserved':True})
    write('EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',{'new_falsification':'prehybrid C first-use availability',
        'parent_ids':[[646,3],[653,4]],'actual_shared_A_demotion_bit':['A',133,24,1],'old_g':154,
        'no_new_g_demotion_between_consumers':True,'later_target_B_ancestry_recreated_between_consumers':False,
        'proved_structural_alternatives':'PROOF_LEDGER.md G0,G1,N',
        'historical_unit_root_entry_and_last_loss_refutations_preserved':True,
        'universal_unweighted_ancestry_mass_bound_claimed':False})
    pp=json.loads((ROOT/'COUNTEREXAMPLE_PACKET_PAYMENT.json').read_text())
    assert {tuple(z['actual_A_StepEv']) for z in pp['selected_parent_allocations']}=={('A',646,1),('A',653,1)}
    assert not pp['literal_overflow'] and pp['maximum_actual_A_StepEv_gap_load']<=6
    interface=json.loads((ROOT/'PACKET_INTERFACE_VERIFICATION.json').read_text());assert len(interface)==13
    write('EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',{'analytic_proofs':'PROOF_LEDGER.md P1-P3,N',
        'fixed_column_parent_per_KEEP_capacity':1,'fixed_column_gap_load_per_actual_A_StepEv':3,
        'quota_parent_load_per_actual_A_StepEv':2,'quota_gap_load_per_actual_A_StepEv':6,
        'actual_cyclic_KEEP_gap_resource_partition_load':1,
        'counterexample_column_and_quota_donors':pp,
        'same_coefficient_new_Q_interface':'47+48 C_seq+102 C_DF plus literal overflow',
        'new_missing_bound':'sum_h(b_h(D)-2A(G_h))_+ <= K0 A, source-uniform; OPEN',
        'source_uniform_packet_fit_or_column_count_assumed':False})
    resources=[{'file':p.name,**json.loads(p.read_text())} for p in sorted(ROOT.glob('RESOURCE_*.json'))]
    cpu=sum(z['process_CPU_seconds'] for z in resources);peak=max(z['memory']['peak_working_set_bytes'] for z in resources)
    assert cpu<800 and peak<3*1024**3
    assert len(sources)<=352 and max(len(s['initial_B']['children']) for s in sources)<=769
    assert max(len(s['operations']) for s in sources)<=8192
    write('EXP04_EXPERIMENT_LOG.json',{'measured_research_CPU_seconds':cpu,'planning_CPU_allocation':800,
        'all_failed_measured_runs_included':True,'resource_receipt_missing':False,
        'unmetered':'short inspections, ad-hoc metadata/path checks, report authoring and final hashing',
        'hard_host_quota_observed':False,'peak_observed_working_set_bytes':peak,'working_set_aim_bytes':3*1024**3,
        'planning_reviews':['STRATEGY_REVIEW_01.md','STRATEGY_REVIEW_02.md','STRATEGY_REVIEW_03.md'],
        'new_complete_sources':301,'full_original_Pi_sources':13,'physical_only_sources':288,
        'largest_population':max(len(s['initial_B']['children']) for s in sources),
        'longest_operation_word':max(len(s['operations']) for s in sources),
        'resources':resources,'result':'C. New exact obstruction','primary_universal_K_proved':False})
    required=['EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_THEOREM_LEDGER.md','EXP04_COUNTEREXAMPLE_LEDGER.md',
        'EXP04_RESIDUAL_INVENTORY.json','EXP04_PHYSICAL_LIFECYCLES.json','EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',
        'EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json','EXP04_SOURCE_WITNESSES.json','EXP04_EXPERIMENT_LOG.json',
        'EXP04_REPRODUCTION.md','EXP04_FINAL_VERDICT.md']
    assert all((ROOT/p).exists() for p in required)
    write('FINAL_VERIFICATION.json',{'date':'2026-11-11','HEAD':head,'branch':branch,'tracked_changes':[],
        'preserved_C3_files':101,'preserved_C2_files':109,'transitive_historical_pins':counts,
        'new_complete_source_state_and_prefix_checks':301,'full_original_Pi_classifications':13,
        'independent_counterexample':{'primitive_SET_transitions':8340,'U':23,'cohorts':16,'pairs':7},
        'original_paid_selectors_independently_reimplemented':False,
        'new_counterexample_to':'Prehybrid C first-use availability','counterexample_to_primary_R_upper_O_A':False,
        'new_global_payment_budgets':{'one_fixed_g_column':3,'quota_replacing_original_prefix':6},
        'new_full_Q_coefficient':'47+48 C_seq+102 C_DF plus literal overflow',
        'measured_CPU_seconds':cpu,'all_required_deliverables':True,'Python_ASTs_valid':True,
        'result':'C. New exact obstruction','primary_universal_conservation':'OPEN',
        'audit_scope':'same-agent analytic proofs and independent programs; no formal/external/complete-DO audit'})
    files={p.relative_to(ROOT).as_posix():file_hash(p) for p in sorted(ROOT.rglob('*'))
           if p.is_file() and p.name!='CONT03B_DELIVERY_MANIFEST.json'}
    write('CONT03B_DELIVERY_MANIFEST.json',{'HEAD':head,'branch':branch,'date':'2026-11-11','files':files,
        'required_deliverables':required,'excluded_self':'CONT03B_DELIVERY_MANIFEST.json',
        'result':'C. New exact obstruction','primary_universal_R_upper_O_A':'OPEN',
        'new_exact_refutation':'577-key original prehybrid C first-use law counterexample',
        'new_alternative_route':'Real A-gap quota6A and literal residual-parent overflow',
        'historical_pin_counts':counts})
    print('PASS sealed continued C3:',len(files),'artifacts;301 complete sources;13 original Pi;',
        '8340-bit independent counterexample; CPU',cpu,'; Outcome C, universal target OPEN',flush=True)
