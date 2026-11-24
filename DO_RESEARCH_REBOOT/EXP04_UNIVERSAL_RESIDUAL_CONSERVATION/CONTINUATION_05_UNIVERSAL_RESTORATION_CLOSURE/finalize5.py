from stage5 import *
import ast

REQUIRED=[
 'UNIVERSAL_THEOREM_TARGET.md','RESTORATION_BATCH_PROOF.md','SAME_SIDE_CONSERVATION.md',
 'OPPOSITE_SIDE_CONSERVATION.md','GLOBAL_A_WORK_ACCOUNTING.md','PACKET_OVERFLOW_PROOF.md',
 'DIRECT_CD_ALTERNATIVE.md','COUNTEREXAMPLE_LEDGER.md','SOURCE_WITNESSES.json',
 'INDEPENDENT_VERIFICATION.md','DO_REDUCTION_AUDIT.md','PROOF_LEDGER.md',
 'EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_REPRODUCTION.md']

if __name__=='__main__':
    cpu=time.process_time();wall=time.perf_counter()
    inp=load(ROOT/'INPUT_MANIFEST.json');pinned=preserve()
    assert all(inp[k]==v for k,v in pinned.items())
    for p,h in inp['additional_file_hashes'].items():assert filehash(REPO/p)==h,p
    for p in REQUIRED:assert (ROOT/p).is_file(),p
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
    ss=load(ROOT/'SOURCE_WITNESSES.json')
    scr=load(ROOT/'PHYSICAL_SCREENS.json');v=load(ROOT/'INDEPENDENT_RESULTS.json')
    assert len(ss)==len(scr)==len(v)==6
    for s,a,b in zip(ss,scr,v):
        assert a['source']==b['source']==s['name']
        assert a['source_sha256']==b['source_sha256']==digest(s)
        assert a['genuine_support']==a['population']==len(s['initial_B']['children'])
        assert a['raw_periodic_cost']<=10*a['A']
        assert a['old_periodic_paid'] and a['prescribed_overflow']==0
        assert s['initial_A']==s['closing_A'] and s['initial_B']==s['closing_B']
    measured_ops=sum(x['operations'] for x in scr);assert measured_ops==16267
    pi=[z for z in v if z['full_original_Pi']];assert len(pi)==5
    bits=sum(z['immutable_primitive_check']['complete_immutable_primitive_rotations'] for z in pi)
    us=sum(z['original_U'] for z in pi)
    cohorts=sum(z['independent_cohort_R6_check']['cohort_count'] for z in pi)
    pairs=sum(len(z['independent_cohort_R6_check']['independently_recomputed_all_original_pairs']) for z in pi)
    assert (bits,us,cohorts,pairs)==(13273,290,194,96)
    large=v[2]
    assert not large['full_original_Pi'] and 'original_R_star' not in large
    assert large['reused_count']==128 and large['minimum_local_causal_span_congestion']==128
    assert large['only_A_StepEv_in_all_these_causal_spans']==['A',2,1]
    assert large['B_ancestry_gains_between_B_phases']==0
    assert v[3]['counted_gain_mass_lower_bound']==49
    assert len(v[4]['verified_long_strict_chain'])==16
    assert v[5]['critical_restorer_diagnostic']['classification']=='silent_restoration'
    assert v[5]['restorer_and_consumer_in_U']==[True,True]
    forest=load(ROOT/'LAST_PROMOTION_FORESTS.json')
    mass=next(z for z in forest if 'mass' in z['source'])
    assert any(z['predecessor']==[140,2] and z['children']==[[142,1],[148,2]] for z in mass['overlapping_child_frames'])
    ch=load(ROOT/'CHALLENGE_RESULTS.json');assert len(ch)==11
    assert ch[-1]['additional_priced_classes']['restorer_old_hybrid_protected']==1
    co=load(ROOT/'COERCION_CHECK.json')
    assert co['ordered_pairs']==196 and co['maximum_macro_requests']<=13
    write('FINAL_VERIFICATION.json',{'principal_outcome':'C','global_target':'OPEN',
        'same_frozen_D_and_coefficient':True,'C04_and_transitive_preservation':pinned,
        'new_complete_sources':6,'new_full_Pi_sources':5,'new_physical_only_sources':1,
        'new_independently_checked_measured_operations':measured_ops,
        'new_independently_checked_primitives_for_Pi':bits,
        'original_U':us,'cohorts':cohorts,'adjacent_pairs':pairs,
        'principal_large_source':large['source'],'verified_local_span_load_lower_bound':128,
        'true_post_hybrid_overflow_found':False,
        'universal_emptiness_inferred_from_samples':False,
        'coercion_table_all_ordered_pairs':196,'conditional_DO_premise_discharged':False})
    write('CPU_finalization.json',{'stage':'finalization','completed':True,
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
        'memory':inherited.memory()})
    records=[{'file':p.name,**load(p)} for p in sorted(ROOT.glob('CPU_*.json'))]
    measured=sum(z['cpu_seconds'] for z in records)
    peak=max(z['memory']['peak_working_set_bytes'] for z in records)
    assert measured<=360 and peak<=2*(1<<30)
    write('RESOURCE_RECORD.json',{'timed_stage_receipts':records,'measured_stage_CPU_seconds':measured,
        'observed_process_peak_working_set_bytes':peak,'CPU_allocation_seconds':360,
        'observed_peak_aim_bytes':2*(1<<30),'new_source_cap':12,'test_population_cap':1025,
        'unmetered':'Imports before meters, short read-only inspections, prose authoring, tool overhead and final hash pass.',
        'not_a_host_quota_or_theorem_hypothesis':True})
    files={p.relative_to(ROOT).as_posix():filehash(p) for p in sorted(ROOT.rglob('*'))
           if p.is_file() and p.name!='CONT05_DELIVERY_MANIFEST.json'}
    write('CONT05_DELIVERY_MANIFEST.json',{'date':'2026-11-11','HEAD':pinned['HEAD'],'branch':pinned['branch'],
        'principal_outcome':'C','excluded_self':'CONT05_DELIVERY_MANIFEST.json','files':files})
    print('SEALED',len(files),'files; measured CPU',measured,'peak bytes',peak,flush=True)
