"""Read-only preservation audit and exclusive delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BASE=HERE.parent


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():assert sha(ROOT/rel)==h,rel
    prefix=BASE.relative_to(ROOT).as_posix()+'/'
    old_inventory={rel for rel in entry['files'] if rel.startswith(prefix)}
    actual_inventory={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual_inventory==old_inventory
    assert len(actual_inventory)==entry['prior_campaign_files']==809
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    stage_now={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert stage_now==entry['stage_files'] and len(stage_now)==125
    assert git('rev-parse','HEAD')==entry['head']=='8c378d49283b3738b18e7175886772a98025e4e9'
    assert git('branch','--show-current')==entry['branch']=='coarse-double-branch'
    assert git('status','--porcelain=v1','--untracked-files=no')==''
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    independent=read(HERE/'independent_audit.json')
    assert independent['status']=='PASS' and independent['total_checks']==17587
    assert independent['closed_source_sha256']==sha(HERE/'closed_source_certificate.json')
    source=read(HERE/'closed_source_certificate.json');ledger=read(HERE/'proof_status_ledger.json')
    assert source['totals']['Gamma_PF']==1 and source['totals']['reserved_loss_fresh']==29
    assert source['totals']['source_delta']==-28
    for orientation in ['ordinary','reflected']:
        for protocol in ['FI','PF']:
            cuts=source['all_cut_audits'][orientation][protocol]
            assert [r['cut'] for r in cuts]==list(range(19))
            assert all(not r['accepted'] and r['final_debt']==1 and r['periods']==1 for r in cuts)
        injection=source['direct_injection'][orientation]
        assert injection['complete'] and injection['paid_demands']==22
        assert injection['startup_units_used']==injection['reused_units']==0
    assert ledger['universal_Coarse_Double']=='OPEN' and not ledger['Step_3_complete']
    assert ledger['general_all_history_one_unit_repay_or_synchronize']=='OPEN'
    assert ledger['unchanged_original_FI_PF_algorithms'] and ledger['matching_terminal']=='FROZEN'
    save('final_integrity.json',dict(status='PASS',head=entry['head'],branch=entry['branch'],tracked_status='',
        inherited_files_preserved=len(entry['files']),prior_campaign_inventory_preserved=len(actual_inventory),
        stage_11g_files_preserved=125,matching_terminal='FROZEN',
        PF_fresh_corollary='PROVED—UNIVERSAL',reservation_loss_decompositions='PROVED—UNIVERSAL',
        first_return_rule='REFUTED—EXACT',unchanged_FI_PF_completeness='REFUTED—EXACT',
        new_positive_Gamma_PF_closed_family=True,fixed_family_direct_injection='PROVED—RESTRICTED DOMAIN',
        independent_checks=17587,one_period_physical_cut_trials=76,
        larger_finite_fits=0,new_key_count_sweeps=0,larger_m_replays=0,
        original_algorithms_and_source_unchanged=True,general_one_unit_theorem='OPEN',
        universal_Coarse_Double='OPEN',strategy_review='COMPLETED',automatic_successor_launched=False,
        v001_sentinel_error_preserved=True,v002_scope_and_selection_unchanged=True))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(schema='raw SHA256; manifest excludes itself',files=files,
        sealed_files=len(files),final_integrity_sha256=sha(HERE/'final_integrity.json')))
    print(json.dumps(dict(status='PASS',sealed_files=len(files),inherited_files_preserved=len(entry['files']),
        prior_campaign_inventory_preserved=len(actual_inventory),stage_11g=125,
        PF_fresh_corollary='PROVED',PF_completeness='REFUTED by reachable closed source family',
        direct_family_source_injection='PROVED',universal_Coarse_Double='OPEN'),indent=2))


if __name__=='__main__':main()
