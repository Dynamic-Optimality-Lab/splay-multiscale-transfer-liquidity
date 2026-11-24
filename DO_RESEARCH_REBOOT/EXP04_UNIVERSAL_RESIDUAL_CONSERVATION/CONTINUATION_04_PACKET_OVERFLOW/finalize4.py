from campaign4 import *
import ast

REQUIRED=['PROOF_LEDGER.md','COUNTEREXAMPLE_LEDGER.md','PACKET_OVERFLOW_INVENTORY.json',
    'PHYSICAL_PACKET_LIFECYCLES.json','AGGREGATE_CONSERVATION_EXPERIMENTS.json','SOURCE_WITNESSES.json',
    'ACCOUNTING_AUDIT.md','EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_REPRODUCTION.md']

if __name__=='__main__':
    start=time.process_time();wall=time.perf_counter()
    old=preservation()
    initial=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    assert old['checkpoints']==initial['checkpoints']
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head==initial['HEAD']=='6d532b2c795c0778f57d8023b23b5fedfc48b010'
    assert branch==initial['branch']=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    for name in REQUIRED:assert (ROOT/name).is_file(),name
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=p.name)
    sources=json.loads((ROOT/'SOURCE_WITNESSES.json').read_text())
    assert len(sources)==3 and len({s['name'] for s in sources})==3
    for s in sources:
        assert s['initial_A']==s['closing_A'] and s['initial_B']==s['closing_B']
        assert s['reaching_prefix']==[] and s['initial_A']==s['diagonal_initial']==s['initial_B']
    cert=json.loads((ROOT/'COUNTEREXAMPLE_CERTIFICATE.json').read_text())
    assert cert['source_sha256']==digest(sources[0])
    assert (cert['population'],cert['operations'],cert['A'],cert['Q_B'])==(1027,7176,15193,9464)
    packet=cert['critical_packet'];assert (packet['h'],packet['a_h'],packet['b_h'],packet['e_h'])==(2566,1,3,1)
    assert [p['id'] for p in packet['original_parents']]==[[2566,3],[2566,4],[2566,5]]
    assert [p['old_g'] for p in packet['original_parents']]==[20,68,260]
    assert sum(len(p['original_gaps']) for p in packet['original_parents'])==5
    assert cert['old_positive_periodic']['B_cyclic']==29484<=10*15193
    assert not cert['is_post_hybrid_escape'] and not cert['refutes_aggregate_conservation']
    pi=json.loads((ROOT/'NEW_INDEPENDENT_PI.json').read_text())
    co=json.loads((ROOT/'NEW_INDEPENDENT_R6.json').read_text())
    assert pi['complete_immutable_primitive_rotations']==47777
    assert len(pi['independently_reconstructed_all_original_U'])==528
    assert co['cohort_count']==369 and len(co['independently_recomputed_all_original_pairs'])==159
    trace=json.loads((ROOT/'TRACE_CHECK.json').read_text())
    assert trace['primitive_count']==47777 and trace['operation_boundary_count']==7176
    assert trace['event_sha256']==sources[0]['trace_hash']==cert['original_primitive_event_sha256']
    inventory=json.loads((ROOT/'PACKET_OVERFLOW_INVENTORY.json').read_text())
    assert len(inventory['sources'])==3
    assert all(z['sum_e_h']==0 and z['R_overflow']==[] for z in inventory['sources'])
    verified=json.loads((ROOT/'WIDTH_VERIFICATION.json').read_text())
    assert len(verified)==2 and all(z['physical']['paired_closure'] for z in verified)
    assert verified[0]['post_hybrid_quota']['sum_parent_overflow']==0
    assert verified[0]['prehybrid_original_R_star_quota']['sum_parent_overflow']==1
    part=verified[0]['literal_partition'];ids=[digest(e['rho']) for block in part.values() for e in block]
    assert len(ids)==len(set(ids))==40
    sc=json.loads((ROOT/'STRUCTURAL_CHECKS.json').read_text())
    assert sc['new_large_spine_control']['independent_physical']['paired_closure']
    assert len(sc['historical_DH_controls'])==2
    failure=json.loads((ROOT/'FAILUREMODE_CHECKS.json').read_text())
    assert len(failure['historical_full_source_controls'])==3
    assert failure['root_coupling_counterexample']['pointwise_suffix']['A']==1
    batch=json.loads((ROOT/'SIMULTANEOUS_RECREATION_BATCH.json').read_text())
    assert batch['small_full_tree_orientation_checks']==4081
    assert batch['necessary_B_ancestry_gains_to_reuse_all_three_at_one_later_KEEP']==2
    write('FINAL_VERIFICATION.json',{'principal_outcome':'C','primary_fixed_D_target':'OPEN',
        'new_obstruction_scope':cert['scope'],'independent_primitive_events':47777,
        'independent_U':528,'independent_cohorts':369,'independent_adjacent_pairs':159,
        'original_gap_assignment_disjoint_and_exhaustive':True,
        'frozen_coefficient':'47+48 C_seq+102 C_DF','quota_is_replacement_not_an_extra6A':True,
        'historical_preservation':old,'HEAD':head,'branch':branch,'tracked_files_unchanged':True,
        'complete_new_sources':3,'full_original_Pi_sources':1,'physical_only_sources':2,
        'universal_proof_from_empty_finite_inventory_claimed':False,
        'independent_selector_qualification':cert['selector_qualification']})
    # Final validation timing stops before administrative manifest hashing.
    write('RESOURCE_finalization.json',{'stage':'finalization','status':'completed',
        'process_CPU_seconds':time.process_time()-start,'wall_seconds':time.perf_counter()-wall,
        'memory':memory(),'qualification':'Final manifest hashing and tool/authoring overhead are not timed research phases.'})
    receipts=[]
    for p in sorted(ROOT.glob('RESOURCE_*.json')):
        z=json.loads(p.read_text(encoding='utf-8-sig'))
        if 'stage' in z:receipts.append({'file':p.name,**z})
    measured=sum(z['process_CPU_seconds'] for z in receipts if z.get('process_CPU_seconds') is not None)
    upper=sum(z.get('conservative_CPU_upper_bound_seconds',0) for z in receipts if z.get('process_CPU_seconds') is None)
    peak=max(z.get('memory',{}).get('peak_working_set_bytes',0) for z in receipts)
    allocation=json.loads((ROOT/'RESOURCE_REVIEW.json').read_text())
    assert measured+upper<=allocation['reviewed_research_CPU_seconds'],(measured,upper)
    assert peak<=allocation['memory_aim_bytes'],peak
    write('RESOURCE_RECORD.json',{'receipts':receipts,'measured_research_stage_CPU_seconds':measured,
        'interrupted_stage_conservative_CPU_upper_bound_seconds':upper,
        'measured_plus_interrupted_stage_upper_bound_seconds':measured+upper,
        'reviewed_research_CPU_allocation_seconds':allocation['reviewed_research_CPU_seconds'],
        'peak_observed_process_working_set_bytes':peak,
        'is_exact_total_campaign_CPU':False,
        'additional_unmetered_costs':'Initial pre-Meter import-alias failure(tool wall1.93s), Python startup/imports, short inspections, report authoring, tool/shell overhead and final manifest hashing; see CORRECTIONS_AND_LIMITS.md.',
        'hard_host_quota_claimed':False})
    files={p.relative_to(ROOT).as_posix():file_hash(p) for p in sorted(ROOT.rglob('*'))
        if p.is_file() and p.name!='CONT04_DELIVERY_MANIFEST.json'}
    write('CONT04_DELIVERY_MANIFEST.json',{'date':'2026-11-11','HEAD':head,'branch':branch,
        'principal_outcome':'C','excluded_self':'CONT04_DELIVERY_MANIFEST.json','files':files})
    print('SEALED',len(files),'files; measured CPU',measured,'plus interrupted bound',upper,
        '; principal C prehybrid obstruction; universal bound OPEN',flush=True)
