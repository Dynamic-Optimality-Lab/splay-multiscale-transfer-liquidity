"""Exclusive seal of the graph refutation and its below-threshold return control."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
STAGE = ROOT / 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, value):
    with (HERE / name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    entry = json.loads((HERE / 'entry_source_pins.json').read_text(encoding='utf-8'))
    for rel, h in entry['files'].items():
        assert sha(ROOT / rel) == h, rel
    prefix = HERE.parent.relative_to(ROOT).as_posix() + '/'
    previous = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*') if p.is_file() and HERE not in p.parents}
    assert previous == {rel for rel in entry['files'] if rel.startswith(prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch, status = git('rev-parse', 'HEAD'), git('branch', '--show-current'), git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (entry['head'], entry['branch'], entry['tracked_status']) and not status
    assert sha(HERE / 'KC00_FOUR_RULE_GATE.md') == entry['gate_sha256']
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    graph = json.loads((HERE / 'reachable_relation_certificate.json').read_text(encoding='utf-8'))
    control = json.loads((HERE / 'literal_return_certificate.json').read_text(encoding='utf-8'))
    ledger = json.loads((HERE / 'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['source_table_sha256'] == sha(HERE / 'source_transition_table.json')
    assert audit['relation_sha256'] == sha(HERE / 'reachable_relation_certificate.json')
    assert audit['positive_extension_sha256'] == sha(HERE / 'positive_extension_certificate.json')
    assert (audit['pointer_source_calls'], audit['strict_BST_tree_occurrences']) == (6038, 12076)
    assert (graph['states'], graph['edges'], len(graph['positive_edges'])) == (18450, 109410, 324)
    assert graph['outcome'] == 'NO_FURTHER_EXCESS_CLAIM_REFUTED' and graph['queue_exhausted']
    assert control['status'] == 'PASS' and control['paired_closed'] and control['source_actions'] == 19
    assert control['source_table_sha256'] == audit['source_table_sha256']
    assert control['source_audit_sha256'] == sha(HERE / 'independent_audit.json')
    assert (control['E'], control['C_D'], control['G_B'], control['J_B']) == (2, 4, 2, 0)
    assert control['physical_resets'] == 2 and control['additional_engine_calls'] == 0
    assert ledger['literal_control_E'] == 2 and ledger['literal_control_J_B'] == 0
    assert ledger['higher_budget_amplification_and_return'] == 'OPEN; NOT CONSTRUCTED'
    assert not ledger['new_original_CD_walk_class_settled'] and not ledger['general_two_reset_impossibility_claimed']
    assert ledger['larger_finite_fits'] == ledger['SCC_or_maximum_amplification_searches'] == ledger['new_clock_searches'] == 0
    assert ledger['matching_terminal_line'] == 'FROZEN' and ledger['universal_CD'] == 'OPEN'
    assert ledger['mandatory_strategy_review_completed'] and not ledger['automatic_successor_launched']
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
        inherited_source_and_prior_files_unchanged=len(entry['files']), previous_research_inventory_unchanged=True,
        stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True, head=head, branch=branch, tracked_status=status,
        matching_terminal_line='FROZEN', no_further_excess_claim='REFUTED—EXACT',
        exact_below_threshold_pair_return=True, control_E=2, control_C_D=4, control_G_B=2, control_J_B=0,
        requested_high_threshold_identity='OPEN; NOT CONSTRUCTED', universal_CD='OPEN', automatic_successor_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', prior_files=len(entry['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), exact_return=True, E=2, C_D=4, G_B=2, J_B=0,
        high_threshold_identity='OPEN'), indent=2))


if __name__ == '__main__':
    main()
