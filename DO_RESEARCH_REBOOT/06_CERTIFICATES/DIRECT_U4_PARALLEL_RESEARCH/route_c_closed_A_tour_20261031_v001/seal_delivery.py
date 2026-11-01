"""Exclusive seal of the exhausted fixed A-tour class and all prior files."""
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
    assert sha(HERE / 'AT00_FOUR_RULE_GATE.md') == entry['gate_sha256']
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    ledger = json.loads((HERE / 'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['cases'] == 276 and audit['cap_cases'] == 0
    assert audit['A_identity_sha256'] == sha(HERE / 'closed_A_identity_certificate.json')
    assert audit['mode_class_sha256'] == sha(HERE / 'mode_class_certificate.json')
    assert audit['total_pointer_source_calls'] == 21168 and audit['strict_BST_tree_occurrences'] == 42336
    assert audit['max_G_B_all_cycles'] == audit['max_J_B_all_cycles'] == audit['max_E_all_cycles'] == 0
    assert ledger['examined_cases'] == ledger['declared_cases'] == 276
    assert ledger['one_period_exact_two_reset_cycles'] == 168 and ledger['two_period_four_reset_cycles'] == 108
    assert not ledger['general_all_A_tour_obstruction_claimed'] and not ledger['new_original_CD_walk_class_settled']
    assert ledger['finite_fits'] == ledger['adaptive_tour_changes'] == ledger['FI_UD_cut_trials'] == 0
    assert ledger['universal_CD'] == 'OPEN' and ledger['matching_terminal_line'] == 'FROZEN'
    assert not ledger['next_campaign_launched'] and ledger['mandatory_strategy_review_completed']
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
        inherited_source_and_previous_run_files_unchanged=len(entry['files']), previous_research_inventory_unchanged=True,
        stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True, head=head, branch=branch, tracked_status=status,
        matching_terminal_line='FROZEN', fixed_mode_class_cases=276, complete_classification=True,
        max_G_B=0, max_J_B=0, max_E=0, requested_cycle='NOT FOUND; general existence OPEN',
        new_original_CD_walk_class_settled=False, strict_FI_only_closed_walk_coverage='NOT ESTABLISHED',
        universal_CD='OPEN', next_campaign_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_files=len(entry['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), complete_mode_class=276, G_B=0, J_B=0, E=0,
        requested_cycle='NOT FOUND'), indent=2))


if __name__ == '__main__':
    main()
