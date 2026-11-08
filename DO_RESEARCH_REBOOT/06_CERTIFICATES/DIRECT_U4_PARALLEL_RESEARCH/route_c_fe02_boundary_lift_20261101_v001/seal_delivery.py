"""Append-only raw delivery and frozen-state/inventory audit."""
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
    assert len(actual)==pins['prior_campaign_files']==970
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==pins['stage_files'] and len(stage)==125
    assert sha(HERE/'BL00_FOUR_RULE_GATE.md')==pins['gate_sha256']
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']
    assert git('status','--short','--untracked-files=no')==pins['tracked_status']==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8-sig')
    frozen={}
    for name in ['route_c_fe01_first_entry_20261101_v001','route_c_pf_positive_gap_closure_20261101_v001',
            'route_c_fe02_saturated_return_20261101_v001','route_c_fe02_paired_compatibility_20261101_v001',
            'route_c_fe02_approach_discharge_20261101_v001','route_c_fe02_unequal_interval_escape_20261101_v001',
            'route_c_fe02_odd_restoration_20261101_v001']:
        p=BASE/name/'delivery_manifest.json';d=read(p)
        for f,h in d['files'].items():assert sha(p.parent/f)==h,(name,f)
        frozen[name]=dict(manifest_sha256=sha(p),files=len(d['files']),all_raw_hashes_valid=True)
    audit=read(HERE/'independent_audit.json')
    assert audit['status']=='PASS' and audit['total_checks']==34696
    assert sha(HERE/'independent_verify_boundary_lift.py')==audit['script_sha256']
    for p,h in audit['certificate_hashes'].items():assert sha(HERE/p)==h,p
    for p,h in audit['original_source_hashes'].items():assert sha(ROOT/p)==h,p
    certificate=read(HERE/'boundary_lift_source_certificate.json')
    for p,h in certificate['source_hashes'].items():assert sha(ROOT/p)==h,p
    assert certificate['status']=='PASS' and not certificate['discrepancies']
    ad=read(BASE/'route_c_fe02_approach_discharge_20261101_v001/closed_discharge_certificate.json')
    for name,c in ad['cases'].items():
        rs=c['rows']
        for i,r in enumerate(rs):
            prev=rs[i-1]
            assert (prev['destination_A'],prev['destination_B'])==(r['source_A'],r['source_B']),(name,i)
    shortcut=read(HERE/'composition_shortcut_obstruction_certificate.json')
    assert shortcut['complete_A_returns'] and shortcut['number_of_A_comparison_corrections']==1
    assert shortcut['opposite_A_comparison_corrections']==0
    assert shortcut['base_lift']!=shortcut['original_A_source']==shortcut['corrected_result']
    ledger=read(HERE/'proof_status_ledger.json')
    assert ledger['FE02_CD']==ledger['FE02_RIGIDITY']==ledger['Universal_Coarse_Double']=='OPEN'
    for p in HERE.iterdir():
        assert p.is_file(),('unexpected cache/subdirectory',p)
        if p.suffix=='.json':read(p)
    out=dict(status='PASS',HEAD=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_file_hashes_checked=len(pins['files']),prior_campaign_exact_inventory=970,
        Stage11G_files=125,Stage11G_exact_bytes_and_inventory_unchanged=True,
        FE01_PG02_and_all_prior_research_unchanged=True,matching_terminal='FROZEN',
        frozen_manifests=frozen,independent_checks=34696,fixed_source_rows=179,
        source_classification='PROVED by source identity and arbitrary-prefix induction',
        global_composition='OPEN; proof gate not passed',
        expanded_FE02_source_domain='PROVED with original distinct-unit injection',
        FE02_CD='OPEN',Universal_Coarse_Double='OPEN',Coarse_Double_counterexample=False,
        larger_finite_fits=0,larger_source_key_count_replays=0,source_graph_or_coefficient_search=False,
        Git_writes=False,all_writes_confined_to_this_new_directory=True)
    save(HERE/'final_integrity.json',out)
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file()}
    assert 'delivery_manifest.json' not in files
    save(HERE/'delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files))
    print(json.dumps(dict(status='PASS',inherited_hashes=len(pins['files']),prior_inventory=970,
        Stage11G_files=125,delivery_files=len(files)+1,FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
