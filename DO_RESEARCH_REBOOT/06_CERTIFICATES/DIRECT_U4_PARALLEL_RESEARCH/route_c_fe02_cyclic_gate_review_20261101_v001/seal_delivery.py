"""Final read-only inherited freeze audit and append-only review seal."""
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
    assert expected==actual and len(actual)==pins['prior_campaign_files']==1038
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert sha(HERE/'CG00_PRE_EXECUTION_GATE_REVIEW.md')==pins['gate_sha256']
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
        'route_c_fe02_turn_reset_20261101_v001',
        'route_c_fe02_deep_closure_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';d=read(p)
        for f,h in d['files'].items():assert sha(p.parent/f)==h,(dirname,f)
        frozen[dirname]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_source_review.json')
    assert audit['status']=='PASS' and audit['total_checks']==47635
    assert sha(HERE/'audit_source_telescope.py')==audit['script_sha256']
    assert sha(HERE/'existing_source_telescope_review_certificate.json')==audit['certificate_sha256']
    assert sha(BASE/'route_c_fe02_turn_reset_20261101_v001/independent_verify_turn_reset.py')==audit['frozen_harness_sha256']
    for p,h in audit['original_source_hashes'].items():assert sha(ROOT/p)==h,p
    source=read(HERE/'existing_source_telescope_review_certificate.json')
    assert source['review_only'] and not source['new_proof_campaign_authorized']
    for p,h in source['inherited_source_hashes'].items():assert sha(ROOT/p)==h,p
    assert source['source_rows_audited']==291 and len(source['corpora'])==14
    ledger=read(HERE/'proof_status_ledger.json')
    assert ledger['global_eventual_discharge_campaign_gate']['status']=='FAIL'
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    assert ledger['new_actual_reachable_closed_walk_coverage']=='NONE'
    assert ledger['existing_source_review']['checks']==47635
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    result=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=1038,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_unchanged=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,independent_checks=47635,old_source_rows=291,old_corpus_representations=14,
        proof_campaign_gate='FAIL; mandatory strategy/source review only',new_proof_campaign_executed=False,
        mathematical_advancement_of_FE02='NONE',new_actual_reachable_closed_walk_coverage='NONE',
        unrestricted_eventual_repayment='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        new_source_states_or_words_constructed=0,new_key_counts_or_fringe_substitutions=0,
        larger_finite_fits=0,source_graph_or_connector_search=False,Coarse_Double_counterexample=False,
        Git_writes=False,all_new_writes_confined_to_this_directory=True)
    save('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=1038,
        Stage11G_files=125,delivery_files=len(files)+1,proof_campaign_gate='FAIL; review only',FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
