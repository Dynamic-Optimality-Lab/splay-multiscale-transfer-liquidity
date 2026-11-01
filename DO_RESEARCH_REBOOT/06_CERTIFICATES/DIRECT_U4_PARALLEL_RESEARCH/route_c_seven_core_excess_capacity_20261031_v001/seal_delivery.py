"""Exclusive integrity seal; no old source/research/status writers are run."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    entry = read(HERE / 'entry_source_pins.json')
    for rel, h in entry['files'].items():
        assert sha(ROOT / rel) == h, rel
    prior_prefix = HERE.parent.relative_to(ROOT).as_posix()+'/'
    prior_files = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*')
                   if p.is_file() and HERE not in p.parents}
    assert prior_files == {rel for rel in entry['files'] if rel.startswith(prior_prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch = git('rev-parse', 'HEAD'), git('branch', '--show-current')
    status = git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (entry['head'], entry['branch'], entry['tracked_status'])
    assert not status
    assert sha(HERE / 'EC00_FOUR_RULE_GATE.md') == entry['gate_sha256']
    cap = read(HERE / 'capacity_certificate.json')
    joint = read(HERE / 'joint_return_certificate.json')
    audit = read(HERE / 'independent_audit.json')
    uniform = read(HERE / 'uniform_return_identity.json')
    injection = read(HERE / 'event_unit_injection_certificate.json')
    ledger = read(HERE / 'proof_status_ledger.json')
    assert audit['status'] == injection['status'] == 'PASS'
    assert audit['joint_return_sha256'] == sha(HERE / 'joint_return_certificate.json')
    assert audit['full_source_replays_sha256'] == injection['source_replays_sha256'] == sha(HERE / 'full_source_replays.json')
    assert audit['uniform_identity_sha256'] == sha(HERE / 'uniform_return_identity.json')
    assert cap['status'] == 'UNBOUNDED_CORE_TAIL_EXCESS'
    assert joint['status'] == 'JOINT_THRESHOLD_RETURN_CONSTRUCTED'
    assert joint['capacity_sha256'] == sha(HERE / 'capacity_certificate.json')
    assert joint['completion_gate_sha256'] == sha(HERE / 'EC00A_JOINT_COMPONENT_COMPLETION_GATE.md')
    assert (audit['E'], audit['C_D'], audit['G_B'], audit['J_B']) == (12, 4, 17, 5)
    assert (audit['diagonal_return_actions'], audit['physical_resets'], audit['A'], audit['Q_B'], audit['Z_B']) == (139, 2, 204, 176, 73)
    assert (uniform['E'], uniform['C_D'], uniform['G_B'], uniform['J_B']) == ('2+2m', 4, '2+3m', 'm')
    assert uniform['status'] == 'PROVED—RESTRICTED DOMAIN'
    assert len(uniform['recurrent_R7_inputs']) == 34 and not joint['off_diagonal_reset_input_found']
    assert joint['off_diagonal_return'] is None and not audit['nowhere_diagonal']
    assert ledger['concrete_non_simple_closed_walk'] and not ledger['concrete_full_cyclic_core_scan']
    assert not ledger['new_original_CD_walk_class_settled']
    assert ledger['strict_FI_only_closed_walk_coverage'] == 'NOT ESTABLISHED'
    assert ledger['universal_Step3_CD'] == audit['universal_CD'] == uniform['universal_CD'] == 'OPEN'
    assert ledger['new_source_engine_calls'] == ledger['new_active_core_sizes'] == ledger['larger_finite_fits'] == 0
    assert ledger['matching_terminal_line'] == 'FROZEN' and ledger['mandatory_strategy_review_completed']
    assert not ledger['automatic_successor_launched']
    assignments = injection['checked_mapping']
    assert len(assignments) == len({tuple(r['unit']) for r in assignments}) == len({tuple(r['demand']) for r in assignments}) == 176
    assert injection['DELETE_units_used'] == injection['reachability_prefix_units_used'] == injection['reused_units'] == 0
    assert injection['helper_demand_assignments'] == 12
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    for name in ['EC01_UNIFORM_RETURN_IDENTITY.md', 'EC02_GRAPH_AND_SOURCE_AUDIT.md',
                 'EC03_BEFORE_RESULT_AFTER.md', 'EC04_REPRODUCTION.md']:
        assert (HERE / name).is_file()
    save('final_integrity.json', dict(status='PASS', date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']),
        previous_research_inventory_unchanged=True, stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True,
        head=head, branch=branch, tracked_status=status,
        uniform_return_identity='PROVED—RESTRICTED DOMAIN; all m>=0, arbitrary untouched fringe',
        concrete_E=12, concrete_C_D=4, concrete_G_B=17, concrete_J_B=5,
        physical_resets=2, each_reset_a=1, concrete_nowhere_diagonal=False,
        concrete_non_simple_closed_walk=True, event_capacity_reuse=0,
        new_original_CD_walk_class_settled=False, universal_CD='OPEN',
        matching_terminal_line='FROZEN', automatic_successor_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-11-01', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', prior_files=len(entry['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), uniform_return='PROVED—RESTRICTED DOMAIN',
        E=12, C_D=4, G_B=17, J_B=5, physical_resets=2, universal_CD='OPEN'), indent=2))


if __name__ == '__main__':
    main()
