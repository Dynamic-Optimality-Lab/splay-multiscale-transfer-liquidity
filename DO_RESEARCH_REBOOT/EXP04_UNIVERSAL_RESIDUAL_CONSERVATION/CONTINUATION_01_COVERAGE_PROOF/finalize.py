from core import *
from periodic_payment import periodic_cost
import subprocess


def verify_pins():
    counts={}
    def check(name,base,pins):
        for p,h in pins.items():assert file_hash(base/p)==h,(name,p)
        counts[name]=len(pins)
    c1=json.loads((ROOT/'INPUT_MANIFEST.json').read_text())
    check('parent_EXP04',PARENT,c1['parent_files'])
    p4=json.loads((PARENT/'EXP04_INPUT_MANIFEST.json').read_text())
    check('inherited_EXP03',PARENT.parent/'EXP03_FINAL_R6_ESCAPE_CONSERVATION',p4['EXP03_files'])
    p3=json.loads((PARENT.parent/'EXP03_FINAL_R6_ESCAPE_CONSERVATION/EXP03_INPUT_MANIFEST.json').read_text())
    check('inherited_EXP02',PARENT.parent/'EXP02_FINAL_RESIDUAL_CLOSURE',p3['EXP02_complete_delivery_hashes_verified'])
    check('additional_repository_pins',ROOT.parents[2],p3['additional_repository_pins'])
    p2=json.loads((PARENT.parent/'EXP02_FINAL_RESIDUAL_CLOSURE/EXP02_INPUT_MANIFEST.json').read_text())
    check('EXP01_and_older_pins',ROOT.parents[2],p2['pins'])
    return counts


if __name__=='__main__':
    pins=verify_pins();repo=ROOT.parents[2]
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=repo,text=True).strip()
    assert head=='6d532b2c795c0778f57d8023b23b5fedfc48b010' and branch=='coarse-double-branch'
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=repo,text=True).strip()
    source_files=['SOURCE_WITNESSES.json','OWNERSHIP_SOURCES.json','COLUMN_SOURCES.json','INTERIOR_SOURCES.json',
                  'GUARD_CONTAMINATION_SOURCES.json','WIDE_GUARD_SOURCES.json','INTRINSIC5_SOURCES.json']
    sources=[];names=set()
    for f in source_files:
        for s in json.loads((ROOT/f).read_text()):
            assert s['name'] not in names;sources.append(s);names.add(s['name'])
    assert len(sources)==44
    assert max(len(s['operations']) for s in sources)<=12000
    assert max(len(s['initial_B']['children']) for s in sources)<=513
    write('EXP04_SOURCE_WITNESSES.json',{'inherited_archive':'../EXP04_SOURCE_WITNESSES.json',
        'inherited_archive_sha256':file_hash(PARENT/'EXP04_SOURCE_WITNESSES.json'),
        'new_unique_sources':sources,'source_batches':source_files,'new_unique_source_count':len(sources)})
    result_files=['OSCILLATION_RESULTS.json','RESCUE_ATTACK_RESULTS.json','OWNERSHIP_RESULTS.json','COLUMN_RESULTS.json',
                  'INTERIOR_RESULTS.json','GUARD_CONTAMINATION_RESULTS.json','WIDE_GUARD_RESULTS.json','INTRINSIC5_RESULTS.json']
    records={}
    for f in result_files:
        zs=json.loads((ROOT/f).read_text());zs=zs if isinstance(zs,list) else [zs]
        for z in zs:
            ev=z.get('R_star');assert ev is None or isinstance(ev,list)
            records[z['source']]={'source':z['source'],'A':z['A'],'Q_B':z['Q_B'],
                'original_R_star':ev,'original_Pi_classified':ev is not None,'result_artifact':f,
                'independent_original_operations':z['independent_operations']}
    assert set(records)==names
    for s in sources:
        xs=[x for tag,x in s['operations'] if tag=='K'];J=closure(Tree(s['initial_B']),xs)
        c=periodic_cost(xs,J);c['cut_before']=1;c['variant']='raw';c['eligible_B_cyclic_le_10A']=c['B_cyclic']<=10*s['A']
        records[s['name']]['raw_periodic_certificate']=c
    write('EXP04_RESIDUAL_INVENTORY.json',{'original_definition':'EXP03 unhandled minus EXP03 original equality-restart paid occurrences; unchanged',
        'latest_residual_definition':'R_next^P: remove frozen carrier, frozen four skipped-rank, cheap KEEP-gap, then periodic-or-local hybrid paid sets from original R_*',
        'universal_empty_or_O_A_status':'OPEN','new_sources':list(records.values()),
        'new_original_Pi_classified_sources':sum(z['original_Pi_classified'] for z in records.values()),
        'screening_without_Pi_sources':sum(not z['original_Pi_classified'] for z in records.values()),
        'no_finite_coverage_percentage_is_a_universal_proof':True})
    witness=json.loads((ROOT/'OWNERSHIP_RESULTS.json').read_text())[0]
    write('EXP04_PHYSICAL_LIFECYCLES.json',{'critical_original_escape':witness['lifecycles'],
        'additional_complete_lifecycle_records_in':['OSCILLATION_RESULTS.json','RESCUE_ATTACK_RESULTS.json','COLUMN_RESULTS.json'],
        'original_lifecycles_are_not_reclassified_on_comparisons':True})
    write('EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',{'focus':'Physical coverage rather than a new ancestry potential',
        'critical_source':witness['source'],'original_lifecycle_artifact':'EXP04_PHYSICAL_LIFECYCLES.json',
        'actual_original_parent':[645,2],'old_grandparent':18,'new_raw_ancestry_mass_bound_claimed':False,
        'inherited_refutations_preserved':True})
    small=json.loads((ROOT/'CRITICAL_WITNESS_CERTIFICATE.json').read_text())
    write('EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json',{'proof':'PROOF_LEDGER.md C1-C6',
        'original_A_load_bounds':{'cyclic_KEEP_gap_partition':1,'all_arc_irredundant_subcover':2,
                                 'frozen_carrier_directions':2,'frozen_skipped_rank_systems':4},
        'hybrid_periodic_and_local_cases':'source-disjoint; use maximum30 C_DF budget, not sum',
        'small_implementation_sanity_families':small['all_cyclic_arc_families_n_le_4'],
        'universal_congestion_proof_is_analytic':True})
    resources=[{'file':p.name,**json.loads(p.read_text())} for p in sorted(ROOT.glob('EXP04_RESOURCE_*.json'))]
    cpu=sum(r['process_CPU_seconds'] for r in resources)
    write('EXP04_EXPERIMENT_LOG.json',{'metered_research_CPU_seconds_including_interrupted_run':cpu,
        'unmetered':'small shell inspections, report authoring, and final archive/index hashing',
        'initial_staged_CPU_allocation':1200,'reviewed_staged_CPU_allocation':1800,
        'allocation_is_not_an_observed_host_quota':True,'resources':resources,
        'source_count_unique':44,'original_Pi_classified_unique':32,'guard_screening_without_Pi':12,
        'largest_population':max(len(s['initial_B']['children']) for s in sources),
        'longest_measured_source_operations':max(len(s['operations']) for s in sources),
        'interrupted_interval_search_has_no_negative_certificate':True,
        'research_cycles':['Backward tail conjecture refuted','Frozen exhaustive cover refuted',
            'All raw4 interval coverage refuted exactly','Cyclic subcover and all-arc payment proved',
            'Guarded exact-return payment proved and attacked','KEEP-gap cheap payment and hard guards proved',
            'Large hard-consumer source reconstructed and verified','Closed periodic initialization cancellation proved',
            'Restricted-support diagnostic proved; larger hard rank traffic remains open'],
        'universal_coverage_proved':False})
    write('FINAL_VERIFICATION.json',{'historical_hash_pin_counts':pins,'HEAD':head,'branch':branch,
        'tracked_changes':[],'critical_counterexample_checks':'CRITICAL_WITNESS_CERTIFICATE.json',
        'independent_original_Pi':'INDEPENDENT_ORIGINAL_PI.json','large_source_checks':'LARGE_SOURCE_VERIFICATION.json',
        'new_full_source_count':44,'metered_research_CPU_seconds':cpu,'universal_coverage_status':'REFUTED for frozen union; OPEN for enlarged hybrid',
        'proof_audit':'same-agent symbolic and programmatic; no formal/external end-to-end audit'})
    required=['EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_THEOREM_LEDGER.md','EXP04_COUNTEREXAMPLE_LEDGER.md',
        'EXP04_RESIDUAL_INVENTORY.json','EXP04_PHYSICAL_LIFECYCLES.json','EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',
        'EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json','EXP04_SOURCE_WITNESSES.json','EXP04_EXPERIMENT_LOG.json',
        'EXP04_REPRODUCTION.md','EXP04_FINAL_VERDICT.md']
    assert all((ROOT/p).exists() for p in required)
    hashes={str(p.relative_to(ROOT)).replace('\\','/'):file_hash(p) for p in sorted(ROOT.rglob('*'))
            if p.is_file() and p.name!='CONT01_DELIVERY_MANIFEST.json'}
    write('CONT01_DELIVERY_MANIFEST.json',{'HEAD':head,'branch':branch,'files':hashes,'required_deliverables':required,
        'historical_hash_pin_counts':pins,'mathematical_verdict':'Frozen exhaustiveness refuted; enlarged source-uniform partial payment proved; universal availability OPEN',
        'metered_research_CPU_seconds':cpu,'excluded_self':'CONT01_DELIVERY_MANIFEST.json'})
    print('PASS historical pins',pins,'new sources',len(sources),'files',len(hashes),'metered CPU',cpu,flush=True)
