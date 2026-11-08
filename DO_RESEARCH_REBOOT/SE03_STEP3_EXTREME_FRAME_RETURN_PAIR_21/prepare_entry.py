"""Provenance metadata only. Does not import or execute a source engine."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_new(name, data):
    with (B / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

prior = read(OLD / 'dependency_pins.json')
pins = {x['path']: x for x in prior['pins']}
for x in read(OLD / 'campaign_manifest.json')['files']:
    pins[x['path']] = {'path': x['path'], 'sha256': x['sha256'],
                       'origin': 'C20_CONTENT_CHECKPOINT_NOT_SEALED'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {
    'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'origin': 'C20_manifest'}
for x in pins.values():
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
for x in prior['external_pins']:
    assert sha(Path(x['path'])) == x['sha256'], x['path']

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status', '--porcelain', '--untracked-files=no')
r = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == {'symbolic': 118.671875, 'independent': 299.125}
write_new('dependency_pins.json', {
    'status': 'PROVENANCE_ONLY_NOT_PROOF_AUDIT',
    'pins': sorted(pins.values(), key=lambda x: x['path']),
    'external_pins': prior['external_pins']})
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'worktree_status': git('status', '--porcelain', '--untracked-files=all'),
    'pins_verified': len(pins), 'source_provenance': 'actual local C20 checkpoint',
    'new_source_verifier_audit_controller_processes': 0,
    'caps_renewed': False, 'metadata_CPU_excluded': time.process_time(),
    'CPU_ledger': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'frozen_obligation_sha256': sha(B / 'EXTREME_FRAME_FROZEN_OBLIGATION.md'),
    'current_request': 'Campaign21 user message, 2026-11-04; no attachment path claimed'})
print(json.dumps({'status': 'C21_ENTRY_FROZEN', 'pins_verified': len(pins),
                  'new_source_or_audit_processes': 0}))
