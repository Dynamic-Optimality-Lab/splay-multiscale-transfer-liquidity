"""Read-only inherited integrity checks, append-only current delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT,text=True).strip()


def main():
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():assert sha(ROOT/p)==h,p
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in pins['files'] if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert expected==actual and len(actual)==pins['prior_campaign_files']==1020
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    for p,h in pins['gate_hashes'].items():assert sha(HERE/p)==h,p
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    frozen={}
    for dirname in ['route_c_fe01_first_entry_20261101_v001',
        'route_c_pf_positive_gap_closure_20261101_v001',
        'route_c_fe02_saturated_return_20261101_v001',
        'route_c_fe02_paired_compatibility_20261101_v001',
        'route_c_fe02_approach_discharge_20261101_v001',
        'route_c_fe02_unequal_interval_escape_20261101_v001',
        'route_c_fe02_odd_restoration_20261101_v001',
        'route_c_fe02_boundary_lift_20261101_v001',
        'route_c_fe02_coupled_excursions_20261101_v001',
        'route_c_fe02_turn_reset_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';d=read(p)
        for f,h in d['files'].items():assert sha(p.parent/f)==h,(dirname,f)
        frozen[dirname]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_audit.json')
    assert audit['status']=='PASS' and audit['total_checks']==12002
    assert audit['both_original_engines'] and not audit['current_producer_imported']
    assert sha(HERE/'independent_verify_deep_closure.py')==audit['script_sha256']
    harness=BASE/'route_c_fe02_turn_reset_20261101_v001/independent_verify_turn_reset.py'
    assert sha(harness)==audit['frozen_harness_sha256']
    for p,h in audit['certificate_hashes'].items():assert sha(HERE/p)==h,p
    for p,h in audit['original_source_hashes'].items():assert sha(ROOT/p)==h,p
    profile=read(HERE/'terminal_depth_profile_certificate.json')
    assert profile['status']=='PASS' and len(profile['core_next_rows'])==15 and len(profile['gap_table'])==17
    assert profile['all_nonroot_core_queries_negative'] and profile['all_matched_gap_queries_negative']
    escape=read(HERE/'unequal_gap_escape_certificate.json')
    assert escape['status']=='PASS' and escape['total_explicit_keys']==22 and escape['core_keys']==16
    assert (escape['actual_capacity'],escape['actual_demand'])==(14,15)
    assert escape['no_negative_block'] and escape['positive_blocks']==[0] and not escape['paired_closed']
    assert not escape['reachable_closed_FE02_refutation'] and not escape['Coarse_Double_counterexample']
    ledger=read(HERE/'proof_status_ledger.json')
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    assert ledger['independent_evidence']['checks']==12002
    assert ledger['immediate_discharge_from_equal_gap_key_sets']['total_explicit_nodes']==22
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    result=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=1020,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_unchanged=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,independent_checks=12002,
        source_core_next_targets=15,formal_gap_pairs=17,unbounded_matched_gap_proof='source substitution plus exact two-parity identity',
        immediate_unequal_gap_discharge='REFUTED—EXACT at fixed source scope',
        inherited_core_nodes=16,explicit_fringe_nodes=6,total_explicit_nodes_in_single_fixed_substitution=22,
        diagonal_reachability_of_deep_pattern='NOT ESTABLISHED',
        actual_reachable_closed_nonvacuity_of_deep_pattern='NOT ESTABLISHED',
        unequal_escape_prefix_closed=False,unequal_escape_prefix_capacity=14,unequal_escape_prefix_demands=15,
        unrestricted_reachable_paired_cyclic_discharge='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        Coarse_Double_counterexample=False,larger_finite_fits=0,source_graph_or_connector_search=False,
        strict_new_FI_PF_FE_coverage='NOT CLAIMED',Git_writes=False,
        all_new_writes_confined_to_this_directory=True)
    save('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=1020,
        Stage11G_files=125,delivery_files=len(files)+1,independent_checks=12002,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
