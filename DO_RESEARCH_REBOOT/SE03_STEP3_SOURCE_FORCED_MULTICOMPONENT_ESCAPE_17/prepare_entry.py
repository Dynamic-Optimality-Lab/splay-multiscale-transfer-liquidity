"""Metadata-only C17 source freeze; not the unfinished C15 audit suffix."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16'
REQUEST=Path('C:/Users/Saif malik/.codex/attachments/a0af24f4-32d6-4361-8d42-440cb5519085/Pasted text.txt')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def out(n,x):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
prior=read(OLD/'dependency_pins.json');pins={x['path']:x for x in prior['pins']}
for x in read(OLD/'campaign_manifest.json')['files']:
    pins[x['path']]={'path':x['path'],'sha256':x['sha256'],'origin':'C16_CONTENT_CHECKPOINT_NOT_PROOF_SEAL'}
mp=(OLD/'campaign_manifest.json').relative_to(ROOT).as_posix()
pins[mp]={'path':mp,'sha256':sha(OLD/'campaign_manifest.json'),'origin':'C16_manifest'}
for x in pins.values():assert sha(ROOT/x['path'])==x['sha256'],x['path']
external=prior['external_pins']+[{'path':str(REQUEST),'sha256':sha(REQUEST),'origin':'C17_directive'}]
for x in external:assert sha(Path(x['path']))==x['sha256'],x['path']
r=read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU']==3608.328125
assert r['cumulative_group_CPU']=={'symbolic':107.828125,'independent':299.125}
assert r['group_caps']=={'symbolic':120,'independent':300}
git=lambda *a:subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch'
assert git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'ENTRY_PROVENANCE_ONLY_NOT_INDEPENDENT_SEAL',
    'pins':sorted(pins.values(),key=lambda x:x['path']),'external_pins':external})
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),
    'tracked_status':'','worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
    'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,
    'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,
    'pins_verified':len(pins),'no_cap_reset':True,'metadata_CPU_excluded':time.process_time(),
    'C15_integrity_seal':'PENDING_CAP','C16_new_derivations':'AUDIT_PENDING_NOT_SEALED'})
with (B/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(REQUEST.read_text(encoding='utf-8'))
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text(encoding='utf-8'))
print(json.dumps({'status':'ENTRY_FROZEN','pins':len(pins),'CPU':r['cumulative_CPU'],
    'group_remaining':r['group_remaining'],'no_new_audit_allowance':True}),flush=True)
