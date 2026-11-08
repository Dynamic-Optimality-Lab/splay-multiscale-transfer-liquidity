"""Metadata-only source reconstruction; no allowance or group cap reset."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_UNARY_A_LIFT_14'
DIRECTIVE=Path('C:/Users/Saif malik/.codex/attachments/eeebd7eb-eba3-43e3-bdce-e1dccbd4c14d/Pasted text.txt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
prior=read(OLD/'dependency_pins.json');pins={p['path']:p for p in prior['pins']}
for p in read(OLD/'campaign_manifest.json')['files']:pins[p['path']]={'path':p['path'],'sha256':p['sha256'],'origin':'sealed_unary14'}
manifest=(OLD/'campaign_manifest.json').relative_to(ROOT).as_posix()
pins[manifest]={'path':manifest,'sha256':sha(OLD/'campaign_manifest.json'),'origin':'latest_manifest'}
for p in pins.values():assert sha(ROOT/p['path'])==p['sha256'],p['path']
external=prior['external_pins']+[{'path':str(DIRECTIVE),'sha256':sha(DIRECTIVE),'origin':'current_directive'}]
for p in external:assert sha(Path(p['path']))==p['sha256'],p['path']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_CPU']==3590.875
assert r['cumulative_group_CPU']=={'symbolic':102.984375,'independent':286.515625}
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS_ALL_AUTHORITATIVE_LOCAL_AND_DIRECTIVE_PINS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':external})
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'no_cap_reset':True,
    'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
with (B/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(DIRECTIVE.read_text())
print(json.dumps({'status':'ENTRY_VERIFIED','pins':len(pins),'CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}),flush=True)
