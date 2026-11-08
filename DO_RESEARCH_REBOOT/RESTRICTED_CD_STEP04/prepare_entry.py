"""Metadata-only provenance snapshot; executes no imported research code."""
import hashlib,json,shutil,subprocess,time
from pathlib import Path
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent.parent
RESEARCH=ROOT/'DO_RESEARCH_REBOOT'
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def write(n,d):
    with (BASE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2)
start=time.process_time()
pins={}
def add(path,expected,origin):
    path=Path(path);key=path.relative_to(ROOT).as_posix()
    actual=sha(path)
    assert actual==expected,(key,origin,'changed input')
    if key in pins:
        assert pins[key]['sha256']==expected
        pins[key]['origins'].append(origin)
    else:pins[key]={'path':key,'sha256':actual,'origins':[origin]}
baseline=read(RESEARCH/'M3_XFER19/entry_baseline.json')
old_prefixes=(
 '06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/',
 '06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE/',
 '06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE/',
 '06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER/',
 '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP01_GRAPH_DOMAIN_AND_REDUCTION/')
for row in baseline['files']:
    path=Path(row['path']);rel=path.relative_to(RESEARCH).as_posix()
    if rel.startswith(old_prefixes) and '__pycache__' not in rel:
        add(path,row['sha256'],'XFER19 historical entry baseline')
    elif rel in ('06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_RULE_FREEZE.md',
                 '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_PROOF_TARGETS.json',
                 '06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/11G_FOUR_STEP_DEPENDENCY_PLAN.md'):
        add(path,row['sha256'],'XFER19 historical entry baseline')
for dirname in ('M3_XFER19','M3_XFER21'):
    manifest=RESEARCH/dirname/'final_manifest.json'
    for row in read(manifest)['files']:add(manifest.parent/row['file'],row['sha256'],dirname+' final seal')
    add(manifest,sha(manifest),'entry pin of existing seal')
for row in read(RESEARCH/'M3_XFER21/dependencies_final.json')['pins']:
    add(row['path'],row['sha256'],'XFER21 sealed dependency')
add(RESEARCH/'M3_XFER19/entry_baseline.json',sha(RESEARCH/'M3_XFER19/entry_baseline.json'),'historical pin index')
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
dirty=subprocess.check_output(['git','status','--short','--untracked-files=no'],cwd=ROOT,text=True).strip()
assert not dirty
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
resources=read(RESEARCH/'M3_XFER21/resources_final.json')
assert resources['cumulative_uniform_CPU']==3194.140625
write('dependency_pins.json',{'status':'ALL_REUSED_DECLARED_HASHES_MATCH','pins':sorted(pins.values(),key=lambda x:x['path']),
      'source':'Existing hashes checked, not merely newly assigned hashes',
      'completed_semantic_checks_replayed':0})
write('entry.json',{'head':head,'tracked_tree_clean':True,'prior_uniform_CPU':3194.140625,'global_allowance':7200,
      'required_reserve':5,'remaining_CPU_including_reserve':4005.859375,
      'old_signature_ledger_unchanged':7195.203125,'symbolic_CPU_cap':120,'audit_CPU_cap':300,
      'canonical_query_cap':2000000,'live_record_cap':2000000,'input_DAG_cap':4000000,
      'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
      'existing_declared_pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-start})
with (BASE/'run_phase.py').open('x',encoding='utf-8') as f:
    f.write((RESEARCH/'M3_XFER21/run_phase.py').read_text())
print(json.dumps({'status':'ENTRY_PIN_AND_RESOURCE_PASS','pins':len(pins),'head':head}))
