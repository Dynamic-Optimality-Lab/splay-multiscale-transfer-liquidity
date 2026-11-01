"""Seal this bounded run without modifying prior artifacts or Git."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name):return json.loads((OUT/name).read_text(encoding='utf-8'))
def save(name,v):
    with (OUT/name).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('crossing_certificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'crossing_certificate.json')
    assert sha(OUT/'CT00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert now==sorted(e['stage11g_all_files']) and not changed
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31',
      'results':[
        {'claim':'Hk DELETE bound for every fixed positive k and every finite same-key pair','status':'PROVED—UNIVERSAL','proof':'CT01_STRUCTURAL_DEFINITION_AND_DELETE.md'},
        {'claim':'H2 full root-conditioned B law','status':'REFUTED—EXACT','proof':'CT02_EXACT_REPAYMENT_OBSTRUCTION.md','witness':{'n':4,'a':0,'q':1,'z':1,'H2_change':0,'required_upper':-1}},
        {'claim':'Every fixed positive integer crossing threshold fails as a universal source potential','status':'REFUTED—EXACT','proof':'CT02_EXACT_REPAYMENT_OBSTRUCTION.md','scope':'fixed k independent of n; excludes no size-dependent or weighted profile'},
        {'claim':'Finite source incidences, reflected controls and physical closed replay','status':'FINITE-EXACT','certificate':'crossing_certificate.json','independent_audit':'independent_audit.json'},
        {'claim':'Existence of a structural potential satisfying both universal source bounds','status':'OPEN'},
        {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Capped residual candidate refuted; monotone bracket class excluded; general potential open',
      'result':'Crossing-threshold A law proved; B law and fixed threshold class refuted',
      'after':'General structural potential and CD remain open',
      'original_load_bearing_obligations_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'CT03_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('CT*.md'):
        text=p.read_text(encoding='utf-8');assert '\ufffd' not in text and text.endswith('\n')
        for target in re.findall(r'\]\(([^)]+)\)',text):
            if target.startswith(('http://','https://')):continue
            # final_integrity is this seal's prospective output.
            if target=='final_integrity.json':continue
            assert (OUT/target).resolve().is_file(),(p.name,target)
            links+=1
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'stage11g_files_checked':len(now),'stage11g_file_inventory_unchanged':True,'stage11g_all_pinned_bytes_unchanged':True,
      'head':head,'branch':branch,'tracked_modifications':tracked,'head_and_branch_preserved':True,
      'old_reports_and_certificates_overwritten':False,'write_scope':OUT.relative_to(ROOT).as_posix(),
      'independent_source_and_chord_audit':'PASS','written_gate_preserved':True,'report_links_checked':links,
      'finite_potential_fits':0,'larger_fits':0,'new_pair_state_graphs':0,
      'single_tree_connector':c['connector'],'new_threshold_candidates_after_failure':0,
      'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,
      'exclusion':'self hash excluded','final_report':'CT04_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'report_links_verified':links,'delivery_files_hashed':len(files),'final_report':'CT04_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
