"""Append-only entry for full-source invariant construction."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_DONOR04';start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
pins={}
def add(p,h,origin):
    assert sha(p)==h,p
    key=p.relative_to(ROOT).as_posix()
    if key in pins:assert pins[key]['sha256']==h;pins[key]['origins'].append(origin)
    else:pins[key]={'path':key,'sha256':h,'origins':[origin]}
for p in read(OLD/'dependency_pins.json')['pins']:add(ROOT/p['path'],p['sha256'],'inherited')
for p in read(OLD/'checkpoint_manifest.json')['files']:add(OLD/p['file'],p['sha256'],'DONOR04 checkpoint')
add(OLD/'checkpoint_manifest.json',sha(OLD/'checkpoint_manifest.json'),'DONOR04 manifest')
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_uniform_CPU']==3216.09375
assert len(pins)==1338
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
out('dependency_pins.json',{'status':'PASS_INHERITED_PINS','pins':sorted(pins.values(),key=lambda q:q['path'])})
out('entry.json',{'head':head,'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':{g:v['combined_CPU'] for g,v in r['original_SE03_phase_groups'].items()},
    'group_caps':{'symbolic':120,'independent':300},'canonical_query_cap':2000000,'live_record_cap':2000000,
    'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
    'Bank25':25,'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-start,'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('USER_REQUEST.json',{'target':'Use completed machinery to close universal six-key Step2 via full source allocation and exchange',
    'constraints':['R1-R4','Bank25','current caps','existing allocations','reuse completed proofs','no finite tests'],
    'universal_promotion_requires':'explicit source funding invariant, every source obligation, full ownership, closure and independent audit'})
print(json.dumps({'status':'ENTRY_PASS','pins_verified':len(pins),'prior_uniform_CPU':r['cumulative_uniform_CPU']}))
