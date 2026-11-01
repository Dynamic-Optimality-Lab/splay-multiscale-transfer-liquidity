"""Exclusive final seal of the nowhere-diagonal immediate-residual witness."""
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
        json.dump(value, f, indent=2, ensure_ascii=False)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


def main():
    entry = read(HERE / 'entry_source_pins.json')
    for rel, h in entry['files'].items():
        assert sha(ROOT / rel) == h, rel
    prefix = HERE.parent.relative_to(ROOT).as_posix()+'/'
    prior_inventory = {p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*')
                       if p.is_file() and HERE not in p.parents}
    assert prior_inventory == {rel for rel in entry['files'] if rel.startswith(prefix)}
    stage = {p.relative_to(STAGE).as_posix(): sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == entry['stage_files'] and len(stage) == 125
    head, branch = git('rev-parse', 'HEAD'), git('branch', '--show-current')
    tracked = git('status', '--porcelain=v1', '--untracked-files=no')
    assert (head, branch, tracked) == (entry['head'], entry['branch'], entry['tracked_status'])
    assert not tracked
    assert entry['gate_sha256'] == sha(HERE / 'NI00_FOUR_RULE_GATE.md')
    local = read(HERE / 'local_fragment_certificate.json')
    result = read(HERE / 'nowhere_return_certificate.json')
    audit = read(HERE / 'independent_audit.json')
    uniform = read(HERE / 'uniform_nowhere_identity.json')
    cut = read(HERE / 'immediate_helper_cut.json')
    ledger = read(HERE / 'proof_status_ledger.json')
    assert audit['status'] == 'PASS'
    for key, name in [('local_certificate_sha256', 'local_fragment_certificate.json'),
                      ('return_certificate_sha256', 'nowhere_return_certificate.json'),
                      ('full_source_replays_sha256', 'full_source_replays.json'),
                      ('immediate_helper_cut_sha256', 'immediate_helper_cut.json'),
                      ('uniform_identity_sha256', 'uniform_nowhere_identity.json')]:
        assert audit[key] == sha(HERE / name)
    assert local['gate_sha256'] == entry['gate_sha256']
    assert result['local_certificate_sha256'] == audit['local_certificate_sha256']
    assert result['status'] == 'THRESHOLD_AND_RESIDUAL_RETURN_CONSTRUCTED'
    assert (local['internal_positive_edges_checked'], local['next_KEEP_fragments_checked'], local['qualifying_count']) == (282, 1508, 16)
    assert (audit['E'], audit['C_D'], audit['G_B'], audit['J_B'], audit['R_imm']) == (5, 4, 5, 5, 5)
    assert (audit['concrete_actions'], audit['A'], audit['Q_B'], audit['Z_B']) == (102, 137, 98, 63)
    assert audit['nowhere_diagonal'] and audit['physical_resets'] == 2 and audit['reset_a_values'] == [1, 1]
    assert uniform['status'] == 'PROVED—RESTRICTED DOMAIN' and uniform['nowhere_diagonal'] and uniform['paired_closed']
    assert (uniform['E'], uniform['C_D'], uniform['G_B'], uniform['J_B'], uniform['R_imm']) == ('m', 4, 'm', 'm', 'm')
    assert len(cut['demands']) == len({tuple(d) for d in cut['demands']}) == 25
    assert len(cut['pair_capacity_units']) == len({tuple(u) for u in cut['pair_capacity_units']}) == 20
    assert len(cut['all_DELETE_units']) == 4 and cut['deficit'] == 1
    assert not ({tuple(u) for u in cut['all_DELETE_units']} & {tuple(u) for u in cut['pair_capacity_units']})
    assert cut['no_reused_units'] and cut['reachability_prefix_units_used'] == 0
    assert not cut['original_Hall_graph_claimed'] and not cut['universal_CD_counterexample_claimed']
    assert ledger['concrete_nowhere_diagonal'] and ledger['concrete_non_simple_closed_walk']
    assert not ledger['concrete_full_cyclic_core_scan'] and not ledger['request_word_proper_power']
    assert ledger['startup_units_used_for_cycle'] == 0 and ledger['separate_startup_DELETEs'] == 2
    assert ledger['strict_new_FI_only_closed_walk_coverage'] == 'NOT ESTABLISHED'
    assert ledger['FI_acceptance'] == 'NOT CLASSIFIED' and ledger['UD_rejection_every_cut'] == 'NOT ESTABLISHED'
    assert ledger['universal_Step3_CD'] == audit['universal_CD'] == result['universal_CD'] == 'OPEN'
    assert ledger['new_source_engine_calls'] == ledger['larger_finite_fits'] == ledger['new_active_core_sizes'] == ledger['new_source_clock_searches'] == 0
    assert ledger['mandatory_strategy_review_completed'] and not ledger['automatic_successor_launched']
    assert ledger['matching_terminal_line'] == result['matching_terminal_line'] == 'FROZEN'
    freeze = HERE.parent / 'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    for name in ['NI01_NOWHERE_RETURN_AND_PROOF.md', 'NI02_SOURCE_AND_UNIT_AUDIT.md',
                 'NI03_BEFORE_RESULT_AFTER.md', 'NI04_REPRODUCTION.md']:
        assert (HERE / name).is_file()
    save('final_integrity.json', dict(status='PASS', date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']),
        prior_research_inventory_unchanged=True, Stage_11G_files_unchanged=len(stage), Stage_11G_inventory_unchanged=True,
        head=head, branch=branch, tracked_status=tracked,
        source_identity='PROVED—RESTRICTED DOMAIN; all m>=0 and arbitrary untouched fringe',
        nowhere_diagonal=True, recurrent_resets=2, each_reset_a=1, concrete_actions=102,
        E=5, C_D=4, G_B=5, J_B=5, R_imm=5, immediate_pair_plus_DELETE_cut_deficit=1,
        independent_checks=sum(audit['checks'].values()), prefix_credit_used=0, no_reused_cut_units=True,
        strict_FI_only_coverage='NOT ESTABLISHED', universal_CD='OPEN', matching_terminal_line='FROZEN',
        automatic_successor_launched=False))
    files = {p.name: sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name != 'delivery_manifest.json'}
    save('delivery_manifest.json', dict(date='2026-11-01', files=files, manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS', preserved_prior_files=len(entry['files']), preserved_Stage_11G_files=len(stage),
        sealed_artifacts=len(files), nowhere_diagonal=True, recurrent_resets=2, E=5, C_D=4,
        G_B=5, J_B=5, R_imm=5, strict_immediate_template_cut_deficit=1, universal_CD='OPEN'), indent=2))


if __name__ == '__main__':
    main()
