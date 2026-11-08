"""Append-only Step1 continuation; provenance bookkeeping only."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent
OLD=B.parent/'SE03_NONREJOIN01';start=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
pins={}
def add(p,h,origin):
    k=p.relative_to(ROOT).as_posix();assert sha(p)==h,k
    if k in pins:assert pins[k]['sha256']==h;pins[k]['origins'].append(origin)
    else:pins[k]={'path':k,'sha256':h,'origins':[origin]}
for p in read(OLD/'dependency_pins.json')['pins']:
    add(ROOT/p['path'],p['sha256'],'SE03 inherited declared pin')
for p in read(OLD/'checkpoint_manifest.json')['files']:
    add(OLD/p['file'],p['sha256'],'SE03 checkpoint; inherited status OPEN')
add(OLD/'checkpoint_manifest.json',sha(OLD/'checkpoint_manifest.json'),'SE03 checkpoint integrity')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_uniform_CPU']==3205.84375
out('dependency_pins.json',{'status':'PASS_ALL_INHERITED_HASHES','pins':sorted(pins.values(),key=lambda q:q['path'])})
out('entry.json',{'head':head,'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,
    'reserve':5,'inherited_group_CPU':{'symbolic':r['combined_phase_groups']['symbolic']['CPU'],
    'independent':r['combined_phase_groups']['independent']['CPU']},'group_caps':{'symbolic':120,'independent':300},
    'canonical_queries':2000000,'live_records':2000000,'compiled_DAG_nodes':4000000,'stored_edges':5000000,
    'memory_cap_bytes':32*1024**3,'per_phase_wall_hours':12,'Bank25':25,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time()-start,'no_allowance_or_group_cap_reset':True})
out('USER_REQUEST.json',{'request':'Complete Step1: use sealed M3 to fund every actual erased five-key/core-nine auxiliary double with identified original A-event units; proceed until this Step1 outcome is proved and audited.',
    'preserved_constraints':'R1-R4 and current caps; reuse completed checks; no finite tests; no inherited writes',
    'Step2_separate':'prove original signed marginal fits the explicitly available units',
    'Step3_separate':'source-complete arbitrary-support coverage'})
print(json.dumps({'status':'STEP1_ENTRY_PASS','pins':len(pins),'prior_uniform_CPU':r['cumulative_uniform_CPU']}))
