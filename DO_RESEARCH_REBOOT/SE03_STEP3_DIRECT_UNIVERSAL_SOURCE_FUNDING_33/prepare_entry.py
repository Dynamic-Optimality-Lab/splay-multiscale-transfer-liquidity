"""Append-only campaign entry and inherited resource freeze; metadata only."""
import json,hashlib,time,subprocess
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;C=B.parent/'SE03_STEP3_EXCEPTIONAL_PREFIX_CARRY_ONE_32/CONTINUATION_01'
def rd(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def txt(n,v):
    with (B/n).open('x',encoding='utf-8') as f:f.write(v)
old=rd(C/'dependency_pins.json');pins={v['path']:v for v in old['pins']}
for v in rd(C/'campaign_manifest.json')['files']:pins[v['path']]={'path':v['path'],'sha256':v['sha256']}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=C/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
for p in pins.values():assert sha(ROOT/p['path'])==p['sha256'],p['path']
branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip();head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert branch=='coarse-double-branch' and head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
r=rd(C/'resources_checkpoint.json')
out('entry.json',{'branch':branch,'head':head,'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],
 'group_caps':r['group_caps'],'global_allowance':7200,'global_reserve':5,'controller_reserve':1,'Bank25':25,
 'phase_caps':{'source':20,'independent':90},'phase_query_caps':{'source':50000,'independent':50000},
 'inherited_conservative_queries':r['conservative_all_queries'],'remaining_conservative_queries':r['conservative_remaining_queries'],'query_limit':r['query_limit'],
 'usage_reset':False,'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'pins':sorted(pins.values(),key=lambda v:v['path']),'external_pins':old['external_pins']})
directive=Path('C:/Users/Saif malik/.codex/attachments/3b3837a3-caa3-4c37-b106-c5617ddbff9c/Pasted text.txt')
txt('USER_DIRECTIVE.txt',directive.read_text(encoding='utf-8'))
out('directive_pin.json',{'path':str(directive),'sha256':sha(directive)})
txt('run_phase.py',(C/'run_phase_authorized.py').read_text().replace("entry_authorized.json","entry.json"))
print(json.dumps({'status':'U33_ENTRY_FROZEN','pins':len(pins),'CPU':r['cumulative_CPU'],'groups':r['cumulative_group_CPU'],'queries':r['conservative_all_queries']}))
