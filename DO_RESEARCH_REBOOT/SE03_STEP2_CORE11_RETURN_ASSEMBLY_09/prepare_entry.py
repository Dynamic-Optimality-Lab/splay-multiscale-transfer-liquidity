"""Campaign09 authoritative local source pins and cumulative resource entry."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_PLUS_ONE_ZERO_TAIL_08'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(p,h,origin):
    assert p.is_file() and sha(p)==h,str(p)
    key=p.relative_to(ROOT).as_posix()
    if key in pins:assert pins[key]['sha256']==h;pins[key]['origins'].append(origin)
    else:pins[key]={'path':key,'sha256':h,'origins':[origin]}
old=read(OLD/'dependency_pins.json')
for p in old['pins']:add(ROOT/p['path'],p['sha256'],'inherited')
for p in read(OLD/'campaign_manifest.json')['files']:add(ROOT/p['path'],p['sha256'],'Campaign08 manifest')
add(OLD/'campaign_manifest.json',sha(OLD/'campaign_manifest.json'),'Campaign08 manifest itself')
attachment=Path('C:/Users/Saif malik/.codex/attachments/bb51b8cf-85f6-41a0-9ba7-fa1e6bd477e2/Pasted text.txt')
ext=old['external_pins']+[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'entire Campaign09 directive'}]
for p in ext:assert sha(Path(p['path']))==p['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_CPU']==3348.671875
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':'coarse-double-branch','tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'],'directive_stale_CPU':3328.53125,'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':{'symbolic':120,'independent':300},
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':34359738368,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time(),'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
inspections=[]
for name in ('SOURCE_SPEC.md','FULL_PROOF.md','FINAL_VERDICT.md','CHECKPOINT.md','final_zero_inverse.json',
    'terminal_seeds.json','zero_closure.json','separator.json','independent_audit.json','adversarial_audit.json',
    'source_control_replay.json','seal_audit.json','campaign_manifest.json'):
    p=OLD/name;item={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'status':'accepted local08 interface inspected/reused'}
    if p.suffix=='.json':
        d=read(p)
        if 'status' in d:item['recorded_status']=d['status']
        if name=='zero_closure.json':item.update({'closed':d['closed'],'records':len(d['records']),'bound':d['bound']})
    inspections.append(item)
out('source_inspection.json',{'status':'PASS_CURRENT_LOCAL_RECONSTRUCTION','Campaign08':inspections,
    'accepted06':'saturation3.json, proof/audits/seal pinned; invalid saturation.json never a premise',
    'accepted07':'terminal_seeds,zero_closure,independent_audit2,seal/manifest pinned, exact scope retained',
    'earlier_sources':'original semantics, negative classification, actual q5/q1 successor, density, M3 and auxiliary allocation inspected/reused',
    'critical_missing_dependencies':[],'full_signed_or_physical_Step2':'OPEN'})
out('USER_REQUEST.json',{'target':'CORE11-RETURN: T11^-2 intersect Pre_R01(F11_q4 union F11_q5q1) is empty',
    'R01':'0* union 0*1 0*; no interior negative or weight>=2 edges',
    'paired_destination':'actual full q5 macro AND actual q1 successor, H1 each, both A/BE/chart trajectories retained',
    'budget_product':'initial b1 at paired sources; backward +1 consumes it; zeros preserve b; b is proof metadata only',
    'terminal_outcomes':['A','E','UNRESOLVED_RESOURCE_OR_PROOF_LIMIT'],'no_new_debt_or_allocation':True})
print(json.dumps({'status':'PASS','pins':len(pins),'prior_CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}))
