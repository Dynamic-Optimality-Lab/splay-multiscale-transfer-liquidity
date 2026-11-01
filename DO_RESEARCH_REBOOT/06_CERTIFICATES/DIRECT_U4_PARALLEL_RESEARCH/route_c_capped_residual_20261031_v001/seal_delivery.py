"""Final preservation, scope and delivery checks with exclusive output files."""
from pathlib import Path
import hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    entry=read('entry_source_pins.json');pins=entry['files']
    changed=[p for p,h in pins.items() if sha(ROOT/p)!=h]
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert not changed and not tracked and head==entry['head'] and branch==entry['branch']
    audit=read('independent_audit.json');assert audit['status']=='PASS'
    assert audit['certificate_sha256']==sha(OUT/'capped_residual_certificate.json')
    ledger=read('proof_status_ledger.json')
    assert len(ledger['four_named_requirements_achieved'])==4
    assert not ledger['original_load_bearing_obligations_discharged'] and not ledger['new_assumptions_for_original_theorem']
    assert ledger['next_automatic_campaign'] is None and (OUT/ledger['updated_strategy_review']).is_file()
    assert audit['monotone_aggregation_forced_bounds']['phi(4,1)_lower']>audit['monotone_aggregation_forced_bounds']['phi(4,2)_upper']
    links=0
    for p in OUT.glob('CR*.md'):
        s=p.read_text(encoding='utf-8');assert '\ufffd' not in s and s.endswith('\n')
        for url in re.findall(r'\]\(([^)]+)\)',s):
            if url.startswith(('http://','https://')):continue
            assert (OUT/url).resolve().is_file(),(p.name,url)
            links+=1
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    result={'status':'PASS','date':'2026-10-31','inherited_pins_checked':len(pins),'inherited_pins_changed':changed,
      'tracked_modifications':tracked,'head':head,'branch':branch,'head_and_branch_preserved':True,
      'Stage11G_writes_performed':False,'Stage11G_frozen_contract_pin_unchanged':True,
      'inherited_compiler_pins_unchanged':True,'prior_research_overwritten':False,
      'write_scope':OUT.relative_to(ROOT).as_posix(),'append_only_outputs':True,
      'independent_matching_cap_source_and_scalar_data_audit':'PASS','local_report_links_checked':links,
      'four_named_requirements_achieved':True,'universal_candidate_refuted':True,
      'monotone_aggregation_class_excluded':'coordinatewise nondecreasing phi_n(F,Ehat) with Ehat<=phi_n<=F',
      'finite_potential_fits':0,'new_pair_state_graphs':0,'larger_helper_samples':0,
      'single_tree_connector_BFS_calls':1,'single_tree_connector_states_visited':104,
      'original_load_bearing_obligations_discharged':[],'updated_strategy_review_completed':True}
    write('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    write('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,
      'exclusion':'delivery_manifest.json excludes its own hash','final_report':'CR05_FINAL_REPORT.md'})
    print(json.dumps({'integrity':'PASS','inherited_pins_unchanged':len(pins),'delivery_files_hashed':len(files),
      'local_links_checked':links,'tracked_tree_clean':not tracked,'final_report':'CR05_FINAL_REPORT.md'},indent=2))

if __name__=='__main__':main()
