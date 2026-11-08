"""Long-path delivery seal, preserving explicit historical baseline limits."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
RAW_HERE=Path(__file__).resolve().parent;RAW_ROOT=RAW_HERE.parents[3]
ROOT=Path('\\\\?\\'+str(RAW_ROOT))
HERE=ROOT/RAW_HERE.relative_to(RAW_ROOT);BASE=HERE.parent
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=RAW_ROOT,text=True).strip()


def main():
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():assert sha(ROOT/p)==h,p
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in pins['files'] if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert expected==actual and len(actual)==pins['prior_campaign_files']==1038
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    full=read(HERE/'full_stage_inventory_review.json')
    assert full['status']=='PASS' and full['actual_file_count']==528
    assert stage==full['current_full_baseline'] and len(stage)==528
    assert len(pins['stage_files'])==125
    for p,h in pins['stage_files'].items():assert stage[p]==h,p
    assert full['tracked_HEAD_files']==510 and full['tracked_raw_HEAD_matches']==416
    assert full['tracked_EOL_only_matches']==94 and full['tracked_content_differences']==[]
    assert full['untracked_file_count']==18 and len(full['untracked_without_entry_pin'])==15
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
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    result=dict(status='PASS_WITH_DOCUMENTED_BASELINE_LIMIT',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_raw_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=1038,
        FE01_PG02_and_all_prior_campaign_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,Stage11G_actual_files=528,Stage11G_entry_pinned_files=125,
        Stage11G_entry_pinned_raw_hashes_unchanged=True,Stage11G_full_current_baseline_rechecked=True,
        Stage11G_tracked_files=510,Stage11G_tracked_raw_HEAD_matches=416,Stage11G_tracked_EOL_only_matches=94,
        Stage11G_tracked_non_EOL_content_differences=0,Stage11G_untracked_files=18,
        Stage11G_untracked_without_entry_hashes=15,Stage11G_source_writes=0,
        Stage11G_historical_raw_baseline_limit='Fifteen untracked files lacked entry hashes; current hashes establish a new baseline, not retrospective raw equality. Newly visible tracked files compared independently to frozen HEAD.',
        Stage11G_legacy_complete_125_file_claim='CORRECTED; actual inventory528',
        full_stage_review_sha256=sha(HERE/'full_stage_inventory_review.json'),
        independent_source_checks=47635,old_source_rows=291,old_corpus_representations=14,
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
    print(json.dumps(dict(status=result['status'],inherited_hashes=len(pins['files']),prior_inventory=1038,
        Stage11G_actual_files=528,Stage11G_entry_pinned_unchanged=125,
        Stage11G_tracked_HEAD_content_verified=510,Stage11G_untracked_without_entry_hash=15,
        delivery_files=len(files)+1,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
