"""Final integrity and claim-scope manifest for roadmap step #1 only."""
import json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('DO_RESEARCH_REBOOT/M3_S3P01');OUT=BASE/'manifest.json';ROOT=Path.cwd()
REPORT="DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_S3P01_CORE3_SINGLETON_PORT.md"
def native(rel):
    p=str(ROOT/rel)
    return Path('\\\\?\\'+p) if os.name=='nt' else Path(p)
def fp(rel):
    b=native(rel).read_bytes()
    return {'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def main():
    assert not OUT.exists()
    baseline=json.loads((BASE/'entry_baseline.json').read_text());assert len(baseline)==156
    for row in baseline:assert fp(row['path'])['sha256']==row['sha256'],row['path']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    branch=git('branch','--show-current');head=git('rev-parse','HEAD')
    assert branch=='coarse-double-branch' and head=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    remote=git('ls-remote','--heads','origin','coarse-double-branch').split()
    assert remote==[head,'refs/heads/coarse-double-branch']
    new=set(git('ls-files','--others','--exclude-standard').splitlines())-{r['path'] for r in baseline}
    assert all(p==REPORT or p.startswith(BASE.as_posix()+'/') for p in new)
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in new)
    cert=json.loads((BASE/'core3_certificate.json').read_text())
    audit=json.loads((BASE/'audit_results.json').read_text())
    ctrl=json.loads((BASE/'original_core3_controls.json').read_text())
    wrong=json.loads((BASE/'wrong_inventory_controls.json').read_text())
    assert cert['status']==audit['status']==ctrl['status']==wrong['status']=='COMPLETE'
    assert cert['new_low_edges']==audit['new_edges_regenerated_and_old_images_checked']==239010
    assert cert['joint_nodes']==481562 and cert['combined_low_edges']==2874573
    assert audit['old_G0P01_states_unchanged']==469346 and audit['minimum_new_residual']==0
    assert audit['original_low_roots_accepted']==16 and audit['original_high_roots_accepted']==1
    assert audit['wrong_inventory_roots_rejected']==4 and audit['closed_mixed_cycle_weight']==8
    assert cert['new_label_fit']==audit['new_label_fit']==False
    oldm=json.loads(Path('DO_RESEARCH_REBOOT/M3_G0P01/manifest.json').read_text(encoding='utf-8'))
    for row in oldm['dependencies']:assert fp(row['path'])['sha256']==row['sha256']
    deps=[r['path'] for r in oldm['dependencies']]
    deps += ['DO_RESEARCH_REBOOT/M3_G0P01/'+p for p in (
       'manifest.json','port_catalog.json','potential.bin','ordinary_a.bin','ordinary_b.bin','images.bin',
       'source.bin','destination.bin','weights.bin','refinement_certificate.json','audit_results.json',
       'certify_refinement.py','port_potential.py','original_port_controls.py')]
    deps += [r['path'] for r in oldm['files_excluding_this_manifest'] if r['path'].endswith('.md')]
    deps=list(dict.fromkeys(deps))
    files=[fp(p) for p in sorted(new) if p!=OUT.as_posix()]
    result={'campaign':'IAGS-11G-S03-M3-S3P01','completed_utc':datetime.now(timezone.utc).isoformat(),
      'status':'COMPLETE','outcome':'A, roadmap step #1 proved at registered fixed-sector singleton-port scope',
      'roadmap_step_completed':1,'roadmap_step2_executed':False,
      'branch':branch,'local_head':head,'remote_branch_ref':remote[1],'remote_branch_tip':remote[0],
      'tracked_tree_unchanged':True,'baseline_files_preserved':156,'new_paths_confined_to_authorized_scope':True,
      'no_bytecode_created':True,'SMT_solver_invoked':False,'new_label_fit':False,'backend_switched':False,
      'graph':'G_AF','bank25':25,
      'theorem':{'status':'PROVED—RESTRICTED DOMAIN','mu':341,'sigma':[1]+[0]*9,'region':'chi8',
        'new_port':'unique S3 leaf forced by visible S2/S4 bounds; no anonymous content',
        'observable_patterns':['root2 / right4 / RL port','root4 / left2 / LR port'],
        'A_witness_family':'physical A10 trees with S3 leaf hidden; also both S3 and gap0 leaves hidden; other cuts canonical at depth six',
        'tabulated_B_scope':'same canonical full B profiles as the inherited physical certificate',
        'low_scope':'all registered H1 and exposed-fringe Gamma1 H2 whole macros by commuting/fusion/normalization',
        'additional_scope':'arbitrary Gamma0 H2 by range/floor; arbitrary original chi8 high legs with SAME midpoint',
        'construction':'physical J evaluated on state-only S3 refinement followed by prior gap0 refinement; old fallback otherwise',
        'old_G0P01_values_preserved':True,'range':[-2,0],'psi_floor_preserved':True,
        'path_bound':'W>=Theta(last)-Theta(first)>=-2','fully_closed_walk_bound':'W>=0',
        'all_masks_or_signatures':False,'arbitrary_other_S_ports_covered':False,
        'arbitrary_other_coarse_boundary_ports_covered':False,'is_full_M3_theorem':False},
      'source_content_lemma':{'status':'PROVED at stated boundary/signature hypotheses',
        'port_interval':'[r2+1,r4)','hidden_S_exactly':[3],'all_anonymous_populations':0,
        'uses_private_inventory_as_observable':False,
        'source_mechanism':'visible child bounds + full S-order + exact S-cover + population conservation/compatibility'},
      'certificate':{'status':'FINITE-EXACT VERIFIED','filtered_S3_leaf_A10_trees':4862,
        'filtered_both_leaf_A10_trees':1430,'independent_insertion_completeness':True,
        'source_access_queries_per_scan':43615,'whole_tree_commutations':14845,
        'new_port_shadow_classes':54,'new_port_states':12216,'ordinary_states':481562,
        'old_G0P01_states_unchanged':469346,'new_H1_edges':224322,'new_H2_edges':14688,
        'new_low_edges':239010,'combined_low_edges':2874573,'minimum_new_residual':0,
        'old_extension_failures_repaired':6622,'cheap_H1_failures_repaired':6491,
        'negative_H1_failures_repaired':131,'original_low_roots_accepted':16,
        'original_high_roots_accepted':1,'wrong_inventory_roots_rejected':4,
        'full_states_intervals_and_midpoint_audited':True,'whole_macro_variants':4,
        'closed_mixed_control_weight':8,'both_core3_orientations_and_fringe_port_on_cycle':True},
      'entrypoints':{'finite_certificate':'certify_core3_v2.py','positive_original_controls':'original_core3_controls.py',
         'wrong_inventory_controls':'reject_wrong_inventory_v2.py','independent_audit':'audit_results.py',
         'potential':'core3_potential.py','integrity':'write_manifest.py'},
      'implementation_provenance':{'preserved_failed_revisions':['certify_core3.py','reject_wrong_inventory.py'],
         'corrections':['typed ordinary-root filter','compiler import paths'],
         'mathematical_refinement_or_potential_failure':False,'registered_domain_changed':False,
         'result_files_overwritten':False},
      'ledger':{'M1':'OPEN','M2':'PROVED—UNIVERSAL (inherited)','M3':'OPEN','Step03':'OPEN','Step04':'UNAUTHORIZED',
         'restricted_CoarseDouble':'OPEN','DynamicOptimality':'OPEN','negative_mixed_cycles_certified':0},
      'resources':{'diagnostic_states':481562,'combined_diagnostic_edges':2874573,'original_low_DAG_nodes':1400081,
         'original_high_DAG_nodes':53455,'successful_finite_CPU_seconds':cert['cpu_seconds'],
         'positive_original_CPU_seconds':ctrl['cpu_seconds'],'negative_original_CPU_seconds':wrong['cpu_seconds'],
         'independent_finite_CPU_seconds':audit['finite_audit_CPU_seconds'],
         'independent_original_CPU_seconds':audit['original_audit_CPU_seconds'],
         'source_access_queries_including_preserved_failed_pass_upper_bound':130845,
         'all_completed_phases_below_registered_caps':True},
      'files_excluding_this_manifest':files,'dependencies':[fp(p) for p in deps],'entry_baseline':baseline}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
    saved=json.loads(OUT.read_text(encoding='utf-8'))
    for row in saved['files_excluding_this_manifest']+baseline:assert fp(row['path'])['sha256']==row['sha256']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    print(json.dumps({'status':'COMPLETE','roadmap_step_completed':1,'roadmap_step2_executed':False,
      'old_files_preserved':156,'new_artifacts_including_manifest':len(files)+1,'dependencies_hashed':len(deps),
      'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),'tracked_tree_unchanged':True,
      'remote_tip':head,'new_low_edges':239010,'new_label_fit':False,'M3':'OPEN'}),flush=True)
if __name__=='__main__':main()

