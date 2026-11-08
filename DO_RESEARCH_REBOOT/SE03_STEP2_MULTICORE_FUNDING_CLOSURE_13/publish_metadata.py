"""Exact cumulative resource and manifest publication after PARTIAL seal."""
import hashlib,json,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
def read(n):return json.loads((B/n).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
e=read('entry.json');total=e['prior_uniform_CPU'];groups=dict(e['inherited_group_CPU']);phases=[]
for p in sorted(B.glob('run_*_result.json')):
    r=json.loads(p.read_text());c=read('controller_'+r['phase']+'_exit.json')
    assert r['status']=='PASS' and not c['error'];charge=r['child_CPU']+c['whole_process_CPU_seconds']
    total+=charge;groups[r['group']]+=charge
    phases.append({'phase':r['phase'],'group':r['group'],'child_CPU':r['child_CPU'],
        'whole_controller_CPU':c['whole_process_CPU_seconds'],'charge':charge,'source_engine_calls':r['source_engine_calls'],
        'historical_period_rows':r['old_semantic_rows_replayed'],'status':r['status']})
assert read('seal_audit.json')['terminal_outcome']=='UNRESOLVED_MATHEMATICAL_PROOF_LIMIT'
assert total<7195 and all(groups[g]<e['group_caps'][g] for g in groups)
out('resources_checkpoint.json',{'status':'ALL_EXISTING_CAPS_PRESERVED','prior_CPU':e['prior_uniform_CPU'],
    'cumulative_CPU':total,'ceiling':7200,'required_reserve':5,'remaining_CPU':7200-total,
    'available_before_reserve':7195-total,'cumulative_group_CPU':groups,'group_caps':e['group_caps'],
    'remaining_group_CPU':{g:e['group_caps'][g]-groups[g] for g in groups},'phases':phases,
    'campaign_source_engine_calls':sum(p['source_engine_calls'] for p in phases),'query_live_cap':2000000,
    'DAG_cap':4000000,'edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'no_reset':True,
    'stopping_reason':'MATHEMATICAL_PROOF_LIMIT_NOT_RESOURCE_EXHAUSTION',
    'metadata_convention':'unchanged inherited entry/provenance/prose/publication exclusion; all proof/route/source/check/seal and whole controller CPU charged',
    'this_publication_metadata_CPU_excluded':time.process_time()})
out('publication_receipt.json',{'status':'SEALED_PARTIAL_CAMPAIGN13','branch':e['branch'],'HEAD':e['head'],
    'tracked_status':'','old_research':'preserved; new paths only13','outcome':'UNRESOLVED',
    'core7':'COMPLETE','core8':'COMPLETE','core9':'RESTRICTED_ONLY','core10':'OPEN','core11':'OPEN',
    'Gate_U13':'U-B','Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','CPU':total,'remaining_CPU':7200-total})
files=[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(B.rglob('*')) if p.is_file()]
out('campaign_manifest.json',{'status':'SEALED_PARTIAL_MULTICORE_CAMPAIGN','terminal_outcome':'UNRESOLVED',
    'branch':e['branch'],'HEAD':e['head'],'files':files,'self_hash':'manifest excludes itself; console receipt gives its SHA256',
    'artifact_status_reference':'artifact_status_ledger.json','Step2':'OPEN','CD6':'OPEN','Universal_CD':'OPEN','Dynamic_Optimality':'OPEN'})
assert all(sha(ROOT/v['path'])==v['sha256'] for v in files)
print(json.dumps({'status':'PARTIAL_MANIFEST_ALL_BYTES_VERIFIED','files':len(files),'manifest_sha256':sha(B/'campaign_manifest.json'),
    'CPU':total,'remaining_CPU':7200-total,'groups':groups,'outcome':'UNRESOLVED'}))
