"""Append-only old-byte/inventory audit and current delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BASE=HERE.parent
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,d):
    with p.open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')
def git(*a):return subprocess.check_output(['git','--no-optional-locks',*a],cwd=ROOT,text=True).strip()


def main():
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():assert sha(ROOT/p)==h,p
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in pins['files'] if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert expected==actual,(sorted(actual-expected),sorted(expected-actual))
    assert len(actual)==pins['prior_campaign_files']==988
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert sha(HERE/'CE00_FOUR_RULE_GATE.md')==pins['gate_sha256']
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    frozen={}
    for dirname in ['route_c_fe01_first_entry_20261101_v001','route_c_pf_positive_gap_closure_20261101_v001',
            'route_c_fe02_saturated_return_20261101_v001','route_c_fe02_paired_compatibility_20261101_v001',
            'route_c_fe02_approach_discharge_20261101_v001','route_c_fe02_unequal_interval_escape_20261101_v001',
            'route_c_fe02_odd_restoration_20261101_v001','route_c_fe02_boundary_lift_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';d=read(p)
        for f,h in d['files'].items():assert sha(p.parent/f)==h,(dirname,f)
        frozen[dirname]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_audit.json')
    assert audit['status']=='PASS' and audit['total_checks']==14201
    assert sha(HERE/'independent_verify_coupled_excursions.py')==audit['script_sha256']
    for p,h in audit['certificate_hashes'].items():assert sha(HERE/p)==h,p
    for p,h in audit['original_source_hashes'].items():assert sha(ROOT/p)==h,p
    source=read(HERE/'coupled_excursion_control_certificate.json')
    assert source['status']=='VERIFIED_FE02_ORDERED_EXCURSION_CONTROL'
    assert (source['block_count'],source['excursion_count'],source['A'],source['Q'])==(35,17,45,22)
    assert source['positive_blocks']==[8] and source['full_pair_closed']
    coverage=read(HERE/'anchor_coverage_certificate.json')
    assert coverage['qualifying_anchors']==[] and len(coverage['anchors'])==13
    oldp=BASE/'route_c_fe02_odd_restoration_20261101_v001/odd_restoration_source_certificate.json'
    assert coverage['source_certificate_sha256']==sha(oldp)
    ledger=read(HERE/'proof_status_ledger.json')
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    result=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=988,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_unchanged=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,independent_checks=14201,
        coupled_source_theorem='PROVED at ordered-anchor excursion scope, arbitrary number and sides',
        actual_FE02_control=dict(blocks=35,excursions=17,A=45,Q=22,positive_block=8),
        unqualified_anchor_coverage='REFUTED—EXACT by valid OR34 control',
        arbitrary_nonordered_composition='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        Coarse_Double_counterexample=False,larger_finite_fits=0,larger_source_key_count_replays=0,
        source_graph_or_coefficient_search=False,Git_writes=False,
        all_writes_confined_to_this_new_research_directory=True)
    save(HERE/'final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save(HERE/'delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=988,
        Stage11G_files=125,delivery_files=len(files)+1,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
