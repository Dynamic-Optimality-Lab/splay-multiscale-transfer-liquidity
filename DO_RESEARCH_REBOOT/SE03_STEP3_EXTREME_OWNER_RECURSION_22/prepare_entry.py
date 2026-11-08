"""Metadata and verbatim saved-evidence transcription. No source engine/checker."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21'
DIRECTIVE = Path('C:/Users/Saif malik/.codex/attachments/ace620c2-55db-4cf9-8111-9f403214ba16/Pasted text.txt')

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write_new(n, data):
    with (B / n).open('x', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

prior = read(OLD / 'dependency_pins.json')
pins = {x['path']: x for x in prior['pins']}
for x in read(OLD / 'campaign_manifest.json')['files']:
    pins[x['path']] = {'path': x['path'], 'sha256': x['sha256'],
                       'origin': 'C21_CONTENT_CHECKPOINT_AUDIT_PENDING'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {'path': p.relative_to(ROOT).as_posix(),
                                     'sha256': sha(p), 'origin': 'C21_manifest'}
for x in pins.values():
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
external = prior['external_pins'] + [{'path': str(DIRECTIVE), 'sha256': sha(DIRECTIVE),
                                      'origin': 'current recursive resource-discovery directive'}]
for x in external:
    assert sha(Path(x['path'])) == x['sha256'], x['path']

def git(*a):
    return subprocess.check_output(['git', *a], cwd=ROOT, text=True).strip()

assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status', '--porcelain', '--untracked-files=no')
r = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == {'symbolic': 118.671875, 'independent': 299.125}
write_new('dependency_pins.json', {'status': 'PROVENANCE_ONLY_NOT_PROOF_AUDIT',
                                  'pins': sorted(pins.values(), key=lambda x: x['path']),
                                  'external_pins': external})
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'inherited_local_pins_verified': len(pins),
    'untracked_inventory_sha256': hashlib.sha256(git('status', '--porcelain', '--untracked-files=all').encode()).hexdigest(),
    'frozen_target_sha256': sha(B / 'FROZEN_TARGET_AND_BOXES.md'),
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_audit_processes': 0, 'caps_extended': False,
    'metadata_CPU_excluded': time.process_time()})
with (B / 'USER_DIRECTIVE.txt').open('x', encoding='utf-8') as f:
    f.write(DIRECTIVE.read_text(encoding='utf-8'))

# Copy supplied historical evidence, WITHOUT replay, owner-map validation,
# new arithmetic, or a closure assertion. Original producer status is retained.
source = B.parent / 'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/fully_aligned_countercertificates.json'
data = read(source)
c = next(x for x in data['cases'] if x['erased'] == 13 and x['mirrored'] is False
         and x['actual_interval'] == [179, 258])
old_fact = read(B.parent / 'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20/frozen_local_owner_witness.json')
write_new('source_countercontrol.json', {
    'status': 'VERBATIM_SAVED_EVIDENCE_TRANSCRIPTION_NOT_NEW_VERIFICATION',
    'inherited_status': data['status'], 'source_path': source.relative_to(ROOT).as_posix(),
    'source_sha256': sha(source), 'selector': {'erased': 13, 'mirrored': False, 'actual_interval': [179, 258]},
    'common_initial': c['common_initial'], 'actual_reaching_prefix': c['actual_reaching_prefix'],
    'initial_A': c['initial_A'], 'initial_BF': c['initial_BF'], 'initial_BE': c['initial_BE'],
    'original_period_operations': [{k: x[k] for k in ['occurrence', 'mode', 'target']} for x in c['rows']],
    'stored_final_trees': c['rows'][-1]['after'], 'maps': c['maps'],
    'stored_row_223': next(x for x in c['rows'] if x['occurrence'] == 223),
    'transcribed_owner_fact': old_fact['local_units'][1],
    'new_rotation_replays': 0, 'new_semantic_or_independent_checks': 0,
    'scope': 'refutes free-fE implies free-a ONLY; not a new extreme-frame counterexample'})

ledger = read(OLD / 'dependency_ledger.json')
for row in ledger['rows']:
    row['R22_status'] = 'inherited exact scope/status; content provenance only unless inspected below'
additional = []
for rel in [
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_NONLOCAL_SUPPLY.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_OWNER_EXCHANGE.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/OWNER_FRONTIER_CLOSURE_OBLIGATION.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/CHECKPOINT.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/resources_checkpoint.json',
    'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/HIGH_CREATOR_REDUCTION.md',
    'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/MARKED_PARENT_THEOREM.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/HIGH_LOW_INTERFACE.md',
    'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/cd6_allocator.py',
    '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md']:
    p = B.parent / rel
    additional.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                       'inspection': 'relevant manuscript/source read, not executed or independently audited',
                       'status': 'inherited scope/status preserved'})
ledger.update(status='PROVENANCE_AND_SCOPES_NOT_PROOF_SEAL', continuation_inspected=additional)
write_new('dependency_ledger.json', ledger)
print(json.dumps({'status': 'R22_ENTRY_AND_TRANSCRIPTION_RECORDED', 'pins': len(pins),
                  'new_source_or_audit_processes': 0}))
