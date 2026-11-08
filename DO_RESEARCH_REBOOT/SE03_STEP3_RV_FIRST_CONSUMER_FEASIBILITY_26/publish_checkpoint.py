"""Metadata-only content checkpoint, never a source proof or mathematical audit."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25'


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
assert sha(B / 'C26_FROZEN_ARCHITECTURE_TEST.md') == entry['frozen_target_sha256']
assert not (B / 'FULL_PROOF.md').exists()
assert not (B / 'FROZEN_EXTENSION_COUNTERCERTIFICATE.md').exists()
required = '''SOURCE_INTEGRITY.md C25_INHERITANCE_LEDGER.md
C26_FROZEN_ARCHITECTURE_TEST.md IAGS_DEPENDENCY_GRAPH.md
RV_RETENTION_FIRST_CONSUMER.md TWO_ARRIVAL_RV_REALIZABILITY.md
RV_EFFECTIVE_OWNER_CERTIFICATE.md RV_SOURCE_NORMAL_FORMS.md
FROZEN_EXTENSION_FORMAL_SPEC.md SOURCE_FORCED_FROZEN_EXPANSION.md
FROZEN_EXTENSION_ARCHITECTURE_VERDICT.md PHYSICAL_DONOR_ELIGIBILITY_LEDGER.md
COLLECTIVE_RV_OWNER_COMPATIBILITY.md ALTERNATIVE_FUNDING_INVARIANT_SPEC.md
ADVERSARIAL_SOURCE_CONTROLS.md FINAL_VERDICT.md CHECKPOINT.md
C27_G_DEFICIT_HANDOFF.md GATE_U_DEPENDENCY_STATUS.md
INDEPENDENT_AUDIT_STATUS.md resources_checkpoint.json
DIRECT_CONSUMER_SOURCE_BRIDGE.md RESEARCH_STATUS.json
symbolic_receipt_certificate.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# Only file bytes, JSON syntax, declared resource/status fields, Git metadata.
# No source word, tree, potential, owner map, or mathematical formula is evaluated.
for p in B.glob('*.json'):
    read(p)
pins = read(B / 'dependency_pins.json')
for x in pins['pins']:
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
for x in pins['external_pins']:
    assert sha(Path(x['path'])) == x['sha256'], x['path']
assert sha(B / 'USER_DIRECTIVE.txt') == entry['current_directive_sha256']
r = read(B / 'resources_checkpoint.json')
prior = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == prior['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == prior['cumulative_group_CPU']
assert r['new_controllers'] == r['new_independent_runs'] == r['campaign_source_engine_calls'] == 0
assert r['Bank25'] == prior['Bank25'] == 25
s = read(B / 'RESEARCH_STATUS.json')
assert s['outcome'] == 'UNRESOLVED' and not s['independently_sealed']
assert not s['FULL_PROOF_created'] and not s['FROZEN_EXTENSION_COUNTERCERTIFICATE_created']
assert not s['primary_theorem_refuted'] and not s['RV26_complete'] and not s['B26_decided']
assert s['guarded_consuming_source_nonvacuity'] == 'UNKNOWN'
assert not s['frozen_owners_changed'] and not s['Step1_and_CD6_reopened']
assert s['unconditional_Gate_U'] == s['Universal_CD'] == s['Dynamic_Optimality'] == 'OPEN'
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_MATHEMATICAL_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_26': True,
        'inherited_local_pins_preserved': len(pins['pins']),
        'frozen_target_unchanged': True, 'C25_content_checkpoint_preserved': True,
        'primary_outcome': 'UNRESOLVED_SOURCE_AND_LICENSED_ARCHITECTURE',
        'new_smaller_results': 'MANUSCRIPT_DERIVATIONS_INDEPENDENT_AUDIT_PENDING',
        'nonvacuity': 'UNKNOWN_FOR_GUARDED_CONSUMING_CLASS',
        'architecture': 'COUNTING_EXTENSION_CONDITIONAL_ON_TOTAL_H; FULL_F_UNDECIDED',
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
print(json.dumps({'status': 'C26_CONTENT_CHECKPOINT_PUBLISHED_PARENT_OPEN',
                  'files': len(files), 'inherited_pins': len(pins['pins']),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
