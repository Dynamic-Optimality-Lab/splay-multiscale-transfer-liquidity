from base7 import *
from independent7 import full_physical,elision_check
from independent6 import original_predecessors,local_prices
from model0 import prefix_check
from gate1 import packets
from rn1_audit5 import audit as old_predecessors
from workload7 import canonical_edges,paths_from_edges,path_workload
from rooted7 import rooted_test
from global7 import fresh_sources,root_account
from catalog7 import known_inputs

RESULT='E — EXACT GLOBAL COMPARISON REFUTATION'
REQUIRED=['M1_CONT07_THEOREM_TARGET.md','CANONICAL_PF_COMPARISON_ENVELOPE.md','GLOBAL_NESTED_PATH_CONSTRUCTION.md',
 'SHARED_INITIALIZATION_THEOREM.md','MONOTONE_SCAN_CONSERVATION.md','RESIDUAL_SENSITIVE_PATH_SELECTION.md',
 'GLOBAL_CROSS_COLUMN_OVERLAP.md','NESTED_HYBRID_EXCLUSION.md','PF_GLOBAL_COMPARISON_THEOREM.md',
 'PROMOTION_MEDIATED_COMPARISON_BOUNDARY.md','GLOBAL_COMPARISON_COUNTEREXAMPLES.md',
 'M1_CONT07_INDEPENDENT_VERIFICATION.md','M1_CONT07_ACCOUNTING_AUDIT.md','M1_CONT07_TO_M2_M3_INTERFACE.md',
 'M1_CONT07_PROOF_LEDGER.md','M1_CONT07_FINAL_REPORT.md','M1_CONT07_REPRODUCTION.md']

def inventory():return {p.relative_to(ROOT).as_posix():hfile(p) for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def audit():
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    for name in REQUIRED:assert (ROOT/name).is_file(),name
    for q in ROOT.glob('*.py'):ast.parse(q.read_text(encoding='utf-8-sig'),filename=q.name)
    ss=fresh_sources();assert len(ss)==10 and len({digest(s) for s in ss})==10
    independent=[];fresh=[];summary=[];merge=None;fresh_paths=[];newrn=[]
    for i,s in enumerate(ss):
        paths={k:ROOT/f'FRESH_{k}_{i:02}.json' for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH','ORDERED','REDUCTION','RENEWAL','RESULT')}
        p,f,w,an,b,acc,red,rn,row=(load(paths[k]) for k in paths)
        assert digest(s)==row['source_sha256']==p['source_sha256']==b['source_sha256']==acc['source_sha256']
        assert prefix_check(s)==row['prefix'];phy=full_physical(s,p)
        assert (phy['A'],phy['Q_B'],phy['primitives'])==(row['A'],row['Q_B'],row['primitives'])
        assert row['A']==an['A']==b['A']==acc['A'] and row['Q_B']==an['Q_B']==b['Q_B']
        assert an['primitive_edges_and_all_complete_boundaries_verified'] and f['root_donors_injective'] and f['vertex_count']==row['Q_B']
        assert b['original_SET_and_sign_checks']==row['primitives'] and not w['R_overflow'] and not any(z['w'] for z in w['vertices'])
        star=acc['native_original_R_star'];r6={digest(e['rho']):e for e in b['original_R6']};ids={digest(e['rho']) for e in star}
        assert star==row['original_R_star'] and len(ids)==len(star) and ids<=set(r6)
        used=[]
        for cls,pool in acc['disjoint_original_assignments'].items():
            for e in pool:assert e['original_parent']==r6[digest(e['rho'])]['parent'];used.append(digest(e['rho']))
        assert len(used)==len(set(used))==len(star) and set(used)==ids
        assert {k:len(v) for k,v in acc['disjoint_original_assignments'].items()}==row['assigned_counts']
        assert not acc['exact_D'] and not red['literal_S_UU'] and red['sum_z_h']==0 and row['actual_S_UU']==[]
        assert digest(packets(s,p,b,f,an,acc['exact_D'],star))==digest(red)
        assert digest(old_predecessors(s,p,f,b,an,acc))==digest(rn)
        original=original_predecessors(p,acc,rn);edges=canonical_edges(s,p,acc);assert digest(edges)==digest(row['canonical_edges'])
        paths0=paths_from_edges(edges);details=[path_workload(s,p,path) for path in paths0]
        assert digest(details)==digest(row['maximal_PF_paths'])
        assert sum(z['M_PF'] for z in details)==row['M_PF']
        union=sorted({k for path in details for d in path['full_initial_domains'] for k in d});assert union==row['distinct_domain_key_union']
        assert row['KEY_UNION_2_refuted']==(row['M_PF']>2*len(union))
        roots=root_account(p,acc,edges,details,row['A'],row['Q_B'])
        root_tests=[rooted_test(p,path) for path in details]
        if 'physical_kernel' in row:
            k=row['physical_kernel'];u=tuple(k['u']);v=tuple(k['v']);physical=path_workload(s,p,[u,v])
            assert digest(physical)==digest(k['full_physical_PF_path_test'])
            assert physical['merged_inside_shadow']['full_g_component_failure'] and not physical['merged_inside_shadow']['all_original_old_g_matched']
            root_tests.append(rooted_test(p,physical))
            if i==6:
                assert k['u_U'] and k['v_U'] and not k['v_original_R6'] and not k['u_C_old'] and not k['v_C_old']
                Uv=b['U'][str(v)];creator=tuple(Uv['creator']);assert Uv['output_kind']=='parent' and not Uv['exposed'] and str(creator) in b['U']
                assert next(d for d in an['C_fringe_depths'] if tuple(d['vertex'])==v)['distance']==1
                merge={'candidate':'Broader MERGE0 physical PF/U/silent-component preservation; canonical C_old specialization is NOT refuted.',
                    'complete_original_source':s,'source_sha256':digest(s),'physical_kernel':k,'consumer_U':Uv,'creator_U':b['U'][str(creator)],
                    'literal_R6_at_consumer':[],'literal_C_old_at_consumer':[],'actual_S_PF':[],
                    'scope':'Exact protected U/O, unacquired-sibling physical counterexample; shallow and no original R6/C_old demand.'}
        if 'epochless' in row:
            z=row['epochless'];g=z['old_g'];assert len(z['all_double_column'])==1 and not z['A_reset_or_promotion_ids']
            assert z['forest_entries'][0]['type']=='P' and not z['canonical_C_old_uses']
            assert not any(e['actor']=='A' and (e['pivot']==g or e['promoted']==g) for e in p['events'])
            assert row['A']==9 and row['Q_B']==8 and g not in phy['original_genuine_M'] and g in phy['original_S']
        if 'period_copies' in s:
            T=s['period_copies'];assert row['A']==1082*T and row['Q_B']==274*T and row['M_PF']==28*T and row['PF_path_count']==T
        assert row['raw_periodic_cost']==acc['raw_periodic_certificate']<=10*row['A']
        newrn.append(rn);fresh_paths.extend(details)
        independent.append({'source':s['name'],'physical':phy,'independent_original_predecessors':original,'root_account':roots,
            'rooted_shadow_checks':len(root_tests),'all_actual_residuals_empty_by_existing_periodic_case':True})
        meta={k:row[k] for k in ('source','index','population','operations','A','Q_B','primitives','raw_periodic_cost','C_old_gaps','PF_path_count','M_PF','assigned_counts')}
        meta.update(actual_S_PF=[],actual_S_PM=[],KEY_UNION_2_refuted=row['KEY_UNION_2_refuted'])
        if 'physical_kernel' in row:meta['kernel_predicates']={k:row['physical_kernel'][k] for k in ('u','v','u_U','v_U','v_sigma','u_C_old','v_C_old','v_original_R6')}
        if 'epochless' in row:meta['epochless']=row['epochless']
        summary.append(meta)
        fresh.append({'source':s,'source_sha256':digest(s),'fresh_index':i,'certificates':{k:{'file':q.name,'sha256':hfile(q)} for k,q in paths.items()},
            'native_scope':'Full original U/all-pair/R6 independently matched, native R_*, exact original frozen accounting, physical/immutable and independent edge checks.'})
        del p,f,w,an,b,acc,red,rn,row;gc.collect();print('PASS independent complete source',i,s['name'],flush=True)
    assert merge is not None
    old=load(ROOT/'INHERITED_PATH_WORKLOADS.json');assert len(old)==48 and len(known_inputs())==48
    assert len(load(ROOT/'NON_U_SCAN_BUDGET_AUDIT.json'))==58
    for z in load(ROOT/'NON_U_SCAN_BUDGET_AUDIT.json'):
        assert z['M_hit_non_U']<=2*z['original_non_U_doubles']<=z['proved_non_U_scan_budget_24A']
        assert z['maximum_hits_per_original_double']<=2
    globals0=load(ROOT/'GLOBAL_ROOT_AND_SCAN_AUDIT.json');assert len(globals0)==22
    for z in globals0:
        a=z['global_original_root_and_scan_account'];assert a['maximum_A_bit_load']<=2 and a['maximum_A_StepEv_root_load']<=4
        assert z['M_component_rooted']==z['M_inside']+sum(t['root_atoms'] for t in a['root_origins'])
        assert z['M_hit']==a['M_hit']<=a['unpriced_B_bit_budget_2Q']
    graphs=load(ROOT/'COMPLETE_PHYSICAL_GRAPH_INDEX.json');refs=load(ROOT/'ALL_COMPLETE_CONTROL_REFERENCES.json');assert len(graphs)==len(refs)==120
    assert len({digest(e['source']) for e in refs})==120
    total_vertices=total_phys=0
    for i,(entry,ref) in enumerate(zip(graphs,refs)):
        assert digest(ref['source'])==entry['source_sha256'];assert hfile(ROOT/entry['file'])==entry['sha256']
        g=load(ROOT/entry['file']);assert g['source_sha256']==entry['source_sha256'] and len(g['all_original_B_double_forest'])==g['Q_B']
        assert g['full_root_injection_checked'] and g['binary_outdegree_checked'] and g['real_A_bits']<=2*g['A']
        if ref.get('physical') and ref.get('physical_sha256'):assert hfile(ref['physical'])==ref['physical_sha256']
        total_vertices+=len(g['all_original_B_double_forest']);total_phys+=len(g['all_physical_index_noncheap_epoch_renewals'])
    assert graphs[-2]['epochless_old_g_columns']==[4] and graphs[-1]['epochless_old_g_columns']==[2]
    probe=load(ROOT/'MERGE_PROBE_SUMMARY.json');assert probe['intervals']==227 and not probe['component_failures'] and not probe['full_C_old_candidate_refuted']
    elision=elision_check();key=load(ROOT/'EXACT_GLOBAL_KEY_UNION_REFUTATION.json')
    assert key['M_PF']==112>key['candidate_bound']==56 and len(key['union_physical_keys'])==28 and key['complete_original_source']==ss[5]
    local=[]
    for i,price in ((1,27),(4,211)):
        s=load(C6/'FRESH_SOURCE_CATALOG.json')[i];p=load(C6/f'FRESH_PHYS_{i:02}.json');geo=load(C6/f'FRESH_NESTED_{i:02}.json')
        z=local_prices(s,p,geo);assert all(t['raw']['D']==price and t['threshold_5A']==10 for t in z)
        local.append({'source':s['name'],'source_sha256':digest(s),'independent_preserved_original_local_checks':z});del p;gc.collect()
    write('INDEPENDENT_FRESH_VERIFICATION.json',independent);write('FRESH_RESULTS_SUMMARY.json',summary)
    write('INDEPENDENT_ELISION_VERIFICATION.json',elision);write('PRESERVED_55_535_LOCAL_VERIFICATION.json',local)
    write('EXACT_PROTECTED_PHYSICAL_MERGE_REFUTATION.json',merge)
    write('CANONICAL_ACCOUNTING_INVENTORY.json',{'inherited_complete_native_sources':48,'fresh_complete_native_sources':10,'combined_native_sources':58,
        'inherited_workload_file':'INHERITED_PATH_WORKLOADS.json','fresh_original_predecessor_records':newrn,
        'unknown_historical_native_scopes_retained':True})
    inherited=[{'source':e['source']['name'],'source_sha256':digest(e['source']),'complete_source_catalog':'ALL_COMPLETE_CONTROL_REFERENCES.json','catalog_index':i,
        'physical':e.get('physical'),'origin':e['origin'],'physical_graph':graphs[i]['file'],
        'scope':'Sealed original native/expansion scope inherited; no new full long native R_* classification.'} for i,e in enumerate(refs[:110])]
    write('M1_CONT07_SOURCE_WITNESSES.json',{'principal_result':RESULT,'fresh_complete_original_sources':fresh,'inherited_complete_sources':inherited,
        'complete_physical_graphs':120,'authoritative_original_C_old_accounting_sources':58,'fresh_full_native_replays':10,
        'principal_exact_refutations':['EXACT_GLOBAL_KEY_UNION_REFUTATION.json','EXACT_PAID_HIT_ELISION_REFUTATION.json'],
        'broader_physical_counterexample':'EXACT_PROTECTED_PHYSICAL_MERGE_REFUTATION.json','canonical_MERGE0_refuted':False,
        'main_M_PF_A_bound_refuted':False,'positive_actual_S_PF_certified':False,'finite_coverage_is_universal_proof':False,
        'long_native_scope':'Original complete lossless physical/event expansion and G/H proofs only; unrun full native predicates remain unrun.'})
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    return {'principal_result':RESULT,'full_M1':'OPEN','universal_PF_conservation':'OPEN','universal_K_PF':None,'universal_K_UU':None,'approved_completed_transfer_X':None,
        'main_M_PF_A_bound':'Neither proved nor refuted','preserved_paid_coefficient':'161+48 C_seq+102 C_DF',
        'optional_root_only_coefficient':'161+60 C_seq+102 C_DF with unpriced selected interior/PM roots',
        'optional_root_plus_nonU_scan_coefficient':'161+132 C_seq+102 C_DF with unpriced selected U-scan/padding/PM roots',
        'actual_positive_S_PF_certified':False,'new_actual_S_UU_gaps':0,'fresh_complete_native_replays':10,'complete_physical_graphs':120,
        'original_B_double_vertices_in_graph_inventory':total_vertices,'physical_noncheap_entries_in_graph_inventory':total_phys,
        'authoritative_original_C_old_accounting_sources':58,
        'new_source_uniform_results':['Exact canonical stem/hit/padding decomposition','Component-rooted one-sided envelope removes exterior stem',
            'Safe actual-hard selection/late initialization coverage envelope','A-origin roots<=4A and PM roots<=2 unweighted P entries',
            'Inside-hit injection<=2Q_B and original non-U-container scan class<=24A'],
        'exact_refutations':['KEY-UNION-2 on a complete native canonical source112>56','ELIDE-FE on original39-key canonical path',
            'Broader physical/U MERGE0 fails; canonical C_old specialization remains unrefuted'],
        'new_epochless_physical_control':'5-key closed source/reflection, no A reset of its nonempty old-g column; actual entry is P and has no C_old gap',
        'first_missing_implication':'Global A-work price or complete hybrid contradiction for actual selected interior-U scan/support-padding and PM-origin roots, including cross-column reuse; separate PM residual price still open.',
        'verification_scope':'Same-agent component proofs and independent implementations; no external reviewer/formal kernel.',
        'preservation':load(ROOT/'INPUT_MANIFEST.json')}

def verify_only():
    m=load(ROOT/MANIFEST);assert inventory()==m['files'],'Exact delivery inventory mismatch'
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    assert m['principal_result']==RESULT and m['full_M1']=='OPEN'
    print('PASS read-only C7 delivery and all inherited seals/HEAD/branch/tracked bytes;',len(m['files']),'files; E, full M1/PF conservation OPEN.',flush=True)

def seal():
    unsealed();cpu0=time.process_time();wall0=time.perf_counter();ok=False;name='CPU_finalization.json';i=2
    while (ROOT/name).exists():name=f'CPU_finalization_{i}.json';i+=1
    try:z=audit();write('FINAL_VERIFICATION.json',z);ok=True
    finally:write(name,{'completed':ok,'cpu_seconds':time.process_time()-cpu0,'wall_seconds':time.perf_counter()-wall0,'memory':memory(),
        'scope':'Full independent fresh original-event/SET/frame/closure/accounting/comparison checks and all transitive preservation; imports excluded.'})
    receipts={q.name:load(q) for q in ROOT.glob('CPU_*.json')};failed=[n for n,z in receipts.items() if not z['completed']];assert not failed,failed
    cpu=sum(z['cpu_seconds'] for z in receipts.values());peak=max(z['memory']['peak_working_set_bytes'] for z in receipts.values())
    assert cpu<=1800 and peak<2*1024**3
    write('RESOURCE_RECORD.json',{'allocation':{'measured_script_CPU_seconds':1800,'unique_fresh_source_cap':10,'initial_fresh_cap':8,
        'extension':'EPOCHLESS_ADDENDUM.md before the two extra5-key constructions','population_cap':1027,'operation_cap':40000,'per_process_peak_working_set_aim_bytes':2*1024**3},
        'measured_script_CPU_seconds_total':cpu,'maximum_measured_peak_working_set_bytes':peak,'receipts':receipts,
        'unique_fresh_complete_sources':10,'full_fresh_native_replays':10,'constructor_outputs_including_duplicate':12,
        'duplicate_semantic_run':'Protected synthesis regenerated once to correct A-return diagnostic metadata before native classification; identical physical source states/word; both receipts retained.',
        'max_fresh_population':55,'max_fresh_operations':3484,'failed_semantic_runs':failed,
        'failed_survivor_attempts':'All10 targeted sources are periodically paid; no actual positive PF residual. Protected merge kernel reaches U/O but lacks deep R6/C_old eligibility.',
        'administrative_failures':'Read-only guessed filename lookup and rejected atomic patch contexts corrected; no original data/predicates changed.',
        'unmetered':['Imports before meters','Read-only searches/inspections','Mathematical proof reasoning and prose/patch writing','Resource/manifest serialization and read-only post-seal verification'],
        'measurement_scope':'Measured script CPU only, not total reasoning CPU/session wall time. All semantic probes/classifications/rechecks include receipts.',
        'historical_writes':0,'Git_mutations':0,'subagents':0,'installations':0,'external_reviewers':0})
    write(MANIFEST,{'principal_result':RESULT,'full_M1':'OPEN','universal_PF_conservation':'OPEN','format':'Exact SHA256 relative inventory excluding only this manifest.',
        'C6_manifest_sha256':hfile(C6/'M1_CONT06_DELIVERY_MANIFEST.json'),'files':inventory()})
    print('PASS sealed',len(inventory()),'files;',round(cpu,3),'measured script CPU seconds; E, main PF/M1 A bound OPEN.',flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:assert not sys.argv[1:];seal()
