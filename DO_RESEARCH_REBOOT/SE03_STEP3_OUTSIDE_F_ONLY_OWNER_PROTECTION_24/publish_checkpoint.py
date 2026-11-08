"""Content-only checkpoint; no source evaluator or mathematical certification."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23'

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()

assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status', '--porcelain', '--untracked-files=no')
entry = read(B / 'entry.json')
assert sha(B / 'OWNER24_FROZEN_BOX.md') == entry['frozen_target_sha256']
assert not (B / 'FULL_PROOF.md').exists()
required = '''SOURCE_SPEC.md C23_INHERITANCE_LEDGER.md OWNER24_FROZEN_BOX.md
SOURCE_INTEGRITY.md EXTERNAL_OWNER_PROVENANCE.md EFFECTIVE_RESERVE_INVENTORY.md
EXTERNAL_OWNER_NORMAL_FORMS.md OWNERSHIP_IMMUTABILITY_THEOREM.md
SOURCE_FORCED_OCCUPANCY_BOUND.md LICENSED_F_ONLY_EXCHANGE.md
GLOBAL_OWNER_FRONTIER_THEOREM.md OWNER_QUALIFIED_CAPACITY_INTERFACE.md
COLLECTIVE_EXTERNAL_OWNER_LEDGER.md C23_CORRECTED_OWNER_LEDGER.md
OWNER_ABSOLUTE_PERIOD_THEOREM.md C25_G_DEFICIT_HANDOFF.md
C26_GLOBAL_EXPANSION_INTERFACE.md ADVERSARIAL_OWNER_CONTROLS.md
IAGS_PROOF_TREE.md INDEPENDENT_AUDIT_STATUS.md FINAL_VERDICT.md CHECKPOINT.md
resources_checkpoint.json SS_SOURCE_INVERSE_LEMMA.md
SOURCE_EXACT_EXTERNAL_OWNER_CONTROL.md RESEARCH_STATUS.json
owner24_symbolic_certificate.json saved_source_control.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# JSON syntax, content identity and recorded status consistency ONLY.
# Never evaluate the source recipes, inverse recursion, formulas or maps.
for p in B.glob('*.json'):
    read(p)
pins = read(B / 'dependency_pins.json')
for row in pins['pins']:
    assert sha(ROOT / row['path']) == row['sha256'], row['path']
for row in pins['external_pins']:
    assert sha(Path(row['path'])) == row['sha256'], row['path']
assert sha(B / 'USER_DIRECTIVE.txt') == entry['current_directive_sha256']
assert sha(B / 'saved_source_control.json') == entry['saved_source_control_sha256']
r = read(B / 'resources_checkpoint.json')
prior = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == prior['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == prior['cumulative_group_CPU']
assert r['new_controllers'] == r['new_independent_runs'] == r['campaign_source_engine_calls'] == 0
s = read(B / 'RESEARCH_STATUS.json')
assert s['outcome'] == 'UNRESOLVED' and not s['independently_sealed']
assert not s['FULL_PROOF_created'] and not s['primary_OWNER24_refuted']
assert s['new_control_two_selected_T19_arrival_guard'] == 'NOT_ESTABLISHED'
assert s['unconditional_Gate_U'] == s['Universal_CD'] == s['Dynamic_Optimality'] == 'OPEN'
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_MATHEMATICAL_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_24': True,
        'inherited_local_pins_preserved': len(pins['pins']),
        'frozen_target_unchanged': True, 'C23_content_checkpoint_preserved': True,
        'primary_outcome': 'UNRESOLVED_MATHEMATICAL_SOURCE_BRIDGE',
        'new_smaller_results': 'MANUSCRIPT_DERIVATIONS_INDEPENDENT_AUDIT_PENDING',
        'new_control_scope': 'geometric G2/natural-common-Hprime only; selected-arrival and mandatory-later-policy guards not established',
        'Gate_U': 'OPEN', 'new_source_or_audit_processes': 0,
        'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
        'entry_metadata_CPU_excluded': entry['metadata_CPU_excluded'],
        'publication_metadata_CPU_excluded': time.process_time(),
        'FULL_PROOF_created': False, 'proof_assistant_or_external_audit': False}, f, indent=2)
files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
         for p in sorted(B.iterdir()) if p.is_file() and p.name != 'campaign_manifest.json']
with (B / 'campaign_manifest.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
               'primary': 'UNRESOLVED', 'Gate_U': 'OPEN', 'files': files}, f, indent=2)
print(json.dumps({'status': 'C24_CONTENT_CHECKPOINT_PUBLISHED_OWNER24_OPEN',
                  'files': len(files), 'inherited_pins': len(pins['pins']),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
