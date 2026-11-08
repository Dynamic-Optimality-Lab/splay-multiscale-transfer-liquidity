"""Campaign08 frozen source provenance and cumulative controls; no cap reset."""
import collections,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_FINAL_PLUS_ONE_07'
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
for p in read(OLD/'campaign_manifest.json')['files']:add(ROOT/p['path'],p['sha256'],'Campaign07 manifest')
add(OLD/'campaign_manifest.json',sha(OLD/'campaign_manifest.json'),'Campaign07 manifest itself')
attachment=Path('C:/Users/Saif malik/.codex/attachments/2905c573-81f2-441f-a7fb-ec8fd7bf9df5/Pasted text.txt')
ext=old['external_pins']+[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'entire Campaign08 directive'}]
for p in ext:assert sha(Path(p['path']))==p['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_CPU']==3328.53125
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':'coarse-double-branch','tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':{'symbolic':120,'independent':300},
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':34359738368,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time(),'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
inspect=[]
for name in ('SOURCE_SPEC.md','FULL_PROOF.md','CASE_LEDGER.md','INDEPENDENT_AUDIT.md','TERMINAL_SEEDS.md',
    'ZERO_PREDECESSOR_CLOSURE.md','terminal_seeds.json','zero_closure.json','independent_audit2.json',
    'adversarial_audit.json','source_control_replay2.json','delete_event_control.json','campaign_manifest.json','seal_audit.json','CHECKPOINT.md'):
    p=OLD/name;item={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'status':'current accepted interface inspected/reused'}
    if p.suffix=='.json':
        d=read(p)
        if 'status' in d:item['recorded_status']=d['status']
        if name=='zero_closure.json':item.update({'closed':d['closed'],'records':len(d['records']),'bound':d['bound']})
    inspect.append(item)
out('source_inspection.json',{'status':'PASS_CURRENT_LOCAL_SOURCE_RECONSTRUCTION','Campaign07':inspect,
    'Campaign06_authority':'accepted saturation3.json and seal verified by inherited pins; invalid saturation.json never used',
    'earlier_sources':'Campaign01-05 current accepted specifications/checkpoints inspected and inherited by hash',
    'TP_DEPTH3':'PROVED sealed scope','FINAL_PLUS1':'PROVED sealed scope','old_chart_normalization':'REFUTED',
    'P1Z_RETURN':'OPEN at entry','Step2':'OPEN','critical_missing_dependencies':[]})
out('USER_REQUEST.json',{'target':'P1Z-RETURN: T11^-2 intersect Pre0*(Pre+1(Pre0_final(F11_q4))) is empty',
    'P1_A':'H1Q1','P1_B':'H2Q3, must prove exclusion or cover','final_zero':'source-exact H1Q2 neutral2->2',
    'domain':'original closed six-genuine-KEEP core11, arbitrary private BSTs and charts, both NEG2 starts',
    'outcomes':['A','E','UNRESOLVED_RESOURCE_OR_PROOF_LIMIT'],'no_new_debt_or_allocation':True})
print(json.dumps({'status':'PASS','pins':len(pins),'prior_CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}))
