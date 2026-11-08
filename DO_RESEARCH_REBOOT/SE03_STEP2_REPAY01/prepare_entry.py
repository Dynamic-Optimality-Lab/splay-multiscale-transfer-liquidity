"""Append-only Step2 provenance bookkeeping; no source or proof engines."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP1_FUND01'
start=time.process_time()
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
for p in read(OLD/'dependency_pins.json')['pins']:add(ROOT/p['path'],p['sha256'],'inherited input')
for p in read(OLD/'final_manifest.json')['files']:add(OLD/p['file'],p['sha256'],'sealed Step1')
add(OLD/'final_manifest.json',sha(OLD/'final_manifest.json'),'sealed Step1 manifest')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
r=read(OLD/'resources_final.json');assert r['cumulative_uniform_CPU']==3207.125
out('dependency_pins.json',{'status':'PASS_ALL_INHERITED_HASHES','pins':sorted(pins.values(),key=lambda p:p['path'])})
out('entry.json',{'head':head,'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':{k:v['combined_CPU'] for k,v in r['original_SE03_phase_groups'].items()},
    'group_caps':{'symbolic':120,'independent':300},'canonical_query_cap':2000000,'live_record_cap':2000000,
    'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
    'Bank25':25,'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-start,'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('USER_REQUEST.json',{'request':'Complete Step2 signed repayment into the explicit Step1 reserve and negative-interference releases; continue investigating until genuinely proved; do not replace the target by a restricted or circular result.',
    'constraints':'R1-R4, inherited caps, no finite tests, reuse completed proofs, separate source/math audit'})
print(json.dumps({'status':'STEP2_ENTRY_PASS','pins':len(pins),'prior_uniform_CPU':r['cumulative_uniform_CPU']}))
