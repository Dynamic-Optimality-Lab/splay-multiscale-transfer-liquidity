"""Metadata-only continuation entry; no source semantics executed."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent;ROOT=OLD.parent.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
prior=read(OLD/'dependency_pins.json');pins={x['path']:x for x in prior['pins']}
for x in read(OLD/'campaign_manifest.json')['files']:
    pins[x['path']]={'path':x['path'],'sha256':x['sha256'],'origin':'C27_INITIAL_CHECKPOINT_AUDIT_PENDING'}
p=OLD/'campaign_manifest.json';pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p),'origin':'C27 initial manifest'}
for x in pins.values():assert sha(ROOT/x['path'])==x['sha256'],x['path']
for x in prior['external_pins']:assert sha(Path(x['path']))==x['sha256']
assert git('branch','--show-current')=='coarse-double-branch'
assert git('rev-parse','HEAD')=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status','--porcelain','--untracked-files=no')
r=read(OLD/'resources_checkpoint.json')
out('entry.json',{'branch':git('branch','--show-current'),'head':git('rev-parse','HEAD'),
    'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
    'group_caps':{'symbolic':240,'independent':600},'phase_caps':{'construct':25,'owners':60,'independent':299},
    'global_allowance':7200,'global_reserve':5,'controller_reserve':1,'Bank25':25,
    'authorization':'User explicitly authorized cumulative symbolic cap120->240 and independent300->600; all other caps unchanged.',
    'usage_reset':False,'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time(),
    'new_source_queries_before_entry':0})
out('dependency_pins.json',{'status':'CONTENT_PROVENANCE_NOT_PROOF','pins':sorted(pins.values(),key=lambda x:x['path']),'external_pins':prior['external_pins']})
print(json.dumps({'status':'C27_CONTINUATION_AUTHORIZED','pins':len(pins),'new_caps':{'symbolic':240,'independent':600}}))
