"""Exclusive final seal of the fixed102-cut strict FI-versus-UD audit."""
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
    prefix = HERE.parent.relative_to(ROOT).as_posix()+'/'
    prior = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*') if p.is_file() and HERE not in p.parents}
    assert prior == {rel for rel in entry['files'] if rel.startswith(prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch, status = git('rev-parse', 'HEAD'), git('branch', '--show-current'), git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, status) == (entry['head'], entry['branch'], entry['tracked_status']) and not status
    assert entry['gate_sha256'] == sha(HERE / 'CA00_FOUR_RULE_GATE.md')
    summary = read(HERE / 'cut_summary.json')
    audit = read(HERE / 'independent_audit.json')
    ledger = read(HERE / 'proof_status_ledger.json')
    ud = read(HERE / 'UD_no_KEEP_lending_certificate.json')
    fi = read(HERE / 'FI_three_block_payment_certificate.json')
    assert audit['status'] == 'PASS'
    for key, name in [('source_fact_table_sha256', 'source_fact_table.json'),
                      ('cut_ledgers_sha256', 'cut_ledgers.json'), ('cut_summary_sha256', 'cut_summary.json'),
                      ('UD_no_KEEP_lending_sha256', 'UD_no_KEEP_lending_certificate.json'),
                      ('FI_three_block_payment_sha256', 'FI_three_block_payment_certificate.json')]:
        assert audit[key] == sha(HERE / name)
    assert summary['fact_table_sha256'] == audit['source_fact_table_sha256']
    assert summary['cut_ledgers_sha256'] == audit['cut_ledgers_sha256']
    assert summary['gate_sha256'] == entry['gate_sha256']
    assert summary['status'] == 'STRICT_FI_ONLY_WITNESS_VERIFIED'
    assert summary['UD_accepted_cuts'] == ud['accepted_UD_cuts'] == []
    assert len(summary['FI_accepted_cuts']) == 92 and summary['FI_accepted_cuts'] == fi['accepted_cuts']
    assert audit['FI_rejected_cuts'] == fi['rejected_cuts'] == [18, 19, 35, 36, 52, 53, 69, 70, 86, 87]
    assert (audit['normal_passes_checked'], audit['reflected_passes_checked'], audit['steps_checked']) == (204, 204, 41616)
    assert audit['source_facts_checked'] == 970 and audit['periods_per_pass'] == 1
    assert audit['physical_pool_visits_per_pass'] == 102
    assert len(ud['inequalities']) == 475 and all(r['ceiling'] >= r['capacity'] for r in ud['inequalities'])
    assert ud['positive_residual_demand'] == 5 and ud['total_DELETE_capacity'] == 4 and ud['final_debt_lower_bound_every_cut'] == 1
    assignments = fi['cut0_full_injection']
    assert len(assignments) == len({tuple(a['unit']) for a in assignments}) == len({tuple(a['demand']) for a in assignments}) == 98
    assert fi['selected_cut'] == 0 and fi['DELETE_units_used'] == fi['startup_units_used'] == fi['reused_units'] == 0
    assert ledger['UD_accepted_count'] == audit['UD_accepted_count'] == 0
    assert ledger['FI_accepted_count'] == audit['FI_accepted_count'] == 92
    assert ledger['reused_units_per_pass'] == ledger['startup_units_used_per_pass'] == ledger['earlier_or_later_lap_units_used'] == 0
    assert ledger['new_source_engine_calls'] == ledger['new_source_words'] == ledger['new_m_values_audited'] == ledger['larger_finite_fits'] == 0
    assert ledger['universal_Step3_CD'] == audit['universal_CD'] == summary['universal_CD'] == 'OPEN'
    assert ledger['matching_terminal_line'] == audit['matching_terminal_line'] == summary['matching_terminal_line'] == 'FROZEN'
    assert ledger['mandatory_strategy_review_completed'] and not ledger['automatic_successor_launched']
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    table = (HERE / 'CA02_ALL_CUTS.md').read_text(encoding='utf-8')
    assert sum(line.startswith('|') for line in table.splitlines()) == 104
    assert summary['source_replays_sha256'] in (HERE / 'CA04_REPRODUCTION.md').read_text(encoding='utf-8')
    for name in ['CA01_STRICT_FI_COVERAGE_AND_PROOF.md', 'CA03_BEFORE_RESULT_AFTER.md']:
        assert (HERE / name).is_file()
    save('final_integrity.json', dict(status='PASS', date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']), prior_research_inventory_unchanged=True,
        Stage_11G_files_unchanged=len(stage), Stage_11G_inventory_unchanged=True,
        head=head, branch=branch, tracked_status=status, four_rule_gate='PASS before execution',
        normal_passes_checked=204, reflected_passes_checked=204, cuts_per_protocol=102, periods_per_pass=1,
        UD_accepted_count=0, FI_accepted_count=92, FI_rejected_count=10,
        independent_checks=sum(audit['checks'].values()), source_reachable=True, nowhere_diagonal=True,
        strict_FI_closed_walk_coverage_beyond_UD='PROVED by exact source witness and established containment',
        no_reused_units=True, no_startup_or_other_lap_credits=True, selected_FI_injection_distinct_units=98,
        new_source_engine_calls=0, larger_finite_fits=0, matching_terminal_line='FROZEN',
        universal_CD='OPEN', automatic_successor_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-11-01', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_prior_files=len(entry['files']), preserved_Stage_11G_files=len(stage),
        sealed_artifacts=len(files), cuts_per_protocol=102, UD_accepted=0, FI_accepted=92,
        independent_checks=sum(audit['checks'].values()), strict_FI_only_witness=True,
        reused_units=0, startup_units=0, universal_CD='OPEN'), indent=2))


if __name__ == '__main__':
    main()
