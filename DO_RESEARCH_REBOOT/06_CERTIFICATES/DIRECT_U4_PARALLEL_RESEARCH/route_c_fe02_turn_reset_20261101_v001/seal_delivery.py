"""Append-only raw-byte freeze verification and current delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
STAGE = ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def save(name, value):
    with (HERE/name).open('x', encoding='utf-8') as f:
        json.dump(value, f, indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git','--no-optional-locks',*args],cwd=ROOT,text=True).strip()


def main():
    pins = read(HERE/'entry_source_pins.json')
    for path, h in pins['files'].items():
        assert sha(ROOT/path) == h, path
    prefix = BASE.relative_to(ROOT).as_posix()+'/'
    expected = {p for p in pins['files'] if p.startswith(prefix)}
    actual = {p.relative_to(ROOT).as_posix() for p in BASE.rglob('*')
              if p.is_file() and HERE not in p.parents}
    assert actual == expected, (sorted(actual-expected),sorted(expected-actual))
    assert len(actual) == pins['prior_campaign_files'] == 1004
    stage = {p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage == pins['stage_files'] and len(stage) == 125
    assert sha(HERE/'TR00_FOUR_RULE_GATE.md') == pins['gate_sha256']
    assert git('rev-parse','HEAD') == pins['head']
    assert git('branch','--show-current') == pins['branch']
    assert git('status','--short','--untracked-files=no') == pins['tracked_status'] == ''
    freeze = BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    frozen = {}
    for dirname in ['route_c_fe01_first_entry_20261101_v001',
        'route_c_pf_positive_gap_closure_20261101_v001',
        'route_c_fe02_saturated_return_20261101_v001',
        'route_c_fe02_paired_compatibility_20261101_v001',
        'route_c_fe02_approach_discharge_20261101_v001',
        'route_c_fe02_unequal_interval_escape_20261101_v001',
        'route_c_fe02_odd_restoration_20261101_v001',
        'route_c_fe02_boundary_lift_20261101_v001',
        'route_c_fe02_coupled_excursions_20261101_v001']:
        p = BASE/dirname/'delivery_manifest.json'
        d = read(p)
        for f,h in d['files'].items():
            assert sha(p.parent/f) == h, (dirname,f)
        frozen[dirname] = dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit = read(HERE/'independent_audit.json')
    assert audit['status'] == 'PASS' and audit['total_checks'] == 33261
    assert audit['fixed_source_updates'] == 140 and audit['qualifying_old_closed_return_contexts'] == 52
    assert sha(HERE/'independent_verify_turn_reset.py') == audit['script_sha256']
    for p,h in audit['certificate_hashes'].items():
        assert sha(HERE/p) == h, p
    for p,h in audit['original_source_hashes'].items():
        assert sha(ROOT/p) == h, p
    source = read(HERE/'inward_reset_source_certificate.json')
    assert source['gate_sha256'] == pins['gate_sha256']
    assert source['new_exact_symbolic_core_keys'] == 16
    assert (source['actual_capacity'],source['actual_demand']) == (10,11)
    assert source['no_negative_block'] and source['positive_blocks'] == [0]
    assert (source['initial_B_child'],source['final_B_child']) == (11,5)
    assert source['rows'][-1]['destination_A'] != source['source_A']
    assert source['rows'][-1]['destination_B'] != source['source_B']
    assert not source['reachable_closed_FE02_refutation']
    assert not source['Coarse_Double_counterexample']
    for p,h in read(HERE/'closed_source_LCA_audit_certificate.json')['source_hashes'].items():
        assert sha(ROOT/p) == h, p
    ledger = read(HERE/'proof_status_ledger.json')
    assert ledger['FE02_CD'] == ledger['FE02_RIGIDITY'] == ledger['Universal_Coarse_Double'] == 'OPEN'
    assert ledger['new_exact_symbolic_core_keys'] == 16
    assert ledger['fixed_source_audit']['independent_checks'] == audit['total_checks']
    assert ledger['unrestricted_valid_source_child_reset_payment']['status'] == 'REFUTED—EXACT'
    for p in HERE.iterdir():
        assert p.is_file(), ('unexpected subdirectory or cache',p)
        if p.suffix == '.json':
            read(p)
    result = dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=1004,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_unchanged=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,independent_checks=audit['total_checks'],
        source_identity='PROVED—UNIVERSAL at initially-rooted one-sided source scope',
        near_anchor_return_repayment='PROVED—UNIVERSAL at explicit h_B-j_B+e_B<=3 condition',
        coupled_closure='PROVED—RESTRICTED DOMAIN: ordered or qualifying-endpoint phases',
        new_exact_symbolic_core_keys=16,open_episode_capacity=10,open_episode_demand=11,
        diagonal_reachability_of_new_episode='NOT ESTABLISHED',
        full_paired_closed_provenance_of_new_episode='NOT ESTABLISHED; episode itself is not closed',
        arbitrary_deep_turn_coupled_closure='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        Coarse_Double_counterexample=False,larger_finite_fits=0,
        source_graph_or_coefficient_search=False,Git_writes=False,
        all_writes_confined_to_this_new_research_directory=True)
    save('final_integrity.json', result)
    files = {p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=1004,
        Stage11G_files=125,delivery_files=len(files)+1,independent_checks=audit['total_checks'],
        new_exact_symbolic_core_keys=16,FE02_CD='OPEN'),indent=2))


if __name__ == '__main__':
    main()
