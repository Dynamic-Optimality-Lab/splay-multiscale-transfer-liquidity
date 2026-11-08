"""Exact old-file preservation and current append-only delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def save(p,d):
    with p.open('x',encoding='utf-8') as f:json.dump(d,f,indent=2);f.write('\n')


def main():
    pins=read(HERE/'entry_source_pins.json')
    for p,h in pins['files'].items():assert sha(ROOT/p)==h,p
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    expected={p for p in pins['files'] if p.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert expected==actual,(sorted(actual-expected),sorted(expected-actual))
    assert len(actual)==pins['prior_campaign_files']==897
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    old_manifests={}
    for dirname in ['route_c_fe01_first_entry_20261101_v001','route_c_pf_positive_gap_closure_20261101_v001',
            'route_c_fe02_saturated_return_20261101_v001','route_c_fe02_paired_compatibility_20261101_v001']:
        p=BASE/dirname/'delivery_manifest.json';d=read(p)
        for name,h in d['files'].items():assert sha(p.parent/name)==h,(dirname,name)
        old_manifests[dirname]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_audit.json');assert audit['status']=='PASS' and audit['total_checks']==20549
    for name,h in audit['certificate_hashes'].items():assert sha(HERE/name)==h,name
    assert sha(HERE/'independent_verify_discharge.py')==audit['script_sha256']
    for name,h in audit['source_hashes'].items():assert sha(ROOT/name)==h,name
    scoped=read(HERE/'scoped_obstruction_certificate.json')
    assert sha(HERE/'independent_audit.json')==scoped['independent_audit_sha256']
    assert sha(HERE/'closed_discharge_certificate.json')==scoped['source_certificate_sha256']
    for p in HERE.iterdir():
        assert p.is_file(),('no unrecorded caches/subdirectories',p)
        if p.suffix=='.json':read(p)
    ledger=read(HERE/'proof_status_ledger_v002.json')
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    result=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_inventory=897,
        prior_campaign_exact_inventory_preserved=True,Stage11G_files=125,
        Stage11G_exact_inventory_and_bytes_preserved=True,matching_terminal='FROZEN',
        FE01_PG02_original_algorithms_and_all_frozen_certificates_unchanged=True,
        frozen_manifests=old_manifests,new_independent_checks=audit['total_checks'],
        scoped_immediate_discharge_obstruction='REFUTED—EXACT; no FE02 counterexample',
        final_status_ledger='proof_status_ledger_v002.json',FE02_CD='OPEN',
        Universal_Coarse_Double='OPEN',larger_finite_fits=0,Git_writes=False,
        writes_confined_to_new_append_only_research_directory=True)
    save(HERE/'final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save(HERE/'delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=897,
        Stage11G_files=125,delivered_files=len(files)+1,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
