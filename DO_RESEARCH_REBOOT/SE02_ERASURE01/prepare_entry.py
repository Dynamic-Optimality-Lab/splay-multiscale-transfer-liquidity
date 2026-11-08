"""Provenance-only entry; no research imports or semantic queries."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent
R=B.parent
ROOT=R.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time();prior=R/'CD_UNIFORM01';pins={}
def add(p,h,origin):
    p=Path(p);k=p.relative_to(ROOT).as_posix();assert sha(p)==h,k
    if k in pins:assert pins[k]['sha256']==h;pins[k]['origins'].append(origin)
    else:pins[k]={'path':k,'sha256':h,'origins':[origin]}
for p in read(prior/'dependency_pins.json')['pins']:
    add(ROOT/p['path'],p['sha256'],'CD_UNIFORM01 declared input pin')
for p in read(prior/'final_manifest.json')['files']:
    add(prior/p['file'],p['sha256'],'CD_UNIFORM01 final publication')
add(prior/'final_manifest.json',sha(prior/'final_manifest.json'),'entry pin of existing partial publication')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
res=read(prior/'resources_final.json');assert res['cumulative_uniform_CPU']==3197.78125
directive=Path('C:/Users/Saif malik/.codex/attachments/ec91c3c7-fb26-43f5-837f-4ecafd22b57c/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(directive.read_text(encoding='utf-8'))
write('dependency_pins.json',{'status':'ALL_EXISTING_DECLARED_HASHES_MATCH','pins':sorted(pins.values(),key=lambda x:x['path']),
  'user_directive_path':str(directive),'user_directive_sha256':sha(directive)})
write('entry.json',{'head':head,'tracked_tree_clean':True,'prior_uniform_CPU':3197.78125,'global_allowance':7200,
  'remaining_CPU_including_reserve':4002.21875,'required_reserve':5,'symbolic_CPU_cap':120,'audit_CPU_cap':300,
  'canonical_query_cap':2000000,'live_record_cap':2000000,'input_DAG_cap':4000000,'stored_edge_cap':5000000,
  'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'old_signature_ledger_unchanged':7195.203125,
  'declared_pins_verified':len(pins),'matching_terminal_modified':False,'metadata_CPU_excluded':time.process_time()-start})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((prior/'run_phase.py').read_text())
print(json.dumps({'status':'ENTRY_PASS','declared_pins':len(pins)}))
