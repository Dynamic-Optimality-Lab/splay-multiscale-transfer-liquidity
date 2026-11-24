"""Verify unchanged inputs, summarize measured resources, hash final delivery."""
from exp03_core import *
from exp03_inheritance import file_hash
import subprocess


if __name__=='__main__':
    cpu=timing.process_time();wall=timing.perf_counter()
    inputs=json.loads((ROOT/'EXP03_INPUT_MANIFEST.json').read_text())
    for p,h in inputs['EXP02_complete_delivery_hashes_verified'].items():assert file_hash(OLD/p)==h
    for p,h in inputs['additional_repository_pins'].items():assert file_hash(REPO/p)==h
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO,text=True).strip()==inputs['HEAD']
    assert subprocess.check_output(['git','branch','--show-current'],cwd=REPO,text=True).strip()==inputs['branch']
    required=['EXP03_DISCOVERY_REPORT.md','EXP03_UNHANDLED_PARENT_INVENTORY.json','EXP03_OMITTED_HIT_EPISODES.json',
        'EXP03_MISSING_GRANDPARENT_EPISODES.json','EXP03_SOURCE_WITNESSES.json','EXP03_CAUSAL_EPISODE_RESULTS.json',
        'EXP03_THEOREM_AND_REFUTATION_LEDGER.md','EXP03_REPRODUCTION.md']
    assert all((ROOT/p).is_file() for p in required)
    tests=json.loads((ROOT/'EXP03_TEST_RESULTS.json').read_text());assert tests['status']=='PASS'
    summary=json.loads((ROOT/'EXP03_SUMMARY.json').read_text())
    assert summary['new']['sources']==89 and summary['source_count']==260
    assert summary['new']['unhandled_gaps']==270 and summary['new']['remaining']==110
    archive=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
    canonical_names={s['name'] for s in archive['new_sources']}
    extra_pilots={}
    for file in ('EXP03_OUTSIDE_PILOT.json','EXP03_OUTSIDE_BOUNDARY_PILOT.json'):
        for row in json.loads((ROOT/file).read_text()):
            if row['source']['name'] not in canonical_names:extra_pilots[row['source']['name']]=file
    # Count all named complete pilot records conservatively, even where an
    # earlier pilot used the same physical word/state under an older name.
    assert len(canonical_names)+len(extra_pilots)<=100
    write('EXP03_RESOURCE_package.json',{'stage':'package','status':'completed','process_CPU_seconds':timing.process_time()-cpu,
        'wall_seconds':timing.perf_counter()-wall,'memory':memory(),
        'measurement_boundary':'input/delivery preflight; subsequent resource-summary serialization and final file hashing excluded from this small stage measurement'})
    stages=[json.loads(p.read_text()) for p in sorted(ROOT.glob('EXP03_RESOURCE_*.json')) if p.name!='EXP03_RESOURCE_SUMMARY.json']
    total_cpu=sum(s['process_CPU_seconds'] for s in stages)
    assert total_cpu<=1000,total_cpu
    resource={'recorded_process_CPU_seconds':total_cpu,'sum_recorded_stage_wall_seconds':sum(s['wall_seconds'] for s in stages),
        'peak_working_set_bytes':max(s['memory']['peak_working_set_bytes'] for s in stages),
        'peak_pagefile_bytes':max(s['memory']['peak_pagefile_bytes'] for s in stages),'stages':stages,
        'bounds':{'new_sources':100,'physical_population':513,'operations_per_source':20000,'recorded_CPU_seconds':1000},
        'actual':{'canonical_new_sources':summary['new']['sources'],'new_named_complete_source_records_including_pilots':len(canonical_names)+len(extra_pilots),
            'additional_pilot_records':extra_pilots,'physical_population':summary['maximum_population'],'operations_per_source':summary['maximum_source_operations']},
        'unmeasured':'Interactive shell inspections, brief diagnostic snippets without Meter, prose drafting, and final manifest hashing are not included. No total session CPU or peak across every interactive tool process is claimed.'}
    write('EXP03_RESOURCE_SUMMARY.json',resource)
    files={str(p.relative_to(ROOT)).replace('\\','/'):file_hash(p) for p in ROOT.rglob('*') if p.is_file() and p.name not in ('EXP03_DELIVERY_MANIFEST.json','EXP03_PACKAGE.log')}
    write('EXP03_DELIVERY_MANIFEST.json',{'files':files,'historical_input_hashes_rechecked':len(inputs['EXP02_complete_delivery_hashes_verified']),
        'HEAD':inputs['HEAD'],'branch':inputs['branch'],'required_deliverables':required,'mathematical_verdict':'SUBSTANTIVE PARTIAL QUANTITATIVE PASS; universal residual closure open',
        'excluded_self_or_live_output':['EXP03_DELIVERY_MANIFEST.json','EXP03_PACKAGE.log']})
    print(json.dumps({'files':len(files),'CPU_seconds':total_cpu,'peak_working_set_bytes':resource['peak_working_set_bytes'],
        'tests':tests,'summary':summary},indent=2),flush=True)
