"""Append-only Campaign02 provenance; inherited proofs and caps unchanged."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_COLD_NEG2_01';started=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
pins={}
def add(p,h,origin):
    assert sha(p)==h,str(p)
    key=p.relative_to(ROOT).as_posix()
    if key in pins:assert pins[key]['sha256']==h;pins[key]['origins'].append(origin)
    else:pins[key]={'path':key,'sha256':h,'origins':[origin]}
oldpins=read(OLD/'dependency_pins.json')
for p in oldpins['pins']:add(ROOT/p['path'],p['sha256'],'inherited')
for p in read(OLD/'checkpoint_manifest.json')['files']:add(OLD/p['file'],p['sha256'],'COLD_NEG2_01 checkpoint')
add(OLD/'checkpoint_manifest.json',sha(OLD/'checkpoint_manifest.json'),'COLD_NEG2_01 manifest')
attachment=Path('C:/Users/Saif malik/.codex/attachments/11d5ff4b-394a-4d5a-a91d-19d0bfb482d9/Pasted text.txt')
external=oldpins['external_pins']+[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'entire Campaign02 directive inspected'}]
for p in external:assert sha(Path(p['path']))==p['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_uniform_CPU']==3223.046875
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
tracked=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=no'],cwd=ROOT,text=True);assert not tracked.strip()
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=ROOT,text=True)
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),'external_pins':external})
out('entry.json',{'head':head,'branch':'coarse-double-branch','tracked_status':tracked,'worktree_status':status,
    'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':{g:v['combined_CPU'] for g,v in r['original_SE03_phase_groups'].items()},
    'group_caps':{'symbolic':120,'independent':300},'canonical_query_cap':2000000,'live_record_cap':2000000,
    'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
    'Bank25':25,'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-started,'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('USER_REQUEST.json',{'target':'FZ-INCOMING: source-valid zero/+1 return barrier T->Pre0*(F), and negative entry into Z',
    'new_potential_authorized':False,'old_normalization':'accepted REFUTED; not rescued or repeated',
    'states':'actual A,BF,BE,M,z,full recent order,ready packet phase; no Score-only state merging',
    'constraints':['R1-R4','Bank25','fixed allocations','cumulative caps','append-only','no source/graph/solver changes'],
    'source_search_authorized':'current Gate F bounded deterministic exact-source tests, not a universal finite proof'})
print(json.dumps({'status':'ENTRY_PASS','pins_verified':len(pins),'CPU':r['cumulative_uniform_CPU']}))
