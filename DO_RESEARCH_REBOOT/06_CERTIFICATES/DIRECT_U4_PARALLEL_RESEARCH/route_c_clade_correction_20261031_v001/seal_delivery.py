"""Preservation, artifact and status checks; exclusive final records."""
from pathlib import Path
import hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    entry=read('entry_source_pins.json');pins={**entry['files'],**read('additional_source_pins.json')['files']}
    changes=[p for p,h in pins.items() if sha(ROOT/p)!=h]
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert not changes and not tracked and head==entry['head'] and branch==entry['branch']
    assert read('independent_audit.json')['status']==read('sharp_bound_audit.json')['status']=='PASS'
    cert=OUT/'clade_correction_countercertificate.json';digest=sha(cert)
    assert digest==read('independent_audit.json')['certificate_sha256']==read('right_vine_closed_rotation.json')['source_certificate_sha256']
    status=read('proof_status_ledger.json')
    assert not status['original_load_bearing_obligations_discharged'] and status['next_automatic_campaign'] is None
    assert status['candidate_and_scalar_family_refuted'] and status['new_assumptions_for_original_theorem']==[]
    links=0
    for p in OUT.glob('CC*.md'):
        text=p.read_text(encoding='utf-8');assert '\ufffd' not in text and text.endswith('\n')
        for url in re.findall(r'\]\(([^)]+)\)',text):
            if url.startswith(('http://','https://')):continue
            assert (OUT/url).is_file(),(p.name,url)
            links+=1
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    result={'status':'PASS','date':'2026-10-31','pinned_inputs_checked':len(pins),'pinned_inputs_changed':changes,
      'tracked_modifications':tracked,'head':head,'branch':branch,'head_and_branch_preserved':True,
      'Stage11G_writes_performed':False,'Stage11G_frozen_contract_pin_unchanged':True,
      'inherited_compiler_pins_unchanged':True,'old_research_overwritten':False,
      'write_scope':OUT.relative_to(ROOT).as_posix(),'append_only_outputs':True,
      'source_and_sharp_bound_audits':'PASS','local_report_links_checked':links,
      'finite_fits':0,'new_pair_graphs':0,'coefficient_fits':0,
      'original_load_bearing_obligations_discharged':[],'strategy_record':'CC05_STRATEGY_AND_PROOF_STATUS.md'}
    write('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    write('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,
      'exclusion':'delivery_manifest.json excludes its own hash','final_report':'CC06_FINAL_REPORT.md'})
    print(json.dumps({'integrity':'PASS','inherited_pins_unchanged':len(pins),'delivery_files_hashed':len(files),
      'local_links_checked':links,'tracked_tree_clean':not tracked,'final_report':'CC06_FINAL_REPORT.md'},indent=2))

if __name__=='__main__':main()
