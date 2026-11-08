"""Campaign11 local pins, frozen scope/eligibility and cumulative entry."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_FULL_FUNDING_CLOSURE_10'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(path,h,origin):
    p=ROOT/path;assert p.is_file() and sha(p)==h,path
    if path not in pins:pins[path]={'path':path,'sha256':h,'origins':[]}
    assert pins[path]['sha256']==h;pins[path]['origins'].append(origin)
old=read(OLD/'dependency_pins.json')
for v in old['pins']:add(v['path'],v['sha256'],'inherited')
for v in read(OLD/'campaign_manifest.json')['files']:add(v['path'],v['sha256'],'Campaign10 partial manifest')
add((OLD/'campaign_manifest.json').relative_to(ROOT).as_posix(),sha(OLD/'campaign_manifest.json'),'Campaign10 manifest itself')
req=Path('C:/Users/Saif malik/.codex/attachments/bd3725bc-d4ca-4116-b2cf-d98a1f3a60ab/Pasted text.txt')
ext=old['external_pins']+[{'path':str(req),'sha256':sha(req),'used_sections':'entire Campaign11 directive'}]
for v in ext:assert sha(Path(v['path']))==v['sha256']
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_CPU']==3404.1875
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':ext})
out('entry.json',{'head':git('rev-parse','HEAD'),'branch':git('branch','--show-current'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,'reserve':5,
    'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'metadata_CPU_excluded':time.process_time(),'no_cap_reset':True})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('source_reconstruction.json',{'status':'PASS','Campaign10_FULL_PROOF_exists':(OLD/'FULL_PROOF.md').exists(),
    'Campaign10_status':'UNRESOLVED proof limit, not complete Step2',
    'definitions':{'R':'actual last (Q-2H)+ full demand slots per original macro',
        'partial_a':'fixed common map plus successful h0 terminal paths',
        'Pstar':'D minus domain(partial_a)','Wstar':'actual A bits minus image(partial_a)'},
    'eligibility_frozen_before_execution':
        'inherited physical counting-bit/block-cyclic interface on one actual aligned period; source-valid independent full receipts plus fixed-owner exchange; no native strict-time/matching-terminal assertion',
    'one_bit_rule':'produce independent full h from actual spare, then free terminal against ALL already-paid a owners; no old assignment changed',
    'scope':'core7, six genuine marks, exactly one R slot only; no multi-slot/global CD6 theorem',
    'old_normalization':'REFUTED unchanged; only its independent Hamiltonian incoming-splay structural proof reused',
    'missing_dependency':[]})
print(json.dumps({'status':'PASS','pins':len(pins),'prior_CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU']}))
