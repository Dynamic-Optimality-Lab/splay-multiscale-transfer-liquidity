"""Content metadata only: no source replay, allocation, debt or proof audit."""
import hashlib
import json
import subprocess
import time
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25'
DIRECTIVE = Path('C:/Users/Saif malik/.codex/attachments/80876125-9de8-47ec-9552-89f86e47fc02/Pasted text.txt')


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
                       'origin': 'C25_CONTENT_CHECKPOINT_AUDIT_PENDING'}
p = OLD / 'campaign_manifest.json'
pins[p.relative_to(ROOT).as_posix()] = {
    'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p), 'origin': 'C25_manifest'}
for x in pins.values():
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
external = prior['external_pins'] + [{
    'path': str(DIRECTIVE), 'sha256': sha(DIRECTIVE), 'origin': 'C26 user directive'}]
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
paths = [
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/CHECKPOINT.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/FINAL_VERDICT.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/resources_checkpoint.json',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/C24_INHERITANCE_LEDGER.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/R_V_CARRY_FRONTIER.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/T19_ARRIVAL_LOCALIZATION.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/RETAINED_FULL_ERASED_RECEIPTS.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/FROZEN_OWNER_GLOBAL_FUNDING.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/OWNER_POLICY_COMPLETENESS.md',
    'SE03_STEP3_EXTERIOR_F_ONLY_RECEIPTS_25/GATE_U_DISCHARGE_STATUS.md',
    'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/FULL_PROOF.md',
    'SE03_STEP3_NONIDENTITY_A_TREE_FLIP_23/ERASED_FULL_B_RETURN_CLASSIFICATION.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/OWNER_QUALIFIED_CAPACITY_INTERFACE.md',
    'SE03_STEP3_OUTSIDE_F_ONLY_OWNER_PROTECTION_24/GLOBAL_OWNER_FRONTIER_THEOREM.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/COLLECTIVE_SOURCE_SUPPLY.md',
    'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/SOURCE_SPEC.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/FROZEN_OWNER_COMPATIBILITY.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/SOURCE_SPEC.md',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/cd6_allocator.py',
    'SE03_STEP2_UNARY_A_LIFT_14/branch_funding.py',
    'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/debt_funding.py',
    'SE03_STEP2_MULTICORE_FUNDING_CLOSURE_13/source_funding.py',
    'SE03_STEP2_COLD_NEG2_01/source_model.py',
    'SE03_STEP2_CORE7_SINGLE_EXCESS_11/single_slot_allocator.py',
    'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py',
    'SE03_STEP1_FUND01/source_allocation.py',
    '06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md',
]
for rel in paths:
    p = B.parent / rel
    inspected.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                      'inspection': 'relevant source/manuscript interface read or reused from continuation; not executed or independently audited',
                      'status': 'original scope/status retained; see C25_INHERITANCE_LEDGER.md'})
ledger.update(status='CONTENT_PROVENANCE_AND_SCOPE_LEDGER_NOT_PROOF_SEAL',
              C26_inspected=inspected, C26_parent='UNRESOLVED')
write_new('dependency_ledger.json', ledger)
write_new('entry.json', {
    'branch': git('branch', '--show-current'), 'head': git('rev-parse', 'HEAD'),
    'tracked_status': '', 'inherited_local_pins_verified': len(pins),
    'untracked_inventory_sha256': hashlib.sha256(
        git('status', '--porcelain', '--untracked-files=all').encode()).hexdigest(),
    'frozen_target_sha256': sha(B / 'C26_FROZEN_ARCHITECTURE_TEST.md'),
    'current_directive_sha256': sha(DIRECTIVE),
    'snapshot_timing': 'after manuscript derivation; frozen target was first new artifact',
    'global_CPU': r['cumulative_CPU'], 'group_CPU': r['cumulative_group_CPU'],
    'new_source_or_audit_processes': 0, 'caps_extended': False,
    'metadata_CPU_excluded': time.process_time()})
print(json.dumps({'status': 'C26_CONTENT_PROVENANCE_RECORDED',
                  'inherited_pins': len(pins), 'new_source_or_audit_processes': 0}))
