"""Exclusive preservation and exact-source filter delivery seal."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2);f.write('\n')


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():assert sha(ROOT/rel)==h,rel
    prefix=HERE.parent.relative_to(ROOT).as_posix()+'/'
    prior={p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*') if p.is_file() and HERE not in p.parents}
    assert prior=={rel for rel in entry['files'] if rel.startswith(prefix)}
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==entry['stage_files'] and len(stage)==125
    head,branch,status=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert (head,branch,status)==(entry['head'],entry['branch'],entry['tracked_status']) and not status
    assert entry['gate_sha256']==sha(HERE/'RC00_FOUR_RULE_GATE.md')
    audit=read(HERE/'independent_audit.json');summary=read(HERE/'audit_summary.json')
    ledger=read(HERE/'proof_status_ledger.json');theorem=read(HERE/'source_filter_theorem.json')
    assert audit['status']=='PASS' and audit['audited_summary_sha256']==sha(HERE/'audit_summary.json')
    assert audit['analytic_proof_sha256']==sha(HERE/'RC01_CERTIFICATES_AND_STRICT_FILTER_PROOF.md')
    assert summary['gate_sha256']==entry['gate_sha256']
    for name,h in audit['output_hashes'].items():
        assert sha(HERE/name)==h and summary[name+'_sha256']==h
    certs=read(HERE/'FI_rejection_certificates.json')['certificates']
    assert len(certs)==44 and all(c['terminal_debt']>0 for c in certs)
    for c in certs:
        assert c['terminal_debt']==c['positive_excess']-c['certified_offer_sum']==c['source_delta_sum']+c['reserved_loss_sum']
        assert all(v>0 for v in c['relative_busy_prefix_balances'])
        assert not c['reset_history_at_busy_start'] and not c['prefix_units_imported']
        assert not c['whole_cycle_FI_rejection_claimed']
    assert sum(bool(c['paid_source_history_before_busy']) for c in certs)==32
    assert sum(c['reserved_loss_sum']>0 for c in certs)==0
    assert (audit['existing_cuts_checked'],audit['accepted_cuts'],audit['rejected_cuts'])==(636,592,44)
    assert audit['fresh_budget_covered_controls']==14 and audit['controls_with_starved_individual_runs']==[6,7]
    assert audit['positive_Gamma_controls']==[] and not audit['new_all_cut_FI_counterexamples_claimed']
    budget=read(HERE/'fresh_run_budget_certificate.json')['cases']
    assert len(budget)==14 and all(b['Gamma']<0 and b['Gamma']==b['E']-b['C_D']-b['L_fresh'] for b in budget)
    for b in budget:
        assert b['auxiliary_selected_ledger']['accepted'] and b['actual_FI_selected_ledger']['accepted']
        for key in ['auxiliary_selected_ledger','actual_FI_selected_ledger']:
            t=b[key];a=t['assignments']
            assert len(a)==len({tuple(x['unit']) for x in a})==len({tuple(x['demand']) for x in a})
            assert t['startup_units_used']==t['reused_units']==0 and t['periods']==1
    assert budget[12]['E']==5 and budget[12]['C_D']==4 and budget[12]['L_fresh']==5 and budget[12]['Gamma']==-4
    assert ledger['remaining_class_proper_subset_of_E_gt_C_D'].startswith('PROVED')
    assert ledger['positive_Gamma_implies_FI_failure']==theorem['positive_Gamma_implies_FI_failure']=='NOT ESTABLISHED'
    assert ledger['remaining_class_nonemptiness']==theorem['remaining_domain_nonemptiness']=='OPEN'
    assert not ledger['FI_algorithm_class_enlarged'] and not ledger['certificate_identity_alone_counts_as_CD_advancement']
    assert ledger['new_all_cut_FI_rejecting_source_walks_claimed']==0
    assert ledger['new_source_words']==ledger['new_source_engine_calls']==ledger['new_m_values_replayed']==ledger['larger_finite_fits']==0
    assert ledger['startup_or_other_lap_units_used']==ledger['reused_units']==0
    assert ledger['universal_Step3_CD'].startswith('OPEN') and theorem['universal_CD']==audit['universal_CD']=='OPEN'
    assert ledger['mandatory_strategy_review_completed'] and not ledger['automatic_successor_launched']
    freeze=HERE.parent/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    for name in ['RC02_CONTROL_AND_CERTIFICATE_TABLES.md','RC03_BEFORE_RESULT_AFTER.md','RC04_REPRODUCTION_AND_SCOPE.md']:
        assert (HERE/name).is_file()
    save('final_integrity.json',dict(status='PASS',date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']),prior_research_inventory_unchanged=True,
        Stage_11G_files_unchanged=len(stage),Stage_11G_inventory_unchanged=True,
        head=head,branch=branch,tracked_status=status,four_rule_gate='PASS before execution',
        exact_rejection_certificates=44,existing_source_cuts_checked=636,fresh_budget_controls_covered=14,
        independent_checks=sum(audit['checks'].values()),
        constructive_source_coverage='PROVED: Gamma<=0 implies an FI-successful positive-run cut',
        strict_necessary_remaining_domain='E>C_D+L_fresh, proper subset of E>C_D',
        positive_Gamma_sufficiency='NOT ESTABLISHED',new_all_cut_FI_counterexamples_claimed=False,
        new_source_words=0,new_source_engine_calls=0,new_m_values_replayed=0,larger_finite_fits=0,
        source_history_retained=True,no_reused_or_startup_units=True,matching_terminal_line='FROZEN',
        universal_CD='OPEN',automatic_successor_launched=False))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-11-01',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_prior_files=len(entry['files']),preserved_Stage_11G_files=len(stage),
        sealed_artifacts=len(files),exact_rejection_certificates=44,existing_cuts=636,
        independent_checks=sum(audit['checks'].values()),source_coverage='Gamma<=0 implies FI acceptance',
        strict_remaining_class='E>C_D+L_fresh',new_source_words=0,larger_finite_fits=0,universal_CD='OPEN'),indent=2))


if __name__=='__main__':main()
