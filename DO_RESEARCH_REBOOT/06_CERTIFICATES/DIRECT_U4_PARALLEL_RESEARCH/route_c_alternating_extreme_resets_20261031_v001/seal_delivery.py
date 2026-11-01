"""Exclusive integrity seal; preserve the failed gate and open global target."""
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
    for rel, digest in entry['files'].items():
        assert sha(ROOT / rel) == digest, rel
    prefix = HERE.parent.relative_to(ROOT).as_posix() + '/'
    previous = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*') if p.is_file() and HERE not in p.parents}
    assert previous == {rel for rel in entry['files'] if rel.startswith(prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch, status = git('rev-parse', 'HEAD'), git('branch', '--show-current'), git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (entry['head'], entry['branch'], entry['tracked_status']) and not status
    assert sha(HERE / 'AE00_FOUR_RULE_GATE.md') == entry['gate_sha256']
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    cert = json.loads((HERE / 'B_preflight_certificate.json').read_text(encoding='utf-8'))
    ledger = json.loads((HERE / 'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['B_preflight_sha256'] == sha(HERE / 'B_preflight_certificate.json')
    assert cert['outcome'] == 'B_BUDGET_BLOCKED'
    assert (audit['recurrent_G_B'], audit['recurrent_J_B'], audit['pointer_B_calls']) == (4, 1, 60)
    assert audit['A_policy_cases_executed'] == cert['A_policy_cases_executed'] == ledger['A_policy_cases_executed'] == 0
    assert not ledger['general_two_reset_nonexistence_claimed'] and not ledger['A_orbit_classification_claimed']
    assert not ledger['new_original_CD_walk_class_settled'] and not ledger['next_campaign_launched']
    assert ledger['universal_CD'] == 'OPEN' and ledger['matching_terminal_line'] == 'FROZEN'
    assert ledger['finite_fits'] == ledger['word_replacements'] == ledger['FI_UD_cut_trials'] == 0
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
        inherited_source_and_previous_run_files_unchanged=len(entry['files']), previous_research_inventory_unchanged=True,
        stage_11G_files_unchanged=len(stage), stage_inventory_unchanged=True, head=head, branch=branch, tracked_status=status,
        matching_terminal_line='FROZEN', mandatory_B_gate='FAILED: G_B=4',
        scoped_effective_two_reset_exclusion=True, A_policy_cases_executed=0,
        requested_A_B_cycle='NOT FOUND; general existence OPEN', universal_CD='OPEN',
        strict_FI_only_closed_walk_coverage='NOT ESTABLISHED', next_campaign_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_files=len(entry['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), G_B=4, J_B=1, A_cases=0, requested_cycle='NOT FOUND'), indent=2))


if __name__ == '__main__':
    main()
