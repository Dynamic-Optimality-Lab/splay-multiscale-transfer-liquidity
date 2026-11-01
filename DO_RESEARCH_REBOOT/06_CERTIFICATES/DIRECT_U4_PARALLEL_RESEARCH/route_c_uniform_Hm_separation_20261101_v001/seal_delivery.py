"""Exclusive seal of the analytic all-m source-family separation proof."""
import hashlib
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STAGE=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(name,value):
    with (HERE/name).open('x',encoding='utf-8') as f:
        json.dump(value,f,ensure_ascii=False,indent=2)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()


def main():
    entry=read(HERE/'entry_source_pins.json')
    for rel,h in entry['files'].items():
        assert sha(ROOT/rel)==h,rel
    prefix=HERE.parent.relative_to(ROOT).as_posix()+'/'
    old_inventory={p.relative_to(ROOT).as_posix() for p in HERE.parent.rglob('*')
        if p.is_file() and HERE not in p.parents}
    assert old_inventory=={rel for rel in entry['files'] if rel.startswith(prefix)}
    stage={p.relative_to(STAGE).as_posix():sha(p) for p in STAGE.rglob('*') if p.is_file()}
    assert stage==entry['stage_files'] and len(stage)==125
    head,branch,status=git('rev-parse','HEAD'),git('branch','--show-current'),git('status','--porcelain=v1','--untracked-files=no')
    assert (head,branch,status)==(entry['head'],entry['branch'],entry['tracked_status']) and not status
    assert entry['gate_sha256']==sha(HERE/'UH00_FOUR_RULE_GATE.md')
    kernel=read(HERE/'fixed_source_kernel.json')
    proof=read(HERE/'uniform_proof_certificate.json')
    audit=read(HERE/'independent_audit.json')
    ledger=read(HERE/'proof_status_ledger.json')
    assert audit['status']=='PASS'
    assert audit['source_kernel_sha256']==proof['source_kernel_sha256']==sha(HERE/'fixed_source_kernel.json')
    assert audit['proof_certificate_sha256']==sha(HERE/'uniform_proof_certificate.json')
    assert audit['analytic_proof_sha256']==sha(HERE/'UH01_UNIFORM_SEPARATION_PROOF.md')
    assert kernel['gate_sha256']==entry['gate_sha256']
    assert proof['maximum_A_depth']==6 and proof['maximum_KEEP_capacity']==6
    assert proof['phase_B_changes']==dict(P=6,W=17,X=9)
    assert proof['successive_anchor_B_change_gaps']==dict(internal_repeat=17,wrap_through_X_P=32)
    for orientation in ['normal','reflected']:
        cases=proof['short_lag_UD_cases'][orientation]
        assert len(cases)==7 and [r['k'] for r in cases]==list(range(7))
        assert all(r['UD_ceiling']>=r['capacity'] for r in cases)
        fp=proof['FI_source_frame'][orientation]
        assert (fp['h'],fp['mu'],fp['outer_doubles'],fp['matching_outer_doubles'],fp['U'])==(3,0,1,0,2)
    assert proof['UD_accepted_cuts']==ledger['uniform_UD_accepted_cuts']==0
    assert proof['UD_final_debt_lower_bound']==ledger['uniform_UD_final_debt_lower_bound']=='m-4'
    assert proof['FI_accepted_count']==ledger['uniform_FI_accepted_count']=='17+15m'
    assert proof['FI_rejected_count']==ledger['uniform_FI_rejected_count']=='2m'
    assert proof['FI_local_debt_recurrence']==[0,1,1,0]
    assert proof['symbolic_residual_demand']=='(0,i_r,2)' and proof['symbolic_donor_unit']=='(0,i_r+2,0,1)'
    assert proof['FI_DELETE_or_startup_units_used']==proof['reused_units']==0
    assert proof['new_m_values_replayed']==kernel['new_m_values_replayed']==audit['new_m_values_replayed']==ledger['new_m_values_constructed_or_replayed']==0
    assert proof['new_source_engine_calls']==ledger['new_source_engine_calls']==ledger['new_protocol_cut_trials']==ledger['larger_finite_fits']==0
    assert ledger['periods_per_cut']==1 and ledger['recurrent_one_StepEv_resets']==2
    assert ledger['source_reachable'] and ledger['nowhere_diagonal'] and ledger['non_simple_closed_walks']
    assert ledger['mandatory_strategy_review_completed'] and not ledger['automatic_successor_launched']
    assert ledger['universal_Step3_CD']==proof['universal_CD']==audit['universal_CD']=='OPEN'
    assert ledger['matching_terminal_line']==proof['matching_terminal_line']=='FROZEN'
    freeze=HERE.parent/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    for name in ['UH02_BEFORE_RESULT_AFTER.md','UH03_SOURCE_AND_REPRODUCTION.md','UH04_INHERITED_PROTOCOL_PREMISES.md']:
        assert (HERE/name).is_file()
    save('final_integrity.json',dict(status='PASS',date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']),prior_research_inventory_unchanged=True,
        Stage_11G_files_unchanged=len(stage),Stage_11G_inventory_unchanged=True,
        head=head,branch=branch,tracked_status=status,four_rule_gate='PASS before execution',
        uniform_theorem='PROVED—RESTRICTED DOMAIN: every m>=5, arbitrary untouched fringe, reflection',
        UD_accepted_cuts=0,UD_final_debt_lower_bound='m-4',FI_accepted_count='17+15m',FI_rejected_count='2m',
        proof_type='source identities, exhaustive lag split and chronological triple induction',
        independent_source_premise_checks=sum(audit['checks'].values()),new_m_values_replayed=0,
        new_protocol_trials=0,new_source_engine_calls=0,larger_finite_fits=0,
        startup_or_other_lap_units_used=0,reused_units=0,matching_terminal_line='FROZEN',
        universal_CD='OPEN',automatic_successor_launched=False))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-11-01',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_prior_files=len(entry['files']),preserved_Stage_11G_files=len(stage),
        sealed_artifacts=len(files),uniform_for='all integer m>=5',UD_accepted=0,FI_accepted='17+15m',
        FI_rejected='2m',UD_debt_lower_bound='m-4',new_m_values_replayed=0,larger_finite_fits=0,
        independent_checks=sum(audit['checks'].values()),universal_CD='OPEN'),indent=2))


if __name__=='__main__':
    main()
