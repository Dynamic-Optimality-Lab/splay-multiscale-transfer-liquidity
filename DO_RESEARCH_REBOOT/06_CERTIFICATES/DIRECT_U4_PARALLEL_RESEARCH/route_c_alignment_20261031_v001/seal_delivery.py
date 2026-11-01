"""Final read-only preservation checks and exclusive delivery records."""
from pathlib import Path
from fractions import Fraction
import hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(name,x):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(x,f,indent=2)
def main():
    original=read('entry_source_pins.json');pins={**original['files'],**read('additional_source_pins.json')['files']}
    changed=[p for p,h in pins.items() if sha(ROOT/p)!=h]
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert not changed and not tracked and head==original['head'] and branch==original['branch']
    assert read('independent_audit.json')['status']=='PASS'
    ledger=read('proof_status_ledger.json')
    assert not ledger['genuinely_deleted_original_obligations'] and ledger['net_original_proof_advancement']==0
    assert ledger['strategy_review_completed']=='AL05_STRATEGY_REVIEW.md' and ledger['next_automatic_campaign'] is None
    assert Fraction(2*13-11,7)>2 and Fraction(2*13-13,2*13-4)>Fraction(4,7)
    local_links=0
    for p in OUT.glob('AL*.md'):
        text=p.read_text(encoding='utf-8')
        assert '\ufffd' not in text and text.endswith('\n')
        for url in re.findall(r'\]\(([^)]+)\)',text):
            if url.startswith(('https://','http://')):continue
            assert (OUT/url).is_file(),(p.name,url)
            local_links+=1
    old_audit=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_potential_20261031_v001/independent_audit.json'
    assert sha(old_audit)==pins[old_audit.relative_to(ROOT).as_posix()]
    result={'status':'PASS','date':'2026-10-31','pinned_inputs_checked':len(pins),'pinned_inputs_changed':changed,
       'tracked_modifications':tracked,'head':head,'branch':branch,'head_and_branch_preserved':True,
       'Stage11G_writes_performed':False,'Stage11G_frozen_contract_pin_unchanged':True,
       'inherited_compiler_pins_unchanged':True,'old_certificates_overwritten':False,
       'write_scope':OUT.relative_to(ROOT).as_posix(),'append_only_outputs':True,
       'independent_exact_audit':'PASS','report_local_links_checked':local_links,
       'larger_finite_fits':0,'new_pair_graphs':0,'coefficient_fits':0,
       'original_obligations_discharged':[],'strategy_review_completed':True}
    write('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    write('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,
       'exclusion':'delivery_manifest.json excludes its own hash','final_report':'AL06_FINAL_REPORT.md'})
    print(json.dumps({'integrity':result['status'],'pinned_inputs_unchanged':len(pins),'delivery_files_hashed':len(files),
       'local_report_links_checked':local_links,'tracked_tree_clean':not tracked,'final_report':'AL06_FINAL_REPORT.md'},indent=2))

if __name__=='__main__':main()
