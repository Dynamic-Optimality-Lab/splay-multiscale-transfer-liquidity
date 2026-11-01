"""Exclusive seal of the fixed failed return attack and source lemmas."""
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
    assert entry['gate_sha256']==sha(HERE/'PF00_FOUR_RULE_GATE.md')
    ret=read(HERE/'fixed_return_certificate.json');bd=read(HERE/'failure_boundary_certificate.json')
    spans=read(HERE/'directed_span_certificates.json');audit=read(HERE/'independent_audit.json')
    ledger=read(HERE/'proof_status_ledger.json');theorem=read(HERE/'source_bound_theorem.json')
    assert audit['status']=='PASS'
    for key,name in [('fixed_return_sha256','fixed_return_certificate.json'),
                     ('failure_boundary_sha256','failure_boundary_certificate.json'),
                     ('directed_span_sha256','directed_span_certificates.json'),
                     ('analytic_proof_sha256','PF01_SOURCE_ATTACK_AND_RESULT.md')]:
        assert audit[key]==sha(HERE/name)
    assert bd['completion_scope_sha256']==sha(HERE/'PF00A_FAILURE_BOUNDARY_SCOPE.md')
    assert ret['reachable_nodes_count']==1 and ret['allowed_reachable_edges']==0
    assert ret['paths']==dict(anchor_return=None,reset_return=None)
    assert ledger['fixed_return_mechanism']=='REFUTED—EXACT'
    assert ledger['strict_closed_walk_FI_subset_PF']==theorem['strict_closed_walk_PF_extension_of_FI']=='NOT ESTABLISHED'
    assert not ledger['new_closed_positive_Gamma_witness'] and not spans['positive_Gamma_closed_walk_claimed']
    assert not spans['closed_walk_counterexample_claimed']
    assert len(bd['core_successors'])==6
    assert [r['key'] for r in bd['core_successors'] if r['old_offer']==0]==[3]
    assert next(r for r in bd['core_successors'] if r['key']==3)['target_pair']==[176,176]
    assert bd['fringe_depth_formulas']['minimum_offer']==3
    for parity in ['even_f','odd_f']:assert bd['fringe_depth_formulas'][parity]['offer']==[3,1]
    triple=spans['examples']['three_block']['normal'];quad=spans['examples']['synchronizing_four_block']['normal']
    assert triple['FI']['final_debt']==1 and triple['PF']['final_debt']==0
    claims=triple['PF']['assignments']
    assert len(claims)==len({tuple(x['unit']) for x in claims})==len({tuple(x['demand']) for x in claims})==6
    assert sum(r['a'] for r in triple['rows'])==3 and sum(r['q'] for r in triple['rows'])==6
    assert (quad['FI']['source_delta_sum'],quad['FI']['reserved_loss_sum'],quad['FI']['final_debt'])==(-1,2,1)
    assert quad['rows'][-1]['destination_A']==quad['rows'][-1]['destination_B']
    assert ledger['new_source_engine_calls']==ledger['new_active_key_sizes']==ledger['new_m_values_replayed']==ledger['larger_finite_fits']==0
    assert ledger['new_closed_source_words']==0 and ledger['new_directed_source_spans']==2
    assert not ledger['alternative_search_after_failure'] and not ledger['automatic_successor_launched']
    assert ledger['mandatory_strategy_review_completed']
    assert ledger['general_positive_Gamma_source_class']==ledger['universal_Step3_CD']==audit['universal_CD']==theorem['universal_CD']=='OPEN'
    assert ledger['matching_terminal_line']==theorem['matching_terminal_line']=='FROZEN'
    freeze=HERE.parent/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    for name in ['PF02_BEFORE_RESULT_AFTER.md','PF03_REPRODUCTION_AND_SCOPE.md','independent_verify_v002.py']:
        assert (HERE/name).is_file()
    save('final_integrity.json',dict(status='PASS',date='2026-11-01',
        inherited_source_and_prior_files_unchanged=len(entry['files']),prior_research_inventory_unchanged=True,
        Stage_11G_files_unchanged=len(stage),Stage_11G_inventory_unchanged=True,
        head=head,branch=branch,tracked_status=status,four_rule_gate='PASS before execution',
        independent_checks=sum(audit['checks'].values()),
        fixed_return_mechanism='REFUTED—EXACT',local_parent_outer_fringe_bound='PROVED—UNIVERSAL source identity',
        earlier_open_span_repayment='PROVED—RESTRICTED DOMAIN',
        source_run_exclusion='specified6,4,1 source prefix cannot have positive fresh run gap on a closed continuation',
        strict_new_closed_walk_PF_coverage='NOT ESTABLISHED',new_closed_positive_Gamma_witness=False,
        new_source_engine_calls=0,new_active_key_sizes=0,larger_finite_fits=0,
        matching_terminal_line='FROZEN',general_positive_Gamma_class='OPEN',universal_CD='OPEN',
        automatic_successor_launched=False))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(date='2026-11-01',files=files,manifest_excludes_itself=True))
    print(json.dumps(dict(status='PASS',preserved_prior_files=len(entry['files']),preserved_Stage_11G_files=len(stage),
        sealed_artifacts=len(files),independent_checks=sum(audit['checks'].values()),
        fixed_return='REFUTED—EXACT',local_source_bound='PROVED',source_run_pattern='excluded from positive gap',
        new_closed_Gamma_positive_witness=False,universal_CD='OPEN'),indent=2))


if __name__=='__main__':main()
