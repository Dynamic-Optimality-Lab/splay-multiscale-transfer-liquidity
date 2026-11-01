"""Seal this append-only component, its limits, and every prior-file pin."""
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
    old_inventory = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*')
        if p.is_file() and HERE not in p.parents}
    prefix = HERE.parent.relative_to(ROOT).as_posix() + '/'
    assert old_inventory == {rel for rel in entry['files'] if rel.startswith(prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch, status = git('rev-parse', 'HEAD'), git('branch', '--show-current'), git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (entry['head'], entry['branch'], entry['tracked_status']) and not status
    assert sha(HERE / 'BC00_FOUR_RULE_GATE.md') == entry['gate_sha256']
    audit = json.loads((HERE / 'independent_audit.json').read_text(encoding='utf-8'))
    assert audit['status'] == 'PASS' and audit['certificate_sha256'] == sha(HERE / 'burst_B_cycle_certificate.json')
    assert (audit['Q_B'], audit['Z_B'], audit['G_B'], audit['J_B']) == (20, 19, 5, 5)
    assert audit['simple'] and audit['length'] == 26 and audit['pointer_source_accesses'] == 52
    assert audit['delayed_anchor_payer_entries'] == 48 and audit['no_guaranteed_minimum_pool_UD_spare']
    delayed = json.loads((HERE / 'delayed_UD_ceiling_profile.json').read_text(encoding='utf-8'))
    assert len(delayed['entries']) == 48 and all(v['UD_own_work_ceiling'] >= 2 for v in delayed['entries'])
    ledger = json.loads((HERE / 'proof_status_ledger.json').read_text(encoding='utf-8'))
    assert ledger['source_component_target'] == 'ACHIEVED' and ledger['G_B'] == ledger['J_B'] == 5
    assert not ledger['actual_E_or_C_D_certified'] and not ledger['new_original_CD_walk_class_settled']
    assert ledger['actual_A_resets_executed'] == ledger['FI_UD_cut_trials'] == ledger['finite_fits'] == 0
    assert ledger['universal_CD'] == 'OPEN' and ledger['all_cut_UD_rejection'] == 'NOT ESTABLISHED'
    assert ledger['matching_terminal_line'] == 'FROZEN' and not ledger['next_campaign_launched']
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    save('final_integrity.json', dict(status='PASS', date='2026-10-31',
        inherited_source_and_previous_run_files_unchanged=len(entry['files']),
        previous_research_inventory_unchanged=True, stage_11G_files_unchanged=len(stage),
        stage_inventory_unchanged=True, head=head, branch=branch, tracked_status=status,
        matching_terminal_line='FROZEN', source_component_target='ACHIEVED', G_B=5, J_B=5,
        simple_cycle_length=26, delayed_ceiling_entries=48,
        no_guaranteed_minimum_pool_UD_spare=True, actual_A_resets_executed=0,
        all_cut_UD_rejection='NOT ESTABLISHED', strict_FI_only_closed_walk_coverage='NOT ESTABLISHED',
        universal_CD='OPEN', next_campaign_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-10-31', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_files=len(entry['files']), stage_11G_files=len(stage),
        sealed_artifacts=len(files), G_B=5, J_B=5, paired_strictness='OPEN'), indent=2))


if __name__ == '__main__':
    main()
