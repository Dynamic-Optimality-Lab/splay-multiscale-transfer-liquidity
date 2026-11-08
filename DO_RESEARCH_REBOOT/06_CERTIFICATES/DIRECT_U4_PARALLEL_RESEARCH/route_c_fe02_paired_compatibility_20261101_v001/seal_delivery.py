"""Exclusive integrity seal for the FE02 paired continuation, with open scope."""
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
    prior={rel for rel in entry['files'] if rel.startswith(prefix)}
    actual={p.relative_to(ROOT).as_posix() for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents}
    assert actual==prior and len(actual)==entry['prior_campaign_files']
    for dirname in ['route_c_pf_positive_gap_closure_20261101_v001','route_c_fe01_first_entry_20261101_v001',
                    'route_c_fe02_saturated_return_20261101_v001']:
        folder=BASE/dirname
        for name,h in read(folder/'delivery_manifest.json')['files'].items():assert sha(folder/name)==h,(dirname,name)
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    current_stage={p.relative_to(stage).as_posix():sha(p) for p in stage.rglob('*') if p.is_file()}
    assert current_stage==entry['stage_files'] and len(current_stage)==125
    assert git('rev-parse','HEAD')==entry['head']
    assert git('branch','--show-current')==entry['branch']=='coarse-double-branch'
    assert git('status','--porcelain=v1','--untracked-files=no')==''
    assert sha(HERE/'PC00_FOUR_RULE_GATE.md')==entry['gate_sha256']
    freeze=BASE/'route_c_full_form_obstruction_audit_20261031_v001/FF01_MATCHING_TERMINAL_FREEZE.md'
    assert 'FROZEN BY EXPLICIT USER INSTRUCTION' in freeze.read_text(encoding='utf-8')
    audit=read(HERE/'independent_audit.json');ledger=read(HERE/'proof_status_ledger.json')
    assert audit['status']=='PASS' and audit['far_side_contexts']==4836
    assert audit['existing_geometry_trees']==99 and audit['existing_geometry_key_count']==13
    for name,h in audit['witness_hashes'].items():assert sha(HERE/name)==h,name
    deep=read(HERE/'walk_deep_certificate.json')['data']
    for orientation in ['ordinary','reflected']:
        r=deep[orientation]['returns'][4]
        assert r['retreat_only'] and (r['A_return_depth'],r['B_return_depth'])==(2,3)
        assert not deep[orientation]['returns'][0]['retreat_only']
    counter=read(HERE/'discordance_obstruction_certificate.json')
    assert counter['A_DELETE_connector']==[5,3,5,1]
    assert counter['symbolic_D_before']==dict(constant=3,coefficient_of_fringe_size=0)
    assert counter['symbolic_D_after']==dict(constant=4,coefficient_of_fringe_size=2)
    assert counter['reachability_refinement_sha256']==sha(HERE/'PC00B_REACHABILITY_REFINEMENT_GATE.md')
    assert counter['actual_Coarse_Double_margin']<0 and counter['no_Coarse_Double_counterexample_claimed']
    assert ledger['FE02_RIGIDITY']==ledger['FE02_CD']==ledger['Universal_Coarse_Double']=='OPEN'
    assert not ledger['Step_3_complete'] and not ledger['new_FE02_counterexample_claimed']
    for p in HERE.glob('*.py'):compile(p.read_text(encoding='utf-8'),str(p),'exec')
    # V003 is a transparent first-output extension of the retained V002 resume.
    wrapper=(HERE/'build_paired_certificates_v002.py').read_text(encoding='utf-8')
    assert wrapper.count("if name=='walk_deep_certificate.json':")==1
    compile(wrapper.replace("if name=='walk_deep_certificate.json':", "if name=='walk_deep_certificate.json' and (HERE/name).exists():"),
            str(HERE/'build_paired_certificates_v003.py'),'exec')
    assert not any(p.is_dir() for p in HERE.iterdir()),'no accidental caches/nested outputs'
    save('final_integrity.json',dict(status='PASS',head=entry['head'],branch=entry['branch'],tracked_status='',
        inherited_files_preserved=len(entry['files']),prior_campaign_inventory_preserved=len(actual),
        old_FE01_PG02_FE02_manifests='UNCHANGED',Stage11G_files_and_inventory_preserved=125,
        matching_terminal='FROZEN',all_original_sources_and_prior_statuses='UNCHANGED',
        paired_far_side_and_ordered_retreat_theorems='PROVED—UNIVERSAL at stated source scope',
        equality_separators_and_approach_transfer_necessity='PROVED—UNIVERSAL',
        all_reachable_saturated_edge_discordance_monotonicity='REFUTED—EXACT',
        counter_scope='specified transition law only; no FE02/CD counterexample',
        FE02_RIGIDITY='OPEN',FE02_CD='OPEN',Universal_Coarse_Double='OPEN',Step_3_complete=False,
        independent_checks=audit['total_checks'],far_side_contexts=4836,existing_geometry_key_count=13,
        explicit_counter_key_count=5,qualitative_control_key_count=4,
        fixed_source_connector=[5,3,5,1],paired_graph_used=False,
        larger_finite_fits=0,larger_repetition_replays=0,automatic_FE03_launched=False,
        campaign_continuity='FE02 objective retained with refined approaching-transfer obstruction'))
    files={p.name:sha(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',dict(schema='raw SHA256; excludes this manifest',files=files,
        sealed_files=len(files),final_integrity_sha256=sha(HERE/'final_integrity.json')))
    print(json.dumps(dict(status='PASS',sealed_files=len(files),inherited_files_preserved=len(entry['files']),
        prior_campaign_inventory_preserved=len(actual),Stage11G=125,checks=audit['total_checks'],
        paired_compatibility_sublemma='PROVED',D_transition_bridge='REFUTED',FE02_CD='OPEN'),indent=2))


if __name__=='__main__':main()
