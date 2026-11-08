"""Dependency scope/provenance transcription only; no mathematical execution."""
import hashlib
import json
from pathlib import Path

B = Path(__file__).resolve().parent
ROOT = B.parent.parent
OLD = B.parent / 'SE03_STEP3_H1Q6_COLLECTIVE_SUPPLY_20'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

rows = json.loads((OLD / 'dependency_ledger.json').read_text(encoding='utf-8'))['rows']
inspected = {
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/CD6_FINAL_CERTIFICATE.json',
    'SE03_STEP2_CD6_FINAL_ASSEMBLY_14/UNIFORM_R_TRANSFER.md',
    'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/UNIFORM_LEAF_CHANNEL_THEOREM.md',
    'SE03_STEP3_UNIFORM_DONOR_GROUPING_15/FROZEN_OWNER_EXCHANGE.md',
    'SE03_STEP3_NONLOCAL_OWNERSHIP_TRANSFER_16/NONLOCAL_AUGMENTATION.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/BIRTH_GROUP_REDUCTION.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/FROZEN_OWNER_PRESERVATION.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/HIGH_LOW_INTERFACE.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/COMPARISON_SAFE_FRONTIERS.md',
    'SE03_STEP3_JOINT_LOW_BUNDLE_REPAYMENT_19/ZERO_WEIGHT_NONLOCAL_TRANSFER.md'
}
for x in rows:
    assert sha(ROOT / x['path']) == x['sha256'], x['path']
    rel = x['path'].removeprefix('DO_RESEARCH_REBOOT/')
    x['C21_inspection'] = ('source manuscript/interface read; no independent audit' if rel in inspected
                            else 'inherited exact status and scope reused; content hash only')

c20 = [
    ('REMAINING_EXTREME_FRAME.md', 'Original extreme effective-owner target', 'OPEN'),
    ('FINAL_VERDICT.md', 'Three positive source classes; primary U20 open', 'PROVISIONAL_CHECKPOINT'),
    ('FROZEN_H1Q6_OBLIGATION.md', 'Exact deep two-arrival domain and owner distinctions', 'FROZEN_OPEN_TARGET'),
    ('THREE_PREDECESSOR_CLASSIFICATION.md', 'Saturated unary/branch p/v/t source forms', 'DERIVATION_AUDIT_PENDING'),
    ('H1Q6_RECOVERY_NORMAL_FORM.md', 'H1 word/geometry and deep support rigidity', 'DERIVATION_AUDIT_PENDING'),
    ('SECOND_NONLOCAL_DONOR.md', 'G20 root degree, guards and post-own-tail freshness', 'DERIVATION_AUDIT_PENDING'),
    ('ORDERED_ANCESTOR_SUPPLY.md', 'O20 order G<R<C<x/reflection', 'DERIVATION_COMPLETE_AUDIT_PENDING'),
    ('FIRST_DIRECTION_CHANGE_SUPPLY.md', 'F20 order G<R<x<C/reflection, at most5 predecessors', 'DERIVATION_COMPLETE_AUDIT_PENDING'),
    ('SECOND_DIRECTION_CHANGE_SUPPLY.md', 'M20 order G<C<x<R/reflection', 'DERIVATION_COMPLETE_AUDIT_PENDING'),
    ('LOCAL_SPARE_LEDGER.md', 'Stored actual A80 owners, B82 ownership unknown', 'PINNED_PROVISIONAL_SOURCE_EVIDENCE'),
    ('COLLECTIVE_SOURCE_SUPPLY.md', 'Joint comparison injection versus effective completion', 'PARTIAL_MAIN_OPEN'),
    ('GATE_U_DISCHARGE.md', 'Exact open E_r interfaces', 'U_OPEN'),
    ('INDEPENDENT_AUDIT_STATUS.md', 'No C20 proof process and pending statuses', 'AUDIT_PENDING'),
    ('resources_checkpoint.json', 'Authoritative unchanged cap balances', 'FROZEN_METADATA')
]
for name, statement, status in c20:
    p = OLD / name
    rows.append({
        'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
        'exact_interface': statement, 'result_state': status,
        'source_domain': 'exact C20 domain; see frozen obligation and C20 dependency reconstruction',
        'proof_inspection': 'full relevant manuscript/interface read in C21; no source/independent execution',
        'accepted_or_provisional': 'scope preserved; no seal promotion'})

sources = []
for rel in ['SE03_STEP2_COLD_NEG2_01/source_model.py',
            'SE03_STEP2_FULL_FUNDING_CLOSURE_10/physical_exchange.py']:
    p = B.parent / rel
    sources.append({'path': p.relative_to(ROOT).as_posix(), 'sha256': sha(p),
                    'inspection': 'source read only; not imported or executed'})
with (B / 'dependency_ledger.json').open('x', encoding='utf-8') as f:
    json.dump({'status': 'PROVENANCE_SCOPE_NOT_PROOF_SEAL', 'rows': rows,
               'source_artifacts': sources, 'independent_runs': 0}, f, indent=2)
print(json.dumps({'status': 'C21_DEPENDENCIES_RECORDED', 'rows': len(rows),
                  'source_artifacts': len(sources)}))
