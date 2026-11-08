"""Metadata-only content checkpoint. No source test, verifier or proof seal."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*a):
    return subprocess.check_output(['git', *a], cwd=ROOT, text=True).strip()

assert not git('status', '--porcelain', '--untracked-files=no')
assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
entry = read(B / 'entry.json')
assert sha(B / 'FROZEN_TARGET_AND_BOXES.md') == entry['frozen_target_sha256']
assert not (B / 'FULL_PROOF.md').exists()

required = '''FROZEN_TARGET_AND_BOXES.md INCOMING_EXTREME_EXPOSURE.md
CREATOR_POLICY_COMPATIBILITY.md ALTERNATE_ENTRY_COMPONENTS.md
AUXILIARY_NEUTRAL_RETURN.md COLLECTIVE_AUXILIARY_RESERVE.md
PAIRED_LEDGER_FUNDING.md COMPOSITE_RETURN_BLOCKS.md SOURCE_COUNTERCONTROLS.md
RECURSION_AND_ALTERNATIVES.md NEXT_SOURCE_BOX.md SOURCE_SPEC.md
INDEPENDENT_AUDIT_STATUS.md FINAL_VERDICT.md CHECKPOINT.md
resources_checkpoint.json proof_resource_certificate.json
RESEARCH_STATUS.json source_countercontrol.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# JSON syntax and immutable content hashes only, not mathematical validation.
for p in B.glob('*.json'):
    read(p)
for x in read(B / 'dependency_pins.json')['pins']:
    assert sha(ROOT / x['path']) == x['sha256'], x['path']

r = read(B / 'resources_checkpoint.json')
prior = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == prior['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == prior['cumulative_group_CPU']
assert r['new_controllers'] == r['new_independent_runs'] == r['campaign_source_engine_calls'] == 0

with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_PROOF_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_22': True,
        'inherited_local_pins_preserved': entry['inherited_local_pins_verified'],
        'frozen_target_unchanged': True, 'C21_content_checkpoint_preserved': True,
        'primary_outcome': 'UNRESOLVED', 'Gate_U': 'U_OPEN',
        'new_child_results': 'DERIVATIONS_COMPLETE_AT_STATED_SCOPES_INDEPENDENT_AUDIT_PENDING',
        'new_source_or_audit_processes': 0,
        'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
        'entry_metadata_CPU_excluded': entry['metadata_CPU_excluded'],
        'publication_metadata_CPU_excluded': time.process_time(),
        'FULL_PROOF_created': False}, f, indent=2)

files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
         for p in sorted(B.iterdir()) if p.is_file() and p.name != 'campaign_manifest.json']
with (B / 'campaign_manifest.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'CONTENT_CHECKPOINT_NOT_PROOF_SEAL', 'primary': 'UNRESOLVED',
               'Gate_U': 'U_OPEN', 'files': files}, f, indent=2)
print(json.dumps({'status': 'PUBLISHED_R22_PRIMARY_OPEN', 'files': len(files),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
