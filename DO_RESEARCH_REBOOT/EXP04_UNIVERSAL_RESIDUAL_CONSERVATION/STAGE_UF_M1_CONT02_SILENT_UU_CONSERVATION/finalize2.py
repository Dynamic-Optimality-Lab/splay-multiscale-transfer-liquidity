"""Seal the exact-obstruction checkpoint; --verify-only is read-only."""
from base2 import *
import ast,gc,re

MANIFEST='M1_CONT02_DELIVERY_MANIFEST.json'
REQUIRED=['M1_CONT02_THEOREM_TARGET.md','SILENT_UU_EXACT_ELIGIBILITY.md','SILENT_UU_CREATOR_GEOMETRY.md',
 'SILENT_UU_LIFECYCLE_PROOF.md','SILENT_UU_CONSERVATION_PROOF.md','SILENT_UU_TRANSFER_INTERFACE.md',
 'SILENT_UU_COUNTEREXAMPLE_LEDGER.md','SILENT_UU_SOURCE_WITNESSES.json','SILENT_UU_INDEPENDENT_VERIFICATION.md',
 'M1_CONT02_GLOBAL_ACCOUNTING.md','M1_CONT02_TO_M2_M3_INTERFACE.md','M1_CONT02_PROOF_LEDGER.md',
 'M1_CONT02_FINAL_REPORT.md','M1_CONT02_REPRODUCTION.md']

def files():return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!=MANIFEST}

def gitstate():
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=REPO,text=True).strip()
    return head,branch

def verify():
    z=load(ROOT/MANIFEST);assert files()==set(z['files'])
    for n,h in z['files'].items():assert hfile(ROOT/n)==h,n
    assert all((ROOT/n).is_file() for n in REQUIRED)
    assert gitstate()==(z['HEAD'],z['branch'])
    assert preserve()==load(ROOT/'INPUT_MANIFEST.json')
    print('PASS read-only exact continuation02 seal:',len(z['files']),'files; all C1/M1/M0/transitive pins unchanged; full M1 OPEN',flush=True)

def build(cpu,wall,receipt):
    assert not (ROOT/MANIFEST).exists(),'Already sealed; use --verify-only.'
    pins=preserve();assert pins==load(ROOT/'INPUT_MANIFEST.json');head,branch=gitstate()
    oldcat=load(ROOT/'INHERITED_SOURCE_CATALOG.json');oldrows=load(ROOT/'INHERITED_SIGNATURE_RESULTS.json')
    assert len(oldcat)==len(oldrows)==52
    witnesses=[];total=Counter();unique=set()
    for i,(e,row) in enumerate(zip(oldcat,oldrows)):
        assert digest(e['source'])==row['source_sha256']==e['source_sha256']
        for k,h in e['sealed_input_hashes'].items():assert hfile(e[k])==h
        assert row['actual_S_UU']==[]
        witnesses.append({'group':'inherited','index':i,'source':row['source'],'source_sha256':e['source_sha256'],
            'complete_source_catalog':'INHERITED_SOURCE_CATALOG.json','catalog_index':i,
            'evidence':{k:{'path':e[k],'sha256':h} for k,h in e['sealed_input_hashes'].items()},
            'actual_S_UU':0,'original_R_star_scope':row['original_R_star_scope']})
    specifications=[('RUN_A','RUN_A_SOURCE_CATALOG.json','RUN_A_RESULTS.json',6),
                    ('RUN_B','RUN_B_SOURCE_CATALOG.json','RUN_B_RESULTS.json',6),
                    ('FAN','FAN_SOURCE_CATALOG.json','FAN_RESULTS.json',2)]
    for stem,cn,rn,count in specifications:
        ss=load(ROOT/cn);rows=load(ROOT/rn);assert len(ss)==len(rows)==count
        for i,(s,row) in enumerate(zip(ss,rows)):
            sh=digest(s);assert sh==row['source_sha256'] and sh not in unique;unique.add(sh)
            p=load(ROOT/f'{stem}_PHYS_{i:02}.json');b=load(ROOT/f'{stem}_BIRTH_{i:02}.json')
            f=load(ROOT/f'{stem}_FOREST_{i:02}.json');w=load(ROOT/f'{stem}_WEIGHTS_{i:02}.json')
            assert p['source_sha256']==b['source_sha256']==sh
            assert len(p['events'])==row['primitives']==b['original_SET_and_sign_checks']
            assert len(p['boundaries'])==row['operations']==len(s['operations'])
            assert p['state_pool']['all_complete_operation_states_checked_against_immutable_engine']
            assert row['prefix']['complete_reached_pair_verified'] and b['actual_R_C_deep']==0
            assert {tuple(v['parent']) for v in p['doubles']}=={tuple(v['parent']) for v in f['vertices']}=={tuple(v['parent']) for v in w['vertices']}
            assert all(z['w']==0 for z in w['vertices']) and w['R_overflow']==0
            rank={x:j for j,x in enumerate(p['original_S'])};xs=[x for tag,x in s['operations'] if tag=='K']
            raw=sum((x!=xs[j-1])+abs(rank[x]-rank[xs[j-1]]).bit_length() for j,x in enumerate(xs))
            assert raw==row['raw_periodic_cost']<=10*row['A']
            if stem=='RUN_B':
                cr=row['critical_consumers'];assert len(cr)==s['k']-1
                assert all(z['R6'] and z['A_gap']==1 and z['j']==s['L']+1 and z['distance']>2 for z in cr)
                assert all(z['quota_early']==(s['L']==1) for z in cr)
            total['fresh_measured_operations']+=len(s['operations']);total['fresh_original_primitives']+=len(p['events'])
            total['fresh_full_tuple_replay_sources']+=1;total['fresh_R6_directly_reconstructed']+=len(b['original_R6'])
            total['fresh_max_population']=max(total['fresh_max_population'],len(s['initial_B']['children']))
            scope=row.get('native_R_star_scope','EXECUTED')
            witnesses.append({'group':stem,'index':i,'source':s['name'],'source_sha256':sh,
                'complete_source_catalog':cn,'catalog_index':i,'catalog_file_sha256':hfile(ROOT/cn),
                'evidence':{k:{'file':f'{stem}_{k}_{i:02}.json','sha256':hfile(ROOT/f'{stem}_{k}_{i:02}.json')}
                    for k in ('PHYS','FOREST','WEIGHTS','M1_AUDIT','BIRTH')},
                'full_mutable_immutable_scope':'Every actor operation, complete states and all original primitive SET/Pi/cohorts/R6',
                'native_U_all_pair_agreement':True,'native_R_star_scope':scope,'actual_S_UU':0})
            del p,b,f,w;gc.collect()
    ar=load(ROOT/'RUN_A_RESULTS.json');assert [z['original_R6'] for z in ar]==[3,0,0,0,0,0]
    assert load(ROOT/'RUN_A_BIRTH_01.json')['original_pairs']==[]
    ordered=load(ROOT/'ORDERED_RESULTS.json');assert len(ordered)==3
    for z in ordered:assert z['actual_S_UU']==0 and z['no_H_diagnostic_all_quota_selected']
    exact=load(ROOT/'ORDERED_01.json')
    rho=[5,[3,6],[4,3]];e=next(e for e in exact['native_original_R_star'] if e['rho']==rho)
    assert e in exact['disjoint_original_assignments']['H_all']
    birth=load(ROOT/'RUN_B_BIRTH_01.json');rr=next(z for z in birth['C_U_births'] if z['consumer']==[5,6])
    assert rr['creator']==[3,6] and rr['distance']==6 and rr['creator_class']=='U'
    # Short source is full independent/native U/R6; long source uses exact state/event replication.
    ss=load(ROOT/'BOOST_SOURCE_CATALOG.json');br=load(ROOT/'BOOST_RESULTS.json')
    assert len(ss)==2
    for s,key in zip(ss,('short','long')):
        sh=digest(s);assert sh==br[key]['source_sha256'] and sh not in unique;unique.add(sh)
        total['fresh_measured_operations']+=len(s['operations'])
        total['fresh_max_population']=max(total['fresh_max_population'],len(s['initial_B']['children']))
        witnesses.append({'group':'BOOST_'+key,'source':s['name'],'source_sha256':sh,
            'complete_source_catalog':'BOOST_SOURCE_CATALOG.json','catalog_index':0 if key=='short' else 1,
            'catalog_file_sha256':hfile(ROOT/'BOOST_SOURCE_CATALOG.json'),
            'evidence':['BOOST_SHORT_PHYS.json','BOOST_SHORT_FOREST.json','BOOST_SHORT_BIRTH.json'] if key=='short' else
                ['BOOST_SHORT_PHYS.json','BOOST_EVENT_EXPANSION.json','EXPANDED_EVENT_AUDIT.json','BOOST_LONG_FAST_STATES.json'],
            'original_R_star_scope':'NOT_CLASSIFIED',
            'U_R6_scope':'Complete independent/native U/cohort/R6' if key=='short' else
                'Exact internal-label/scan/first-hit replication law from checked short source, with whole-word fast physical replay; no full long native Pi rerun',
            'actual_S_UU':0,'positive_certificate':'raw' if key=='short' else 'G and H'})
    short,long=ss;assert len(unique)==16 and total['fresh_max_population']<=1027
    assert short['initial_A']==long['initial_A'] and short['initial_B']==long['initial_B']
    assert short['reaching_prefix']==long['reaching_prefix']
    p=load(ROOT/'BOOST_SHORT_PHYS.json');b=load(ROOT/'BOOST_SHORT_BIRTH.json');rule=load(ROOT/'BOOST_EVENT_EXPANSION.json')
    assert p['source_sha256']==b['source_sha256']==digest(short)
    assert p['state_pool']['all_complete_operation_states_checked_against_immutable_engine']
    assert br['short']['native_U_and_all_original_pairs_agree'] and br['short']['prefix']['complete_reached_pair_verified']
    assert br['short']['original_R6']==len(b['original_R6'])==62
    assert len(br['short']['preserved_late_silent_UU_R6_parents'])==62
    assert br['short']['preserved_late_silent_UU_R6_parents']==br['long']['inherited_late_silent_UU_R6_parents']
    lo,hi=rule['template_primitive_slice_zero_based'];assert hi-lo==4
    assert rule['copies_in_long']==long['replication']==141843
    expansion=load(ROOT/'EXPANDED_EVENT_AUDIT.json')
    assert expansion['original_primitives']==len(p['events'])+4*(long['replication']-1)==622928
    assert expansion['real_A_StepEv']==br['long']['A']==314555 and expansion['original_B_doubles']==4324
    total['fresh_original_primitives']+=len(p['events'])+expansion['original_primitives']
    total['fresh_full_tuple_replay_sources']+=1;total['fresh_replication_fast_sources']+=1
    total['fresh_R6_directly_reconstructed']+=len(b['original_R6'])
    del p,b;gc.collect()
    fast=load(ROOT/'BOOST_LONG_FAST_STATES.json');assert len(fast['rows'])==len(long['operations'])==308011
    assert fast['full_A_B_return_verified']
    L=long['rootzig_loop_start'];end=L+2*long['replication']
    for i,(op,row) in enumerate(zip(long['operations'],fast['rows']),1):
        assert row['t']==i and [row['tag'],row['x']]==op
        assert 0<=row['B_state']<len(fast['states'])
        if L<=i<end:assert row['a']==1 and row['q']==0 and row['B_steps'][0][0]=='ZIG'
    for z in br['long']['G_H_periodic_certificates']:
        assert z['B_cyclic']==13512<=10*z['A'] and z['eligible_periodic']
        assert not any(L<=h<end for h in z['retained_original_operations'])
    assert br['long']['raw_periodic_cost']==3145551==10*br['long']['A']+1
    del fast;gc.collect()
    fan=load(ROOT/'FAN_RESULTS.json');assert [z['original_R6'] for z in fan]==[2,7]
    assert len(fan[1]['critical']['candidate_old_grandparents'])==17
    fb=load(ROOT/'FAN_BIRTH_01.json');critical=[z for z in fb['C_U_births'] if z['consumer'][0]==2]
    assert len(critical)==16 and all(z['creator_class']=='whole_frame_exposed' for z in critical)
    assert load(ROOT/'LOCAL_PACKING_SCREEN.json')['physical_violations']==[]
    assert all(not z['violation'] for r in fan for z in r['physical_local_packing_rows'])
    write('EXACT_OBSTRUCTIONS.json',{'principal_outcome':'D','full_M1':'OPEN',
        'H_LATE':{'claim':'Absolute height bound on deep silent original U/R6 C chains beyond j>2a_h',
            'status':'REFUTED parameterized complete sources','parameters':'k>=4,odd L>=3',
            'height':'k-1','original_j':'L+1','original_A_gap':1,'physical_distances':'3,6,...,3(k-1)'},
        'literal_native_R_star_example':{'catalog':'RUN_B_SOURCE_CATALOG.json','index':1,'rho':rho,
            'original_parent':[5,6],'creator':[3,6],'distance':6,'actual_paid_by':'H_all; no-H diagnostic also quota-fits'},
        'RAW_UU':{'status':'REFUTED complete source','source_sha256':digest(long),'A':314555,'Q_B':4324,
            'raw':3145551,'ten_A':3145550,'G_H':[13512,13512],'actual_S_UU':0},
        'PAD_ALL':{'status':'REFUTED k4,L2','catalog':'RUN_A_SOURCE_CATALOG.json','index':1,
            'original_adjacent_pair_count':0,'original_R6':0,'T_label_claimed':False},
        'local_packing':'OPEN; no finite violation; fan wide U packet has non-U creators',
        'unbounded_S_UU_over_A_claimed':False,'positive_prescribed_S_UU_witness':False})
    write('SILENT_UU_SOURCE_WITNESSES.json',{'principal_outcome':'D','full_M1':'OPEN','date':'2026-11-11',
        'sources':witnesses,'complete_inherited_sources':52,'unique_complete_fresh_sources':16,
        'full_mutable_immutable_fresh_sources':15,'exact_replication_and_full_fast_fresh_sources':1,
        'source_completeness':'All catalog entries contain full labelled initial A/B trees, legal reaching prefix and full original measured operation list; no source is merely a hash.',
        'IDs':'Source-scoped original rho=(h,inner original producer,outer original producer); B double(h,j); primitive(actor,h,j,bit).',
        'long_event_format':'Lossless short full primitive/state stream plus original occurrence expansion; decoder and full original source included.',
        'positive_S_UU_witness':False})
    for n in REQUIRED:assert (ROOT/n).is_file(),n
    for p in ROOT.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    for p in ROOT.glob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
            if '://' not in link:assert (ROOT/link).exists(),(p.name,link)
    write('FINAL_VERIFICATION.json',{'principal_outcome':'D — NEW EXACT PHYSICAL OBSTRUCTION','full_M1':'OPEN',
        'universal_K_UU':None,'approved_physical_transfer_X':None,'positive_prescribed_S_UU_witness':False,
        'inherited_interface':'Q_B <= (161+48 C_seq+102 C_DF) A + |S_UU| + R_P',
        'new_A_coefficient_added':0,'new_exact_obstructions':['H-LATE bounded late qualified-chain height','RAW-UU forced raw periodic certificate'],
        'gate_status':{'UU-1':'Exact literal signature and necessary rank/noncheap/periodic-negative conditions reconstructed',
            'UU-2':'Mandatory G/O/cyclic structural law inherited; new explicit arbitrary late-chain and return-replication laws',
            'UU-3':'OPEN for actual S_UU conservation/elimination/transfer','UU-4':'OPEN global A-load for actual S_UU',
            'UU-5':'Complete M1 OPEN; retain114/161 residual interface'},
        'first_missing_bridge':'Globally price or eliminate noncheap silent-UU original D-tail gaps that evade all applicable periodic and local comparisons.',
        'finite_local_packing_status':'No violation; universal lemma OPEN, not a proof',
        'historical_sources':52,'fresh_unique_sources':16,'counts':dict(total),
        'long_original_primitives':622928,'long_native_Pi_R_star_rerun':False,
        'long_verification':'Full short independent/native U/R6 plus exact complete-state insertion law, lossless ID/event expansion and whole-long-word fast full-state replay.',
        'native_R_star_missingness_retained':True,'finite_source_coverage_claimed_as_universal':False,
        'formal_proof_assistant':False,'external_mathematical_review':False,'same_agent_distinct_implementations':True,
        'preservation':pins,'HEAD':head,'branch':branch,'tracked_Git_unchanged':True,
        'Universal_Relaxed_Coarse_Double':'OPEN','Dynamic_Optimality':'OPEN'})
    write(receipt,{'completed':True,'stage':'finalization','cpu_seconds':time.process_time()-cpu,
        'wall_seconds':time.perf_counter()-wall,'memory':prev.base0.old.inherited.memory()})
    receipts=[{'file':p.name,**load(p)} for p in sorted(ROOT.glob('CPU*.json'))]
    measured=sum(z['cpu_seconds'] for z in receipts);peak=max(z['memory']['peak_working_set_bytes'] for z in receipts)
    assert measured<=1200 and peak<=2*(1<<30)
    write('RESOURCE_RECORD.json',{'timed_stage_receipts':receipts,'measured_stage_CPU_seconds':measured,
        'observed_per_process_peak_working_set_bytes':peak,'CPU_allocation_seconds':1200,
        'observed_per_process_peak_aim_bytes':2*(1<<30),'fresh_source_cap':16,'fresh_unique_complete_sources':16,
        'fresh_population_cap':1027,'fresh_max_population':total['fresh_max_population'],
        'failed_and_duplicate_audits_included':True,
        'unmetered':'Module imports before meters, shell inspections, mathematical reasoning/prose/patch authoring, final manifest hashing and read-only seal verification, tool overhead.',
        'not_a_host_quota_or_theorem_hypothesis':True,'resource_limit_not_asserted_as_mathematical_reason_for_open_target':True})
    hashes={n:hfile(ROOT/n) for n in sorted(files())}
    write(MANIFEST,{'date':'2026-11-11','principal_outcome':'D','full_M1':'OPEN','HEAD':head,'branch':branch,
        'C1_manifest_sha256':pins['C1_manifest_sha256'],'excluded_self':MANIFEST,'files':hashes})
    print('SEALED',len(hashes),'files; D, full M1 OPEN; measured CPU',measured,'peak bytes',peak,flush=True)

if __name__=='__main__':
    if sys.argv[1:]==['--verify-only']:verify()
    else:
        assert not sys.argv[1:],'Use no arguments or --verify-only.'
        cpu=time.process_time();wall=time.perf_counter();name='CPU_finalization.json';j=2
        while (ROOT/name).exists():name=f'CPU_finalization_{j}.json';j+=1
        try:build(cpu,wall,name)
        except Exception as exc:
            write(name,{'completed':False,'stage':'finalization','error':repr(exc),
                'cpu_seconds':time.process_time()-cpu,'wall_seconds':time.perf_counter()-wall,
                'memory':prev.base0.old.inherited.memory()});raise
