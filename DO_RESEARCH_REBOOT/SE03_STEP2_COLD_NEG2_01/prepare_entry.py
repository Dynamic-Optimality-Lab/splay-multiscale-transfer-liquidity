"""Pin current local source and cumulative allowance, append-only."""
import hashlib,json,subprocess,time
from pathlib import Path
B=Path(__file__).resolve().parent;ROOT=B.parent.parent;OLD=B.parent/'SE03_STEP2_DONOR06';started=time.process_time()
def xp(p):return Path('\\\\?\\'+str(p.resolve()))
def read(p):return json.loads(xp(p).read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(xp(p).read_bytes()).hexdigest()
def out(n,v):
    with (B/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
pins={}
def pin(p,h,origin):
    assert sha(p)==h,str(p)
    key=p.relative_to(ROOT).as_posix()
    if key in pins:assert pins[key]['sha256']==h;pins[key]['origins'].append(origin)
    else:pins[key]={'path':key,'sha256':h,'origins':[origin]}
for p in read(OLD/'dependency_pins.json')['pins']:pin(ROOT/p['path'],p['sha256'],'inherited')
for p in read(OLD/'checkpoint_manifest.json')['files']:pin(OLD/p['file'],p['sha256'],'DONOR06 checkpoint')
pin(OLD/'checkpoint_manifest.json',sha(OLD/'checkpoint_manifest.json'),'DONOR06 manifest')
for name in ['python/independent/splay.py','python/independent/pair.py','DO_RESEARCH_REBOOT/RESEARCH_RULES.md',
    'DO_RESEARCH_REBOOT/ORIGINAL_PIPELINE.md','DO_RESEARCH_REBOOT/M3_LDR01/negative_run_census.json',
    'DO_RESEARCH_REBOOT/M3_H1F01/cheap_census.json','DO_RESEARCH_REBOOT/M3_XFER16/debt_definition.json',
    'DO_RESEARCH_REBOOT/M3_XFER17/debt_definition.json','DO_RESEARCH_REBOOT/M3_XFER21/FULL_M3_PROOF.md']:
    p=ROOT/name;pin(p,sha(p),'COLD-NEG2 inspected source')
attachment=Path('C:/Users/Saif malik/.codex/attachments/0202b78f-c0f4-4eb9-9158-8848d5ed842e/Pasted text.txt')
r=read(OLD/'resources_checkpoint.json');assert r['cumulative_uniform_CPU']==3220.21875
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
assert head=='8c378d49283b3738b18e7175886772a98025e4e9'
assert subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()=='coarse-double-branch'
tracked=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=no'],cwd=ROOT,text=True)
assert not tracked.strip()
status=subprocess.check_output(['git','status','--porcelain=v1','--untracked-files=normal'],cwd=ROOT,text=True)
out('dependency_pins.json',{'status':'PASS','pins':sorted(pins.values(),key=lambda p:p['path']),
    'external_pins':[{'path':str(attachment),'sha256':sha(attachment),'used_sections':'24 IAGS,25 research-quality rules'}]})
out('entry.json',{'head':head,'branch':'coarse-double-branch','tracked_status':tracked,'worktree_status':status,
    'prior_uniform_CPU':r['cumulative_uniform_CPU'],'global_allowance':7200,'reserve':5,
    'inherited_group_CPU':{g:v['combined_CPU'] for g,v in r['original_SE03_phase_groups'].items()},
    'group_caps':{'symbolic':120,'independent':300},'canonical_query_cap':2000000,'live_record_cap':2000000,
    'DAG_cap':4000000,'stored_edge_cap':5000000,'memory_cap_bytes':32*1024**3,'wall_cap_hours':12,
    'Bank25':25,'pins_verified':len(pins),'metadata_CPU_excluded':time.process_time()-started,'no_cap_reset':True,
    'source_replay_authorization':'Current user directive Gate E explicitly requires deterministic actual source replays; no new universal graph/solver project.'})
controller=(OLD/'run_phase.py').read_text()
controller=controller.replace("'new_finite_tests':0,'source_engine_calls':0,'old_semantic_rows_replayed':0}",
    "'new_finite_tests':ex.get('new_finite_tests',0),'source_engine_calls':ex.get('source_engine_calls',0),'old_semantic_rows_replayed':0}")
with (B/'run_phase.py').open('x',encoding='utf-8') as f:f.write(controller)
out('USER_REQUEST.json',{'target':'COLD-NEG2: prove/refute exact normalized width-two chart debt endpoint0->2 on every source-valid weight-2 cold packet',
    'packet_price':'2min(H,4)-Q','classes':['singleton H1,Q4','actual q5/q1 pair Hsum2,Q6'],
    'terminal_outcomes':['A NEG2 proved','B normalized candidate refuted','C partial','D dependency blocked'],
    'constraints':['R1-R4','Bank25','existing allocation ownership','all resource caps','append-only research','inspect local latest source','Gates A-G'],
    'tests':'Gate E actual deterministic bottom-up replay explicitly authorized; not universal evidence',
    'forbidden_promotions':['entire Step2','CD6','Universal CD','Dynamic Optimality']})
print(json.dumps({'status':'ENTRY_PASS','pins_verified':len(pins),'prior_uniform_CPU':r['cumulative_uniform_CPU'],'tracked_tree_clean':True}))
