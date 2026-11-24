"""Seal the reviewed M0 delivery, or verify its exact seal without writes.

This is data/provenance verification, not a formal mathematical proof checker.
"""
from base0 import *
from independent0 import scan_forest, audit_forest
from residual0 import gap_costs
import ast, gc

MANIFEST='M0_DELIVERY_MANIFEST.json'
REQUIRED=[
    'M0_THEOREM.md','M0_FOREST_CONSTRUCTION.md','M0_FRAME_DESCENT_PROOF.md',
    'M0_ROOT_INJECTION_PROOF.md','M0_RESIDUAL_PARTITION_PROOF.md',
    'M0_TO_M1_M2_M3_INTERFACE.md','M0_COUNTEREXAMPLE_LEDGER.md',
    'M0_FOREST_WITNESSES.json','M0_INDEPENDENT_VERIFICATION.md',
    'M0_ACCOUNTING_AUDIT.md','M0_PROOF_LEDGER.md','M0_FINAL_REPORT.md',
    'M0_REPRODUCTION.md']

def actual_files():
    return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
            if p.is_file() and p.name!=MANIFEST}

def git_state():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010'
    assert branch=='coarse-double-branch'
    return head,branch

def pins():
    out=preservation();original=load(ROOT/'INPUT_MANIFEST.json')
    for name,h in original['M0_additional_pins'].items():assert hfile(REPO/name)==h,name
    assert out['C05_manifest_sha256']==original['C05_manifest_sha256']
    return out

def verify_only():
    seal=load(ROOT/MANIFEST)
    assert actual_files()==set(seal['files'])
    for name,h in seal['files'].items():assert hfile(ROOT/name)==h,name
    assert all((ROOT/n).is_file() for n in REQUIRED)
    head,branch=git_state();assert (head,branch)==(seal['HEAD'],seal['branch'])
    pins()
    print('PASS read-only exact seal,',len(seal['files']),'files; historical pins and tracked Git state unchanged',flush=True)

def build():
    assert not (ROOT/MANIFEST).exists(),'Already sealed: use --verify-only or a fresh reproduction directory.'
    cpu=time.process_time();wall=time.perf_counter();pinned=pins()
    cat=load(ROOT/'SOURCE_CATALOG.json');rows=load(ROOT/'STRUCTURAL_RESULTS.json')
    accounting=load(ROOT/'RESIDUAL_AUDIT.json');inventory=load(ROOT/'WEIGHT_INVENTORY.json')
    diag=load(ROOT/'DIAGNOSTIC_PREHYBRID_WEIGHTS.json')
    assert len(cat)==len(rows)==len(accounting)==len(inventory)==20
    index=[];totals=Counter();archive_checked={}
    for i,(entry,row,acc,inv) in enumerate(zip(cat,rows,accounting,inventory)):
        s=entry['source'];name=s['name'];sh=digest(s)
        assert name==row['source']==acc['source']==inv['source']
        assert sh==entry['source_sha256']==row['source_sha256']
        ar=Path(entry['archive'])
        if str(ar) not in archive_checked:archive_checked[str(ar)]=hfile(ar)
        assert archive_checked[str(ar)]==entry['archive_sha256']
        names=[f'PHYS_{i:02}.json',f'FOREST_{i:02}.json',f'WEIGHTS_{i:02}.json']
        phys,f,w=(load(ROOT/n) for n in names)
        assert phys['source']==f['source']==name and phys['source_sha256']==sh
        assert digest(phys['events'])==row['original_event_sha256']==phys['state_pool']['original_event_sha256']
        if 'trace_hash' in s:assert digest(phys['events'])==s['trace_hash']
        ds={tuple(z['parent']):{k:v for k,v in z.items() if k!='parent'} for z in phys['doubles']}
        r=SimpleNamespace(ops=s['operations'],events=phys['events'],boundaries=phys['boundaries'],
            doubles=ds,A=row['A'],bits={k:1<<(k-1) for k in phys['original_S']})
        fresh=scan_forest(r)
        recorded={tuple(z['parent']):{k:(tuple(v) if k in ('predecessor','A_donor') and v is not None else v)
                  for k,v in z.items() if k!='parent'} for z in f['vertices']}
        assert recorded==fresh
        checks=audit_forest(r,fresh)
        for k,v in checks.items():assert f[k]==row[k]==v,(name,k)
        assert len(ds)==row['Q_B']==len(recorded)==len(w['vertices'])
        assert row['prefix_check']['complete_reached_pair_verified']
        assert phys['state_pool']['all_complete_operation_states_checked_against_immutable_engine']
        nstates=len(phys['state_pool']['states'])
        for z in phys['boundaries']:
            for k in ('pre_A_state','post_A_state','pre_B_state','post_B_state'):assert 0<=z[k]<nstates
        for z in ds.values():
            for k in ('pre_step_state','post_step_state'):assert 0<=z[k]<nstates
        weights={tuple(z['parent']):z for z in w['vertices']}
        assert set(weights)==set(recorded)
        for v,z in weights.items():assert z['type']==recorded[v]['type'] and 0<=z['w']<=3
        assert sum(z['w'] for z in weights.values())==w['R_overflow']==inv['R_overflow']==0
        assert all(w['R_'+k]==len(w['literal_gap_lists_by_vertex_type'][k])==0 for k in 'RCP')
        assert all(z['w']==0 for v,z in weights.items() if recorded[v]['type']=='R')
        assert acc['old_raw_periodic_certificate']<=10*row['A']
        if 'C_old' in acc:
            E={digest(z['rho']) for z in acc['E_old']}
            assert all(digest(z['rho']) in E for z in acc['C_old'] if recorded[tuple(z['original_parent'])]['type']=='R')
            gs=gap_costs(s,phys['boundaries'])
            for z in acc['quota_rows']:
                assert z['a_h']==gs[z['h']]
                assert z['selected']==z['parents'][:2*z['a_h']]
                assert z['b_h']<=2*z['a_h']
        rootseams=sum(z['type']=='R' and z['A_donor'][1]>v[0] for v,z in fresh.items())
        edgeseams=sum(z['type']!='R' and z['predecessor'][0]>v[0] for v,z in fresh.items())
        index.append({'index':i,'source':name,'population':len(s['initial_B']['children']),
            'source_sha256':sh,'complete_source_record':{'file':'SOURCE_CATALOG.json','zero_based_index':i},
            'historical_archive':entry['archive'],'historical_archive_sha256':entry['archive_sha256'],
            'physical':{'file':names[0],'sha256':hfile(ROOT/names[0]),'complete_state_pool_size':nstates},
            'forest':{'file':names[1],'sha256':hfile(ROOT/names[1]),**checks},
            'weights':{'file':names[2],'sha256':hfile(ROOT/names[2]),'literal_R_overflow':w['R_overflow']},
            'root_donors_across_printed_seam':rootseams,'edges_across_printed_seam':edgeseams,
            'membership_scope':acc['membership_scope'],'full_higher_R_star_available_in_M0':acc['original_R_star'] is not None,
            'periodic_certificate':acc['old_raw_periodic_certificate'],'periodic_threshold':10*row['A']})
        for k in ('original_operations','A','Q_B','primitive_bits','real_A_bits','root_count'):totals[k]+=row[k]
        for k in 'RCP':totals['type_'+k]+=row['types'].get(k,0)
        del r,phys,f,w,ds,fresh,recorded,weights;gc.collect()
    assert totals['Q_B']==19323 and totals['root_count']==18585
    assert sum(z['fresh_first_edge_beta_checks'] for z in diag)==45
    for source in ROOT.glob('*.py'):ast.parse(source.read_text(encoding='utf-8'),filename=str(source))
    write('M0_FOREST_WITNESSES.json',{'scope':'Complete original sources and full physical/forest/weight records; indexed rather than duplicated.',
        'canonical_IDs':{'vertex':'source-scoped (operation h, original B double j)',
            'primitive':'(actor,h,j,bit)','gap':'original rho=(consumer,inner birth,outer birth)'},
        'state_codes':'Collision-free full labelled child-pointer codes; see PHYS state_pool definition. Not hash-only witnesses.',
        'sources':index})
    assert all((ROOT/n).is_file() for n in REQUIRED)
    head,branch=git_state()
    write('FINAL_VERIFICATION.json',{'date':'2026-11-11','principal_result':'M0-A',
        'gates':{k:'PROVED by written mathematical argument; finite independent-implementation checks pass' for k in 'ABCDE'},
        'formal_proof_assistant':False,'external_human_or_agent_review':False,
        'independence':'Separately written implementations, same operating agent; scope in M0_INDEPENDENT_VERIFICATION.md.',
        'control_count':20,'totals':dict(totals),'fresh_nonempty_prehybrid_beta_checks':45,
        'tested_post_hybrid_overflow':0,'nonempty_prescribed_overflow_witness_certified':False,
        'universal_emptiness_inferred_from_finite_controls':False,
        'root_bound':'|V_R| <= real A bits = 2A-Z_A <= 2A',
        'exact_partition':'R_overflow=R_R+R_C+R_P; for frozen selectors R_R=0',
        'mandatory_interface':'R_overflow <= 6A+R_C+R_P',
        'descendant_conservation':'OPEN','Universal_Relaxed_Coarse_Double':'OPEN','Dynamic_Optimality':'OPEN',
        'C05_and_transitive_preservation':pinned,'M0_additional_pins_rechecked':True,
        'tracked_Git_state_unchanged':True})
    write('CPU_finalization.json',{'stage':'finalization','completed':True,
        'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,'memory':old.inherited.memory()})
    receipts=[{'file':p.name,**load(p)} for p in sorted(ROOT.glob('CPU_*.json'))]
    measured=sum(z['cpu_seconds'] for z in receipts)
    peak=max(z['memory']['peak_working_set_bytes'] for z in receipts)
    assert measured<=600 and peak<=2*(1<<30)
    write('RESOURCE_RECORD.json',{'timed_stage_receipts':receipts,'measured_stage_CPU_seconds':measured,
        'observed_process_peak_working_set_bytes':peak,'CPU_allocation_seconds':600,
        'observed_peak_aim_bytes':2*(1<<30),'control_cap':24,'controls_used':20,'fresh_population_cap':1027,
        'unmetered':'Imports before meters, shell startup, short read-only inspections, prose reasoning/authoring, tool overhead, final hash/seal passes.',
        'not_a_host_quota_or_theorem_hypothesis':True,'failed_adapter_receipt_included':True})
    files={name:hfile(ROOT/name) for name in sorted(actual_files())}
    write(MANIFEST,{'date':'2026-11-11','HEAD':head,'branch':branch,'principal_result':'M0-A',
        'excluded_self':MANIFEST,'files':files})
    print('SEALED',len(files),'files; measured CPU',measured,'peak bytes',peak,flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:
        assert len(sys.argv)==1,'Use no arguments to build or --verify-only.'
        build()
