"""Final preservation, accounting, resource and delivery checks."""
from exp04_core import *
import subprocess


if __name__=='__main__':
    cpu=timing.process_time();wall=timing.perf_counter();check_count=0
    inp=json.loads((ROOT/'EXP04_INPUT_MANIFEST.json').read_text())
    for p,h in inp['EXP03_files'].items():assert file_hash(PREV/p)==h;check_count+=1
    oldpins=json.loads((PREV/'EXP03_INPUT_MANIFEST.json').read_text())
    for p,h in oldpins['EXP02_complete_delivery_hashes_verified'].items():assert file_hash(OLD/p)==h;check_count+=1
    p02=json.loads((OLD/'EXP02_INPUT_MANIFEST.json').read_text())['pins']
    for p,h in p02.items():assert file_hash(REPO/p)==h;check_count+=1
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==inp['HEAD']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==inp['branch']
    assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=REPO,text=True).strip()
    tests=json.loads((ROOT/'EXP04_TEST_RESULTS.json').read_text());assert tests['status']=='PASS'
    summary=json.loads((ROOT/'EXP04_SUMMARY.json').read_text());assert summary['canonical_sources']==380 and summary['new_sources']==120
    assert summary['R_star']==499 and summary['R_next_finite']==0
    inv=json.loads((ROOT/'EXP04_RESIDUAL_INVENTORY.json').read_text());by={s['source']:s for s in inv['inherited_sources']+inv['new_sources']}
    assert len(by)==380
    for s in by.values():
        assert len(s['EXP04_assignments'])==s['R_star']==len(s['events'])
        assert len({digest(e['rho']) for e in s['EXP04_assignments']})==s['R_star']
        assert max(Counter(tuple(e['original_parent']) for e in s['events']).values(),default=0)<=3
        check_count+=3
    for z in json.loads((ROOT/'EXP04_MONOTONE_CERTIFICATES.json').read_text()):
        row=by[z['source']];available={tuple(e) for e in row['A_StepEv']};loads=Counter()
        for system in z['monotone_comparison']['systems']:
            used=set()
            for w in system['windows']:
                assert len(w['J'])<=2*(w['ell']-1)
                assert len(w['original_A_transition_witnesses'])==w['ell']-1
                for e in w['original_A_transition_witnesses']:
                    key=tuple(e);assert key in available and key not in used;used.add(key);loads[key]+=1
            assert sum(w['domain_size'] for w in system['windows'])<=2*len(used)<=2*row['A']
            check_count+=3
        assert max(loads.values(),default=0)<=4;check_count+=1
    for z in json.loads((ROOT/'EXP04_FINAL_CYCLE_DENSITY.json').read_text()):
        row=by[z['source']];used=set();available={tuple(e) for e in row['A_StepEv']}
        for w in z['windows']:
            assert w['density_D']<=4*w['original_A']
            assert len(w['original_A_StepEv'])==w['original_A']
            for e in w['original_A_StepEv']:
                key=tuple(e);assert key in available and key not in used;used.add(key)
        assert len(used)<=row['A'];check_count+=3
    required=['EXP04_DISCOVERY_REPORT.md','EXP04_RESEARCH_FRONTIER.md','EXP04_THEOREM_LEDGER.md','EXP04_COUNTEREXAMPLE_LEDGER.md',
        'EXP04_RESIDUAL_INVENTORY.json','EXP04_PHYSICAL_LIFECYCLES.json','EXP04_ANCESTRY_DISCREPANCY_EXPERIMENTS.json',
        'EXP04_GLOBAL_CONGESTION_EXPERIMENTS.json','EXP04_SOURCE_WITNESSES.json','EXP04_EXPERIMENT_LOG.json','EXP04_REPRODUCTION.md','EXP04_FINAL_VERDICT.md']
    assert all((ROOT/p).is_file() for p in required)
    write('EXP04_PRESERVATION_AUDIT.json',{'status':'PASS','checks':check_count,'EXP03_files':len(inp['EXP03_files']),
        'EXP02_files':len(oldpins['EXP02_complete_delivery_hashes_verified']),'earlier_pins':len(p02),'HEAD':inp['HEAD'],'branch':inp['branch'],
        'tracked_diff':'empty','qualification':'Hash checks preserve bytes; proof truth is a separate mathematical obligation.'})
    # Version final preflight measurements, even if packaging is repeated.
    name='EXP04_RESOURCE_package.json';v=2
    while (ROOT/name).exists():name=f'EXP04_RESOURCE_package_v{v:03d}.json';v+=1
    write(name,{'stage':'package_preflight','status':'completed','process_CPU_seconds':timing.process_time()-cpu,
        'wall_seconds':timing.perf_counter()-wall,'memory':memory(),
        'measurement_boundary':'preflight only; subsequent resource aggregation and final manifest hashing are excluded'})
    stages=[json.loads(p.read_text()) for p in sorted(ROOT.glob('*RESOURCE*.json')) if p.name!='EXP04_RESOURCE_SUMMARY.json']
    measured=[s for s in stages if isinstance(s.get('process_CPU_seconds'),(int,float))]
    total=sum(s['process_CPU_seconds'] for s in measured);assert total<=1800,total
    write('EXP04_RESOURCE_SUMMARY.json',{'recorded_process_CPU_seconds':total,'sum_recorded_stage_wall_seconds':sum(s['wall_seconds'] for s in measured),
        'peak_working_set_bytes':max(s['memory']['peak_working_set_bytes'] for s in measured),'peak_pagefile_bytes':max(s['memory']['peak_pagefile_bytes'] for s in measured),
        'allocation':{'initial_measured_CPU_seconds':1200,'reviewed_measured_CPU_seconds':1800,'new_complete_sources':120,'population':513,'operations_per_new_source':12000},
        'actual':{'canonical_sources':380,'new_complete_sources':120,'maximum_population':summary['maximum_population'],'maximum_new_operations':summary['maximum_new_operations']},
        'stages':stages,'unmeasured':'First cycle10 resource record was overwritten; marked explicitly, not estimated. Interactive inspections/prose and final hashing are not continuously measured. No exact total session CPU or hard scheduler quota is claimed.',
        'checkpoint_reason':'Recorded new-source allocation120 is used. Universal research remains open; no mathematical completion or host-impossibility claim.'})
    files={str(p.relative_to(ROOT)).replace('\\','/'):file_hash(p) for p in ROOT.rglob('*') if p.is_file()
        and p.name!='EXP04_DELIVERY_MANIFEST.json' and not(p.suffix=='.log' and 'package' in p.name.lower())}
    write('EXP04_DELIVERY_MANIFEST.json',{'files':files,'required_deliverables':required,'HEAD':inp['HEAD'],'branch':inp['branch'],
        'verdict':'SUBSTANTIVE PARTIAL THEOREMS; RESUMABLE CHECKPOINT; UNIVERSAL TARGET OPEN',
        'excluded':['EXP04_DELIVERY_MANIFEST.json','live package*.log output (including versioned reproduction names)']})
    print(json.dumps({'files':len(files),'preflight_checks':check_count,'measured_CPU':total,
        'summary':summary,'tests':tests},indent=2),flush=True)
