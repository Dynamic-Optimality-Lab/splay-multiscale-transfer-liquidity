"""Preservation only: frozen raw baselines and explicitly required manifests."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode=True
RAW_HERE=Path(__file__).resolve().parent;RAW_ROOT=RAW_HERE.parents[3]
ROOT=Path('\\\\?\\'+str(RAW_ROOT));HERE=ROOT/RAW_HERE.relative_to(RAW_ROOT);BASE=HERE.parent
OLD=BASE/'route_c_fe02_cyclic_gate_review_20261101_v001'
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(n,d):
    with (HERE/n).open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=RAW_ROOT,text=True).strip()


def main():
    previous=read(OLD/'entry_source_pins.json');files=dict(previous['files'])
    for p,h in files.items():assert sha(ROOT/p)==h,p
    old_manifest=read(OLD/'delivery_manifest.json')
    assert {p.name for p in OLD.iterdir()}==set(old_manifest['files'])|{'delivery_manifest.json'}
    for p,h in old_manifest['files'].items():assert sha(OLD/p)==h,p
    for p in OLD.iterdir():
        assert p.is_file();files[p.relative_to(ROOT).as_posix()]=sha(p)
    full=read(OLD/'full_stage_inventory_review.json')
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==full['current_full_baseline'] and len(stage)==528
    for p,h in stage.items():files[(STAGE/p).relative_to(ROOT).as_posix()]=h
    assert len(files)==1605
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in files if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert expected==actual and len(actual)==1056
    assert git('rev-parse','HEAD')==previous['head']
    assert git('branch','--show-current')==previous['branch']
    assert git('status','--short','--untracked-files=no')==previous['tracked_status']==''
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
        'route_c_fe02_deep_closure_20261101_v001',
        'route_c_fe02_cyclic_gate_review_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';manifest=read(p)
        for f,h in manifest['files'].items():assert sha(p.parent/f)==h,(dirname,f)
        frozen[dirname]=dict(manifest_sha256=sha(p),files=len(manifest['files']),all_raw_hashes_valid=True)
    legacy=BASE/'route_c_analytic_20261030_v001'
    legacyfile=legacy/'entry_source_pins.json'
    legacykey=legacyfile.relative_to(ROOT).as_posix()
    legacy_expected=read(legacy/'delivery_manifest.json')['files']['entry_source_pins.json']
    legacy_actual=sha(legacyfile)
    assert legacy_actual==previous['files'][legacykey] and legacy_actual!=legacy_expected
    mismatch=dict(path=legacykey,manifest_expected_sha256=legacy_expected,
        actual_raw_sha256=legacy_actual,prior_CG_entry_hash=previous['files'][legacykey],
        current_turn_changed_file=False,classification='PRE-EXISTING LEGACY MANIFEST INCONSISTENCY',
        old_files_preserved=True)
    pins=dict(head=previous['head'],branch=previous['branch'],tracked_status='',files=files,
        stage_files=stage,prior_campaign_files=1056,corrected_complete_Stage11G_entry_baseline=528,
        historical_baseline_limit='Fifteen untracked files first baselined in CG; all528 have a prior baseline for this turn',
        gate_sha256=sha(HERE/'RR00_GATE.md'),proof_campaign_gate='FAIL')
    save('entry_source_pins.json',pins)
    for p,h in files.items():assert sha(ROOT/p)==h,p
    result=dict(status='PASS_WITH_DOCUMENTED_LEGACY_MANIFEST_LIMIT',HEAD=previous['head'],branch=previous['branch'],
        tracked_status='',inherited_raw_hashes_checked=1605,prior_campaign_exact_inventory=1056,
        Stage11G_complete_files=528,Stage11G_all528_prior_raw_hashes_unchanged=True,
        FE01_PG02_matching_terminal_and_prior_research_unchanged=True,matching_terminal='FROZEN',
        required_frozen_manifests=frozen,unmodified_legacy_manifest_mismatch=mismatch,
        all_legacy_manifests_internally_valid='NOT CLAIMED',
        source_engines_imported=False,new_source_experiments=0,larger_finite_fits=0,
        source_graph_or_connector_search=False,Git_writes=False,
        mathematical_proof_campaign_gate='FAIL',new_proof_campaign_executed=False,
        independent_residual_bound='NOT DERIVED',FE02_CD='OPEN',FE02_RIGIDITY='OPEN',
        Universal_Coarse_Double='OPEN',mathematical_advancement='NONE',new_closed_walk_coverage='NONE',
        all_new_writes_confined_to_this_directory=True)
    save('final_integrity.json',result)
    manifest={p.name:sha(p) for p in HERE.iterdir() if p.is_file()}
    assert 'delivery_manifest.json' not in manifest
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=manifest))
    print(json.dumps(dict(status=result['status'],inherited_hashes=1605,Stage11G_complete_files=528,
        all528_prior_hashes_unchanged=True,proof_campaign_gate='FAIL',FE02_CD='OPEN',
        pre_existing_legacy_manifest_mismatch_recorded=True,new_source_experiments=0,
        delivery_files=len(manifest)+1),indent=2))


if __name__=='__main__':main()
