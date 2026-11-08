"""Campaign10 local reconstruction and cumulative entry; metadata only."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_CORE11_RETURN_ASSEMBLY_09'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(path,h,origin):
    p=ROOT/path;assert p.is_file() and sha(p)==h,path
    if path not in pins:pins[path]={'path':path,'sha256':h,'origins':[]}
    assert pins[path]['sha256']==h;pins[path]['origins'].append(origin)
old=read(OLD/'dependency_pins.json')
for v in old['pins']:add(v['path'],v['sha256'],'inherited')
for v in read(OLD/'campaign_manifest.json')['files']:add(v['path'],v['sha256'],'accepted09 manifest')
add((OLD/'campaign_manifest.json').relative_to(ROOT).as_posix(),sha(OLD/'campaign_manifest.json'),'accepted09 manifest itself')
req=Path('C:/Users/Saif malik/.codex/attachments/e0741678-81f6-4fc8-893b-6dbac104a40f/Pasted text.txt')
ext=old['external_pins']+[{'path':str(req),'sha256':sha(req),'used_sections':'entire Campaign10 directive'}]
for v in ext:assert sha(Path(v['path']))==v['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_CPU']==3399.796875
assert git('branch','--show-current')=='coarse-double-branch'
assert git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
    'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'no_cap_reset':True,'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('source_reconstruction.json',{'status':'PASS_LOCAL_SCOPE_RECONSTRUCTION',
    'accepted09':'full source proof/physical interface/checkpoint/independent audit/manifests/seal inspected; no reopening',
    'Step1_scope':'explicit debt allocator for aligned five-key/core9 auxiliary; arbitrary smaller aux core not silently included',
    'CD5':'complete support<=5 scalar theorem, independent of requested CD6',
    'full_core_sizes':[6,7,8,9,10,11],'fixed_labeled_full_core':'constant on each closed period, no size switching',
    'source_semantic_clarification':'BF processes ALL KEEP operations; nongenuine root repeats are exact BF identities, A work and BE action retained',
    'critical_missing_input':[],'old_normalization':'REFUTED unchanged','Step2':'OPEN'})
print(json.dumps({'status':'PASS','pins':len(pins),'prior_CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}))
