"""Append-only continuation freeze/provenance; no semantic work."""
import json,hashlib,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;OLD=B.parent;P=OLD.parent;ROOT=P.parent
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,s):
    with (B/n).open('x',encoding='utf-8') as f:f.write(s)
def out(n,v):write(n,json.dumps(v,indent=2))
r=read(OLD/'resources_checkpoint.json');old=read(OLD/'dependency_pins.json');pins={z['path']:z for z in old['pins']}
for z in read(OLD/'campaign_manifest.json')['files']:pins[z['path']]={'path':z['path'],'sha256':z['sha256']}
for n in ('campaign_manifest.json','publication_exit.json','publication_seal.json'):
    p=OLD/n;pins[p.relative_to(ROOT).as_posix()]={'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)}
for z in pins.values():assert sha(ROOT/z['path'])==z['sha256'],z['path']
assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()=='8c378d49283b3738b18e7175886772a98025e4e9'
assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
write('FROZEN_H2_SLACK_BOX.md','''# Continue to closure: exact H2 zero-slack exclusion

Parent: principal FR32-CARRY1 remains open; user directs continued work.
Child target: immediate H1 activation with D_new(v)=1,E7(v)=1, actual
H_return2, terminal A381 and BF1060/1063. Prove Lambda_new>=1, or produce
a source-valid paired-closed Lambda_new0 counterexample. R=Lambda_new-1.

Conditions/Inheritance: all original EXC source, R1-R4, Bank25, frozen
owners, source periods, arbitrary private terms; accepted complete old
six-key LOW/HIGH relations and D, fixed-core/q5-packet bridges. Only cached
relations may be reused; source-query budget is0, CPU caps unchanged.

Exact proof route: since each COMPLETE original packet has nonnegative
integer certificate margin, Lambda0 requires EVERY packet margin0.
Compute the zero-margin reachable overapproximation using ONLY already
audited cached A/B relations, from both D1 entry quotient forms. Excluding
both terminal sectors there proves the actual source theorem by forward
simulation. A projected path alone is NOT a source counterexample.

Ambiguities: q5 shared midpoint and complete LOW/HIGH packet relation,
actual A7 geometry forgotten by old quotient, cold transfer/H1 terminal
parent branches. Never splice abstract states and call them realizable.
No new original tree access, root/path query, source-frame compilation,
resource reset or successful owner change is authorized.
''')
out('entry.json',{'branch':'coarse-double-branch','head':'8c378d49283b3738b18e7175886772a98025e4e9',
 'prior_uniform_CPU':r['cumulative_CPU'],'inherited_group_CPU':r['cumulative_group_CPU'],'group_caps':r['group_caps'],
 'global_allowance':7200,'global_reserve':5,'controller_reserve':1,'Bank25':25,
 'phase_caps':{'proof':20,'independent':90},'phase_query_caps':{'proof':0,'independent':0},
 'inherited_conservative_queries':2000000,'remaining_conservative_queries':0,'usage_reset':False,
 'inherited_pins':len(pins),'metadata_CPU_excluded':time.process_time()})
out('dependency_pins.json',{'pins':sorted(pins.values(),key=lambda z:z['path']),'external_pins':old['external_pins']})
write('run_phase.py',(OLD/'run_phase.py').read_text())
print(json.dumps({'status':'CONTINUATION_FROZEN','CPU':r['cumulative_CPU'],'symbolic_remaining':r['group_remaining']['symbolic'],'queries':0,'pins':len(pins)}),flush=True)
