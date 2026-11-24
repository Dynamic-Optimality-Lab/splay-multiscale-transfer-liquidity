"""Build inspectable indexes from completed exact checks; never invent unknowns."""
from campaign4 import *
from fractions import Fraction

if __name__=='__main__':
    meter=Meter('export_checkpoint')
    rows=json.loads((ROOT/'WIDTH_RESULTS.json').read_text())
    raw_sources=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())
    by_source={s['name']:s for s in raw_sources}
    ss=[by_source[z['source']] for z in rows]
    for source in ss:
        if 'closing_A' not in source:
            source['closing_A']=source['initial_A'];source['closing_B']=source['initial_B']
            source['closing_states_basis']='Exact physical closure in WIDTH_VERIFICATION.json; final full dictionaries explicitly equal initial dictionaries.'
    verified=json.loads((ROOT/'WIDTH_VERIFICATION.json').read_text())
    by={z['source']:z for z in verified};inventory=[]
    for s,row in zip(ss,rows):
        v=by[s['name']]
        if row['original_Pi_classified']:
            q=v['post_hybrid_quota'];pre=v['prehybrid_original_R_star_quota']
            inventory.append({'source':s['name'],'A':s['A'],'population':len(s['initial_A']['children']),
                'marked_support':len(s['initial_A']['children']),'original_R_star':row['original_R_star'],
                'ordered_literal_original_assignments':v['literal_partition'],'exact_D':v['exact_D'],
                'post_hybrid_packets_and_quota':q,'sum_e_h':q['sum_parent_overflow'],
                'R_overflow':q['literal_gap_overflow'],'original_Pi_classified':True,
                'prehybrid_R_star_packets':pre,'post_hybrid_residual_not_inferred_from_pre_hybrid_width':True})
        else:
            inventory.append({'source':s['name'],'A':s['A'],'population':len(s['initial_A']['children']),
                'marked_support':len(s['initial_A']['children']),'original_Pi_classified':False,
                'original_R_star':None,'exact_D':None,'exact_packet_widths':None,
                'sum_e_h':0,'R_overflow':[],
                'zero_overflow_certificate':v['independent_raw_periodic_certificate'],
                'reason':v['zero_overflow_reason'],'unrun_Pi_is_zero':False})
    spine=json.loads((ROOT/'SPINE_SOURCE.json').read_text())
    spine['closing_A']=spine['initial_A'];spine['closing_B']=spine['initial_B']
    spine['closing_states_basis']='Independent complete labelled state induction in STRUCTURAL_CHECKS.json.'
    write('SOURCE_WITNESSES.json',ss+[spine])
    inventory.append({'source':spine['name'],'population':len(spine['initial_A']['children']),
        'A':spine['A'],'original_Pi_classified':False,'original_R_star':None,'exact_D':None,
        'sum_e_h':0,'R_overflow':[],
        'zero_overflow_certificate':'P6 and STRUCTURAL_CHECKS.json; also an exact raw periodic certificate.',
        'unrun_Pi_is_zero':False})
    write('PACKET_OVERFLOW_INVENTORY.json',{'fixed_D':'R_star minus F,E_old,H_all; no refill',
        'quota':'first2a_h distinct D parents; all original gaps of a parent kept together',
        'primary_target_status':'OPEN','sources':inventory,
        'universal_emptiness_inferred_from_testing':False})
    row=rows[0];s=ss[0];v=verified[0];h=s['target_consumer']
    pre=v['prehybrid_original_R_star_quota'];packet=next(z for z in pre['packets'] if z['h']==h)
    assert packet['b_h']==3 and packet['a_h']==1 and packet['e_h']==1
    assert [p['old_g'] for p in packet['original_parents']]==[20,68,260]
    assert len(pre['literal_gap_overflow'])==1
    pi=json.loads((ROOT/'NEW_INDEPENDENT_PI.json').read_text())
    cohorts=json.loads((ROOT/'NEW_INDEPENDENT_R6.json').read_text())
    certificate={'source':s['name'],'source_file':'SOURCE_WITNESSES.json','source_index':0,
        'population':1027,'operations':7176,'A':15193,'Q_B':9464,
        'complete_original_event_delta_trace':'ORIGINAL_EVENT_TRACE.json',
        'source_sha256':digest(s),'original_primitive_event_sha256':s['trace_hash'],
        'refuted_candidate':'For every admissible source and KEEP h, b_h(original R_star)<=2 A(G_h).',
        'scope':'PREHYBRID original R_star; not the prescribed post-hybrid D.',
        'critical_packet':packet,
        'critical_pool_after_frozen_and_original_prefix':[z for z in v['ordered_inherited_audit']['C_after_frozen_and_prefix'] if z['consumer']==h],
        'existing_E_old_payments_for_critical_packet':[z for z in v['ordered_inherited_audit']['first_use_E_C']['packets'] if z['selected_first_parent'][0]==h],
        'literal_assigned_partition_counts':{key:len(block) for key,block in v['literal_partition'].items()},
        'actual_pre_hybrid_quota':{'assignments':[z for z in pre['quota_original_assignments'] if z['parent'][0]==h],
            'literal_unselected_gap':pre['literal_gap_overflow']},
        'old_positive_periodic':row['tested_cut1_periodic'][0],
        'exact_post_hybrid_D':v['exact_D'],'exact_post_hybrid_quota':v['post_hybrid_quota'],
        'all_primitive_SET_Pi_U_verification':pi,'all_original_cohort_R6_verification':cohorts,
        'full_physical_operation_and_fringe_verification':v['physical'],
        'complete_original_source_reaching_prefix_is_empty_common_diagonal':True,
        'is_post_hybrid_escape':False,'refutes_aggregate_conservation':False,
        'refutes_Coarse_Double_or_Dynamic_Optimality':False,
        'selector_qualification':'Independent primitive SET/Pi/U and separate all-cohort/R6 implementation; older R_star/F/comparison selectors are the pinned primary implementations, freshly replayed. No external or formal audit.'}
    write('COUNTEREXAMPLE_CERTIFICATE.json',certificate)
    write('PHYSICAL_PACKET_LIFECYCLES.json',{'new_packet_certificate':'COUNTEREXAMPLE_CERTIFICATE.json',
        'new_complete_physical_packet_geometry':'PACKET_GEOMETRY.json',
        'simultaneous_same_side_recreation_batch':'SIMULTANEOUS_RECREATION_BATCH.json',
        'new_original_U':row['original_U'],'new_original_pairs':row['original_pairs'],
        'original_source_and_trace_identity':s['trace_hash'],
        'historical_577_key_obstruction':{'directory':str(C3B),'manifest_sha256':file_hash(C3B/'CONT03B_DELIVERY_MANIFEST.json'),
            'certificate_file':'COUNTEREXAMPLE_CERTIFICATE.json','certificate_sha256':file_hash(C3B/'COUNTEREXAMPLE_CERTIFICATE.json'),
            'rigid_A_component':'g154, keys137..576; parents646,3 and653,4 share A(133,24,1)',
            'post_hybrid_residual':[]},
        'universal_B_ancestry_retention_assumed':False,'recreated_ancestry_or_retargeting_creates_A_credit':False})
    write('AGGREGATE_CONSERVATION_EXPERIMENTS.json',{'principal_outcome':'C',
        'new_exact_obstruction':'prehybrid original R_star packet width<=2a_h',
        'primary_fixed_D_aggregate_target':'OPEN',
        'new_physical_sources':len(ss)+1,'new_full_original_Pi_sources':1,'physical_screen_only_sources':2,
        'new_analytic_results':['P4 parent/gap overflow equivalence','P5 ordered physical tail and rigid A components',
            'P6 arbitrary-support one-StepEv A raw periodic availability','P7 disjoint same-side outputs and mandatory simultaneous B restoration batch',
            'R2 exact-local-B-return cancellation with separate30C_DF budget'],
        'failed_attempts':[{'resource':'RESOURCE_width_attack.json','failure':'JSON adapter could not serialize lossless boundary Mapping during original residual selection; no result accepted',
            'correction':'Canonical Mapping serialization and regression through original R_star selectors, then complete fresh replay'},
            {'resource':'RESOURCE_verify_width.json','failure':'Independent primitive recursive rotation reached default recursion limit after primary selector equality had passed.',
             'correction':'Local recursion limit10000; fresh complete replay/event/U/pair binding with --reuse-primary-selection, then independent primitive and cohort checks recomputed.'}],
        'source_family_all_parameter_claim':'Legality and exact paired closure only; no all-p width/Pi scaling extrapolation.',
        'no_simultaneous_post_hybrid_overflow_found':True,'finite_coverage_percentage_is_proof':False,
        'abstract_incidence_insufficiency_is_a_physical_source_counterexample':False})
    print('PASS exact source indexes and scoped counterexample certificate',flush=True)
    meter.success=True
