from base5 import *
from finalize3 import verify_physical
from residual0 import E_stream
from gate1 import packets

MANIFEST='M1_CONT05_DELIVERY_MANIFEST.json'
REQUIRED=['M1_CONT05_THEOREM_TARGET.md','NONCHEAP_FIRST_INDEX_REDUCTION.md','REPEATED_COLUMN_RENEWAL_GEOMETRY.md',
 'RENEWAL_PRIMITIVE_TRANSITIONS.md','RENEWAL_SURVIVOR_SIGNATURE.md','RENEWAL_CONSERVATION_THEOREM.md',
 'GLOBAL_RENEWAL_MULTIPLICITY.md','CYCLIC_RENEWAL_POTENTIAL.md','RENEWAL_RANK_HYBRID_COUPLING.md',
 'REPEATED_NONCHEAP_COUNTEREXAMPLES.md','M1_CONT05_INDEPENDENT_VERIFICATION.md','M1_CONT05_GLOBAL_ACCOUNTING.md',
 'M1_CONT05_TO_M2_M3_INTERFACE.md','M1_CONT05_PROOF_LEDGER.md','M1_CONT05_FINAL_REPORT.md','M1_CONT05_REPRODUCTION.md']

def inventory():return {p.relative_to(ROOT).as_posix():hfile(p) for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def audit():
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    for name in REQUIRED:assert (ROOT/name).is_file(),name
    for q in ROOT.glob('*.py'):ast.parse(q.read_text(encoding='utf-8-sig'),filename=q.name)
    fresh=[];new_reductions=[]
    for stem in ('NEW','RENEW','FRINGE'):
        ss=load(ROOT/f'{stem}_SOURCE_CATALOG.json');rows=load(ROOT/f'{stem}_RESULTS.json');assert len(ss)==len(rows)==(4 if stem=='RENEW' else 2)
        for i,(s,row) in enumerate(zip(ss,rows)):
            paths={k:ROOT/f'{stem}_{k}_{i:02}.json' for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH','ORDERED','REDUCTION','RENEWAL')}
            p,f,w,an,b,acc,red,rn=(load(paths[k]) for k in paths)
            assert digest(s)==row['source_sha256']==p['source_sha256']==b['source_sha256']==acc['source_sha256']
            phy=verify_physical(s,p);assert (phy['A'],phy['Q_B'],phy['primitives'])==(row['A'],row['Q_B'],row['primitives'])
            assert p['original_S']==p['original_genuine_M']==list(range(1,s['n']+1))
            assert f['root_donors_injective'] and f['vertex_count']==row['Q_B']
            assert an['primitive_edges_and_all_complete_boundaries_verified'] and b['original_SET_and_sign_checks']==row['primitives']
            assert w['R_overflow']==0 and all(q['w']==0 for q in w['vertices'])
            star=acc['native_original_R_star'];assert star==row['original_R_star']
            r6={digest(e['rho']):e for e in b['original_R6']};starids={digest(e['rho']) for e in star};assert len(starids)==len(star) and starids<=set(r6)
            used=[]
            for es in acc['disjoint_original_assignments'].values():
                for z in es:assert z['original_parent']==r6[digest(z['rho'])]['parent'];used.append(digest(z['rho']))
            assert len(used)==len(set(used))==len(star) and set(used)==starids
            assert not acc['disjoint_original_assignments']['overflow'] and acc['actual_S_UU']==0
            assert digest(packets(s,p,b,f,an,acc['exact_D'],star))==digest(red)
            assert not red['literal_S_UU'] and red['sum_z_h']==0
            assert {digest(e['rho']) for e in E_stream(p,acc['C_old'])}=={digest(e['rho']) for e in acc['E_old']}
            assert row['raw_periodic_cost']==acc['raw_periodic_certificate']<=10*row['A']
            for edge in rn['canonical_renewals']:
                assert edge['earlier_original_C_old_rhos'] and edge['later_original_C_old_rhos']
                assert edge['later_parent'][0]==edge['later_original_C_old_rhos'][0][0]
            new_reductions.append(rn)
            fresh.append({'source':s['name'],'source_sha256':digest(s),'catalog':f'{stem}_SOURCE_CATALOG.json','catalog_index':i,
                'population':s['n'],'operations':len(s['operations']),'A':row['A'],'Q_B':row['Q_B'],
                'creator':row['creator'],'critical':row['critical'],'original_R_star_gaps':len(star),
                'assigned_counts':row['assigned_counts'],'actual_D_gaps':len(acc['exact_D']),'literal_S_UU':[],
                'canonical_C_old_renewals':rn['canonical_renewals_count'],
                'certificates':{k:{'file':q.name,'sha256':hfile(q)} for k,q in paths.items()},
                'scope':'Full original mutable/immutable plus independent edge/Pi/U/cohort/R6 and native R_*; exact original accounting and no-H diagnostic kept separate.'})
            del p,f,w,an,b,acc,red;gc.collect()
    assert len(fresh)==8 and len({e['source_sha256'] for e in fresh})==8
    assert max(e['population'] for e in fresh)==107 and max(e['operations'] for e in fresh)==1591
    oldreduction=load(ROOT/'RN1_REDUCTION_AUDIT.json');assert len(oldreduction)==34
    allreduction=oldreduction+new_reductions
    write('CANONICAL_REDUCTION_INVENTORY.json',{'complete_original_accounting_audits':len(allreduction),
        'source_records':allreduction,'actual_posthybrid_survivor_certified':False})
    physical=load(ROOT/'PHYSICAL_RENEWAL_RESULTS_FINAL.json');refs=load(ROOT/'ALL_CONTROL_REFERENCES_FINAL.json')
    assert len(physical)==len(refs)==104
    assert len({z['source_sha256'] for z in physical})==104
    assert {z['source_sha256'] for z in physical}=={z['source_sha256'] for z in refs}
    inherited=[]
    for i,e in enumerate(refs):
        assert digest(e['source'])==e['source_sha256']
        if e.get('physical'):assert hfile(e['physical'])==e['physical_sha256']
        if not e['origin'].startswith('C5_'):
            inherited.append({'source':e['source']['name'],'source_sha256':e['source_sha256'],'full_source_reference':{'catalog':'ALL_CONTROL_REFERENCES_FINAL.json','index':i},
                'physical':e.get('physical'),'physical_sha256':e.get('physical_sha256'),'origin':e['origin'],
                'scope':'Pinned inherited complete physical/predicate scopes; long sources use their exact event/boundary expansion. No new full long native R_* run.'})
    assert len(inherited)==96
    counts=Counter();case=set()
    for z in physical:
        assert z['promotion_mediators_injective'] and len(z['mediator_bits'])==z['noncheap_renewal_counts'].get('promotion_mediated',0)
        assert len({tuple(q) for q in z['mediator_bits']})==len(z['mediator_bits'])
        phi=z['ownership_potential'];assert phi['cyclic_initial']==phi['cyclic_final']
        assert phi['first_noncheap_B_increments']==phi['A_reset_decrements']<=phi['A_bit_budget']<=2*z['A']
        assert z['no_reset_promotion_necessity_verified']
        counts.update(z['noncheap_renewal_counts']);case.update(k for k in z['noncheap_renewal_counts'] if k.startswith('case_'))
    assert case=={'case_LL','case_RR','case_LR','case_RL'}
    table=load(ROOT/'LOCAL_PRIMITIVE_TABLE_AUDIT.json');assert table['four_key_shapes']==14 and table['target_traces']==56
    assert all(table['cases'][c]>0 for c in ('LL','RR','LR','RL','ZIG'))
    geom=load(ROOT/'FILTERED_RENEWAL_GEOMETRY.json');assert len(geom)==11
    assert sum(len(z['canonical_original_C_old_renewals']) for z in geom)==21
    for z in geom:
        assert z['mediator_injection_verified'] and z['no_full_source_residual_inferred']
        for edge in z['canonical_original_C_old_renewals']:
            assert edge['transition'] in ('promotion_free','promotion_mediated')
    obstruction=load(ROOT/'EXACT_NONCHEAP_VERSUS_C_OLD_OBSTRUCTION.json')
    assert obstruction['earlier_receiving_cohort']==[] and obstruction['earlier_original_R_star']==[]
    assert obstruction['later_E_old_gaps'] and obstruction['earlier_physical_noncheap_parent']['parent'][1]>2
    debit=load(ROOT/'EXACT_OWNERSHIP_DEBIT_OBSTRUCTION.json')
    assert debit['state']['ownership_before']==debit['state']['ownership_after']
    assert debit['candidate_r_at_event']==1 and debit['actual_posthybrid_r_at_event']==0 and debit['delta_any_function_of_ownership_vector']==0
    assert len(load(ROOT/'REPLICATION_RENEWAL_INVARIANCE.json'))==2
    write('M1_CONT05_SOURCE_WITNESSES.json',{'fresh_complete_original_sources':fresh,'inherited_complete_controls':inherited,
        'new_full_native_original_classifications':8,'physical_source_audits':104,'original_C_old_accounting_audits':42,
        'long_native_scope':'Inherited exact expansion/invariance/physical certificates only; no full long native R_* rerun.',
        'complete_source_words_and_states':'All source catalogs contain full labelled initial states, legal reaching prefixes and measured words; PHYS and pinned expansion files supply every original event/state.',
        'finite_coverage_is_universal_proof':False})
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    return {'principal_result':'E — NEW SOURCE-UNIFORM STRUCTURAL ADVANCE','full_M1':'OPEN',
        'universal_K_UU':None,'approved_completed_transfer_X':None,'original_interface_changed':False,
        'new_complete_sources':8,'new_full_native_classifications':8,'max_new_population':107,'max_new_operations':1591,
        'all_physical_controls':104,'exact_original_accounting_reductions':42,'direct_filtered_geometry_sources':11,'direct_filtered_geometry_edges':21,
        'physical_transition_totals':dict(counts),'genuine_positive_S_UU_certified':False,'new_literal_S_UU_gaps':0,
        'universal_structural_results':['Exact C_old predecessor with reset-free cyclic exception','Full A rigidity and FREE/MEDIATED frame alternative',
            'Globally injective mediation by real SS promotion/P entry','Cyclic binary-ownership law with zero repeated-use debit',
            'Specified paired identity replication preserves physical noncheap renewal graph'],
        'exact_refutations':['Earlier physical noncheap use does not necessarily exhaust E_old','Ownership-only positive local repeat debit fails before H/quota'],
        'first_missing_implication':'Absolute global A price or prior-hybrid contradiction for actual promotion-free repeated original C_old sigma demand, with bounded cross-column reuse. Mediated unweighted P count also lacks a completed A/transfer price.',
        'verification_scope':'Same agent, separate original engines and physical/selector audits; no external reviewer or formal kernel.',
        'preservation':load(ROOT/'INPUT_MANIFEST.json')}

def verify_only():
    m=load(ROOT/MANIFEST);assert inventory()==m['files']
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    assert m['full_M1']=='OPEN' and m['principal_result']=='E — NEW SOURCE-UNIFORM STRUCTURAL ADVANCE'
    print('PASS read-only exact C5 delivery and all inherited seals/HEAD/tracked bytes;',len(m['files']),'files; full M1 OPEN.',flush=True)

def seal():
    assert not (ROOT/MANIFEST).exists(),'Never overwrite a sealed stage.'
    t0=time.process_time();w0=time.perf_counter();ok=False;name='CPU_finalization.json';i=2
    while (ROOT/name).exists():name=f'CPU_finalization_{i}.json';i+=1
    try:result=audit();write('FINAL_VERIFICATION.json',result);ok=True
    finally:write(name,{'completed':ok,'cpu_seconds':time.process_time()-t0,'wall_seconds':time.perf_counter()-w0,'memory':memory(),
        'scope':'Final full new edge/SET/boundary and accounting consistency plus all transitive preservation; imports excluded.'})
    receipts={p.name:load(p) for p in ROOT.glob('CPU_*.json')}
    failed=[n for n,z in receipts.items() if not z['completed']]
    assert failed==['CPU_exhaustive_physical_renewal_law.json'],failed
    cpu=sum(z['cpu_seconds'] for z in receipts.values());peak=max(z['memory']['peak_working_set_bytes'] for z in receipts.values())
    assert cpu<=1800 and peak<2*1024**3
    write('RESOURCE_RECORD.json',{'allocation':{'measured_script_CPU_seconds':1800,'fresh_complete_source_cap':8,'population_cap':259,
        'operation_cap':40000,'per_process_peak_working_set_aim_bytes':2*1024**3},
        'measured_script_CPU_seconds_total':cpu,'maximum_measured_peak_working_set_bytes':peak,'receipts':receipts,
        'fresh_complete_sources':8,'fresh_full_native_sources':8,'max_fresh_population':107,'max_fresh_operations':1591,
        'failed_implementation_run':'First physical audit lacked the later-vertex-is-first-P-entry case; exact original script, partial96 records and failed receipt preserved. No source or theorem changed.',
        'failed_survivor_attempts':'All8 full native sources remain paid. Scope and failure of each necessary-conjunction construction are recorded.',
        'unmetered':['Imports before meters','Read-only searches/inspections, including corrected filename and long-relative-path lookups',
            'Proof reasoning and prose/patch construction','Final serialization and read-only post-seal verification'],
        'resources_are':'Measured script scope, not total reasoning CPU or session wall time. Allocation is operational, not a mathematical assumption.',
        'historical_writes':0,'Git_mutations':0,'subagents':0,'external_reviewers':0,'installations':0})
    write(MANIFEST,{'principal_result':'E — NEW SOURCE-UNIFORM STRUCTURAL ADVANCE','full_M1':'OPEN',
        'format':'Exact relative SHA256 inventory excluding only this manifest.','C4_manifest_sha256':hfile(C4/'M1_CONT04_DELIVERY_MANIFEST.json'),'files':inventory()})
    print('PASS sealed',len(inventory()),'files;',round(cpu,3),'measured script CPU seconds; structural E, full M1 OPEN.',flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:assert not sys.argv[1:];seal()
