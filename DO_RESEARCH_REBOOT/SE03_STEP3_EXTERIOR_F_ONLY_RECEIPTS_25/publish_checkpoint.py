"""Metadata-only checkpoint. No source proof/evaluator or certification."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24'

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
assert sha(B / 'OWNER25_FROZEN_SOURCE_BOX.md') == entry['frozen_target_sha256']
assert not (B / 'FULL_PROOF.md').exists()
required = '''OWNER25_FROZEN_SOURCE_BOX.md C24_INHERITANCE_LEDGER.md
SOURCE_INTEGRITY.md EXTERIOR_RECEIPT_NORMAL_FORMS.md
RETAINED_FULL_ERASED_RECEIPTS.md EXTERIOR_OWNER_PROVENANCE.md
G2_SOURCE_COMPLETION.md G2_T19_TWO_ARRIVAL_TEST.md G2_LATER_POLICY_VALIDITY.md
G2_FINAL_DISPOSITION.md CORRECTED_EXTERIOR_CAPACITY.md
EXTERIOR_OCCUPANCY_THEOREM.md FROZEN_OWNER_GLOBAL_FUNDING.md
R_BLOCK_RECEIPT_COMPLETENESS.md COLLECTIVE_RECEIPT_NONCOLLISION.md
ABSOLUTE_PERIOD_PROOF.md ADVERSARIAL_SOURCE_CERTIFICATES.md IAGS_PROOF_TREE.md
INDEPENDENT_AUDIT_STATUS.md FINAL_VERDICT.md CHECKPOINT.md
C26_G_DEFICIT_COMPENSATION_INTERFACE.md GATE_U_DISCHARGE_STATUS.md
resources_checkpoint.json OWNER_POLICY_COMPLETENESS.md
CANONICAL_G_V_EXCLUSION.md FIVE_KEY_G_V_EXCLUSION.md R_V_CARRY_FRONTIER.md
T19_ARRIVAL_LOCALIZATION.md PREHISTORY_ZERO_ORIGIN_ATTEMPT.md
RESEARCH_STATUS.json source_receipt_certificate.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# Syntactic/content/status checks only. Never execute a mathematical word,
# simulate a tree, evaluate debts, construct a source map or audit a lemma.
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
s = read(B / 'RESEARCH_STATUS.json')
assert s['outcome'] == 'UNRESOLVED' and not s['independently_sealed']
assert not s['FULL_PROOF_created'] and not s['primary_theorem_refuted']
assert not s['all_G2_sources_impossible']
assert s['unconditional_Gate_U'] == s['Universal_CD'] == s['Dynamic_Optimality'] == 'OPEN'
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_MATHEMATICAL_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_25': True,
        'inherited_local_pins_preserved': len(pins['pins']),
        'frozen_target_unchanged': True, 'C24_content_checkpoint_preserved': True,
        'primary_outcome': 'UNRESOLVED_MATHEMATICAL_SOURCE_CLASSIFICATION',
        'new_smaller_results': 'MANUSCRIPT_DERIVATIONS_INDEPENDENT_AUDIT_PENDING',
        'G2_scope': 'unchanged695 word only; no impossibility claim for every modified G2 source',
        'safe_owner_scope': 'canonical raw or actual original-Step1-normalized G-producer v receipts; no all-receipt promotion',
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
print(json.dumps({'status': 'C25_CONTENT_CHECKPOINT_PUBLISHED_PARENT_OPEN',
                  'files': len(files), 'inherited_pins': len(pins['pins']),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
