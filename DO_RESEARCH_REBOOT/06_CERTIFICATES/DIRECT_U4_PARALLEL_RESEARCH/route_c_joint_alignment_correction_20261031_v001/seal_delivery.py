"""Append-only preservation and status seal for the joint correction."""
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
    assert a['status']=='PASS' and a['certificate_sha256']==sha(OUT/'joint_alignment_certificate.json')
    assert sha(OUT/'JA00_FOUR_RULE_GATE.md')==e['gate_sha256']
    changed=[p for p,h in e['files'].items() if sha(ROOT/p)!=h]
    stage=ROOT/'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE'
    now=sorted(p.relative_to(ROOT).as_posix() for p in stage.rglob('*') if p.is_file())
    assert not changed and now==sorted(e['stage11g_all_files'])
    git=lambda *args:subprocess.check_output(['git','-C',str(ROOT),*args]).decode().strip()
    head=git('rev-parse','HEAD');branch=git('branch','--show-current');tracked=git('status','--porcelain=v1','--untracked-files=no')
    assert head==e['head'] and branch==e['branch'] and not tracked
    save('proof_status_ledger.json',{'date':'2026-10-31','results':[
      {'claim':'Explicit nonnegative unbounded joint R_joint=mu_r times different-root indicator','status':'SOURCE DEFINITION','source':'JA01_JOINT_CONSTRUCTION_AND_PARTIAL_LAWS.md'},
      {'claim':'H DELETE bound when source roots differ, and root-no-op case','status':'PROVED—RESTRICTED DOMAIN','proof':'JA01_JOINT_CONSTRUCTION_AND_PARTIAL_LAWS.md'},
      {'claim':'Registered all-size drift/zero-double repairs, opposite vines and arbitrary-fringe whole helpers for H','status':'PROVED—RESTRICTED DOMAIN','proof':'JA01_JOINT_CONSTRUCTION_AND_PARTIAL_LAWS.md'},
      {'claim':'Universal DELETE bound for H','status':'REFUTED—EXACT','proof':'JA02_EQUAL_ROOT_DELETE_AND_CLASS_OBSTRUCTION.md','counterexample':{'n':6,'a':1,'q':0,'H_source':1,'H_destination':5,'budget':2}},
      {'claim':'A nonnegative joint R vanishing on every equal-root pair can satisfy full DELETE for P+R','status':'REFUTED—EXACT','proof':'JA02_EQUAL_ROOT_DELETE_AND_CLASS_OBSTRUCTION.md','qualification':'does not exclude signed R or R(A,A)=0 alone'},
      {'claim':'Seven controls/reflections, inherited local P duals and physical paired closure','status':'FINITE-EXACT','certificate':'joint_alignment_certificate.json','audit':'independent_audit.json'},
      {'claim':'Full universal root-conditioned B q-law for H','status':'OPEN','qualification':'not established or refuted in this run; stopped after DELETE refutation'},
      {'claim':'Explicit unbounded joint correction satisfying both universal bounds','status':'OPEN'},
      {'claim':'Universal Coarse-Double','status':'OPEN'}],
      'before':'Scalar metric envelopes and scalar B-maximum normalizations refuted; generic joint correction open',
      'result':'Joint correction passes old controls, fails equal-root DELETE; nonnegative equal-root-zero class excluded',
      'after':'Generic joint correction and CD remain open',
      'original_load_bearing_obligations_discharged':[],'new_assumptions_for_original_theorem':[],
      'net_full_original_proof_advancement':0,'strategy_review':'JA03_STRATEGY_REVIEW.md','next_automatic_campaign':None})
    links=0
    for p in OUT.glob('JA*.md'):
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
      'independent_inherited_dual_joint_and_source_audit':'PASS','all_size_proof_verification':'written interval/matching argument, not finite extrapolation',
      'written_gate_hash_unchanged':True,'report_links_checked':links,'finite_potential_fits':0,
      'matching_solver_calls':0,'new_BFS_calls':0,'new_pair_graphs':0,'new_metric_graphs':0,'auxiliary_trees_enumerated':0,
      'automatic_successor_campaigns':0,'original_obligations_discharged':[],'full_original_proof_advancement':0}
    save('final_integrity.json',result)
    for p in OUT.glob('*.json'):json.loads(p.read_text(encoding='utf-8'))
    files={p.name:sha(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='delivery_manifest.json'}
    save('delivery_manifest.json',{'date':'2026-10-31','hash_algorithm':'SHA256','files':files,'exclusion':'self hash excluded','final_report':'JA04_FINAL_REPORT.md'})
    print(json.dumps({'status':'PASS','source_pins_unchanged':len(e['files']),'Stage11G_files_unchanged':len(now),
      'tracked_tree_clean':True,'report_links_checked':links,'delivery_files_hashed':len(files),'final_report':'JA04_FINAL_REPORT.md'},indent=2))
if __name__=='__main__':main()
