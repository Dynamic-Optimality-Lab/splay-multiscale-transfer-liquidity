"""Metadata-only publication. Never a mathematical checker or proof seal."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTREME_OWNER_RECURSION_22'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

assert not git('status', '--porcelain', '--untracked-files=no')
assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
entry = read(B / 'entry.json')
assert sha(B / 'CAMPAIGN23_FROZEN_SOURCE_BOX.md') == entry['frozen_target_sha256']
required = '''CAMPAIGN23_FROZEN_SOURCE_BOX.md SOURCE_INTEGRITY.md
C22_INHERITANCE_LEDGER.md A_FLIP_NORMAL_FORM.md A_FLIP_SOURCE_VALIDITY.md
ERASED_FULL_B_RETURN_CLASSIFICATION.md A_FLIP_PHYSICAL_COST.md
COMPRESSION_VALIDITY_THEOREM.md EXACT_FLIP_CORRECTION.md
CD6_LEGAL_TRANSFER_INTERFACE.md FLIP_COMPOSITION_THEOREM.md
PAIRED_LEDGER_FLIP_INTERFACE.md R22_RESERVE_FLIP_COMPATIBILITY.md
NEXT_OWNER_INTERFACE.md ADVERSARIAL_SOURCE_TESTS.md IAGS_PROOF_TREE.md
INDEPENDENT_AUDIT_STATUS.md FULL_PROOF.md FINAL_VERDICT.md CHECKPOINT.md
resources_checkpoint.json RESEARCH_STATUS.json flip_source_certificate.json
flip_correction_certificate.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# Syntax/content checks ONLY. Do not evaluate a tree, source word, owner map
# or mathematical claim in any of these static manuscript certificates.
for p in B.glob('*.json'):
    read(p)
pins = read(B / 'dependency_pins.json')
for row in pins['pins']:
    assert sha(ROOT / row['path']) == row['sha256'], row['path']
for row in pins['external_pins']:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
assert sha(B / 'USER_DIRECTIVE.txt') == entry['current_directive_sha256']
r = read(B / 'resources_checkpoint.json')
prior = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == prior['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == prior['cumulative_group_CPU']
assert r['new_controllers'] == r['new_independent_runs'] == r['campaign_source_engine_calls'] == 0
s = read(B / 'RESEARCH_STATUS.json')
assert s['outcome'] == 'A' and not s['independently_sealed']
assert s['unconditional_Gate_U'] == s['Universal_CD'] == s['Dynamic_Optimality'] == 'OPEN'
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_MATHEMATICAL_PROOF_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_23': True,
        'inherited_local_pins_preserved': len(pins['pins']),
        'frozen_target_unchanged': True, 'C22_content_checkpoint_preserved': True,
        'primary_outcome': 'A_MATHEMATICAL_DERIVATION_COMPLETE_INDEPENDENT_AUDIT_PENDING',
        'Gate_U': 'OPEN', 'new_source_or_audit_processes': 0,
        'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
        'entry_metadata_CPU_excluded': entry['metadata_CPU_excluded'],
        'publication_metadata_CPU_excluded': time.process_time(),
        'FULL_PROOF_created': True, 'proof_assistant_or_external_audit': False}, f, indent=2)
files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
         for p in sorted(B.iterdir()) if p.is_file() and p.name != 'campaign_manifest.json']
with (B / 'campaign_manifest.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
               'primary': 'A_MATHEMATICAL_DERIVATION_COMPLETE_INDEPENDENT_AUDIT_PENDING',
               'Gate_U': 'OPEN', 'files': files}, f, indent=2)
print(json.dumps({'status': 'C23_CONTENT_CHECKPOINT_PUBLISHED_NOT_PROOF_SEALED',
                  'files': len(files), 'inherited_pins': len(pins['pins']),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
