"""Read-only inherited provenance and exclusive creation of SE03 metadata."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent
ROOT=B.parent.parent
def xp(p): return Path('\\\\?\\'+str(p.resolve()))
def read(p): return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (B/n).open('x',encoding='utf-8') as f: json.dump(d,f,indent=2)
start=time.process_time(); old=B.parent/'SE02_ERASURE01'; pins={}
def add(p,h,origin):
    p=Path(p); k=p.relative_to(ROOT).as_posix(); assert sha(p)==h,k
    if k in pins:
        assert pins[k]['sha256']==h
        pins[k]['origins'].append(origin)
    else: pins[k]={'path':k,'sha256':h,'origins':[origin]}
for d in read(old/'dependency_pins.json')['pins']:
    add(ROOT/d['path'],d['sha256'],'inherited SE02 declared input')
for d in read(old/'final_manifest_v2.json')['files']:
    add(old/d['file'],d['sha256'],'sealed SE02 final v2')
add(old/'final_manifest_v2.json',sha(old/'final_manifest_v2.json'),'entry pin of SE02 seal')
fe=B.parent/'06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_fe01_first_entry_20261101_v001'
for n in ['FE01_UNIVERSAL_ENTRY_SHIFT_THEOREM.md','FE02_SOURCE_EXACT_DEPTH_AND_CEILING.md','proof_status_ledger.json','delivery_manifest.json']:
    p=fe/n; add(p,sha(p),'FE01 source geometry reference only; no unproved completeness premise')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert branch=='coarse-double-branch'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
res=read(old/'resources_final_v2.json'); assert res['cumulative_uniform_CPU']==3201.375
directive=Path('C:/Users/Saif malik/.codex/attachments/aeaca490-b810-429c-9209-cdc8d31fb118/Pasted text.txt')
with (B/'USER_DIRECTIVE.txt').open('x',encoding='utf-8') as f:f.write(directive.read_text(encoding='utf-8'))
write('dependency_pins.json',{'status':'ALL_EXISTING_DECLARED_HASHES_MATCH','pins':sorted(pins.values(),key=lambda x:x['path']),
    'directive_path':str(directive),'directive_sha256':sha(directive)})
write('entry.json',{'head':head,'branch':branch,'tracked_tree_clean':True,'prior_uniform_CPU':3201.375,
    'global_allowance':7200,'remaining_CPU_including_reserve':3998.625,'required_reserve':5,
    'symbolic_CPU_cap':120,'audit_CPU_cap':300,'canonical_query_cap':2000000,'live_record_cap':2000000,
    'input_DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
    'old_signature_ledger_unchanged':7195.203125,'declared_pins_verified':len(pins),
    'matching_terminal_modified':False,'Bank25':25,'metadata_CPU_excluded':time.process_time()-start})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((old/'run_phase.py').read_text())
print(json.dumps({'status':'SE03_ENTRY_PASS','pins':len(pins),'prior_uniform_CPU':3201.375}))
