"""Campaign07 source reconstruction and unchanged cumulative allowances."""
import collections,hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_TERMINAL_PAIR_06'
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
for p in read(OLD/'campaign_manifest.json')['files']:add(ROOT/p['path'],p['sha256'],'accepted Campaign06 manifest')
add(OLD/'campaign_manifest.json',sha(OLD/'campaign_manifest.json'),'Campaign06 manifest itself')
attachment=Path('C:/Users/Saif malik/.codex/attachments/2fa12492-6af5-45f0-acf7-4d6d3154e02a/Pasted text.txt')
ext=old['external_pins']+[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'entire Campaign07 directive'}]
for p in ext:assert sha(Path(p['path']))==p['sha256']
resource=read(OLD/'resources_checkpoint.json');assert resource['cumulative_CPU']==3253.1875
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':'coarse-double-branch','tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':resource['cumulative_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':resource['cumulative_group_CPU'],'group_caps':{'symbolic':120,'independent':300},
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':34359738368,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time(),'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
inspections=[]
for name in ('FULL_PROOF.md','CASE_LEDGER.md','saturation3.json','independent_audit.json','adversarial_audit.json',
             'interface_audit.json','INDEPENDENT_AUDIT.md','campaign_manifest.json','seal_audit.json','resources_checkpoint.json','CHECKPOINT.md'):
    p=OLD/name;d=read(p) if p.suffix=='.json' else p.read_text()
    item={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size,'status':'accepted inherited interface; not reopened'}
    if name=='saturation3.json':
        item.update({'closed':d['closed'],'goal':d['goal'],'records':len(d['records']),
            'leaf_budget_observations':dict(collections.Counter((str(r['budget']) for r in d['records'])))})
    if isinstance(d,dict) and 'status' in d:item['recorded_status']=d['status']
    inspections.append(item)
out('source_inspection.json',{'status':'PASS_CURRENT_LOCAL_SOURCE_RECONSTRUCTION','Campaign06_inspected':inspections,
    'invalid_saturation_json':'preserved, excluded from proof inheritance',
    'critical_source_gaps':[],'old_normalization':'REFUTED','Step2':'OPEN','TP_DEPTH3':'PROVED at sealed scope'})
out('USER_REQUEST.json',{'target':'FINAL-PLUS1: T11^-2 intersect Pre0*(Pre+1_H1Q1(F11_q4)) is empty',
    'return':'zero prefix of arbitrary finite length, then sole H1Q1 +1; both NEG2 source classes',
    'source':'original reachable exactly A/BF/BE paired-closed core11, actual charts and all operations',
    'terminal_outcomes':['A','E','UNRESOLVED_RESOURCE_OR_PROOF_LIMIT'],
    'mandatory_controls_replay_authorized':True,'no_new_debt_or_frozen_edits':True})
print(json.dumps({'status':'PASS','pins':len(pins),'prior_CPU':resource['cumulative_CPU']}))
