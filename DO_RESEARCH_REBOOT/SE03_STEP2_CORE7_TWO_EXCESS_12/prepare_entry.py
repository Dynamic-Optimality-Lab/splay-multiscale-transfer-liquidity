"""Campaign12 metadata only: preserve all sealed dependencies and budgets."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_CORE7_SINGLE_EXCESS_11'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(path,h,origin):
    assert (ROOT/path).is_file() and sha(ROOT/path)==h,path
    if path not in pins:pins[path]={'path':path,'sha256':h,'origins':[]}
    assert pins[path]['sha256']==h;pins[path]['origins'].append(origin)
old=read(OLD/'dependency_pins.json')
for v in old['pins']:add(v['path'],v['sha256'],'inherited11')
for v in read(OLD/'campaign_manifest.json')['files']:add(v['path'],v['sha256'],'sealed11')
add((OLD/'campaign_manifest.json').relative_to(ROOT).as_posix(),sha(OLD/'campaign_manifest.json'),'manifest11')
req=Path('C:/Users/Saif malik/.codex/attachments/7b1ebf0c-333a-4945-beea-605130549281/Pasted text.txt')
ext=old['external_pins']+[{'path':str(req),'sha256':sha(req),'used_sections':'entire Campaign12 directive'}]
for v in ext:assert sha(Path(v['path']))==v['sha256']
r=read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU']==3415.84375 and r['remaining_CPU']==3784.15625
assert r['cumulative_group_CPU']=={'symbolic':66.5,'independent':147.96875}
assert git('branch','--show-current')=='coarse-double-branch'
assert git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
    'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,'canonical_query_cap':2000000,
    'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'no_cap_reset':True,'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('source_reconstruction.json',{'status':'PASS_FROZEN_BEFORE_PROOF_EXECUTION',
    'authoritative_predecessor':'Campaign11 seal_audit2.json and final manifest',
    'definitions':{'R':'actual last (Q-2H)+ demand slots per natural full macro',
        'a':'Campaign10 common locks plus successful partial h0/l paths',
        'Pstar':'D minus domain(a)','Wstar':'actual A units minus image(a)'},
    'new_scope':'core7, SIX genuine KEEP keys, EXACTLY TWO physical excess slots on aligned I',
    'proposed_bridge':'each critical H1Q3 has predecessor Q<=1; predecessor map is injective on distinct macros; h0 extends at two slots using distinct own-unused bits; simultaneous complete exchange preserves all old paths',
    'eligibility':'original actual-ID counting/block-cyclic complete h/l exchange on exact common C; no new native timing or terminal-key rule',
    'status_at_entry':'two-slot theorem OPEN; structural one-slot local facts accepted only at verified hypotheses',
    'old_changing_chart_normalization':'REFUTED unchanged',
    'no_additional_assumption':'no Hall premise, aggregate CD inequality, empty-owner assumption or invented fE',
    'Step2':'OPEN','CD6':'OPEN','Step3':'OPEN','missing_dependency':[]})
print(json.dumps({'status':'ENTRY_PINS_AND_BUDGET_VERIFIED','pins':len(pins),'CPU':r['cumulative_CPU'],'remaining':r['remaining_CPU']}))
