"""Exclusive FE02 seal; never promote open rigidity from finite checks."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
FE=BASE/'route_c_fe01_first_entry_20261101_v001'


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():assert sha(ROOT/rel)==h,rel
    for rel,h in read(HERE/'additional_dependency_pins.json')['files'].items():assert sha(ROOT/rel)==h,rel
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    old={rel for rel in entry['files'] if rel.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual==old and len(actual)==entry['prior_campaign_files']
    for name,h in read(FE/'delivery_manifest.json')['files'].items():assert sha(FE/name)==h,name
    assert sha(FE/'independent_audit.json')==entry['inherited_FE01_audit_sha256']
    prior=read(FE/'independent_audit.json');assert prior['status']=='PASS' and prior['total_checks']==350259
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    current_stage={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert current_stage==entry['stage_files'] and len(current_stage)==125
    assert git('rev-parse','HEAD')==entry['head']
    assert git('branch','--show-current')==entry['branch']=='coarse-double-branch'
    assert git('status','--porcelain=v1','--untracked-files=no')==''
    assert sha(HERE/'FE02_00_FOUR_RULE_GATE.md')==entry['gate_sha256']
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    audit=read(HERE/'independent_audit.json');diag=read(HERE/'exact_return_loss_diagnostic.json')
    root=read(HERE/'root_return_certificate.json');ledger=read(HERE/'proof_status_ledger.json')
    assert audit['status']==diag['status']=='PASS'
    assert audit['root_access_cases']==1287 and audit['root_input_trees']==99
    assert audit['root_return_certificate_sha256']==sha(HERE/'root_return_certificate.json')
    assert audit['mixed_certificate_sha256']==sha(HERE/'mixed_timing_certificate.json')
    assert diag['root_audit_sha256']==sha(HERE/'independent_audit.json')
    assert root['source_formula_sha256']==sha(HERE/'source_root_budget.py')
    assert not root['actual_saturated_return_found'] and root['formal_signature_not_a_counterexample']
    for orientation in ['ordinary','reflected']:
        r=root['regression'][orientation]
        assert (r['source_totals']['A'],r['source_totals']['Q_B'],r['source_totals']['negative_slack'])==(25,22,29)
        assert r['source_forced_donor']==4 and r['direct_injection']['paid_demands']==22
        assert r['direct_injection']['startup_units_used']==r['direct_injection']['reused_units']==0
        assert r['inherited_FE_cut0']['accepted'] and r['inherited_FE_cut0']['final_debt']==0
    assert ledger['FE02_RIGIDITY']==ledger['FE02_CD']==ledger['universal_Coarse_Double']=='OPEN'
    assert not ledger['Step_3_complete'] and not ledger['Coarse_Double_counterexample_claimed']
    for p in HERE.glob('*.py'):
        compile(p.read_text(encoding='utf-8'),str(p),'exec')
    # Check the append-only reproduction print repair without executing capture.
    old_capture=(HERE/'capture_entry.py').read_text(encoding='utf-8')
    assert old_capture.count("len(pins['files'])")==1
    compile(old_capture.replace("len(pins['files'])",'len(pins)'),str(HERE/'capture_entry_v002.py'),'exec')
    assert not any(p.is_dir() for p in HERE.iterdir()),'unexpected cache or nested output'
    save('final_integrity.json',dict(status='PASS',head=entry['head'],branch=entry['branch'],tracked_status='',
        inherited_files_preserved=len(entry['files']),prior_campaign_inventory_preserved=len(actual),
        additional_read_dependencies_preserved=2,stage_11g_files_and_inventory_preserved=125,
        inherited_FE01_seal_and_350259_checks='UNCHANGED',matching_terminal='FROZEN',
        original_source_FI_PF_FE_PG_M1_M2_M3_and_prior_statuses='UNCHANGED',
        outcome='B — partial source-return theorem; principal FE02 OPEN',
        arithmetic_saturation_reduction='PROVED—UNIVERSAL',mixed_block_timing_reduction='PROVED—UNIVERSAL costed boundaries',
        root_departure_return_gap_and_short_donor_criterion='PROVED—UNIVERSAL',
        exact_loss_identity='PROVED diagnostic; not counted as target advancement',
        FE02_RIGIDITY='OPEN',FE02_CD='OPEN',universal_Coarse_Double='OPEN',
        actual_saturated_return_found=False,Coarse_Double_counterexample_claimed=False,
        new_independent_source_checks=audit['total_checks'],exact_diagnostic_checks=diag['total_checks'],
        mandatory_W_A=25,mandatory_W_Q=22,new_direct_donor_block=4,FE01_designated_cut_preserved=True,
        physical_key_count=13,repetition_controls=[1],larger_finite_fits=0,source_searches=0,
        larger_key_count_or_repetition_replays=0,automatic_FE03_launched=False,
        saved_capture_print_fix='V002, never executed over retained entry; scientific capture succeeded inline'))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(schema='raw SHA256; excludes this manifest',files=files,
        sealed_files=len(files),final_integrity_sha256=sha(HERE/'final_integrity.json')))
    print(json.dumps(dict(status='PASS',sealed_files=len(files),inherited_files_preserved=len(entry['files']),
        prior_campaign_inventory_preserved=len(actual),stage_11g=125,
        new_checks=audit['total_checks'],diagnostic_checks=diag['total_checks'],
        FE02_RIGIDITY='OPEN',FE02_CD='OPEN',universal_Coarse_Double='OPEN'),indent=2))


if __name__=='__main__':main()
