"""Append-only source, Stage 11G and proof-status seal."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('root_completion_certificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'root_completion_certificate.json')
    assert sha(OUT/'CP00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Explicit joint correction R=F(A,S_root(A) B)+Q-P','status':'SOURCE DEFINITION','source':'CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md'},
      {'claim':'Full universal root-conditioned B repayment Delta Phi=-q','status':'PROVED—UNIVERSAL','proof':'CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md'},
      {'claim':'Equal-root reserve R=mu_r, unbounded on prior JA family','status':'PROVED—RESTRICTED DOMAIN','proof':'CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md'},
      {'claim':'Established arbitrary-fringe whole helpers and all opposite-vine starved accesses','status':'PROVED—RESTRICTED DOMAIN','proof':'CP01_EXPLICIT_CORRECTION_AND_UNIVERSAL_B_LAW.md'},
      {'claim':'Universal DELETE law for Phi','status':'REFUTED—EXACT','proof':'CP02_ALL_ODD_DELETE_AND_TERMINAL_CLASS_OBSTRUCTION.md','witness':{'n':7,'a':1,'actual_q':0,'Phi_source':5,'Phi_destination':8,'budget':2}},
      {'claim':'Some scalar terminal f_n(F_completed)+Q satisfies both bounds','status':'REFUTED—EXACT','proof':'CP02_ALL_ODD_DELETE_AND_TERMINAL_CLASS_OBSTRUCTION.md','scope':'arbitrary finite f_n of completed-pair F only'},
      {'claim':'Local P duals, source/completion traces, correction values and physical paired closure','status':'FINITE-EXACT','certificate':'root_completion_certificate.json','audit':'independent_audit.json'},
      {'claim':'Explicit unbounded joint R retaining equal-root reserve and satisfying both universal bounds','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Equal-root-zero nonnegative corrections excluded; retained-reserve joint correction open',
      'result':'Exact universal B completion identity and retained reserve; all-odd-n DELETE refutation',
      'after':'Generic joint correction and CD open; terminal-F-only completion class excluded',
      'original_load_bearing_obligations_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'CP03_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('CP*.md'):
        s=p.read_text(encoding='utf-8');assert '\ufffd' not in s and s.endswith('\n')
        for target in re.findall(r'\]\(([^)]+)\)',s):
            if target.startswith(('http://','https://')):continue
            if target=='final_integrity.json':continue
            assert (OUT/target).resolve().is_file(),(p.name,target)
            links+=1
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'Stage11G_files_checked':len(now),'Stage11G_inventory_and_bytes_unchanged':True,
      'head':head,'branch':branch,'tracked_modifications':tracked,'head_and_branch_preserved':True,
      'prior_artifacts_overwritten':False,'append_only_write_scope':OUT.relative_to(ROOT).as_posix(),
      'independent_dual_completion_and_source_audit':'PASS','all_size_proof_verification':'written idempotence and odd-vine interval proof, not finite extrapolation',
      'written_gate_hash_unchanged':True,'report_links_checked':links,'finite_potential_fits':0,'matching_solver_calls':0,
      'new_pair_graphs':0,'new_metric_graphs':0,'connector':c['connector'],'connector_is_not_a_fit':True,
      'automatic_successor_campaigns':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'CP04_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'CP04_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
