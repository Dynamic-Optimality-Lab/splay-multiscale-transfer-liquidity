"""Metadata-only content publication. No source or mathematical evaluation."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26'


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
assert sha(B / 'N26_E4_FROZEN_GUARDS.md') == entry['frozen_target_sha256']
for name in ['FULL_PROOF.md', 'GUARDED_E4_SOURCE_WITNESS.md', 'GUARDED_E4_UNIVERSAL_EXCLUSION.md']:
    assert not (B / name).exists(), name
required = '''SOURCE_INTEGRITY.md C26_INHERITANCE_LEDGER.md N26_E4_FROZEN_GUARDS.md
GUARDED_E4_DEPENDENCY_GRAPH.md TWO_SELECTED_ZERO_LIFETIMES.md
RV_EPSILON1_BANK_SOURCE_BRIDGE.md E4_FIRST_CONSUMPTION_SOURCE_THEOREM.md
ORIGINAL_PAIRED_SOURCE_REALIZABILITY.md NORMALIZED_F6_GUARDED_POLICY.md
GUARDED_PERIOD_CLOSURE.md SOURCE_DECISION_LEDGER.md ACTUAL_E4_EFFECTIVE_OWNER_LEDGER.md
E4_ARCHITECTURE_CONSEQUENCE.md REMAINING_RV_SOURCE_CLASSES.md GATE_U_DEPENDENCY_STATUS.md
ADVERSARIAL_SOURCE_CONTROLS.md IAGS_PROOF_TREE.md INDEPENDENT_AUDIT_STATUS.md
FINAL_VERDICT.md CHECKPOINT.md resources_checkpoint.json EXACT_REJECTED_CANDIDATE.md
NONLEAF_REFRESH_NECESSITY.md RESEARCH_STATUS.json source_decision_certificate.json'''.split()
for name in required:
    assert (B / name).is_file() and (B / name).stat().st_size > 0, name

# Syntactic/status/provenance checks only. No source operations, tree paths,
# debt vectors, bank formulas, creator groups or owner maps are evaluated.
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
assert s['guarded_e4_existence'] == 'UNDECIDED'
assert not s['guarded_source_witness_created'] and not s['guarded_universal_exclusion_created']
assert not s['FULL_PROOF_created'] and not s['all_refreshed_sources_excluded']
assert not s['frozen_owners_changed'] and not s['Step1_and_CD6_reopened']
assert s['unconditional_Gate_U'] == s['Universal_CD'] == s['Dynamic_Optimality'] == 'OPEN'
with (B / 'publication_provenance.json').open('x', encoding='utf-8') as f:
    json.dump({
        'status': 'CONTENT_METADATA_NOT_MATHEMATICAL_CERTIFICATION',
        'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
        'tracked_status': '', 'all_new_writes_confined_to_27': True,
        'inherited_local_pins_preserved': len(pins['pins']),
        'frozen_target_unchanged': True, 'C26_content_checkpoint_preserved': True,
        'primary_outcome': 'UNRESOLVED_GUARDED_SOURCE_EXISTENCE',
        'new_smaller_results': 'MANUSCRIPT_DERIVATIONS_INDEPENDENT_AUDIT_PENDING',
        'candidate': 'REJECTED_SECOND_ORIGIN_PAID_AND_ERASED_ROW_TRANSIENT',
        'Gate_U': 'OPEN', 'new_source_or_audit_processes': 0,
        'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
        'entry_metadata_CPU_excluded': entry['metadata_CPU_excluded'],
        'publication_metadata_CPU_excluded': time.process_time(),
        'completed_witness_or_exclusion_created': False,
        'proof_assistant_or_external_audit': False}, f, indent=2)
files = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'bytes': p.stat().st_size}
         for p in sorted(B.iterdir()) if p.is_file() and p.name != 'campaign_manifest.json']
with (B / 'campaign_manifest.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'CONTENT_CHECKPOINT_NOT_PROOF_SEAL',
               'primary': 'UNRESOLVED', 'Gate_U': 'OPEN', 'files': files}, f, indent=2)
print(json.dumps({'status': 'C27_CONTENT_CHECKPOINT_PUBLISHED_PARENT_OPEN',
                  'files': len(files), 'inherited_pins': len(pins['pins']),
                  'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
                  'new_source_or_audit_processes': 0}))
