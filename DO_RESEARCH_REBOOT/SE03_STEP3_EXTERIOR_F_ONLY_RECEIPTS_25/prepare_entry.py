"""Metadata provenance only. No source/allocator/proof evaluator is run."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24'
DIRECTIVE = Path('C:/Users/Saif malik/.codex/attachments/d0001a2a-6911-477b-8c1d-2d2b924929dc/Pasted text.txt')

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
pins = {x['path']: x for x in prior['pins']}
for x in read(OLD / 'campaign_manifest.json')['files']:
    pins[x['path']] = {'path': x['path'], 'sha256': x['sha256'],
                       'origin': 'C24_CONTENT_CHECKPOINT_AUDIT_PENDING'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {
    'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'origin': 'C24_manifest'}
for x in pins.values():
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
external = prior['external_pins'] + [{
    'path': str(DIRECTIVE), 'sha256': sha(DIRECTIVE), 'origin': 'C25 user directive'}]
for x in external:
    assert sha(Path(x['path'])) == x['sha256'], x['path']
assert git('branch', '--show-current') == 'coarse-double-branch'
assert git('rev-parse', 'HEAD') == '8c378d49283b3738b18e7175886772a98025e4e9'
assert not git('status', '--porcelain', '--untracked-files=no')
r = read(OLD / 'resources_checkpoint.json')
assert r['cumulative_CPU'] == 3619.171875
assert r['cumulative_group_CPU'] == {'symbolic': 118.671875, 'independent': 299.125}
write_new('dependency_pins.json', {
    'status': 'CONTENT_PROVENANCE_NOT_MATHEMATICAL_AUDIT',
    'pins': sorted(pins.values(), key=lambda x: x['path']), 'external_pins': external})
with (B / 'USER_DIRECTIVE.txt').open('xb') as f:
    f.write(DIRECTIVE.read_bytes())

ledger = read(OLD / 'dependency_ledger.json')
for x in ledger['rows']:
    x['C25_status'] = 'inherited exact scope/status; file identity is not new mathematical validation'
inspected = []
for rel in [
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/CHECKPOINT.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/FINAL_VERDICT.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/resources_checkpoint.json',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/OWNER_QUALIFIED_CAPACITY_INTERFACE.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/GLOBAL_OWNER_FRONTIER_THEOREM.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/SOURCE_EXACT_EXTERNAL_OWNER_CONTROL.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/EXTERNAL_OWNER_PROVENANCE.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/EXTERNAL_OWNER_NORMAL_FORMS.md',
    'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/FULL_PROOF.md',
    'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/ERASED_FULL_B_RETURN_CLASSIFICATION.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/PAIRED_LEDGER_FUNDING.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/INCOMING_EXTREME_EXPOSURE.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/CREATOR_POLICY_COMPATIBILITY.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_ORDER_NORMAL_FORM.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_NONLOCAL_SUPPLY.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/H1Q6_EFFECTIVE_OWNER_LEDGER.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/COLLECTIVE_SOURCE_SUPPLY.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/BIRTH_GROUP_REDUCTION.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FROZEN_OWNER_COMPATIBILITY.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CLOSED_PERIOD_CORE_CONSTANCY.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/cd6_allocator.py',
    'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py',
    'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/debt_funding.py',
    'SE03_STEP2_UNARY_A_LIFT_14/branch_funding.py',
    'SE03_STEP2_COLD_NEG2_01/source_model.py',
    'SE03_STEP2_CORE7_SINGLE_EXCESS_11/single_slot_allocator.py',
    'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py',
    'SE03_STEP1_FUND01/source_allocation.py',
    'SE03_STEP1_FUND01/SOURCE_BRIDGE.md',
    'SE03_STEP1_FUND01/SCOPE_AND_DEPENDENCY_AUDIT.md',
    'SE03_STEP1_FUND01/AUXILIARY_FUNDING_THEOREM.md']:
    p = B.parent / rel
    inspected.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                      'inspection': 'relevant manuscript/source interface inspected or reused; not executed or independently audited',
                      'status': 'original accepted/pending scope preserved; see C24_INHERITANCE_LEDGER.md'})
ledger.update(status='CONTENT_PROVENANCE_AND_SCOPE_LEDGER_NOT_PROOF_SEAL', C25_inspected=inspected)
write_new('dependency_ledger.json', ledger)
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'inherited_local_pins_verified': len(pins),
    'untracked_inventory_sha256': hashlib.sha256(
        git('status', '--porcelain', '--untracked-files=all').encode()).hexdigest(),
    'frozen_target_sha256': sha(B / 'OWNER25_FROZEN_SOURCE_BOX.md'),
    'current_directive_sha256': sha(DIRECTIVE),
    'snapshot_timing': 'after manuscript derivation; frozen target was first new artifact',
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_audit_processes': 0, 'caps_extended': False,
    'metadata_CPU_excluded': time.process_time()})
print(json.dumps({'status': 'C25_CONTENT_PROVENANCE_RECORDED', 'inherited_pins': len(pins),
                  'new_source_or_audit_processes': 0}))
