"""Append-only status and preservation seal; retain the OPEN disposition."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('antichain_terminal_certificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'antichain_terminal_certificate.json')
    assert c['disposition']=='OPEN' and c['first_failure'] is None and not a['universal_DELETE_proved']
    assert sha(OUT/'AT00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Explicit terminal K=F-alpha, with residual right antichain matching','status':'SOURCE DEFINITION','source':'AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md'},
      {'claim':'Fixed-C primitive A one-Lipschitz law for K','status':'PROVED—UNIVERSAL','proof':'AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md'},
      {'claim':'Full universal root-conditioned B repayment Delta Phi=-q','status':'PROVED—UNIVERSAL','proof':'AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md'},
      {'claim':'Unbounded equal-root reserve and both known all-size DELETE-family repairs','status':'PROVED—RESTRICTED DOMAIN','proof':'AT02_ALL_SIZE_REPAIRS_AND_OPEN_ROOT_STEPS.md'},
      {'claim':'Full DELETE follows if all depth-one/two root steps have increment<=2','status':'CONDITIONAL','open_premise':'root-step condition (R)','proof':'AT02_ALL_SIZE_REPAIRS_AND_OPEN_ROOT_STEPS.md'},
      {'claim':'Universal root-step condition (R)','status':'OPEN'},
      {'claim':'Universal DELETE for this completed Phi','status':'OPEN','qualification':'not inferred from frozen finite survival'},
      {'claim':'Arbitrary-fringe whole-helper safety for this new terminal K','status':'OPEN','qualification':'only m=0 helper controls checked; old F/Ehat proofs not transferred'},
      {'claim':'Six frozen controls, reflections, full closed word and optimal antichain evaluations','status':'FINITE-EXACT','certificate':'antichain_terminal_certificate.json','audit':'independent_audit.json'},
      {'claim':'Both universal bounds for this explicit correction','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Scalar terminal F refuted, joint terminal correction open',
      'result':'Antichain terminal function repairs old families, proves terminal stability and B; frozen audit survives',
      'after':'Explicit unrefuted candidate; universal DELETE reduced to root steps but unproved',
      'original_load_bearing_obligations_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'AT03_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('AT*.md'):
        s=p.read_text(encoding='utf-8');assert '\ufffd' not in s and s.endswith('\n')
        for target in re.findall(r'\]\(([^)]+)\)',s):
            if target.startswith(('http://','https://')):continue
            if target=='final_integrity.json':continue
            assert (OUT/target).resolve().is_file(),(p.name,target)
            links+=1
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'Stage11G_files_checked':len(now),'Stage11G_inventory_and_bytes_unchanged':True,'head':head,'branch':branch,
      'tracked_modifications':tracked,'head_and_branch_preserved':True,'prior_artifacts_overwritten':False,
      'append_only_write_scope':OUT.relative_to(ROOT).as_posix(),'independent_antichain_dual_and_source_audit':'PASS',
      'candidate_disposition':'OPEN','universal_DELETE_proved':False,'finite_survival_not_promoted':True,
      'written_gate_hash_unchanged':True,'report_links_checked':links,'finite_potential_fits':0,'new_BFS_calls':0,
      'new_pair_graphs':0,'new_metric_graphs':0,'coefficient_searches':0,'automatic_successor_campaigns':0,
      'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'AT04_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'candidate_disposition':'OPEN','report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'AT04_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
