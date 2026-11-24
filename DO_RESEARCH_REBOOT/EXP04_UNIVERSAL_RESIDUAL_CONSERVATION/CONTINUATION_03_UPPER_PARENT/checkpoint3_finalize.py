from delivery3_support import *
import ast


if __name__=='__main__':
    inp=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    assert file_hash(C2/'CONT02_DELIVERY_MANIFEST.json')==inp['C2_manifest_sha256']
    for p,h in inp['C2_files'].items():assert file_hash(C2/p)==h,('C2',p)
    import checkpoint_finalize as previous
    previous.ROOT=C2;counts=previous.inherited_pins();assert counts==inp['historical_pin_counts']
    exp1=REPO/'DO_RESEARCH_REBOOT/EXP01_PHYSICAL_RESIDUAL_DISCOVERY'
    for p,h in inp['EXP01_root_entry_inputs'].items():assert file_hash(exp1/p)==h,('EXP01',p)
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head==inp['HEAD']=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
    sources,rows,provenance=collect();names={s['name'] for s in sources}
    checked=json.loads((ROOT/'ALL_NEW_SOURCE_VERIFICATION.json').read_text())
    assert len(checked)==17 and {z['source'] for z in checked}==names
    assert all(z['all_complete_intermediate_states_equal_by_exact_edge_and_fringe_induction'] and
               z['S_is_entire_full_physical_population'] and z['paired_closure'] for z in checked)
    ordered={}
    for z in rows.values():
        if 'ordered_accounting' in z:ordered[z['source']]=z['ordered_accounting']
    for p in ['LARGE_ORDERED_ACCOUNTING.json','EXTRA_ORDERED_ACCOUNTING.json']:
        z=json.loads((ROOT/p).read_text());zs=z if isinstance(z,list) else [z]
        for a in zs:ordered[a['source']]=a
    full_names={n for n,z in rows.items() if z['original_Pi_classification']}
    assert len(full_names)==13 and set(ordered)==full_names
    inventory=[]
    for s in sources:
        z=rows[s['name']];a=ordered.get(s['name'])
        cert=a['positive_old_periodic_certificate'] if a else z['G_periodic']
        assert cert and cert['eligible_periodic'] and cert['B_cyclic']<=10*s['A']
        if a:
            assert a['disjoint_assignment_verified'] and a['literal_requested_R_upper']==[]
            E=a['first_use_E_C'];own=a['ordered_original_assignments']['4_pre_A_path_old_g']
            assert {digest(d['rho']) for d in own}<={digest(d['rho']) for d in E['selected_original_gaps']}
            assert len(E['selected_original_gaps'])<=6*s['A']
        inventory.append({'source':s['name'],**provenance[s['name']],
            'population':len(s['initial_B']['children']),'operations':len(s['operations']),
            'A':s['A'],'Q_B':s['Q_B'],'full_original_Pi_classification':z['original_Pi_classification'],
            'original_R_star':z.get('original_R_star'),
            'ordered_original_assignment':a['ordered_original_assignments'] if a else None,
            'new_epoch_E_C':a['first_use_E_C'] if a else None,
            'literal_requested_R_upper':[],
            'final_residual_zero_reason':'Existing funded periodic certificate, not an unrun Pi oracle or a finite universal-coverage inference.',
            'positive_old_periodic_certificate':{k:v for k,v in cert.items() if k!='retained_original_operations'},
            'independent_full_state_verification':'ALL_NEW_SOURCE_VERIFICATION.json'})
    write('EXP04_SOURCE_WITNESSES.json',{'inherited_C2_archive':'../CONTINUATION_02_HARD_RESIDUAL_CONSERVATION/EXP04_SOURCE_WITNESSES.json',
        'inherited_C2_archive_sha256':file_hash(C2/'EXP04_SOURCE_WITNESSES.json'),
        'new_unique_complete_source_count':17,'new_unique_complete_sources':sources,
        'source_batches':[a for a,b in BATCHES],'historical_controls_not_counted_as_new':
            ['C02_private_h_stride3','mixed_p5_Gcopies2','DW_5_1_at31','DW_6_1_at31']})
    write('EXP04_RESIDUAL_INVENTORY.json',{'requested_R_upper':'Literal original R_star minus frozen carrier/skipped, original B prefixes, pre-A-path oldg, then unchanged hybrid.',
        'C':'Literal remainder after frozen and prefix, before own and hybrid.',
        'new_R_renew':'C minus (E(C) union hybrid) = R_upper minus E(C)',
        'optional_R_deep':'R_upper minus (E(C) union immediate_A_fringe_roots)',
        'optional_R_deep_wide':'R_deep minus preserved <=8-genuine-key B-return consumers',
        'primary_universal_bound_status':'OPEN','new_scoped_E_C_budget':'6A, contains former own-path class',
        'new_sources':inventory,'full_original_Pi_sources':13,'physical_only_sources':4,
        'all_cut_or_all_local_negative_certificate_claimed':False,
        'source_uniform_availability_inferred_from_finite_inventory':False})
    controls=json.loads((ROOT/'EPOCH_CONTROL_RESULTS.json').read_text())
    hall=[]
    for name,h,k,step in [('DW_5_1_at31',163,2,13),('DW_6_1_at31',323,3,25)]:
        row=next(r for r in controls if r['source']==name);graph=row['original_root_entry_R6_incidence']
        sole=[d for d,vs in graph['edges'].items() if json.loads(d)[0]==h and vs==[[h,step]]]
        assert len(sole)>=k
        hall.append({'source':name,'demand_original_rho':[json.loads(d) for d in sole[:k]],
            'ONLY_actual_root_entry_StepEv':[h,step],'Hall_demand_count':k,'resource_count':1,
            'refutes_root_entry_load':k-1,'scope':'Original EXP01 R6 incidence graph, not the new epoch graph.'})
    write('ROOT_ENTRY_HALL_AUDIT.json',{'exact_single_resource_Hall_sets':hall,
        'EXP01_original_flow_certificates_sha256':inp['EXP01_root_entry_inputs']['EXP01_INCIDENCE_CERTIFICATES.json'],
        'old_refutations_not_relaxed':True})
    obstruction=json.loads((ROOT/'EPOCH_OBSTRUCTION_CERTIFICATE.json').read_text())
    write('EXP04_PHYSICAL_LIFECYCLES.json',{'new_epoch_obstruction':obstruction,
        'rigid_packet_verification':json.loads((ROOT/'RIGID_PACKET_VERIFICATION.json').read_text()),
        'new_large_complete_trace':'LARGE_UPPER_TRACE.json','new_large_independent_Pi':'LARGE_INDEPENDENT_PI.json',
        'preserved_historical_lifecycles':'../CONTINUATION_02_HARD_RESIDUAL_CONSERVATION/EXP04_PHYSICAL_LIFECYCLES.json',
        'all_original_ownership_and_first_hits_unchanged':True})
    write('EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',{'new_geometry':'PROOF_LEDGER.md G',
        'strict_new_epoch_after_frozen_prefix':{'private193':'PRIVATE_ORDERED_ACCOUNTING.json','large769':'LARGE_ORDERED_ACCOUNTING.json'},
        'old_historical_last_loss_collision_preserved':True,
        'root_entry_Hall_audit':'ROOT_ENTRY_HALL_AUDIT.json',
        'no_global_ancestry_mass_Lipschitz_or_repair_supply_assumed':True,
        'B_retargeting_without_new_relation_recreation':'DW5 g34->19 persists until parent179,2; actual histories saved in EPOCH_OBSTRUCTION_CERTIFICATE.json'})
    write('EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',{'analytic_proof':'PROOF_LEDGER.md E,F1',
        'first_use_parent_load_per_actual_A_bit':1,'first_use_gap_load_per_actual_A_bit':3,
        'actual_bits_per_A_StepEv_at_most':2,'new_epoch_A_coefficient':6,
        'fringe_strict_attachment_gap_load_per_A_bit':3,'fringe_target_children_gap_load_per_actual_A_StepEv':6,
        'optional_fringe_A_coefficient':12,'small_return_A_coefficient':42,
        'optimized_Q_coefficients':{'renew':'47+48 C_seq+102 C_DF','deep':'59+48 C_seq+102 C_DF','deep_wide':'101+48 C_seq+102 C_DF'},
        'requested_target_partial_coefficients':{'renew':6,'deep':18,'deep_wide':60},
        'later_parent_packet_overlap_bound':'OPEN','ownership_transfers_are_not_physical_credit':True})
    resources=[{'file':p.name,**json.loads(p.read_text())} for p in sorted(ROOT.glob('RESOURCE_*.json'))]
    cpu=sum(z['process_CPU_seconds'] for z in resources);peak=max(z['memory']['peak_working_set_bytes'] for z in resources)
    assert cpu<1000 and peak<3*1024**3
    assert len(sources)<=24 and max(len(s['operations']) for s in sources)<=120000
    write('EXP04_EXPERIMENT_LOG.json',{'measured_research_CPU_seconds':cpu,'includes_failed_initial_preflight':True,
        'planning_CPU_allocation':1000,'hard_host_quota_observed':False,
        'unmetered':'short inspections, ad-hoc metadata/path checks, report authoring and final index hashing',
        'research_receipt_missing':False,'peak_observed_working_set_bytes':peak,'working_set_aim_bytes':3*1024**3,
        'new_unique_complete_sources':17,'full_original_Pi_classified_sources':13,'physical_only_sources':4,
        'largest_new_population':max(len(s['initial_B']['children']) for s in sources),
        'longest_new_operation_word':max(len(s['operations']) for s in sources),
        'resources':resources,'result':'B. New scoped conservation theorem','universal_K_proved':False})
    large=json.loads((ROOT/'LARGE_INDEPENDENT_PI.json').read_text())
    assert large['complete_immutable_primitive_rotations']==15924 and len(large['independently_reconstructed_all_original_U'])==110
    p=json.loads((ROOT/'PRIVATE_ORDERED_ACCOUNTING.json').read_text());l=json.loads((ROOT/'LARGE_ORDERED_ACCOUNTING.json').read_text())
    assert len(p['strict_new_E_C_minus_own'])==1 and len(l['strict_new_E_C_minus_own'])==3
    assert 47==35+6+6 and 59==47+12 and 101==59+42 and 60==6+12+42
    required=['EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_THEOREM_LEDGER.md','EXP04_COUNTEREXAMPLE_LEDGER.md',
        'EXP04_RESIDUAL_INVENTORY.json','EXP04_PHYSICAL_LIFECYCLES.json','EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',
        'EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json','EXP04_SOURCE_WITNESSES.json','EXP04_EXPERIMENT_LOG.json',
        'EXP04_REPRODUCTION.md','EXP04_FINAL_VERDICT.md']
    assert all((ROOT/p).exists() for p in required)
    write('FINAL_VERIFICATION.json',{'HEAD':head,'branch':branch,'tracked_changes':[],
        'C2_files_unchanged':109,'historical_pin_counts':counts,'EXP01_additional_pin_count':len(inp['EXP01_root_entry_inputs']),
        'new_sources_independently_full_state_verified':17,'new_full_original_Pi_sources':13,
        'new_large_independent_primitive_SET_Pi_U':{'rotations':15924,'U':110},
        'independent_epoch_obstruction_primitives':obstruction['independently_verified_primitive_rotations'],
        'strict_epoch_enlargement_after_frozen_prefix':{'private193_original_gaps':1,'large769_original_gaps':3},
        'all_required_deliverables_present':True,'all_new_Python_ASTs_valid':True,
        'measured_CPU_seconds':cpu,'result':'B. New scoped conservation theorem','primary_unrestricted_conservation':'OPEN',
        'qualification':'same-agent analytic proofs and independent program checks; no external/formal/complete-DO audit'})
    hashes={p.relative_to(ROOT).as_posix():file_hash(p) for p in sorted(ROOT.rglob('*'))
            if p.is_file() and p.name!='CONT03_DELIVERY_MANIFEST.json'}
    write('CONT03_DELIVERY_MANIFEST.json',{'HEAD':head,'branch':branch,'files':hashes,
        'required_deliverables':required,'historical_pin_counts':counts,'excluded_self':'CONT03_DELIVERY_MANIFEST.json',
        'result':'B. New scoped conservation theorem','unrestricted_R_upper_O_A_status':'OPEN',
        'new_main_partial_bound':'R_upper<=6A+R_renew; unchanged Q coefficient47+48 C_seq+102 C_DF',
        'optional_deep_wide_bound':'R_upper<=60A+R_deep_wide; Q coefficient101+48 C_seq+102 C_DF'})
    print('PASS C3 delivery',len(hashes),'artifacts;17 sources;13 original Pi; measured CPU',cpu,
          '; old checkpoints unchanged; Outcome B, universal objective OPEN',flush=True)
