"""Metadata-only source freeze. This is NOT the unfinished C15 audit seal."""
import hashlib, json, subprocess, time
from pathlib import Path
B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_UNIFORM_DONOR_GROUPING_15'
REQUEST = Path('C:/Users/Saif malik/.codex/attachments/cf8b4342-97cd-4725-b53b-13ca48047211/Pasted text.txt')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def out(name, obj):
    with (B/name).open('x', encoding='utf-8') as f: json.dump(obj, f, indent=2)
prior = read(OLD/'dependency_pins.json')
pins = {p['path']:p for p in prior['pins']}
for p in read(OLD/'campaign_manifest.json')['files']:
    pins[p['path']] = {'path':p['path'], 'sha256':p['sha256'], 'origin':'C15_content_checkpoint_NOT_final_seal'}
mp = (OLD/'campaign_manifest.json').relative_to(ROOT).as_posix()
pins[mp] = {'path':mp, 'sha256':sha(OLD/'campaign_manifest.json'), 'origin':'C15_manifest'}
for p in pins.values():
    assert sha(ROOT/p['path']) == p['sha256'], p['path']
external = prior['external_pins'] + [{'path':str(REQUEST), 'sha256':sha(REQUEST), 'origin':'C16_directive'}]
for p in external: assert sha(Path(p['path'])) == p['sha256'], p['path']
r = read(OLD/'resources_checkpoint.json')
assert r['cumulative_CPU'] == 3607.6875
assert r['cumulative_group_CPU'] == {'symbolic':107.1875, 'independent':299.125}
assert r['group_caps'] == {'symbolic':120, 'independent':300}
assert not (OLD/'partial_seal.json').exists()
git = lambda *a: subprocess.check_output(['git', *a], cwd=ROOT, text=True).strip()
assert git('rev-parse','HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert git('branch','--show-current') == 'coarse-double-branch'
assert not git('status','--porcelain','--untracked-files=no')
out('dependency_pins.json', {'status':'ENTRY_CONTENT_HASHES_MATCH_NOT_AUDIT_SEAL',
    'pins':sorted(pins.values(), key=lambda p:p['path']), 'external_pins':external})
out('entry.json', {'branch':git('branch','--show-current'), 'head':git('rev-parse','HEAD'),
    'tracked_status':'', 'worktree_status':git('status','--porcelain','--untracked-files=all'),
    'prior_uniform_CPU':r['cumulative_CPU'], 'inherited_group_CPU':r['cumulative_group_CPU'],
    'group_caps':r['group_caps'], 'global_allowance':7200, 'reserve':5,
    'canonical_query_cap':2000000, 'live_record_cap':2000000, 'DAG_cap':4000000,
    'stored_edge_cap':5000000, 'memory_cap_bytes':32*1024**3, 'wall_cap_hours':12,
    'Bank25':25, 'no_cap_reset':True, 'pins_verified':len(pins),
    'C15_integrity_seal':'PENDING_CAP_NOT_COMPLETED_BY_ENTRY_HASHING',
    'metadata_CPU_excluded':time.process_time()})
with (B/'USER_DIRECTIVE.txt').open('x', encoding='utf-8') as f: f.write(REQUEST.read_text(encoding='utf-8'))
with (B/'run_phase.py').open('x', encoding='utf-8') as f: f.write((OLD/'run_phase.py').read_text(encoding='utf-8'))
print(json.dumps({'status':'ENTRY_FROZEN_NOT_INDEPENDENT_SEAL','pins':len(pins),
    'symbolic_remaining':12.8125,'independent_remaining':0.875}), flush=True)
