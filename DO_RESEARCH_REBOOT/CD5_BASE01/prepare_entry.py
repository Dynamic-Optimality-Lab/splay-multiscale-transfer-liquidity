"""Metadata-only inherited hash audit and bounded-phase setup."""
import hashlib,json,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
R=BASE.parent
ROOT=R.parent
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time();pins={}
def add(p,expected,origin):
    p=Path(p);k=p.relative_to(ROOT).as_posix();actual=sha(p)
    assert actual==expected,(k,origin)
    if k in pins:
        assert pins[k]['sha256']==actual
        pins[k]['origins'].append(origin)
    else:pins[k]={'path':k,'sha256':actual,'origins':[origin]}
prior=R/'RESTRICTED_CD_STEP04'
for row in read(prior/'dependency_pins.json')['pins']:
    add(ROOT/row['path'],row['sha256'],'Restricted-CD inherited dependency pin')
for row in read(prior/'final_manifest.json')['files']:
    add(prior/row['file'],row['sha256'],'Restricted-CD final seal')
add(prior/'final_manifest.json',sha(prior/'final_manifest.json'),'entry pin of existing publication seal')
baseline=R/'M3_XFER19/entry_baseline.json'
selected=0
for row in read(baseline)['files']:
    p=Path(row['path']);rel=p.relative_to(R).as_posix()
    if any(rel.startswith('06_CERTIFICATES/'+d+'/') for d in ('DIRECT_NFKS_RT2','DIRECT_CD_K4','DIRECT_CDK5_LOW')) or rel in (
      '02_PROVED/DIRECT_NFKS_RT2_three_keep_key_coarse_double.md',
      '02_PROVED/DIRECT_CD_K4_four_keep_key_coarse_double.md',
      '02_PROVED/DIRECT_CDK5_LOW_five_key_submaximal_core.md',
      '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_06_RESTRICTED_CD_INHERITANCE.md',
      '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',
      'RESEARCH_RULES.md'):
        if '__pycache__' not in rel:add(p,row['sha256'],'XFER19 historical baseline');selected+=1
assert selected>=51
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
# Pin the tracked physical semantics against the existing commit, not merely
# against a newly declared working-tree hash.
for rel in ('python/liquidity/legacy_embedding.py','python/independent/splay.py','scripts/wp6_cycle_ratio.py'):
    committed=subprocess.check_output(['git','show','HEAD:'+rel],cwd=ROOT)
    expected=hashlib.sha256(committed).hexdigest()
    working=xp(ROOT/rel).read_bytes()
    # Git checkout line endings can differ. Both byte pins are recorded;
    # tracked-tree cleanliness and normalized bytes prove commit agreement.
    assert committed.replace(b'\r\n',b'\n')==working.replace(b'\r\n',b'\n')
    add(ROOT/rel,hashlib.sha256(working).hexdigest(),'unchanged tracked source at HEAD; LF-normalized commit SHA256='+expected)
res=read(prior/'resources_final.json');assert res['cumulative_uniform_CPU']==3195.546875
write('dependency_pins.json',{'status':'ALL_PREVIOUSLY_DECLARED_INPUT_HASHES_MATCH','pins':sorted(pins.values(),key=lambda x:x['path']),
  'newly_selected_older_component_files':selected,'completed_semantic_checks_replayed':0})
write('entry.json',{'head':head,'tracked_tree_clean':True,'prior_uniform_CPU':3195.546875,
  'global_allowance':7200,'remaining_CPU_including_reserve':4004.453125,'required_reserve':5,
  'old_signature_ledger_unchanged':7195.203125,'symbolic_CPU_cap':120,'audit_CPU_cap':300,
  'canonical_query_cap':2000000,'live_record_cap':2000000,'input_DAG_cap':4000000,
  'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
  'declared_pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-start})
with (BASE/'run_phase.py').open('x',encoding='utf-8') as f:f.write((prior/'run_phase.py').read_text())
print(json.dumps({'status':'ENTRY_PASS','declared_pins':len(pins),'older_component_files':selected,'head':head}))
