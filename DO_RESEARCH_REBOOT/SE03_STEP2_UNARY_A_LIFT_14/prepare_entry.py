"""Metadata continuation; no CPU/cap reset and no frozen research writes."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(path,h,origin):
    assert sha(ROOT/path)==h,path
    if path not in pins:pins[path]={'path':path,'sha256':h,'origins':[]}
    assert pins[path]['sha256']==h;pins[path]['origins'].append(origin)
prior=read(OLD/'dependency_pins.json')
for v in prior['pins']:add(v['path'],v['sha256'],'inherited13')
for v in read(OLD/'campaign_manifest.json')['files']:add(v['path'],v['sha256'],'sealed13')
add((OLD/'campaign_manifest.json').relative_to(ROOT).as_posix(),sha(OLD/'campaign_manifest.json'),'manifest13')
for v in prior['external_pins']:assert sha(Path(v['path']))==v['sha256']
r=read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU']==3507.703125 and r['remaining_CPU']==3692.296875
assert r['cumulative_group_CPU']=={'symbolic':81.859375,'independent':224.46875}
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':prior['external_pins']})
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'no_cap_reset':True,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
with (B/'USER_REQUEST.txt').open('x',encoding='utf-8') as f:f.write('Close the core9 unary anonymous A-ancestor lifting gap, then continue until cores 9–11 funding is closed. Preserve R1–R4, Bank25, frozen owners and current caps; reuse completed proofs and independently audit each new certificate.\n')
print(json.dumps({'status':'ENTRY_PINS_AND_CAPS_VERIFIED','pins':len(pins),'CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}))
