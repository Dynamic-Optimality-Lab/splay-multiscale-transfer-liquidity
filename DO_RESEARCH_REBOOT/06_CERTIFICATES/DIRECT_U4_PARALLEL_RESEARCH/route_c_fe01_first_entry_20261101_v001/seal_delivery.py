"""Exclusive FE01 delivery seal and complete preservation audit."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent
PG=BASE/'route_c_pf_positive_gap_closure_20261101_v001'


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    pins=read(HERE/'entry_source_pins.json')
    for rel,h in pins['files'].items():assert sha(ROOT/rel)==h,rel
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    old_inventory={rel for rel in pins['files'] if rel.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual==old_inventory and len(actual)==pins['prior_campaign_files']
    for name,h in read(PG/'delivery_manifest.json')['files'].items():assert sha(PG/name)==h,name
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert stage_now==pins['stage_files'] and len(stage_now)==125
    assert git('rev-parse','HEAD')==pins['head']
    assert git('branch','--show-current')==pins['branch']=='coarse-double-branch'
    assert git('status','--porcelain=v1','--untracked-files=no')==''
    assert sha(HERE/'FE00_FOUR_RULE_GATE.md')==pins['gate_sha256']
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    audit=read(HERE/'independent_audit.json');witness=read(HERE/'FE_witness_certificate.json')
    ledger=read(HERE/'proof_status_ledger.json')
    assert audit['status']=='PASS' and audit['geometry']['present_xy_cases']==16731
    assert audit['geometry']['distinct_trees']==99 and audit['fixed_cut_trials']==114
    assert audit['symbolic_double_roles']==28 and audit['symbolic_zig_roles']==10
    for field,name in [('witness_certificate_sha256','FE_witness_certificate.json'),
                       ('geometry_certificate_sha256','source_geometry_certificate.json'),
                       ('symbolic_certificate_sha256','symbolic_rotation_certificate.json'),
                       ('uniform_algebra_sha256','uniform_copy_algebra_certificate.json')]:
        assert audit[field]==sha(HERE/name)
    assert witness['source_only_profile_sha256']==sha(HERE/'source_first_entry.py')
    assert witness['inherited_PG_source_sha256']==sha(PG/'closed_source_certificate.json')
    for orientation in ['ordinary','reflected']:
        for protocol in ['FI','PF']:
            old=witness['all_cut_trials'][orientation][protocol]
            assert len(old)==19 and all(not t['accepted'] and t['final_debt']==1 for t in old)
        new=witness['all_cut_trials'][orientation]['FE']
        assert [t['cut'] for t in new if t['accepted']]==[0]+list(range(3,19))
        assert new[0]['final_debt']==0 and len(new[0]['assignments'])==22
        loans=[a for a in new[0]['assignments'] if a['kind']=='loan']
        assert loans==[dict(demand=[0,0,2],unit=[0,2,0,1],kind='loan')]
        budget=witness['fresh_budgets'][orientation]
        assert (budget['E'],budget['C_D'],budget['L_FE_fresh'],budget['Gamma_FE'],budget['Lambda_FE_fresh'])==(1,0,1,0,28)
    assert ledger['D_FE_universal_one_unit_positive_coverage']=='OPEN / NOT CLAIMED'
    assert ledger['E_universal_Coarse_Double']=='OPEN' and not ledger['Step_3_complete']
    required=[f'FE{i:02d}_' for i in range(8)]
    for start in required:assert any(p.name.startswith(start) and p.suffix=='.md' for p in HERE.iterdir())
    assert not any(p.is_dir() for p in HERE.iterdir()),'no caches or accidental nested outputs'
    save('final_integrity.json',dict(status='PASS',head=pins['head'],branch=pins['branch'],tracked_status='',
        inherited_source_and_prior_files_preserved=len(pins['files']),
        prior_campaign_files_and_inventory_preserved=len(actual),stage_11g_files_and_inventory_preserved=125,
        matching_terminal='FROZEN',original_FI_PF_PG_M1_M2_M3_and_old_statuses='UNCHANGED',
        universal_exact_entry_and_H='PROVED—UNIVERSAL',FE_soundness_and_PF_preservation='PROVED—UNIVERSAL',
        strict_W_F_m_coverage='PROVED—RESTRICTED DOMAIN, all m>=1 and permitted arbitrary fringes',
        PF_proper_subset_FE='PROVED',FE_fresh_budget_corollary='PROVED—UNIVERSAL',
        universal_FE_one_unit_coverage='OPEN / NOT CLAIMED',universal_Coarse_Double='OPEN',Step_3_complete=False,
        independent_checks=audit['total_checks'],physical_geometry_trees=99,present_xy_cases=16731,
        physical_cut_trials=114,FE_designated_cut_complete_demands=22,
        physical_key_count=13,repetition_controls=[1],larger_m_or_n_replays=0,
        larger_finite_fits=0,new_strictness_witnesses=0,automatic_successor_launched=False,
        source_formula_never_uses_observed_post_depth_or_future_q=True))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files,
        sealed_files=len(files),final_integrity_sha256=sha(HERE/'final_integrity.json')))
    print(json.dumps(dict(status='PASS',sealed_files=len(files),inherited_files_preserved=len(pins['files']),
        prior_campaign_files_preserved=len(actual),stage_11g=125,independent_checks=audit['total_checks'],
        universal_exact_H='PROVED',PF_proper_subset_FE='PROVED',all_m_strict_witness='PROVED',
        universal_Coarse_Double='OPEN',head=pins['head']),indent=2))


if __name__=='__main__':main()
