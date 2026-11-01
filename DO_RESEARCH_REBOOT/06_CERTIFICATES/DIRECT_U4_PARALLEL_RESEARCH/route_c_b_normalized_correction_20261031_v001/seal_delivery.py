"""Append-only preservation and status seal for the normalized correction."""
from pathlib import Path
import hashlib,json,re,subprocess
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((OUT/n).read_text(encoding='utf-8'))
def save(n,v):
    with (OUT/n).open('x',encoding='utf-8') as f:json.dump(v,f,indent=2)
def main():
    e=read('entry_source_pins.json');a=read('independent_audit.json')
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'b_normalization_certificate.json')
    assert sha(OUT/'BN00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Explicit Phi=J-M(B), R=Phi-P with finite present-state maxima','status':'SOURCE DEFINITION','source':'BN01_EXPLICIT_CORRECTION_AND_REPAIRS.md'},
      {'claim':'Universal DELETE bound for Phi','status':'PROVED—UNIVERSAL','proof':'BN01_EXPLICIT_CORRECTION_AND_REPAIRS.md'},
      {'claim':'Unbounded R and repairs of registered DELETE and zero-double B families','status':'PROVED—RESTRICTED DOMAIN','scope':'explicit family for all n>=4','proof':'BN01_EXPLICIT_CORRECTION_AND_REPAIRS.md'},
      {'claim':'M(B)<=n-2 when both extreme keys are B leaves','status':'PROVED—RESTRICTED DOMAIN','proof':'BN02_STARVED_HELPER_AND_GAUGE_OBSTRUCTION.md'},
      {'claim':'Full universal B repayment for Phi','status':'REFUTED—EXACT','proof':'BN02_STARVED_HELPER_AND_GAUGE_OBSTRUCTION.md','witness':{'n':6,'a':0,'q':2,'z':0,'Phi_source':-1,'Phi_destination_lower':-2,'required_destination_upper':-3}},
      {'claim':'A scalar c_n in J-c_n M(B) satisfies both full bounds','status':'REFUTED—EXACT','proof':'BN02_STARVED_HELPER_AND_GAUGE_OBSTRUCTION.md','same_n6_necessary_bounds':{'old_B_edge':'c6>=1','helper_B_edge':'c6<=0'}},
      {'claim':'Fourteen local P duals, six controls and twelve-step physical closure','status':'FINITE-EXACT','certificate':'b_normalization_certificate.json','audit':'independent_audit.json'},
      {'claim':'A general unbounded correction to P satisfying both universal laws','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Scalar metric envelopes of P refuted; a general two-law correction open',
      'result':'Explicit B-dependent correction with universal DELETE and old repairs; positive-q helper refutation',
      'after':'Scalar M-normalization family excluded; generic Step 3 and CD open',
      'original_load_bearing_obligations_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'BN04_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('BN*.md'):
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
      'independent_local_dual_bound_and_source_audit':'PASS','global_upper_bound_verification':'written extremal-leaf proof, not finite exhaustion',
      'written_gate_hash_unchanged':True,'report_links_checked':links,'finite_potential_fits':0,
      'new_pair_graphs':0,'new_metric_graphs':0,'new_BFS_calls':0,'auxiliary_trees_enumerated':0,'coefficient_searches':0,
      'automatic_successor_campaigns':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'BN05_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'BN05_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
