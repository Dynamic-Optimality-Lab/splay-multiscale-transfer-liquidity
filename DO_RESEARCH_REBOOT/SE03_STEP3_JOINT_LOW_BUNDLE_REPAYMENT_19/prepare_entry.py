"""Metadata-only C19 continuation freeze; no source or audit work."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18'
DIRECTIVE=Path('C:/Users/Saif malik/.codex/attachments/b1985215-a831-4415-b898-2af2571e2490/Pasted text.txt')
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
prior=read(OLD/'dependency_pins.json');pins={x['path']:x for x in prior['pins']}
for x in read(OLD/'campaign_manifest.json')['files']:
    pins[x['path']]={'path':x['path'],'sha256':x['sha256'],'origin':'C18_CONTENT_CHECKPOINT_AUDIT_PENDING'}
q=(OLD/'campaign_manifest.json').relative_to(ROOT).as_posix()
pins[q]={'path':q,'sha256':sha(OLD/'campaign_manifest.json'),'origin':'C18_manifest'}
for x in pins.values():assert sha(ROOT/x['path'])==x['sha256'],x['path']
external=list(prior['external_pins'])
external.append({'path':str(DIRECTIVE),'sha256':sha(DIRECTIVE),'origin':'C19_user_directive'})
for x in external:assert sha(Path(x['path']))==x['sha256'],x['path']
r=read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU']==3616.671875 and r['cumulative_group_CPU']=={'symbolic':116.171875,'independent':299.125}
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'ENTRY_PROVENANCE_NOT_AUDIT','pins':sorted(pins.values(),key=lambda x:x['path']),'external_pins':external})
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),
 'tracked_status':'','worktree_status':git('status','--porcelain','--untracked-files=all'),
 'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
 'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
 'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
 'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,
 'pins_verified':len(pins),'no_cap_reset':True,'independent_remaining':0.875,
 'symbolic_remaining':3.828125,'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text(encoding='utf-8'))
with (B/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(DIRECTIVE.read_text(encoding='utf-8'))
print(json.dumps({'status':'C19_ENTRY_FROZEN','pins':len(pins),'symbolic_remaining':3.828125,'independent_remaining':0.875}))
