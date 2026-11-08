"""Preserve all prior evidence and pin the deterministic single-fringe-port certificate."""
import json,hashlib,subprocess,os
from pathlib import Path
from datetime import datetime,timezone
BASE=Path('DO_RESEARCH_REBOOT/M3_G0P01');OUT=BASE/'manifest.json';ROOT=Path.cwd()
REPORT="DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11G_FINAL_CLOSURE/STEP03_UNIVERSAL_POTENTIAL_CERTIFICATE/IAGS_WSIGN02A_ZERO_COST_IMPOSSIBILITY/IAGS_11G_S03_M3_G0P01_SINGLE_FRINGE_PORT_REFINEMENT.md"
def physical(rel):
    p=str(ROOT/rel)
    return Path('\\\\?\\'+p) if os.name=='nt' else Path(p)
def fp(rel):
    b=physical(rel).read_bytes()
    return {'path':rel,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
def main():
    assert not OUT.exists()
    baseline=json.loads((BASE/'entry_baseline.json').read_text());assert len(baseline)==131
    for row in baseline:assert fp(row['path'])['sha256']==row['sha256'],row['path']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    branch=git('branch','--show-current');head=git('rev-parse','HEAD')
    assert branch=='coarse-double-branch' and head=='fea2a25b05e97f726b6e1891cebb12c4cfca821a'
    remote=git('ls-remote','--heads','origin','coarse-double-branch').split()
    assert remote==[head,'refs/heads/coarse-double-branch']
    new=set(git('ls-files','--others','--exclude-standard').splitlines())-{r['path'] for r in baseline}
    assert all(p==REPORT or p.startswith(BASE.as_posix()+'/') for p in new)
    assert not any('__pycache__' in p or p.endswith('.pyc') for p in new)
    cert=json.loads((BASE/'refinement_certificate.json').read_text())
    audit=json.loads((BASE/'audit_results.json').read_text())
    catalog=json.loads((BASE/'port_catalog.json').read_text())
    assert cert['status']==audit['status']=='COMPLETE' and cert['new_label_fit']==False
    assert cert['new_interface_edges']==audit['new_edges_independently_regenerated_and_image_checked']==719976
    assert catalog['nodes']==469346 and catalog['combined_edges']==2635563
    assert audit['old_interface_failures_repaired']==5568 and audit['cheap_interface_failures_repaired']==5544
    assert audit['old_physical_nodes_unchanged']==342796 and audit['minimum_new_residual']==0
    oldm=json.loads(Path('DO_RESEARCH_REBOOT/M3_H1F01/manifest.json').read_text(encoding='utf-8'))
    for row in oldm['dependencies']:assert fp(row['path'])['sha256']==row['sha256']
    deps=[r['path'] for r in oldm['dependencies']]
    deps += ['DO_RESEARCH_REBOOT/M3_H1F01/'+p for p in (
        'manifest.json','graph_catalog.json','potential.bin','offsets.bin','targets.bin','weights.bin','meta.bin',
        'ordinary_a.bin','ordinary_b.bin','cheap_census.json','edge_audit.json','original_audit.json',
        'one_gap_potential.py','build_fragment.py')]
    deps += ['DO_RESEARCH_REBOOT/M3_H2R01/original_h2_controls.py',
             'DO_RESEARCH_REBOOT/M3_FRC01/verify_original_compensation.py']
    deps=list(dict.fromkeys(deps))
    files=[fp(p) for p in sorted(new) if p!=OUT.as_posix()]
    result={'campaign':'IAGS-11G-S03-M3-G0P01','completed_utc':datetime.now(timezone.utc).isoformat(),
      'status':'COMPLETE','outcome':'A, deterministic fringe-leaf port refinement at registered scope',
      'branch':branch,'local_head':head,'remote_branch_ref':remote[1],'remote_branch_tip':remote[0],
      'tracked_tree_unchanged':True,'baseline_files_preserved':131,'new_paths_confined_to_authorized_scope':True,
      'no_bytecode_created':True,'SMT_solver_invoked':False,'new_potential_fit':False,
      'backend_switched':False,'graph':'G_AF','bank25':25,
      'theorem':{'status':'PROVED—RESTRICTED DOMAIN','mu':341,'sigma':[1]+[0]*9,'region':'chi8',
        'new_A_witness_family':'every core A9 tree, gap0 singleton fringe leaf hidden as one port; no S keys in this port; other prefix cuts canonical at depth six',
        'new_H1_scope':'unit-charge marked core accesses and full H1 macros by inherited fusion, including entering/leaving the observed leaf-port shadow',
        'H2_scope':'old physical Gamma1 class unchanged; arbitrary Gamma0 by range/floor',
        'high_scope':'all original chi8 OM/MO legs, SAME midpoint, via range',
        'construction':'K(s)=J(rho(alpha_s),mu_s,b_s,sigma_s) on two deterministic port patterns; old evaluation otherwise',
        'range':[-2,0],'psi_floor_preserved':True,'old_physical_values_unchanged':True,
        'path_bound':'W>=Theta(last)-Theta(first)>=-2','fully_closed_walk_bound':'W>=0',
        'all_masks_or_signatures':False,'arbitrary_S_containing_ports_covered':False,
        'noncanonical_unused_alpha_fields_covered':False,'is_full_M3_theorem':False},
      'certificate':{'status':'FINITE-EXACT VERIFIED','core_A_trees':4862,'source_access_queries_per_complete_scan':24310,
        'whole_tree_commutations':8634,'new_port_shadow_classes':256,'joint_nodes':469346,
        'new_port_nodes':126550,'retained_old_physical_nodes':342796,'new_low_interfaces':719976,
        'combined_low_edges':2635563,'physical_to_port_edges':187256,'port_to_physical_edges':263762,
        'port_to_port_edges':268958,'old_interface_failures_repaired':5568,'cheap_interface_failures_repaired':5544,
        'negative_H1_interface_failures_repaired':24,'minimum_new_residual':0,
        'full_original_low_roots':12,'full_original_high_roots':2,'full_original_state_and_midpoint_audit':True,
        'closed_mixed_control_weights':[4,8],'observed_port_at_all_ordinary_vertices_in_weight8_cycle':True},
      'inherited_physical_certificate':{'edges':1915587,'not_fully_rerun':True,
        'all_inherited_file_hashes_preserved':True,'new_edge_CSR_images_individually_checked':True},
      'ledger':{'M1':'OPEN','M2':'PROVED—UNIVERSAL (inherited)','M3':'OPEN','Step03':'OPEN','Step04':'UNAUTHORIZED',
        'restricted_CoarseDouble':'OPEN','DynamicOptimality':'OPEN','negative_mixed_cycles_certified':0},
      'next_proposed_target':{'description':'unmarked core3 singleton leaf port fixed by visible core2/core4 interval bounds',
        'status':'PROPOSED, NOT EXECUTED'},
      'resources':{'diagnostic_states':469346,'combined_diagnostic_edges':2635563,
        'source_access_queries_both_scans':48620,'all_registered_CPU_caps_passed':True,
        'finite_certificate_CPU_seconds':cert['cpu_seconds'],
        'finite_audit_CPU_seconds':audit['finite_audit_CPU_seconds'],
        'original_audit_CPU_seconds':audit['original_audit_CPU_seconds']},
      'files_excluding_this_manifest':files,'dependencies':[fp(p) for p in deps],'entry_baseline':baseline}
    with OUT.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2,ensure_ascii=False)
    saved=json.loads(OUT.read_text(encoding='utf-8'))
    for row in saved['files_excluding_this_manifest']+baseline:assert fp(row['path'])['sha256']==row['sha256']
    assert not git('diff','--name-only') and not git('diff','--cached','--name-only')
    print(json.dumps({'status':'COMPLETE','old_files_preserved':131,'new_artifacts_including_manifest':len(files)+1,
      'dependencies_hashed':len(deps),'manifest_sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
      'tracked_tree_unchanged':True,'remote_tip':head,'M3':'OPEN','new_interface_edges':719976,
      'new_label_fit':False}),flush=True)
if __name__=='__main__':main()

