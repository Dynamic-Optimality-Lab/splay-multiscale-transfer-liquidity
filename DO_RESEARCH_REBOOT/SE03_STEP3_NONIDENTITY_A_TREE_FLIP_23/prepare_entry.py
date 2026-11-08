"""Content provenance only. No source engine, mathematical evaluator or audit."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTREME_OWNER_RECURSION_22'
DIRECTIVE = Path('C:/Users/Saif malik/.codex/attachments/8b773c76-cae2-4f64-93c8-9d331c22fc4e/Pasted text.txt')

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

def write_new(name, data):
    with (B / name).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

prior = read(OLD / 'dependency_pins.json')
pins = {row['path']: row for row in prior['pins']}
for row in read(OLD / 'campaign_manifest.json')['files']:
    pins[row['path']] = {'path': row['path'], 'sha256': row['sha256'],
                         'origin': 'C22_CONTENT_CHECKPOINT_AUDIT_PENDING'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {
    'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'origin': 'C22_manifest'}
for row in pins.values():
    assert sha(ROOT / row['path']) == row['sha256'], row['path']
external = prior['external_pins'] + [{
    'path': str(DIRECTIVE), 'sha256': sha(DIRECTIVE), 'origin': 'C23 user directive'}]
for row in external:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status', '--porcelain', '--untracked-files=no')
r = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == {'symbolic': 118.671875, 'independent': 299.125}
write_new('dependency_pins.json', {
    'status': 'CONTENT_PROVENANCE_ONLY_NOT_MATHEMATICAL_AUDIT',
    'pins': sorted(pins.values(), key=lambda row: row['path']), 'external_pins': external})
with (B / 'USER_DIRECTIVE.txt').open('xb') as f:
    f.write(DIRECTIVE.read_bytes())

ledger = read(OLD / 'dependency_ledger.json')
for row in ledger['rows']:
    row['C23_status'] = 'inherited exact scope/status; content pin only unless separately inspected'
additional = []
for rel in [
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/FINAL_VERDICT.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/NEXT_SOURCE_BOX.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/PAIRED_LEDGER_FUNDING.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/COMPOSITE_RETURN_BLOCKS.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/SOURCE_SPEC.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/resources_checkpoint.json',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_ORDER_NORMAL_FORM.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_NONLOCAL_SUPPLY.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/cd6_allocator.py',
    'SE03_STEP2_COLD_NEG2_01/source_model.py',
    '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md']:
    p = B.parent / rel
    additional.append({
        'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
        'inspection': 'relevant manuscript/source interface read; not executed or independently audited',
        'status': 'accepted or audit-pending exactly as specified in C22_INHERITANCE_LEDGER.md'})
ledger.update(status='CONTENT_PROVENANCE_AND_INHERITED_SCOPES_NOT_PROOF_SEAL',
              C23_inspected=additional)
write_new('dependency_ledger.json', ledger)
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'inherited_local_pins_verified': len(pins),
    'untracked_inventory_sha256': hashlib.sha256(
        git('status', '--porcelain', '--untracked-files=all').encode()).hexdigest(),
    'frozen_target_sha256': sha(B / 'CAMPAIGN23_FROZEN_SOURCE_BOX.md'),
    'current_directive_sha256': sha(DIRECTIVE),
    'source_reconstruction_precedes_proof': 'recorded in first frozen artifact; metadata snapshot made after manuscript derivation',
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_audit_processes': 0, 'caps_extended': False,
    'metadata_CPU_excluded': time.process_time()})
print(json.dumps({'status': 'C23_CONTENT_PROVENANCE_RECORDED', 'pins': len(pins),
                  'new_source_or_audit_processes': 0}))
