"""Metadata provenance only. No mathematical evaluator, source replay or audit."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26'
DIRECTIVE = Path('C:/Users/Saif malik/.codex/attachments/d5f31f91-e806-4618-8ba9-ddbf4740f43f/Pasted text.txt')


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def write_new(name, value):
    with (B / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2)


prior = read(OLD / 'dependency_pins.json')
pins = {x['path']: x for x in prior['pins']}
for x in read(OLD / 'campaign_manifest.json')['files']:
    pins[x['path']] = {'path': x['path'], 'sha256': x['sha256'],
                       'origin': 'C26_CONTENT_CHECKPOINT_AUDIT_PENDING'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {
    'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'origin': 'C26_manifest'}
for x in pins.values():
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
external = prior['external_pins'] + [{
    'path': str(DIRECTIVE), 'sha256': sha(DIRECTIVE), 'origin': 'C27 user directive'}]
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
inspected = []
for rel in [
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/CHECKPOINT.md',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/FINAL_VERDICT.md',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/resources_checkpoint.json',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/RV_RETENTION_FIRST_CONSUMER.md',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/RV_EFFECTIVE_OWNER_CERTIFICATE.md',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/DIRECT_CONSUMER_SOURCE_BRIDGE.md',
    'SE03_STEP3_RV_FIRST_CONSUMER_FEASIBILITY_26/SOURCE_FORCED_FROZEN_EXPANSION.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/T19_ARRIVAL_LOCALIZATION.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/R_V_CARRY_FRONTIER.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/PREHISTORY_ZERO_ORIGIN_ATTEMPT.md',
    'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/ERASED_FULL_B_RETURN_CLASSIFICATION.md',
    'SE03_STEP3_EXTREME_FRAME_RETURN_PAIR_21/EXTREME_ORDER_NORMAL_FORM.md',
    'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20/REMAINING_EXTREME_FRAME.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/PAIRED_LEDGER_FUNDING.md',
    'SE03_STEP3_EXTREME_OWNER_RECURSION_22/CREATOR_POLICY_COMPATIBILITY.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/COLLECTIVE_SOURCE_SUPPLY.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/BIRTH_GROUP_REDUCTION.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/LEAF_RECOVERY_BARRIER.md',
    'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/SOURCE_EXACT_EXTERNAL_OWNER_CONTROL.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/SS_SOURCE_INVERSE_LEMMA.md',
    'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/HIGH_CREATOR_REDUCTION.md',
    'SE03_STEP3_RR7_CREATOR_MARKED_FRONTIERS_18/MARKED_PARENT_THEOREM.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FROZEN_OWNER_COMPATIBILITY.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CLOSED_PERIOD_CORE_CONSTANCY.md',
    'SE03_STEP2_UNARY_A_LIFT_14/branch_funding.py',
]:
    p = B.parent / rel
    inspected.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                      'inspection': 'relevant manuscript/interface read or reused from C26 continuation; not executed or independently audited',
                      'status': 'original accepted/pending scopes unchanged; C26_INHERITANCE_LEDGER.md'})
ledger.update(status='CONTENT_PROVENANCE_AND_SCOPE_LEDGER_NOT_PROOF_SEAL',
              C27_inspected=inspected, C27_primary='UNRESOLVED')
write_new('dependency_ledger.json', ledger)
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'inherited_local_pins_verified': len(pins),
    'untracked_inventory_sha256': hashlib.sha256(
        git('status', '--porcelain', '--untracked-files=all').encode()).hexdigest(),
    'frozen_target_sha256': sha(B / 'N26_E4_FROZEN_GUARDS.md'),
    'current_directive_sha256': sha(DIRECTIVE),
    'snapshot_timing': 'after manuscript derivation; frozen guards were first new artifact',
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_audit_processes': 0, 'caps_extended': False,
    'metadata_CPU_excluded': time.process_time()})
print(json.dumps({'status': 'C27_CONTENT_PROVENANCE_RECORDED',
                  'inherited_pins': len(pins), 'new_source_or_audit_processes': 0}))
