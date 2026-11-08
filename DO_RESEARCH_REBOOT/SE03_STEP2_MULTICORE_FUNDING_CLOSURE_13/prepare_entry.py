"""Metadata-only exact continuation of the sealed cumulative ledger."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_CORE7_TWO_EXCESS_12'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
pins={}
def add(path,h,origin):
    assert sha(ROOT/path)==h,path
    if path not in pins:pins[path]={'path':path,'sha256':h,'origins':[]}
    assert pins[path]['sha256']==h;pins[path]['origins'].append(origin)
old=read(OLD/'dependency_pins.json')
for v in old['pins']:add(v['path'],v['sha256'],'inherited12')
for v in read(OLD/'campaign_manifest.json')['files']:add(v['path'],v['sha256'],'sealed12')
add((OLD/'campaign_manifest.json').relative_to(ROOT).as_posix(),sha(OLD/'campaign_manifest.json'),'manifest12')
req=Path('C:/Users/Saif malik/.codex/attachments/e81808b0-4872-4c00-b94e-0172d689e7b9/Pasted text.txt')
ext=old['external_pins']+[{'path':str(req),'sha256':sha(req),'used_sections':'entire Campaign13 directive'}]
for v in ext:assert sha(Path(v['path']))==v['sha256']
r=read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU']==3439.609375 and r['remaining_CPU']==3760.390625
assert r['cumulative_group_CPU']=={'symbolic':71.421875,'independent':166.8125}
assert git('branch','--show-current')=='coarse-double-branch' and git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':ext})
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),'tracked_status':'',
    'worktree_status':git('status','--porcelain','--untracked-files=all'),'prior_uniform_CPU':r['cumulative_CPU'],
    'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],'global_allowance':7200,
    'reserve':5,'canonical_query_cap':2000000,'live_record_cap':2000000,'DAG_cap':4000000,'stored_edge_cap':5000000,
    'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,'Bank25':25,'pins_verified':len(pins),
    'no_cap_reset':True,'metadata_CPU_excluded':time.process_time()})
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write((OLD/'run_phase.py').read_text())
out('source_reconstruction.json',{'status':'SOURCE_FROZEN',
    'original_domain':'reachable finite exactly paired-closed Pair Access, six genuine KEEP keys, every original operation',
    'full_core_constancy':'to be re-established from monotonicity and exact closure, not imposed',
    'ownership':'literal10 R,alpha,a,Pstar,Wstar and supplied certified fE; all old values fixed',
    'eligibility':'inherited actual-ID counting/block-cyclic receipt, not strict arbitrary-seam online or terminal-key donor policy',
    'core7_next':'all slot counts via distinct actual cyclic predecessors and simultaneous licensed exchange',
    'larger_core_attempt':'source-complete finite BF skeleton comparison with free-gap lifting may provide a debt/physical spare allocator; no abstract BF cycle presumed an actual cheap A history',
    'source_chart_corrections':'literal full physical D, signed C/P/N; old chart normalization remains REFUTED',
    'proof_status_at_entry':'only prior scopes accepted; complete multicore/Step2/CD6/Step3 OPEN'})
print(json.dumps({'status':'ENTRY_VERIFIED','pins':len(pins),'CPU':r['cumulative_CPU'],'remaining':r['remaining_CPU']}))
