"""Seal the reviewed restricted M1 checkpoint; --verify-only makes no writes."""
from base1 import *
from fractions import Fraction
import ast,gc,re

MANIFEST='M1_DELIVERY_MANIFEST.json'
REQUIRED=['M1_THEOREM_TARGET.md','M1_SAME_COLUMN_GEOMETRY.md','M1_CHAIN_LIFECYCLES.md',
    'M1_CONSERVATION_PROOF.md','M1_PHYSICAL_TRANSFER_INVARIANT.md','M1_GLOBAL_ACCOUNTING.md',
    'M1_COUNTEREXAMPLE_LEDGER.md','M1_SOURCE_WITNESSES.json','M1_INDEPENDENT_VERIFICATION.md',
    'M1_TO_M2_M3_INTERFACE.md','M1_PROOF_LEDGER.md','M1_FINAL_REPORT.md','M1_REPRODUCTION.md']

def actual_files():
    return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def git_state():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return head,branch

def verify_only():
    m=load(ROOT/MANIFEST);assert actual_files()==set(m['files'])
    for n,h in m['files'].items():assert hfile(ROOT/n)==h,n
    assert all((ROOT/n).is_file() for n in REQUIRED)
    head,branch=git_state();assert (head,branch)==(m['HEAD'],m['branch'])
    p=preserve();assert p['M0_manifest_sha256']==m['M0_manifest_sha256']
    print('PASS read-only exact M1 seal,',len(m['files']),'files; M0 and all historical pins unchanged',flush=True)

def build():
    assert not (ROOT/MANIFEST).exists(),'Already sealed; use --verify-only or a fresh sibling.'
    cpu=time.process_time();wall=time.perf_counter();pins=preserve()
    assert pins['M0_manifest_sha256']==load(ROOT/'INPUT_MANIFEST.json')['M0_manifest_sha256']
    cat=load(M0/'SOURCE_CATALOG.json');oldrows=load(ROOT/'HISTORICAL_RESULTS.json')
    news=load(ROOT/'NEW_SOURCE_CATALOG.json');newrows=load(ROOT/'NEW_RESULTS.json')
    assert len(cat)==len(oldrows)==20 and len(news)==len(newrows)==16
    historical=[];fresh=[];tot=Counter();maxloads=Counter()
    for historical_flag,ss,rows in ((True,[z['source'] for z in cat],oldrows),(False,news,newrows)):
        for i,(s,row) in enumerate(zip(ss,rows)):
            name=s['name'];assert row['source']==name and row['source_sha256']==digest(s)
            an=f'HISTORICAL_AUDIT_{i:02}.json' if historical_flag else f'NEW_AUDIT_{i:02}.json'
            z=load(ROOT/an);assert z['source']==name and z['primitive_edges_and_all_complete_boundaries_verified']
            assert z['actual_R_C']==z['actual_R_P']==0
            ft=z['flux_totals']
            assert ft.get('B_loss_atoms',0)==ft.get('B_gain_atoms',0)+ft.get('A_signed_flux',0)
            assert ft.get('B_loss_atoms',0)>=2*z['Q_B']+z['Z_B']
            assert sum(v['C_count'] for v in z['maximal_C_chains'])==z['C_parent_count']
            assert len(z['exact_B_ancestry_lifetimes'])==len(z['saturated_column_counterexamples'])==z['C_parent_count']
            assert all(v['physical_C_ticket_count']<=v['gain_capacity'] for v in z['restoration_packets'])
            for rr in z['bounded_fringe_payments']:
                r=rr['radius'];width=(1<<r)-1
                assert rr['global_gap_coefficient']==12*width and rr['selected_original_gap_weight']==0
                ids=[tuple(v['vertex']) for v in rr['mapping']];assert len(ids)==len(set(ids))==rr['selected_physical_C_parents']
                load_per=Counter(tuple(v['actual_A_StepEv']) for v in rr['mapping'])
                assert max(load_per.values(),default=0)==rr['maximum_parent_load_per_actual_A_StepEv']<=4*width
                assert len(ids)<=4*width*z['A']
                maxloads[r]=max(maxloads[r],rr['maximum_parent_load_per_actual_A_StepEv'])
            tot['C_physical_parents']+=z['C_parent_count']
            tot['radius2_physical_C_parents']+=z['bounded_fringe_payments'][1]['selected_physical_C_parents']
            if historical_flag:
                ref={'original_catalog':str(M0/'SOURCE_CATALOG.json'),'zero_based_index':i,
                    'source_sha256':digest(s),'historical_archive':cat[i]['archive'],'historical_archive_sha256':cat[i]['archive_sha256'],
                    'complete_physical_file':str(M0/f'PHYS_{i:02}.json'),'complete_physical_sha256':hfile(M0/f'PHYS_{i:02}.json'),
                    'global_forest_file':str(M0/f'FOREST_{i:02}.json'),'original_weights_file':str(M0/f'WEIGHTS_{i:02}.json'),
                    'new_independent_audit':an,'new_independent_audit_sha256':hfile(ROOT/an)}
                historical.append({'source':name,**ref})
            else:
                files={k:f'NEW_{k}_{i:02}.json' for k in ('PHYS','FOREST','WEIGHTS')}
                phys=load(ROOT/files['PHYS']);forest=load(ROOT/files['FOREST']);w=load(ROOT/files['WEIGHTS'])
                assert phys['source_sha256']==digest(s) and phys['source']==forest['source']==name
                assert len(phys['events'])==row['original_primitive_bits']
                assert len(phys['boundaries'])==row['original_operations']==len(s['operations'])
                assert row['prefix']['complete_reached_pair_verified']
                assert len(phys['original_S'])==row['original_S_size']
                xs=[x for tag,x in s['operations'] if tag=='K'];rank={x:j for j,x in enumerate(phys['original_S'])}
                raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs)) if rank else 0
                assert raw==row['old_raw_periodic_cost']<=10*row['A']
                V={tuple(v['parent']) for v in forest['vertices']}
                assert V=={tuple(v['parent']) for v in phys['doubles']}=={tuple(v['parent']) for v in w['vertices']}
                assert all(v['w']==0 for v in w['vertices']) and w['R_overflow']==0
                if 'full_original_Pi_file' in row:
                    pi=load(ROOT/row['full_original_Pi_file'])
                    assert pi['original_event_sha256']==digest(phys['events'])
                    assert pi['original_R6_count']==0 and pi['original_R_star']==[]
                fresh.append({'index':i,'source':s,'source_sha256':digest(s),
                    'files':{**{k:{'file':n,'sha256':hfile(ROOT/n)} for k,n in files.items()},
                             'AUDIT':{'file':an,'sha256':hfile(ROOT/an)}},
                    'full_original_Pi_file':row.get('full_original_Pi_file'),
                    'exact_current_zero_reason':'Positive frozen original periodic certificate plus unchanged cheap quota; no unrun Pi zero asserted.'})
                del phys,forest,w;gc.collect()
            del z;gc.collect()
    for n in REQUIRED:
        if n!='M1_SOURCE_WITNESSES.json':assert (ROOT/n).is_file(),n
    write('M1_SOURCE_WITNESSES.json',{'scope':'Complete new original sources, with immutable references to complete historical sources/states and fresh independent audits.',
        'historical_sources':historical,'new_sources':fresh,
        'canonical_IDs':{'vertex':'source-scoped original (operation h,B double j)','primitive':'(actor,h,j,bit)',
            'gap':'original rho=(consumer,inner birth,outer birth)','ancestry_lifetime':'(opening B primitive,g,target,first closing B primitive)'},
        'source_physical_states':'Full child-pointer state codes are in PHYS, not hash-only substitutes.',
        'positive_unpaid_R_C_claimed':False})
    cert=load(ROOT/'TEMPLATE_FAILURE_CERTIFICATES.json')
    assert len(cert['volume_price_obstructions'])==5 and len(cert['long_chain_indicator_obstructions'])==6
    for z in cert['volume_price_obstructions']:
        assert Fraction(z['exact_flux_over_A'])==Fraction(z['n'],2)
        assert z['A_signed_volume_flux']==z['B_target_marked_gain_volume']
    core=load(ROOT/'CORE_GAP_SCREEN.json');assert core['candidate_countercomponents']==[]
    assert [v['n'] for v in core['rows']]==list(range(3,9))
    assert all(v['maximum_observed_open_gap_core_keys']==1 for v in core['rows'])
    assert sum(v['recurrent_components_checked'] for v in core['rows'])==5065
    assert (tot['C_physical_parents'],tot['radius2_physical_C_parents'])==(1954,330)
    oldstats=load(M0/'STRUCTURAL_RESULTS.json')
    ops=sum(v['original_operations'] for v in oldstats+newrows)
    bits=sum(v['primitive_bits'] for v in oldstats)+sum(v['original_primitive_bits'] for v in newrows)
    assert (ops,bits)==(67316,197991)
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for p in ROOT.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link:assert (ROOT/link).exists(),(p.name,link)
    head,branch=git_state()
    write('FINAL_VERIFICATION.json',{'principal_outcome':'M1-D','full_M1':'OPEN','approved_complete_X':None,
        'scoped_theorem':'R_C,ell<=r <= 12(2^r-1) A; radius2 gives36A with exact deep complement',
        'additional_interface':'Q_B <= (83+48C_seq+102C_DF) A + R_C,ell>2 + R_P',
        'gate_status':{'M1-A':'PROVED','M1-B':'OPEN globally','M1-C':'PROVED scoped; OPEN globally',
                       'M1-D':'OPEN for the full c1/X target','M1-E':'Scoped interface sound; full completion gate OPEN'},
        'historical_complete_sources':20,'fresh_complete_sources':16,'independent_measured_operations':ops,
        'independent_primitive_edge_checks':bits,'physical_C_parents':1954,'radius2_physical_C_parents':330,
        'max_observed_parent_load_per_StepEv_by_radius':dict(maxloads),
        'new_full_original_Pi_sources':3,'nonempty_prescribed_R_C_witness':False,
        'universal_emptiness_inferred_from_samples':False,'universal_scalar_template_obstruction':'Written proof plus exact complete controls',
        'finite_core_screen':'5065 recurrent components through n8, active-set sizes2..4; no universal claim',
        'formal_proof_assistant':False,'external_mathematical_review':False,
        'same_agent_independent_implementation_scope':'Independent edge updater and mask/complete-state checks, plus immutable/pointer source replay and selected original Pi/cohort checks.',
        'M0_and_transitive_preservation':pins,'tracked_files_unchanged':True,
        'Universal_Relaxed_Coarse_Double':'OPEN','Dynamic_Optimality':'OPEN'})
    write('CPU_finalization.json',{'stage':'finalization','completed':True,'cpu_seconds':time.process_time()-cpu,
        'wall_seconds':time.perf_counter()-wall,'memory':base0.old.inherited.memory()})
    receipts=[{'file':p.name,**load(p)} for p in sorted(ROOT.glob('CPU_*.json'))]
    measured=sum(v['cpu_seconds'] for v in receipts);peak=max(v['memory']['peak_working_set_bytes'] for v in receipts)
    assert measured<=900 and peak<=2*(1<<30)
    write('RESOURCE_RECORD.json',{'timed_stage_receipts':receipts,'measured_stage_CPU_seconds':measured,
        'observed_process_peak_working_set_bytes':peak,'CPU_allocation_seconds':900,'observed_peak_aim_bytes':2*(1<<30),
        'fresh_source_cap':24,'fresh_complete_sources':16,'fresh_physical_population_cap':1027,
        'not_a_host_quota_or_mathematical_hypothesis':True,
        'unmetered':'Imports before meters including the first failed core-screen module-path attempt; first draft finalization stopped on omitted zero-valued Counter keys before writing its final receipt; initial/final read-only hash passes; short inspections; prose/reasoning; tool overhead.',
        'failed_API_adapter_receipt_included':True,'resource_limit_asserted_as_reason_for_unproved_theorem':False})
    files={n:hfile(ROOT/n) for n in sorted(actual_files())}
    write(MANIFEST,{'date':'2026-11-11','HEAD':head,'branch':branch,'principal_outcome':'M1-D','full_M1':'OPEN',
        'M0_manifest_sha256':pins['M0_manifest_sha256'],'excluded_self':MANIFEST,'files':files})
    print('SEALED',len(files),'files; M1-D, full M1 OPEN; measured CPU',measured,'peak bytes',peak,flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify_only()
    else:
        assert len(sys.argv)==1,'Use no arguments or --verify-only.'
        build()
