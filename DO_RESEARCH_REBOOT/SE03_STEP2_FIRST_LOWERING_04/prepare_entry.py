"""Campaign04 entry provenance and unchanged cumulative accounting."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_LEAF_LOWERING_03'
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
pins={}
def add(p,h,origin):
    assert sha(p)==h,str(p)
    rel=p.relative_to(ROOT).as_posix()
    if rel in pins:assert pins[rel]['sha256']==h;pins[rel]['origins'].append(origin)
    else:pins[rel]={'path':rel,'sha256':h,'origins':[origin]}
old=read(OLD/'dependency_pins.json')
for p in old['pins']:add(ROOT/p['path'],p['sha256'],'inherited')
for p in read(OLD/'campaign_manifest.json')['files']:add(ROOT/p['path'],p['sha256'],'Campaign03 manifest')
add(OLD/'campaign_manifest.json',sha(OLD/'campaign_manifest.json'),'Campaign03 manifest itself')
attachment=Path('C:/Users/Saif malik/.codex/attachments/0ece12bc-2029-4899-beda-da676c3bff65/Pasted text.txt')
ext=old['external_pins']+[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'entire Campaign04 request'}]
for p in ext:assert sha(Path(p['path']))==p['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_uniform_CPU']==3230.265625
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
assert git('branch','--show-current')=='coarse-double-branch'
assert git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':'coarse-double-branch','tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=normal'),
    'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':{g:v['combined_CPU'] for g,v in r['original_SE03_phase_groups'].items()},
    'group_caps':{'symbolic':120,'independent':300},'canonical_query_cap':2000000,'live_record_cap':2000000,
    'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':34359738368,'wall_cap_hours':12,
    'Bank25':25,'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time(),'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('USER_REQUEST.json',{'target':'core11 E0/E1 first-lowering reachability; source-exact entry or universal exclusion',
    'local_task':'NEG2 exit, nonlowering H1Q2 prefixes and at most one H1Q1 intervention',
    'no_new_debt':True,'source_testing':'Gate F authorized bounded exact source tests',
    'constraints':['R1-R4','Bank25','all allocations fixed','all cumulative caps','no frozen graph edits'],
    'terminal_outcomes':['A','B','C','D','E']})
print(json.dumps({'status':'PASS','pins':len(pins),'cumulative_CPU':r['cumulative_uniform_CPU']}))
