"""Seal the exact refutation without changing any historical artifact."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json');c=read('root_bound_countercertificate.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'root_bound_countercertificate.json')
    assert a['universal_root_zig_double_bound']=='REFUTED—EXACT' and c['candidate_modified'] is False
    assert sha(OUT/'RB00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Universal A-root zig/double bound2 for the fixed completed AT potential','status':'REFUTED—EXACT','proof':'RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md','witness':{'n':7,'dA':1,'a':1,'actual_q':0,'Phi_before':4,'Phi_after':7,'increment':3,'bound':2}},
      {'claim':'Universal DELETE for the unchanged completed antichain candidate','status':'REFUTED—EXACT','proof':'RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md'},
      {'claim':'Unbounded root-zig drift (n-1)/2 on all odd n>=7','status':'PROVED—RESTRICTED DOMAIN','proof':'RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md'},
      {'claim':'Scalar f_n(K_completed)+Q repairs this root-step failure','status':'REFUTED—EXACT','proof':'RB01_ALL_ODD_ROOT_ZIG_REFUTATION.md','scope':'same completion and terminal K; not all terminal functions'},
      {'claim':'Fixed-C terminal A stability and full universal B repayment','status':'PROVED—UNIVERSAL','qualification':'inherited valid component theorems; not refuted by a change of completed C','proof':'../route_c_antichain_terminal_20261031_v001/AT01_TERMINAL_DEFINITION_AND_PROVED_LAWS.md'},
      {'claim':'Both zig orientations, exact packing optima and actual closed replay','status':'FINITE-EXACT','certificate':'root_bound_countercertificate.json','audit':'independent_audit.json'},
      {'claim':'Separate classification of root-double-only cases','status':'OPEN','qualification':'not attempted after zig refuted the universal conjunction'},
      {'claim':'General explicit joint correction satisfying both universal bounds','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'AT candidate survived frozen audit; root-step bound and universal DELETE open',
      'result':'Exact all-odd root-zig counterfamily and reachable n7 certificate',
      'after':'Fixed candidate and universal root-step bound refuted; generic Step3/CD open',
      'requested_local_objective':'completed by exact refutation','original_load_bearing_obligations_discharged':[],
      'new_assumptions_for_original_theorem':[],'net_full_original_proof_advancement':0,
      'strategy_review':'RB03_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('RB*.md'):
        s=p.read_text(encoding='utf-8');assert '\ufffd' not in s and s.endswith('\n')
        for target in re.findall(r'\]\(([^)]+)\)',s):
            if target.startswith(('http://','https://')):continue
            if target=='final_integrity.json':continue
            assert (OUT/target).resolve().is_file(),(p.name,target)
            links+=1
    result={'status':'PASS','date':'2026-10-31','source_pins_checked':len(e['files']),'changed_pins':changed,
      'Stage11G_files_checked':len(now),'Stage11G_inventory_and_bytes_unchanged':True,'head':head,'branch':branch,
      'tracked_modifications':tracked,'head_and_branch_preserved':True,'prior_artifacts_overwritten':False,
      'append_only_write_scope':OUT.relative_to(ROOT).as_posix(),'unchanged_candidate_and_evaluator_pins_verified':True,
      'independent_antichain_dual_source_and_completion_audit':'PASS','root_bound_verdict':'REFUTED—EXACT',
      'all_size_proof':'written odd-parity interval/antichain argument, not finite extrapolation',
      'written_gate_hash_unchanged':True,'report_links_checked':links,'finite_potential_fits':0,
      'new_pair_graphs':0,'new_metric_graphs':0,'connector':c['connector'],'connector_is_not_a_fit':True,
      'automatic_successor_campaigns':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'RB04_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'root_bound':'REFUTED—EXACT','report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'RB04_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
