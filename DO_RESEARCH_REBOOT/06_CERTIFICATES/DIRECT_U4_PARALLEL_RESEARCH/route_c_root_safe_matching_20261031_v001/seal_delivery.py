"""Append-only status and preservation seal for the frozen matching audit."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('root_matching_certificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'root_matching_certificate.json')
    assert sha(OUT/'RS00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Root-conditioned B nonincrease for P','status':'PROVED—UNIVERSAL','proof':'RS01_DEFINITION_AND_TRANSPORT_LAWS.md','qualification':'weak <=0, not full <=-q'},
      {'claim':'A primitive one-Lipschitz bound for P when its root is preserved','status':'PROVED—RESTRICTED DOMAIN','proof':'RS01_DEFINITION_AND_TRANSPORT_LAWS.md'},
      {'claim':'All-size opposite-vine repayment and established arbitrary-fringe whole-helper laws for P','status':'PROVED—RESTRICTED DOMAIN','proof':'RS02_NAMED_REPAYMENT_CLASSES.md'},
      {'claim':'Full universal DELETE bound for P','status':'REFUTED—EXACT','proof':'RS03_UNBOUNDED_DELETE_OBSTRUCTION.md','counterexample':{'n':6,'a':1,'q':0,'P_before':1,'P_after':4,'budget':2}},
      {'claim':'Uniformly bounded additive correction repairs P DELETE on all valid pairs','status':'REFUTED—EXACT','proof':'RS03_UNBOUNDED_DELETE_OBSTRUCTION.md','scope':'all-valid-pair family, fixed size-independent bound'},
      {'claim':'Four frozen starved source consumers, matching duals and closed replay','status':'FINITE-EXACT','certificate':'root_matching_certificate.json','independent_audit':'independent_audit.json'},
      {'claim':'Full universal root-conditioned B q-law for P','status':'OPEN','qualification':'not established or refuted universally in this run'},
      {'claim':'Globally coupled potential satisfying both full source bounds','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Local crossing thresholds refuted; general globally coupled construction open',
      'result':'Global root-eligible matching transport and named laws; unbounded root-changing DELETE refutation',
      'after':'Generic structural potential and CD remain open',
      'original_load_bearing_premises_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'RS04_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('RS*.md'):
        s=p.read_text(encoding='utf-8');assert '\ufffd' not in s and s.endswith('\n')
        for url in re.findall(r'\]\(([^)]+)\)',s):
            if url.startswith(('http://','https://')):continue
            if url=='final_integrity.json':continue
            assert (OUT/url).resolve().is_file(),(p.name,url)
            links+=1
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'Stage11G_files_checked':len(now),'Stage11G_inventory_and_pinned_bytes_unchanged':True,
      'tracked_modifications':tracked,'head':head,'branch':branch,'head_and_branch_preserved':True,
      'prior_artifacts_overwritten':False,'append_only_write_scope':OUT.relative_to(ROOT).as_posix(),
      'independent_matching_dual_and_source_audit':'PASS','written_gate_hash_unchanged':True,'report_links_checked':links,
      'finite_potential_fits':0,'larger_fits':0,'new_pair_state_graphs':0,'connector':c['connector'],
      'automatic_successor_campaigns':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'RS05_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'RS05_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
