"""Append-only preservation and raw-byte delivery verification."""
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
    assert len(actual)==pins['prior_campaign_files']==948
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert sha(HERE/'OR00_FOUR_RULE_GATE.md')==pins['gate_sha256']
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    manifests={}
    for dirname in ['route_c_fe01_first_entry_20261101_v001','route_c_pf_positive_gap_closure_20261101_v001',
            'route_c_fe02_saturated_return_20261101_v001','route_c_fe02_paired_compatibility_20261101_v001',
            'route_c_fe02_approach_discharge_20261101_v001','route_c_fe02_unequal_interval_escape_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';d=read(p)
        for name,h in d['files'].items():assert sha(p.parent/name)==h,(dirname,name)
        manifests[dirname]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_audit.json')
    assert audit['status']=='PASS' and audit['total_checks']==11841
    assert sha(HERE/'independent_verify_restoration.py')==audit['script_sha256']
    for p,h in audit['certificate_hashes'].items():assert sha(HERE/p)==h,p
    for p,h in audit['original_source_hashes'].items():assert sha(ROOT/p)==h,p
    source=read(HERE/'odd_restoration_source_certificate.json')
    for name in ['A_return_source_certificate.json','B_child_barrier_certificate.json']:
        d=read(HERE/name)
        assert d['source_certificate_sha256']==sha(HERE/'odd_restoration_source_certificate.json')
        assert d['independent_audit_sha256']==sha(HERE/'independent_audit.json')
    for field in ['rows','symbolic_rows','reflected_rows']:
        rows=source[field];p=source['positive_block'];r=source['first_restoration_block']
        assert rows[p]['source_A']==rows[r]['destination_A']
        assert rows[p]['source_B']!=rows[r]['destination_B']
    rows=source['rows'];assert rows[7]['source_B'][2][0]==2<7<rows[9]['destination_B'][2][0]==8
    ledger=read(HERE/'proof_status_ledger.json')
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    result=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=948,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_preserved=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=manifests,independent_source_checks=11841,
        genuine_FE02_closed_control=dict(blocks=34,A=46,Q=16,one_positive=[1,3]),
        local_first_restoration_payment='REFUTED—EXACT; no CD counterexample',
        ordered_source_restoration_or_B_nonclosure='PROVED at explicit source scope',
        arbitrary_child_reset_payment='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',
        larger_finite_fits=0,larger_key_count_replays=0,connector_or_coefficient_search=False,
        Git_writes=False,all_writes_confined_to_this_new_research_directory=True)
    save(HERE/'final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save(HERE/'delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=948,
        Stage11G_files=125,delivery_files=len(files)+1,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
