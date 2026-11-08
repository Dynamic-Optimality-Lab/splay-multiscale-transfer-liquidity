"""Preserved private full-high control harness, with fresh depths and outputs."""
from pathlib import Path
p=Path('DO_RESEARCH_REBOOT/M2_DSK01/verify_full_high.py')
s=p.read_text();s=s[:s.index('start=time.process_time();records=[]')]
s=s.replace("Path('DO_RESEARCH_REBOOT/M2_DSK01/full_high_controls.json')", "Path('DO_RESEARCH_REBOOT/M3_OUT01/high_controls.json')")
s=s.replace("'potential_checked':accepted,", "'environment':env,'potential_checked':accepted,")
s+='''
start=time.process_time();records=[]
prior=json.loads(Path('DO_RESEARCH_REBOOT/M2_DSK01/full_high_controls.json').read_text())
points=[r for r in prior['records'] if r['label'].startswith('positive_')]
for j,r in enumerate(points):
    for depth in range(10,14):
        records.append(check(r['source'],r['target'],depth,r['sigma'],f'outside_cheap_candidate_{j}_d{depth}',False))
    records.append(check(r['source'],r['target'],r['d'],r['sigma'],f'positive_boundary_{j}',True))
    assert time.process_time()-start<300,'UNKNOWN high-control cap'
for r in prior['records']:
    if not r['label'].startswith('potential_boundary_clean_h0'):continue
    for depth in (10,11,12,13,18):
        records.append(check(r['source'],r['target'],depth,r['sigma'],r['label']+f'_newd{depth}',True))
        assert chi(records[-1]['destination'])
for r in records:
    assert d.ev_ground(H['root'],r['environment'])==r['expected']
res={'status':'PASS','queries':len(records),'accepted':sum(r['high_root'] for r in records),
     'rejected_cheap_dirty_candidates':sum(not r['high_root'] for r in records),
     'clean_h0_correction_retained':True,'DAG_nodes':len(d.nodes),
     'cpu_seconds':round(time.process_time()-start,3),'records':records}
with OUT.open('x',encoding='utf-8') as f:json.dump(res,f,indent=2)
print(json.dumps({k:v for k,v in res.items() if k!='records'},indent=2))
'''
out=Path('DO_RESEARCH_REBOOT/M3_OUT01/high_audit.py')
with out.open('x',encoding='utf-8') as f:f.write(s)
print('Prepared fresh original high audit.')
