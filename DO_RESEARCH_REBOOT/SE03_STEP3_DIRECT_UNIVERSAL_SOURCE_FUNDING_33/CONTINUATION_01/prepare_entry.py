"""Append-only resumption metadata; preserves the initial C33 publication."""
import json,hashlib,time,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent;ROOT=OLD.parent.parent
def rd(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x') as f:json.dump(v,f,indent=2)
old=rd(OLD/'dependency_pins.json');pins={v['path']:v for v in old['pins']}
for v in rd(OLD/'campaign_manifest.json')['files']:pins[v['path']]={'path':v['path'],'sha256':v['sha256']}
for n in ('campaign_manifest.json','publication_seal.json','publication_exit.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
r=rd(OLD/'resources_checkpoint.json');entry=rd(OLD/'entry.json')
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==entry['head']
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
entry.update(prior_uniform_CPU=r['cumulative_CPU'],inherited_group_CPU=r['cumulative_group_CPU'],
             inherited_conservative_queries=r['conservative_all_queries'],remaining_conservative_queries=r['conservative_remaining_queries'],
             phase_caps={'proof':20,'independent':90},phase_query_caps={'proof':0,'independent':0},
             metadata_CPU_excluded=time.process_time(),inherited_pins=len(pins))
out('entry.json',entry);out('dependency_pins.json',{'pins':sorted(pins.values(),key=lambda z:z['path']),'external_pins':old['external_pins']})
with (B/'run_phase.py').open('x') as f:f.write((OLD/'run_phase.py').read_text())
print(json.dumps({'status':'C33_RESUMED','pins':len(pins),'CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU'],'queries':r['conservative_all_queries']}))
